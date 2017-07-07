#!/usr/bin/python
#coding:utf-8
import source
import Window
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

Window.Window(source.get_selected_codes()).show()
