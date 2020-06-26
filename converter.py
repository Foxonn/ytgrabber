import os
import subprocess
from mylogger import logging

# need download to extract dir libs, https://ffmpeg.zeranoe.com/builds/

PATH_TO_FFMPEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libs', 'ffmpeg', "bin")
os.environ["PATH"] += os.path.pathsep + PATH_TO_FFMPEG


class YTConverter:
    """
    Converted [.webm, .mp4] file to .mp3 file
    """
    __allow_extensions: list = ['webm', 'mp4']
    __files: list = []
    __dir_files: str = ''

    @staticmethod
    def __del_source_file(file: str) -> None:
        if os.path.isfile(file):
            os.unlink(file)

    @classmethod
    def __filter_files(cls, dir_files):
        if not os.path.isdir(dir_files):
            try:
                raise NotADirectoryError
            except Exception as err:
                logging.exception(err)
                raise

        for file in os.scandir(dir_files):
            for ext in cls.__allow_extensions:
                if file.name.endswith(ext):
                    cls.__files.append(file)

        return True if cls.__files else False

    @classmethod
    def convert(cls, dir_files) -> None:
        """
        :param dir_files: path to directory containing [.webm, .mp4] files.
        """
        if not cls.__filter_files(dir_files):
            logging.warning("Files not found!")

        for file in cls.__files:
            path_to_file, file_name = file.path, file.name

            if os.path.isdir(file.path):
                continue

            save_to = os.path.join(dir_files)

            if not os.path.isdir(save_to):
                os.makedirs(save_to)

            path_to_new_file = os.path.join(dir_files, "%s.mp3" % file_name.split(".")[0])

            logging.info(f"Started converting file '{file.name}'.")

            res = subprocess.call(f"ffmpeg -loglevel error -y -i {path_to_file} -acodec libmp3lame {path_to_new_file}")

            if res == 0 and os.path.isfile(path_to_new_file):
                cls.__del_source_file(path_to_file)
                logging.info(f"Finished converting file '{file.name}'.")
                continue

            logging.error(f"Error converting file '{file.name}'.")


if __name__ == '__main__':
    YTConverter.convert(r"D:\music\alina-gingertail")
