# from src.io.czi_loader import display_all_slices_separate_windows_rgb_mapping
#
# if __name__ == "__main__":
#     display_all_slices_separate_windows_rgb_mapping("data/raw/A1(15).czi")
from src.io.czi_loader import display_all_slices_separate_windows_rgb_mapping

from src.analysis.roi_pipeline import process_roi_from_mip
from src.io.sholl import sholl_analysis

# def main():
#     # sholl_analysis(
#     #     image_path=r"data/trashhold/MAX_A1.czi - A1.czi #01-1_502.3068.tif",
#     #     step_size=5,
#     #     max_radius=250,
#     #     save_path="outputs/sholl_MAX_A1.png"
#     # )
#     display_all_slices_separate_windows_rgb_mapping("data/raw/A1(15).czi")
#
# if __name__ == "__main__":
#     main()
#if __name__ == "__main__":
#    process_roi_from_mip("data/raw/A1(15).czi")
from skimage.io import imread
from src.analysis.roi_pipeline import process_roi_from_mip
from src.io.sholl import sholl_analysis

def main():
    file_path = "data/raw/A1(15).czi"
    output_dir = "outputs"

    print("🔄 Pas 1: Se rulează procesarea ROI...")
    process_roi_from_mip(file_path, output_dir)

    binary_path = f"{output_dir}/roi_binary.tif"
    try:
        print("✅ Lansez analiza Sholl pe imaginea binarizată...")
        binary_img = imread(binary_path)
        sholl_analysis(
            image=binary_img,
            step_size=5,
            max_radius=250,
            save_path=f"{output_dir}/sholl_roi_binary.png"
        )
        print("✅ Analiza Sholl a fost realizată cu succes.")
    except FileNotFoundError:
        print("❌ Eroare: roi_binary.tif nu a fost generat. Verifică dacă ROI a fost selectat corect.")

if __name__ == "__main__":
    main()
