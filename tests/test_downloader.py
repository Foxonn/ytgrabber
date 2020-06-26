import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from downloader import YTDownloader

class TestYTDownloader:
    def test_video_permission_denide(self):
        ytd = YTDownloader()

        videos = {
            "videos": [
                {"href": "https://www.youtube.com/watch?v=b6J7aez8-qU&list=PLyIFQr1wryPKdWJzPV-bRccsnJqbNP1a6&index=21",
                 "title": "Flux Gemini - Andromeda"}],
            "channel": "NewRetroWave",
            "playlist": "NRW Presents: Supreme Spacewave",
        }

        ytd.start(videos=videos, type='audio')
