from PIL import Image, ImageFilter


class Settings:
    def __init__(self, blur_radii: (int, int), luminosity_point: int, tau: float, coloured: bool, function_list):
        self.blur_radii = blur_radii
        self.function_list = function_list
        self.luminosity_point = luminosity_point
        self.tau = tau
        self.coloured = coloured


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

type Pixel = (int, int, int)


def pixel_subtract(a: Pixel, b: Pixel):
    return (
        abs(a[0] - b[0]),
        abs(a[1] - b[1]),
        abs(a[2] - b[2])
    )


def pixel_multiply(a: float, b: Pixel):
    return (
        round(a * b[0]),
        round(a * b[1]),
        round(a * b[2])
    )


def pixel_luminance(a: Pixel) -> int:
    (R, G, B) = a
    return (
        int(0.2126*R) +
        int(0.7152*G) +
        int(0.0722*B)
    )


def dog(im: Image, settings: Settings) -> Image:
    image_size = im.size
    (blur_radius_a, blur_radius_b) = settings.blur_radii

    blur_a = im.filter(ImageFilter.GaussianBlur(blur_radius_a))
    blur_b = im.filter(ImageFilter.GaussianBlur(blur_radius_b))

    ret = Image.new("RGB", image_size)
    for i in range(im.width):
        for j in range(im.height):
            px = pixel_subtract(blur_a.getpixel((i, j)),
                                pixel_multiply(
                                    settings.tau, blur_b.getpixel((i, j)))
                                )
            ret.putpixel((i, j), px)

    return ret


def colour(original: Image, target: Image, settings: Settings) -> Image:
    ret = Image.new("RGB", original.size)
    for i in range(original.width):
        for j in range(original.height):
            px = pixel_multiply(
                pixel_luminance(target.getpixel((i, j))) / 255,
                original.getpixel((i, j))
            )
            ret.putpixel((i, j), px)

    return ret


def map_over_image(im: Image, settings: Settings, function) -> Image:
    ret = Image.new("RGB", im.size)
    for i in range(im.width):
        for j in range(im.height):
            ret.putpixel((i, j), function(im.getpixel((i, j)), settings))

        if i % 10 == 0:
            print("col", i, "of", im.width)

    return ret


def set_black_or_white(p: Pixel, settings: Settings) -> Pixel:
    if pixel_luminance(p) >= settings.luminosity_point:
        return WHITE
    return BLACK


def luminance_pixel(p: Pixel, settings: Settings) -> Pixel:
    p_lum = pixel_luminance(p)
    return (p_lum, p_lum, p_lum)


def invert_pixel(p: Pixel, settings: Settings) -> Pixel:
    (a, b, c) = p
    return (255-a, 255-b, 255-c)
