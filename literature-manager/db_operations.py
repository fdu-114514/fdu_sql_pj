# db_operations.py
import logging
from models import db, Paper, Author, Institution, Keyword, ConferenceJournal
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime # 确保导入了 timedelta
import random


def get_or_create(session, model, **kwargs):
    """
    Checks if an instance of a model exists in the database.
    If it exists, return it. Otherwise, create a new one, add, commit, and return it.
    """
    try:
        return session.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def add_paper_from_parsed_data(parsed_data):
    """
    Adds a paper and its related data to the database, with random date generation for missing dates.
    """
    if not parsed_data: return None
    session = db.session
    if session.query(Paper).filter_by(title=parsed_data['title']).first(): return None

    pub_info = parsed_data.get('publication_info', {})
    conference_journal_obj = None
    paper_publish_date = None

    if pub_info.get('name'):
        conference_journal_obj = get_or_create(session, ConferenceJournal, name=pub_info['name'])
        conference_journal_obj.type = pub_info.get('type')
        conference_journal_obj.location = pub_info.get('location')

        date_str = pub_info.get('publication_date')
        if date_str:
            try:
                paper_publish_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                try:
                    paper_publish_date = datetime.strptime(date_str, '%Y').date()
                except (ValueError, TypeError):
                    paper_publish_date = None

        conference_journal_obj.publication_date = paper_publish_date
        session.add(conference_journal_obj)
        session.commit()

    # 创建 Paper 对象
    new_paper = Paper(
        title=parsed_data['title'],
        abstract=parsed_data['abstract'],
        pdf_file_path=parsed_data['pdf_file_path'],
        publish_date=paper_publish_date,
        conference_journal_id=conference_journal_obj.id if conference_journal_obj else None
    )

    # 处理作者和关键词
    processed_author_ids = set()
    for author_data in parsed_data.get('authors', []):
        if not author_data.get('name'): continue
        author_obj = get_or_create(session, Author, name=author_data['name'])
        if author_obj.id not in processed_author_ids:
            for inst_name in author_data.get('institutions', []):
                inst_obj = get_or_create(session, Institution, name=inst_name)
                if inst_obj not in author_obj.institutions:
                    author_obj.institutions.append(inst_obj)
            new_paper.authors.append(author_obj)
            processed_author_ids.add(author_obj.id)

    for keyword_word in parsed_data.get('keywords', []):
        keyword_obj = get_or_create(session, Keyword, word=keyword_word)
        if keyword_obj not in new_paper.keywords:
            new_paper.keywords.append(keyword_obj)

    session.add(new_paper)
    session.commit()
    return new_paper