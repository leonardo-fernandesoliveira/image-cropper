import shutil
from pathlib import Path
from fire import Fire

def main(base_folder: str, output_folder: str) -> None:
    base_folder = Path(base_folder)
    output_folder = Path(output_folder)
    for subfolder in base_folder.iterdir():
        for img in subfolder.rglob("**/*.jpg"):
            folder = Path(output_folder / img.stem)
            folder.mkdir(parents=True, exist_ok=True)
            output_path = folder / (subfolder.name + img.suffix)
            shutil.copy(img, output_path)

if __name__ == "__main__":
    Fire(main)
