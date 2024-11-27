import os
import logging
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from moviepy.editor import AudioFileClip
from tqdm import tqdm

def setup_logging():
    """Logging ayarlarını yapılandır"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('conversion.log')
        ]
    )

def convert_file(input_file: Path, output_file: Path) -> tuple:
    """Tek bir dosyayı dönüştür"""
    try:
        audio_clip = AudioFileClip(str(input_file))
        audio_clip.write_audiofile(str(output_file), codec='mp3', logger=None)
        audio_clip.close()
        return (True, input_file.name, None)
    except Exception as e:
        return (False, input_file.name, str(e))

def main():
    # Klasör yollarını yapılandır
    input_folder = Path("path_of_webm_file")
    output_folder = Path("path_of_mp3_file")

    # Logging'i başlat
    setup_logging()
    logger = logging.getLogger(__name__)

    # Çıktı klasörünü oluştur
    output_folder.mkdir(parents=True, exist_ok=True)

    # Dönüştürülecek dosyaları bul
    webm_files = list(input_folder.glob("*.webm"))
    total_files = len(webm_files)

    if not webm_files:
        logger.warning("Dönüştürülecek .webm dosyası bulunamadı!")
        return

    logger.info(f"Toplam {total_files} adet .webm dosyası bulundu. Dönüştürme başlıyor...")

    # İşlemci sayısına göre paralel işleme havuzu oluştur
    with ProcessPoolExecutor() as executor:
        # Dönüştürme işlemlerini başlat
        futures = []
        for webm_file in webm_files:
            output_file = output_folder / f"{webm_file.stem}.mp3"
            futures.append(
                executor.submit(convert_file, webm_file, output_file)
            )

        # İlerleme çubuğu ile sonuçları takip et
        successful = 0
        failed = 0
        
        with tqdm(total=total_files, desc="Dönüştürülüyor") as pbar:
            for future in as_completed(futures):
                success, filename, error = future.result()
                if success:
                    successful += 1
                    logger.info(f"Başarılı: {filename}")
                else:
                    failed += 1
                    logger.error(f"Hata ({filename}): {error}")
                pbar.update(1)

    # Sonuçları göster
    logger.info(f"\nDönüştürme tamamlandı!")
    logger.info(f"Başarılı: {successful}")
    logger.info(f"Başarısız: {failed}")

if __name__ == "__main__":
    main()
