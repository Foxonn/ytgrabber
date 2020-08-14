import re
import os
import requests
import selenium
from mylogger import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

from exception import PageNotFound, PageOops


def _run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError as err:
        return False


if _run_from_ipython():
    from xvfbwrapper import Xvfb


class YTGrabber:
    """
    Return dictionary with all videos, channel name, playlist name.
    """
    __SELECTOR_PLAYLIST_VIDEOS = "#contents #contents #contents > *"
    __SELECTOR_ALL_VIDEOS = "#contents #contents #items > *"
    __SELECTOR_SPINNER = "#contents #contents #continuations #spinner"
    __SELECTOR_NAME_PLAYLIST = ".yt-simple-endpoint.style-scope.yt-formatted-string"
    __SELECTOR_CHANNEL_NAME = ".style-scope.ytd-channel-name"
    __YOUTUBE_OOPS_PAGE = "https://www.youtube.com/oops"

    @staticmethod
    def __check_os_name() -> str:
        path_to_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_driver_dir = os.path.join(path_to_dir, 'driver')

        if os.name == 'nt':
            driver_path = os.path.join(path_to_driver_dir, "chromedriver.exe")
        else:
            driver_path = os.path.join(path_to_driver_dir, "chromedriver")

        if not os.path.isfile(driver_path):
            try:
                raise FileExistsError(driver_path)
            except Exception as err:
                logging.error(err)
                raise

        return driver_path

    def __check_valid_url(self, url: str) -> bool:
        self.__url = url.strip()

        if re.match(r"^https://www\.youtube\.com/user/[\W\w]+/videos$", self.__url):
            return True

        if re.match(r"^https://www\.youtube\.com/(playlist\?list=|channel/)[\W\w]+(/playlists|/videos)$", self.__url):
            return True

        if re.match(r"https://www\.youtube\.com/(playlist\?list=|channel/)[\W\w]+", self.__url):
            return True

        raise ValueError("URL is not correct!")

    def __find_html_block(self) -> None:
        try:
            self.__html = WebDriverWait(self.__driver, 3).until(
                EC.presence_of_element_located((By.TAG_NAME, "html")),
                "`html` tag not found !")
        except Exception as err:
            logging.error(err)
            raise

    def __get_page(self, url) -> bool:
        self.__check_valid_url(url)

        resp = requests.get(self.__url, allow_redirects=True)

        if resp.text.find("404 Not Found") >= 0:
            try:
                raise PageNotFound
            except Exception as err:
                logging.error(err)
                raise

        if resp.url == self.__YOUTUBE_OOPS_PAGE:
            try:
                raise PageOops
            except Exception as err:
                logging.error(err)
                raise

        self.__driver.get(self.__url)

        return True

    def __preloader_handler(self) -> None:
        while True:
            self.__html.send_keys(Keys.END)
            try:
                WebDriverWait(self.__driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.__SELECTOR_SPINNER)))
            except:
                break

    def __find_videos(self) -> selenium.webdriver.remote.webelement.WebElement:
        videos = self.__html.find_elements(By.CSS_SELECTOR, self.__SELECTOR_ALL_VIDEOS)

        if not videos:
            videos = self.__html.find_elements(By.CSS_SELECTOR, self.__SELECTOR_PLAYLIST_VIDEOS)

        if not videos:
            logging.error("Videos not found !")
            quit()

        return videos

    def __find_name_playlist(self) -> str:
        name_playlist = self.__html.find_elements(By.CSS_SELECTOR, self.__SELECTOR_NAME_PLAYLIST)
        return name_playlist[0] if name_playlist else None

    def __find_name_channel(self) -> str:
        channel_name = self.__html.find_elements(By.CSS_SELECTOR, self.__SELECTOR_CHANNEL_NAME)

        if channel_name[2]:
            channel_name = channel_name[2]

        if not channel_name.text:
            logging.error("Channel name not found !")
            quit()

        return channel_name

    def extract_videos(self, url: str) -> dict:
        """
        :param url: url of the video tab or playlist page
        :return: dict
        """
        self.__get_page(url)

        self.__find_html_block()

        videos = self.__find_videos()

        channel_name = self.__find_name_channel()

        playlist_name = self.__find_name_playlist()

        content = {
            "playlist": playlist_name.text if playlist_name else None,
            "channel": channel_name.text,
            "videos": [],
        }

        for video in videos:
            content['videos'].append({
                "title": video.find_element_by_id("video-title").get_attribute("title"),
                "href": video.find_element_by_id("video-title").get_attribute("href") or
                        video.find_element_by_class_name("ytd-thumbnail").get_attribute("href"),
                "thumbnail": video.find_element_by_id("img").get_attribute("src"),
            })

        return content

    def __init__(self) -> None:
        self.__driver = None
        self.__vdisplay = None

    def __call__(self, url: str) -> dict:
        """
        :param url: url of the video tab or playlist page
        :return: dict
        """
        return self.extract_videos(url)

    def __enter__(self) -> 'YTGrabber':
        logging.info("YTGrabber started working.")

        if _run_from_ipython():
            self.__vdisplay = Xvfb()
            self.__vdisplay.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

        driver_path = self.__check_os_name()

        self.__driver = webdriver.Chrome(options=options, executable_path=driver_path)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        logging.info("YTGrabber finished working.")

        if self.__driver:
            self.__driver.close()

        if _run_from_ipython() and self.vdisplay:
            self.__vdisplay.stop()


if __name__ == '__main__':
    with YTGrabber() as yt:
        print(yt(url='https://www.youtube.com/playlist?list=PLnwx-Ko_Jo_360x-41QTqiiG7lTWGn-Tp'))
