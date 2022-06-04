
## 必选
- "name"
  纯小写，以"_"间隔
  
- "path"
  <path>标签的D属性，命令同SVG，其参数（航点坐标）用x\y\w\h以及控制点.[xyhw]的组合式表示
  
## 可选
- "control_point_num"
  控制点数量
  
- "controls"
  列表，包含关于每个控制点的描述，其长度必须与control_point_num相等
  
### 控制点描述
- "control_name"
  必选，描述控制点的标识名，可以在"path"与"constrain"中使用
  
- "default_position"
  必选，描述控制点的初始位置，由x、y、h、w构成的表达式描述
  - "default_x"
  - "default_y"
  
- "move_method"
  必选，描述控制点的移动方式，分为以下四种：
  - "0"
    仅能横向移动（只需指定x_range）
  - "1"
    仅能纵向移动（只需指定y_range）
  - "2"
    能够在横向和纵向移动
  - "3"
    水平和垂直方向上移动的距离始终相等
  

- "move_update"
  必选，描述矩形关键点改变时控制点的从动方式
  - "1"：保持距离左边界和上边界的距离（除非超出范围）
  - "0"：距离左边界和上边界的距离随着width和height等比例变化

- "x_range"
  描述控制点水平方向的移动范围，由x和w的表达式描述；根据移动方式决定是否必须
  - "max"
  - "min"
  
- "y_range"
  描述控制点垂直方向的移动范围，同理。
  
- "constrain"
  可选，描述控制点的约束，基于C++的语法，可以以$变量名的形式引用控制点变量


```json
{
  "name": "component_name",
  "control_point_num": "2（可选）",
  "path": "M x abc.y L abc.x abc.y L abc.x y L x+w y+h*0.5 L abc.x y+h L abc.x y+h-abc.h L x y+h-abc.h L cde.x cde.y L x abc.y",
  "controls": [
    {
      "control_name": "abc",
      "default_position": {
        "default_x": "x+w*0.75",
        "default_y": "y+h*0.25"
      },
      "move_method": "2",
      "move_update": "0",
      "x_range": {
        "min": "x",
        "max": "x+w"
      },
      "y_range": {
        "min": "y",
        "max": "y+h*0.5"
      },
      "constrain": "if($abc.x<$cde.x){$abc->setX($cde.x);}"
    },
    {
      "control_name": "cde",
      "default_position": {
        "default_x": "x",
        "default_y": "y+h*0.5"
      },
      "move_method": "0",
      "move_update": "1",
      "x_range": {
        "min": "x",
        "max": "x+w"
      },
      "y_range": {
        "min": "y",
        "max": "y+h"
      },
      "constrain": "if($cde.x>$abc.x){$cde->setX($abc.x);}"
    }
  ]
}
```