from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SentenceDataORM(Base):
    __tablename__ = 'SENTENCES_DATA'

    # 主键ID，自动递增
    ID = Column(Integer, primary_key=True, autoincrement=True)

    # 句子内容
    SENTENCE = Column(String(128))

    # 相同依存关系计数
    SAME_DEPENDENCY = Column(Integer)

    # 依存路径
    DEPENDENCY_PATH = Column(String(128))

    # 短语类型
    PHRASE_TYPE = Column(String(32))

    # 短语词汇
    PHRASE_WORD = Column(String(32))

    # 短语词汇词性
    PHRASE_WORD_POS = Column(String(32))

    # 问题词汇
    QUESTION_WORD = Column(String(32))

    # 问题词汇词性
    QUESTION_WORD_POS = Column(String(32))

    # 数量修饰词
    NUMMOD = Column(Integer)

    # obl:tmod相关字段
    OBL_TMOD = Column(Integer)

    # advcl相关字段
    ADVCL = Column(Integer)

    # obl:agent相关字段
    OBL_AGENT = Column(Integer)

    # 并列连词
    CONJ = Column(Integer)

    # obl相关字段
    OBL = Column(Integer)

    # 并列连词
    CC = Column(Integer)

    # obl:npmod相关字段
    OBL_NPMOD = Column(Integer)

    # cc:preconj相关字段
    CC_PRECONJ = Column(Integer)

    # 系动词
    COP = Column(Integer)

    # nmod:poss相关字段
    NMOD_POSSESS = Column(Integer)

    # 标点符号
    PUNCT = Column(Integer)

    # xcomp相关字段
    XCOMP = Column(Integer)

    # 空语类
    EXPL = Column(Integer)

    # 助动词
    AUX = Column(Integer)

    # 宾语
    OBJ = Column(Integer)

    # 属性补语
    ACL = Column(Integer)

    # 结果补语
    CCOMP = Column(Integer)

    # 定语从句关系词
    ACL_RELCL = Column(Integer)

    # 依赖关系
    DEP = Column(Integer)

    # 同位关系
    APPOS = Column(Integer)

    # 被动主语
    NSUBJ_PASS = Column(Integer)

    # 平坦结构
    FLAT = Column(Integer)

    # 格标记
    CASE = Column(Integer)

    # 形容词修饰名词
    AMOD = Column(Integer)

    # 根节点
    ROOT = Column(Integer)

    # nmod:npmod相关字段
    NMOD_NPMOD = Column(Integer)

    # 被动态助动词
    AUX_PASS = Column(Integer)

    # 标记
    MARK = Column(Integer)

    # advcl:relcl相关字段
    ADVCL_RELCL = Column(Integer)

    # 副词修饰语
    ADVMOD = Column(Integer)

    # nmod相关字段
    NMOD = Column(Integer)

    # 间接宾语
    IOBJ = Column(Integer)

    # det:predet相关字段
    DET_PREDET = Column(Integer)

    # 固定表达
    FIXED = Column(Integer)

    # 决定词
    DET = Column(Integer)

    # 合成词
    COMPOUND = Column(Integer)

    # 主语
    NSUBJ = Column(Integer)