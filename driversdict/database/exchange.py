from operator import index
from typing import Dict, List, Optional, Tuple, Union
from .model import QueryJournal, CertainPassword, DB
from datetime import date


def query_passwd(md5sum: bytes) -> List[str]:
    """查询数据库中可能存在的密码，如果没有，则返回空列表
    """
    query = CertainPassword.select(
        CertainPassword.passwd).where(CertainPassword.md5sum == md5sum)
    passwords = [it.passwd for it in query]
    if passwords:
        now = date.today()
        with DB.atomic():
            action = QueryJournal.insert_many([(md5sum, pw, now)
                                               for pw in passwords],
                                              fields=[
                                                  QueryJournal.md5sum,
                                                  QueryJournal.passwd,
                                                  QueryJournal.date
                                              ])
            action.execute()
    return passwords


ExportedPassword = Dict[str, Union[List[str], List[Tuple[bytes, str]]]]


def export_passwd() -> ExportedPassword:
    """将数据库中的密码以 JSON 的形式备份出来

    .. code:: json

        {
            "fields": ["md5sum", "passwd"],
            "data": [
                (b"...", "..."),
                ...
            ]
        }
    """
    query = CertainPassword.select(CertainPassword.md5sum,
                                   CertainPassword.passwd)
    data = [(it.md5sum, it.passwd) for it in query]
    return {"fields": ["md5sum", "passwd"], "data": data}


def all_passwords() -> List[str]:
    """提取所有密码，以便合并入字典
    """
    query = CertainPassword.select(CertainPassword.passwd)
    passwords = [it.passwd for it in query]
    return passwords


def add_passwd_certainly(md5sum: bytes, passwd: str):
    """插入一条确定的密码，成功返回 True，如果已经存在，则不会插入并返回 False
    """
    _, created = CertainPassword.get_or_create(md5sum=md5sum, passwd=passwd)
    return created


def import_passwords(json: ExportedPassword):
    """向数据库中导入，传输格式与导出功能相同

    :returns: 实际插入的条数
    """
    fields, data = json["fields"], json["data"]
    passwords = [it[fields.index("passwd")] for it in data]
    md5sums = [it[fields.index("md5sum")] for it in data]
    data_ = set(zip(md5sums, passwords))
    existed = set([(it.md5sum, it.passwd) for it in CertainPassword.select()])
    new = data_ - existed
    with DB.atomic() as txn:
        CertainPassword.insert_many(
            new, fields=[CertainPassword.md5sum,
                         CertainPassword.passwd]).execute()
        txn.commit()
    return len(new)


def deduplicate_passwords():
    """去除数据库中的重复密码。

    重复：md5sum 和 passwd 都相同
    """
    raise NotImplementedError