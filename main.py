import os
import argparse
import sys
from CommandExecutor import CommandExecutor
from src.FormatShaper import FormatShaper
from src.Editor import Editor


def prepare_to_run(directory, opened_file):
    format_changer = FormatShaper
    Editor.clear_changes_history()
    first_editor_file = os.path.join(directory, 'ChangesHistory', 'start_file.wav')
    try:
        format_changer.change_format(opened_file, first_editor_file)
    except ValueError or TypeError as e:
        sys.exit(e)
    return format_changer, Editor(first_editor_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Audio-editor", add_help=False,
                                     usage='main.py FILE_NAME')
    parser.add_argument("-h", "--help", help="показывает это сообщение", action="help")
    parser.add_argument("FILE_NAME", help="название файла")
    args = parser.parse_args()
    directory = os.path.dirname(__file__)
    changer, editor = prepare_to_run(directory, args.FILE_NAME)
    command_caller = CommandExecutor(editor, changer, directory)
    command_caller.run()
