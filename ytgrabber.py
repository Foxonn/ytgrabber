import re
import requests
from selenium import webdriver
from xvfbwrapper import Xvfb
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

class YTGrabber:
    '''
    Класс принимает Youtube URL страниц, все плейлисты, плейлист и все видео, 
    и возваращает все видеоматериалы данной страницы.
    '''
    driver = None
    vdisplay = None
    
    def _check_valid_url(self, url):
        
        if type(url) is int:
            raise TypeError("URL is not to be int type!")
        
        self.url = url.strip()          
        
        if re.match(r"https://www\.youtube\.com/(playlist\?list=|channel/)[\w]+(/playlists|/videos)", self.url):
            return True
        
        if re.match(r"https://www\.youtube\.com/(playlist\?list=|channel/)[\w]+", self.url):
            return True
        
        raise ValueError("URL is not correct!")
    
    def _get_page(self, url):
        self._check_valid_url(url)       
                   
        resp = requests.get(self.url)
        
        if resp.text.find("404 Not Found") >= 0:
            raise ValueError("'{}' , страница не найдена либо не существует".format(self.url))
        
        if resp.text.find("Произошла ошибка! - YouTube") >= 0:
            raise ValueError("'{}' , Произошла ошибка! - YouTube".format(self.url))
            
        self.driver.get(self.url)
        
        return True
    
    def get_content(self, url):
        self._get_page(url)
        
        preload = True        
        
        html = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.TAG_NAME , "html")), "Содержимое не найден или его нет !")            
        
        while preload:    
            html.send_keys(Keys.END)
            try:
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#contents #contents #continuations #spinner")))
            except:
                preload = False
        
        items = self.driver.find_elements(By.CSS_SELECTOR , "#contents #contents #items > *")   
        
        if not items:
             items = self.driver.find_elements(By.CSS_SELECTOR , "#contents #contents #contents > *")
        
        if not items:
            raise ValueError("Содержимое не найден или его нет !")
        
        videos = []

        for item in items:
            videos.append({
                "title": item.find_element_by_id("video-title").get_attribute("title"),
                "href": item.find_element_by_id("video-title").get_attribute("href") or item.find_element_by_class_name("ytd-thumbnail").get_attribute("href"),
                "thumbnail": item.find_element_by_id("img").get_attribute("src"),
            })
        
        return videos
    
    def __enter__(self):
        self.vdisplay = Xvfb()
        self.vdisplay.start()
        
        options = webdriver.ChromeOptions()
        options.handless = False
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")

        self.driver = webdriver.Chrome(options=options, executable_path="driver/chromedriver")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.close()
            
        if self.vdisplay:
            self.vdisplay.stop()