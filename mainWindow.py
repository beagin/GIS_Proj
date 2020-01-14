# -*- coding:utf-8 _*-
"""
@author: tengyuanjian
@file: mainWindow.py
@create time: 2020/1/9
@contact: yuanjianteng@pku.edu.cn

"""

from PyQt5.QtWidgets import QPushButton, QInputDialog, QMainWindow, QAction, QFileDialog, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QLabel, QDialog, QVBoxLayout
from PyQt5.QtGui import QPainter, QPen, QBrush, QImage, QPixmap, QPolygonF
from PyQt5.QtCore import Qt, QRect, QPointF
import cv2
from GIS_Proj.dataOperation import *
from GIS_Proj.PostGISOperation import *
from osgeo import osr


class Layer():
    def __init__(self, file, type:str, name:str, proj):
        self.file = file        # shpfile对象
        self.type = type
        self.name = name
        self.proj = proj
        self.visible = True


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        # 存储图层信息的列表
        self.layers = []
        # 当前投影方式
        self.proj = osr.SpatialReference()
        self.proj.SetWellKnownGeogCS("WGS84")
        # 图像范围信息
        self.minX = 20
        self.minY = 40
        self.RectWidth = 800
        self.RectHeight = 800
        # 坐标bbox信息
        # 海南省/县界bbox：[388285.0499364063, 1876707.7161650453, 667828.1476304457, 2099819.7981660534]
        # 台风轨迹：[102.4, 12.5, 141.5, 19.7]
        self.minLon = 388285
        self.minLat = 1876707
        self.maxLon = 667828
        self.maxLat = 2099819
        # 比例尺倒数
        self.scale = 375
        # 是否需要更新
        self.needRefresh = False
        # 窗体初始化
        self.InitUI()

    def InitUI(self):
        """
        Initialize the window
        :return:
        """
        self.resize(1100, 900)

        # 菜单栏
        menuBar = self.menuBar()
        # >文件
        menu_file = menuBar.addMenu("文件")
        # >文件>打开...
        act_openFile =      QAction("打开...", self)
        act_openFile.setShortcut("Ctrl+O")
        act_openFile.setStatusTip("打开文件")
        act_openFile.triggered.connect(self.openFileDialog)
        menu_file.addAction(act_openFile)
        # >文件>导出...
        act_exportFile =    QAction("导出...", self)
        act_exportFile.setShortcut("Ctrl+E")
        act_exportFile.setStatusTip("导出图像为...")
        menu_file.addAction(act_exportFile)
        # >投影
        menu_proj = menuBar.addMenu("投影")
        # >投影>查看投影
        act_currentProj =   QAction("查看投影", self)
        act_currentProj.setShortcut("Ctrl+P")
        act_currentProj.setStatusTip("查看当前地图的投影信息")
        act_currentProj.triggered.connect(self.projDialog)
        menu_proj.addAction(act_currentProj)
        # >投影>投影转换
        act_transformProj = QAction("投影转换...", self)
        act_transformProj.setShortcut("Ctrl+T")
        act_transformProj.setStatusTip("将当前地图转换至另一投影")
        act_transformProj.triggered.connect(self.transformDialog)
        menu_proj.addAction(act_transformProj)
        # >数据库
        menu_database = menuBar.addMenu("数据库")
        # >数据库>连接数据库
        act_connect =       QAction("连接数据库", self)
        act_connect.setShortcut("Ctrl+C")
        menu_database.addAction(act_connect)
        # >数据库>加载shp数据
        act_loadDatabase =  QAction("加载数据库数据", self)
        act_loadDatabase.setShortcut("Ctrl+L")
        menu_database.addAction(act_loadDatabase)
        # >数据库>

        # >帮助
        menu_help = menuBar.addMenu("帮助")
        # >帮助>关于
        act_about =         QAction("关于", self)
        act_about.setShortcut("Ctrl+A")
        menu_help.addAction(act_about)
        # 状态栏
        self.status = self.statusBar()
        self.status.showMessage('这是状态栏提示', 4000)

        # 显示图片的标签
        self.label = QLabel()
        self.label.setGeometry(self.minX, self.minY, self.RectWidth, self.RectHeight)

        # 按钮
        self.btn = QPushButton("Dialog", self)
        self.btn.move(101, 210)
        self.btn.clicked.connect(self.ShowDialog)

        self.setWindowTitle("mainWindow")
        self.show()

    ############################################# 菜单栏 ################################################
    ###################### 文件
    # 打开...
    def openFileDialog(self):
        # 打开文件的对话框，限制文件类型
        fileName = QFileDialog.getOpenFileName(self, '打开文件', '/', "shapefile(*.shp);;image(*.tif *.tiff)")
        if fileName[0]:
            print(fileName)
            # tiff文件
            if "tif" in fileName[0].split('.')[-1]:
                print("open tiff file: " + fileName[0])
                tifData = readTiff(fileName[0])
                if len(self.layers) == 1:
                    self.proj = tifData.GetProjection()
                newLayer = Layer(tifData, "tiff", fileName[0].split('/')[-1][:-4], tifData.GetProjection())
                self.layers.append(newLayer)
                print("done read tif")
                self.addImage(len(self.layers)-1)   # 显示图像
                self.needRefresh = True
            # shp文件
            elif fileName[0].split('.')[-1] == "shp":
                print("is shp file: " + fileName[0])
                # 读取shp文件信息
                shpfile, proj, bbox = readShp(fileName[0])
                # 如果是第一个图层则修改地图投影方式
                if len(self.layers) == 0:
                    self.proj = proj
                # 添加图层至地图
                newLayer = Layer(shpfile, "shp", fileName[0].split('/')[-1][:-4], proj)
                self.layers.append(newLayer)
                # 更新地图bbox及比例尺
                self.minLon = min(bbox[0], self.minLon)
                self.minLat = min(bbox[1], self.minLat)
                self.maxLon = max(bbox[2], self.maxLon)
                self.maxLat = max(bbox[3], self.maxLat)
                self.scale = max((self.maxLon-self.minLon)/800, (self.maxLat-self.minLat)/800) * 1.1
                # 地图需重新绘制
                self.needRefresh = True

        # TODO
        # 修改bbox信息——tif

    # 导出...
    # TODO

    ###################### 投影
    # 查看投影
    def projDialog(self):
        # 新建对话框
        self.dialog = QDialog()
        self.dialog.resize(400, 300)
        # 标签
        label = QLabel()
        print(self.proj)
        label.setText(str(self.proj))
        # 按钮
        okBtn = QPushButton("确定")
        okBtn.move(200, 250)
        okBtn.clicked.connect(self.ok)
        # 标签与按钮进行布局
        vbox = QVBoxLayout()    # 纵向布局
        vbox.addWidget(label)
        vbox.addWidget(okBtn)
        self.dialog.setLayout(vbox)
        self.dialog.setWindowTitle("地图投影信息")                   # 窗口标题
        self.dialog.setWindowModality(Qt.ApplicationModal)          # 对话框模式：用户只有关闭弹窗后，才能关闭主界面
        self.dialog.exec_()

    def ok(self):
        print("结束查看")
        self.needRefresh = True
        self.dialog.close()

    # 投影转换
    def transformDialog(self):
        geosrs = osr.SpatialReference()
        geosrs.ImportFromEPSG(3857)
        self.transformProj(geosrs)

    def transformProj(self, newProj):
        """
        对所有图层进行投影变换
        :param newProj: 一个osr.SpatialReference()对象，即进行变换后的投影方式
        :return:
        """
        # 对每个图层进行变换
        print(self.proj, newProj)
        for i in range(len(self.layers)):
            if self.layers[i].type == "shp":
                for j in range(len(self.layers[i].file.shapes())):
                    shape = self.layers[i].file.shapes()[j]
                    newPoints = []
                    for k in range(len(shape.points)):
                        # 修改每个点
                        point = shape.points[k]
                        xy = osr.CoordinateTransformation(self.proj, newProj).TransformPoint(point[0], point[1])
                        # print(point, xy[:-1])
                        print("here")
                        newPoints.append(xy[:-1])
                    #### BIG QUESTION: 不能修改shapefile对象里的坐标信息
                    self.layers[i].file.shapes()[j].points.clear()
                    self.layers[i].file.shapes()[j].points = newPoints
                    print(newPoints[0])
                    print(self.layers[i].file.shapes()[j].points[0])
                print("done transform layer " + str(i))

        # 变换之后，修改bbox信息
        print(self.minLon, self.maxLon, self.minLat, self.maxLat)
        print(self.scale)
        self.minLon = min([layer.file.bbox[0] for layer in self.layers])
        self.minLat = min([layer.file.bbox[1] for layer in self.layers])
        self.maxLon = max([layer.file.bbox[2] for layer in self.layers])
        self.maxLat = max([layer.file.bbox[3] for layer in self.layers])
        self.scale = max((self.maxLon - self.minLon) / 800, (self.maxLat - self.minLat) / 800) * 1.1
        print(self.minLon, self.maxLon, self.minLat, self.maxLat)
        print(self.scale)
        # 转换后重新绘制
        self.needRefresh = True

    def paintEvent(self, *args, **kwargs):
        painter = QPainter()
        painter.begin(self)
        # 绘制地图框
        self.drawRect(painter)
        # 绘制每个图层
        if len(self.layers) > 0 and self.needRefresh:
            for i in range(len(self.layers)):
                print("call drawLayer")
                if self.layers[i].type == "shp":
                    self.drawLayer(i, painter)
            self.needRefresh = False
        painter.end()

    def addImage(self, layerIndex):
        """

        :param layerIndex:
        :return:
        """
        layer = self.layers[layerIndex]
        # 加载图片
        data = layer.ReadAsArray(0, 0, layer.RasterXSize, layer.RasterYSize)
        img = QImage(data, layer.RasterXSize, layer.RasterYSize, QImage.Format_Grayscale8)
        print("loading image")
        #img.scaled(self.RectWidth, self.RectHeight, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        pix = QPixmap.fromImage(img)
        self.label.setPixmap(pix)

        # self.item = QGraphicsPixmapItem(pix)    # 图元
        # self.scene = QGraphicsScene()           # 场景
        # self.scene.addItem(self.item)           # 图元添加至场景
        # self.graphicsView = QGraphicsView()     # 视图
        # self.graphicsView.setGeometry(QRect(self.minX, self.minY, self.RectWidth, self.RectHeight))
        # self.graphicsView.setScene(self.scene)  # 场景添加至视图
        print("done tiff display")

    def drawRect(self, painter):
        # 绘制画布区域
        # 填充白色，边界黑色
        brush = QBrush(Qt.white, Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawRect(self.minX, self.minY, self.RectWidth, self.RectHeight)

    def drawLayer(self, layerIndex, painter):
        """
        绘制一个图层
        :param layerIndex:
        :param painter:
        :return:
        """
        print("start draw")
        layer = self.layers[layerIndex]
        if layer.type == "tiff":
            pass

        elif layer.type == "shp":
            # 显示shp图像
            shapetype = layer.file.shapes()[0].shapeType
            if shapetype == 1:
                # 点
                print("display points")
            elif shapetype == 5:
                # 多边形
                pen = QPen(Qt.darkBlue, 1, Qt.SolidLine)
                painter.setPen(pen)
                print("display polygon")
                for shape in layer.file.shapes():
                    partCount = 1
                    points = []
                    for i in range(len(shape.points)):
                        # 进入下一个part (polygon)
                        if partCount < len(shape.parts) and i == shape.parts[partCount]:
                            polygon = QPolygonF(points)
                            painter.drawPolygon(polygon)
                            points = []
                            partCount += 1
                        x, y = self.cal_screenXY(shape.points[i][0], shape.points[i][1])
                        points.append(QPointF(x, y))
                    # 绘制最后一个多边形
                    polygon = QPolygonF(points)
                    painter.drawPolygon(polygon)
                    print("draw a polygon")

    def ShowDialog(self):
        text, ok = QInputDialog.getText(self, "Input Dialog", "Enter your name:")
        if ok:
            pass

    def cal_screenXY(self, mapX:float, mapY:float):
        """
        地图坐标(Lon, Lat)-->屏幕坐标(x, y)
        :return:
        """
        screenX = self.minX + (mapX-self.minLon+0.05*(self.maxLon-self.minLon)) / self.scale
        screenY = self.minY + self.RectHeight + (self.minLat-0.05*(self.maxLat-self.minLat)-mapY) / self.scale
        return screenX, screenY

    def testPen(self, painter):
        pen = QPen(Qt.darkCyan, 2, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(self.minX, self.minY, self.minX+100, self.minY+100)
