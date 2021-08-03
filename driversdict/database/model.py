"""
1. 表1 - 密码对照表
2. 文本文件 - 字典，无对照
3. 表2 - 解码统计
"""

from peewee import *

__all__ = ["CertainPassword", "QueryJournal", "DB"]


DB = DatabaseProxy()

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