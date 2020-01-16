import shapefile


def readShp(filePath:str):
    """
    To
    :param filePath:
    :return:
    """
    sf = shapefile.Reader(filePath)
    