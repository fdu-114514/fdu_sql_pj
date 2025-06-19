# models.py
from flask_sqlalchemy import SQLAlchemy

# 创建 SQLAlchemy 实例
db = SQLAlchemy()

# 关联表定义
# Paper 和 Author 的多对多关系表
paper_authors = db.Table('Paper_Authors',
                         db.Column('paper_id', db.Integer, db.ForeignKey('papers.id', ondelete='CASCADE'),
                                   primary_key=True),
                         db.Column('author_id', db.Integer, db.ForeignKey('authors.id', ondelete='CASCADE'),
                                   primary_key=True)
                         )

# Paper 和 Keyword 的多对多关系表
paper_keywords = db.Table('Paper_Keywords',
                          db.Column('paper_id', db.Integer, db.ForeignKey('papers.id', ondelete='CASCADE'),
                                    primary_key=True),
                          db.Column('keyword_id', db.Integer, db.ForeignKey('keywords.id', ondelete='CASCADE'),
                                    primary_key=True)
                          )

# Author 和 Institution 的多对多关系表
author_institutions = db.Table('Author_Institutions',
                               db.Column('author_id', db.Integer, db.ForeignKey('authors.id', ondelete='CASCADE'),
                                         primary_key=True),
                               db.Column('institution_id', db.Integer,
                                         db.ForeignKey('institutions.id', ondelete='CASCADE'), primary_key=True)
                               )


# 模型类定义

class Paper(db.Model):
    __tablename__ = 'papers'
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(512), nullable=False, index=True)

    abstract = db.Column(db.Text)

    publish_date = db.Column(db.Date, index=True)

    pdf_file_path = db.Column(db.String(255), nullable=False)

    conference_journal_id = db.Column(db.Integer, db.ForeignKey('conference_journals.id'), index=True)

    authors = db.relationship('Author', secondary=paper_authors, back_populates='papers')
    keywords = db.relationship('Keyword', secondary=paper_keywords, back_populates='papers')
    conference_journal = db.relationship('ConferenceJournal', back_populates='papers')


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True, nullable=False)

    papers = db.relationship('Paper', secondary=paper_authors, back_populates='authors')
    institutions = db.relationship('Institution', secondary=author_institutions, back_populates='authors')


class Institution(db.Model):
    __tablename__ = 'institutions'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), unique=True, nullable=False)

    authors = db.relationship('Author', secondary=author_institutions, back_populates='institutions')


class Keyword(db.Model):
    __tablename__ = 'keywords'
    id = db.Column(db.Integer, primary_key=True)

    word = db.Column(db.String(100), unique=True, nullable=False)

    papers = db.relationship('Paper', secondary=paper_keywords, back_populates='keywords')


class ConferenceJournal(db.Model):
    __tablename__ = 'conference_journals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum('Conference', 'Journal'))
    publication_date = db.Column(db.Date)
    location = db.Column(db.String(255))

    papers = db.relationship('Paper', back_populates='conference_journal')