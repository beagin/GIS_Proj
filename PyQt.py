# -*- coding:utf-8 _*-
"""
@author: tengyuanjian
@file: PyQt.py
@time: 2020/1/9
@contact: yuanjianteng@pku.edu.cn

"""


import sys
from PyQt5.QtWidgets import QApplication
from GIS_Proj.mainWindow import mainWindow
from GIS_Proj.dataOperation import *
from GIS_Proj.PostGISOperation import *


if __name__ == '__main__':
    readShp("data/海南省界/Province_Hainan.shp")
    readTiff("data/DEM数据/Hainan_DEM_100m.tif")
    #testSQL()
    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())