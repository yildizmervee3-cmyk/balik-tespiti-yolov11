import os
import shutil

# --- DOSYA YOLLARI ---
DATASET_PATH = "Balik_Tespiti.v2i.yolov11"

# Çıktının kaydedileceği Masaüstü konumu
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
OUTPUT_PATH = os.path.join(DESKTOP_PATH, "Baliklar_Siniflandirilmis")

# 1. HOCANIZIN İSTEDİĞİ 113 SINIFLI TAM LİSTE (classes.txt İÇİN)
FULL_CLASS_NAMES = [
    "Cod", "Garfish", "Mackrel", "Perch", "Rainbow_trout", "Salmon", "Sardinella_aurita",
    "Pagellus_acarne", "Upeneus_moluccensis", "Nemipterus_randalli", "Pomadasys_stridens",
    "Unknown", "Bream", "Brook_trout", "Common_carp", "Flounder", "Golden_trout",
    "Grayling", "Ide", "Lake_trout", "Pike", "Pikeperch", "Plaice", "River_trout",
    "Roach", "Rudd", "Saithe", "Sea_bass", "Sea_trout", "Sturgeon", "Turbot",
    "Baillons_wrasse", "Balpan_wrasse", "Bass", "Bib", "Black_goby", "Black_seabream",
    "Blackmouthed_dogfish", "Blonde_ray", "Blue_shark", "Brill", "Brown_crab",
    "Bull_huss", "Bull_rout", "Butterfish", "Coalfish", "Common_goby", "Common_skate",
    "Conger_eel", "Corkwing_wrasse", "Couchs_seabream", "Cuckoo_wrasse", "Dab",
    "Dover_sole", "Dragonet", "European_squid", "Five_bearded_rockling",
    "Four_bearded_rockling", "Freshwater_eel", "Giant_goby", "Gilthead_seabream",
    "Golden_grey_mullet", "Goldsinney_wrasse", "Greater_weever_fish", "Grey_gurnard",
    "Haddock", "Herring", "John_dory", "Lemon_sole", "Leopard_spotted_goby",
    "Lesser_spotted_dogfish", "Lesser_weever", "Ling", "Lobster", "Lumpsucker",
    "Northern_squid", "Pollack", "Poor_cod", "Red_gurnard", "Red_mullet",
    "Rock_cook_wrasse", "Rock_goby", "Sandeep", "Sardinella_Aurita", "Scad",
    "Sea_scorpion", "Shanny", "Shore_rockling", "Small_eyed_ray", "Smelt",
    "Smoothhound", "Spider_crab", "Spotted_ray", "Spurdog", "Starry_smoothound",
    "Stingray", "Thick_lipped_grey_mullet", "Thin_lipped_grey_mullet", "Thornback_ray",
    "Three_bearded_rockling", "Tompot_blenny", "Tope", "Tub_gurnard", "Undulate_ray",
    "Vivaporous_blenny", "Whiting", "Lobster_", "Crab", "Scallop", "Nephrop",
    "Hake", "Horse_mackerel", "Megrim"
]

# 2. ETİKETLERDEKİ (0,1,2,3,4,5) ID'LERİN GERÇEK BÖLÜNMÜŞ KLASÖR KARŞILIKLARI
TARGET_CLASSES = ['BIB', 'HKE', 'HOM', 'MAC', 'MEG', 'MUR']


def organize_dataset_fixed():
    if not os.path.exists(DATASET_PATH):
        print(f"HATA: '{DATASET_PATH}' klasoru projenizde bulunamadi!")
        return

    # Önceki hatalı klasörleri sil ve sıfırla
    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)

    os.makedirs(OUTPUT_PATH, exist_ok=True)

    # 1. ANA KLASÖRE 113 SINIFLI CLASSES.TXT DOSYASINI YAZ
    classes_file_path = os.path.join(OUTPUT_PATH, "classes.txt")
    with open(classes_file_path, "w", encoding="utf-8") as f:
        for name in FULL_CLASS_NAMES:
            f.write(f"{name}\n")

    # 2. SADECE 6 ANA GERÇEK BALIK KLASÖRÜNÜ VE ARKA PLAN KLASÖRÜNÜ OLUŞTUR
    for name in TARGET_CLASSES:
        os.makedirs(os.path.join(OUTPUT_PATH, name), exist_ok=True)

    ARKA_PLAN_DIR = os.path.join(OUTPUT_PATH, "ARKA_PLAN")

    processed_images = set()
    total_count = 0

    subfolders = ['train', 'valid', 'test']

    # 3. ETİKETLERİ VE RESİMLERİ 6 DOĞRU KLASÖRE DAĞIT
    for sub in subfolders:
        labels_dir = os.path.join(DATASET_PATH, sub, 'labels')
        images_dir = os.path.join(DATASET_PATH, sub, 'images')

        if not os.path.exists(labels_dir) or not os.path.exists(images_dir):
            continue

        for label_file in os.listdir(labels_dir):
            if not label_file.endswith('.txt') or label_file == 'classes.txt':
                continue

            label_path = os.path.join(labels_dir, label_file)

            with open(label_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                class_id = None
                if lines:
                    first_line = lines[0].strip().split()
                    if first_line:
                        class_id = int(first_line[0])

            # Etiketteki ID'ye göre doğru klasöre yönlendir (0->BIB, 1->HKE...)
            if class_id is not None and class_id < len(TARGET_CLASSES):
                target_class = TARGET_CLASSES[class_id]
            else:
                target_class = 'HOM'

            dest_dir = os.path.join(OUTPUT_PATH, target_class)

            base_name = os.path.splitext(label_file)[0]
            for ext in ['.jpg', '.png', '.jpeg', '.JPG', '.PNG']:
                img_name = base_name + ext
                img_path = os.path.join(images_dir, img_name)
                if os.path.exists(img_path):
                    shutil.copy(img_path, os.path.join(dest_dir, img_name))
                    shutil.copy(label_path, os.path.join(dest_dir, label_file))
                    processed_images.add(img_path)
                    total_count += 1
                    break

    # 4. ARKA PLAN RESİMLERİNİ AKTAR
    for sub in subfolders:
        images_dir = os.path.join(DATASET_PATH, sub, 'images')
        if not os.path.exists(images_dir):
            continue

        for img_name in os.listdir(images_dir):
            if any(img_name.endswith(ext) for ext in ['.jpg', '.png', '.jpeg', '.JPG', '.PNG']):
                img_path = os.path.join(images_dir, img_name)
                if img_path not in processed_images:
                    os.makedirs(ARKA_PLAN_DIR, exist_ok=True)
                    shutil.copy(img_path, os.path.join(ARKA_PLAN_DIR, img_name))
                    total_count += 1

    print(f"\nİŞLEM TAMAMLANDI!")
    print(f"113 sınıflı 'classes.txt' ana klasöre koyuldu.")
    print(f"Resimler doğru klasörlerine (BIB, HKE, HOM, MAC, MEG, MUR) ayrıldı.")


if __name__ == "__main__":
    organize_dataset_fixed()