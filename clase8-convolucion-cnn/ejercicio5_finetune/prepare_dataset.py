"""Construye el dataset de segmentacion "labrador vs gato" (Ejercicio 5).

Pasos:
  1. Lee Stanford Dogs (espejo amaye15/stanford-dogs de Hugging Face, parquet).
  2. Elige todos los labradores y 8 candidatas de cada una de 30 razas distintas.
  3. Genera MASCARAS con yolov8m-seg preentrenado en COCO (clase 16 = dog). Son
     pseudo-etiquetas: Stanford Dogs solo trae etiqueta de raza y caja, no mascaras.
  4. Filtra las pseudo-etiquetas dudosas.
  5. Reparte 70/15/15 por IMAGEN de origen (antes de armar los collages, para no filtrar
     la misma foto entre train y test).
  6. Escribe el dataset en formato YOLO-seg: imagenes sueltas (640x640 con bordes grises)
     y collages 2x2 de cuatro perros de razas distintas.

Clases: 0 = labrador, 1 = gato (convencion de la practica: cualquier otro perro se llama "gato").

Uso:
    python prepare_dataset.py --parquet-dir DIR_CON_PARQUET --out DIR_SALIDA
"""
import argparse
import io
import json
import random
from pathlib import Path

import cv2
import numpy as np
import pyarrow.parquet as pq
from PIL import Image

LABRADOR = 67          # indice de "Labrador Retriever" en el ClassLabel de Stanford Dogs
COCO_DOG = 16
N_RAZAS_OTRAS = 30     # razas "gato"
CAND_POR_RAZA = 8      # candidatas por raza antes de filtrar
LADO = 640
SEED = 0


def leer_candidatas(carpeta, rng):
    """Devuelve lista de (raza_idx, nombre_raza, bytes_jpg) con todos los labradores y candidatas de otras razas."""
    archivos = sorted(Path(carpeta).glob("*.parquet"))
    nombres = None
    por_raza = {}
    for f in archivos:
        pf = pq.ParquetFile(f)
        if nombres is None:
            meta = json.loads(pf.schema_arrow.metadata[b"huggingface"])
            nombres = meta["info"]["features"]["label"]["names"]
        for lote in pf.iter_batches(batch_size=256):
            etiquetas = lote.column("label").to_pylist()
            imgs = lote.column("pixel_values").to_pylist()
            for e, im in zip(etiquetas, imgs):
                por_raza.setdefault(e, []).append(im["bytes"])
    otras = [i for i in range(len(nombres)) if i != LABRADOR]
    elegidas = otras[::4][:N_RAZAS_OTRAS]
    salida = [(LABRADOR, nombres[LABRADOR], b) for b in por_raza[LABRADOR]]
    for r in elegidas:
        lista = por_raza[r][:]
        rng.shuffle(lista)
        salida += [(r, nombres[r], b) for b in lista[:CAND_POR_RAZA]]
    return salida


def pseudo_etiquetar(candidatas, modelo_seg="yolov8m-seg.pt", device="mps"):
    """Mascara del perro principal con YOLOv8m-seg. Devuelve lista de dicts (solo las que pasan el filtro)."""
    from ultralytics import YOLO
    modelo = YOLO(modelo_seg)
    buenas, descartadas = [], 0
    for raza, nombre, jpg in candidatas:
        rgb = np.asarray(Image.open(io.BytesIO(jpg)).convert("RGB"))
        alto, ancho = rgb.shape[:2]
        r = modelo(rgb[..., ::-1], conf=0.08, retina_masks=True, device=device, verbose=False)[0]
        if r.masks is None:
            descartadas += 1
            continue
        perros = []
        for caja, m in zip(r.boxes, r.masks.data.cpu().numpy()):
            if int(caja.cls) == COCO_DOG:
                perros.append((float(caja.conf), m > 0.5))
        if not perros:
            descartadas += 1
            continue
        areas = [m.sum() / m.size for _, m in perros]
        k = int(np.argmax(areas))
        conf, mask = perros[k]
        otro_fuerte = any(a > 0.015 for j, a in enumerate(areas) if j != k)
        if conf < 0.5 or areas[k] < 0.06 or otro_fuerte:
            descartadas += 1
            continue
        contornos, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = max(contornos, key=cv2.contourArea)
        c = cv2.approxPolyDP(c, 0.003 * cv2.arcLength(c, True), True)[:, 0, :].astype(float)
        if len(c) < 6:
            descartadas += 1
            continue
        c[:, 0] /= ancho
        c[:, 1] /= alto
        buenas.append({"raza": raza, "nombre": nombre, "cls": 0 if raza == LABRADOR else 1,
                       "conf": conf, "area": float(areas[k]), "poly": c.tolist(), "jpg": jpg})
    return buenas, descartadas


def letterbox(rgb, poly, lado):
    """Reescala la imagen a un cuadrado de `lado` con bordes grises y transforma el poligono (normalizado) al cuadrado."""
    alto, ancho = rgb.shape[:2]
    s = lado / max(alto, ancho)
    nw, nh = round(ancho * s), round(alto * s)
    lienzo = np.full((lado, lado, 3), 114, np.uint8)
    ox, oy = (lado - nw) // 2, (lado - nh) // 2
    lienzo[oy:oy + nh, ox:ox + nw] = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_AREA)
    p = np.array(poly)
    p = np.stack([(p[:, 0] * nw + ox) / lado, (p[:, 1] * nh + oy) / lado], 1)
    return lienzo, p


def escribir(carpeta, split, nombre, img, instancias):
    (carpeta / "images" / split).mkdir(parents=True, exist_ok=True)
    (carpeta / "labels" / split).mkdir(parents=True, exist_ok=True)
    Image.fromarray(img).save(carpeta / "images" / split / f"{nombre}.jpg", quality=92)
    lineas = []
    for cls, p in instancias:
        coords = " ".join(f"{x:.5f} {y:.5f}" for x, y in np.clip(p, 0, 1))
        lineas.append(f"{cls} {coords}")
    (carpeta / "labels" / split / f"{nombre}.txt").write_text("\n".join(lineas) + "\n")


def construir(buenas, salida, rng, n_collages_por_img=0.45):
    salida = Path(salida)
    idx = list(range(len(buenas)))
    rng.shuffle(idx)
    # reparto estratificado por clase
    split_de = {}
    for cls in (0, 1):
        sub = [i for i in idx if buenas[i]["cls"] == cls]
        n = len(sub)
        a, b = round(0.70 * n), round(0.85 * n)
        for j, i in enumerate(sub):
            split_de[i] = "train" if j < a else ("val" if j < b else "test")
    conteo = {}
    for split in ("train", "val", "test"):
        miembros = [i for i in idx if split_de[i] == split]
        decod = {i: np.asarray(Image.open(io.BytesIO(buenas[i]["jpg"])).convert("RGB")) for i in miembros}
        # imagenes sueltas
        for i in miembros:
            img, p = letterbox(decod[i], buenas[i]["poly"], LADO)
            escribir(salida, split, f"{split}_solo_{i:04d}", img, [(buenas[i]["cls"], p)])
        # collages 2x2: cuatro perros de razas distintas, al menos un labrador en la mitad
        n_col = round(len(miembros) * n_collages_por_img)
        labs = [i for i in miembros if buenas[i]["cls"] == 0]
        otros = [i for i in miembros if buenas[i]["cls"] == 1]
        for k in range(n_col):
            elegir = []
            if k % 2 == 0 and labs:
                elegir.append(rng.choice(labs))
            while len(elegir) < 4:
                i = rng.choice(miembros)
                if i not in elegir and all(buenas[i]["raza"] != buenas[j]["raza"] for j in elegir):
                    elegir.append(i)
            rng.shuffle(elegir)
            lienzo = np.zeros((LADO, LADO, 3), np.uint8)
            inst = []
            mitad = LADO // 2
            for pos, i in enumerate(elegir):
                celda, p = letterbox(decod[i], buenas[i]["poly"], mitad)
                fx, fy = (pos % 2) * mitad, (pos // 2) * mitad
                lienzo[fy:fy + mitad, fx:fx + mitad] = celda
                p = np.stack([(p[:, 0] * mitad + fx) / LADO, (p[:, 1] * mitad + fy) / LADO], 1)
                inst.append((buenas[i]["cls"], p))
            escribir(salida, split, f"{split}_collage_{k:04d}", lienzo, inst)
        conteo[split] = {"solo": len(miembros), "collages": n_col,
                         "labradores": len(labs), "gatos": len(otros)}
    (salida / "data.yaml").write_text(
        f"path: {salida.resolve()}\ntrain: images/train\nval: images/val\ntest: images/test\n"
        "names:\n  0: labrador\n  1: gato\n")
    return conteo, split_de


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parquet-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--device", default="mps")
    a = ap.parse_args()
    rng = random.Random(SEED)
    cand = leer_candidatas(a.parquet_dir, rng)
    print("candidatas:", len(cand))
    buenas, desc = pseudo_etiquetar(cand, device=a.device)
    print("aceptadas:", len(buenas), "descartadas:", desc)
    conteo, _ = construir(buenas, a.out, rng)
    razas = sorted({b["nombre"] for b in buenas if b["cls"] == 1})
    resumen = {"aceptadas": len(buenas), "descartadas": desc,
               "labradores": sum(b["cls"] == 0 for b in buenas),
               "gatos": sum(b["cls"] == 1 for b in buenas),
               "razas_gato": razas, "splits": conteo}
    (Path(a.out) / "resumen.json").write_text(json.dumps(resumen, indent=1, ensure_ascii=False))
    print(json.dumps(resumen, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
