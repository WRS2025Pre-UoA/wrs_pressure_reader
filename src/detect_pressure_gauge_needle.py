import cv2
import numpy as np
import os
from datetime import datetime

def detect_pressure_gauge_needle(image, output_path):
    # グレースケールに変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # エッジ検出
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Hough変換で直線を検出
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)
    
    if lines is not None:
        max_len = 0
        needle_line = None
        
        # 最も長い直線を特定
        for line in lines:
            for x1, y1, x2, y2 in line:
                length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if length > max_len:
                    max_len = length
                    needle_line = (x1, y1, x2, y2)
        
        if needle_line is not None:
            x1, y1, x2, y2 = needle_line
            
            # 針の直線を描画
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # 傾きを計算
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            print(f'針の角度: {angle} 度')
            
            # 画像を保存
            cv2.imwrite(output_path, image)
            print(f'結果の画像が保存されました: {output_path}')
            
            return angle
    else:
        print('針が検出されませんでした')
        return None

def process_images_in_folder(input_folder, output_folder):
    # 入力フォルダ内のすべての画像ファイルを取得
    image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    
    for image_file in image_files:
        input_image_path = os.path.join(input_folder, image_file)
        
        # 画像の読み込み
        image = cv2.imread(input_image_path)
        
        if image is not None:
            # 出力画像のパスを生成
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_image_name = f'{os.path.splitext(image_file)[0]}_needle_detection_{timestamp}.jpg'
            output_image_path = os.path.join(output_folder, output_image_name)
            
            # 針の検出と傾き計算を実行
            detect_pressure_gauge_needle(image, output_image_path)
        else:
            print(f'画像を読み込めませんでした: {input_image_path}')

# 入力フォルダのパス
input_folder_path = '/Users/nagasawa/wrs/data/cropped_images'

# 出力フォルダのパス
output_folder_path = '/Users/nagasawa/wrs/data/result'

# フォルダ内のすべての画像を処理
process_images_in_folder(input_folder_path, output_folder_path)

