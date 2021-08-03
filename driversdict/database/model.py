"""
1. 表1 - 密码对照表
2. 文本文件 - 字典，无对照
3. 表2 - 解码统计
"""

from peewee import *
from ..resource import database_file

import os

__all__ = ["CertainPassword", "QueryJournal", "DB"]

# TESTING = True if os.getenv("TESTING") else False
TESTING = False

if not TESTING:
    DB = SqliteDatabase(database_file())
else:
    print("TESTING MODE")
    DB = SqliteDatabase(":memory:")


class CertainPassword(Model):
    "能直接通过 MD5 查询的密码"
    # 自动生成 id = AutoField()
    passwd = TextField()
    md5sum = BlobField()

    class Meta:
        database = DB


# UncertainPassword 就是字典中的密码


class QueryJournal(Model):
    "查询日志"

    md5sum = BlobField()
    passwd = TextField()
    date = DateField()

    class Meta:
        database = DB