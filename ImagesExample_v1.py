import numpy as np
from PIL import Image


# https://newbedev.com/how-can-i-create-a-circular-mask-for-a-numpy-array

def create_circular_mask(h=256, w=256, center=None, radius=10):
    if center is None:  # use the middle of the image
        center = (int(w / 2), int(h / 2))
    if radius is None:  # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w - center[0], h - center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)

    mask = (dist_from_center <= radius) * 256
    return mask


def Ber(U1):
    return np.random.binomial(1, 1 - U1)


def BerExp(C, Dnum, Dstr):
    if Dstr == "H":
        out = 0.75 * Dnum + 0.5 * C + 0.25
    else:
        out = 2.5 * Dnum + 1.75 * C - 0.25
    out = 1 / (1 + np.exp(-out))
    out = np.random.binomial(1, out)
    return out


def drawImage(H, V, R, C, output_path):
    image = np.zeros(shape=(256, 256))
    randInd = np.random.randint(low=1, high=10000)
    if H == 1:
        randPosH = np.random.randint(low=10, high=246)
        image[randPosH - 5:randPosH + 5, :] = 256

    if V == 1:
        randPosV = np.random.randint(low=10, high=246)
        image[:, randPosV - 5:randPosV + 5] = 256

    if C == 1:
        randC1 = np.random.randint(low=10, high=246)
        randC2 = np.random.randint(low=10, high=246)

        mask = create_circular_mask(center=(randC1, randC2))
        image = image + mask

    image = image + np.random.binomial(1, 0.005, size=(256, 256)) * 256
    image = Image.fromarray(image)
    image = image.convert("L")
    image.save(output_path + "/" + str(randInd) + ".png")
