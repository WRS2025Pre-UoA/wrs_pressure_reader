# 圧力計

このプロジェクトは、圧力計の画像から圧力値を読み取るためのものです。画像処理と解析はPythonとOpenCVを使用して行われます。

実行：python src/main.py

## アルゴリズム
step1. 圧力メーターを含む写真を撮影
step2. 画像の中から、圧力計をトリミング→位相限定相関法
step3. トリミングした画像の中の針の角度を出力→ハフ変換によるエッジ検出
step4. 角度から圧力メーターの値を出力→圧力メーターの種類だけ出力

## 使い方
    > git clone 
    > pip install -r requirements.txt
    > python main.py



## ソースコードファイル


### `src/`

  
- `main.py`
  - メインスクリプト。他のモジュールから関数を呼び出して、画像の前処理、針の検出、角度の計算、そして圧力値の計算を実行します。

- `camera_helper.py`: 
  - カメラの起動
  - 正しく圧力計を撮影するための補助線を表示
  
- `image_processing.py`:
  - 入力:画像のファイルパス
  - 出力:圧力計の中心と、針の両端の座標
  - 画像をバイナリ化し、ハフ検出
  
- `needle_angle.py`: 
  - 圧力計の中心から単位ベクトルと、正規化した針のベクトルからラジアンを出力
  - ラジアンに対応した圧力値を出力



