from PIL import Image
from pytesseract import image_to_string
import os
import json
import concurrent.futures as cf


def getImages(folder="Kvittering/Processed/"):
    return [Image.open(folder+name) for name in os.listdir(folder)]


def processImage(img: Image):
    return image_to_string(img, lang="nor+eng", config="--psm 4")


def toJsonFile(data: list, fileName="ocr_results.json"):
    with open(fileName, "w") as outfile:
        print(f"writing to {fileName}")
        json.dump(data, outfile)
    print(f"saved to {fileName}")


def processBatch(images):
    with cf.ProcessPoolExecutor(max_workers=12) as executor:
        print(f"processing {len(images)} images ")
        futures = [executor.submit(processImage, image)
                   for image in images]
        texts = []
        for future in cf.as_completed(futures):
            texts.append(future.result())
            print(f"-> {len(texts)}/{len(images)} completed",
                  end="\r", flush=True)
    print("\ndone")
    return texts


def main():
    print("ocr running")
    images_to_ocr = getImages()
    texts = processBatch(images_to_ocr)
    toJsonFile(texts)
    print("ocr complete")


if __name__ == "__main__":
    main()
