from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path


DB_NAME = "database.db"


app = Flask('__name__')
app.config['SECRET_KEY'] = "sjfss dfs"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db = SQLAlchemy(app)


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Articles %r>" % self.id


def create_db(app):
    if not path.exists("." + DB_NAME):
        db.create_all(app=app)
        print("DB is created")


create_db(app)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()

    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def post_more(id):
    article = Article.query.get(id)

    return render_template("post_more.html", article=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "An error occurred while deleting the article"


@app.route('/posts/<int:id>/edit', methods=['POST', 'GET'])
def post_edit(id):
    article = Article.query.get(id)

    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "An error occurred while editing the article"
    else:
        return render_template("post-edit.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "An error occurred while adding the article"
    else:
        return render_template("create-article.html")


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
