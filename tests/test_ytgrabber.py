import sys
import os
import pytest
from selenium import webdriver
from xvfbwrapper import Xvfb
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

sys.path.append(os.getcwd())

from ytgrabber import YTGrabber


class TestYTGrabber:            
    def test_check_valid_url_not_corect_protocol(self):
        grabber = YTGrabber()
        with pytest.raises(ValueError) as exc_info:
            grabber._check_valid_url('http://www.youtube.com/channel/UCMXHtrkazQjeCOteE4sof8g/playlists')
        assert exc_info.type is ValueError   
            
    def test_check_valid_url_mistake_some_chars(self):
        grabber = YTGrabber()
        with pytest.raises(ValueError) as exc_info:
            grabber._check_valid_url('https://www.outube.com/chanel/UCMXHtrkazQjeCOteE4sof8g/playlists')
        assert exc_info.type is ValueError
    
    def test_check_valid_url_int(self):
        grabber = YTGrabber()
        with pytest.raises(TypeError) as exc_info:
            grabber._check_valid_url(123123)
        assert exc_info.type is TypeError
    
    def test_check_valid_url_random_chars(self):
        grabber = YTGrabber()
        with pytest.raises(ValueError) as exc_info:
            grabber._check_valid_url('sdfsdf')
        assert exc_info.type is ValueError

    def test_check_valid_url_empty_string(self):
        grabber = YTGrabber()
        with pytest.raises(ValueError) as exc_info:
            grabber._check_valid_url(' ') 
        assert exc_info.type is ValueError
        
    def test_run_application_page_not_found(self):
        with pytest.raises(ValueError) as exc_info:
            with YTGrabber() as grabber:
                assert grabber._get_page('https://www.youtube.com/channel/UCMXHtrkazQjeCOteE4sof8gj/playlists')
        assert exc_info.type is ValueError   
    
    def test_run_application_page_error(self):
        with pytest.raises(ValueError) as exc_info:
            with YTGrabber() as grabber:
                assert grabber._get_page('https://www.youtube.com/playlist?list=PLyIFQr1wryPLLpctn9JLqZzUiDN1vnzYu00')
        assert exc_info.type is ValueError
    
    def test_run_application_page_found(self):
        with YTGrabber() as grabber:
            assert grabber._get_page('https://www.youtube.com/playlist?list=PLyIFQr1wryPLLpctn9JLqZzUiDN1vnzYu') == True
    
    def test_run_application_get_content(self):        
        with YTGrabber() as grabber:
            assert grabber.get_content('https://www.youtube.com/playlist?list=PLyIFQr1wryPLLpctn9JLqZzUiDN1vnzYu') is not None
