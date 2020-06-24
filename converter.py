import os
import subprocess

# need download to extract dir libs, https://ffmpeg.zeranoe.com/builds/

PATH_TO_FFMPEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libs', 'ffmpeg', "bin")
os.environ["PATH"] += os.path.pathsep + PATH_TO_FFMPEG


class YTConverter:
    """
    Converted [.webm, .mp4] file to .mp3 file
    """
    __allow_extensions = ['webm', 'mp4']

    @staticmethod
    def _del_source_file(file: str) -> None:
        if os.path.isfile(file):
            os.unlink(file)

    @classmethod
    def _check_extension(cls, file_name: str) -> bool:
        name, extension = file_name.split(".")

        if extension in cls.__allow_extensions:
            return True

        return False

    @classmethod
    def convert(cls, dir_files: str) -> None:
        """
        :param dir_files: path to directory containing [.webm, .mp4] files.
        """

        if not os.path.isdir(dir_files):
            raise NotADirectoryError

        for file in os.scandir(dir_files):
            path_to_file, file_name = file.path, file.name

            if os.path.isdir(file.path):
                continue

            if not cls._check_extension(file_name=file_name):
                continue

            save_to = os.path.join(dir_files)

            if not os.path.isdir(save_to):
                os.makedirs(save_to)

            path_to_new_file = os.path.join(dir_files, "%s.mp3" % file_name.split(".")[0])

            res = subprocess.call(f"ffmpeg -loglevel error -y -i {path_to_file} -acodec libmp3lame {path_to_new_file}")

            if res == 0 and os.path.isfile(path_to_new_file):
                cls._del_source_file(path_to_file)
                print(f"File '{file.name}' converted.")
                continue

            print(f"File '{file.name}' failed converted.")


if __name__ == '__main__':
    YTConverter.convert(r"D:\music\newretrowave\nrw-presents-supreme-spacewave")
