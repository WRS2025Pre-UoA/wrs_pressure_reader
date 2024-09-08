import cv2
import numpy as np

def add_margin_to_scale(image, scale):
    """
    画像に余白を追加して、指定されたスケールになるように調整する。

    :param image: 入力画像（numpy.ndarray）
    :param scale: スケール（0.5 や 0.75 など）
    :return: 余白が追加された新しい画像（numpy.ndarray）
    """
    original_height, original_width = image.shape[:2]
    new_height = int(original_height / scale)
    new_width = int(original_width / scale)
    
    top_margin = (new_height - original_height) // 2
    bottom_margin = new_height - original_height - top_margin
    left_margin = (new_width - original_width) // 2
    right_margin = new_width - original_width - left_margin

    color = [0, 0, 0]  # 黒い余白
    new_image = cv2.copyMakeBorder(image, top_margin, bottom_margin, left_margin, right_margin, cv2.BORDER_CONSTANT, value=color)
    return new_image

def main():
    input_path = '/Users/nagasawa/wrs/data/template_new/template_1のコピー2.png'
    output_path_50 = '/Users/nagasawa/wrs/data/template_new/output_image_50.jpg'
    output_path_75 = '/Users/nagasawa/wrs/data/template_new/output_image_75.jpg'
    
    # 画像の読み込み
    image = cv2.imread(input_path)
    
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {input_path}")
    
    # 余白を追加してスケール0.5になるように調整
    image_scaled_50 = add_margin_to_scale(image, 0.5)
    
    # 余白を追加してスケール0.75になるように調整
    image_scaled_75 = add_margin_to_scale(image, 0.75)
    
    # 新しい画像の保存
    cv2.imwrite(output_path_50, image_scaled_50)
    print(f"Image saved with scale 0.5 at: {output_path_50}")
    
    cv2.imwrite(output_path_75, image_scaled_75)
    print(f"Image saved with scale 0.75 at: {output_path_75}")

if __name__ == "__main__":
    main()
