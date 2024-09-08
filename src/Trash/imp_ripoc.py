# # 画像の読み込み
# template_paths = [
#     '/Users/nagasawa/wrs/data/template_new/output_image_50.jpg',
#     '/Users/nagasawa/wrs/data/template_new/output_image_75.jpg',
#     '/Users/nagasawa/wrs/data/template_new/template_1のコピー2.png'
# ]
# image_path = '/Users/nagasawa/wrs/data/Origin_data_renamed/test_1.jpg'

import cv2
import numpy as np
import matplotlib.pyplot as plt
from ripoc import ripoc

def draw_match(image, top_left, bottom_right):
    image_with_rectangle = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(image_with_rectangle, top_left, bottom_right, (0, 255, 0), 2)
    return image_with_rectangle

def apply_ripoc_with_multiple_templates(image, templates):
    best_score = float('-inf')
    best_template = None
    best_result = None

    for template in templates:
        if template.shape[0] > image.shape[0] or template.shape[1] > image.shape[1]:
            continue  # テンプレートが比較画像よりも大きい場合はスキップ

        shift_y, shift_x, angle, scale_factor = ripoc(template, image)

        # 一致度を評価（シフト量、回転角度、スケール変化の逆数をスコアとする）
        score = 1 / (abs(shift_y) + abs(shift_x) + abs(angle) + abs(scale_factor - 1))

        if score > best_score:
            best_score = score
            best_template = template
            best_result = (shift_y, shift_x, angle, scale_factor)

    return best_template, best_result

# 画像の読み込み
template_paths = [
    '/Users/nagasawa/wrs/data/template_new/output_image_50.jpg',
    '/Users/nagasawa/wrs/data/template_new/output_image_75.jpg',
    '/Users/nagasawa/wrs/data/template_new/template_1のコピー2.png'
]
image_path = '/Users/nagasawa/wrs/data/Origin_data_renamed/test_1.jpg'

# テンプレート画像の読み込み
templates = [cv2.imread(template_path, cv2.IMREAD_GRAYSCALE) for template_path in template_paths]
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# 画像が正しく読み込まれたかを確認
if any(template is None for template in templates):
    raise FileNotFoundError("One or more template images not found.")
if image is None:
    raise FileNotFoundError(f"Image not found at path: {image_path}")

# 各テンプレートに対してripocを適用
best_template, best_result = apply_ripoc_with_multiple_templates(image, templates)

# 一致が見つからなかった場合の処理
if best_result is None:
    raise ValueError("No matching template found.")

best_shift, best_angle, best_scale = best_result

print(f"Best Shift Y: {best_shift[0]}")
print(f"Best Shift X: {best_shift[1]}")
print(f"Best Angle: {best_angle}")
print(f"Best Scale: {best_scale}")

# マッチした部分を描画
template_h, template_w = best_template.shape
top_left = (int(best_shift[1]), int(best_shift[0]))
bottom_right = (top_left[0] + template_w, top_left[1] + template_h)
image_with_match = draw_match(image, top_left, bottom_right)

# 結果を表示
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].imshow(best_template, cmap='gray')
axs[0].set_title('Best Template Image')
axs[1].imshow(image_with_match)
axs[1].set_title('Matched Image with Template Area')
plt.show()


