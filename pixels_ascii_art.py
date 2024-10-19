import requests
from PIL import Image
import numpy as np
import io
import random

def fetch_random_image():
    api_key = 'YOUR_PEXELS_API_KEY'  # 替换为你的Pexels API密钥
    response = requests.get(f'https://api.pexels.com/v1/search?query=nature&per_page=15', 
                            headers={'Authorization': api_key})
    data = response.json()
    image_url = random.choice(data['photos'])['src']['original']
    return image_url

def image_to_ascii(image_url):
    response = requests.get(image_url)
    image = Image.open(io.BytesIO(response.content))
    image = image.resize((100, 50))  # 调整大小以适应ASCII
    image = image.convert('L')  # 转为灰度
    ascii_chars = "@%#*+=-:. "
    
    pixels = np.array(image)
    ascii_image = "".join([ascii_chars[pixel // 32] for pixel in pixels.flatten()])
    return "\n".join([ascii_image[i:i + 100] for i in range(0, len(ascii_image), 100)])

if __name__ == "__main__":
    image_url = fetch_random_image()
    ascii_art = image_to_ascii(image_url)
    print(ascii_art)
