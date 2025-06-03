import os
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from aicsimageio import AICSImage
from skimage import filters, measure, morphology
from skimage.io import imsave
from src.io.sholl import sholl_analysis
from src.io.sholl_exported_values import ShollCSVLogger
import shutil


class MultiRoiProcessorBase:
    def __init__(self, file_path: str, output_dir: str = "outputs"):
        self.file_path = file_path
        self.output_dir = output_dir

        # Golește complet outputs la fiecare rulare
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            print(f"🗑️  Folderul '{output_dir}/' vechi a fost șters.")
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"✅ Folderul '{output_dir}/' nou a fost creat.")

        self.img = AICSImage(file_path)
        self.data = self.img.get_image_data("CZYX", T=0, S=0)
        self.mip = self.data.max(axis=1)
        self.rgb = self._generate_rgb()

        imsave(os.path.join(self.output_dir, "full_rgb.png"), (self.rgb * 255).astype(np.uint8))

    def _generate_rgb(self):
        rgb = np.zeros((*self.mip.shape[1:], 3), dtype=np.float32)
        for c, color in enumerate([(0, 0, 1), (0, 1, 0), (1, 0, 0)]):
            channel = self.mip[c]
            norm = channel / channel.max() if channel.max() > 0 else channel
            for i in range(3):
                rgb[..., i] += norm * color[i]
        rgb = np.clip(rgb * 2.0, 0, 1)  # intensificare culoare
        return rgb


class MultiRoiProcessor(MultiRoiProcessorBase):
    def __init__(self, file_path: str, output_dir: str = "outputs"):
        super().__init__(file_path, output_dir)
        self.roi_coords = []

    def select_rois(self):
        self.fig, self.ax = plt.subplots()
        self.ax.imshow(self.rgb)
        self.ax.set_title("Selectează ROI-uri. ENTER când ai terminat.")
        self.roi_coords = []

        def _onselect(eclick, erelease):
            if eclick.xdata is None or erelease.xdata is None:
                print("⚠️ Click în afara imaginii – selecție ignorată.")
                return

            x1, y1 = int(eclick.xdata), int(eclick.ydata)
            x2, y2 = int(erelease.xdata), int(erelease.ydata)

            if abs(x2 - x1) < 5 or abs(y2 - y1) < 5:
                print("⚠️ ROI prea mic – ignorat.")
                return

            roi = (min(y1, y2), max(y1, y2), min(x1, x2), max(x1, x2))
            self.roi_coords.append(roi)
            self.ax.add_patch(plt.Rectangle(
                (roi[2], roi[0]), roi[3] - roi[2], roi[1] - roi[0],
                fill=False, color="red", linewidth=2
            ))
            print(f"✅ ROI adăugat: {roi}")
            self.fig.canvas.draw_idle()

        def _on_key(event):
            if event.key == 'enter':
                print(f"🔵 ENTER apăsat. ROI-uri selectate: {len(self.roi_coords)}")
                plt.close()

        self.fig.canvas.mpl_connect("key_press_event", _on_key)
        self.selector = RectangleSelector(
            self.ax, _onselect,
            useblit=False,
            button=[1],
            spancoords='pixels',
            props=dict(edgecolor='red', linewidth=2, fill=False)
        )
        print("🔄 Poți selecta mai mulți neuroni. Apasă ENTER când termini.")
        plt.show()

    def process_all(self):
        logger = ShollCSVLogger()
        for i, (y1, y2, x1, x2) in enumerate(self.roi_coords):
            roi_dir = os.path.join(self.output_dir, f"roi_{i+1}")
            os.makedirs(roi_dir, exist_ok=True)

            roi_red = self.mip[2, y1:y2, x1:x2]
            roi_green = self.mip[1, y1:y2, x1:x2]
            roi_blue = self.mip[0, y1:y2, x1:x2]

            roi_rgb = np.stack([
                roi_blue / roi_blue.max(),
                roi_green / roi_green.max(),
                roi_red / roi_red.max()
            ], axis=-1)
            roi_rgb = np.clip(roi_rgb * 2.0, 0, 1)
            imsave(os.path.join(roi_dir, "roi_rgb.png"), (roi_rgb * 255).astype(np.uint8))

            for channel, name in zip([roi_green, roi_blue, roi_red], ["Greens", "Blues", "Reds"]):
                fig, ax = plt.subplots()
                ax.imshow(channel, cmap=name)
                ax.set_title(f"Canal {name}")
                plt.savefig(os.path.join(roi_dir, f"roi_{name.lower()}.png"))
                plt.close(fig)

            red_norm = roi_red / roi_red.max()
            threshold = filters.threshold_yen(red_norm)
            binary = red_norm > threshold
            binary = morphology.remove_small_objects(binary, min_size=64)

            binary_path = os.path.join(roi_dir, "roi_binary.tif")
            imsave(binary_path, (binary * 255).astype(np.uint8))

            contours = measure.find_contours(binary, 0.5)
            fig, ax = plt.subplots()
            ax.imshow(binary, cmap="gray")
            for contour in contours:
                ax.plot(contour[:, 1], contour[:, 0], linewidth=1, color="red")
            ax.set_title("Contur ROI")
            plt.savefig(os.path.join(roi_dir, "roi_contours.png"))
            plt.close(fig)

            if binary.sum() > 0:
                sholl_path = os.path.join(roi_dir, "sholl_analysis.png")
                max_i, total_i = sholl_analysis(
                    image_path=binary_path,
                    step_size=5,
                    max_radius=250,
                    save_path=sholl_path
                ) or (0, 0)

                roi_shape = roi_red.shape
                binary_area = int(binary.sum())
                roi_folder = f"roi_{i + 1}"

                logger.log_result(
                    image_name=os.path.basename(self.file_path),
                    roi_index=i + 1,
                    roi_folder=roi_folder,
                    roi_shape=roi_shape,
                    binary_area=binary_area,
                    max_intersections=max_i,
                    total_intersections=total_i
                )

    def run(self):
        self.select_rois()
        self.process_all()
