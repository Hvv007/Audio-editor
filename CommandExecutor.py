#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

commands_msg = "Команды для изменения файла:\n" \
               "change_speed [coef]\n" \
               "change_volume [coef]\n" \
               "cut [start] [end]\n" \
               "concatenate [file_name]\n" \
               "reverse\n" \
               "undo\n" \
               "Выйти:\n" \
               "exit\n" \
               "Выйти и сохранить:\n" \
               "exit_save [file_name.format]"

more_args_msg = 'Необходимо ввести имя с указанным расширением и ничего больше'


class CommandExecutor:
    def __init__(self, editor, changer, path):
        self.concatenated_files_count = 0
        self.editor = editor
        self.changer = changer
        self.path = path

    def run(self):
        print('Пропишите commands, чтобы увидеть список доступных комманд')
        for line in sys.stdin:
            try:
                self.execute_command(line.split())
            except ValueError as e:
                print(e)

    def execute_command(self, args):
        try:
            if args[0] == 'commands':
                print(commands_msg)
            elif args[0] == 'undo':
                self.editor.undo()
            elif args[0] == 'exit':
                sys.exit()
            elif args[0] == 'exit_save':
                self.handle_exit_with_save(args)
            elif args[0] == 'change_volume' or args[0] == 'change_speed':
                self.handle_volume_and_speed(args)
            elif args[0] == 'concatenate':
                self.handle_concatenation(args)
            elif args[0] == 'cut':
                self.handle_cut(args)
            elif args[0] == 'reverse':
                self.editor.reverse()
            else:
                print('Неверный ввод, пропишите commands, чтобы ознакомиться со списком доступных команд')
        except IndexError:
            print('Не балуйтесь с кнопкой Enter, пустой ввод ничего не сделает')

    def handle_volume_and_speed(self, args):
        try:
            coef = args[1:]
            if len(coef) != 1:
                print('Должен быть один коэфициент и ничего больше')
                return
        except IndexError:
            print('Введите коэфициент')
            return
        if args[0] == 'change_volume':
            self.editor.change_volume(coef[0])
        else:
            self.editor.change_speed(coef[0])

    def handle_cut(self, args):
        try:
            cut_args = args[1:]
            if len(cut_args) != 2:
                print('Должно быть 2 аргумента: начало и конец фрагмента')
                return
        except IndexError:
            print('Введите начало и конец фрагмента')
            return
        self.editor.cut(*cut_args)

    def handle_concatenation(self, args):
        try:
            name = args[1:]
            if len(name) != 1:
                print(more_args_msg)
                return
        except IndexError:
            print('Введите имя файла для склейки')
            return
        file_to_concatenate = os.path.join(self.path, 'ChangesHistory',
                                           f'file_to_concatenate_{self.concatenated_files_count}.wav')
        try:
            self.changer.change_format(args[1], file_to_concatenate)
        except FileNotFoundError or NameError as e:
            print(e)
            return
        self.concatenated_files_count += 1
        self.editor.concatenate(file_to_concatenate)

    def handle_exit_with_save(self, args):
        try:
            name = args[1:]
            if len(name) != 1:
                print(more_args_msg)
                return
        except IndexError:
            print('Введите имя для сохраняемого файла')
            return
        export_name = os.path.join('Results', name[0])
        if export_name is None:
            return
        try:
            self.changer.change_format(self.editor.current_change, export_name)
        except ValueError or TypeError as e:
            print(e)
            return
        print("Аудиодорожка сохранена")
        sys.exit()
