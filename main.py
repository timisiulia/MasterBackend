from src.analysis.multi_roi_processor import MultiRoiProcessor

def main():
    file_path = "data/raw/A1(9).czi"
    output_dir = "outputs"

    processor = MultiRoiProcessor(file_path, output_dir)
    processor.run()

if __name__ == "__main__":
    main()

