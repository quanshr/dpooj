from init import db, app
from models import User
#from flask_script import Manager, Shell

with app.app_context():
    users = User.query.all()

    for user in users:
        print(f"\033[1m\033[35m",
                f"id: {user.id} |",
                f"username: {user.username} |",
                f"email: {user.email} |",
                f"uploaded: {user.is_uploaded} |",
                f"got WA:{user.is_wrong}\033[0m",sep=" ")