from flask import render_template, request, Blueprint
from portfolio.models import Post

main = Blueprint('main', __name__)

# tells the application which URL should call the associated function. 
@main.route("/")
@main.route("/home")
def home():
    return render_template('index.html')

@main.route("/blog")
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('blog.html', posts=posts)

@main.route('/experience')
def experience():
    return render_template('experience.html')

@main.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@main.route('/education')
def education():
    return render_template('education.html')

@main.route('/achievements')
def achievements():
    return render_template('achievements.html')
