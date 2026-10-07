 YOLOv11 ile Balık Tespiti ve Sınıflandırma Projesi

Bu proje, YOLOv11 nesne tespiti modelini kullanarak balık türlerinin tespiti ve sınıflandırılması amacıyla geliştirilmiştir.

 📁 Proje Yapısı

- `train.py`: YOLOv11 modelinin eğitimi için kullanılan ana script.
- `siniflandir.py`: Eğitilmiş model ile görseller üzerinde tespit ve sınıflandırma yapan kod.
- `dataset_split.py`: Veri setini Eğitim (Train), Doğrulama (Validation) ve Test bölümlerine ayıran yapı.
- `create_yaml.py`: YOLO modelinin sınıf ve yol yapılandırma dosyasını (`data.yaml`) oluşturan script.
- `data.yaml`: Veri seti sınıflarını ve dosya yollarını tanımlayan yapılandırma dosyası.

 🛠️ Kullanılan Teknolojiler
- Python
- PyTorch
- Ultralytics (YOLOv11)
- Roboflow
