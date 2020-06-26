import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grabber import YTGrabber
from exception import PageNotFound, PageOops


class TestYTGrabber:
    def test_check_valid_url_not_corect_protocol(self):
        with pytest.raises(ValueError) as exc_info:
            with YTGrabber() as ytg:
                ytg('http://www.youtube.com/channel/UCMXHtrkazQjeCOteE4sof8g/playlists')
        assert exc_info.type is ValueError

    def test_check_valid_url_mistake_some_chars(self):
        with pytest.raises(ValueError) as exc_info:
            with YTGrabber() as ytg:
                ytg('https://www.outube.com/chanel/UCMXHtrkazQjeCOteE4sof8g/playlists')
        assert exc_info.type is ValueError

    def test_check_valid_url_random_chars(self):
        with pytest.raises(ValueError) as exc_info:
            with YTGrabber() as ytg:
                ytg('sdfsdf')
        assert exc_info.type is ValueError

    def test_check_valid_url_empty_string(self):
        with pytest.raises(ValueError) as exc_info:
            with YTGrabber() as ytg:
                ytg(' ')
        assert exc_info.type is ValueError

    def test_run_application_page_not_found(self):
        with pytest.raises(PageNotFound) as exc_info:
            with YTGrabber() as ytg:
                ytg("https://www.youtube.com/channel/UCMXHtrkazQjeCOteE4sof8gj/playlists")
        assert exc_info.type is PageNotFound

    def test_run_application_page_error(self):
        with pytest.raises(PageOops) as exc_info:
            with YTGrabber() as ytg:
                ytg("https://www.youtube.com/playlist?list=PLyIFQr1wryPLLpctn9JLqZzUiDN1vnzYu00")
        assert exc_info.type is PageOops

    def test_run_application_get_content(self):
        with YTGrabber() as ytg:
            assert type(ytg('https://www.youtube.com/playlist?list=PLyIFQr1wryPLLpctn9JLqZzUiDN1vnzYu')) == dict
