import pytest
import wave
import os
from src.Editor import Editor
from src.FormatShaper import FormatShaper


@pytest.fixture()
def test_file():
    path = os.path.join('test_files', 'Apollo.mp3')
    return path


@pytest.fixture()
def editor(test_file):
    return Editor(test_file)


def test_speed_change(test_file, editor):
    with wave.open(test_file) as file:
        start_speed = file.getframerate()
    editor.change_speed(0.1)
    assert editor.frame_rate == start_speed * 0.1