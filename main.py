from flask import Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'aldkjfla;f;akjfdaads;lkja;lfdkjlkjsaloewijfnvz'   


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(500))


    def __init__(self, name, body):
        self.name = name
        self.body = body


@app.route("/", methods=['GET','POST'])
def index():
    blogs = Blog.query.all()

    return render_template('new_blog_template.html', title="Build-a-Blog", blogs=blogs)


@app.route("/blogs", methods=['GET', 'POST'])
def blogs():

    if request.method == 'POST':
        blog_body = request.form['blog']
        blog_name = request.form['blog_name']
        new_blog = Blog(blog_name, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        newblog_id = new_blog.id
        blogs = Blog.query.filter_by(id=newblog_id).all()
        return render_template('new_blog_template.html', title="blog_name", blogs=blogs)

@app.route('/blog')
def single_blog():
    id = request.args.get('id')
    entry = Blog.query.filter_by(id=id).first()
    blog_name = entry.name
    blog_body = entry.body
    return render_template('blog_view.html', blog_name=blog_name, blog_body=blog_body) 



@app.route("/newpost", methods=['POST', 'GET'])
def new_blog():
    blogs = Blog.query.all()
   
    if request.method == 'POST':
        blog_body = request.form['blog']
        blog_name = request.form['blog_name']
        new_blog = Blog(blog_name, blog_body)
        
        if blog_body == '':
            flash('Please Fill in Your Blog', 'error')
        
        if blog_name == '':
            flash('Please Add a Title', 'error')

    
        if not blog_name == '' and not blog_body == '':
            db.session.add(new_blog)
            db.session.commit()
            blog_id = new_blog.id


            return redirect('/?id={0}'.format(blog_id))
    
    return render_template('post.html', title="Build-a-Blog", blogs=blogs)
    
  
if __name__ == '__main__':
    app.run()
