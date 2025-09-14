from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


@app.route('/', endpoint='index')
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)

@app.route('/create', endpoint='create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        post = Post(title=request.form['title'],description=request.form['description'], image=request.form['image'])
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('posts/create.html')

@app.route('/edit/<int:id>', endpoint='edit', methods=['GET', 'POST'])
def edit(id):
    post = db.get_or_404(Post, id)
    if request.method == 'POST':

        post.title = request.form['title']
        post.description = request.form['description']
        post.image = request.form['image']

        db.session.commit()
        return redirect(url_for('show', id=post.id))

    return render_template('posts/edit.html', post=post)


@app.route('/show/<int:id>', endpoint='show')
def show(id):
    post = db.get_or_404(Post, id)
    return render_template('posts/show.html', post=post)

@app.route('/delete/<int:id>', endpoint='delete')
def delete(id):
    post = db.get_or_404(Post, id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))


@app.errorhandler(404)
def error_not_found(error):
    return render_template('404.html')


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    image = db.Column(db.String(50))
    description = db.Column(db.Text)

    def __str__(self):
        return f"{self.title}"

    @property
    def image_url(self):
        return url_for("static", filename=f"posts/{self.image}")

    @property
    def delete_url(self):
        return url_for('delete', id=self.id)

    @property
    def show_url(self):
        return url_for('show', id=self.id)

    @property
    def edit_url(self):
        return url_for('edit', id=self.id)

if __name__ == "__main__":
    app.run(debug=True)