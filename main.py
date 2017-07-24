#!/usr/bin/python
# coding:utf-8
import source
import Window
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import benefit

# benefit.sort_benefit()

Window.Window(source.get_origin_selected_codes()).show()
