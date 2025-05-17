import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, measure
from skimage.morphology import skeletonize


def sholl_analysis(image=None, image_path: str = None, soma_coords: tuple = None,
                   step_size: int = 10, max_radius: int = 300, save_path: str = None):
    if image is None:
        if image_path is None:
            raise ValueError("Trebuie să oferi o imagine (image) sau un path (image_path).")
        image = io.imread(image_path)

    binary = image > 0

    if soma_coords is None:
        labeled_img = measure.label(binary)
        regions = measure.regionprops(labeled_img)
        largest_region = max(regions, key=lambda r: r.area)
        soma_coords = tuple(map(int, largest_region.centroid[::-1]))

    skeleton = skeletonize(binary)
    radii = np.arange(0, max_radius, step_size)
    intersections = []

    for r in radii:
        circle = _create_circle_mask(binary.shape, center=soma_coords, radius=r)
        overlap = skeleton & circle
        intersections.append(np.count_nonzero(overlap))

    # Fit polinomial de gradul 20
    degree = 20
    coeffs = np.polyfit(radii, intersections, degree)
    poly_fit = np.poly1d(coeffs)
    radii_fine = np.linspace(min(radii), max(radii), 500)
    intersections_fine = poly_fit(radii_fine)

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    axs[0].imshow(binary, cmap="gray")
    axs[0].scatter(*soma_coords[::-1], c='red', s=40)
    axs[0].set_title("Segmentare + Soma")
    axs[1].plot(radii, intersections, 'o', label='Date brute')
    axs[1].plot(radii_fine, intersections_fine, '-', label=f'Fit grad {degree}', color='blue')
    axs[1].set_title("Sholl Analysis")
    axs[1].set_xlabel("Rază (pixeli)")
    axs[1].set_ylabel("Nr. Intersecții")
    axs[1].legend()
    axs[1].grid(True)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
    else:
        plt.show()


def _create_circle_mask(shape, center, radius):
    Y, X = np.ogrid[:shape[0], :shape[1]]
    dist = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)
    return (dist >= radius) & (dist < radius + 1)
