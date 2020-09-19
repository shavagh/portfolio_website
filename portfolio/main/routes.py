from flask import render_template, request, Blueprint
from portfolio.models import Post

main = Blueprint('main', __name__)

# tells the application which URL should call the associated function. 
@main.route("/")
@main.route("/home")
def home():
    return render_template('main_pages/index.html')

@main.route("/blog")
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('main_pages/blog.html', posts=posts)

@main.route('/experience')
def experience():
    return render_template('main_pages/experience.html')

@main.route('/portfolio')
def portfolio():
    return render_template('main_pages/portfolio.html')

@main.route('/education')
def education():
    return render_template('main_pages/education.html')

@main.route('/achievements')
def achievements():
    return render_template('main_pages/achievements.html')
