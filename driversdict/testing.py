from typing import Optional
from subprocess import run, DEVNULL, PIPE
from . import shell_encoding
from sys import stderr

def testing_archive(archivef: str, passwd: str) -> Optional[str]:
    """测试一个加密归档的密码，如果正确，返回密码，否则，返回 None

    :param str archivef: 归档文件路径
    :param str passwd: 猜测的密码
    :returns: 如果猜测的密码正确，返回密码，否则，返回 None
    """
    try:
        result = run(["7z", "t", f"-p{passwd}", archivef],
                        stdout=DEVNULL,
                        stderr=PIPE)
        if result.returncode == 0:
            return passwd
        else:
            encoding = shell_encoding()
            err_msg = result.stderr.decode(encoding)
            if "Wrong password" in err_msg:
                pass
            else:
                print("driversdict: error - unknown error")
                print(err_msg, file=stderr)
    except Exception as e:
        print(e, file=stderr)
