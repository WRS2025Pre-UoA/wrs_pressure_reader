from detect_pressure_gauge_needle import detect_pressure_gauge_needle

def main():
    # 入力と出力のフォルダのパス
    input_folder_path = '/Users/nagasawa/wrs/data/cropped_images'
    output_folder_path = '/Users/nagasawa/wrs/data/result'

    # フォルダ内のすべての画像を処理
    detect_pressure_gauge_needle(input_folder_path, output_folder_path)


if __name__ == "__main__":
    main()
