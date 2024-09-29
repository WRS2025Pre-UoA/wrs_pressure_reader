import numpy as np

def calculate_angle(center, line):
    """
    針の角度を計算する関数。
    2つの端点のうち、圧力計の中心から遠い方を針の先端とみなして角度を計算します。

    Parameters:
    center (tuple): 圧力計の中心座標 (x, y)
    line (tuple): 針の2つの端点 (x1, y1, x2, y2)

    Returns:
    float: 針の角度（度数法）
    """
    # 圧力計の中心からの距離を計算
    x1, y1, x2, y2 = line[0]
    distance_to_point1 = np.linalg.norm([x1 - center[0], y1 - center[1]])  # 点1の距離
    distance_to_point2 = np.linalg.norm([x2 - center[0], y2 - center[1]])  # 点2の距離

    # 圧力計の中心から遠い方を針の先端とみなす
    if distance_to_point1 > distance_to_point2:
        needle_endpoint = (x1, y1)
    else:
        needle_endpoint = (x2, y2)

    # 針の先端と中心を結ぶベクトルを計算
    needle_vector = np.array([needle_endpoint[0] - center[0], needle_endpoint[1] - center[1]])
    reference_vector = np.array([0, -1])  # 12時方向の基準ベクトル

    # ベクトルを正規化
    needle_vector = needle_vector / np.linalg.norm(needle_vector)
    reference_vector = reference_vector / np.linalg.norm(reference_vector)

    # 内積から角度を計算
    dot_product = np.dot(needle_vector, reference_vector)
    angle_rad = np.arccos(dot_product)  # ラジアンの角度
    angle_deg = np.degrees(angle_rad)   # 度数法に変換

    # 針が左半分にある場合は、360度 - angle_deg にする
    if needle_vector[0] < 0:
        angle_deg = 360 - angle_deg

    return angle_deg


def pressure_value_from_angle(angle_deg, max_pressure=100):
    """
    針の角度から圧力計の値を計算する関数。
    228度の時に0Pa, 360度と0度の時に0.5MPa, 132度の時に1MPa。

    Parameters:
    angle_deg (float): 針の角度（度数法）

    Returns:
    float: 圧力値（MPa）
    """

    
    if 228 <= angle_deg < 270:
        # 228度から270度までは0MPaから0.16MPaに線形補間
        pressure = (angle_deg - 228) * (0.16 / (270 - 228))
    elif 270 <= angle_deg <= 360:
        # 270度から360度までは0.16MPaから0.5MPaに線形補間
        pressure = 0.16 + (angle_deg - 270) * (0.34 / (360 - 270))
    elif 0 <= angle_deg <= 90:
        # 0度から90度までは0.5MPaから0.84MPaに線形補間
        pressure = 0.5 + (angle_deg / 90) * (0.84 - 0.5)
    elif 90 < angle_deg <= 132:
        # 90度から132度までは0.84MPaから1.0MPaに線形補間
        pressure = 0.84 + ((angle_deg - 90) / (132 - 90)) * (1.0 - 0.84)
    else:
        # 132度から228度までは0MPa
        pressure = 0.0
    return pressure

