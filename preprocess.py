from PIL.Image import Image as ImageType
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import os


def imageCrop(img, boxCrop=(550, 0, 1700, 3250)):
    return img.crop(boxCrop)


def enhanceImage(img: ImageType):
    img = img.convert("L")

    img = img.filter(ImageFilter.MinFilter(size=3))
    img = ImageEnhance.Brightness(img).enhance(1.5)
    img = ImageEnhance.Contrast(img).enhance(1.5)
    img = ImageEnhance.Sharpness(img).enhance(1.1)

    img = img.point(lambda p: p * 1.1 if p > 220 else p * 0.8)
    # mono
    # img = img.convert('1')

    return img


def preprocess(img: ImageType):

    # apply whatever thransforms are in exif
    img = ImageOps.exif_transpose(img)

    img = imageCrop(img)
    img = enhanceImage(img)

    # add border
    img = ImageOps.expand(img, border=100, fill='white')

    return img


def batch(in_path="Kvittering/Camera/",
          out_path="Kvittering/Processed/"):
    filesToProcess = os.listdir(in_path)
    for i, name in enumerate(filesToProcess):

        img = Image.open(in_path+name)

        img = preprocess(img)

        img.save(out_path + f"p_{i}.jpg")

        print(f"-> ({i+1}/{len(filesToProcess)}) processed -> {name}\r",
              end="\r", flush=True)
    print("\n...batch preprocess completed...")


def main():
    print("preprocess starting")
    batch()
    print("preprocess complete")


if __name__ == '__main__':
    main()
    # preprocess(Image.open("test_raw2.jpg")).show()
