from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'some_safe_secret'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(30), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.author}', '{self.content}')"
#
#
# data = [
#     {
#         'title': 'First Blog',
#         'author': 'author one',
#         'content': 'this is the content of blog bla bla...',
#         'date_posted': 'aug 20, 2020'
#     },
#     {
#         'title': 'Second Blog',
#         'author': 'author two',
#         'content': 'this is the content of blog bla bla...',
#         'date_posted': 'aug 21, 2020'
#     }
# ]


@app.route('/')
@app.route('/home')
def home():
    data = Post.query.all()
    return render_template('home.html', posts=data)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        post = Post(title=title, author=author, content=content)
        db.session.add(post)
        db.session.commit()
        flash("post is created")
        return redirect('/')
    return render_template('create_post.html', post=None)


@app.route('/update/<int:id>')
def update(id):
    if not id or id != 0:
        post = Post.query.get(id)
        if post:
            return render_template('update_post.html', post=post)

    return


@app.route('/update_post/<int:id>', methods=['GET', 'POST'])
def update_post(id):
    if not id or id != 0:
        post = Post.query.get(id)
        if post:
            db.session.delete(post)
            db.session.commit()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        post = Post(title=title, author=author, content=content)

        db.session.add(post)
        db.session.commit()
        flash("post is created")
        return redirect('/')
    return render_template('create_post.html', post=None)


@app.route('/delete/<int:id>')
def delete(id):
    if not id or id != 0:
        post = Post.query.get(id)
        if post:
            db.session.delete(post)
            db.session.commit()
        return redirect('/')

    return


if __name__ == '__main__':
    app.run(debug=True)
