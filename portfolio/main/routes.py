from flask import render_template, request, Blueprint
from portfolio.models import Post

# create Blueprint to display main pages in the website
main = Blueprint('main', __name__)

# url path to display home page
@main.route("/")
@main.route("/home")
def home():
    return render_template('main_pages/index.html')

# url path to display blog page
@main.route("/blog")
def blog():
    # get current page number , default page set to 1, and are integers
    page = request.args.get('page', 1, type=int)
    # order posts in descending order (newest first) and split post 5 per page
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # display blog page and pass post infomation
    return render_template('main_pages/blog.html', posts=posts)

# url path to display experience page
@main.route('/experience')
def experience():
    return render_template('main_pages/experience.html')

# url path to display portfolio page
@main.route('/portfolio')
def portfolio():
    return render_template('main_pages/portfolio.html')

# url path to display education page
@main.route('/education')
def education():
    return render_template('main_pages/education.html')

# url path to display achievement page
@main.route('/achievements')
def achievements():
    return render_template('main_pages/achievements.html')
