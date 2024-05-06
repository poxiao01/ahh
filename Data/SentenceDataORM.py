import json

from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class SentenceDataORM(Base):
    __tablename__ = 'SENTENCES_DATA'

    ID = Column(Integer, primary_key=True)
    SENTENCE = Column(String(128))
    SAME_DEPENDENCY = Column(Boolean)
    DEPENDENCY_PATH = Column(String(128))
    SENTENCE_PATTERN = Column(String(32))
    SENTENCE_STRUCTURE_WORD = Column(String(32))
    SENTENCE_STRUCTURE_WORD_POS = Column(String(32))
    QUESTION_WORD_POS = Column(String(32))
    NUMMOD = Column(Boolean)
    OBL_TMOD = Column(Boolean)
    ADVCL = Column(Boolean)
    OBL_AGENT = Column(Boolean)
    CONJ = Column(Boolean)
    OBL = Column(Boolean)
    CC = Column(Boolean)
    OBL_NPMOD = Column(Boolean)
    CC_PRECONJ = Column(Boolean)
    COP = Column(Boolean)
    NMOD_POSSESS = Column(Boolean)
    PUNCT = Column(Boolean)
    XCOMP = Column(Boolean)
    EXPL = Column(Boolean)
    AUX = Column(Boolean)
    OBJ = Column(Boolean)
    ACL = Column(Boolean)
    CCOMP = Column(Boolean)
    ACL_RELCL = Column(Boolean)
    DEP = Column(Boolean)
    APPOS = Column(Boolean)
    NSUBJ_PASS = Column(Boolean)
    FLAT = Column(Boolean)
    CASE = Column(Boolean)
    AMOD = Column(Boolean)
    ROOT = Column(Boolean)
    NMOD_NPMOD = Column(Boolean)
    AUX_PASS = Column(Boolean)
    MARK = Column(Boolean)
    ADVCL_RELCL = Column(Boolean)
    ADVMOD = Column(Boolean)
    NMOD = Column(Boolean)
    IOBJ = Column(Boolean)
    DET_PREDET = Column(Boolean)
    FIXED = Column(Boolean)
    DET = Column(Boolean)
    COMPOUND = Column(Boolean)
    NSUBJ = Column(Boolean)

    def create_sentence_data_from_list(self, temp_list):
        """
        根据temp_list中的数据创建SentenceDataORM实例。
        假设temp_list的元素顺序与SentenceDataORM的字段顺序一致。
        """
        field_names = [
            'SENTENCE',  # 句子
            'SAME_DEPENDENCY',  # 是否同依赖
            'DEPENDENCY_PATH',  # 依赖路径
            'SENTENCE_PATTERN',  # 句子类型(疑问句 or 陈述句)
            'SENTENCE_STRUCTURE_WORD',  # 句型词（此字段之前遗漏，现已加入）
            'SENTENCE_STRUCTURE_WORD_POS',  # 句型词词性
            'QUESTION_WORD_POS',  # 疑问词词性
            'NUMMOD', 'OBL_TMOD', 'ADVCL', 'OBL_AGENT', 'CONJ', 'OBL', 'CC',
            'OBL_NPMOD', 'CC_PRECONJ', 'COP', 'NMOD_POSSESS', 'PUNCT', 'XCOMP',
            'EXPL', 'AUX', 'OBJ', 'ACL', 'CCOMP', 'ACL_RELCL', 'DEP', 'APPOS',
            'NSUBJ_PASS', 'FLAT', 'CASE', 'AMOD', 'ROOT', 'NMOD_NPMOD', 'AUX_PASS',
            'MARK', 'ADVCL_RELCL', 'ADVMOD', 'NMOD', 'IOBJ', 'DET_PREDET', 'FIXED',
            'DET', 'COMPOUND', 'NSUBJ'  # 所有依赖关系
        ]

        # 确保temp_list的长度与field_names匹配
        assert len(temp_list) == len(field_names), "temp_list的长度与字段数量不匹配"

        dependency_path = temp_list[2]  # 第三个元素是依赖路径列表
        if isinstance(dependency_path, list):
            temp_list[2] = json.dumps(dependency_path, ensure_ascii=False)  # 转换列表为JSON字符串

        # 使用zip函数将字段名与值配对，然后转换为字典
        data_dict = dict(zip(field_names, temp_list))

        # 使用字典解包创建SentenceDataORM实例
        return SentenceDataORM(**data_dict)

    # CREATE
    # TABLE
    # SENTENCES_DATA(
    #     ID
    # NUMBER
    # GENERATED
    # BY
    # DEFAULT
    # ON
    # NULL
    # AS
    # IDENTITY
    # PRIMARY
    # KEY,
    # SENTENCE
    # VARCHAR2(128),
    # SAME_DEPENDENCY
    # NUMBER(1),
    # DEPENDENCY_PATH
    # VARCHAR2(128),
    # SENTENCE_PATTERN
    # VARCHAR2(32),
    # SENTENCE_STRUCTURE_WORD
    # VARCHAR2(32),
    # SENTENCE_STRUCTURE_WORD_POS
    # VARCHAR2(32),
    # QUESTION_WORD_POS
    # VARCHAR2(32),
    # NUMMOD
    # NUMBER(1),
    # OBL_TMOD
    # NUMBER(1),
    # ADVCL
    # NUMBER(1),
    # OBL_AGENT
    # NUMBER(1),
    # CONJ
    # NUMBER(1),
    # OBL
    # NUMBER(1),
    # CC
    # NUMBER(1),
    # OBL_NPMOD
    # NUMBER(1),
    # CC_PRECONJ
    # NUMBER(1),
    # COP
    # NUMBER(1),
    # NMOD_POSSESS
    # NUMBER(1),
    # PUNCT
    # NUMBER(1),
    # XCOMP
    # NUMBER(1),
    # EXPL
    # NUMBER(1),
    # AUX
    # NUMBER(1),
    # OBJ
    # NUMBER(1),
    # ACL
    # NUMBER(1),
    # CCOMP
    # NUMBER(1),
    # ACL_RELCL
    # NUMBER(1),
    # DEP
    # NUMBER(1),
    # APPOS
    # NUMBER(1),
    # NSUBJ_PASS
    # NUMBER(1),
    # FLAT
    # NUMBER(1),
    # CASE
    # NUMBER(1),
    # AMOD
    # NUMBER(1),
    # ROOT
    # NUMBER(1),
    # NMOD_NPMOD
    # NUMBER(1),
    # AUX_PASS
    # NUMBER(1),
    # MARK
    # NUMBER(1),
    # ADVCL_RELCL
    # NUMBER(1),
    # ADVMOD
    # NUMBER(1),
    # NMOD
    # NUMBER(1),
    # IOBJ
    # NUMBER(1),
    # DET_PREDET
    # NUMBER(1),
    # FIXED
    # NUMBER(1),
    # DET
    # NUMBER(1),
    # COMPOUND
    # NUMBER(1),
    # NSUBJ
    # NUMBER(1)
    # );
