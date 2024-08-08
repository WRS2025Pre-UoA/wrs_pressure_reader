import os
import shutil

def rename_files_in_folder(folder_path):
    # 元のフォルダ名に_renamedを付けた新しいフォルダを生成
    new_folder_path = f"{folder_path}_renamed"
    os.makedirs(new_folder_path, exist_ok=True)

    # フォルダ内のファイルを列挙し、test_number形式に名前を変更
    for i, filename in enumerate(os.listdir(folder_path), start=1):
        old_file_path = os.path.join(folder_path, filename)
        if os.path.isfile(old_file_path):
            new_file_name = f"test_{i}{os.path.splitext(filename)[1]}"
            new_file_path = os.path.join(new_folder_path, new_file_name)
            shutil.copy2(old_file_path, new_file_path)

    print(f"ファイル名を変更し、新しいフォルダにコピーしました: {new_folder_path}")

# 使用例
folder_path ="/Users/nagasawa/wrs/data/Origin_data"
rename_files_in_folder(folder_path)
