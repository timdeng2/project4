from pathlib import Path

import fire
from matplotlib import pyplot as plt
import json

from .generate_qa import draw_detections, extract_frame_info, extract_kart_objects, extract_track_info


def generate_caption(info_path: str, view_index: int, img_width: int = 150, img_height: int = 100) -> list:
    """
    Generate caption for a specific view.
    """
    karts = extract_kart_objects(info_path, view_index)
    info_path_obj = Path(info_path)
    image_file = f"{info_path_obj.parent.name}/{info_path_obj.stem.replace('_info', '')}_{view_index:02d}_im.jpg"

    track = extract_track_info(info_path)

    out = []
    out.append(
        {
            "image_file": image_file,
            "caption": f"The track is {track}."
        }  
    )

    center_kart_idx = -1
    center_kart_coords = (-1,-1)
    for i, kart in enumerate(karts):
        if kart['is_center_kart']:
            out.append(
                {
                    "image_file": image_file,
                    "caption": f"{kart['kart_name']} is the ego car."
                }
            )
            center_kart_idx = i
            center_kart_coords = kart['center']
            break
    
    if center_kart_idx == -1:
        print("Could not find ego kart")
        return out
    
    out.append(
        {
            "image_file": image_file,
            "caption": f"There are {str(len(karts))} karts in the scene."
        }
    )



    for i, kart in enumerate(karts):
        if i == center_kart_idx:
            continue

        x, y = kart['center']

        # if abs(x - center_kart_coords[0]) >= abs(y - center_kart_coords[1]):
        # horizontal comparison
        direction = ""
        if x < center_kart_coords[0]:
            direction = "left"
        elif x > center_kart_coords[0]:
            direction = "right"
        
        if direction != "":
            out.append(
                {
                    "image_file": image_file,
                    "caption": f"{kart['kart_name']} is {direction} of the ego car."
                }
            )
        # else:
            # vertical comparison
        if y < center_kart_coords[1]:
            out.append(
                {
                    "image_file": image_file,
                    "caption": f"{kart['kart_name']} is behind the ego car."
                }
            )
        elif y > center_kart_coords[1]:
            out.append(
                {
                    "image_file": image_file,
                    "caption": f"{kart['kart_name']} is in front of the ego car."
                }
            )
            
    kart_names = [kart['kart_name'] for kart in karts]
    out.append(
        {
            "image_file": image_file,
            "caption": f"The karts in the scene are {', '.join(kart_names)}."
        }
    )

    # 1. Ego car
    # {kart_name} is the ego car.

    # 2. Counting
    # There are {num_karts} karts in the scenario.

    # 3. Track name
    # The track is {track_name}.

    # 4. Relative position
    # {kart_name} is {position} of the ego car.

    return out


def generate_all_captions(info_dir: str, output_file: str):
    info_dir = Path(info_dir)
    all_captions = []

    info_files = list(info_dir.glob("*_info.json"))
    print(f"Found {len(info_files)} info files")

    for i, info_file in enumerate(info_files):
        with open(info_file) as f:
            info = json.load(f)

        num_views = len(info.get("detections", []))

        for view_index in range(num_views):
            base_name = info_file.stem.replace("_info", "")
            image_files = list(info_dir.glob(f"{base_name}_{view_index:02d}_im.jpg"))
            if not image_files:
                print(f"Skipping view {base_name}_{view_index:02d}_im.jpg — no image found")
                continue

            try:
                captions = generate_caption(str(info_file), view_index)
                all_captions.extend(captions)
            except Exception as e:
                print(f"Error processing view {base_name}_{view_index:02d}: {e}")
                continue

        if i % 25 == 0: 
            print(f"Processed {i} info_files / {len(info_files)}")

    print(f"\nTotal captions generated: {len(all_captions)}")

    with open(output_file, "w") as f:
        json.dump(all_captions, f, indent=2)

    print(f"Saved to {output_file}")

def check_caption(info_file: str, view_index: int):
    captions = generate_caption(info_file, view_index)

    print("\nCaption:")
    print("-" * 50)
    for i, caption in enumerate(captions):
        print(f"{i + 1}. {caption}")
        print("-" * 50)

    info_path = Path(info_file)
    base_name = info_path.stem.replace("_info", "")
    image_file = list(info_path.parent.glob(f"{base_name}_{view_index:02d}_im.jpg"))[0]

    annotated_image = draw_detections(str(image_file), info_file)

    plt.figure(figsize=(12, 8))
    plt.imshow(annotated_image)
    plt.axis("off")
    plt.title(f"Frame {extract_frame_info(str(image_file))[0]}, View {view_index}")
    plt.show()


"""
Usage Example: Visualize QA pairs for a specific file and view:
   python generate_captions.py check --info_file ../data/valid/00000_info.json --view_index 0

You probably need to add additional commands to Fire below.
"""


def main():
    fire.Fire({"check": check_caption, "generate_all": generate_all_captions})


if __name__ == "__main__":
    main()
