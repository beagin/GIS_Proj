# -*- coding:utf-8 _*-
"""
@author: tengyuanjian
@file: dataOperation.py
@time: 2020/1/9
@contact: yuanjianteng@pku.edu.cn

"""

import shapefile
import cv2
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from pyproj import *
import numpy as np


def readShp(filePath : str):
    """
    To read a .shp file and get the data
    :param filePath:
    :return:
    """
    ######################### shapefile库 ######################
    # attrs of shape: 'bbox', 'parts', 'points', 'shapeType', 'shapeTypeName'
    # shapetype: 1-point, 3-polyline, 5-polygon
    shpfile = shapefile.Reader(filePath, encoding='gbk')
    print(shpfile.bbox)
    print(shpfile.__dir__())
    print("successfully read shp")
    shapes = shpfile.shapes()
    print(shpfile.shapes())
    for i in range(len(shapes)):
        print(shapes[i].points)

    p1 = Proj(init="epsg:4326")     # WGS84
    p2 = Proj(init="epsg:3857")     # web墨卡托
    p3 = Proj(init="epsg:9001")     # UTM 50N

    x0 = shapes[0].points[0][0]
    y0 = shapes[0].points[0][1]
    x1, y1 = p2(x0, y0)
    print(x1)
    print(y1)
    x2, y2 = transform(p3, p1, shapes[0].points[0][1], shapes[0].points[0][0], radians=True)
    print(x2)
    print(y2)



    ########################
    gdal.SetConfigOption("SHAPE_ENCODING", "")

    ogr.RegisterAll()
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.Open(filePath)
    layer = ds.GetLayerByIndex(0)

    # layerDefinition = layer.GetLayerDefn()
    # feat = layer.GetNextFeature()
    # while feat:
    #     for i in range(layerDefinition.GetFieldCount()):
    #         fieldName = layerDefinition.GetFieldDefn(i).GetName()
    #         value = feat.GetField(fieldName)
    #         try:
    #             print(fieldName + " : " + str(value))
    #         except Exception as e:
    #             print(e)
    #     feat = layer.GetNextFeature()

    # 投影转换测试
    pro = layer.GetSpatialRef()
    print(pro)
    geosrs = osr.SpatialReference()
    geosrs.SetWellKnownGeogCS("WGS84")
    xy = osr.CoordinateTransformation(pro, geosrs).TransformPoint(x0, y0)
    print(type(xy))
    return shpfile, pro, shpfile.bbox


def readTiff(filePath:str):
    """
    To read a .tif or .tiff file and get the data
    :param filePath:
    :return:
    """
    # try:
    dataset = gdal.Open(filePath)
    if dataset == None:
        print(filePath + "文件无法打开")
        return
    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数
    im_bands = dataset.RasterCount  # 波段数
    im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 获取数据
    im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息
    im_proj = dataset.GetProjection()  # 获取投影信息:6326
    print(im_data.dtype)
    print(im_width)
    print(im_height)
    print(im_bands)
    print(im_proj)
    print(type(im_proj))
    # except Exception as e:
    #     print(e)
    print(im_data[100, 1000])

    # 平均值
    mean = np.average(im_data)
    print(mean)


    return dataset


def dataAnalysis(dataset):
    pass