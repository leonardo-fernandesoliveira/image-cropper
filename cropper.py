import os
import glob
import json
from pathlib import Path
from fire import Fire
from PIL import Image
from tqdm import tqdm

def load_images(base_folder, scene_name):
    extensions = ["png", "jpg", "jpeg", "bmp", "tiff", "gif"]
    return [
        img
        for ext in extensions
        for img in glob.glob(os.path.join(base_folder, f"*/{scene_name}.{ext}"))
    ]

def apply_crops(base_folder: str, crops_json: str):
    # Load the crop regions from the JSON file
    with open(crops_json, 'r') as f:
        all_data = json.load(f)

    if not os.path.exists('crops'):
        os.mkdir('crops')

    # Loop through all experiments in the JSON file
    for experiment, data in tqdm(all_data.items()):
        coords = data["coords"]
        rotate_angle = data.get("rotate", 0)  # Get rotation angle if exists, otherwise default to 0
        image_paths = load_images(base_folder, experiment)
        
        for image_path in image_paths:
            im = Image.open(image_path)
            
            # Saving full image
            full_img_path = Path('crops/full')
            experiment_name = os.path.basename(os.path.dirname(image_path))
            full_img_path.mkdir(parents=True, exist_ok=True)
            im.save(full_img_path / Path(experiment_name + "_" + str(Path(image_path).name)))

            for idx, coord in enumerate(coords):
                x, y, w, h = coord
                x1, y1, x2, y2 = [x, y, x + w, y + h]
                crop = im.crop((x1, y1, x2, y2))
                if rotate_angle:
                    crop = crop.rotate(rotate_angle)
                experiment_name = os.path.basename(os.path.dirname(image_path))
                
                # Saving crop
                dest_folder = Path('crops/' + experiment_name)
                dest_folder.mkdir(parents=True, exist_ok=True)
                crop.save(dest_folder / f'{experiment_name}_{experiment}_{idx}.png')

if __name__ == "__main__":
    Fire(apply_crops)
