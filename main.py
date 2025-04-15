import os
from src.io.czi_loader import display_all_slices

def main():
    folder = "data/raw"
    files = sorted(f for f in os.listdir(folder) if f.endswith(".czi"))
    for file in files:
        path = os.path.join(folder, file)
        print(f"Afișez: {file}")
        display_all_slices(path)

if __name__ == "__main__":
    main()
