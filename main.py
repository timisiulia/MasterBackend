# from src.analysis.roi_pipeline import process_roi_from_mip
#
# def main():
#     file_path = "data/raw/A1(9).czi"
#     output_dir = "outputs"
#
#     print("🔄 Se rulează selecția și analiza ROI (cu Sholl)...")
#     process_roi_from_mip(file_path, output_dir)
#     print("✅ Toți neuronii au fost procesați.")
#
# if __name__ == "__main__":
#     main()
from src.analysis.multi_roi_processor import MultiRoiProcessor

def main():
    file_path = "data/raw/A1(9).czi"  # sau calea reală
    output_dir = "outputs"

    processor = MultiRoiProcessor(file_path, output_dir)
    processor.run()  # foarte important!

if __name__ == "__main__":
    main()

