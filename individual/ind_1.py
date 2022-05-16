#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Выполнить индивидуальное задание 1 лабораторной работы 2.19,
добавив возможность работы с исключениями и логгирование.
"""

import pathlib
import argparse
import logging
from dataclasses import dataclass
import xml.etree.ElementTree as ET


@dataclass
class Student:
    name: str
    group: int
    average_estimation: float


# Выводит список студентов
def show_list(staff):
    if staff:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 8
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
                "No",
                "Ф.И.О.",
                "Группа",
                "Средняя оценка"
            )
        )
        print(line)
        # Вывести данные о всех студентах.
        for idx, student in enumerate(staff, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                    idx,
                    student.name,
                    student.group,
                    student.average_estimation
                )
            )
        print(line)
    else:
        print("Список пуст")


# Выводит справку о работе с программой
def show_help():
    print("Список команд:\n")
    print("add - добавить студента;")
    print("list - вывести список студентов;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")


# Сохраняет данные в файл
def save_students(file_name, staff):
    root = ET.Element('students')
    for student in staff:
        student_element = ET.Element('student')
        name_element = ET.SubElement(student_element, 'name')
        name_element.text = student.name
        group_element = ET.SubElement(student_element, 'group')
        group_element.text = str(student.group)
        average_estimation = ET.SubElement(student_element,
                                           'average_estimation')
        average_estimation.text = str(student.average_estimation)
        root.append(student_element)
    tree = ET.ElementTree(root)
    with open(file_name, "wb") as fout:
        tree.write(fout, encoding='utf8', xml_declaration=True)


# Читает данные из файла
def load_students(file_name):
    with open(file_name, "r", encoding="utf8") as fin:
        xml = fin.read()

    parser = ET.XMLParser(encoding="utf8")
    tree = ET.fromstring(xml, parser=parser)

    students = []
    for student_elements in tree:
        name, group, average_estimation = None, None, None
        for element in student_elements:
            if element.tag == "name":
                name = element.text
            elif element.tag == "group":
                group = int(element.text)
            elif element.tag == "average_estimation":
                average_estimation = float(element.text)

        if name is not None and group is not None \
                and average_estimation is not None:
            students.append(Student(
                name=name, group=group, average_estimation=average_estimation
            ))

    return students


def main(command_line=None):
    # Парсер для определения имени файла
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Основной парсер командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument("--home", type=bool, default=False)
    subparsers = parser.add_subparsers(dest="command")

    # Субпарсер для добавления студента
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new student"
    )
    add.add_argument(
        "-n",
        "--name",
        help="The student`s name"
    )
    add.add_argument(
        "-g",
        "--group",
        help="The student`s group"
    )
    add.add_argument(
        "-ae",
        "--average_estimation",
        help="The student`s average estimation"
    )

    # Субпрасер показывающий список студентов
    subparsers.add_parser(
        "list",
        parents=[file_parser],
        help="Show list of student`s"
    )

    # # # Работа программы # # #
    args = parser.parse_args(command_line)
    if args.home:
        filename = pathlib.Path.home() / args.filename
    else:
        filename = pathlib.Path(args.filename)

    # Обработка ошибки если файл не существует
    try:
        students = load_students(filename)
    except FileNotFoundError:
        logging.warning("Файл не найден, создастся новый")
        students = []

    is_dirty = False
    if args.command == "add":
        student = Student(args.name, args.group, args.average_estimation)
        students.append(student)
        is_dirty = True
    elif args.command == "list":
        show_list(students)
    else:
        print("Неизвестная команда!")

    if is_dirty:
        save_students(filename, students)


if __name__ == '__main__':
    main()
