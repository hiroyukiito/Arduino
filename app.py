
#Sinar大判デジタル撮影計算機

pip install streamlit

import math

def sinar_p25_calculator():
    print("--- 伊藤さん専用: Sinar P & P25 撮影計算機 ---")
    
    # 基本設定 (Phase One P25)
    pixel_size_um = 9.0  # P25の画素ピッチ
    focal_length_mm = 90  # 使用レンズ (Fujinon 90mm等)
    
    # 許容錯乱円の定義 (デジタルバック用に厳しめに設定)
    # 通常の4x5フィルム(0.1mm)に対し、P25では約0.03mm程度が理想
    coc_mm = 0.03 

    try:
        # 入力セクション (レーザー距離計の数値を入力)
        dist_near = float(input("近点までの距離 (m): "))
        dist_far = float(input("遠点までの距離 (m): "))
        
        if dist_near >= dist_far:
            print("エラー: 遠点は近点より遠い必要があります。")
            return

        # 1. 最適なピント合わせ距離 (調和平均)
        focus_dist = (2 * dist_near * dist_far) / (dist_near + dist_far)
        
        # 2. 必要絞り値 (F値) の計算
        # 計算式: F = (f^2 * ΔD) / (2 * CoC * D1 * D2)
        delta_d = dist_far - dist_near
        required_f = (focal_length_mm**2 * delta_d * 1000) / (2 * coc_mm * (dist_near * 1000) * (dist_far * 1000))
        
        # 3. 回折限界のチェック
        # 一般的に青色光(550nm)基準で、エアリーディスク径が画素ピッチの2倍を超えるとボケが目立つ
        diffraction_limit_f = pixel_size_um / 1.5 

        print("\n" + "="*40)
        print(f"【計算結果】")
        print(f"■ 推奨ピント位置: {focus_dist:.3f} m")
        print(f"■ 理論上の必要絞り: F {required_f:.1f}")
        
        print("\n【現場でのアクション】")
        if required_f > 16:
            print(f"⚠️ 警告: F{required_f:.1f}は絞りすぎです(回折ボケが発生します)。")
            print("   → Sinar Pのアオリ（ティルト）を使い、ピント面を倒してください。")
        elif required_f < 5.6:
            print(f"✅ F8〜11で十分にパンフォーカスが得られます。")
        else:
            print(f"👉 レンズを F {math.ceil(required_f)} 程度まで絞ってください。")
            
        print(f"\n※P25の回折限界目安: F {diffraction_limit_f:.1f}")
        print("="*40)

    except ValueError:
        print("数値を入力してください。")

sinar_p25_calculator()
