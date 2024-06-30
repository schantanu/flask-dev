from flask import Flask

from datetime import datetime
from pytz import timezone
from re import X
from sqlalchemy import func
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, render_template_string
from flaskapp import db
from flaskapp.challenge.forms import CreateChallengeForm, JoinChallengeForm
from flaskapp.posts.forms import PostForm
from flaskapp.models import User, Challenge, Entry, Post
from flask_login import current_user, login_required
from flaskapp.challenge.utils import bmi_calculator, test_posts

challenge = Blueprint('challenge', __name__)

@challenge.route("/challenges", methods=['GET'])
@login_required
def challenges():
    """ Show a list of all challenges """
    challenges = Challenge.query.all()
    user = User.query.filter_by(id=current_user.id).first()
    entry = Entry.query.filter_by(user_id=current_user.id).first()

    for challenge in challenges:
        for entry in challenge.entries:
            print(challenge.name, entry.user_id)

    return render_template('challenges.html', user=user, challenges=challenges, entry=entry)


@challenge.route("/challenge/new", methods=['GET','POST'])
@login_required
def new_challenge():

    if current_user.is_authenticated:
        form = CreateChallengeForm()

        if form.validate_on_submit():

            # Restrict challenge creation by Users challenge count
            # user_challenges = Challenge.query.filter_by(user_id=current_user.id).all()
            # if user_challenges is None:

            user = User.query.filter_by(id=current_user.id).first()
            if user.role == 'admin':
                challenge = Challenge(name=form.name.data, type=form.type.data, description=form.description.data,
                                        start_date=form.start_date.data, end_date=form.end_date.data)
                db.session.add(challenge)
                db.session.commit()

                flash(f"Your {form.type.data} challenge '{form.name.data}' has been created. Good luck!", 'success')
                return redirect(url_for('main.home'))

            else:
                flash(f'You currently do not have permission to create a Fitness challenge. Reach out to the site admin for further details.', 'success')
                return redirect(url_for('main.home')) 
       
    return render_template('new_challenge.html', title='Create Challenge', form=form)


# @challenge.route("/challenge/<int:challenge_id>/update", methods=['GET','POST'])
# @login_required
# def update_challenge(challenge_id):
#     challenge = Challenge.query.get_or_404(challenge_id)
#     if challenge.user != current_user:
#         abort(403)
#     form = CreateChallengeForm()
#     if form.validate_on_submit():
#         challenge.name = form.name.data
#         challenge.type = form.type.data
#         challenge.description = form.description.data
#         challenge.start_date = form.start_date.data
#         challenge.end_date = form.end_date.data
#         db.session.commit()
#         flash(f'The {form.name.data} challenge has been updated!', 'success')
#         return redirect(url_for('challenge.challenge_page', challenge_id=challenge.id))
#     elif request.method == 'GET':
#         form.name.data = challenge.name
#         form.type.data = challenge.type
#         form.description.data = challenge.description
#         form.start_date.data = challenge.start_date
#         form.end_date.data = challenge.end_date
#     return render_template('new_challenge.html', title='Update Challenge', form=form)


# @challenge.route("/challenge/<int:challenge_id>/delete", methods=['POST'])
# @login_required
# def delete_challenge(challenge_id):

#     challenge = Challenge.query.get_or_404(challenge_id)
#     print(challenge_id, current_user.id)
#     if challenge.user_id != current_user.id:
#         abort(403)
#     db.session.delete(challenge)
#     db.session.commit()
#     flash(f'The {challenge.name.data} has been deleted!','success')
#     return redirect(url_for('main.home'))


@challenge.route("/join_challenge/<int:challenge_id>", methods=['GET','POST'])
@login_required
def join_challenge(challenge_id):
    
    if current_user.is_authenticated:
        challenge = Challenge.query.filter_by(id=challenge_id).first()
        entry = Entry.query.filter_by(user_id=current_user.id).filter_by(challenge_id=challenge_id).first()

        if entry and entry.enrolled is False:
            flash(f'You have already enrolled in the challenge, and pending approval from the admin.', 'info')
            return redirect(url_for('main.home'))
        elif entry and entry.enrolled is True:
            return redirect(url_for('challenge.challenge_page', challenge_id=challenge.id))
        else:
            form = JoinChallengeForm()

            if form.validate_on_submit():
                current_bmi, current_category = bmi_calculator(form.metric.data, form.current_weight.data,
                                                                form.height_ft.data, form.height_in.data)

                goal_bmi, goal_category = bmi_calculator(form.metric.data, form.goal_weight.data,
                                                            form.height_ft.data, form.height_in.data)
                print(current_bmi, current_category)
                print(goal_bmi, goal_category)

                entry = Entry(challenge_id=challenge_id,
                                user_id=current_user.id,
                                region=form.region.data, 
                                metric=form.metric.data, 
                                current_weight=form.current_weight.data, 
                                goal_weight=form.goal_weight.data)
                db.session.add(entry)
                db.session.commit()

                flash(f'You have applied for the challenge. Please await admin moderation.', 'success')
                return redirect(url_for('main.home'))
    return render_template('join_challenge.html', title='Join Challenge', form=form, challenge=challenge)


@challenge.route("/challenge/<int:challenge_id>", methods=['GET','POST'])
@login_required
def challenge_page(challenge_id):

    if current_user.is_authenticated:
        
        user = User.query.filter_by(id=current_user.id).first()
        entry = Entry.query.filter_by(user_id=current_user.id).first()
        challenge = Challenge.query.filter_by(id=challenge_id).first()

        page = request.args.get('page', 1, type=int)
        posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        
        # Get user's latest post
        todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
        latest_post = Post.query.filter_by(user_id=current_user.id).filter(Post.date_posted >= todays_datetime).order_by(Post.date_posted.desc()).first()
        
        if latest_post:
            # print("User ID", latest_post.__table__.c)
            # print("User ID", latest_post)
            print("User ID", latest_post.user_id)

        # for i in latest_post:
        #     print(i.animal)
        
        # print("Latest timezone is", latest_post.date_posted.astimezone(timezone('US/Central')).strftime('%Y-%m-%d %H:%M:%S %Z%z'))

        form = PostForm()

        if form.validate_on_submit():
            if latest_post is None:
                post = Post(user_id=current_user.id, type=challenge.type, weight=form.weight.data)
                db.session.add(post)
                db.session.commit()
                flash(f'Your weight has been added for {datetime.today().strftime("%Y-%m-%d")}!','success')
                return redirect(url_for('challenge.challenge_page', challenge_id=challenge.id))
            else:
                post = Post.query.get_or_404(latest_post.id)
                post.weight = form.weight.data
                post.date_posted = datetime.utcnow()
                db.session.commit()
                flash(f'Your weight has been updated for {datetime.today().strftime("%Y-%m-%d")}.','success')
                return redirect(url_for('challenge.challenge_page', challenge_id=challenge.id))
        return render_template('challenge.html',form=form,posts=posts,user=user, entry=entry,challenge=challenge)
        # return render_template('challenge.html', challenge=challenge)
    
    return redirect(url_for('main.home')) #, challenge_id=challenge.id))
    # return render_template('challenge.html', title='Challenge')
    
@challenge.app_template_filter('localtime')
def datetimefilter(dtime, tzone, format='%b %d %I:%M %p'):
    tz = timezone('Asia/Kolkata')  # timezone you want to convert to from UTC (America/Los_Angeles)
    # tz = timezone('US/Central')
    utc = timezone('UTC')
    dtime = utc.localize(dtime, is_dst=None).astimezone(utc)
    local_dt = dtime.astimezone(tz)
    return local_dt.strftime(format)


@challenge.app_template_filter('datetimefilter')
def datetimefilter(value, format='%b %d %I:%M %p'):
    tz = timezone('Asia/Kolkata')  # timezone you want to convert to from UTC (America/Los_Angeles)
    # tz = timezone('US/Central')
    utc = timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)
