#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import wave
import os
from src.Editor import Editor
import src.FormatShaper as FormatShaper


@pytest.fixture()
def test_file():
    return 'test_files/Apollo.wav'


@pytest.fixture()
def editor(test_file):
    return Editor(test_file)


@pytest.fixture()
def file_to_concatenate():
    return 'test_files/small_file.wav'


@pytest.fixture()
def small_editor(file_to_concatenate):
    return Editor(file_to_concatenate)


def test_speed_change(test_file, editor):
    file = wave.open(test_file)
    start_speed = file.getframerate()
    file.close()
    editor.change_speed(0.1)
    assert editor.frame_rate == start_speed * 0.1


def test_volume_back(editor):
    editor.change_volume(2)
    assert editor.volume == 1


def test_undo(editor):
    editor.change_volume(2)
    assert editor.changes_stack
    editor.undo()
    assert not editor.changes_stack
    with pytest.raises(Exception) as e_info:
        editor.undo()
    assert str(e_info.value) == "Начальный файл. Нет изменений, которые можно было бы отменить"


def test_cut(editor):
    editor.cut(0, 30)
    assert len(editor.frames) == editor.sample_width * editor.channels_number * editor.frame_rate * 30


def test_concatenate(editor, file_to_concatenate):
    starting_len = len(editor.frames)
    file = wave.open(file_to_concatenate)
    adding_len = len(file.readframes(-1))
    file.close()
    editor.concatenate(file_to_concatenate)
    assert starting_len + adding_len == len(editor.frames)


def test_reverse(small_editor):
    starting_bytes = small_editor.frames
    starting_len = len(starting_bytes)
    small_editor.reverse()
    assert starting_len == len(small_editor.frames)
    small_editor.reverse()
    assert starting_bytes == small_editor.frames


def test_clear(editor):
    editor.change_volume(3)
    directory = os.path.join('ChangesHistory')
    files = os.listdir(directory)
    assert files
    editor.clear_changes_history()
    files_after_clear = os.listdir(directory)
    assert not files_after_clear


def test_wrong_input(small_editor):
    with pytest.raises(Exception) as e_info:
        small_editor.cut(-1, 5)
    assert str(e_info.value) == 'Начало отрезка должно быть не меньше 0'

    with pytest.raises(Exception) as e_info:
        small_editor.cut(2, 1)
    assert str(e_info.value) == 'Конец фрагмента должен быть больше начала фрагмента'

    with pytest.raises(Exception) as e_info:
        small_editor.cut(11, 12)
    assert str(e_info.value) == 'Начало фрагмента должен быть не больше длины аудидорожки равной 10'

    with pytest.raises(Exception) as e_info:
        small_editor.cut(0, 12)
    assert str(e_info.value) == 'Конец фрагмента должен быть не больше длины аудидорожки равной 10'

    with pytest.raises(Exception) as e_info:
        small_editor.cut(0, 12)
    assert str(e_info.value) == 'Конец фрагмента должен быть не больше длины аудидорожки равной 10'

    with pytest.raises(Exception) as e_info:
        small_editor.change_volume(-1)
    assert str(e_info.value) == 'Коэффициент должен быть не меньше нуля 0'

    with pytest.raises(Exception) as e_info:
        small_editor.change_speed(-1)
    assert str(e_info.value) == 'Коэффициент должен быть больше нуля 0'


def test_format_shaper_help_funcs():
    with pytest.raises(Exception) as e_info:
        FormatShaper.check_file_existence('test_files/ap.wav')
    assert str(e_info.value) == "Файл test_files/ap.wav не существует"

    with pytest.raises(Exception) as e_info:
        FormatShaper.check_file_format('test_files/ap.mp4')
    assert str(e_info.value) == "Редактор не поддерживает формат .mp4"
