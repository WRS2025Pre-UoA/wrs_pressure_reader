import cv2
import numpy as np
import os
from datetime import datetime
import cv2.ximgproc as ximgproc

def calculate_pressure_value(angle):
    # 圧力値の計算
    if 135 <= angle <= 225:
        pressure_value = (225 - angle) / 90.0  # 0 MPaから1 MPa
    else:
        pressure_value = 0.0  # デフォルトの値

    # 0.02刻みに調整
    pressure_value = round(pressure_value * 50) / 50.0
    return pressure_value

def detect_and_draw_line(image, output_path, image_file_name):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bw = cv2.threshold(gray,60,255, cv2.THRESH_BINARY)
    #edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    #thinned_edges = ximgproc.thinning(edges)
    thinned_edges = ximgproc.thinning(bw)
    ed = cv2.dilate(thinned_edges,np.ones((3,3), np.uint8))
    lines = cv2.HoughLinesP(ed, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=5)
    
    if lines is not None:
        longest_line = max(lines, key=lambda line: np.sqrt((line[0][2] - line[0][0]) ** 2 + (line[0][3] - line[0][1]) ** 2))[0]
        
        # 直線の両端の座標
        x1, y1, x2, y2 = longest_line
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # 画像の中心を計算
        center_x = image.shape[1] // 2
        center_y = image.shape[0] // 2
        
        # 直線の端のうち、中心から最も遠い点を選択
        dist1 = np.sqrt((x1 - center_x) ** 2 + (y1 - center_y) ** 2)
        dist2 = np.sqrt((x2 - center_x) ** 2 + (y2 - center_y) ** 2)
        
        if dist1 > dist2:
            farthest_point = (x1, y1)
            closest_point = (x2, y2)
        else:
            farthest_point = (x2, y2)
            closest_point = (x1, y1)
        
        # 画像の中心と直線の端の座標を結ぶ直線を描画
        cv2.line(image, (center_x, center_y), farthest_point, (255, 0, 0), 2)
        
        # 針の角度を計算
        angle = np.arctan2(-farthest_point[1] + center_y, farthest_point[0] - center_x)
        angle = np.degrees(angle)
        if angle < 0:
            angle += 360
        print(f'{image_file_name}: 針の角度 {angle} 度')
        
        # 角度から圧力計の値を計算
        pressure_value = calculate_pressure_value(angle)
        print(f'{image_file_name}: 圧力計の値 {pressure_value:.2f} MPa')

        cv2.imwrite(output_path, image)
        print(f'結果の画像が保存されました: {output_path}')
    else:
        print(f'{image_file_name}: 直線が検出されませんでした')

def process_images_in_folder(input_folder, output_folder):
    image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    
    for image_file in image_files:
        input_image_path = os.path.join(input_folder, image_file)
        image = cv2.imread(input_image_path)
        
        if image is not None:
            output_image_name = f'{os.path.splitext(image_file)[0]}_result.jpg'
            output_image_path = os.path.join(output_folder, output_image_name)
            
            detect_and_draw_line(image, output_image_path, image_file)
        else:
            print(f'画像を読み込めませんでした: {input_image_path}')

# 入力フォルダのパス
input_folder_path = '/Users/nagasawa/wrs/data/result_trimming'

# 出力フォルダのパス
output_folder_path = '/Users/nagasawa/wrs/data/result'

# フォルダ内のすべての画像を処理
process_images_in_folder(input_folder_path, output_folder_path)






