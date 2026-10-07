import os
import shutil
import random

# --- YOLLAR ---
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
SOURCE_DIR = os.path.join(DESKTOP_PATH, "Baliklar_Siniflandirilmis")
OUTPUT_DIR = os.path.join(DESKTOP_PATH, "Baliklar_YOLO_Dataset")

# Oranlar (%70 Train, %15 Val, %15 Test)
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

# Hedef 6 balık sınıfı
CLASSES = ['BIB', 'HKE', 'HOM', 'MAC', 'MEG', 'MUR']

def split_dataset():
    if not os.path.exists(SOURCE_DIR):
        print(f"HATA: '{SOURCE_DIR}' klasörü bulunamadı!")
        return

    # YOLO için Hedef Klasör Yapısını Oluştur (train/val/test altında images ve labels)
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(OUTPUT_DIR, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(OUTPUT_DIR, split, 'labels'), exist_ok=True)

    # classes.txt dosyasını kopyala
    src_classes = os.path.join(SOURCE_DIR, "classes.txt")
    if os.path.exists(src_classes):
        shutil.copy(src_classes, os.path.join(OUTPUT_DIR, "classes.txt"))

    print("Veriler her sınıfa özel %70-%15-%15 oranında ayrılıyor...\n")

    # Her sınıf klasörünü tek tek dolaş ve kendi içinde böl
    for cls in CLASSES:
        cls_dir = os.path.join(SOURCE_DIR, cls)
        if not os.path.exists(cls_dir):
            continue

        # Sadece resim dosyalarını al
        images = [f for f in os.listdir(cls_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        random.shuffle(images)

        total_imgs = len(images)
        train_end = int(total_imgs * TRAIN_RATIO)
        val_end = train_end + int(total_imgs * VAL_RATIO)

        train_imgs = images[:train_end]
        val_imgs = images[train_end:val_end]
        test_imgs = images[val_end:]

        splits = {'train': train_imgs, 'val': val_imgs, 'test': test_imgs}

        for split_name, img_list in splits.items():
            for img_name in img_list:
                base_name = os.path.splitext(img_name)[0]
                label_name = base_name + ".txt"

                src_img = os.path.join(cls_dir, img_name)
                src_label = os.path.join(cls_dir, label_name)

                dst_img = os.path.join(OUTPUT_DIR, split_name, 'images', img_name)
                dst_label = os.path.join(OUTPUT_DIR, split_name, 'labels', label_name)

                # Resim ve Label dosyasını taşı
                shutil.copy(src_img, dst_img)
                if os.path.exists(src_label):
                    shutil.copy(src_label, dst_label)

        print(f"[{cls}] Sınıfı -> Toplam: {total_imgs} | Train: {len(train_imgs)} | Val: {len(val_imgs)} | Test: {len(test_imgs)}")

    print(f"\nTüm sınıflar birleştirildi! Yeni Veri Seti Konumu: {OUTPUT_DIR}")

if __name__ == "__main__":
    random.seed(42)  # Tekrarlanabilir rastgele dağılım için
    split_dataset()