# Audio-editor
## Предустановка UNIX-подобные:
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

## Описание
Консольный аудиоредактор. 
`CommandExecutor.py` отвечает за считывание команд приработе аудиоредактора.
Модули с логикой находятся в папке `src` -
`Editor.py` отвечает за редактирование аудидорожки после введения команды, а
`FormatShaper.py` за смену формата файла. 
В папку `ChangeHistory` сохраняются промежуточные изменения, папка очищается после очередного
запуска редактора. В папку `Results` сохраняются конечные файлы 
после выхода с сохранением.

## Доступные команды:
`change_speed [num]` - изменить скорость с коэффициентом `num`, `num > 0`

`change_volume [num]` - изменить громкость с коэффициентом `num`, `num >= 0`

`cut [start] [end]` - вырезать фрагмент с секунды `start` до секунды `end`

`concatenate [file_name]` - приклеить в конец аудиодорожку `file_name`

`reverse` - развернуть аудидорожку

`undo` - вернуться к предыдущему состоянию

`exit` - выйти без сохранения

`exit_save [file_name.format]` - выйти и сохранить аудидорожку в файл `file_name.format`,
 где `format` - поддерживаемый формат. Сохранение происходит в папку Results
 
 ## Тесты
 Находятся в файле `Tests.py`
 
 Чтобы посмотреть покрытие модулей с логикой необходимо прописать:
```sh
python3 -m pytest Tests.py --cov=src
```
Покрытие составляет `93%`

В случае, если `pytest` не воспринимает аргумент `--cov`, пропишите
 ```sh
pip install pytest-cov
```