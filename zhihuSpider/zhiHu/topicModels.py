# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class TopicInfo(Base):
    '''
    话题的信息，包含一级话题和二级话题： '一级话题/二级话题'
    '''
    __tablename__ = 'topicInfo'

    id = Column(Integer, Sequence('topicInfo_id_seq'), primary_key=True)
    topicCategory = Column(String(255))
    topicLink = Column(Text)

    def __repr__(self):
        return "<TopicInf(topicCategory='%s', topicLink='%s')>" % (
            self.topicCategory, self.topicLink)


class QuestionDec(Base):
    '''
    问答的基本描述
    '''
    __tablename__ = 'questionDec'

    id = Column(Integer, Sequence('questionDec_id_seq'), primary_key=True)
    # topicCategory = Column(String(255))
    questionName = Column(String(255))
    questionLikenum = Column(Integer)
    questionCommentnum = Column(Integer)
    questionLink = Column(Text)
    creatTime = Column(String(255))

    def __repr__(self):
        return "<QuestionDec(questionName='%s', questionLink='%s')>" % (
            self.questionName, self.questionLink)


class AnswerInfo(Base):
    '''
    问答的答案信息
    '''
    __tablename__ = 'answerInfo'

    id = Column(Integer, Sequence('answerInfo_id_seq'), primary_key=True)
    questionName = Column(String(255))
    questionInfo = Column(String(255))
    answer = Column(String(255))
    answerContentInfo = Column(Text)

    def __repr__(self):
        return "<QuestionDec(answer='%s')>" % self.questionName


class ArticleDec(Base):
    '''
    文章的基本描述信息
    '''
    __tablename__ = 'articleDec'

    id = Column(Integer, Sequence('articleDec_id_seq'), primary_key=True)
    # topicCategory = Column(String(255))
    articleName = Column(String(255))
    articleLikenum = Column(Integer)
    articleCommentnum = Column(Integer)
    articleLink = Column(Text)
    creatTime = Column(String(255))

    def __repr__(self):
        return "<QuestionDec(articleName='%s', articleLink='%s')>" % (
            self.articleName, self.articleLink)


class ArticleInfo(Base):
    '''
    文章的详细信息
    '''
    __tablename__ = 'articleInfo'

    id = Column(Integer, Sequence('articleInfo_id_seq'), primary_key=True)
    articleTitle = Column(String(255))
    articleauthor = Column(String(255))
    articleContent = Column(Text)

    def __repr__(self):
        return "<QuestionDec(articleTitle='%s', articleauthor='%s')>" % (
            self.articleTitle, self.articleauthor)


class TopicModel(object):
    '''
    管理数据库操作的总类
    parms: host: 'mysql+pymysql://user:pw@ip:3306/dbname?charset=utf8'
    '''
    def __init__(self, host, cmdEcho=True):
        self._host = host
        self.engine = create_engine(host, echo=cmdEcho, encoding='utf-8')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.dbSession = self.Session()

    def insertTopicInfo(self, category, link):
        '''
        插入TopicInfo表
        '''
        if isinstance(category, list) and isinstance(link, list):
            topicInfoList = [
                TopicInfo(topicCategory=category[i], topicLink=link[i]
                          ) for i in range(len(link))
            ]
            self.dbSession.add_all(topicInfoList)
            self.dbSession.commit()
            return True
        elif not isinstance(category, list) and not isinstance(link, list):
            try:
                self.dbSession.add(TopicInfo(topicCategory=category,
                                             topicLink=link))
                self.dbSession.commit()
            except Exception as e:
                print(e)

            return True
        else:
            raise TypeError

    def insertQuestionDec(self, name,likenum,
                          commentnum, link, creatTime):
        '''
        插入QuestionDec
        '''
        try:
            self.dbSession.add(QuestionDec(
                # topicCategory=category,
                questionName=name,
                questionLikenum=likenum,
                questionCommentnum=commentnum,
                questionLink=link,
                creatTime=creatTime
            ))
            self.dbSession.commit()
        except Exception as e:
            print(e)

    def insertArticleDec(self, name, likenum,
                         commentnum, link, createTime):
        '''
        插入ArticleDec
        '''
        try:
            self.dbSession.add(QuestionDec(
                # topicCategory=category,
                articleName=name,
                articleLikenum=likenum,
                articleCommentnum=commentnum,
                articleLink=link,
                creatTime=creatTime
            ))
            self.dbSession.commit()
        except Exception as e:
            print(e)
