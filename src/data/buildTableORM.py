import os
import subprocess
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from pathlib import Path

# SQL Server 连接信息
database = 'Data'  # 输入你的数据库名
server = 'localhost,1433'  # 输入你的服务器地址和端口，通常默认端口是1433
username = 'sa'  # 输入你的用户名
password = '123456'  # 输入你的密码
driver = 'ODBC+Driver+17+for+SQL+Server'  # 这是SQL Server驱动


# 创建数据库链接
engine: Engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}')

# 定义输出文件名
output_file_path = Path("E:/python_stanford_NLP/src/data/models.py")

# 从engine获取连接字符串并构造sqlacodegen命令
connection_str = str(engine.url)
subprocess_cmd = ["sqlacodegen", connection_str, "--outfile", str(output_file_path)]

# 执行sqlacodegen命令
try:
    subprocess.run(subprocess_cmd, check=True)
    print(f"ORM类已成功生成至: {output_file_path}")
except subprocess.CalledProcessError as e:
    print(f"执行sqlacodegen时发生错误: {e}")
