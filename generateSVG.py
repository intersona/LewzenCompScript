import re

import cairosvg

SVG_PATH = '.\\svg\\'
global sym2num

sym2num = {'x': '0', 'y': '0', 'w': '200', 'h': '200'}


def parse_control_pos(controls):
    for j in range(len(controls)):
        ctr = controls[j]
        for i in range(1, 3):
            clength = ctr[i]  # x[+w(*p)]
            d = clength.split('+')
            if len(d) > 1:
                # clength = 'y+h(*p)'
                e = d[1].split('*')
                if len(e) > 1:
                    # clength = 'y+h*p'
                    clength = sym2num[e[0]] + '*' + e[1]
                    controls[j][i] = clength
                else:
                    # clength = 'y+h'
                    controls[j][i] = sym2num[e[0]]
            else:
                # clength = 'y'
                controls[j][i] = sym2num[d[0]]
    # print("controls in svg:" + str(controls))
    return controls


# 解析类似 x+w*0.5 形式的坐标
# control.[xywh]
# output: getX()+getWidth()*0.5

def parse_position(point, controls):
    controls_names = []

    for control in controls:
        controls_names.append(control[0])

    a = re.split('[+-]', point)
    position = ''
    operations = []
    p_ope = 0
    for char in point:
        if char == '+' or char == '-':
            operations.append(char)

    for j in range(0, len(a)):
        b = a[j].split('*')
        if len(b) > 1:
            if b[0] in sym2num:
                # b[0] == [wh]
                offset = sym2num[b[0]] + '*' + b[1]
            else:
                # b[0] == contorl.[wh]
                # b[1] = double
                c = b[0].split('.')
                index = controls_names.index(c[0])
                clength = None
                if c[1] == 'w' or c[1] == 'x':
                    # clength = 'x+w*p'
                    clength = controls[index][1]
                else:
                    # clength = 'y+h*p'
                    clength = controls[index][2]
                offset = clength
                # d = clength.split('+')
                # # e = d[1].split('*')
                # # clength = sym2num[e[0]] + '*' + e[1]
                # # offset = clength + '*' + b[1]
                # if len(d) > 1:
                #     # clength = 'y+h(*p)'
                #     e = d[1].split('*')
                #     if len(e) > 1:
                #         # clength = 'y+h*p'
                #         clength = sym2num[e[0]] + '*' + e[1]
                #         offset = clength
                #     else:
                #         # clength = 'y+h'
                #         offset = sym2num[e[0]]
                # else:
                #     # clength = 'y'
                #     offset = sym2num[d[0]]
        else:
            if b[0] in sym2num:
                # b[0] == [xywh]
                offset = sym2num[b[0]]
            elif b[0] in ['0', '1']:
                offset = b[0]
            else:
                # b[0] == contorl.[xywh]
                c = b[0].split('.')
                index = controls_names.index(c[0])
                clength = None
                # clength为控制点的初始坐标
                if c[1] == 'w' or c[1] == 'x':
                    # clength = 'x(+w(*p))'
                    clength = controls[index][1]
                else:
                    # clength = 'y(+h(*p))'
                    clength = controls[index][2]
                # d = clength.split('+')
                # if len(d) > 1:
                #     # clength = 'y+h(*p)'
                #     e = d[1].split('*')
                #     if len(e) > 1:
                #         # clength = 'y+h*p'
                #         clength = sym2num[e[0]] + '*' + e[1]
                #         offset = clength
                #     else:
                #         # clength = 'y+h'
                #         offset = sym2num[e[0]]
                # else:
                #     # clength = 'y'
                #     offset = sym2num[d[0]]
                offset = clength

        if not j == 0:
            position += operations[p_ope]
            p_ope += 1
        position += offset
    # print(position)
    return position


def generateSVG(comp, path, write_area, controls, flag):
    out = ''
    arr = path.split(' ')
    if flag == 'cpp':
        controls = parse_control_pos(controls)
    # print('arr in svg' + str(arr))
    for sym in arr:
        if sym not in ['M', 'A', 'C', 'L', 'Q', 'S']:
            arr[arr.index(sym)] = parse_position(sym, controls)

    for sym in arr:
        if sym not in ['M', 'A', 'C', 'L', 'Q', 'S']:
            arr[arr.index(sym)] = eval(arr[arr.index(sym)])
    for sym in arr:
        out += str(sym)
        out += ' '
    return generate_file(comp, out, write_area, controls, flag)


'''
x:getX():0
y:getY():0
w:getWidth():100
h:getHeight():100
control.x:control->getX():0+100*px
control.y:control->getY():0+100*py
control.w:control->getX()-getX():0+100*px
control.h:control->getY()-getY():0+100*px
'''
import os


def generate_file(comp_name, path, wa, controls, flag):
    svg = '''<svg xmlns="http://www.w3.org/2000/svg">
     <g>
      <g stroke=" black" fill=" white" stroke-width="3">
       <path d="%s" id="svg_1"/>
      </g>
     </g>

    </svg>''' % (

        path)
    current_path = os.path.abspath(__file__)
    parent_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    # print(parent_path)
    with open(parent_path + SVG_PATH[1:] + comp_name + '.svg', 'w+', encoding='utf-8') as f:
        f.write(svg)
        # abspath = os.path.abspath(f)
        # abspath = f.__dir__()
    f.close()
    out = parent_path + SVG_PATH[1:] + comp_name + '.svg'
    png_path = parent_path + SVG_PATH[1:] + comp_name + '.png'

    if not flag == 'update':
        cairosvg.svg2png(url=out, write_to=png_path, parent_width=200, parent_height=200, output_width=50,
                         output_height=50)
    # print('svg path in svg:' + out)
    return out

# if __name__ == '__main__':
#     comp_name = 'comp1'
#     controls = [['abc', 'x+w*0.75', 'y+h*0.25'], ['cde', 'x', 'y+h*0.5']]
#     generateSVG(
#         comp_name,
#         'M x abc.y L abc.x abc.y L abc.x y L x+w y+h*0.5 L abc.x y+h L abc.x y+h-abc.h L x y+h-abc.h L cde.x cde.y L x abc.y',
#         ['x', 'y', 'w', 'h'], controls, 'cpp')
