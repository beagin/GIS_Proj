# GIS_Proj

an app for GIS engineering homework.
Version 1: unfinished py version.

## Target
试编写一个小软件工具，实现对5类样例数据实现管理、清洗、分析与可视化：
1. 支持将不同地理投影统一变换至Web墨卡托投影
2. 支持将shp数据导入至postgis数据库管理
3. 统计分析：分别读取postgis和geotiff影像，统计海南各县的平均高程、最大高程、最小高程、平均风速、最大风速、最小风速等统计量，在postgis生成新的统计表
4. 制图功能：多图层叠置并按指定SLD输出地图图片

## Environment
```
Windows 10, i5-8400 CPU @ 2.80 GHz 
python=3.6
PyQt=5.10.1

```

## Questions
* <技术选型>太重要了
    * 语言是否适合进行窗体应用开发
    * 响应速度是否影响用户体验
    * 是否有合适的地理数据处理、地图绘制、数据库处理的相关库
    * 各个模块的组织、镶嵌
    # 尽量提前找到用于进行某些操作的库或项目，不要全部从底层实现
* 部分代码结构还比较丑陋，可以进一步优化