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

print(tk.CURRENT)
x = 50
y = 50


class Block():
    def __init__(self, canvas: tk.Canvas):
        self.item_ids = []
        self.canvas = canvas

        # oval1 = canvas.create_oval(72 + x, 22 + y, 78 + x, 28 + y, fill='orange')
        # oval2 = self.canvas.create_oval(180, 180, 50, 50, fill='white')
        # self.item_ids.append(oval1)
        # self.item_ids.append(oval2)
        # self.set_item_mapping()

    def move_to(self, x: float, y: float):
        for id in self.item_ids:
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

                # if event.x - self.relativePos[0] >= x + 100:
                #     self.itemMap[a[0]].move_to(x + 100, event.y - self.relativePos[1])
                # if event.y - self.relativePos[1] >= y + 100:
                #     self.itemMap[a[0]].move_to(event.x - self.relativePos[0], y + 100)
                # if event.x - self.relativePos[0] <= x:
                #     self.itemMap[a[0]].move_to(x, event.y - self.relativePos[1])
                # if event.y - self.relativePos[1] <= y:
                #     self.itemMap[a[0]].move_to(event.x - self.relativePos[0], y)
                if x + 300 >= event.x - self.relativePos[0] >= x and y + 300 >= event.y - self.relativePos[1] >= y:
                    self.itemMap[a[0]].move_to(event.x - self.relativePos[0], event.y - self.relativePos[1])
                    # print(event.x - self.relativePos[0] - x)
                    # TODO
                    controls[0][1] = str(event.x - self.relativePos[0])
                    controls[0][2] = str(event.y - self.relativePos[1])
                    import generateSVG
                    generateSVG.generateSVG(comp_name, path_d, controls, 'update')
                    global svg_image
                    svg_image.configure(file="./svg/%s.svg" % comp_name)
                    # self.create_image(150 + x, 150 + y, image=svg_image)


global comp_name, path_d, controls
# canvas_width = 190
# canvas_height = 150
from generateCpp import get_comp_by_json
from tkinter.filedialog import *

master = tk.Tk()
filepath = askopenfilename()
# print(filepath)



print(filepath)
filepath = filepath.replace('/', '\\\\')
if filepath[-4:] == 'json':
    print(filepath[-4:])
    [svg_path, comp_name, path_d, controls] = get_comp_by_json(filepath)

    # controls = parse_control_pos(controls)
    # path.replace('\\','\\\\')
    print("controls in ui" + str(controls))
    print(svg_path)

    svg_image = tksvg.SvgImage(file=svg_path)
    w = MyCanvas(master, bg='white')
    #
    w.create_image(100 + x, 100 + y, image=svg_image)
    ovals = []
    oval_map={}
    for ctr in controls:
        oval = w.create_oval(eval(ctr[1]) - 3 + x, eval(ctr[2]) - 3 + y, eval(ctr[1]) + 3 + x, eval(ctr[2]) + 3 + y, fill='orange')
        # oval.id = ctr[0]
        ovals.append(oval)
        oval_map.update(oval,ctr[0])

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
    tk.mainloop()
else:
    exit()
