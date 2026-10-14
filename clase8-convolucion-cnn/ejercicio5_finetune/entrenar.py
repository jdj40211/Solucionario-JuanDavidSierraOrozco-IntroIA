"""Entrena y evalua las tres variantes del Ejercicio 5 y guarda resultados.json.

  baseline : yolov8n-seg.pt tal cual (80 clases COCO), sin entrenar
  completo : fine-tuning de toda la red (freeze=None)
  congelado: fine-tuning con las 10 primeras capas (el backbone) congeladas (freeze=10)

Uso: python entrenar.py --data DATASET/data.yaml --runs DIR_RUNS --out CARPETA_SALIDA [--epochs 40]
"""
import argparse
import json
import shutil
from pathlib import Path

from ultralytics import YOLO


def metricas(m):
    s = m.seg
    return {"mAP50": float(s.map50), "mAP50-95": float(s.map),
            "P": float(s.mp), "R": float(s.mr),
            "mAP50-95_por_clase": [float(x) for x in s.maps]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--runs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--device", default="mps")
    a = ap.parse_args()
    out = Path(a.out)
    (out / "pesos").mkdir(parents=True, exist_ok=True)
    res = {}
    kw = dict(data=a.data, split="test", imgsz=640, device=a.device, workers=0, verbose=False, plots=False)

    # baseline: como no conoce "labrador"/"gato", se mide "encuentra al perro" sin importar la clase (single_cls)
    base = YOLO("yolov8n-seg.pt")
    res["baseline_agnostico"] = metricas(base.val(single_cls=True, project=a.runs, name="val_base", exist_ok=True, **kw))

    for nombre, freeze in [("completo", None), ("congelado", 10)]:
        m = YOLO("yolov8n-seg.pt")
        m.train(data=a.data, epochs=a.epochs, imgsz=640, batch=16, device=a.device, workers=0, seed=0,
                freeze=freeze, project=a.runs, name=nombre, exist_ok=True, plots=False, verbose=False)
        best = Path(a.runs) / nombre / "weights" / "best.pt"
        shutil.copy(best, out / "pesos" / f"{nombre}.pt")
        shutil.copy(Path(a.runs) / nombre / "results.csv", out / f"curvas_{nombre}.csv")
        mod = YOLO(str(best))
        res[nombre] = metricas(mod.val(project=a.runs, name=f"val_{nombre}", exist_ok=True, **kw))
        res[nombre + "_agnostico"] = metricas(mod.val(single_cls=True, project=a.runs, name=f"val_{nombre}_ag", exist_ok=True, **kw))
        (out / "resultados.json").write_text(json.dumps(res, indent=1))
    (out / "resultados.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
