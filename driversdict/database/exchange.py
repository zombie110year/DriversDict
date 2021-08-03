from typing import List, Optional
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