from driversdict.resource import dictionary
import json
from argparse import ArgumentParser
from hashlib import md5
from pathlib import Path
from subprocess import DEVNULL, PIPE, run
from sys import exit, stderr, stdin
from typing import *
from . import DICTIONARY


def cli_main():
    parser = ArgumentParser("drivers-dict")
    command = parser.add_subparsers(title="subcommands", dest="command")
    sort = command.add_parser("sort", description="排序字典中的密码，会剔除重复项")
    sort.add_argument("-d", "--dictionary", help="指定字典文件", default=DICTIONARY)
    test = command.add_parser("test", description="使用字典中存储的密码逐个尝试解压")
    test.add_argument("archive", help="specific the archive file to extract")
    test.add_argument("-d", "--dictionary", help="指定字典文件", default=DICTIONARY)
    add = command.add_parser("add", description="向字典中添加密码，每行一个，可读取文件或 stdin")
    add.add_argument("-d", "--dictionary", help="指定字典文件", default=DICTIONARY)
    add.add_argument("INPUT",
                     nargs="?",
                     help="输入文件路径，若留空则从 stdin 读取密码",
                     default=None)
    command.add_parser("info", description="查看软件信息")
    args = parser.parse_args()

    if "test" == args.command:
        cli_test(args.archive)
    elif "sort" == args.command:
        cli_sort(args.dictionary)
    elif "add" == args.command:
        cli_add(args.dictionary, args.INPUT)
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


def cli_test(compressed: str):
    """测试解压密码"""
    # 测试 7z 是否存在
    try:
        # todo 用 ctypes 重构
        exe7z = run(["7z", "-version"],
                    stdout=PIPE,
                    stderr=PIPE,
                    encoding="utf-8")
    except FileNotFoundError:
        print(
            "driversdict: error - 7z 不存在，请安装或将可执行文件添加到 PATH： https://www.7-zip.org/"
        )
        exit(-1)

    for n, key in enumerate(dictionary()):
        try:
            result = run(["7z", "t", f"-p{key}", compressed],
                            stdout=DEVNULL,
                            stderr=PIPE,
                            encoding="utf-8")
            print(f"{n}: #{key!r}#")
            if result.returncode == 0:
                print(f"findout: --- #{key!r}# ---")
                break
            else:
                if "Wrong password" in result.stderr:
                    continue
                else:
                    print("driversdict: error - unknown error")
                    print(result.stderr, file=stderr)
                    break
        except Exception as e:
            print(e)
            break
    else:
        print("driversdict: warn - 未找到匹配的密码")

def cli_info():
    """向终端输出程序信息"""
    print("NAME: driversdict")
    print("DESCRIPTION: 查询、测试、记录「某些压缩包」的解压密码")
    print(f"DICTIONARY: {DICTIONARY!r}")