from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


class Config(object):
    # sqlalchemy 的配置参数
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/author_book_py04"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app.config.from_object(Config)


db = SQLAlchemy(app)

# 定义数据库的模型


class Author(db.Model):
    __tablename__ = "tbl_authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    books = db.relationship("Book", backref="author")


class Book(db.Model):
    """书籍"""
    __tablename__ = 'tbl_books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    author_id = db.Column(db.Integer, db.ForeignKey('tbl_authors.id'))


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    # 生成数据
    au_xi = Author(name='我吃西红柿')
    au_qian = Author(name='萧潜')
    au_san = Author(name='唐家三少')
    db.session.add_all([au_xi, au_qian, au_san])
    db.session.commit()

    bk_xi = Book(name='吞噬星空', author_id=au_xi.id)
    bk_xi2 = Book(name='寸芒', author_id=au_qian.id)
    bk_qian = Book(name='飘渺之旅', author_id=au_qian.id)
    bk_san = Book(name='冰火魔厨', author_id=au_san.id)
    # 把数据提交给用户会话
    db.session.add_all(
        [bk_xi, bk_xi2, bk_qian, bk_san])
    # 提交会话
    db.session.commit()
    app.run(debug=True)
