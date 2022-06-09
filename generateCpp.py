"""
输入：组件名称（解析掉_）
输入：有无额外关键点
 若无：输入路径（Path命令）及航点坐标（以x、y、w(width)、h(height)以及"关键点.[xyhw]"表示）
 若有：输入其范围（区间及x、y关系）；如何随其他点变化；路径以及航电坐标（以X、Y、width、height以及Control表示）
"""
import sys, getopt, json
import generateSVG

COMPONENT_JSON_PATH = 'json/'
SVG_PATH = 'svg/'

symbols = {'x': 'getX()', 'y': 'getY()', 'w': 'getWidth()', 'h': 'getHeight()'}


# , 'cx': 'Control0->getX()',
#        'cy': 'Control0->getY()', 'cw': '(Control0->getX() - getX())', 'ch': '(Control0->getY() - getY())',
#        'cx1': 'Control1->getX()', 'cy1': 'Control1->getY()', 'cw1': '(Control1->getX() - getX())',
#        'ch1': '(Control1->getY() - getY())',
#        }


def get_symbol(key):
    if symbols.__contains__(key):
        return symbols[key]
    elif re.match('(^\w*\\.[xyhw])$', key):
        if key[-1] == 'x' or key[-1] == 'y':
            # return 'Control%s->get%s()' % (key[2], key[1].upper())
            key = re.sub('\\.[xy]', '->' + symbols[key[-1]], key)
        elif key[-1] == 'h':
            # return '(Control%s->getY() - getY())' % key[2]
            key = re.sub('\\.h', '->getY()-getY()', key)
            key = '(%s)' % key
        elif key[-1] == 'w':
            # return '(Control%s->getX() - getX())' % key[2]
            key = re.sub('\\.w', '->getX()-getX()', key)
            key = '(%s)' % key
        return key


'''
$point.[xy]
$[xy]
$width $height
'''


def parse_constrain(constrain):
    regex = re.compile('\\.[xy]')
    variables = regex.findall(constrain)
    if not len(variables) == 0:
        for v in variables:
            # print(v)
            constrain = re.sub("\\." + v[1:], '->get%s()' % v[1:].upper(), constrain)
    constrain = re.sub('\\$width', 'getWidth()', constrain)
    constrain = re.sub('\\$height', 'getHeight()', constrain)

    regex = re.compile('\\$[xy]')
    variables = regex.findall(constrain)
    if not len(variables) == 0:
        for v in variables:
            # print(v)
            constrain = re.sub('\\$' + v[1:], 'get%s()' % v[1:].upper(), constrain)
    constrain = re.sub("\\$", '', constrain)
    return constrain


global h_code_head, h_code_tail

h_code_head = '''#ifndef __LEWZENSERVER_%s__
#define __LEWZENSERVER_%s__

#include "../comp/rectangle.h"

namespace LewzenServer {
    class %s : virtual public Rectangle {
    protected:
        std::shared_ptr<Lewzen::SVGIPath> SVGIPath;
'''

h_code_tail = '''
        public:
        //// 通用虚接口
        // 非构造初始化
        virtual void init() override;
        // 拷贝
        virtual ComponentAbstract &operator=(const ComponentAbstract &comp) override;
        // 序列化，并记录已操作的
        virtual void serialize(json &j, std::vector<std::string> &processed) override;
        // 反序列化
        virtual ComponentAbstract &operator=(const json &j) override;
        
        //// Writable虚接口
        virtual const ComponentWritable::WriteArea getWriteArea() override;

        //// Basics virtual interface
        virtual void moveCorePoint(const std::string &id, const double &dx, const double &dy) override;

        //// IsometricCube interface
        // 计算路径
        const std::string getPath() const;
    };
}
#endif'''


def get_init(if_control, o_name, c_name, conditions):
    init = '''    //// 通用虚接口
    // 非构造初始化
    void %s::init() {
            // 父类初始化
        Rectangle::init();
        // 设置类型
        setType("%s");

        // 维护图形SVG
        SVGIG->children({}); // 移除旧的图形
        Rectangle::moveCorePoint("RB", -100, 0); // 将区域变更为方形
        SVGIPath = std::make_shared<Lewzen::SVGIPath>();
        SVGIG->add(SVGIPath);
''' % (c_name, o_name)
    # TODO
    if if_control:
        for j in range(control_num):
            condition = conditions[j]
            control_name = 'Control' + str(j)
            control_name = condition[4]
            # if condition
            init += '''        %s = createCorePoint("%s", %s, %s);\n''' % (
                control_name, control_name, condition[0][0], condition[0][1])
            init += '''        %s->setColor("orange");\n''' % control_name
            init += '''                    %s->on_update([&](const double &x, const double &y, const double &nx, const double &ny) {
                        if (!corePointMoving) return;
            ''' % (control_name)
            if condition[1][0] == '0':  # only x
                init += '''            if (nx < %s) %s->setX(%s);  
                        if (nx > %s) %s->setX(%s);
            ''' % (condition[2][0], control_name, condition[2][0], condition[2][1], control_name, condition[2][1])

            if condition[1][0] == '1':  # only y
                init += '''            if (ny < %s) %s->setY(%s);
                        if (ny > %s) %s->setY(%s);
            ''' % (condition[3][0], control_name, condition[3][0], condition[3][1], control_name, condition[3][1])

            if condition[1][0] == '2':  # x and y
                init += '''                        if(nx < (%s))
                                    {
                                        %s->setX(%s);
                                    }
                                    if(nx > %s)
                                    {
                                        %s->setX(%s);
                                    }
                                    if(ny < %s)
                                    {
                                        %s->setY(%s);
                                    }
                                    if(ny > %s)
                                    {
                                        %s->setY(%s);
                                    }
            ''' % (condition[2][0], control_name, condition[2][0], condition[2][1], control_name, condition[2][1],
                   condition[3][0], control_name,
                   condition[3][0], condition[3][1], control_name, condition[3][1])

            if condition[1][0] == '3':  # dx = dy
                init += '''                double maxD = std::min(%s,%s);
                                            if(nx > maxD)
                                            {
                                                %s->setX(maxD);
                                            }
                                            if(nx < getX())
                                            {
                                                %s->setX(getX());
                                            }
                                            if(ny > maxD)
                                            {
                                                %s->setY(maxD);
                                            }
                                            if(ny < getY())
                                            {
                                                %s->setY(getY());
                                            }
            ''' % (condition[2][1], condition[3][1], control_name, control_name, control_name, control_name)
            init += '''
                        });
                            corePoints[%s->getId()] = %s;\n''' % (control_name, control_name)

    init += '''        // 绑定图形属性
        std::function<const std::string()> _getPath = std::bind(&%s::getPath, this);
        SVGIPath->D.bind(_getPath);
    }''' % c_name
    return init


def get_copy(if_control, c_name, conditions):
    copy = '''    // 拷贝
    ComponentAbstract &%s::operator=(const ComponentAbstract &comp) {
        // 拷贝父类
        Rectangle::operator=(comp);
        SVGIG->add(SVGIPath);

        auto &p = dynamic_cast<const %s &>(comp); 

''' % (c_name, c_name)
    # TODO
    if if_control:
        for j in range(control_num):
            control_name = 'Control' + str(j)
            condition = conditions[j]
            control_name = condition[4]
            copy += '''        // 拷贝关键点位置
                    *%s = *(p.%s);
            ''' % (control_name, control_name)
    copy += '        return *this;\n    }\n'
    return copy


def get_serialize(c_name):
    return '''    // 序列化，并记录已操作的
    void %s::serialize(json &j, std::vector<std::string> &processed) {
        // 父类序列化
        Rectangle::serialize(j, processed);
    }
''' % c_name


def get_inverse_serialize(if_control, c_name, conditions):
    iserialize = '''    // 反序列化
    ComponentAbstract &%s::operator=(const json &j) {
        // 父类反序列化
        Rectangle::operator=(j);
        SVGIG->add(SVGIPath);

''' % c_name
    # TODO
    if if_control:
        for j in range(control_num):
            control_name = 'Control' + str(j)
            condition = conditions[j]
            control_name = condition[4]
            iserialize += '''        // 注册关键点
                    %s = corePoints["%s"];
            ''' % (control_name, control_name)
    iserialize += '        return *this;\n    }\n'
    return iserialize


def get_write_area(write_area):
    area = '''    //// Writable虚接口
    const ComponentWritable::WriteArea Rectangle::getWriteArea() {
        return {
            %s,
            %s,
            %s,
            %s
        };
    }\n''' % (parse_position(write_area[0]), parse_position(write_area[1]), parse_position(write_area[2]),
              parse_position(write_area[3]))
    return area


def get_move(c_name, if_control, conditions):
    move = '''    //// Basics虚接口
    void %s::moveCorePoint(const std::string &id, const double &dx, const double &dy) {\n''' % c_name
    # TODO
    if if_control:
        for j in range(control_num):
            control_name = 'Control' + str(j)
            condition = conditions[j]
            control_name = condition[4]
            move += '''        double disY%s = %s->getY() - getY(); // 记录控制点到矩形上边的距离
        double disX%s = %s->getX() - getX();\n''' % (
                j, control_name, j, control_name)
        for j in range(control_num):
            control_name = 'Control' + str(j)
            condition = conditions[j]
            control_name = condition[4]
            if j == 0:
                move += '''        if (id == "%s") { // 移动控制点
            corePointMoving = true; // 开启更新锁\n''' % control_name
            else:
                move += '''        else if (id == "%s") { // 移动控制点
            corePointMoving = true; // 开启更新锁\n''' % control_name

            if condition[1][0] == '0':
                move += '''            *%s += createPoint(dx, 0);\n''' % control_name
            if condition[1][0] == '1':
                move += '''            *%s += createPoint(0, dy);\n''' % control_name
            if condition[1][0] == '2':
                # move += '''            *Control%s += createPoint(dx, 0);\n''' % j
                move += '''            *%s += createPoint(dx, dy);\n''' % control_name
            if condition[1][0] == '3':
                move += '''            *%s += createPoint(dx, dx);\n''' % control_name
            move += '''            corePointMoving = false;\n'''
            # add constrains
            if len(condition) == 6:
                move += parse_constrain(condition[5])
            move += '        }\n'
        move += '''        else {
            Rectangle::moveCorePoint(id, dx, dy);\n'''
        for j in range(control_num):
            condition = conditions[j]
            control_name = condition[4]
            if condition[1][1] == '1' or condition[1][1] == '0':
                if condition[1][0] == '0':
                    move += '''            if (getX()+disX%s > %s) disX%s = %s-getX();\n''' % (
                        j, condition[2][1], j, condition[2][1])
                    move += '''            *%s = createPoint(getX()+disX%s, %s); // 设置新的坐标\n''' % (
                        control_name, j, condition[0][1])
                elif condition[1][0] == '1':
                    move += '''            if (getY()+disY%s > %s) disY%s = %s-getY();\n''' % (
                        j, condition[3][1], j, condition[3][1])
                    move += '''            *%s = createPoint(%s,getY()+disY%s); // 设置新的坐标\n''' % (
                        control_name, condition[0][0], j)
                else:
                    move += '''            if (getX()+disX%s > %s) disX%s = %s-getX();
                    if (getY()+disY%s > %s) disY%s = %s-getY();\n''' % (
                        j, condition[2][1], j, condition[2][1], j, condition[3][1], j, condition[3][1])
                    move += '''            *%s = createPoint(getX()+disX%s,getY()+disY%s); // 设置新的坐标
             *%s = createPoint(getX()+disX%s,getY()+disY%s);''' % (control_name, j, j, control_name, j, j)

        #     if condition[1][1] == '0':
        #         move += '''            if (getX()+ptgX%s > %s) ptgX%s = %s-getX();
        #     if (getX()+ptgX%s < %s) ptgX%s = %s-getX();
        #     if ( getY()+ptgY%s > %s) ptgY%s = %s-getY();
        #     if ( getY()+ptgY%s < %s) ptgY%s = %s-getY();
        #     *%s = createPoint(getX()+ptgX%s, getY() + ptgY%s); // 设置新的坐标
        #     ''' % (
        #             j, condition[2][1], j, condition[2][1], j, condition[2][0], j, condition[2][0],
        #             j, condition[3][1], j, condition[3][1], j, condition[3][0], j, condition[3][0], control_name, j, j)
        move += '        }\n'

        #         move += '''        double disY = Control->getY() - getY(); // 记录控制点到矩形上边的距离
        #         double disX = Control->getX() - getX();
        #         double ptgX = ((Control->getX() - getX()) / getWidth()) * getWidth();
        #         double ptgY = ((Control->getY() - getY()) / getHeight()) * getHeight();
        #         if (id == "Control") { // 移动控制点
        #             corePointMoving = true; // 开启更新锁
        # '''
        #         if condition[1][0] == '0':
        #             move += '''            *Control += createPoint(dx, 0);\n'''
        #         if condition[1][0] == '1':
        #             move += '''            *Control += createPoint(0, dy);\n'''
        #         if condition[1][0] == '2':
        #             move += '''            *Control += createPoint(dx, 0);\n'''
        #             move += '''            *Control += createPoint(0, dy);\n'''
        #         if condition[1][0] == '3':
        #             move += '''            *Control += createPoint(dx, dx);\n'''
        #         move += '''            corePointMoving = false;\n        } else { // 移动其他点
        #             Rectangle::moveCorePoint(id, dx, dy);\n'''
    #         if condition[1][1] == '1':
    #             move += '''            if (disX > %s) disX = %s;
    #             if (disY > %s) disY = %s;\n''' % (condition[2][1], condition[2][1], condition[3][1], condition[3][1])
    #             if condition[1][0] == '0':
    #                 move += '''*Control = createPoint(getX()+disX, %s); // 设置新的坐标\n''' % condition[0][1]
    #             elif condition[1][0] == '1':
    #                 move += '''*Control = createPoint(%s,getY()+disY); // 设置新的坐标\n''' % condition[0][0]
    #
    #         elif condition[1][1] == '0':
    #             move += '''            if (ptgX > %s) ptgX = %s;
    #             if (ptgY > %s) ptgY = %s;
    #             *Control = createPoint(getX()+ptgX, getY() + ptgY); // 设置新的坐标
    # ''' % (condition[2][1], condition[2][1], condition[3][1], condition[3][1])
    #         move += '        }\n'

    else:
        move += '       Rectangle::moveCorePoint(id, dx, dy);\n'
    move += '''        onChanged(); // 更新事件
    }
'''
    return move


# control相关：init；copy；反serialize；move
def get_cpp_code(if_c, o_name, path_code, conditions, write_area):
    c_name = parse_name(o_name)
    output = '''#include "%s.h"

namespace LewzenServer {
''' % o_name
    # functions
    output += get_init(if_c, o_name, c_name, conditions)

    output += get_copy(if_c, c_name, conditions)

    output += get_serialize(c_name)

    output += get_inverse_serialize(if_c, c_name, conditions)

    output += get_write_area(write_area)

    output += get_move(c_name, if_c, conditions)

    output += out_getPath_func(path_code, c_name, conditions)

    output += '}'
    return output


def get_h(o_name, if_control, conditions):
    c_name = parse_name(o_name)
    global h_code_head, h_code_tail
    control_code = '''        std::shared_ptr<CorePoint> %s;\n'''
    code0 = h_code_head % (o_name.upper(), o_name.upper(), c_name)
    output = ''
    output += code0

    if if_control:
        for j in range(control_num):
            control_name = 'Control' + str(j)
            condition = conditions[j]
            control_name = condition[4]
            output += control_code % control_name
    output += h_code_tail
    return output


# input xxx_xxx
# output AxxBxx
def parse_name(name):
    names = name.split('_')
    output_name = ''
    for str in names:
        output_name += str.title()
    return output_name


import re


# 解析类似 x+w*0.5 形式的坐标
# output: getX()+getWidth()*0.5
def parse_position(point):
    # a = point.split('+')
    a = re.split('[+-]', point)
    # position = symbols[a[0]]
    position = ''
    operations = []
    p_ope = 0
    for char in point:
        if char == '+' or char == '-':
            operations.append(char)

    for j in range(0, len(a)):
        b = a[j].split('*')
        if len(b) > 1:
            offset = get_symbol(b[0]) + '*' + b[1]
        else:
            offset = get_symbol(b[0])
        if not j == 0:
            position += operations[p_ope]
            p_ope += 1
        position += offset
    # print(position)
    return position


# a = re.split('[.+]', point)


# def parse_symbol(symbol):
#     return '\"' + symbol + ' ' + '\" +'


# # 输入的符号命令
# input_symbols = []
# 输入的航点[['名称','symbol','x坐标','y坐标'],...]
global input_points
input_points = []
# 航点数目
global points_num
points_num = 0


# 解析点到数组input_points
def parse_points(path_str):
    global points_num, input_points
    arr = path_str.split(' ')
    i = 0
    while i < len(arr):
        if arr[i] == 'Z':
            point_symbol = arr[i]
            input_points.append(['', point_symbol])
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
                point_name = 'p' + str(points_num)
                x_position = parse_position(arr[i + j * 2 + 1])
                y_position = parse_position(arr[i + j * 2 + 2])
                input_points.append([point_name, point_symbol, x_position, y_position])
                points_num += 1
            i += 3
        elif arr[i] == 'Q':
            point_symbol = arr[i]
            for j in range(2):
                point_name = 'p' + str(points_num)
                x_position = parse_position(arr[i + j * 2 + 1])
                y_position = parse_position(arr[i + j * 2 + 2])
                input_points.append([point_name, point_symbol, x_position, y_position])
                points_num += 1
            i += 5
        elif arr[i] == 'S':
            point_symbol = arr[i]
            for j in range(2):
                point_name = 'p' + str(points_num)
                x_position = parse_position(arr[i + j * 2 + 1])
                y_position = parse_position(arr[i + j * 2 + 2])
                input_points.append([point_name, point_symbol, x_position, y_position])
                points_num += 1
            i += 5
        elif arr[i] == 'L':
            point_symbol = arr[i]
            for j in range(1):
                point_name = 'p' + str(points_num)
                x_position = parse_position(arr[i + j * 2 + 1])
                y_position = parse_position(arr[i + j * 2 + 2])
                input_points.append([point_name, point_symbol, x_position, y_position])
                points_num += 1
            i += 3
        elif arr[i] == 'C':
            point_symbol = arr[i]
            for j in range(3):
                point_name = 'p' + str(points_num)
                x_position = parse_position(arr[i + j * 2 + 1])
                y_position = parse_position(arr[i + j * 2 + 2])
                input_points.append([point_name, point_symbol, x_position, y_position])
                points_num += 1
            i += 7
        elif arr[i] == 'A':
            point_name = 'p' + str(points_num)
            point_symbol = arr[i]
            x_position = parse_position(arr[i + 6])
            y_position = parse_position(arr[i + 7])
            input_points.append(
                [point_name, point_symbol, x_position, y_position, parse_position(arr[i + 1]),
                 parse_position(arr[i + 2]), arr[i + 3], arr[i + 4],
                 arr[i + 5]])
            points_num += 1
            i += 8
        else:
            raise JsonException('error symbol')
            # print(input_points)


# 讲已得到的航点生成代码（getPath方法体）
def trans_points2code(points):
    # print('in trans_points2code')
    point_code = '''        auto %s = createPoint(%s, %s);'''
    output = ''
    ss_code0 = '''        std::stringstream ss;\n'''
    ss_code1 = '''        ss << "%s " << %s.get_x() << " " << %s.get_y() << " ";\n'''
    ss_code2 = '''        ss << "%s " << %s.get_x() << " " << %s.get_y()<< " " << %s.get_x() << " " << %s.get_y() << " ";\n'''
    ss_code3 = '''        ss << "%s " << %s.get_x() << " " << %s.get_y()<< " " << %s.get_x() << " " << %s.get_y() << " " << %s.get_x() << " " << %s.get_y() << " ";\n'''
    for i in range(len(points)):
        point = points[i]
        output += point_code % (point[0], point[2], point[3]) + '\n'

    output += ss_code0
    # for i in range(len(points)):
    i = 0
    while i < len(points):
        point = points[i]
        if point[1] == 'Z':
            output += '''        ss << Z;\n'''
        if point[1] == 'M':
            p0 = points[i]
            output += ss_code1 % (p0[1], p0[0], p0[0])
            i += 1
        elif point[1] == 'L':
            p0 = points[i]
            output += ss_code1 % (p0[1], p0[0], p0[0])
            i += 1
        elif point[1] == 'Q':
            p0 = points[i]
            p1 = points[i + 1]
            output += ss_code2 % (p0[1], p0[0], p0[0], p1[0], p1[0])
            i += 2
        elif point[1] == 'S':
            p0 = points[i]
            p1 = points[i + 1]
            output += ss_code2 % (p0[1], p0[0], p0[0], p1[0], p1[0])
            i += 2
        elif point[1] == 'C':
            p0 = points[i]
            p1 = points[i + 1]
            p2 = points[i + 2]
            output += ss_code3 % (p0[1], p0[0], p0[0], p1[0], p1[0], p2[0], p2[0])
            i += 3
        elif point[1] == 'A':
            p0 = points[i]
            output += '''        ss << "%s " << %s << " " << %s<< " " << %s << " " << %s  <<" "<< %s << " " << %s.get_x() << " " << %s.get_y() << " ";\n''' % (
                p0[1], p0[4], p0[5], p0[6], p0[7], p0[8], p0[0], p0[0])
            i += 1
        else:
            raise JsonException('error symbol')

    # output += ss_code1 % ()
    # print(output)
    output += '''        return ss.str();\n'''
    return output


def out_getPath_func(svg_path_code, class_name, conditions):
    parse_points(svg_path_code)
    func_body = trans_points2code(input_points)
    output = '''\n  ////%s interface
    const std::string %s::getPath() const {
%s
    }
''' % (class_name, class_name, func_body)
    return output
    # print(output)


def generate_file(original_name, h_code, cpp_code):
    class_name = parse_name(original_name)
    with open(original_name + '.h', 'w+', encoding='utf-8') as f:
        f.write(h_code)
    f.close()
    with open(original_name + '.cpp', 'w+', encoding='utf-8') as f:
        f.write(cpp_code)
    f.close()
    # print('#include "comp_custom/%s.h"\n' % original_name)
    # print('''std::function<std::shared_ptr<ComponentAbstract>()> new%s = []()
    # {
    #      return std::dynamic_pointer_cast<ComponentAbstract>(std::make_shared<%s>());
    # };''' % (class_name, class_name))
    # print('{"%s",new%s},\n' % (original_name, class_name))


def default_generate():
    original_name = input('输入以_间隔的组件名:')
    control = False if input('输入关键点数目：') == '0' else True
    path = input('输入以x、y、w、h表示的path路径:')
    # print(parse_points(path))

    control_num = int(control)
    conditions = []
    # control = False
    # control_condition = []
    # control因素：初始位置、x范围、y范围、x和y的约束关系、矩形变化时的从动属性
    # [[x0,y0],[maxX,minX],[maxY,minY],]
    if control:
        for i in range(control_num):
            control_condition = []
            control_position_str = input('输入control点%s的初始位置（x、y、w、h表示）：' % i)
            control_position_arr = control_position_str.split(' ')
            control_position = [parse_position(control_position_arr[0]),
                                parse_position(control_position_arr[1])]
            x_range = 'x x+w'
            y_range = 'y y+h'
            while True:
                move_method = input('请输入control点%s的移动方式（0：只能横向移动；1：只能纵向移动；2：可以横向或纵向移动；3：沿对角线移动）：' % i)
                if move_method == '0':
                    x_range = input('请输入横向移动范围（默认为矩形内部）：')
                    break
                elif move_method == '1':
                    y_range = input('请输入纵向移动范围（默认为矩形内部）：')
                    break
                elif move_method == '2':
                    x_range = input('请以"minX maxX"的形式输入横向移动范围（默认为矩形内部）：')
                    y_range = input('请输入纵向移动范围（默认为矩形内部）：')
                    break
                elif move_method == '3':
                    flag = input('请输入Control移动范围（1：半宽高；2：全宽高）：')
                    if flag == '1':
                        x_range = 'x x+w*0.5'
                        y_range = 'y y+h*0.5'
                    break
            # move_update = input('请输入矩形改变时control%s的从动方式（0：等比例变化；1：相对于初始点保持不动）：' % i)
            move_update = '0'
            x_range_arr = x_range.split(' ')
            x_range = [parse_position(x_range_arr[0]), parse_position(x_range_arr[1])]

            y_range_arr = y_range.split(' ')
            y_range = [parse_position(y_range_arr[0]), parse_position(y_range_arr[1])]

            control_condition = [control_position, [move_method, move_update], x_range, y_range]
            conditions.append(control_condition)

    h_code = get_h(original_name, control, conditions)
    cpp_code = get_cpp_code(control, original_name, path, conditions)
    # generate_file(original_name, h_code, cpp_code)


def main(argv):
    global control, control_num
    try:
        opts, args = getopt.getopt(argv, "hdj:", ["help", "default", "json="])
        # print(argv)
    except getopt.GetoptError:
        print('Error: generateCpp.py -j <jsonfile> or: generateCpp.py --json=<jsonfile>')
        print('   or: generateCpp.py -d or: generateCpp.py --default')
        sys.exit(2)
    if len(argv) == 0:
        default_generate()

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('Error: generateCpp.py -j <jsonfile> or: generateCpp.py --json=<jsonfile>')
            print('   or: generateCpp.py -d or: generateCpp.py --default')
            sys.exit()
        elif opt in ("-j", '--json'):
            # print(opt)
            # jsonfile = open(COMPONENT_JSON_PATH + arg)
            # print(COMPONENT_JSON_PATH + arg)
            get_comp_by_json(COMPONENT_JSON_PATH + arg)

        elif opt in ('-d', '--default'):
            default_generate()


global write_area
write_area = ['x', 'y', 'h', 'w']


class JsonException(Exception):
    def __init__(self, reason):
        self.reason = reason


def get_comp_by_json(path):
    global control_num, write_area
    # input0 = input()
    # print("input:" + input0)
    # print("arg:" + arg)
    # str = '{"name":"class_name","path":"M x y"}'
    jsonfile = open(path)
    input_json = jsonfile.read()
    # print("input_json:" + input_json)
    data = json.loads(input_json)
    # print(data)
    controls_arr_for_svg = []
    if not data.__contains__('name'):
        print('need name')
    if not data.__contains__('path'):
        print('need path')
    original_name = data['name']
    if data.__contains__('control_point_num'):
        control = True
        control_num = int(data['control_point_num'])
        if control_num == 0:
            control = False
    else:
        control = False
    path = data['path']
    conditions = []
    control_names = ['RB', 'R', 'RT', 'L', 'LT', 'LB', 'T', 'B']
    if data.__contains__('controls'):
        for condition_json in data['controls']:
            if not condition_json.__contains__('control_name'):
                print('need control name')
                raise Exception
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
                                         condition_json['y_range'] if condition_json.__contains__('y_range') else []])
            control_position = [parse_position(condition_json["default_position"]["default_x"]),
                                parse_position(condition_json["default_position"]["default_y"])]

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
                    x_range = [parse_position(condition_json["x_range"]["min"]),
                               parse_position(condition_json["x_range"]["max"])]
                except KeyError:
                    raise JsonException('wrong x range')

            if condition_json.__contains__('y_range') and not condition_json["y_range"]["min"] == '':
                try:
                    y_range = [parse_position(condition_json["y_range"]["min"]),
                               parse_position(condition_json["y_range"]["max"])]
                except KeyError:
                    raise JsonException('wrong y range')

            if not condition_json.__contains__('constrain'):
                conditions.append(
                    [control_position, [move_method, move_update], x_range, y_range, control_name])
            else:
                conditions.append(
                    [control_position, [move_method, move_update], x_range, y_range,
                     control_name, condition_json['constrain']])

    # h_code = get_h(original_name, control, conditions)
    # cpp_code = get_cpp_code(control, original_name, path, conditions, write_area)
    # generate_file(original_name, h_code, cpp_code)

    # for ctr in conditions:
    #     controls_arr_for_svg.append([ctr[4], ctr[0][0], ctr[0][1]])
    return [generateSVG.generateSVG(original_name, path, write_area, controls_arr_for_svg, 'cpp'), original_name, path,
            write_area, controls_arr_for_svg]


# get_path(path)
global control
global control_num
# if __name__ == "__main__":
    # # main(sys.argv[1:])
    # main(['-j', 'big_arrow_left.json'])
