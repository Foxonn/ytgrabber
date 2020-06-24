import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grabber import YTGrabber
from exception import PageNotFound, PageOops, VideoRestrictions


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
        with pytest.raises(PageNotFound) as exc_info:
            with YTGrabber() as grabber:
                grabber._get_page('https://www.youtube.com/channel/UCMXHtrkazQjeCOteE4sof8gj/playlists')
        assert exc_info.type is PageNotFound

    def test_run_application_page_error(self):
        with pytest.raises(PageOops) as exc_info:
            with YTGrabber() as grabber:
                grabber._get_page('https://www.youtube.com/playlist?list=PLyIFQr1wryPLLpctn9JLqZzUiDN1vnzYu00')
        assert exc_info.type is PageOops

    def test_run_application_page_found(self):
        with YTGrabber() as grabber:
            assert grabber._get_page('https://www.youtube.com/playlist?list=PLyIFQr1wryPLLpctn9JLqZzUiDN1vnzYu') == True

    def test_run_application_get_content(self):
        with YTGrabber() as grabber:
            assert type(grabber.get_content('https://www.youtube.com/playlist?list=PLyIFQr1wryPLLpctn9JLqZzUiDN1vnzYu')) == dict
