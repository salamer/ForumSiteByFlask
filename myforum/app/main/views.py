from datetime import datetime
from flask import render_template,session,redirect,url_for,flash,abort,request,current_app,make_response

from . import main
from .forms import NameForm,EditProfileForm,PostForm,EditProfileAdminForm,CommentForm
from .. import db
from ..models import User,Permission,Post,Role,Comment
from flask.ext.login import login_user,login_required,logout_user,current_user
from ..decorators import admin_required,permission_required


@main.route('/',methods=['GET','POST'])
def index():
    form=PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post=Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    posts=Post.query.order_by(Post.timestamp.desc()).all()
    page=request.args.get('page',1,type=int)
    show_followed=False
    if current_user.is_authenticated():
        show_followed=bool(request.cookies.get('show_followed',''))
    if show_followed:
        query=current_user.followed_posts
    else:
        query=Post.query
    
#    pagination=Post.query.order_by(Pot.timestamp.desc()).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    pagination=Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=10,error_out=False)
    posts=pagination.items
    return render_template('index.html',form=form,posts=posts,pagination=pagination,show_followed=show_followed)
        

@main.route('/all')
@login_required
def show_all():
    resp=make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','',max_age=30*24*60*60)
    return resp
    
@main.route('/followed')
@login_required
def show_followed():
    resp=make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','1',max_age=30*24*60*60)
    return resp

@main.route('/user/<username>')
def user(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts=user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html',user=user,posts=posts)
    
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)
    
    
@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
#    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

#@main.route('/post/<int:id>')
#def post(id):
#    post=Post.query.get_or_404(id)
#    form=CommentForm()
#    if form.validate_on_submit():
#        comment=Comment(body=form.body.data,post=post,author=current_user._get_current_object())
#        db.sesion.add(comment)
#        flash('Your comment had been published')
#        return redirect(url_for('.post',id=post.id,page=-1))
#    page=request.args.get('page',1,type=int)
#    if page==-1:
#        page=(post.comments.count()-1)/current_app.config['FLASKY_COMMENTS_PER_PAGE']+1
#    pagination=post.comments.order_by(Comment.timestamp.asc()).paginate(page,per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],error_out=False)
#    comments=pagination.items
#    return render_template('post.html',post=[post],form=form,comments=comments,pagination=pagination)
    
@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)
    

@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    post=Post.query.get_or_404(id)
    if current_user!=post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.body=form.body.data
        db.session.add(post)
        flash('already updated yo~')
        return redirect(url_for('.post',id=post.id))
    form.body.data=post.body
    return render_template('edit_post.html',form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash('invalid user')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('you are already followed')
        return redirect(url_for('.user',username=username))
    current_user.follow(user)
    flash('you are following %s' % username)
    return redirect(url_for('.user',username=username)) 
        
@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username)) 
        
@main.route('/followers/<username>')
def followers(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash('invalid user')
        return redirect(url_for('.index'))
    page=request.args.get('page',1,type=int)
    pagination=user.followers.paginate(page,per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],error_out=False)
    follows=[{'user':item.follower,'timestamp':item.timestamp} for item in pagination.items]
    return render_template('followers.html',user=user,title="Followers of",endpoint='.followers',pagination=pagination,follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page=request.args.get('page',1,type=int)
    pagination=Comment.query.order_by(Comment.timestamp.desc().paginatate(page,per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],error_out=False))
    comments=pagination.items
    return render_template('moderate.html',comments=comments,pagination=pagination,page=page)   
    
    
@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment=Comment.query.get_or_404(id)
    comment.disabled=False
    db.session.add(comment)
    return redirect(url_for('.moderate',page=request.args.get('page',1,type=int)))
    
    
@main.route('/moderate/disabled/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disabled(id):
    comments=Comment.query.get_or_404(id)
    comment.disabled=True
    db.sessin.add(comment)
    return redirect(url_for('.moderate',page=request.args.get('page',1,type=int)))    





 
      
 
 
 
 
