from .resource import pkg_dictionary
from pathlib import Path

def post_install():
    # 获取用户家目录
    home = Path.home()
    # 创建程序数据文件夹
    prog_home = home / ".local" / "share" / "driversdict"
    if not prog_home.exists():
        prog_home.mkdir(parents=True, exist_ok=True)
    # 复制数据
    dictionary_file = prog_home / "dictionary.txt"
    if dictionary_file.exists():
        old = dictionary_file.read_text("utf-8").strip("\n").split("\n")
        new = pkg_dictionary()
        merged = sorted(list(set(old + new)))
    else:
        merged = pkg_dictionary()
    dictionary_file.write_text("\n".join(merged))
    print(f"driversdict: 字典文件位于 {dictionary_file!s}")