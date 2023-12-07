import json

import aiohttp
import asyncio
import argparse
from enum import Enum
import csv
from os.path import exists
from os import stat


class Methods(Enum):
    POST = 1
    GET = 2
    PUT = 3
    DELETE = 4


async def send_request(method, url, message=None):
    async with aiohttp.ClientSession() as session:
        response = None
        if method == Methods.POST:
            response = await session.post(url, json=message)
        elif method == Methods.PUT:
            response = await session.put(url, json=message)
        elif method == Methods.GET:
            response = await session.get(url)
        elif method == Methods.DELETE:
            response = await session.delete(url)

        status = response.status
        reason = response.reason

        if status < 200 or status > 299:
            print(status, reason, sep="\n")
            await session.close()
            return

        answer = await response.text()
        if answer != "":
            print(answer)

        if method == Methods.GET:
            await update_csv(answer)
        await session.close()


async def update_csv(labs):
    lab_json = json.loads(labs)

    filename = "labs.csv"

    if len(lab_json.keys()) > 1 or not exists(filename) or stat("labs.csv").st_size == 0:
        await update_all_or_create(filename, lab_json)
    else:
        file_labs = await get_file_labs(filename)
        await update_one(filename, file_labs, lab_json)


async def get_file_labs(filename):
    csv_file = open(filename, 'r', newline='')
    reader = csv.reader(csv_file, delimiter=',')
    file_labs = []

    for row in reader:
        file_labs.append(row)

    csv_file.close()
    return file_labs


async def update_all_or_create(filename, lab_json):
    """ Обновление/создание таблицы с данными о всех лабораторных """
    csv_file = open(filename, 'w', newline='')

    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(["Название лабораторной"] +
                    [lab_name for lab_name in lab_json])
    writer.writerow(["Дедлайн"] +
                    [lab_data["dead_line"] for lab_data in lab_json.values()])
    writer.writerow(["Описание лабораторной"] +
                    [lab_data["description"] for lab_data in lab_json.values()])

    students_statuses = dict()
    for lab_name, lab_data in lab_json.items():
        # проходимся по всем студнетам, сдавшим эту лабу
        cur_students = lab_data["passed_students"]
        for student in cur_students:
            if student not in students_statuses:
                students_statuses[student] = []
            students_statuses[student].append(lab_name)

    lab_idx = 1
    labs_indexes = {}
    for lab_name in lab_json:
        labs_indexes[lab_name] = lab_idx
        lab_idx += 1

    for student, passed_labs in students_statuses.items():
        row = []
        for lab in labs_indexes:
            if lab in passed_labs:
                row.append(1)
            else:
                row.append(0)
        writer.writerow([student] + row)
    csv_file.close()


async def update_one(filename, file_labs, lab_json):
    """ Обновление сведений только об одной лабораторной работе """
    # название лабораторной
    lab_name = list(lab_json.keys())[0]
    lab_data = lab_json[lab_name]

    is_lab_in_file = file_labs[0].count(lab_name) > 0

    lab_index = -1
    if is_lab_in_file:
        lab_index = file_labs[0].index(lab_name)

    # обновляем все поля, кроме студентов
    if lab_index == -1:
        # если такой лаборатоной нет в файле: надо ее прибавить к уже имеющимся
        file_labs[0].append(lab_name)
        file_labs[1].append(lab_data["dead_line"])
        file_labs[2].append(lab_data["description"])
    else:
        # если есть: обновляем поля лабораторной
        file_labs[1][lab_index] = lab_json[lab_name]["dead_line"]
        file_labs[2][lab_index] = lab_json[lab_name]["description"]

    rows_num = len(file_labs)

    # если есть студенты
    if rows_num > 3:
        file_names = dict()

        row_idx = 3
        for i in range(3, len(file_labs)):
            cur_name = file_labs[i][0]
            file_names[cur_name] = row_idx
            row_idx += 1

        labs_num = len(file_labs[0])-1
        for name in lab_data["passed_students"]:
            # если студент уже есть в файле, ставим ему единицу напротив этой лабы
            if name in file_names:
                cur_row = file_names[name]
                if lab_index == -1:  # лабы не было, поэтому добавляем единицу
                    file_labs[cur_row].append(1)
                else:                # лаба есть, поэтому просто обновляем значение
                    file_labs[cur_row][lab_index] = 1
            # если студента в файле нет
            else:
                # и еще и лабы такой не было, то добавляем строку в формате "имя_студента, 0,0,0,1"
                marks = ["0" for i in range(labs_num-1)]
                if lab_index == -1:
                    marks.append(str(1))
                else:
                    marks.insert(lab_index-1, str(1))

                new_student_string = [name] + marks
                file_labs.append(new_student_string)

    csv_file = open(filename, 'w', newline='')

    writer = csv.writer(csv_file, delimiter=',')
    writer.writerows(file_labs)

    csv_file.close()


async def add_or_edit_lab(args):
    message = {}
    if args.dead_line:
        message["dead_line"] = args.dead_line
    if args.description:
        message["description"] = args.description
    if args.student:
        message["passed_students"] = args.student
    return message


async def main():
    edit_help_string = "Для изменения параметров лабораторной работы выберите параметр" \
                       "\nВиды параметров:" \
                       "\n\t--dead_line - дедлайн в формате день.месяц.год" \
                       "\n\t--description - описание лабораторной работы" \
                       "\n\t--student - студент сдавший эту лабораторную"

    parser = argparse.ArgumentParser(description='client')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--add', type=str,
                       help="Добавить лабораторную с выбранным именем")
    group.add_argument('--get',
                       help="Получить сведения о выбранной лабораторной")
    group.add_argument('--get_all', action="store_true",
                       help="Получить сведения о всех лабораторных")
    group.add_argument('--edit', type=str,
                       help=edit_help_string)
    group.add_argument('--delete', type=str,
                       help="Удалить выбранную лабораторную работу")
    group.add_argument('--delete_all', action="store_true",
                       help="Удалить все лабораторные работы")

    parser.add_argument("--dead_line", type=str,
                        help="Дедлайн лабораторной работы")
    parser.add_argument("--description", type=str,
                        help="Описание лабораторной работы")
    parser.add_argument("--student", type=str,
                        help="Студент, сдавший эту лабораторную работу")

    args = parser.parse_args()

    message = {}
    method = Methods.POST
    url = "http://localhost:8080/labs"

    if args.add:
        print("Добавление лабораторной")
        method = Methods.POST
        message = await add_or_edit_lab(args)
        message["lab_name"] = args.add
    if args.delete:
        print("Удаление лабораторной")
        method = Methods.DELETE
        message = {"lab_name": args.delete}
        url += "/" + args.delete
    if args.delete_all:
        print("Удаление всех лабораторных")
        method = Methods.DELETE
    if args.get:
        print("Получение сведений о лабораторной")
        method = Methods.GET
        url += "/" + args.get
    if args.get_all:
        print("Получение сведений о всех лабораторных")
        method = Methods.GET
    if args.edit:
        if not (args.dead_line or args.description or args.student):
            print(edit_help_string)
            return

        print("Изменение лабораторной")
        method = Methods.PUT
        message = await add_or_edit_lab(args)
        url += "/" + args.edit

    await send_request(method=method, url=url, message=message)


asyncio.run(main())
