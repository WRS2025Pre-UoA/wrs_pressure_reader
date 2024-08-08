import cv2
import numpy as np
import os

def phase_correlation_matching(image, template):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    # フーリエ変換
    f_image = np.fft.fft2(gray_image)
    f_template = np.fft.fft2(gray_template, s=gray_image.shape)
    
    # フーリエ変換結果の正規化
    conj_f_template = np.conj(f_template)
    R = (f_image * conj_f_template) / np.abs(f_image * conj_f_template)
    
    # 逆フーリエ変換
    r = np.fft.ifft2(R)
    r = np.abs(r)
    
    # 相関ピークの検出
    max_loc = np.unravel_index(np.argmax(r), r.shape)
    max_val = np.max(r)
    
    # 一致領域のトリミング
    top_left = (max_loc[1], max_loc[0])  # (x, y)
    h, w = gray_template.shape[:2]
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cropped_image = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    
    return cropped_image, top_left, bottom_right, max_val

def process_images_with_multiple_templates(image, templates, iterations=3):
    best_cropped_image = None
    best_top_left = None
    best_bottom_right = None
    best_val = -np.inf
    
    for template in templates:
        current_image = image
        for i in range(iterations):
            cropped_image, top_left, bottom_right, max_val = phase_correlation_matching(current_image, template)
            
            if max_val > best_val:
                best_val = max_val
                best_cropped_image = cropped_image
                best_top_left = top_left
                best_bottom_right = bottom_right
            
            # 元の画像におけるトリミング領域を計算
            top_left_original = (best_top_left[0], best_top_left[1])
            bottom_right_original = (best_bottom_right[0], best_bottom_right[1])
            
            # 次のイテレーションのために現在のトリミング画像を更新
            current_image = image[top_left_original[1]:bottom_right_original[1], top_left_original[0]:bottom_right_original[0]]
    
    return best_cropped_image, best_top_left, best_bottom_right

def main():
    folder_path = '/Users/nagasawa/wrs/data/Origin_data_renamed'
    template_paths = [
        #templateを２値化する
        #cos相関
        #圧力計の中身を切り抜く
        '/Users/nagasawa/wrs/data/template_image/template_1.png', 
        '/Users/nagasawa/wrs/data/template_image/template_2.png', 
        '/Users/nagasawa/wrs/data/template_image/template_3.png',
        '/Users/nagasawa/wrs/data/template_image/template_4.png',
        '/Users/nagasawa/wrs/data/template_image/template_5.png',
        '/Users/nagasawa/wrs/data/template_image/template_6.png',
        '/Users/nagasawa/wrs/data/template_image/template_7.png',
        '/Users/nagasawa/wrs/data/template_image/template_8.png',
        '/Users/nagasawa/wrs/data/template_image/template_9.png',
        '/Users/nagasawa/wrs/data/template_image/template_10.png',
        '/Users/nagasawa/wrs/data/template_image/template_11.png',
        '/Users/nagasawa/wrs/data/template_image/template_12.png'
    ]
    result_folder = '/Users/nagasawa/wrs/data/result_trimming_1'
    
    # 結果フォルダを作成
    os.makedirs(result_folder, exist_ok=True)
    
    # テンプレート画像の読み込み
    templates = [cv2.imread(template_path, cv2.IMREAD_UNCHANGED) for template_path in template_paths]
    for i, template in enumerate(templates):
        if template is None:
            print(f"Error: Could not read template from {template_paths[i]}")
            return
        if template.shape[2] == 4:
            templates[i] = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
    
    # フォルダ内のすべての画像を処理
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error: Could not read image from {image_path}")
                continue
            
            # イテレーション回数を設定
            iterations = 3  # 必要に応じて回数を変更
            final_cropped_image, top_left, bottom_right = process_images_with_multiple_templates(image, templates, iterations=iterations)
            
            # 結果を保存
            result_path = os.path.join(result_folder, f"{os.path.splitext(filename)[0]}_trimmed.jpg")
            cv2.imwrite(result_path, final_cropped_image)
            print(f"Processed {filename}: Trimmed region from {top_left} to {bottom_right}")

if __name__ == "__main__":
    main()

