import cv2
import numpy as np
import os

def process_image(image, output_path):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #円検出→中身だけを使う
    #外側のノイズを除去

    # 2値化処理
    _, bw = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    #fisher


    # 細線化処理
    inverted_image = cv2.bitwise_not(bw)
    thinned_edges = cv2.ximgproc.thinning(inverted_image)
    
    # 膨張処理
    ed = cv2.dilate(thinned_edges, np.ones((3,3), np.uint8))
    lines = cv2.HoughLinesP(ed, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=5)
    
    if lines is not None:
        # 画像の中心点を計算
        img_center = (image.shape[1] // 2, image.shape[0] // 2)
        
        def distance_to_center(line):
            x1, y1, x2, y2 = line[0]
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            return np.sqrt((cx - img_center[0]) ** 2 + (cy - img_center[1]) ** 2)
        
        # 中心に近い線を抽出
        center_lines = sorted(lines, key=distance_to_center)[:10]  
        
        def line_length(line):
            x1, y1, x2, y2 = line[0]
            return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
        # 最も長い線を抽出
        longest_line = max(center_lines, key=line_length)
        
        # 最も長い線を描画
        x1, y1, x2, y2 = longest_line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 結果の画像を保存
    cv2.imwrite(output_path, image)
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
output_folder_path = '/Users/nagasawa/wrs/data/thinning_result2'

# フォルダ内のすべての画像を処理
process_images_in_folder(input_folder_path, output_folder_path)




