# props

```json
{
  "name": "class_name",
  "control_point_num": "1",
  "path": "",
  "controls": [
    {
      "control_name": "control0",
      "default_position": {
        "default_x": "x",
        "default_y": "y"
      },
      "move_method": "1",
      "move_update": "1",
      "x_range": {
        "min": "x",
        "max": "x+w"
      },
      "y_range": {
        "min": "y",
        "max": "y+h"
      }
    }
  ]
}
```

# Collate

```
M x+w*0.9 y C x+w y x+w y x+w*0.85 y+h*0.15 L x+w*0.15 y+h*0.85 C x y+h x y+h x+w*0.1 y+h L x+w*0.9 y+h C x+w y+h x+w y+h x+w*0.85 y+h*0.85 L x+w*0.15 y+h*0.15 C x y x y x+w*0.1 y L x+w*0.9 y
```

# Card

```
M x+w y L x+w y+h L x y+h L x y+ch*2 L x+cw*2 y L x+w y
```

# cylinder

```
M x cy A w*0.5 ch 0 0 1 x+w cy A w*0.5 ch 0 0 1 x cy L x y+h-ch A w*0.5 ch 0 0 0 x+w y+h-ch L x+w cy
```

# document

``` 
M x cy A w*0.4 h-ch 0 0 0 x+w*0.5 cy A w*0.4 h-ch 0 0 1 x+w cy L x+w y L x y L x cy
```

# hexagon

```
M x y+h*0.5 L cx y L x+w-cw y L x+w y+h*0.5 L x+w-cw y+h L cx y+h L x y+h*0.5
```

# step

```
M x y L cx cy L x y+h L x+w-cw y+h L x+w y+h*0.5 L x+w-cw y L x y
```

# annotation

```
M x y+h*0.5 L x+w*0.5 y+h*0.5 L x+w*0.5 y L x+w y M x+w*0.5 y+h*0.5 L x+w*0.5 y+h L x+w y+h
```

# data

```
M x y+h L x+cw*2 y L x+w y L x+w-cw*2 y+h L x y+h
```

# database

```
M x y+h*0.2 A w*0.5 y+h*0.2 0 0 1 x+w y+h*0.2 A w*0.5 y+h*0.2 0 0 1 x y+h*0.2 L x y+h*0.8 A w*0.5 y+h*0.2 0 0 0 x+w y+h*0.8 L x+w y+h*0.2
```

# tape

```
M x cy Q x+w*0.25 y+ch*2 x+w*0.5 cy Q x+w*0.75 y x+w cy L x+w y+h-ch Q x+w*0.75 y+h-ch*2 x+w*0.5 y+h-ch Q x+w*0.25 y+h x y+h-ch L x cy
```

# data_storage

```
M x y A x+w*0.7 cw 0 0 1 x y+h L x+w-cw y+h A x+w*0.7 cw 0 0 0 x+w-cw y L x y
```

# actor

```
M x+w*0.5 y A w*0.25 h*0.125 0 0 1 x+w*0.5 y+h*0.25 M x+w*0.5 y A w*0.25 h*0.125 0 0 0 x+w*0.5 y+h*0.25 L x+w*0.5 y+h*0.7 L x+w y+h M x+w*0.5 y+h*0.7 L x y+h M x y+h*0.35 L x+w y+h*0.35
```

# callout

```
M x y L x+w y L x+w y+h*0.7 L x+w*0.7 y+h*0.7 L cx cy L x+w*0.3 y+h*0.7 L x y+h*0.7 L x y
```

# manual_input

```
M x+w y L x+w y+h L x y+h L x y+ch*1.25 L x+w y
```

# tape_data

```
M x+w*0.5 y A w*0.5 h*0.5 0 0 1 x+w*0.5 y+h L x+w y+h M x+w*0.5 y+h A w*0.5 h*0.5 0 0 1 x+w*0.5 y
```

# loop_limit

```
M x y+h L x+w y+h L x+w y+ch*2 L x+w-cw*2 y L x+cw*2 y L x y+ch*2 L x y+h
```

# off_page_connector

```
M x y L x+w y L x+w cy L x+w*0.5 y+h L x cy L x y
```

# delay

```
M x y L cx y A w-cw h*0.5 0 0 1 cx y+h L x y+h L x y
```

# display

```
M x y+h*0.5 L cx y L x+w*0.8 y A w*0.2 h*0.5 0 0 1 x+w*0.8 y+h L cx y+h L x y+h*0.5
```

# arrow_left

```
M x y+h*0.5 L cx y L cx y+h-ch L x+w y+h-ch L x+w cy L cx cy L cx y+h L x y+h*0.5
```

# double_arrow

```
M x y+h*0.5 L x+w-cw y L x+w-cw cy L cx cy L cx y L x+w y+h*0.5 L cx y+h L cx y+h-ch L x+w-cw y+h-ch L x+w-cw y+h L x y+h*0.5
```

# user

```
M x+w*0.5 y A w*0.25 h*0.2 0 0 1 x+w*0.5 y+h*0.4 C x+w y+h*0.45 x+w y+h*0.5 x+w y+h L x y+h C x y+h*0.5 x y+h*0.45 x+w*0.5 y+h*0.4 A w*0.25 h*0.2 0 0 1 x+w*0.5 y
```

---------------------------

# cross

```
M cx cy L cx y L x+w-cw y L x+w-cw cy L x+w cy L x+w y+h-ch L x+w-cw y+h-ch L x+w-cw y+h L cx y+h L cx y+h-ch L x y+h-ch L x cy L cx cy
```

# corner

```
M x y L x+w y L x+w cy L cx cy L cx y+h L x y+h L x y
```

# tee

```json
{"name": "tee",
  "control_point_num": "1",
  "path": "M x y L x+w y L x+w cy L cx cy L cx y+h L x+w-cw y+h L x+w-cw cy L x cy L x y",
  "controls": [
    {
      "default_position": {
        "default_x": "x+w*0.6",
        "default_y": "y+h*0.2"
      },
      "move_method": "2",
      "move_update": "1",
      "x_range": {
        "min": "x+w*0.5",
        "max": "x+w"
      },
      "y_range": {
        "min": "y",
        "max": "y+h"
      },
    "control_update": ""
    }
  ]
}
```