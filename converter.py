""" Converted [.webm, .mp4] file to .mp3 file """

import os
from mylogger import logging
import subprocess

# need download to extract dir libs, https://ffmpeg.zeranoe.com/builds/

PATH_TO_FFMPEG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'libs', 'ffmpeg', "bin")
os.environ["PATH"] += os.path.pathsep + PATH_TO_FFMPEG


def _del_source_file(file_path: str) -> None:
    if os.path.isfile(file_path):
        os.unlink(file_path)


def _filter_files(dir_files, allow_extensions: list = ['webm', 'mp4']):
    files = []

    if not os.path.isdir(dir_files):
        try:
            raise NotADirectoryError
        except Exception as err:
            logging.exception(err)
            raise

    for file in os.scandir(dir_files):
        for ext in allow_extensions:
            if file.name.endswith(ext):
                files.append(file)

    return files if files else False


def convert(dir_files, remove: bool = False) -> None:
    """
    :param dir_files: path to directory containing [.webm, .mp4] files.
    """
    files = _filter_files(dir_files)

    if not files:
        logging.warning("Files not found!")
        return False

    for file in files:
        path_to_file, file_name = file.path, file.name

        if os.path.isdir(file.path):
            continue

        save_to = os.path.join(dir_files)

        if not os.path.isdir(save_to):
            os.makedirs(save_to)

        path_to_new_file = os.path.join(
            dir_files,
            "%s.mp3" % file_name.split(".")[0])

        logging.info(f"Started converting file '{file.name}'.")

        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-i",
               path_to_file, "-acodec", "libmp3lame", path_to_new_file]

        subprocess.run(cmd)

        if remove and os.path.exists(path_to_file):
            os.unlink(path_to_file)
