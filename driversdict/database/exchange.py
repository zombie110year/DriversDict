from typing import Dict, List, Optional, Tuple, Union
from .model import QueryJournal, CertainPassword, DB
from datetime import date

def query_passwd(md5sum: bytes) -> List[str]:
    """查询数据库中可能存在的密码，如果没有，则返回空列表
    """
    query = CertainPassword.select(CertainPassword.passwd).where(CertainPassword.md5sum == md5sum)
    passwords = [it.passwd for it in query]
    if passwords:
        now = date.today()
        with DB.atomic():
            action = QueryJournal.insert_many([
                (md5sum, pw, now) for pw in passwords
            ], fields=[QueryJournal.md5sum, QueryJournal.passwd, QueryJournal.date])
            action.execute()
    return passwords


def export_passwd() -> Dict[str, Union[List[str], List[Tuple[bytes, str]]]]:
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
    query = CertainPassword.select(CertainPassword.md5sum, CertainPassword.passwd)
    data = [(it.md5sum, it.passwd) for it in query]
    return {
        "fields": ["md5sum", "passwd"],
        "data": data
    }


def all_passwords() -> List[str]:
    """提取所有密码，以便合并入字典
    """
    query = CertainPassword.select(CertainPassword.passwd)
    passwords = [it.passwd for it in query]
    return passwords