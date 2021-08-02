# 司机字典

本工具用于提升你的「解压」体验。

当你下载了一个加密的压缩文件，里面存放了你需要的配菜，但是却不知道如何解压时可以尝试使用此工具。

## 安装

需要先安装 Python 3.9 和 7-zip，并将 `7z.exe` 可执行文件所在目录添加进 `PATH` 环境变量中。

```sh
pip install driversdict
# 或者
pipx install driversdict
```

## 使用

1. 添加一个或多个密码，使用 `add` 指令。

```sh
# 不提供文件路径时，将从 stdin 读取，每行一个
driversdict add
# 从文本文件中添加密码，每行一个，使用 UTF-8 字符编码
driversdict add passwords.txt
```

2. 使用字典中的密码测试加密压缩文件，用 `test` 指令。如果压缩文件没有加密，那么程序会将字典中的第一个密码当作答案显示出来，请忽略。

```sh
driversdict test 含密码的压缩文件.7z
```

3. 如果使用其他编辑器修改了字典，想要对字典进行排序和去重，使用 `sort` 指令。

```sh
driversdict sort
```

4. 显示应用程序的信息

```sh
driversdict info

#>
NAME: driversdict
DESCRIPTION: 查询、测试、记录「某些压缩包」的解压密码
DICTIONARY: 'C:/Users/zom/.local/share/driversdict/dictionary.txt'
```