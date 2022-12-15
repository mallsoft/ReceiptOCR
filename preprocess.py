from PIL import Image, ImageOps
import os


def preprocess(img, x=550,
               y=0,
               right=1700,
               bottom=3250):

    # apply whatever thransforms are in exif
    img = ImageOps.exif_transpose(img)

    img = ImageOps.grayscale(img)
    img = ImageOps.autocontrast(img)

    # we don't need the whole thing
    img = img.crop((x, y, right, bottom))

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
    # preprocess(Image.open("test_raw.jpg")).show()
    batch()
    print("preprocess complete")


if __name__ == '__main__':
    main()
