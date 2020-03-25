from server import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    articles = db.relationship('Article', backref='author', lazy='dynamic')

    def __repr__(self):
        return "User: {}".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return self.id

    def get_author_name(self):
        return User.query.filter_by(id=self.author_id).first().username


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    orders = db.relationship('Order', backref='company', lazy='dynamic')

    def __repr__(self):
        return self.id

    def num_order(self):
        return len(Order.query.filter_by(company_id=self.id).all())

    def calc_time(self):
        time = 0
        orders = Order.query.filter_by(company_id=self.id).all()
        for o in orders:
            time += o.calc_time()
        return time


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    reference = db.Column(db.String(140))
    articles = db.relationship('Article', backref='order', lazy='dynamic')

    def calc_time(self):
        time = 0
        articles = Article.query.filter_by(order_id=self.id)
        for a in articles:
            time += a.time
        return time

    def get_company_name(self):
        return Company.query.filter_by(id=self.company_id).first().name

    def num_articles(self):
        return len(Article.query.filter_by(order_id=self.id).all())

    def __repr__(self):
        return self.id


