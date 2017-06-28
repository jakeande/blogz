from flask import Flask, flash, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:blog@localhost:8889/Blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'aldkjfla;f;akjfdaads;lkja;lfdkjlkjsaloewijfnvz'   


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, name, body, owner):
        self.name = name
        self.body = body
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique= True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'sign_up', 'blogs', "index", ]
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route("/", methods=['GET','POST'])
def index():
    return render_template('new_blog_template.html', title="Blogz", user=User.query.all())


@app.route('/signup', methods=['POST', 'Get'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        if password != verify:
            flash('passwords did not match')
            return redirect('/signup')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("This " + username + " is already taken.")
            return redirect('/signup')
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect('/newpost')
    
    return render_template('signup.html')


@app.route('/login', methods= ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash('Logged in')
            return redirect('/')
        else:
            flash('User password incorrect or user name does not exist', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect ('/')

@app.route("/blog", methods=['GET', 'POST'])
def blogs():
    username=  request.args.get("user")
    if username:
        owner = User.query.filter_by(username=username).first()
        #blog = Blog.query.filter_by(user=user).all()
        return render_template('user.html', title="blog_name", blogs=owner.blogs)

    id = request.args.get('id')
    if id:
        entry = Blog.query.filter_by(id=id).first()
        return render_template('blog_view.html', blog=entry)
    
    blogs =  Blog.query.all()
    return render_template('user.html', blogs = blogs)

@app.route("/newpost", methods=['POST', 'GET'])
def new_blog():
    
    owner = User.query.filter_by(username = session["username"]).first()

    if request.method == 'POST':
        blog_body = request.form['blog']
        blog_name = request.form['blog_name']
        new_blog = Blog(blog_name, blog_body, owner)
    
        if blog_body == '':
            flash('Please Fill in Your Blog', 'error')
        
        if blog_name == '':
            flash('Please Add a Title', 'error')
        

    
        if not blog_name == '' and not blog_body == '':
            db.session.add(new_blog)
            db.session.commit()
            blog_id = new_blog.id

            return redirect('/blog?id={0}'.format(blog_id))

    return render_template('post.html', title="Blogz")


if __name__ == '__main__':
    app.run()
