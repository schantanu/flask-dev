from datetime import datetime
from sqlalchemy import func
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskapp import db
from flaskapp.posts.forms import PostForm
from flaskapp.models import Post
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    post = post.query.filter_by(date_posted=datetime.today()).first()
    user_post = Post.query.filter_by(user_id=current_user.id)\
                            .filter(func.DATE(Post.date_posted)==datetime.today().strftime('%Y-%m-%d'))\
                            .first()

    print(f"Post is {user_post}.")
    if form.validate_on_submit():
        if post is None:
            post = Post(title=form.weight.data, user=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your weight has been added!','success')
            return redirect(url_for('challenge.challenge_page'))
        else:
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash('Your weight has been updated!','success')

    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title='Post', post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

