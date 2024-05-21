import sys,os
from PIL import Image


image_foleder = sys.argv[1]
output_folder = sys.argv[2]

if not os.path.exists(output_folder):
  os.makedirs(output_folder)


for image in os.listdir(image_foleder):
  img = Image.open(f'{image_foleder}{image}')
  clean_name = os.path.splitext(image)[0]
  img.save(f'{output_folder}{clean_name}.png', 'png')
  print("done!")