import cv2
import numpy as np
import os

def process_image(image, output_path):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # 2値化処理
    _, bw = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)
    
    # 細線化処理
    inverted_image = cv2.bitwise_not(bw)
    thinned_edges = cv2.ximgproc.thinning(inverted_image)
    
    # 膨張処理
    ed = cv2.dilate(thinned_edges, np.ones((3,3), np.uint8))
    
    # 結果の画像を保存
    cv2.imwrite(output_path, bw)
    #cv2.imwrite(output_path, thinned_edges )
    #cv2.imwrite(output_path, ed)
    print(f'結果の画像が保存されました: {output_path}')

def process_images_in_folder(input_folder, output_folder):
    image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    
    for image_file in image_files:
        input_image_path = os.path.join(input_folder, image_file)
        image = cv2.imread(input_image_path)
        
        if image is not None:
            output_image_name = f'{os.path.splitext(image_file)[0]}_processed.jpg'
            output_image_path = os.path.join(output_folder, output_image_name)
            
            process_image(image, output_image_path)
        else:
            print(f'画像を読み込めませんでした: {input_image_path}')

# 入力フォルダのパス
input_folder_path = '/Users/nagasawa/wrs/data/result_trimming'

# 出力フォルダのパス
output_folder_path = '/Users/nagasawa/wrs/data/binary_result'

# フォルダ内のすべての画像を処理
process_images_in_folder(input_folder_path, output_folder_path)
