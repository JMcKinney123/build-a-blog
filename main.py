from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy, ForeignKey


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'dsfhsad;ufoids7t98ugklchvxckj'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route("/blog", methods=['GET'])
def a_blog():

    if request.args:
        id =  request.args.get('id')
        blog = Blog.query.get(id)
        
        return render_template("one_blog.html", blog=blog, id=id)
    else:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)
    

@app.route("/newpost", methods=["POST", "GET"])
def addnewpost():
    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['body']
        error = ""
        error_too = ""
        if new_title == "":
            error = "Error, title required for blog."          
        
        if new_body == "":
            error_too = "Error, body is blank."
        
        if error or error_too:
            return render_template("add_new_blog.html", error=error, error_too=error_too)
        else:
            blog = Blog(new_title, new_body)
            db.session.add(blog)
            db.session.commit()
            blog_listing = "/blog?id=" + str(blog.id)
            return redirect(blog_listing)
    return render_template("add_new_blog.html")
 


if __name__ == '__main__':
    app.run()