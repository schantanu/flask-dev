from datetime import datetime
from flask import redirect, render_template, request, Blueprint, url_for
from flaskapp.models import User, Entry, Challenge, Post
from flaskapp.challenge.forms import JoinChallengeForm
from flaskapp.posts.forms import PostForm
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
@login_required
def home():
    
    user = User.query.filter_by(id=current_user.id).first()
    challenges = Challenge.query.all()
    entries = Entry.query.filter_by(user_id=current_user.id).filter_by(enrolled=True).all()

    return render_template('home.html', user=user, challenges=challenges, entries=entries)

@main.route("/challenges")
@login_required
def challenges():

    challenges = Challenge.query.all()
    user = User.query.filter_by(id=current_user.id).first()
    return render_template('challenges_all.html', user=user, challenges=challenges)

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/post")
def post():
    
    user = User.query.filter_by(id=current_user.id).first()
    challenges = Challenge.query.all()
    # entries = Entry.query.filter_by(user_id=current_user.id).filter_by(enrolled=True).all()
    entry = Entry.query.filter_by(user_id=current_user.id).first()

    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    
    form = PostForm()

    cal = 100
    print(cal)

    return render_template('home.html', user=user, challenges=challenges, entry=entry, posts=posts, form=form, cal=cal)

@main.route("/dashboard", methods=['GET','POST'])
@login_required
def dashboard():

    if current_user.is_authenticated:
        
        user = User.query.filter_by(id=current_user.id).first()
        entry = Entry.query.filter_by(user_id=current_user.id).first()
        # challenge = Challenge.query.filter_by(id=challenge_id).first()

        page = request.args.get('page', 1, type=int)
        posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        
        # Get user's latest post
        todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
        latest_post = Post.query.filter_by(user_id=current_user.id).filter(Post.date_posted >= todays_datetime).order_by(Post.date_posted.desc()).first()
        
        if latest_post:
            # print("User ID", latest_post.__table__.c)
            # print("User ID", latest_post)
            print("User ID", latest_post.user_id)

@main.route("/new_home", methods=['GET','POST'])
@login_required
def new_home():

    user = User.query.filter_by(id=current_user.id).first()
    challenges = Challenge.query.all()
    entries = Entry.query.filter_by(user_id=current_user.id).filter_by(enrolled=True).all()
    posts = Post.query.filter_by(user_id=current_user.id).all()

    print(posts)

    return render_template('new_home.html', user=user, challenges=challenges, entries=entries, posts=posts)

    