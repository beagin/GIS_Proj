# -*- coding:utf-8 _*-
"""
@author: tengyuanjian
@file: PostGISOperation.py
@time: 2020/1/10
@contact: yuanjianteng@pku.edu.cn

"""

import psycopg2
from postgis.psycopg import register


def testSQL():
    conn = psycopg2.connect(database="postgis_25_zhd", user="postgres", password="658400", host="10.128.201.34", port="5432")
    register(conn)
    cursor = conn.cursor()
    #cursor.execute('CREATE TABLE IF NOT EXISTS mytable ("geom" geometry(LineString) NOT NULL)')
    cursor.execute("show tables")
    results = cursor.fetchall()
    for result in results:
        print(result)
    conn.commit()

