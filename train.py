from ultralytics import YOLO

if __name__ == '__main__':
    # YOLOv11 nano modelini yukluyoruz
    model = YOLO("yolo11n.pt")

    # Eğitimi 50 epoch olarak baslatiyoruz
    model.train(data="data.yaml", epochs=50, imgsz=640, batch=16)