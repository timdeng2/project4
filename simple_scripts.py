import os, pathlib, json
from pathlib import Path
import time
from PIL import Image

DIR = "data"
DATA_DIR = pathlib.Path(DIR)

train_dir = DATA_DIR / "train"
valid_dir = DATA_DIR / "valid"

# print(f"Length of training set : {len([name for name in os.listdir(train_dir)])}")
# print(f"Length of training set with info files: {len([name for name in os.listdir(train_dir) if name.endswith('_info.json')])}")
# print(f"Length of training set with image files: {len([name for name in os.listdir(train_dir) if name.endswith('_im.jpg')])}")

# print(f"Length of validation set : {len([name for name in os.listdir(valid_dir)])}")
# print(f"Length of validation set with info files: {len([name for name in os.listdir(valid_dir) if name.endswith('_info.json')])}")
# print(f"Length of validation set with image files: {len([name for name in os.listdir(valid_dir) if name.endswith('_im.jpg')])}")

# elements = set()

# path = Path("data/train")

# files = list(path.glob("*_info.json"))

# for file in files:
#     with open(file, "r") as f:
#         data = json.load(f)
#         detects = data["detections"]
#         # print(len(detects))
#         # 10 detects, each represents a kart/frame
#         for i in range(len(detects)):
#             # print(detects[i])
#             # print(len(detects[i]))
#             for j in range(len(detects[i])):
#                 assert len(detects[i][j]) == 6
#                 if detects[i][j][0] == 1:
#                     elements.add(detects[i][j][1])
#                     # since only care about karts, if kart, the second element, track_id can only be 0-9
#                 # 0 - Object 1D
#                 # 1 - 
# print(elements)

start = time.time()
train_element = train_dir / "00000_00_im.jpg"
pil_image = Image.open(train_element)
end = time.time()
print(end - start)