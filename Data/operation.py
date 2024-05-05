from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from Data.SentenceDataORM import SentenceDataORM

# 引擎创建与Session配置
engine = create_engine('oracle+cx_oracle://C##POXIAO:123456@127.0.0.1:1521/employeeheal')
Session = sessionmaker(bind=engine)
session = Session()

# 创建SentenceDataORM实例
new_data = SentenceDataORM(
    SENTENCE="这是一个示例句子。",
    SAME_DEPENDENCY=0,
    DEPENDENCY_PATH="示例路径",
    PHRASE_TYPE="示例短语类型",
    # ... 为其他字段填写相应的值
    NSUBJ="示例主语"
)

# 将实例添加到Session
session.add(new_data)

# 提交事务以保存数据到数据库
try:
    session.commit()
    print("数据插入成功！")
except Exception as e:
    # 如果出现异常，回滚事务
    session.rollback()
    print(f"数据插入失败: {e}")

# 最后别忘了关闭Session
session.close()