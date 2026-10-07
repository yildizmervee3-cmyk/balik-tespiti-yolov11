import os
import yaml

# Yollar
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
DATASET_PATH = os.path.join(DESKTOP_PATH, "Baliklar_YOLO_Dataset")

# Görselde açık olan classes.txt dosyasının yolu
CLASSES_FILE = os.path.join(DESKTOP_PATH, "Baliklar_Siniflandirilmis", "classes.txt")

# Eğer yoksa dataset klasöründekine bak
if not os.path.exists(CLASSES_FILE):
    CLASSES_FILE = os.path.join(DATASET_PATH, "classes.txt")

def make_yaml():
    if not os.path.exists(CLASSES_FILE):
        print(f"HATA: '{CLASSES_FILE}' bulunamadı!")
        return

    # classes.txt dosyasını satır satır tam sırasıyla okuyoruz
    with open(CLASSES_FILE, "r", encoding="utf-8") as f:
        classes = [line.strip() for line in f.readlines() if line.strip()]

    # Indeksleri (0, 1, 2...) isimlerle eşliyoruz
    names_dict = {i: cls for i, cls in enumerate(classes)}

    data = {
        'path': DATASET_PATH.replace('\\', '/'),
        'train': 'train/images',
        'val': 'val/images',
        'test': 'test/images',
        'names': names_dict
    }

    yaml_path = os.path.join(os.getcwd(), "data.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

    print(f"Harika! Toplam {len(classes)} sınıf 'classes.txt' sırasına göre 'data.yaml' olarak yazıldı.")

if __name__ == "__main__":
    make_yaml()