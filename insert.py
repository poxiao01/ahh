from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from sqlalchemy import delete
from Data.SentenceDataORM import SentenceDataORM
import csv
from sqlalchemy import select
from pathlib import Path
# SQL Server 连接信息
database='Data'  # 输入你的数据库名
server='localhost,1433'  # 输入你的服务器地址和端口，通常默认端口是1433
username='sa'  # 输入你的用户名
password='123456'  # 输入你的密码
driver='ODBC+Driver+17+for+SQL+Server'  # 这是SQL Server驱动
# 创建数据库链接
engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}')

session = Session(engine)

def insert_data(data_list):
    for temp_list in data_list:
        # ... 处理和填充temp_list的逻辑保持不变 ...
        sentece_data = SentenceDataORM()
        sentece_data = sentece_data.create_sentence_data_from_list(temp_list)  # 注意这里直接赋值返回的新实例

        # 添加实例到会话
        session.add(sentece_data)

    # 提交事务以保存所有数据
    try:
        session.commit()
    except Exception as e:
        session.rollback()  # 如果发生错误，回滚事务
        print(temp_list)
        print(f"An error occurred: {e}")
    finally:
        session.close()  # 关闭会话，释放资源


def clear_table():
    """
    清空 SentenceDataORM 对应的数据表。
    """
    # 构造 DELETE 语句
    delete_statement = delete(SentenceDataORM)

    # 执行 DELETE 语句
    try:
        with session.begin():
            session.execute(delete_statement)
            print("表数据已成功清空。")
            session.execute(text("DBCC CHECKIDENT ('SENTENCES_DATA', RESEED, 0);"))
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"清空表数据时发生错误: {e}")
    finally:
        session.close()


def query_and_save_all_to_csv(model, filepath):
    """
    查询表中的全部数据并保存到指定路径的CSV文件中。
    :param model: ORM模型类
    :param filepath: 要保存的CSV文件的完整路径
    """
    try:
        # 构建查询全部数据的表达式
        query = select(model.__table__)

        # 执行查询
        result = session.execute(query)

        # 获取列名
        headers = result.keys()

        # 确保目录存在，如果不存在则创建
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        # 写入CSV文件
        with open(filepath, 'w', newline='', encoding='gbk') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)  # 写入列名

            # 写入数据行
            for row in result.fetchall():
                writer.writerow(row)

        print(f"表中的全部数据已成功保存到 {filepath}")
    except Exception as e:
        print(f"保存数据到CSV文件时发生错误: {e}")
    finally:
        session.close()

# clear_table()


# 直接使用模型类
model = SentenceDataORM

# 指定完整的保存路径
file_path = 'E:/python_stanford_NLP/all_sentence_data.csv'

# 调用函数，指定模型和文件路径
query_and_save_all_to_csv(model, file_path)