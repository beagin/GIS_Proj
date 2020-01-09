# -*- coding:utf-8 _*-
"""
@author: tengyuanjian
@file: message.py
@time: 2020/1/9
@contact: yuanjianteng@pku.edu.cn

"""


import sys
from PyQt5.QtWidgets import QWidget, QApplication
from GIS_Proj.mainWindow import Example


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())