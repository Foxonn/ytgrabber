"Downloading audio track from YouTube video file."

import os
import pytube
from grabber import YTGrabber
from mylogger import logging
from slugify import slugify
from urllib.error import URLError
from time import sleep
import json


def start_download(datas: YTGrabber, to_save: str, type='audio') -> None:
    path_destination = _downloader(type, to_save, **datas)
    logging.info('YTDownloader work complete.')
    return path_destination


def get_audio(link) -> pytube.Stream:
    try:
        yt = pytube.YouTube(link)
    except json.decoder.JSONDecodeError as err:
        logging.error(err)
        return False

    return yt.streams.filter(only_audio=True).last()


def get_video(link: str) -> pytube.Stream:
    try:
        yt = pytube.YouTube(link)
    except json.decoder.JSONDecodeError as err:
        logging.error(err)
        return False

    return yt.streams.get_lowest_resolution()


def _check_files_is_downloaded(file_name, path_destination) -> bool:
    files = os.scandir(path_destination)

    for file in files:
        if file_name == file.name.split(".")[0]:
            return True

    return False


def _downloader(type, to_save, **kwargs) -> str:
    if type not in ['audio', 'video']:
        try:
            raise ValueError("Type '%s' not support." % type)
        except Exception as err:
            logging.exception(err)

    path_destination = _check_directory(kwargs['channel'],
                                        kwargs['playlist'],
                                        to_save)

    for video in kwargs['videos']:
        filename = slugify(video['title'])

        if _check_files_is_downloaded(filename, path_destination):
            logging.info("Downloaded: %s" % video['href'])
            continue

        logging.info("Start download: %s" % video['href'])

        while True:
            try:
                if type == 'audio':
                    get_audio(video['href']).download(
                        output_path=path_destination,
                        filename=filename
                    )

                elif type == 'video':
                    get_video(video['href']).download(
                        output_path=path_destination,
                        filename=filename
                    )

                logging.info("Download complete: %s" % video['href'])
                break

            except pytube.exceptions.RegexMatchError:
                logging.warning("Video get permission denied.")
                break
            except URLError as err:
                logging.warning(err)
                _sleep()

    return path_destination


def _check_directory(channel, playlist, to_save) -> None:
    channel = slugify(channel).lower()
    playlist = slugify(playlist).lower() if playlist else None

    if to_save:
        if os.path.isdir(to_save):

            if playlist:
                path_destination = os.path.join(to_save, channel, playlist)
            else:
                path_destination = os.path.join(to_save, channel)

            if not os.path.isdir(path_destination):
                os.makedirs(path_destination)
        else:
            try:
                raise NotADirectoryError(to_save)
            except Exception as err:
                logging.exception(err)
                raise

    return path_destination


def _sleep(wait: int = 10):
    sleep_ = wait
    logging.info("***** sleep %s sec. *****" % sleep_)
    sleep(sleep_)
