#フォルダを指定すると、その中の画像を640*640にトリミングするソースコード

import os
from PIL import Image

def crop_center(image, crop_width, crop_height):
    width, height = image.size
    left = (width - crop_width) / 2
    top = (height - crop_height) / 2
    right = (width + crop_width) / 2
    bottom = (height + crop_height) / 2

    return image.crop((left, top, right, bottom))

def process_images(input_folder):
    crop_size = (640, 640)
    
    # 出力フォルダの作成
    output_folder = os.path.join(os.path.dirname(input_folder), 'cropped_images')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 入力フォルダ内のファイルを処理
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path):
            try:
                with Image.open(file_path) as img:
                    # 画像を中心からトリミング
                    cropped_img = crop_center(img, *crop_size)
                    # 保存パスの生成
                    output_path = os.path.join(output_folder, filename)
                    # トリミングされた画像を保存
                    cropped_img.save(output_path)
                    print(f"Cropped and saved: {output_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

# 入力フォルダのパスを指定
input_folder = '/Users/nagasawa/wrs/data/sample'  # ここに入力フォルダのパスを指定してください
process_images(input_folder)


