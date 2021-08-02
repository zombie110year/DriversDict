import json
from argparse import ArgumentParser
from hashlib import md5
from pathlib import Path
from random import shuffle
from subprocess import PIPE, run
from sys import exit, stdin
from typing import *

from driversdict.resource import dictionary

from . import DICTIONARY
from .testing import parallel_testing, simple_testing


def cli_main():
    parser = ArgumentParser("driversdict")
    command = parser.add_subparsers(title="subcommands", dest="command")
    sort = command.add_parser("sort", description="排序字典中的密码，会剔除重复项")
    test = command.add_parser("test", description="使用字典中存储的密码逐个尝试解压")
    test.add_argument("archive", help="指定要测试的压缩文件")
    test.add_argument("--parallel", help="是否使用多线程", action="store_true")
    add = command.add_parser("add", description="向字典中添加密码，每行一个，可读取文件或 stdin")
    add.add_argument("INPUT",
                     nargs="?",
                     help="输入文件路径，若留空则从 stdin 读取密码",
                     default=None)
    command.add_parser("info", description="查看软件信息")
    args = parser.parse_args()

    if "test" == args.command:
        cli_test(args.archive, args.parallel)
    elif "sort" == args.command:
        cli_sort(DICTIONARY)
    elif "add" == args.command:
        cli_add(DICTIONARY, args.INPUT)
    elif "query" == args.command:
        pass
    elif "info" == args.command:
        cli_info()


def cli_add(dictf: str, input: Optional[str] = None):
    """添加密码，从文件或 stdin 读取
    """
    if input is None:
        src = stdin.read()
    else:
        src = Path(input).read_text("utf-8")
    newpasswords = set([i for i in src.split("\n") if i != ""])
    try:
        oldpasswords = set(dictionary())
    except FileNotFoundError:
        oldpasswords = set()
    passwords = oldpasswords | newpasswords
    actuallyadded = newpasswords - oldpasswords
    sorted_password = [i for i in passwords]
    sorted_password.sort()
    Path(dictf).write_text("\n".join(sorted_password), "utf-8")
    for it in actuallyadded:
        print(f"driversdict: added {it!r}")
    print(f"driversdict: add to {dictf!r}")


def cli_sort(dictf: str):
    """排序去重
    """
    try:
        oldpasswords = set(dictionary())
    except FileNotFoundError:
        print("driversdict: warn - 空字典，跳过")
        return
    newpasswords = sorted(list(oldpasswords))
    Path(dictf).write_text("\n".join(newpasswords), "utf-8")
    print(f"driversdict: sorted {dictf!r}")


# todo API 已变更，找到新的 API
def deprecated_cli_query(filepath: str):
    """向 cjtecc 查询解压密码
    """
    api = "http://app.cjtecc.cn/compress.yun.php"
    content = Path(filepath).read_bytes()
    hashcode = md5(content).hexdigest()
    url = api.format(md5code=hashcode)
    resp = requests.get(url, params={"md5": hashcode})
    if resp.status_code == 200:
        answer = resp.text
        if answer == "no":
            print("没有数据")
        else:
            print(answer)
            obj = json.loads(answer)
            print(f"#{obj['password']}#")
    else:
        raise ValueError(f"无正常响应：{resp.status_code}, {hashcode}")


def cli_test(archivef: str, parallel: bool):
    """测试解压密码"""
    # 测试 7z 是否存在
    try:
        # todo 用 ctypes 重构
        exe7z = run(["7z"],
                    stdout=PIPE,
                    stderr=PIPE,
                    encoding="utf-8")
    except FileNotFoundError:
        print(
            "driversdict: error - 7z 不存在，请安装或将可执行文件添加到 PATH： https://www.7-zip.org/"
        )
        exit(-1)

    passwords = dictionary()
    shuffle(passwords)
    result = parallel_testing(archivef, passwords) if parallel else simple_testing(archivef, passwords)
    if result is not None:
        print(f"findout: --- #{result!r}# ---")
    else:
        print("driversdict: warn - 未找到匹配的密码")


def cli_info():
    """向终端输出程序信息"""
    print("NAME: driversdict")
    print("HOMEPAGE: https://github.com/zombie110year/DriversDict")
    print("DESCRIPTION: 查询、测试、记录「某些压缩包」的解压密码")
    print(f"DICTIONARY: {DICTIONARY!r}")
