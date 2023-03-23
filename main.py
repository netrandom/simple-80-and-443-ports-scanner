import socket
import random
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import json
import requests
import base64

tgtoken = ''
imgbbkey = ''
chatid = 
ports = [80, 443]
restrictedtitle = ['Invalid URL', 'Default Web Site Page', 'ERROR: The request could not be satisfied', '403 Forbidden', '404 Not Found', '410 Gone', '503 Service Temporarily Unavailable', '500 Internal Server Error']
bot = Bot(token=tgtoken)
session = requests.Session()

async def scan_port(ip_address, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            result = s.connect_ex((ip_address, port))
            if result == 0:
                return True
            else:
                return False
    except:
        return False

async def main():
    while True:
        ip_address = ".".join(str(random.randint(0, 255)) for _ in range(4))
        open_ports = [port for port in ports if await scan_port(ip_address, port)]
        print(f"Scanning {str(ip_address)}")
        if open_ports:
            driver = webdriver.Firefox()
            try:
                if 80 in open_ports:
                    driver.get(f'http://{ip_address}:80')
                elif 443 in open_ports:
                    driver.get(f'https://{ip_address}:443')
                time.sleep(5)
                server_header = driver.execute_script("""
                    var xhr = new XMLHttpRequest();
                    xhr.open('HEAD', window.location.href, false);
                    xhr.send(null);
                    return xhr.getResponseHeader('Server');
                """)
                title = driver.title
                geo = session.get(f'http://ip-api.com/json/{ip_address}').json()
                driver.save_screenshot('screenshot.png')
                with open("screenshot.png", "rb") as file:
                    cryptimg = base64.b64encode(file.read()).decode('utf-8')
                payload = {
                    "key": imgbbkey,
                    "image": cryptimg,
                }
                res = requests.post("https://api.imgbb.com/1/upload", payload)
                response_dict = json.loads(res.text)
                image_url = response_dict['data']['url']
                driver.quit()
                message = f"Server: #{server_header}\nTitle: {title}\nGeo: {geo['country']}/{geo['city']}\n{'http' if 80 in open_ports else 'https'}://{ip_address}:{80 if 80 in open_ports else 443}/"
                if title not in restrictedtitle:
                    await bot.send_photo(chat_id=chatid, photo=image_url, caption=message)
            except WebDriverException as e:
                driver.quit()



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
