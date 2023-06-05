import os, sys, json,time,zipstream,re
from zipfile import ZIP_DEFLATED
from markupsafe import escape
from flask import  Flask, Response, make_response, render_template, send_file, send_from_directory,url_for, flash, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from init import app, db
from methods import send_email, generate_code, get_ipaddr
from models import User, Validation_code,IPinfo
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_login.mixins import AnonymousUserMixin

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    user = User.query.filter_by(id=user_id).first()
    return user


login_manager.login_view = 'login'


hw = 14
args = {'t': [1, 5],
        'n': [1, 100],
        'm': [1, 100],
        'student_count': [1, 100]}

@app.route('/')
def root():
    return hello()

@app.route('/index', methods=['GET','POST'])
def hello():
    ip=get_ipaddr()
    if current_user is not AnonymousUserMixin and current_user.is_authenticated:
        print(f"\033[1m\033[35m{ip} logged in as:\033[0m",
                f"id: {current_user.id} |",
                f"username: {current_user.username} |",
                f"email: {current_user.email} |",
                f"uploaded: {current_user.is_uploaded} |",
                f"got WA:{current_user.is_wrong}",sep=" ")
    else:
        print(f"\033[1m\033[31m{ip} have not logged in\033[0m")
    if request.method=='GET':
        #db.drop_all()
        db.create_all()
    if current_user.is_authenticated:
        run_args = ""
        if current_user.is_uploaded:
            username=current_user.username
            user_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}"
            runargs_path=f'{user_path}/runargs.json'
            if not os.path.exists(runargs_path):
                 return render_template('index.html',username=current_user.username,info=f"欢迎您，{current_user.username}")
            with open(runargs_path, 'r', encoding='utf8') as fp:
                try:
                    run_args = json.load(fp)
                except json.decoder.JSONDecodeError:
                    return render_template('index.html',username=current_user.username,info=f"欢迎您，{current_user.username}")
            
            return render_template('index.html',username=current_user.username,info=f"欢迎您，{current_user.username}", 
                    t=run_args['t'], n=run_args['n'], m=run_args['m'], student_count=run_args['student_count'])
        else:
            return render_template('index.html',username=current_user.username,info=f"欢迎您，{current_user.username}")
    else:
        return render_template('index.html')
    
@app.route('/about')
def about():
    if(current_user is not AnonymousUserMixin and current_user.is_authenticated):
        print(f"\033[1m\033[33m{current_user.username} founds Easter Egg!\033[0m")
    return render_template('about.html')

@app.route('/feedback')
@login_required
def feedback():
    return render_template('feedback.html')

@app.route('/tofeedback', methods = ['POST'])
@login_required
def tofeedback():
    #flash('Invalid input.')
    print(request.files)
    text = request.form['text'].strip()
    
    now_time = time.strftime('%m-%d_%H:%M:%S', time.localtime())    
    feedback_path=f"{app.config['WORKPLACE_FOLDER']}/feedback/{now_time}@{current_user.username}"
    if text != "":
        have_text = True
        with open(f"{feedback_path}@text", "w") as file:
            file.write(text)
    else:
        have_text = False

    if 'file' in request.files.to_dict():
        have_file = True
        file = request.files['file']
        file.save(f"{feedback_path}&{file.filename}")
    else:
        have_file = False
    
    if not have_text and not have_file:
        flash("未检测到任何有效信息")
        return "false"
    
    result = f"{current_user.username} send feedback"
    if have_text:
        result += " text"
    if have_file:
        result += " file"
    print(f"\033[1m\033[33m{result}\033[0m")
    
    if have_text and have_file:
        flash("成功发送反馈和文件")
    elif have_text:
        flash("成功发送反馈")
    else:
        flash("成功发送文件")
    return "true"

@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'

@app.route('/uploader', methods=['POST'])
def uploader():
    if not current_user.is_authenticated:
        return json.loads('{"code":"1","info":"%s"}'%("请先登录！"))
    # current_user.is_uploaded=0
    # db.session.commit()
    # return "0"
    username=current_user.username
    user_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}"
    havefile=request.form['havefile']
    if(havefile=="1"):
        print("uploading new file")
        f = request.files['file']
        exp=f.filename.split(".")[-1]
        if(exp!="jar" or exp==f.filename):
            return json.loads('{"code":"1","info":"%s"}'%("请上传.jar文件！"))

        if(not os.path.exists(user_path)):
            os.system(f"mkdir {user_path}")
            os.system(f"mkdir {user_path}/output/")
            os.system(f"mkdir {user_path}/wrongdata/")
        f.save(os.path.join(user_path, f"code_hw{hw}.jar"))
        print(f"{username} uploaded {f.filename} as code_hw{hw}.jar in{user_path}")
        os.system(f"rm {user_path}/output/* 2> /dev/null")
        #os.system(f"rm {user_path}/wrongdata/* 2> /dev/null")
        os.system(f"rm {user_path}/result.json 2> /dev/null")
    else:
        print("no new file")
        if not current_user.is_uploaded:
           return json.loads('{"code":"1","info":"%s"}'%("请上传.jar文件！"))
        
         
    #  三个参数，1<=n<=100, 1<=m<=100, 1<=student_count<=100
    print(request.form)
    # amount = request.form['amount']
    t = request.form['t']
    n = request.form['n']
    m = request.form['m']
    student_count = request.form['student_count']

    num_runs = 5
    runargs_path=f'{user_path}/runargs.json'
    os.system(f'touch {runargs_path}')
    with open(runargs_path,'r',encoding='utf8') as fp:
        try:
            runargs = json.load(fp)
        except json.decoder.JSONDecodeError:
            runargs = {}
        try:
            runargs['num_runs'] = num_runs
            runargs['t'] = int(t)
            runargs['n'] = int(n)
            runargs['m'] = int(m)
            runargs['student_count'] = int(student_count)
        except:
            pass
        
    with open(runargs_path,'w',encoding='utf8') as fp:
        json.dump(runargs, fp)

    current_user.is_uploaded = 1
    current_user.is_wrong = 0
    db.session.commit()

    print(f"{username} set t={t} n={n} & m={m} & student_count={student_count}")
    return json.loads('{"code":"0","info":"%s"}'%("上传成功！"))
    

@app.route('/signup')
def gotoSignup():
    return render_template('signup.html')


@app.route('/send_code', methods=['POST'])
def send_code():
    username=request.form['username']
    email=request.form['email']
    if User.query.filter(User.username==username).first() != None:
        return json.loads('{"code":"3","info":"%s"}'%("此用户名已被占用！"))
    if User.query.filter(User.email==email).first() != None:
        return json.loads('{"code":"2","info":"%s"}'%("此邮箱已被使用！"))
    if(re.match(''.join(['[0-9a-zA-Z_\\u4E00-\\u9FFF]{',f'{len(str(username))}','}']),str(username))==None):
        print(len(username))
        return json.loads('{"code":"3","info":"%s"}'%("用户名只能包含中文、英文、数字及下划线"))
    if(re.match('^[a-zA-Z0-9_-\\u4E00-\\u9FFF]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9_-]+)+$',email)==None):
        return json.loads('{"code":"2","info":"%s"}'%("请输入合法的邮箱地址！"))
    validation_code = Validation_code.query.filter(Validation_code.email==request.form['email']).first()
    if validation_code == None:
        validation_code = Validation_code()
        validation_code.last_time = 0
    
    #print(time.time() - validation_code.last_time)
    if time.time() - validation_code.last_time > 30:
        code = generate_code()
        validation_code.email = request.form['email']
        validation_code.set_code(code)
        validation_code.last_time = time.time()
        send_email(request.form['email'], code)
        db.session.add(validation_code)        
        db.session.commit()
        return json.loads('{"code":"0"}') #"send success"
    else:
        return json.loads('{"code":"1","time":"%d"}'%(int(validation_code.last_time + 30 - time.time())))

@app.route('/validate_code', methods=['POST'])
def validate_code():
    assert(request.method == 'POST')
    
    username = request.form['username']
    password = request.form['password']
    agpassword = request.form['agpassword']
    email = request.form['email']
    code = request.form['code']

    if User.query.filter(User.username==username).first() != None:
        return "1" #"already has this username"
    validation_code = Validation_code.query.filter(Validation_code.email==request.form['email']).first()
    if validation_code == None:
        return "2" #"please get validation code first"
    if agpassword != password:
        return "4" 
    if time.time() - validation_code.last_time > 1800:
        return "5"
    if validation_code.validate_code(code):
        user = User(username=username, email=email, is_uploaded=0, is_wrong=0)
        user.set_password(password)
        db.session.add(user)        
        db.session.commit()
        login_user(user)
        return "0" #"signup success"

    else:
        return "3" #"wrong code"

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/handlelogin',methods=['POST'])
def handlelogin():
    ip=get_ipaddr()
    ipinfo=IPinfo.query.filter_by(ip=ip).first()
    if(ipinfo==None):
        ipinfo=IPinfo(ip=ip,tries=1,last_time=time.time())
        db.session.add(ipinfo)
        db.session.commit()
        print(f"add {ip} into ipinfo")
    else:
        if ipinfo.tries==5:
            if(time.time()-ipinfo.last_time < 300):
                return json.loads('{"code":"1","info":"%s"}'%
                          (f"已达到最大错误次数，请{int(300-(time.time()-ipinfo.last_time))}s后再试"))
            else:
                ipinfo.tries=1
                ipinfo.last_time=time.time()
                db.session.commit()
        else:
            ipinfo.tries=ipinfo.tries+1
            ipinfo.last_time=time.time()
            db.session.commit()
    data = json.loads(request.form.get('data'))
    username=data['username']
    password=data['password']
    user=User.query.filter_by(username=username).first()
    if(user==None):
        user=User.query.filter_by(email=username).first()
    #print(user)
    if(user==None or not user.validate_password(password)):
        return json.loads('{"code":"1","info":"%s"}'%
                          (f"用户名或密码错误，还剩{5-ipinfo.tries}次机会"))
    else:
        login_user(user)
        ipinfo.tries=0
        db.session.commit()
        res='{"code":"0","username":"%s"}'%(user.username)
        print(user.username,"logged in")
        return json.loads(res)

@app.route('/logout',methods=['POST'])
@login_required
def logout():
    print(current_user.username,"logged out")
    logout_user()
    return "0"

@app.route('/download',methods=['POST'])
@login_required
def download():
    username=current_user.username
    print(username,"wants to download")
    user_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}"
    if not os.listdir(f"{user_path}/wrongdata"):
        print("blocked")
        res='{"code":"1"}'
    else:
        print("start download")
        os.system(f"rm {user_path}/wrongdata.zip 2> /dev/null")
        os.system(f"cd {user_path};zip -rq ./wrongdata.zip ./wrongdata")
        download_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}/wrongdata.zip"
        filename=download_path.split('/')[-1]
        res='{"code":"0","filename":"%s","path":"%s"}'%(filename,download_path)
    return json.loads(res)

@app.route('/update',methods=['POST'])
@login_required
def update():
    username = current_user.username
    print(username, "wants to update")
    json_path = f"{app.config['WORKPLACE_FOLDER']}/users/{username}/result.json"
    if os.path.exists(json_path):
        with open(json_path, "r") as file:
            json_data = json.load(file)
        runargs_path = f"{app.config['WORKPLACE_FOLDER']}/users/{username}/runargs.json"
        if os.path.exists(runargs_path):
            with open(runargs_path, "r") as file:
                runargs_data = json.load(file)
        json_data['is_running'] = runargs_data['is_running']
        if json_data['all']!=json_data['ac']:
            print(username,"got wrong")
            current_user.is_wrong = 1
            db.session.commit()
        else:
            current_user.is_wrong = 0
            db.session.commit()
        #print(json_data)
        return json.loads('{"code":"0","info":"%s","is_wrong":"%s"}'%(str(json_data),current_user.is_wrong))
    else:
        return json.loads('{"code":"1","info":"%s"}'%("还未开始评测，请稍等"))

def checkargs(runargs):
    print(runargs)
    for arg, bound in args.items():
        if arg not in runargs or not isinstance(runargs[arg], int) \
            or runargs[arg] < bound[0] or runargs[arg] > bound[1]:
            return False
    return True

@app.route('/start',methods=['POST'])
@login_required
def start():
    print(current_user.username,"wants to start")
    username=current_user.username
    user_path=f"{app.config['WORKPLACE_FOLDER']}/users/{username}"
    runargs_path=f'{user_path}/runargs.json'
    can_start=0
    with open(runargs_path, 'r', encoding='utf8') as fp:
        try:
            runargs = json.load(fp)
        except json.decoder.JSONDecodeError:
            runargs = {}
        if 'is_running' not in runargs.keys():
            runargs['is_running'] = 0
            
        if runargs['is_running']:
            can_start = 0
        else:
            can_start = 1
    if not checkargs(runargs):
        print("blocked_args")
        return "请先上传正确的参数"
    if(can_start==0):
        print("blocked")
        return "评测已开始，请等待评测完成后可再次开始"
    print(current_user.username,"started")
    current_user.is_wrong = 0
    db.session.commit()
    print("runner start")
    os.system(f"cd debug && python runner_hw{hw}.py {current_user.username} 2> err.log")
    print("judge for",current_user.username,"finished")
    # if(current_user.is_wrong==0):
    #     print(f"\033[1m\033[32m{current_user.username} got all AC!\033[0m")
    return "评测已完成！"

if __name__=='__main__':
    if sys.argv[0] == 'app.py':
        app.run(host='0.0.0.0', port='8080', debug = False)
    else:
        app.run(host='0.0.0.0', port='5001', debug = True)
    