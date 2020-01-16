# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 9:36
# @Author  : llc
# @File    : standalone.py

import os, sys
from qgis.core import QgsProject, QgsApplication, QgsVectorLayer
from qgis.gui import QgsMapCanvas, QgsMapToolPan, QgsMapToolZoom, QgsMapToolIdentify
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QFileDialog
from ui.main_ui import Ui_MainWindow


class MapExplorer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MapExplorer, self).__init__()
        self.setupUi(self)

        self.init_mapcanvas()
        self.slot_connect()

    def slot_connect(self):
        self.action_open.triggered.connect(self.action_open_triggered)
        self.action_basemap.triggered.connect(self.action_basemap_triggered)
        self.action_mark.triggered.connect(self.action_mark_triggered)
        self.action_zoomin.triggered.connect(self.action_zoomin_triggered)
        self.action_zoomout.triggered.connect(self.action_zoomout_triggered)
        self.action_pan.triggered.connect(self.action_pan_triggered)
        self.action_identify.triggered.connect(self.action_identify_triggered)

    def init_mapcanvas(self):
        self.mapCanvas = QgsMapCanvas()
        self.mapCanvas.xyCoordinates.connect(self.show_lonlat)
        self.mapCanvas.setCanvasColor(Qt.white)
        # self.mapCanvas.show()
        layout = QVBoxLayout(self.centralwidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.mapCanvas)

    def loadMap(self, fullpath):
        print(fullpath)
        self.layer = QgsVectorLayer(fullpath, "shp", "ogr")
        QgsProject.instance().addMapLayer(self.layer)
        self.mapCanvas.setLayers([self.layer])
        self.mapCanvas.setExtent(self.layer.extent())
        self.mapCanvas.refresh()

    def action_open_triggered(self):
        fullpath, format = QFileDialog.getOpenFileName(self, '打开数据', '', '*.shp')
        if os.path.exists(fullpath):
            self.loadMap(fullpath)

    def action_basemap_triggered(self):
        pass

    def action_mark_triggered(self):
        pass

    def action_zoomin_triggered(self):
        self.maptool = QgsMapToolZoom(self.mapCanvas, False)
        self.mapCanvas.setMapTool(self.maptool)

    def action_zoomout_triggered(self):
        self.maptool = QgsMapToolZoom(self.mapCanvas, True)
        self.mapCanvas.setMapTool(self.maptool)

    def action_pan_triggered(self):
        self.maptool = QgsMapToolPan(self.mapCanvas)
        self.mapCanvas.setMapTool(self.maptool)

    def action_identify_triggered(self):
        self.maptool = QgsMapToolIdentify(self.mapCanvas)
        self.mapCanvas.setMapTool(self.maptool)

    def show_lonlat(self, point):
        x = point.x()
        y = point.y()
        self.statusbar.showMessage(f'经度:{x},纬度:{y}')


def main():
    qgs = QgsApplication([], True)
    qgs.setPrefixPath('qgis', True)
    qgs.initQgis()

    window = MapExplorer()
    window.show()

    exit_code = qgs.exec_()
    qgs.exitQgis()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()