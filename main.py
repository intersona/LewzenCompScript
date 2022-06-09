# # from svglib.svglib import svg2rlg
# # from reportlab.graphics import renderPDF, renderPM
# #
# # drawing = svg2rlg("./svg/comp.svg")
# # renderPM.drawToFile(drawing, "temp.png", fmt="PNG")
# #
# #
# # from tkinter import *
# #
# # tk = Tk()
# #
# #
# # from PIL import Image, ImageTk
# #
# # img = Image.open('temp.png')
# # pimg = ImageTk.PhotoImage(img)
# # size = img.size
# #
# #
# # frame = Canvas(tk, width=size[0], height=size[1])
# # frame.pack()
# # frame.create_image(0,0,anchor='nw',image=pimg)
# #
# # tk.mainloop()
#
# import tkinter as tk
# from tkinter import Canvas, Label
# from functools import partial
#
import json

import tksvg

#
#
# class SelectedCanvas(Canvas):
#     '''可调整组件大小、可移动的画布'''
#
#     def __init__(self, master=None, cnf={}, **kw):
#         Canvas.__init__(self, master, cnf, **kw)
#         self.config(bd=0, highlightthickness=0)
#         self.is_sizing = False
#         self.old_width = 0
#         self.old_height = 0
#         self.old_pos_x = 0
#         self.old_pos_y = 0
#         self.start_x = 0
#         self.start_y = 0
#         self.start_root_x = 0
#         self.start_root_y = 0
#         self.on_resize_complete = None
#         self.have_child = False  # 用以辨别是否有组件创建
#
#     def _mousedown(self, event):
#         self.startx = event.x
#         self.starty = event.y
#
#     def _drag(self, event):
#         try:
#             self.place(x=self.winfo_x() + (event.x - self.startx), y=self.winfo_y() + (event.y - self.starty))
#         except AttributeError:
#             raise ValueError("The widget %s is not draggable" % self.widget)
#
#     def set_on_resize_complete(self, on_resize_complete):
#         self.on_resize_complete = on_resize_complete
#
#     def on_update(self):
#         self.create_rectangle(-1, -1, -2, -2, tag='side', dash=3, outline='grey')
#         self.tag_bind('side', "<Button-1>", self._mousedown, add='+')
#         self.tag_bind('side', "<B1-Motion>", self._drag, add='+')
#         self.tag_bind('side', '<Enter>', lambda event: self.config(cursor='fleur'))
#         self.tag_bind('side', '<Leave>', lambda event: self.config(cursor='arrow'))
#         for name in ('nw', 'w', 'sw', 'n', 's', 'ne', 'e', 'se'):
#             self.create_rectangle(-1, -1, -2, -2, tag=name, outline='blue')
#             self.tag_bind(name, "<Enter>", partial(self.on_mouse_enter, name))
#             self.tag_bind(name, "<Leave>", partial(self.on_mouse_leave, name))
#             self.tag_bind(name, "<Button-1>", partial(self.on_mouse_click, name))
#             self.tag_bind(name, "<B1-Motion>", partial(self.on_mouse_move, name))
#             self.tag_bind(name, "<ButtonRelease-1>", partial(self.on_mouse_release, name))
#
#     def show(self, is_fill=False):
#         width = self.winfo_width()
#         height = self.winfo_height()
#         self.coords('side', 6, 6, width - 6, height - 6)
#         self.coords('nw', 0, 0, 7, 7)
#         self.coords('sw', 0, height - 8, 7, height - 1)
#         self.coords('w', 0, (height - 7) / 2, 7, (height - 7) / 2 + 7)
#         self.coords('n', (width - 7) / 2, 0, (width - 7) / 2 + 7, 7)
#         self.coords('s', (width - 7) / 2, height - 8, (width - 7) / 2 + 7, height - 1)
#         self.coords('ne', width - 8, 0, width - 1, 7)
#         self.coords('se', width - 8, height - 8, width - 1, height - 1)
#         self.coords('e', width - 8, (height - 7) / 2, width - 1, (height - 7) / 2 + 7)
#         if is_fill:
#             for name in ('nw', 'w', 'sw', 'n', 's', 'ne', 'e', 'se'):
#                 self.itemconfig(name, fill='blue')
#
#     def hide(self):
#         self.coords('side', -1, -1, -2, -2, )
#         for name in ('nw', 'w', 'sw', 'n', 's', 'ne', 'e', 'se'):
#             self.coords(name, -1, -1, -2, -2)
#
#     def on_mouse_enter(self, tag_name, event):
#         if tag_name in ("nw", "sw", "ne", "se"):
#             self["cursor"] = "sizing"
#         elif tag_name in ("w", "e"):
#             self["cursor"] = "sb_h_double_arrow"
#         else:
#             self["cursor"] = "sb_v_double_arrow"
#
#     def on_mouse_leave(self, tag_name, event):
#         if self.is_sizing:
#             return
#         self["cursor"] = "arrow"
#
#     def on_mouse_click(self, tag_name, event):
#         self.is_sizing = True
#         self.start_x = event.x
#         self.start_y = event.y
#         self.start_root_x = event.x_root
#         self.start_root_y = event.y_root
#         self.old_width = self.winfo_width()
#         self.old_height = self.winfo_height()
#         self.old_pos_x = int(self.place_info()['x'])
#         self.old_pos_y = int(self.place_info()['y'])
#
#     def on_mouse_move(self, tag_name, event):
#         if not self.is_sizing:
#             return
#         if 'e' in tag_name:
#             width = max(0, self.old_width + (event.x - self.start_x))
#             self.place_configure(width=width)
#         if 'w' in tag_name:
#             width = max(0, self.old_width + (self.start_root_x - event.x_root))
#             to_x = event.x - self.start_x + int(self.place_info()['x'])
#             self.place_configure(width=width, x=to_x)
#         if 's' in tag_name:
#             height = max(0, self.old_height + (event.y - self.start_y))
#             self.place_configure(height=height)
#         if 'n' in tag_name:
#             height = max(0, self.old_height + (self.start_root_y - event.y_root))
#             to_y = event.y - self.start_y + int(self.place_info()['y'])
#             self.place_configure(height=height, y=to_y)
#         self.after_idle(self.show)
#
#     def on_mouse_release(self, tag_name, event):
#         self.is_sizing = False
#         if self.on_resize_complete is not None:
#             self.on_resize_complete()
#         self["cursor"] = "arrow"
#
#     def create_widget(self, widget_class, cnf={}, **kw):
#         if self.have_child == True:  # 如果已经创建，则忽略
#             return
#         self.have_child = True
#         self.widget = widget_class(self, cnf, **kw)
#         self.widget.pack(fill='both', expand=True, pady=9, padx=9)
#         # 即使拖动组件，也可以移动
#         self.widget.bind("<Button-1>", self.mousedown, add='+')
#         self.widget.bind("<B1-Motion>", self.drag, add='+')
#         self.widget.bind('<FocusOut>', lambda event: self.delete('all'))
#         self.widget.bind('<FocusIn>', lambda event: (self.on_update(), self.show()))
#
#     def mousedown(self, event):
#         self.widget.focus_set()
#         self.__startx = event.x
#         self.__starty = event.y
#
#     def drag(self, event):
#         self.place(x=self.winfo_x() + (event.x - self.__startx), y=self.winfo_y() + (event.y - self.__starty))
#
#
# window = tk.Tk()

# # label = tk.Label(image=svg_image,bg='white')
# # label.pack()

# canvas = SelectedCanvas(window)
# canvas.create_image(50 + x, 50 + y, image=svg_image)
# # canvas.create_widget(Label,image=svg_image,bg='white')
# canvas.create_oval(72 + x, 22 + y, 78 + x, 28 + y, fill='orange')
# # canvas.create_widget(tk.PhotoImage ,file="./svg/comp1.svg")
# canvas.pack()
# window.mainloop()


import tkinter as tk

from generateJs import read_ori_json

# print(tk.CURRENT)
offset_x = 50
offset_y = 50


class Block():
    def __init__(self, canvas: tk.Canvas):
        self.item_ids = []
        self.canvas = canvas

        # oval1 = canvas.create_oval(72 + x, 22 + y, 78 + x, 28 + y, fill='orange')
        # oval2 = self.canvas.create_oval(180, 180, 50, 50, fill='white')
        # self.item_ids.append(oval1)
        # self.item_ids.append(oval2)
        # self.set_item_mapping()

    def move_to(self, id: int, x: float, y: float):
        self.canvas.move_to(id, x, y)

    def set_item_mapping(self):
        for id in self.item_ids:
            self.canvas.itemMap[id] = self


global svg_image


class MyCanvas(tk.Canvas):
    def __init__(self, parent, cnf={}, **kw):
        super().__init__(parent, cnf={}, **kw)
        self.itemToMove = None
        self.relativePos = ()

        self.itemMap = {}  # 东西的映射。当拖动等事件发生时，修改这个字典中的对象。
        self.bind('<ButtonPress-1>', self.on_mouse_down)
        self.bind('<B1-Motion>', self.on_mouse_drag)
        # self.background = 'white'

    def on_mouse_down(self, event):
        self.relativePos = ()
        a = self.find_withtag(tk.CURRENT)
        if len(a) >= 1:
            coor = self.coords(a[0])
            x, y = event.x - coor[0], event.y - coor[1]
            self.relativePos = (x, y)
            self.itemToMove = a[0]
        else:
            self.itemToMove = None

    def move_to(self, item_id, x, y):
        pos = self.coords(item_id)
        self.move(item_id, x - pos[0], y - pos[1])

    def on_mouse_drag(self, event):
        if not self.itemToMove:  # 如果没有要移动的对象，就直接return,防止出现奇奇怪怪的错误。
            return

        a = self.find_withtag(tk.CURRENT)
        if len(a) >= 1:
            if a[0] in self.itemMap:
                if offset_x + 200 >= event.x - self.relativePos[0] >= offset_x and offset_y + 200 >= event.y - \
                        self.relativePos[1] >= offset_y:
                    global comp_name, path_d, controls, oval_map, svg_path, wa
                    self.itemMap[a[0]].move_to(a[0], event.x - self.relativePos[0], event.y - self.relativePos[1])
                    # print(event.x - self.relativePos[0] - x)
                    ctr_num = get_keys(oval_map, a[0])
                    # TODO
                    controls[int(ctr_num[0])][1] = str(event.x - self.relativePos[0] - offset_x)
                    controls[int(ctr_num[0])][2] = str(event.y - self.relativePos[1] - offset_y)
                    import generateSVG

                    new_svg_path = generateSVG.generateSVG(comp_name, path_d, wa, controls, 'update')
                    global svg_image
                    svg_image.configure(file=new_svg_path)
                    # self.create_image(150 + x, 150 + y, image=svg_image)


global comp_name, path_d, controls, oval_map, svg_path, wa
# canvas_width = 190
# canvas_height = 150
from generateCpp import get_comp_by_json
from tkinter.filedialog import *


# print(filepath)


def get_keys(d, value):
    return [k for k, v in d.items() if v == value]


def save_json():
    global master2
    data['name'] = comp_name_str.get()
    data['path'] = path_str.get()
    if data.__contains__('write_area'):
        data['write_area']['x'] = write_area_x_str.get()
        data['write_area']['y'] = write_area_y_str.get()
        data['write_area']['width'] = write_area_w_str.get()
        data['write_area']['height'] = write_area_h_str.get()

    if data.__contains__('controls'):
        for j in range(len(data['controls'])):
            data['controls'][j]['control_name'] = control_strvs[j][0].get()
            data['controls'][j]['default_position']['default_x'] = control_strvs[j][1].get()
            data['controls'][j]['default_position']['default_y'] = control_strvs[j][2].get()
            data['controls'][j]['move_method'] = control_strvs[j][3].get()
            data['controls'][j]['x_range']['min'] = control_strvs[j][4].get()
            data['controls'][j]['x_range']['max'] = control_strvs[j][5].get()
            data['controls'][j]['y_range']['min'] = control_strvs[j][6].get()
            data['controls'][j]['y_range']['max'] = control_strvs[j][7].get()

    # print(data)
    newjson = json.dumps(data)
    json_file = open(filepath, 'w+')
    print('filepath:' + filepath)
    json_file.write(newjson)
    json_file.close()
    # for i in frame1.winfo_children():
    #     i.destroy()
    # frame1.destroy()
    if filepath[-4:] == 'json':
        if not master2 == None:
            master2.destroy()
        global comp_name, path_d, controls, oval_map, svg_path, svg_image, wa
        # print(filepath[-4:])
        try:
            [svg_path, comp_name, path_d, wa, controls] = get_comp_by_json(filepath)
            read_ori_json(filepath)
            print('svg_path:' + svg_path)
        except Exception as e:
            tk.messagebox.showinfo(title='JsonError', message=e)
            return
        current_path = os.path.abspath(__file__)
        parent_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
        print(parent_path)
        config_path = parent_path + '\\newjson\\config.json'
        config_file = open(config_path)
        config_json = config_file.read()
        config_file.close()
        # print(config_json)
        config_dict = json.loads(config_json)
        config_url = '../main/newjson/%s_js.json' % comp_name
        config_svg = '../main/svg/%s.png' % comp_name
        flag = True
        for comp in config_dict['component']:
            if comp['url'] == config_url:
                flag = False

        if flag:
            config_dict['component'].append(
                {"url": config_url, "svg": config_svg})

        output_config_json = json.dumps(config_dict)
        config_file = open(config_path, 'w+')
        config_file.write(output_config_json)
        config_file.close()

        master2 = tk.Toplevel()
        master2.title('组件预览')

        # controls = parse_control_pos(controls)
        # path.replace('\\','\\\\')
        # print("controls in ui" + str(controls))
        # print(svg_path)

        svg_image = tksvg.SvgImage(file=svg_path)
        w = MyCanvas(master2, bg='white')
        #
        w.create_image(100 + offset_x, 100 + offset_y, image=svg_image)
        ovals = []
        oval_map = {}
        for i in range(len(controls)):
            ctr = controls[i]
            oval = w.create_oval(eval(ctr[1]) - 3 + offset_x, eval(ctr[2]) - 3 + offset_y, eval(ctr[1]) + 3 + offset_x,
                                 eval(ctr[2]) + 3 + offset_y,
                                 fill='orange')
            # oval.id = ctr[0]
            ovals.append(oval)
            oval_map[str(i)] = oval

        # oval = w.create_oval(222 - 3 + x, 72 - 3 + y, 228 + 3 + x, 78 + 3 + y, fill='orange')
        # ovals.append(oval)

        #
        w.pack(fill=tk.BOTH, expand=1)
        #
        # print(w.find_all())
        b = Block(w)
        for oval in ovals:
            b.item_ids.append(oval)
        # b.item_ids.append(oval)
        b.set_item_mapping()
        #
        # tk.mainloop()
        master2.mainloop()
    else:
        exit()


global master2
master2 = None
import tkinter.messagebox

from tkinter import ttk

if __name__ == '__main__':

    master = tk.Tk()
    master.geometry("320x600")
    master.title('设置您的组件')
    canvas = Canvas(master, scrollregion=(0, 0, 300, 1300), height=900)  # 创建canvas
    canvas.place(x=300, y=800)
    frame1 = tk.Frame(canvas)
    frame1.place(width=300, height=800)
    vbar = Scrollbar(canvas, orient=VERTICAL)  # 竖直滚动条
    vbar.place(x=300, width=20, height=800)
    vbar.configure(command=canvas.yview)
    canvas.config(yscrollcommand=vbar.set)  # 设置
    canvas.create_window((150, 550), window=frame1)  # create_window
    canvas.pack()
    filepath = askopenfilename()

    # print(filepath)
    # filepath = filepath.replace('/', '\\\\')
    jsonfile = open(filepath)
    input_json = jsonfile.read()
    # print(input_json)
    jsonfile.close()
    data = json.loads(input_json)
    # print('input_json in ui:' + input_json)
    labels = []
    entries = []

    l_comp_name = Label(frame1, text='组件名')
    comp_name_str = tk.StringVar()
    comp_name_str.set(value=data['name'])
    e1 = Entry(frame1, width=30, textvariable=comp_name_str)
    labels.append(l_comp_name)
    entries.append(e1)

    l_path = Label(frame1, text='path')
    path_str = tk.StringVar()
    path_str.set(data['path'])
    e2 = Entry(frame1, state=NORMAL, width=30, textvariable=path_str)
    labels.append(l_path)
    entries.append(e2)

    if data.__contains__('write_area'):
        l_write_area_x = Label(frame1, text='write_area:x')
        write_area_x_str = tk.StringVar()
        write_area_x_str.set(data['write_area']['x'])
        e3 = Entry(frame1, state=NORMAL, width=30, textvariable=write_area_x_str)
        labels.append(l_write_area_x)
        entries.append(e3)

        l_write_area_y = Label(frame1, text='write_area:y')
        write_area_y_str = tk.StringVar()
        write_area_y_str.set(data['write_area']['y'])
        e4 = Entry(frame1, state=NORMAL, width=30, textvariable=write_area_y_str)
        labels.append(l_write_area_y)
        entries.append(e4)

        l_write_area_w = Label(frame1, text='write_area:w')
        write_area_w_str = tk.StringVar()
        write_area_w_str.set(data['write_area']['width'])
        e5 = Entry(frame1, state=NORMAL, width=30, textvariable=write_area_w_str)
        labels.append(l_write_area_w)
        entries.append(e5)

        l_write_area_h = Label(frame1, text='write_area:h')
        write_area_h_str = tk.StringVar()
        write_area_h_str.set(data['write_area']['height'])
        e6 = Entry(frame1, state=NORMAL, width=30, textvariable=write_area_h_str)
        labels.append(l_write_area_h)
        entries.append(e6)

    for i in range(len(labels)):
        labels[i].pack()
        entries[i].pack()

    control_texts = ["control_name", "default_position:x", "default_position:y", "move_method", "x_range:min",
                     "x_range:max", "y_range:min", "y_range:max"]
    control_entries = []
    control_labels = []
    control_strvs = []

    if data.__contains__('control_point_num'):
        # print('data[control_point_num]:' + data['control_point_num'])
        if not int(data['control_point_num']) == 0:
            ctr_num = int(data['control_point_num'])
            for j in range(ctr_num):
                ctr = data['controls'][j]
                try:
                    ctrs = [ctr['control_name'], ctr['default_position']['default_x'],
                            ctr['default_position']['default_y'],
                            ctr['move_method'], ctr['x_range']['min'], ctr['x_range']['max'], ctr['y_range']['min'],
                            ctr['y_range']['max']]
                except:
                    tk.messagebox.showinfo(title='JsonError', message='json数据不完整')
                control_entries.append([])
                control_labels.append([])
                control_strvs.append([])
                for k in range(len(control_texts)):
                    control_labels[j].append(Label(frame1, text=control_texts[k]))
                    control_strvs[j].append(StringVar())
                    control_strvs[j][k].set(ctrs[k])
                    control_entries[j].append(Entry(frame1,width=30, textvariable=control_strvs[j][k]))
            for j in range(ctr_num):
                for k in range(len(control_texts)):
                    # if 1<=k<=2:
                    #     control_labels[j][k].pack(side=LEFT)
                    #     control_entries[j][k].pack(side=LEFT)
                    # else:
                    #     control_labels[j][k].pack(side=TOP)
                    #     control_entries[j][k].pack(side=TOP)
                    control_labels[j][k].pack(side=TOP)
                    control_entries[j][k].pack(side=TOP)

    save_control_btn = tk.Button(frame1, text='确认配置', command=save_json)
    save_control_btn.pack()

    tk.mainloop()

# frame1.pack()
#
# if filepath[-4:] == 'json':
#
#     print(filepath[-4:])
#     [svg_path, comp_name, path_d, controls] = get_comp_by_json(filepath)
#
#     # controls = parse_control_pos(controls)
#     # path.replace('\\','\\\\')
#     print("controls in ui" + str(controls))
#     print(svg_path)
#
#     svg_image = tksvg.SvgImage(file=svg_path)
#     w = MyCanvas(master, bg='white')
#     #
#     w.create_image(100 + offset_x, 100 + offset_y, image=svg_image)
#     ovals = []
#     oval_map = {}
#     for i in range(len(controls)):
#         ctr = controls[i]
#         oval = w.create_oval(eval(ctr[1]) - 3 + offset_x, eval(ctr[2]) - 3 + offset_y, eval(ctr[1]) + 3 + offset_x,
#                              eval(ctr[2]) + 3 + offset_y,
#                              fill='orange')
#         # oval.id = ctr[0]
#         ovals.append(oval)
#         oval_map[str(i)] = oval
#
#     # oval = w.create_oval(222 - 3 + x, 72 - 3 + y, 228 + 3 + x, 78 + 3 + y, fill='orange')
#     # ovals.append(oval)
#
#     #
#     w.pack(fill=tk.BOTH, expand=1)
#     #
#     # print(w.find_all())
#     b = Block(w)
#     for oval in ovals:
#         b.item_ids.append(oval)
#     # b.item_ids.append(oval)
#     b.set_item_mapping()
#     #
#     # tk.mainloop()
# else:
#     exit()
