import json
from aiohttp import web
import re

routes = web.RouteTableDef()
labs = {}


@routes.post('/labs')
async def post_handler(request):
    """ добавление новой лабораторной """
    request_data = await request.json()
    lab_name = request_data["lab_name"]
    status, reason = add_new_lab(request_data)

    message = str(request.url) + "/" + lab_name
    resp = web.Response(text=message, status=status, reason=reason)
    resp.headers["Location"] = message
    return resp


def add_new_lab(request_data):
    """ добавляем лабораторную, если такой еще не было """
    status = 409
    reason = "Такая лабораторная уже есть\n"

    if "passed_students" in request_data:
        status = 400
        reason = "Лабораторная еще не добавлена, ее еще никто не мог сдать\n"
        return status, reason

    lab_name, description, dead_line = get_new_lab_params(request_data)
    if lab_name not in labs:
        status = 201
        reason = "OK"
        labs[lab_name] = {"dead_line": dead_line, "description": description, "passed_students": []}

    return status, reason


def get_new_lab_params(request_data):
    lab_name = request_data["lab_name"]
    description = ""
    dead_line = ""

    if "description" in request_data:
        description = request_data["description"]
    if "dead_line" in request_data:
        dead_line = request_data["dead_line"]
    return lab_name, description, dead_line

@routes.delete('/labs')
async def delete_all_labs(request):
    """ удаление всех лабораторных """
    status = 404
    reason = "На сервере нет лабораторных, нельзя ничего удалить"

    if len(labs) > 0:
        status = 200
        reason = "OK"
        labs.clear()

    return web.Response(text="", status=status, reason=reason)


@routes.delete('/labs/{lab_name}')
async def delete_lab(request):
    """ удаление лабораторной работы """
    lab_name = request.match_info["lab_name"]

    status = 404
    reason = "Такой лаборатоной нет на сервере"

    if lab_name in labs:
        status = 200
        reason = "OK"
        labs.pop(lab_name)

    return web.Response(text="", status=status, reason=reason)


@routes.get('/labs/{lab_name}')
async def get_lab(request):
    """ получение сведений о лабораторной работе """
    lab_name = request.match_info["lab_name"]

    status = 404
    reason = "Такой лаборатоной нет на сервере"
    message = ""
    if lab_name in labs:
        status = 200
        reason = "OK"
        cur_lab = labs[lab_name]
        message = {
            lab_name: {"dead_line": cur_lab["dead_line"],
                       "description": cur_lab["description"],
                       "passed_students": cur_lab["passed_students"]}
        }

    return web.Response(text=json.dumps(message), status=status, reason=reason)


@routes.get('/labs')
async def get_all_lab(request):
    """ получение сведений о всех лабораторных работах """

    status = 404
    reason = "На сервере нет лабораторных"
    labs_data = {}
    if len(labs) > 0:
        status = 200
        reason = "OK"
        for name, lab_data in labs.items():
            lab = {"dead_line": lab_data["dead_line"],
                   "description": lab_data["description"],
                   "passed_students": lab_data["passed_students"]}
            labs_data[name] = lab

    return web.Response(text=json.dumps(labs_data), status=status, reason=reason)


@routes.put('/labs/{lab_name}')
async def lab_name_post_handler(request):
    """ добавление новой лабораторной """
    lab_name = request.match_info["lab_name"]
    request_data = await request.json()

    status, reason = change_lab_param(lab_name, request_data)
    return web.Response(text="", status=status, reason=reason)


def change_lab_param(lab_name, request_data):
    """ изменение выбранного параметра лабораторной """
    status = 200
    reason = "OK"

    if lab_name not in labs:
        status = 404
        reason = "Такая лабораторная еще не была добавлена"
        return status, reason

    if "dead_line" in request_data:
        status, reason = check_dead_line(request_data["dead_line"])
        if status != 200:
            return status, reason
        dead_line = request_data["dead_line"]
        labs[lab_name]["dead_line"] = dead_line

    if "passed_students" in request_data:
        new_student = request_data["passed_students"]
        if labs[lab_name]["passed_students"].count(new_student) == 0:
            labs[lab_name]["passed_students"].append(new_student)

    if "description" in request_data:
        description = request_data["description"]
        labs[lab_name]["description"] = description

    return status, reason


def check_dead_line(dead_line):
    status = 200
    reason = ""

    if not re.fullmatch(r'\d{1,2}.\d{1,2}.\d{4}', dead_line):
        status = 400
        reason = f"Дедлайн должен иметь формат день.месяц.год"

    return status, reason


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app)
