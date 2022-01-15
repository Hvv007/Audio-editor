# Audio-editor
## Предустановка:
```sh
sudo apt-get install sox
sudo apt-get install ffmpeg
```

## Usage
```sh
python3 main.py -h - help
python3 main.py FILE_NAME - запуск редактора
```

## Поддерживаемые форматы
`MP3`, `WAV`, `FLAC`

## Доступные команды:
`change_speed [num]` - изменить скорость с коэффициентом `num`, `num > 0`

`change_volume [num]` - изменить громкость с коэффициентом `num`, `num >= 0`

`cut [start] [end]` - вырезать фрагмент с секунды `start` до секунды `end`

`concatenate [file_name]` - приклеить в конец аудиодорожку `file_name`

`undo` - вернуться к предыдущему состоянию

`exit` - выйти без сохранения

`exit_save [file_name.format]` - выйти и сохранить аудидорожку в файл `file_name.format`,
 где `format` - поддерживаемый формат