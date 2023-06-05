from init import db, app
from models import User
import os

hw = 14
user_path = "static/workplace/users"
std_path = f"static/workplace/std/code_hw{hw}"

with app.app_context():
    users = User.query.all()

    for user in users:
        if (user.is_uploaded == True):
           name = user.username
           n = len(os.listdir(std_path))
           os.system(f"cp {user_path}/{name}/code_hw{hw}.jar {std_path}/code_{n}.jar")
           