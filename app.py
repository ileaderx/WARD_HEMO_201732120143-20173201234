import os
import re
from datetime import time, datetime
import time
import smtplib
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


app = Flask(__name__)
limiter = Limiter(
    app,
    key_func= get_remote_address,
        default_limits=[]
)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oaps.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
app.config['MAX_CONTENT_LENGTH'] = 0.1 * 1024 * 1024
app.config['DEBUG'] = True

db = SQLAlchemy(app)
from model import *
from service import *

with app.app_context():
    db.init_app(app)
    db.create_all()


def get_element(element):
    return element.title


@app.route('/')
def home():
    subjects = subjectService.find_all_subject(Subject)
    subjects.sort(key=get_element, reverse=False)
    return render_template('home.html', subjects=subjects)

@app.route('/subject/<subject_id>')
def subject():
    subject = subjectService.find_by_id()
    articles = articleService.find_by_subject()
    articles.reverse()
    particles = []
    for article in articles:
        if article.hided == 1:
            articles.remove(article)
            continue
        article.score = articleService.calPopularity(article)
        if article.score >= 0.3:
            particles.append(article)
    particles.sort(key=lambda item: item.score, reverse=True)
    return render_template('subject.html', subject=subject, articles=articles, particles=particles)


@app.route('/create_subject_page')
def create_subject():
    return render_template('create_subject.html')

@app.route('/add_subject',methods=['POST'])
def add_subject():
    form = request.form
    title = form['title'].title()
    upperTitle = title.upper()
    subject = subjectService.find_by_title(title, Subject)
    if subject:
        return 'Subject has existed!<a href="/">back to home</a>'
    subject = Subject(title=title, description=form['description'])
    subjectService.insert(subject)
    return redirect('/')


@app.route('/post')
def postPage():
    return render_template('post.html')

@app.route('/upload', methods=['POST'])
def upload():
    form = request.form
    for blank in form:
        if form[blank] == '': return "Blank can't be empty!"
    if re.match(r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$',form['email']) == None:
        return "Wrong email address format!"
    file = request.files['pdf'].read()
    filename = request.files['pdf'].filename
    split = filename.split('.')
    if len(split) != 2 or split[1] != 'pdf':
        return 'unsupported file type'
    for content in form:
        print(content)
        if content == 'pdf':
            continue
    filename = request.files['pdf'].filename
    email = form['email']
    user = userService.find_by_email(email, User)
    if user is None:
        user = User(email=email)
        userService.insert(user)
    subject = subjectService.find_by_title(form['subject'], Subject)
    if subject is None:
        return '<h2>There is no such subject, please create the subject first.</h2><a href="/">back to home</a>'
    nextid = articleService.nextId(Article)
    article = Article(title=form['title'],
                      postTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                      abstract=form['abstract'],
                      highlight_part=form['highlight'],
                      subject_id=subject.id,
                      user_id=user.id,
                      dl_link="static/"+str(nextid)+".pdf")
    articleService.insert(article)
    new_filename = "static/"+str(nextid)+".pdf"
    newFile = open(new_filename,"wb")
    newFile.write(file)
    newFile.close()
    msg = MIMEText('Thanks for posting article.If you are sure that you haven\'t post any articles in OAPS, please contact <a href="mailto:2912607882@qq.com">2912607882@qq.com</a> to delete it.','html', 'utf-8')
    server = smtplib.SMTP('smtp.qq.com')
    server.set_debuglevel(1)
    server.login('3279308836@qq.com', 'Vzqqc2463')
    server.sendmail('2912607882@qq.com', [email], msg.as_string())
    server.quit()
    return redirect('/article/' + str(article.id))

@app.route('/article/<article_id>')
def article(article_id):
    article = articleService.find_by_id(article_id, Article)
    user = userService.find_by_id(article_id, User)
    ip = ipService.find_ip_by_ip(request.remote_addr, IP)
    aip = ipService.find_aip_both(article_id, ArticleIp)
    comments = commentService.find_by_articleid(article_id, Comment)
    comments.reverse()
    if aip is None:#第一次访问
        aip = ArticleIp(ip_id=ip.id,article_id=article_id,vote_state=0)
        ipService.insert(aip)
        articleService.addAccess(article)
    return render_template('article.html',article = article,user=user,comments=comments,flag=0)


@app.route('/manage/article/<article_id>')
def manage_article(article_id):
    article = articleService.find_by_id(article_id)
    user = userService.find_by_id(article.user_id,userService.user_id)
    ip = ipService.find_ip_by_ip(request.remote_addr)
    aip = ipService.find_aip_both(article_id, ip.id)
    comments = commentService.find_by_articleid(article_id)
    comments.reverse()
    if aip is None:  # 第一次访问
        aip = ArticleIp(ip_id=ip.id, article_id=article_id, vote_state=0)
        ipService.insert(aip)
        articleService.addAccess(article)
    return render_template('article.html', article=article, user=user, comments=comments, flag=1)

@app.route('/<article_id>/comment',methods=['POST'])
@limiter.limit("2 per minute")
def article_comment(article_id):
    article = articleService.find_by_id(article_id, Article)
    form = request.form
    email = form['email']
    user = userService.find_by_email(email, User,)
    if user is None:
        user = User(email=email)
    comment = Comment(user_id=user.id, email=email, article_id=article_id, content=form['content'],postTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    commentService.insert(comment)
    articleService.addComment(article)
    ip = ipService.find_ip_by_ip(request.remote_addr, IP,id)
    cip = ipService.find_cip_by_both(comment.id, ip.id,id)
    if cip is None:
        ipService.insert(CommentIp(ip_id=ip.id, comment_id=comment.id, vote_state=0))
    return redirect('/article/' + article_id)

@app.route('/cupvote/<comment_id>')
def cupvote(comment_id):
    ip = ipService.find_ip_by_ip(request.remote_addr)
    commentService.upvote(comment_id, ip.id)
    return 'vote successfully!'

@app.route('/cdownvote/<comment_id>')
def cdownvote(comment_id):
    ip = ipService.find_ip_by_ip(request.remote_addr,IP)
    commentService.downvote(comment_id, ip.id)
    return 'vote successfully!'


@app.route('/author',methods=['POST'])
def author_find():
    form = request.form
    email = form['email']
    user = userService.find_by_email(email, User)
    if user is None:
        return "Author doesn't exist~!"
    articles = articleService.find_by_user(user.id, Article)
    for article in articles:
        article.score = articleService.calPopularity(article)
        if article.hided == 1:
            articles.remove(article)
            continue
    comments = commentService.find_by_userid(user.id, Comment)
    return render_template('author.html', user=user, articles=articles, comments=comments)


@app.route('/search')
def search():
    content = request.args['content']
    articles = articleService.search(content, Article)
    # print(articles.size())
    comments = commentService.search(content, Comment)
    return render_template('search_result.html', articles=articles, comments=comments)

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/manage')
def manage():
    return render_template('manage.html')



@app.route('/delete_article',methods=['POST'])
def delet_article():
    form = request.form

    aid = form['aid']
    article = articleService.find_by_id(int(aid), Article)
    if(article==None):
        return "Article doesn't exist!"
    articleService.delete(article)
    return render_template('manage.html')


if __name__ == '__main__':
    app.run()