import matplotlib
matplotlib.use("TkAgg")  # ⚠️ esențial pentru ferestre externe

import matplotlib.pyplot as plt
from aicsimageio import AICSImage


def display_all_slices(path):
    img = AICSImage(path)
    data = img.get_image_data("ZCYX", T=0)  # [Z, C, Y, X]

    z_dim = data.shape[0]
    for z in range(z_dim):
        slice_img = data[z, 0, :, :]  # canal 0
        plt.figure()
        plt.imshow(slice_img, cmap="gray")
        plt.title(f"Slice {z} din {path}")
        plt.axis("off")
        plt.show()
