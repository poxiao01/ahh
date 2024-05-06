from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from Data.SentenceDataORM import SentenceDataORM

# 引擎创建与Session配置
engine = create_engine('oracle+cx_oracle://C##POXIAO:123456@127.0.0.1:1521/employeeheal')

# 创建一个 Session 类型
Session = sessionmaker(bind=engine)

# 创建 Session 对象
session = Session()

# 创建一个 SentenceDataORM 实例
data = SentenceDataORM(
    SENTENCE='这是第一句子',
    SAME_DEPENDENCY=True,
    DEPENDENCY_PATH='path1',
    SENTENCE_PATTERN='type1',
    SENTENCE_STRUCTURE_WORD='word1',
    SENTENCE_STRUCTURE_WORD_POS='noun',
    QUESTION_WORD='question1',
    QUESTION_WORD_POS='adverb',
    NUMMOD=True,
    OBL_TMOD=False,
)

# 添加数据到会话
session.add(data)

# 提交事务
session.commit()

# 关闭会话
session.close()