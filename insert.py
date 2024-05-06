from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from Data.SentenceDataORM import SentenceDataORM

Base = declarative_base()
engine = create_engine('oracle+cx_oracle://C##POXIAO:123456@127.0.0.1:1521/employeeheal')
# Base.metadata.create_all(engine)  # 根据模型创建表结构，仅首次运行或表结构变化时需要

Session = sessionmaker(bind=engine)
session = Session()


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