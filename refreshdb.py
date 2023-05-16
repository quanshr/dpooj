from init import db, app
from models import User
#from flask_script import Manager, Shell

with app.app_context():
    users = User.query.all()

    for user in users:
        print(user.username, user.is_uploaded, user.is_wrong)
        user.is_uploaded = 0
        user.is_started = 0
        user.is_wrong = 0
    
    db.session.commit()
