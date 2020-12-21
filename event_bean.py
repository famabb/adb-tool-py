# !/usr/bin/env python
# -*- codin

class event_bean:
    # 事件类型 0:按键  1：点击  2滑动  3：文本
    event_type: int
    # 事件坐标
    event_pos: []
    # 文本
    text: str
    # 按键
    key_code: int
    # time
    time: int
