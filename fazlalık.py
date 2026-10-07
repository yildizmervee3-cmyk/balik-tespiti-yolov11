import os

# Labels klasörünüzün yolu
LABELS_DIR = r"C:\Users\yildi\PycharmProjects\PythonProject\Balik_Tespiti.v2i.yolov11\train\labels"

coklu_etiket_sayisi = 0
tek_etiket_sayisi = 0

if os.path.exists(LABELS_DIR):
    for file_name in os.listdir(LABELS_DIR):
        if file_name.endswith(".txt") and file_name != "classes.txt":
            file_path = os.path.join(LABELS_DIR, file_name)

            with open(file_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]

            if len(lines) > 1:
                coklu_etiket_sayisi += 1
            else:
                tek_etiket_sayisi += 1

    print("\n----------------------------------------")
    if coklu_etiket_sayisi > 0:
        print(f"VAR! Toplam {coklu_etiket_sayisi} adet dosyada birden fazla balık etiketlenmiş.")
        print(f"Sadece tek balık içeren dosya sayısı: {tek_etiket_sayisi}")
    else:
        print("YOK! Tüm görsellerde sadece tek bir balık etiketlenmiş.")
    print("----------------------------------------\n")
else:
    print(f"HATA: '{LABELS_DIR}' klasörü bulunamadı, lütfen klasör yolunu kontrol edin.")