from PIL import Image, ImageFilter
import lib
import sys


modes = {
    "pen_outline": lib.Settings(
        (2, 3),
        15,
        0.95,
        False,
        [
            lib.set_black_or_white,
            # lib.invert_pixel
        ]
    ),
    "b&w": lib.Settings(
        (1, 2),
        5,
        0.82,
        False,
        [
            # lib.luminance_pixel,
            lib.set_black_or_white,
        ]
    )
}


def main():

    settings = modes["pen_outline"]

    try:
        filename = sys.argv[1]
    except IndexError:
        print("Fatal: Please provide a file as argument")
        exit()

    try:
        image = Image.open(filename)
    except FileNotFoundError:
        print("Fatal: File not found")
        exit()

    ret = lib.dog(image, settings)

    for f in settings.function_list:
        ret = lib.map_over_image(ret, settings, f)

    if settings.coloured:
        ret = lib.colour(image.filter(
            ImageFilter.GaussianBlur(4)), ret, settings)

    ret.show()

    if (savename := input("Filename to save? or 'n' to discard")) != "n":
        ret.save(savename + "." + filename.split('.')[-1])


if __name__ == "__main__":
    main()
