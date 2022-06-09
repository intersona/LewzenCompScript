import json
import generateSVG
from generateCpp import JsonException
import re

global control_num, write_area, control


def get_symbol(key):
    symbols = {'x': 'x', 'y': 'y', 'w': 'width', 'h': 'height'}
    return symbols[key] if key in symbols.keys() else key


# x+w*p -> context.x + context.width * p
# abc.x -> context.abc.x
# abc.width -> context.x+context.width-context.abc.x
def parse_position_with_context(ori_pos):
    a = re.split('[+-]', ori_pos)
    position = ''
    operations = []
    p_ope = 0
    for char in ori_pos:
        if char == '+' or char == '-':
            operations.append(char)

    for j in range(0, len(a)):
        b = a[j].split('*')
        if len(b) > 1:
            offset = 'context.' + get_symbol(b[0]) + '*' + b[1]
        else:
            offset = 'context.' + get_symbol(b[0])
        if not j == 0:
            position += operations[p_ope]
            p_ope += 1
        position += offset
    # print(position)
    return position


# 关键点初始位置
def parse_point2num(size, pos):
    trans_arr = {'w': str(size[0]), 'h': str(size[1]), 'x': '0', 'y': '0'}
    pos_num = []
    for p in pos:
        # x+w*p
        exp = ''
        a = re.split('[+]', p)
        if len(a) > 1:
            b = a[1].split('*')
            if len(b) > 1:
                exp = trans_arr[a[0]] + '+' + trans_arr[b[0]] + '*' + b[1]
            else:
                exp = trans_arr[a[0]] + '+' + trans_arr[b[0]]
        else:
            exp = trans_arr[a[0]]
        pos_num.append(eval(exp))

    return {'x': pos_num[0], 'y': pos_num[1]}


# 解析点的坐标
# M x y -> [p1.x,p1.y]
# return [[point_name,symbol,p_x,p_y]] 若为A或Z，另外处理
def get_path_points(ori_path):
    points = []
    pnum = 0
    arr = ori_path.split(' ')
    i = 0
    while i < len(arr):
        if arr[i] == 'Z':
            point_symbol = arr[i]
            points.append(['', point_symbol])
            i += 1
            # TODO
        if arr[i] == 'M':
            # arr[i] = parse_symbol(arr[i])
            # out += arr[i]
            # out += ' '
            point_symbol = arr[i]
            for j in range(1):
                # arr[j] = parsePos(arr[j])
                # out += arr[j]
                point_name = 'p' + str(pnum)
                x_position = parse_position_with_context(arr[i + j * 2 + 1])
                y_position = parse_position_with_context(arr[i + j * 2 + 2])
                points.append([point_name, point_symbol, x_position, y_position])
                pnum += 1
            i += 3
        elif arr[i] == 'Q':
            point_symbol = arr[i]
            for j in range(2):
                point_name = 'p' + str(pnum)
                x_position = parse_position_with_context(arr[i + j * 2 + 1])
                y_position = parse_position_with_context(arr[i + j * 2 + 2])
                points.append([point_name, point_symbol, x_position, y_position])
                pnum += 1
            i += 5
        elif arr[i] == 'S':
            point_symbol = arr[i]
            for j in range(2):
                point_name = 'p' + str(pnum)
                x_position = parse_position_with_context(arr[i + j * 2 + 1])
                y_position = parse_position_with_context(arr[i + j * 2 + 2])
                points.append([point_name, point_symbol, x_position, y_position])
                pnum += 1
            i += 5
        elif arr[i] == 'L':
            point_symbol = arr[i]
            for j in range(1):
                point_name = 'p' + str(pnum)
                x_position = parse_position_with_context(arr[i + j * 2 + 1])
                y_position = parse_position_with_context(arr[i + j * 2 + 2])
                points.append([point_name, point_symbol, x_position, y_position])
                pnum += 1
            i += 3
        elif arr[i] == 'C':
            point_symbol = arr[i]
            for j in range(3):
                point_name = 'p' + str(pnum)
                x_position = parse_position_with_context(arr[i + j * 2 + 1])
                y_position = parse_position_with_context(arr[i + j * 2 + 2])
                points.append([point_name, point_symbol, x_position, y_position])
                pnum += 1
            i += 7
        elif arr[i] == 'A':
            point_name = 'p' + str(pnum)
            point_symbol = arr[i]
            x_position = parse_position_with_context(arr[i + 6])
            y_position = parse_position_with_context(arr[i + 7])
            points.append(
                [point_name, point_symbol, x_position, y_position, parse_position_with_context(arr[i + 1]),
                 parse_position_with_context(arr[i + 2]), arr[i + 3], arr[i + 4],
                 arr[i + 5]])
            pnum += 1
            i += 8
        else:
            raise JsonException('error symbol')
    return [pnum, points]


def get_path(ori_path):
    [pnum, points] = get_path_points(ori_path)

    init_point_code = '''let %s = {x: %s, y: %s};\n'''

    output = ''
    for p in points:
        output += init_point_code % (p[0], p[2], p[3])
    i = 0
    output += 'context.path = '
    while i < len(points):
        point = points[i]
        if not i == 0:
            output += ' + \" \" + '
        if point[1] == 'Z':
            output += '''\"Z\"'''
        if point[1] == 'M':
            p0 = points[i]
            output += '''\"M \" + %s.x + \" \" + %s.y''' % (p0[0], p0[0])
            i += 1
        elif point[1] == 'L':
            p0 = points[i]
            output += '''\"L \" + %s.x + \" \" + %s.y''' % (p0[0], p0[0])
            i += 1
        elif point[1] == 'Q':
            p0 = points[i]
            p1 = points[i + 1]
            output += '''\"Q \" + %s.x + \" \" + %s.y + \" \" + %s.x + \" \" + %s.y''' % (
                p0[0], p0[0], p1[0], p1[0])
            i += 2
        elif point[1] == 'S':
            p0 = points[i]
            p1 = points[i + 1]
            output += '''\"S \" + %s.x + \" \" + %s.y + \" \" + %s.x + \" \" + %s.y''' % (
                p0[0], p0[0], p1[0], p1[0])
            i += 2
        elif point[1] == 'C':
            p0 = points[i]
            p1 = points[i + 1]
            p2 = points[i + 2]
            output += '''\"S \" + %s.x + \" \" + %s.y + \" \" + %s.x + \" \" + %s.y+ \" \" + %s.x + \" \" + %s.y''' % (
                p0[0], p0[0], p1[0], p1[0], p2[0], p2[0])
            i += 3
        elif point[1] == 'A':
            p0 = points[i]
            output += '''\"A \" + (%s) + \" \" + (%s) + \" \" + %s + \" \" + %s + \" \" + %s + \" \" + %s.x + \" \" + %s.y''' % (
                p0[4], p0[5], p0[6], p0[7], p0[8], p0[0], p0[0])
            i += 1
        else:
            raise JsonException('error symbol')
    output += ';'
    return output
    pass


# 读取原始用户输入的json文件，并生成到所需要的json
def read_ori_json(path):
    global control_num, write_area, control
    jsonfile = open(path)
    input_json = jsonfile.read()
    jsonfile.close()
    # print("input_json:" + input_json)
    data = json.loads(input_json)
    # print(data)
    # 存放控制点变量名及位置数值
    controls_arr_for_svg = []
    if not data.__contains__('name'):
        raise JsonException('need name')
    if not data.__contains__('path'):
        raise JsonException('need path')
    original_name = data['name']
    path = data['path']
    size = [100, 100]
    if not data.__contains__('size'):
        raise JsonException('need size')
    else:
        if not (data['size'].__contains__('width') and data['size'].__contains__('height')):
            raise JsonException('wrong size input')
        else:
            size = [int(data['size']['width']), int(data['size']['height'])]
    if data.__contains__('control_point_num'):
        control = True
        control_num = int(data['control_point_num'])
        if control_num == 0:
            control = False
    else:
        control = False

    conditions = []
    control_names = ['RB', 'R', 'RT', 'L', 'LT', 'LB', 'T', 'B']
    if data.__contains__('controls'):
        for condition_json in data['controls']:
            if not condition_json.__contains__('control_name'):
                raise JsonException('need control name')
            control_name = condition_json['control_name']
            if control_names.__contains__(control_name):
                raise JsonException('wrong control name')
            if control_name[0] in ['x', 'y', 'w', 'h']:
                raise JsonException('initial character not legal')
            else:
                control_names.append(control_name)
            if not condition_json.__contains__('default_position'):
                raise JsonException('wrong default position')

            controls_arr_for_svg.append([control_name, condition_json["default_position"]["default_x"],
                                         condition_json["default_position"]["default_y"],
                                         condition_json['x_range'] if condition_json.__contains__('x_range') else [],
                                         condition_json['y_range'] if condition_json.__contains__('y_range') else [],
                                         size])

            control_position = [parse_position_with_context(condition_json["default_position"]["default_x"]),
                                parse_position_with_context(condition_json["default_position"]["default_y"])]

            if not condition_json.__contains__('move_method') or \
                    condition_json["move_method"] not in ['0', '1', '2', '3']:
                raise JsonException('wrong move_method')
            if condition_json.__contains__('write_area'):
                write_area = [condition_json['write_area']['x'], condition_json['write_area']['y'],
                              condition_json['write_area']['width'], condition_json['write_area']['height']]
            else:
                write_area = ['x', 'y', 'w', 'h']
            move_method = condition_json["move_method"]
            # move_update = condition_json["move_update"]
            move_update = '0'
            x_range = []
            y_range = []
            if (not condition_json.__contains__('x_range')) and (not condition_json.__contains__('y_range')):
                raise JsonException('need control range')
            if condition_json.__contains__('x_range') and not condition_json["x_range"]["min"] == '':
                try:
                    x_range = [parse_position_with_context(condition_json["x_range"]["min"]),
                               parse_position_with_context(condition_json["x_range"]["max"])]
                except KeyError:
                    raise JsonException('wrong x range')

            if condition_json.__contains__('y_range') and not condition_json["y_range"]["min"] == '':
                try:
                    y_range = [parse_position_with_context(condition_json["y_range"]["min"]),
                               parse_position_with_context(condition_json["y_range"]["max"])]
                except KeyError:
                    raise JsonException('wrong y range')

            # condition 中的点都是解析后的
            if not condition_json.__contains__('constrain'):
                conditions.append(
                    [control_position, [move_method, move_update], x_range, y_range, control_name])
            else:
                conditions.append(
                    [control_position, [move_method, move_update], x_range, y_range,
                     control_name, condition_json['constrain']])
    get_js_json(original_name, size, path, conditions, controls_arr_for_svg)

    # for ctr in conditions:
    #     controls_arr_for_svg.append([ctr[4], ctr[0][0], ctr[0][1]])
    # return [generateSVG.generateSVG(original_name, path, write_area, controls_arr_for_svg, 'cpp'), original_name, path,
    #         write_area, controls_arr_for_svg]
    pass


# TODO
def parse_constrain(constrain_str):
    return constrain_str.replace('$', 'context.')


# [control_name, x_range, y_range,condition_json['constrain']]
def get_callback(control_constrain):
    control_name = control_constrain[0]
    x_range = control_constrain[1]
    y_range = control_constrain[2]
    output = ''
    output += ''
    callback_template1 = "if(context.%s.%s < %s) context.%s.%s = %s;\n"
    callback_template2 = "if(context.%s.%s > %s) context.%s.%s = %s;\n"
    if len(x_range) == 2 and not x_range[0] == '':
        output += callback_template1 % (control_name, 'nx', x_range[0], control_name, 'x', x_range[0])
        output += callback_template2 % (control_name, 'nx', x_range[1], control_name, 'x', x_range[1])
    if len(y_range) == 2 and not y_range[0] == '':
        output += callback_template1 % (control_name, 'ny', y_range[0], control_name, 'y', y_range[0])
        output += callback_template2 % (control_name, 'ny', y_range[1], control_name, 'y', y_range[1])
    if len(control_constrain) == 4:
        constrain = control_constrain[3]
        output += parse_constrain(constrain)
    output += ''
    return output


def get_delta(ctr_name, move_method):
    if move_method == '0':
        return "context.%s.dy = 0;" % ctr_name
    if move_method == '1':
        return "context.%s.dx = 0;" % ctr_name
    if move_method == '2':
        return ''
    if move_method == '3':
        return "context.%s.dy = dx;" % ctr_name
    pass


# [control_position, [move_method, move_update], x_range, y_range, control_name, condition_json['constrain']]
# 其中点都是解析之后的，除了constrain
# pos_condition为解析
def get_control(conditions, pos_conditions, size):
    output = {'points': []}

    for i in range(len(conditions)):
        ctr = conditions[i]

        ori_ctr_pos = [pos_conditions[i][1], pos_conditions[i][2]]

        if len(ctr) == 6:
            control_constrain = [ctr[4], ctr[2], ctr[3], ctr[5]]
        else:
            control_constrain = [ctr[4], ctr[2], ctr[3]]
        ctr_json = {'pid': ctr[4], 'pos': parse_point2num(size, ori_ctr_pos), 'color': 'orange',
                    'callback': get_callback(control_constrain),
                    'delta': get_delta(ctr[4], ctr[1][0])}
        output['points'].append(ctr_json)
    return output


# [control_position, [move_method, move_update], x_range, y_range, control_name, condition_json['constrain']]
# 其中点都是解析之后的，除了constrain
def get_rect_change(controls):
    output = {"before_rect_change": "", "after_rect_change": ""}
    # get before_rect_change

    for ctr in controls:
        move_method = ctr[1][0]
        template_before_x = "context.dx%s = (context.%s.x - context.x) / context.width;"
        template_before_y = "context.dy%s = (context.%s.y - context.y) / context.height;"
        template_after = "context.%s = {x: %s, y:%s};"
        if move_method == '0':  # only x
            output['before_rect_change'] += template_before_x % (ctr[4], ctr[4])
            output['after_rect_change'] += template_after % (
                ctr[4], 'context.x + context.dx' + ctr[4] + '*context.width', ctr[0][1])
        if move_method == '1':  # only y
            output['before_rect_change'] += template_before_y % (ctr[4], ctr[4])
            output['after_rect_change'] += template_after % (
                ctr[4], ctr[0][0], 'context.y + context.dy' + ctr[4] + '*context.height')
        if move_method == '2':  # x and y
            output['before_rect_change'] += template_before_x % (ctr[4], ctr[4])
            output['before_rect_change'] += template_before_y % (ctr[4], ctr[4])
            output['after_rect_change'] += template_after % (
                ctr[4], 'context.x + context.dx' + ctr[4] + '*context.width',
                'context.y + context.dy' + ctr[4] + '*context.height')
        if move_method == '3':  # x=y
            output['before_rect_change'] += template_before_x % (ctr[4], ctr[4])
            output['before_rect_change'] += template_before_y % (ctr[4], ctr[4])
            output['after_rect_change'] += template_after % (
                ctr[4], 'context.x + context.dx' + ctr[4] + '*context.width',
                'context.y + context.dy' + ctr[4] + '*context.height')

    return output


def get_js_json(original_name, size, path, conditions, controls_arr_for_svg):
    rect_change = get_rect_change(conditions)
    output_json = {'name': original_name, 'size': {'width': size[0], 'height': size[1]},
                   'points': get_control(conditions, controls_arr_for_svg, size)['points'], 'path': get_path(path),
                   'before_rect_change': rect_change['before_rect_change'],
                   'after_rect_change': rect_change['after_rect_change']}

    save_json(original_name, output_json)


import json
import os

SAVE_PATH = '.\\newjson\\'


def save_json(original_name, dict):
    out_json = json.dumps(dict)
    current_path = os.path.abspath(__file__)
    parent_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    file = open(parent_path + SAVE_PATH[1:] + '%s_js.json' % original_name, 'w+')
    file.write(out_json)
    file.close()
    # print(out_json)

# [control_position, [move_method, move_update], x_range, y_range, control_name, condition_json['constrain']]

# if __name__ == "__main__":
#     # out = get_path(
#     #     "M x abc.y L abc.x abc.y L abc.x y L x+w y+h*0.5 L abc.x y+h L abc.x y+h-abc.h L x y+h-abc.h L cde.x cde.y L x abc.y")
#     # out = get_callback(['sad', ['context.x', 'context.x+context.width'], ['context.y', 'context.y+context.height'],
#     #                     'if($abc.x<$cde.x){$abc=$cde.x;}'])
#     # out = get_control(
#     #     [[['context.x+context.width*0.25', 'context.y+context.height*0.25'], ['1'],
#     #       ['context.x', 'context.x+context.width'], ['context.y', 'context.y+context.height'], 'abc']],
#     #     [['abc', 'x+w*0.25', 'y+h*0.25']], [100, 100])
#     # print(out)
#     read_ori_json('./json/data_storage.json')
#     pass
