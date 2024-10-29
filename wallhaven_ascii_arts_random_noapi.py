import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
import numpy as np
import io
import random
import uuid
from datetime import datetime

# Wallhaven 随机图片页面地址
BASE_URL = "https://wallhaven.cc/random/"
# 设置请求头，避免被服务器拒绝
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}
# 常见图片后缀
COMMON_EXTENSIONS = ["jpg", "png", "webp"]

def get_random_image_urls():
    """获取随机图片的真实 URL 列表。"""
    response = requests.get(BASE_URL, headers=HEADERS)
    response.raise_for_status()
    
    # 解析 HTML 内容
    soup = BeautifulSoup(response.text, 'html.parser')
    preview_elements = soup.select("#thumbs ul li figure a.preview")

    image_urls = []
    for preview in preview_elements:
        # 获取图片ID
        href = preview['href']
        image_id = href.split("/")[-1]  # 提取图片ID

        # 构造基础图片 URL（未加文件格式）
        base_image_url = f"https://w.wallhaven.cc/full/{image_id[:2]}/wallhaven-{image_id}"
        image_urls.append(base_image_url)
    
    return image_urls

def fetch_image(image_base_url):
    """尝试多个后缀，找到有效图片 URL 并返回图片二进制内容。"""
    for ext in COMMON_EXTENSIONS:
        image_url = f"{image_base_url}.{ext}"
        try:
            response = requests.get(image_url, headers=HEADERS)
            response.raise_for_status()
            return response.content  # 成功获取图片，返回内容
        except requests.exceptions.HTTPError:
            print(f"尝试 {image_url} 失败，继续尝试下一个后缀...")
    print("所有后缀均尝试失败，跳过该图片。")
    return None

def image_to_ascii(image_data):
    """将图片二进制内容转换为 ASCII 艺术图像。"""
    image = Image.open(io.BytesIO(image_data)).convert("L")  # 转为灰度
    ascii_chars = "@%#*+=-:. "  # 使用的字符集从暗到亮
    pixels = np.array(image)

    # 根据灰度值生成 ASCII 字符
    ascii_image = ""
    for row in pixels:
        ascii_image += "".join([ascii_chars[min(pixel // 25, len(ascii_chars) - 1)] for pixel in row]) + "\n"
    
    return ascii_image

def save_ascii_art(ascii_art):
    """保存 ASCII 艺术图像到 arts 目录下，文件名为日期加 UUID，格式为 .md。"""
    # 创建 arts 目录
    if not os.path.exists("arts"):
        os.makedirs("arts")
    
    # 文件名格式
    filename = f"arts/{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4()}.md"
    
    # 将 ASCII 艺术图像保存到文件
    with open(filename, "w") as f:
        f.write(ascii_art)
    print(f"ASCII Art 已保存到 {filename}")

def main():
    # 获取随机图片 URL 列表
    image_urls = get_random_image_urls()
    
    # 随机选择一个图片 URL，尝试生成 ASCII Art
    if image_urls:
        random.shuffle(image_urls)
        
        for base_image_url in image_urls:
            print(f"尝试获取图片 URL: {base_image_url}")
            image_data = fetch_image(base_image_url)
            if image_data:
                ascii_art = image_to_ascii(image_data)  # 生成 ASCII 艺术图像
                save_ascii_art(ascii_art)  # 保存生成的 ASCII 艺术图像
                break  # 成功生成 ASCII Art 后退出循环
            else:
                print("获取图像失败，尝试下一个图片 URL。")
    else:
        print("未找到任何图片。")

if __name__ == "__main__":
    main()