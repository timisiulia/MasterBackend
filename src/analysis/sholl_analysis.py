from src.io.sholl import sholl_analysis

sholl_analysis(
    image_path=r"data/trashhold/MAX_A1.czi - A1.czi #01-1_502.3068.tif",
    step_size=5,
    max_radius=250,
    save_path="outputs/sholl_MAX_A1.png"
)


