# from src.io.czi_loader import display_all_slices_separate_windows_rgb_mapping
#
# if __name__ == "__main__":
#     display_all_slices_separate_windows_rgb_mapping("data/raw/A1(15).czi")
from src.io.sholl import sholl_analysis

def main():
    sholl_analysis(
        image_path=r"data/trashhold/MAX_A1.czi - A1.czi #01-1_502.3068.tif",
        step_size=5,
        max_radius=250,
        save_path="outputs/sholl_MAX_A1.png"
    )

if __name__ == "__main__":
    main()
