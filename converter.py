import os
import subprocess

PATH_TO_FFMPEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libs', 'ffmpeg', "bin")
os.environ["PATH"] += os.path.pathsep + PATH_TO_FFMPEG


class YTConverter:
    __allow_extensions = ['webm', 'mp4']

    def __init__(self, dir_files: str):
        self.__dir_files = dir_files

    @staticmethod
    def _clear(file: str) -> None:
        if os.path.isfile(file):
            os.unlink(file)

    def _check_extension(self, file_name: str):
        name, extension = file_name.split(".")

        if extension in self.__allow_extensions:
            return True

        return False

    def convert(self) -> None:
        for file in os.scandir(self.__dir_files):
            path_to_file, name_file = file.path, file.name

            if os.path.isdir(file.path):
                continue

            if not self._check_extension(name_file):
                continue

            save_to = os.path.join(self.__dir_files)

            if not os.path.isdir(save_to):
                os.makedirs(save_to)

            path_to_new_file = os.path.join(self.__dir_files, 'audio', "%s.mp3" % name_file.split(".")[0])

            res = subprocess.call(f"ffmpeg -loglevel error -y -i {path_to_file} -acodec libmp3lame {path_to_new_file}")

            if res == 0 and os.path.isfile(path_to_new_file):
                self._clear(path_to_file)
                print(f"File '{file.name}' converted.")
                continue

            print(f"File '{file.name}' failed converted.")


if __name__ == '__main__':
    ytc = YTConverter(r"D:\Development\py-laboratory\newretrowave\essential-retro-electro-tracks-newretrowave-certified")
    ytc.convert()
