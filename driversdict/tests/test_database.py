import pytest
from ..database.model import CertainPassword, QueryJournal, DB
from peewee import *
from datetime import date


@pytest.fixture
def db():
    DB.connect(False)
    DB.create_tables([CertainPassword, QueryJournal])
    yield
    DB.close()


def test_cp(db):
    data1 = CertainPassword(
        passwd="hello",
        md5sum=b'o\x02\x03N\xb9\x07!\x16Z\x0e\xaa\xad\xe1\xb8\x86g')
    data1.save()
    data2 = CertainPassword(passwd="hello",
                            md5sum=b'\x98\xa2z\x181u\x0f\xbd*<\xc5\x88\xbf*7#')
    data2.save()
    data3 = CertainPassword(
        passwd="goodbye",
        md5sum=b'o\x02\x03N\xb9\x07!\x16Z\x0e\xaa\xad\xe1\xb8\x86g')
    data3.save()

    query1 = CertainPassword.select().where(CertainPassword.passwd == "hello")
    md5sum1 = set([it.md5sum for it in query1])
    assert md5sum1 == {
        b'o\x02\x03N\xb9\x07!\x16Z\x0e\xaa\xad\xe1\xb8\x86g',
        b'\x98\xa2z\x181u\x0f\xbd*<\xc5\x88\xbf*7#'
    }
    query2 = CertainPassword.select().where(
        CertainPassword.md5sum ==
        b'o\x02\x03N\xb9\x07!\x16Z\x0e\xaa\xad\xe1\xb8\x86g')
    md5sum2 = set([it.passwd for it in query2])
    assert md5sum2 == {"hello", "goodbye"}


def test_cp_cn(db):
    data = CertainPassword(passwd="你好",
                           md5sum=b'\x98\xa2z\x181u\x0f\xbd*<\xc5\x88\xbf*7#')
    data.save()

    query = CertainPassword.select().where(
        CertainPassword.md5sum ==
        b'\x98\xa2z\x181u\x0f\xbd*<\xc5\x88\xbf*7#').get()
    assert query.passwd == "你好"


def test_journal(db):
    record = QueryJournal(passwd="你好",
                          md5sum=b'\x98\xa2z\x181u\x0f\xbd*<\xc5\x88\xbf*7#',
                          date=date(1970, 1, 1))
    record.save()

    query = QueryJournal.select().where(
        QueryJournal.md5sum ==
        b'\x98\xa2z\x181u\x0f\xbd*<\xc5\x88\xbf*7#').get()
    assert query.passwd == "你好" and query.date == date(
        1970, 1, 1)