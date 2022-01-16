import os
import sys
import wave
import audioop


class Editor:
    def __init__(self, audio_path):
        self.sample_width = None
        self.frame_rate = None
        self.channels_number = None
        self.frames = None
        self.volume = 1
        self.change_number = 0
        self.current_change = audio_path
        self.set_current_change()
        self.changes_stack = []
        self.new_change = None

    def set_current_change(self):
        try:
            with wave.open(self.current_change, 'rb') as file:
                self.sample_width = file.getsampwidth()
                self.frame_rate = file.getframerate()
                self.channels_number = file.getnchannels()
                self.frames = file.readframes(-1)
        except wave.Error as e:
            print("Файл не может быть преобразован в поддерживаемый формат" + e.args[0])
            sys.exit()

    def move_new_to_current_change(self):
        self.changes_stack.append(self.current_change)
        self.current_change = self.new_change
        self.change_number += 1

    def make_new_change(self):
        filename = f'change_step_number_{self.change_number}.wav'
        self.new_change = os.path.join(os.path.dirname(__file__), '../ChangesHistory', filename)

    def set_new_change(self):
        self.make_new_change()
        with wave.open(self.new_change, 'wb') as new_file:
            new_file.setsampwidth(self.sample_width)
            new_file.setframerate(self.frame_rate)
            new_file.setnchannels(self.channels_number)
            new_file.writeframes(audioop.mul(self.frames, self.sample_width, self.volume))
        self.volume = 1
        self.move_new_to_current_change()

    def change_volume(self, new_volume_coef):
        volume_coef = float(new_volume_coef)
        if volume_coef < 0:
            raise ValueError('Коэффициент должен быть не меньше нуля 0')
        self.volume = volume_coef
        self.set_new_change()
        print(f'Громкость изменена с коэффициентом {volume_coef}')

    def change_speed(self, new_speed_coef):
        speed_coef = float(new_speed_coef)
        if speed_coef <= 0:
            raise ValueError('Коэффициент должен быть больше нуля 0')
        self.frame_rate *= speed_coef
        self.set_new_change()
        print(f'Скорость изменена с коэффициентом {speed_coef}')

    def cut(self, start, end):
        start = int(start)
        end = int(end)
        if start < 0:
            raise ValueError('Начало отрезка должно быть не меньше 0')
        if end <= start:
            raise ValueError('Конец фрагмента должен быть больше начала фрагмента')
        frames_per_second = self.sample_width * self.frame_rate * self.channels_number
        audio_len = len(self.frames) // frames_per_second
        first_byte = start * frames_per_second
        last_byte = end * frames_per_second
        if first_byte >= len(self.frames):
            raise ValueError(f'Начало фрагмента должен быть не больше длины аудидорожки равной {audio_len}')
        if end > audio_len:
            raise ValueError(f'Конец фрагмента должен быть не больше длины аудидорожки равной {audio_len}')
        self.frames = self.frames[first_byte:last_byte]
        self.set_new_change()
        print(f'Вырезан фрагмент начиная с {start} по {end} секунду')

    def concatenate(self, new_file):
        with wave.open(new_file, 'rb') as file_to_concatenate:
            sample_width = file_to_concatenate.getsampwidth()
            rate = file_to_concatenate.getframerate()
            channels = file_to_concatenate.getnchannels()
            frames = file_to_concatenate.readframes(-1)
        if sample_width != self.sample_width or rate != self.frame_rate or channels != self.channels_number :
            raise ValueError("Эти файлы нельзя склеить")
        self.frames = self.frames + frames
        self.set_new_change()
        print('Файлы склеины')

    def undo(self):
        if self.changes_stack:
            os.remove(self.current_change)
            self.current_change = self.changes_stack.pop()
            self.set_current_change()
            print("Изменение отменено")
        else:
            raise ValueError("Начальный файл. Нет изменений, которые можно было бы отменить")

    @staticmethod
    def clear_changes_history():
        directory = os.path.join(os.path.dirname(__file__), '../ChangesHistory')
        for file in os.listdir(directory):
            os.remove(os.path.join(directory, file))
