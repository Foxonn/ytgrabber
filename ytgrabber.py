import re
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions


def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


if run_from_ipython:
    from xvfbwrapper import Xvfb


class YTGrabber:
    '''
    Класс принимает Youtube URL страниц, все плейлисты, плейлист и все видео, 
    и возваращает все видеоматериалы данной страницы.
    '''

    def _check_valid_url(self, url):

        if type(url) is int:
            raise TypeError("URL is not to be int type!")

        self.__url = url.strip()

        if re.match(r"^https://www\.youtube\.com/user/[\W\w]+/videos$", self.__url):
            return True

        if re.match(r"^https://www\.youtube\.com/(playlist\?list=|channel/)[\W\w]+(/playlists|/videos)$", self.__url):
            return True

        if re.match(r"https://www\.youtube\.com/(playlist\?list=|channel/)[\W\w]+", self.__url):
            return True

        raise ValueError("URL is not correct!")

    def _get_page(self, url):
        self._check_valid_url(url)

        resp = requests.get(self.__url)

        if resp.text.find("404 Not Found") >= 0:
            raise ValueError("'{}' , страница не найдена либо не существует".format(self.__url))

        if resp.text.find("Произошла ошибка! - YouTube") >= 0:
            raise ValueError("'{}' , Произошла ошибка! - YouTube".format(self.__url))

        self.__driver.get(self.__url)

        return True

    @staticmethod
    def run_from_ipython():
        try:
            __IPYTHON__
            return True
        except NameError:
            return False

    def get_content(self, url):
        self._get_page(url)

        preload = True

        html = WebDriverWait(self.__driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "html")),
                                                     "Содержимое не найден или его нет !")

        while preload:
            html.send_keys(Keys.END)
            try:
                WebDriverWait(self.__driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#contents #contents #continuations #spinner")))
            except:
                preload = False

        items = self.__driver.find_elements(By.CSS_SELECTOR, "#contents #contents #items > *")

        if not items:
            items = self.__driver.find_elements(By.CSS_SELECTOR, "#contents #contents #contents > *")

        if not items:
            raise ValueError("Содержимое не найден или его нет !")

        videos = []

        for item in items:
            videos.append({
                "title": item.find_element_by_id("video-title").get_attribute("title"),
                "href": item.find_element_by_id("video-title").get_attribute("href") or item.find_element_by_class_name(
                    "ytd-thumbnail").get_attribute("href"),
                "thumbnail": item.find_element_by_id("img").get_attribute("src"),
            })

        return videos

    def __init__(self):
        self.__driver = None
        self.__vdisplay = None

    def __call__(self, url):
        self.get_content(url)

    def __enter__(self):

        if run_from_ipython:
            self.__vdisplay = Xvfb()
            self.__vdisplay.start()

        options = webdriver.ChromeOptions()
        options.handless = False
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")

        if os.name == 'nt':
            executable_path = "driver/chromedriver.exe"
        else:
            executable_path = "driver/chromedriver"

        self.__driver = webdriver.Chrome(options=options, executable_path=executable_path)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__driver:
            self.__driver.close()

        if run_from_ipython and self.vdisplay:
            self.__vdisplay.stop()


if __name__ == '__main__':
    with YTGrabber() as yt:
        print(yt('https://www.youtube.com/user/FlandyMusic/videos'))
