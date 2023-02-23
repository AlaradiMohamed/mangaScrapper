# %%
import requests
import urllib
import os
import re

from bs4 import BeautifulSoup
from pathlib import Path
from PIL import Image
from io import BytesIO
from fpdf import FPDF

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from time import sleep

from webdriver_manager.chrome import ChromeDriverManager

# %%
def getImages(title, soup):
    path = f'/Users/mohamedalaradi/Desktop/projects/animeScarpper/manga/{title}/temp'
    Path(path).mkdir(parents=True, exist_ok=True)
    imgCounter = 0

    for img in soup.find_all('img'):
        classes = img.get('class')
        if classes and len(classes) > 0:
            if 'img-content' in classes[0].lower():
                imgUrl = img.get('src')
                imgCounter += 1

    return imgCounter, path    

# %%
def totalImages(html):
    soup = BeautifulSoup(html)
    title = soup.title.string.split('|')[0].strip().replace(' ', '_')
    totalImages, imagesPath = getImages(title, soup)
    return totalImages, imagesPath

# %%
def genPDF(imagesPath):
    image_extensions = ('.jpg', '.jpeg', '.png')
    imagesName = os.listdir(imagesPath)
    imagesName = [file for file in imagesName if file.endswith(image_extensions)]

    imagesName.sort(key=lambda f: int(re.sub('\D', '', f)))
    images = [Image.open(f'{imagesPath}/' + f)for f in imagesName]
    images = [image.convert('RGB') for image in images]
    pdfPath = '/'.join(imagesPath.split('/')[0:-1]) + '/' + imagesPath.split('/')[-2] + '.pdf'
    images[0].save(pdfPath, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])
    return pdfPath

# %%
def initiateScrapping(url, secondServer = True, headless=False):
    options = Options()
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Firefox(options=options, service_log_path='/Users/mohamedalaradi/Desktop/projects/animeScarpper/geckodriver.log')
    delay = 10
    delayTokens = 5

    driver.get(url)
    driver.maximize_window()

    if secondServer:
        for token in range(delayTokens):
            try:
                WebDriverWait(driver, (delay + token*5)).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/span/span[1]/a[2]'))).click()
                continue
            except TimeoutException:
                print('Loading took too much time!')

    html = driver.page_source
    imgCount, imagesPath = totalImages(html)

    for i in range(imgCount):
        with open(f'{imagesPath}/{i+1}.png', 'wb') as file:
            imgElement = WebDriverWait(driver, (10)).until(EC.visibility_of_element_located((By.XPATH, f'/html/body/div[1]/div[3]/img[{i+1}]')))
            file.write(imgElement.screenshot_as_png)

    driver.quit()

    pdfPath = genPDF(imagesPath)

    return pdfPath 


