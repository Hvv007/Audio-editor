import os
import subprocess
import contextlib

supported_formats = {'.mp3', '.wav', '.flac'}


def check_file_existence(filename):
    if not os.path.isfile(filename):
        raise ValueError(f"Файл {filename} не существует")


def check_file_format(filename):
    ext = os.path.splitext(filename)[1]
    if ext not in supported_formats:
        raise TypeError(f"Редактор не поддерживает формат {ext}")


class FormatShaper:
    @staticmethod
    def change_format(filename, export_path):
        check_file_existence(filename)
        check_file_format(filename)
        check_file_format(export_path)
        with contextlib.redirect_stdout(None):
            subprocess.call(['ffmpeg', '-i', filename, export_path],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
