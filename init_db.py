from server import db
from server.models import User


def add_user(name, password):
    user = User(username=name)
    user.set_password(password=password)
    db.session.add(user)


db.reflect()
db.drop_all()
db.create_all()

add_user('erik', 'hello')
db.session.commit()
