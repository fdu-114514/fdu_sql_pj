# app.py
import os
import uuid
import json
import csv
import io
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from sqlalchemy import or_, func

from models import db, Paper, Author, Institution, Keyword, paper_authors, paper_keywords
from parser import parse_pdf_with_grobid
from db_operations import add_paper_from_parsed_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-key-for-this-project'

# !!! 重要：请将下面的 'YourStrongPassword' 替换为您自己的MySQL root 密码 !!!
DB_USER = 'root'
DB_PASS = 'Max114514'
DB_HOST = 'localhost'
DB_NAME = 'literature_management_system'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join('uploads', 'pdfs')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)

# 路由和视图函数

@app.route('/', methods=['GET', 'POST'])
def index():
    """主页：处理高级搜索并显示文献列表"""
    try:
        query = db.session.query(Paper)
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            author_name = request.form.get('author', '').strip()
            institution_name = request.form.get('institution', '').strip()
            keyword_text = request.form.get('keyword', '').strip()
            start_date = request.form.get('start_date', '').strip()
            end_date = request.form.get('end_date', '').strip()

            if title: query = query.filter(Paper.title.like(f"%{title}%"))
            if author_name: query = query.join(Paper.authors).filter(Author.name.like(f"%{author_name}%"))
            if institution_name: query = query.join(Paper.authors).join(Author.institutions).filter(
                Institution.name.like(f"%{institution_name}%"))
            if keyword_text: query = query.join(Paper.keywords).filter(Keyword.word.like(f"%{keyword_text}%"))
            if start_date: query = query.filter(Paper.publish_date >= start_date)
            if end_date: query = query.filter(Paper.publish_date <= end_date)

            papers = query.distinct().order_by(Paper.id.desc()).all()
        else:
            papers = Paper.query.order_by(Paper.id.desc()).all()
        return render_template('index.html', papers=papers)
    except Exception as e:
        print(f"An error occurred in index route: {e}")
        return f"An internal error occurred: {e}", 500


@app.route('/upload', methods=['POST'])
def upload_file():
    """处理批量上传的PDF文件"""
    uploaded_files = request.files.getlist('files')
    if not uploaded_files or uploaded_files[0].filename == '':
        flash('No files selected', 'danger')
        return redirect(url_for('index'))

    success_count, fail_count = 0, 0
    for file in uploaded_files:
        if file and file.filename.endswith('.pdf'):
            unique_filename = str(uuid.uuid4()) + '.pdf'
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(pdf_path)

            parsed_data = parse_pdf_with_grobid(pdf_path)
            if parsed_data:
                new_paper = add_paper_from_parsed_data(parsed_data)
                if new_paper:
                    success_count += 1
                else:
                    fail_count += 1
            else:
                fail_count += 1

    flash(f'Batch upload finished. Added: {success_count}. Failed or already existed: {fail_count}.', 'info')
    return redirect(url_for('index'))


@app.route('/paper/delete/<int:paper_id>', methods=['POST'])
def delete_paper(paper_id):
    """处理删除单篇论文的请求"""
    paper_to_delete = db.session.get(Paper, paper_id)
    if paper_to_delete is None:
        flash(f'Paper with ID {paper_id} not found.', 'danger')
        return redirect(url_for('index'))

    try:
        db.session.delete(paper_to_delete)
        db.session.commit()
        flash(f'Successfully deleted paper: "{paper_to_delete.title}"', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting paper: {str(e)}', 'danger')

    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    """显示数据统计和可视化的仪表盘页面"""
    stats = {
        'total_papers': db.session.query(Paper).count(),
        'total_authors': db.session.query(Author).count(),
        'total_institutions': db.session.query(Institution).count(),
        'total_keywords': db.session.query(Keyword).count(),
        'top_authors': db.session.query(Author, func.count(paper_authors.c.paper_id).label('paper_count')).join(
            paper_authors).group_by(Author.id).order_by(func.count(paper_authors.c.paper_id).desc()).limit(10).all(),
        'top_keywords': db.session.query(Keyword, func.count(paper_keywords.c.paper_id).label('paper_count')).join(
            paper_keywords).group_by(Keyword.id).order_by(func.count(paper_keywords.c.paper_id).desc()).limit(10).all()
    }

    papers_per_year = db.session.query(
        func.extract('year', Paper.publish_date).label('year'),
        func.count(Paper.id).label('count')
    ).filter(
        Paper.publish_date.isnot(None)
    ).group_by('year').order_by('year').all()

    chart_data = {
        'labels': [str(int(entry.year)) for entry in papers_per_year if entry.year is not None],
        'data': [entry.count for entry in papers_per_year if entry.year is not None]
    }

    return render_template('dashboard.html', stats=stats, chart_data=chart_data)


@app.route('/export/json')
def export_json():
    """将所有数据导出为JSON格式"""
    papers = Paper.query.all()
    papers_list = [
        {'title': p.title, 'abstract': p.abstract, 'publish_date': str(p.publish_date),
         'authors': [a.name for a in p.authors], 'keywords': [k.word for k in p.keywords]}
        for p in papers
    ]
    return Response(
        json.dumps(papers_list, indent=4, ensure_ascii=False),
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=papers.json"}
    )


@app.route('/export/csv')
def export_csv():
    """将所有数据导出为CSV格式"""
    string_io = io.StringIO()
    writer = csv.writer(string_io)
    writer.writerow(['Title', 'Abstract', 'Publish Date', 'Authors', 'Keywords'])
    papers = Paper.query.all()
    for p in papers:
        writer.writerow([
            p.title, p.abstract, str(p.publish_date),
            '; '.join([a.name for a in p.authors]),
            '; '.join([k.word for k in p.keywords])
        ])
    output = string_io.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=papers.csv"}
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)