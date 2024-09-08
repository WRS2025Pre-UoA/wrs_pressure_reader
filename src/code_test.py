import cv2
import os

def process_image(image_path):
    # 画像の読み込みとグレースケール化
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # バイナリ化 (しきい値の値は画像に応じて調整)
    _, bw = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    # ノイズ除去（小さいゴミを取り除く）
    bw = cv2.medianBlur(bw, 5)

    return gray, bw

def process_images_in_folder(input_folder, output_folder):
    # 出力フォルダが存在しない場合は新しく作成
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 入力フォルダ内のすべての画像ファイルを処理
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            image_path = os.path.join(input_folder, filename)
            
            # 画像を処理
            gray, bw = process_image(image_path)

            # グレースケール画像とバイナリ化画像を保存
            gray_output_path = os.path.join(output_folder, f"gray_{filename}")
            bw_output_path = os.path.join(output_folder, f"bw_{filename}")
            
            cv2.imwrite(gray_output_path, gray)
            cv2.imwrite(bw_output_path, bw)

            print(f"Processed and saved: {filename}")

# テスト実行
input_folder = '/Users/nagasawa/wrs/data/Origin_data_renamed'  # 入力フォルダを指定
output_folder = '/Users/nagasawa/wrs/data/0908_results'  # 出力フォルダを指定

process_images_in_folder(input_folder, output_folder)
