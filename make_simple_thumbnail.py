import os
import json
import textwrap
from PIL import Image, ImageDraw, ImageFont

# Change current directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def adjust_font_size(draw, text, font_path, max_width, max_height, initial_font_size):
    """
    指定された横幅と高さに収まるようにフォントサイズを調整する関数
    """
    font_size = initial_font_size
    font = ImageFont.truetype(font_path, font_size)
    while True:
        text_width = draw.textbbox((0, 0), text, font=font)[2]
        text_height = draw.textbbox((0, 0), text, font=font)[3]
        if text_width <= max_width and text_height <= max_height:
            break
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
    return font

def create_thumbnail_with_bottom_margin(json_path, background_path, output_path):
    # 背景画像の存在確認
    if not os.path.exists(background_path):
        raise FileNotFoundError(f"Background image not found: {background_path}")
    
    # JSONデータを読み込む
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    title = data["title"]
    best_answer = data["best_answer"]
    
    thumbnail_size = (1280, 720)
    bg_image = Image.open(background_path).convert("RGBA").resize(thumbnail_size)
    overlay = Image.new("RGBA", thumbnail_size, (0, 0, 0, 0))  # 透過レイヤー
    draw = ImageDraw.Draw(overlay)
    
    # フォントパスと初期設定
    font_path = "arial.ttf"  # 適宜変更
    initial_font_size = 60
    fixed_width = 1000
    title_height = 100
    text_height = 500
    bottom_margin = 50  # テキスト下のマージン

    # 全体の余白を計算
    total_content_height = title_height + text_height + bottom_margin
    total_margin = thumbnail_size[1] - total_content_height
    top_margin = total_margin // 2  # 上部の余白

    # タイトルのフォントサイズ調整
    title_font = adjust_font_size(draw, title, font_path, fixed_width, title_height, initial_font_size)
    title_x = (thumbnail_size[0] - fixed_width) // 2
    title_y = top_margin  # 上余白を適用
    draw.rectangle(
        [
            (title_x, title_y),
            (title_x + fixed_width, title_y + title_height)
        ],
        fill=(0, 0, 0, 150)  # 半透明の黒
    )
    title_text_x = title_x + (fixed_width - draw.textbbox((0, 0), title, font=title_font)[2]) // 2
    title_text_y = title_y + (title_height - draw.textbbox((0, 0), title, font=title_font)[3]) // 2
    draw.text((title_text_x, title_text_y), title, font=title_font, fill="white")
    
    # 中央テキストのフォントサイズ調整
    wrapped_text = textwrap.fill(best_answer, width=50)
    text_font = adjust_font_size(draw, wrapped_text, font_path, fixed_width, text_height, initial_font_size)
    text_x = title_x
    text_y = title_y + title_height + top_margin  # タイトルの下に余白を追加
    draw.rectangle(
        [
            (text_x, text_y),
            (text_x + fixed_width, text_y + text_height)
        ],
        fill=(0, 0, 0, 150)  # 半透明の黒
    )

    # 各行の描画
    text_lines = wrapped_text.split("\n")
    line_heights = [draw.textbbox((0, 0), line, font=text_font)[3] for line in text_lines]
    total_text_height = sum(line_heights)
    current_y = text_y + (text_height - total_text_height) // 2  # テキスト内で中央配置
    for i, line in enumerate(text_lines):
        line_width = draw.textbbox((0, 0), line, font=text_font)[2]
        line_x = text_x + (fixed_width - line_width) // 2
        draw.text((line_x, current_y), line, font=text_font, fill="white")
        current_y += line_heights[i]
    
    # テキスト下にマージンを追加（背景なし、マージン分を確保）
    bottom_y = text_y + text_height + bottom_margin

    # 透過背景を合成
    combined = Image.alpha_composite(bg_image, overlay)
    
    # サムネイルを保存
    combined.save(output_path, format="PNG")
    print(f"Thumbnail created: {output_path}")

# 実行例
create_thumbnail_with_bottom_margin(
    json_path="data.json",
    background_path="background.png",  # 背景画像のパス
    output_path="thumbnail.png"       # 出力ファイル名を固定
)
