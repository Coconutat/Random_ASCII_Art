import requests
from PIL import Image
import numpy as np
import io

def fetch_random_wallhaven_image():
    response = requests.get("https://wallhaven.cc/api/v1/search?apikey=/!!!API_KEY!!!/&page=1&purity=110&sorting=random")
    image_url = response.json()['data'][0]['path']
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
    image_url = fetch_random_wallhaven_image()
    ascii_art = image_to_ascii(image_url)
    print(ascii_art)
