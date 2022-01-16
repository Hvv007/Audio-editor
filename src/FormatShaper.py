#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import contextlib

supported_formats = {'.mp3', '.wav', '.flac'}


def check_file_existence(filename):
    if not os.path.isfile(filename):
        raise ValueError("Файл {} не существует".format(filename))


def check_file_format(filename):
    file_format = os.path.splitext(filename)[1]
    if file_format not in supported_formats:
        raise TypeError("Редактор не поддерживает формат {}".format(file_format))


class FormatShaper:
    @staticmethod
    def change_format(filename, export_path):
        check_file_existence(filename)
        check_file_format(filename)
        check_file_format(export_path)
        with contextlib.redirect_stdout(None):
            subprocess.call(['ffmpeg', '-i', filename, export_path],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
