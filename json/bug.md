# 前端
- 关键点重合之后点击不到了

# 脚本
- move_update设置
- 关键点颜色

# big_arrow_left

- 关键点颜色
- 左关键点跟随矩形移动时，位置改变（不在中间位置了）
 
  需要改成保持比例

# circle

- 点移动规则

# manual_input

- 关键点位置偏移，横向拉伸时关键点不等比例右移

# cross/corner/callout

- 变成线后不能移动了
- 爆栈

# callout

- 控制点矩形从动坐标，点可能会进到里面出不来

# card

- 控制点移动坐标异常

# data

- 矩形向上移动到h为0时超出访问边界

# data_storage

- 位置影响图形；关键点有问题

# delay/display/document/double_arrow

- 矩形移动到w或h为0时错误

# loop_limit

- 关键点不能移动

# step 
- 关键点绝对距离问题
- 无边界问题

# tape/tee

# process 

- 不能动控制点

# roundedRect

反转时控制点出界


# new

## loop_limit

控制点不能操控

## tape_data

显示问题

## tee

控制点移动方向


# 6.3

## circle

- 上右点移动
- 角点在非可变化方向移动时矩形变化

## cross

- 控制点最大范围

## double arrow/tee

- 调整关键点位置（应该位于左半侧）

## rounded rect

- 控制点出界

## collate
- 卡顿？

# 组件不闭合

- cylinder
- actor