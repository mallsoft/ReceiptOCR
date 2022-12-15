from PIL.Image import Image as ImageType
from PIL import Image
import concurrent.futures as cf
from pytesseract import image_to_string
import os
import json


def getImages(folder="Kvittering/Processed/"):
    return [(name, Image.open(folder+name)) for name in os.listdir(folder)]


def processImage(imageTup: tuple[str, ImageType]):
    name, img = imageTup
    return (name, image_to_string(img, lang="nor+eng", config="--psm 4"))


def processBatch(imageTups: list[tuple[str, ImageType]]):
    with cf.ProcessPoolExecutor(max_workers=12) as executor:
        print(f"processing {len(imageTups)} images ")
        receipts = []
        for future in [executor.submit(processImage, imageTup) for imageTup in imageTups]:
            receipts.append(future.result())
            print(f"-> {len(receipts)}/{len(imageTups)} completed",
                  end="\r", flush=True)

    print("\ndone")
    return receipts


def toJsonFile(data: list, fileName="ocr_results.json"):
    with open(fileName, "w") as outfile:
        print(f"writing to {fileName}")
        json.dump(data, outfile)
    print(f"saved to {fileName}")


def main():
    print("ocr running")
    receipts = processBatch(getImages())
    toJsonFile(receipts)
    print("ocr complete")


if __name__ == "__main__":
    main()
    # print(processBatch(getImages()[0:5]))
