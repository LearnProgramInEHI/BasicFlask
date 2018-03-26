#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:

先留着，不用

'''

from wtforms.widgets.core import TextArea,HTMLString,html_params,text_type
try:
    from html import escape
except ImportError:
    from cgi import escape
html="""
<div id="div1" class="toolbar">
    </div>
    <div style="padding: 5px 0; color: #ccc">中间隔离带</div>
    <div id="div2" class="text"> <!--可使用 min-height 实现编辑区域自动增加高度-->
        <p>%s</p>
    </div>
"""

class DivArea(TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        return HTMLString(html%field._value())
