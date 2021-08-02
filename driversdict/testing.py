import threading as t
from collections import namedtuple
from queue import Empty, Queue
from subprocess import DEVNULL, PIPE, run
from sys import stderr
from typing import List, Optional

from . import shell_encoding

__all__ = ["parallel_testing", "simple_testing", "testing_archive"]

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

Task = namedtuple("Task", ["archivef", "password"])

class Testor(t.Thread):
    def __init__(self, name: str, tasks: "Queue[Task]", results: "Queue[Optional[str]]"):
        super().__init__(name=name, daemon=True)
        self.name = name
        self.tasks = tasks
        self.results = results
        self.__terminated = False

    def run(self):
        while not self.__terminated:
            try:
                task = self.tasks.get(False)
            except Empty:
                print(f"{self.name}: tasks empty, stopped.", file=stderr)
                break
            archivef, password = task
            # print(f"{self.name}: testing #{password!r}#", file=stderr)
            result = testing_archive(archivef, password)
            self.results.put(result, True, 60)

    def terminate(self):
        self.__terminated = True

class Manager:
    def __init__(self, name: str, tasks: "Queue[Task]", results: "Queue[Optional[str]]", workers: List[Testor], init_passwords: List[str], archivef: str):
        self.name = name
        self.tasks = tasks
        self.results = results
        self.archivef = archivef
        self.workers = workers

        for it in init_passwords:
            self.tasks.put_nowait((archivef, it))

    def run(self):
        while True:
            try:
                result = self.results.get(True, 60)
            except Empty:
                return
            if result is not None:
                for w in self.workers:
                    w.terminate()
                return result

def parallel_testing(archivef: str, passwords: List[str]):
    """使用多线程，并行地测试压缩包密码
    """
    tasks = Queue()
    results = Queue()

    workers = [Testor(name=f"testor-{n}", tasks=tasks, results=results) for n in range(4)]
    manager = Manager(name="manager", tasks=tasks, results=results, workers=workers, init_passwords=passwords, archivef=archivef)

    for worker in workers:
        worker.start()

    # block until complete
    result = manager.run()

    for worker in workers:
        if worker.is_alive():
            worker.join()

    return result

def simple_testing(archivef: str, passwords: List[str]):
    "单线程测试"
    for password in passwords:
        result = testing_archive(archivef, password)
        if result is not None:
            return result
