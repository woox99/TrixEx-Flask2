from flask_app import app
from flask import render_template, redirect, flash, request, session, jsonify, get_flashed_messages
import urllib.parse
from flask_app.models.user import User
from flask_app.models.trick import Trick
from flask_app.models.favorite import Favorite
from flask_app.models.follower import Follower
from flask_app.models.comment import Comment
from flask_app.models.reply import Reply
from flask_app.models.login import Login
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app) 

# INDEX ______________________________________
@app.route('/index')
def index():
    session['active_userID'] = False
    tricks = Trick.get_all()
    return render_template('index.html', tricks=tricks)

# HOME ______________________________________
@app.route('/home')
def home():
    if not session['active_userID']:
        return redirect('/index')
    data = {
        'userID':session['active_userID']
    }
    user = User.get_user_by_id(data)
    tricks = Trick.get_all_with_favorited_by_active_user(data)
    return render_template('home.html', user=user, tricks=tricks)

# SEARCH ______________________________________
@app.route('/view/search')
def view_search():
    if not session['active_userID']:
        return redirect('/index')
    data = {
        'userID':session['active_userID'],
        'searchKey': session['searchKey']
    }
    trick_results = Trick.get_all_search_results_with_faved_by_actuser(data)
    user_results = User.get_search_results(data)
    results = True
    if not trick_results and len(user_results) == 0:
        results = False
    count = 0
    if trick_results != False:
        for trick in trick_results:
            if trick['is_private'] == 1:
                count +=1
        if count == len(trick_results) and len(user_results) == 0:
            results = False    
    user = User.get_user_by_id(data)
    search_value = session['searchValue']
    return render_template('search.html', user=user, trick_results=trick_results, user_results=user_results, search_value=search_value, results=results)

@app.route('/search', methods=['post'])
def search():
    if not session['active_userID']:
        return redirect('/index')
    searchKey = request.form['search_key']
    session['searchValue'] = searchKey
    remove = '@'
    searchKey = searchKey.replace(remove,'')
    session['searchKey'] = '%' + searchKey + '%'
    return redirect('/view/search')

@app.route('/guest/view/search')
def guest_view_search():
    data = {
        'searchKey': session['searchKey']
    }
    trick_results = Trick.get_search_results(data)
    user_results = User.get_search_results(data)
    results = True
    if not trick_results and len(user_results) == 0:
        results = False
    count = 0
    if trick_results != False:
        for trick in trick_results:
            if trick['is_private'] == 1:
                count +=1
        if count == len(trick_results) and len(user_results) == 0:
            results = False 
    search_value = session['searchValue']
    return render_template('guest_search.html', trick_results=trick_results, user_results=user_results, search_value=search_value, results=results)

@app.route('/guest/search', methods=['post'])
def guest_search():
    searchKey = request.form['search_key']
    session['searchValue'] = searchKey
    remove = '@'
    searchKey = searchKey.replace(remove,'')
    session['searchKey'] = '%' + searchKey + '%'
    return redirect('/guest/view/search')

@app.route('/get/search/tricks')
def get_search_tricks():
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return 'Forbidden', 403
    data = {
        'searchKey': session['searchKey']
    }
    trick_results = Trick.get_search_results(data)
    return jsonify(trick_results)

# FAVORITES ______________________________________
@app.route('/favorites')
def favorites():
    if not session['active_userID']:
        return redirect('/index')
    data = {
        'userID':session['active_userID']
    }
    user = User.get_user_by_id(data)
    tricks = Trick.get_all_with_favorited_by_active_user(data)
    return render_template('favorites.html', user=user, tricks=tricks)

@app.route('/favorite/trick', methods=['post'])
def favorite():
    data = {
        'userID':session['active_userID'],
        'trickID':request.json['trickID']
    }
    is_favorite = Favorite.get_favorite(data)
    if not is_favorite:
        Favorite.create(data)
        return jsonify({'is_favorited':True})
    else:
        Favorite.delete(data)
        return jsonify({'was_favorited':False})
    
# PROFILE ________________________
@app.route('/profile/<int:otherID>')
def profile(otherID):
    if not session['active_userID']:
        return redirect('/index')
    other_data = {
        'userID':otherID
    }
    session['otherID'] = otherID
    data = {
        'userID':session['active_userID'],
        'otherID':otherID
    }
    other = User.get_user_by_id(other_data)
    user = User.get_user_by_id(data)
    other_tricks = Trick.get_all_by_otherID(data)
    is_following = Follower.get_follow(data)
    num_followers = Follower.get_follower_count(data)
    num_followers = num_followers['num_followers']
    num_followings = Follower.get_following_count(data)
    num_followings = num_followings['num_followings']
    return render_template('profile.html', user=user, other=other, other_tricks=other_tricks, is_following=is_following, num_followers=num_followers, num_followings=num_followings)

@app.route('/get/other_tricks')
def get_other_tricks():
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return 'Forbidden', 403
    data = {
        'otherID': session['otherID'],
        'userID': session['active_userID']
    }
    other_tricks = Trick.get_all_by_otherID(data)
    return jsonify(other_tricks)

# GUEST PROFILE ____________________________
@app.route('/view/profile/<int:otherID>')
def guest_profile(otherID):
    other_data = {
        'userID':otherID
    }
    session['otherID'] = otherID
    other = User.get_user_by_id(other_data)
    other_tricks = Trick.guest_get_all_by_otherID(other_data)
    data = { 'otherID': otherID }
    num_followers = Follower.get_follower_count(data)
    num_followers = num_followers['num_followers']
    num_followings = Follower.get_following_count(data)
    num_followings = num_followings['num_followings']
    return render_template('guest_profile.html', other=other, other_tricks=other_tricks, num_followers=num_followers, num_followings=num_followings)

@app.route('/guest/get/other_tricks')
def guest_get_other_tricks():
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return 'Forbidden', 403
    other_data = {
        'userID': session['otherID'],
    }
    other_tricks = Trick.guest_get_all_by_otherID(other_data)
    return jsonify(other_tricks)

# FOLLOWERS ______________________________________
@app.route('/followers/<int:otherID>')
def followers(otherID):
    if not session['active_userID']:
        return redirect('/index')
    other_data = {
        'userID':otherID
    }
    data = {
        'userID':session['active_userID'],
        'otherID':otherID
    }
    session['otherID'] = otherID
    other = User.get_user_by_id(other_data)
    followers = Follower.get_all_followers_by_userID(other_data)
    user = User.get_user_by_id(data)
    is_following = Follower.get_follow(data)
    num_followers = Follower.get_follower_count(data)
    num_followers = num_followers['num_followers']
    num_followings = Follower.get_following_count(data)
    num_followings = num_followings['num_followings']
    return render_template('followers.html', user=user, other=other, followers=followers, is_following=is_following, num_followers=num_followers, num_followings=num_followings)

@app.route('/followings/<int:otherID>')
def followings(otherID):
    if not session['active_userID']:
        return redirect('/index')
    other_data = {
        'userID':otherID
    }
    data = {
        'userID':session['active_userID'],
        'otherID':otherID
    }
    session['otherID'] = otherID
    other = User.get_user_by_id(other_data)
    followings = Follower.get_all_followings_by_userID(other_data)
    user = User.get_user_by_id(data)
    is_following = Follower.get_follow(data)
    num_followers = Follower.get_follower_count(data)
    num_followers = num_followers['num_followers']
    num_followings = Follower.get_following_count(data)
    num_followings = num_followings['num_followings']
    return render_template('followings.html', user=user, other=other, followings=followings, is_following=is_following, num_followers=num_followers, num_followings=num_followings)

@app.route('/follow/user', methods=['post'])
def follow():
    if not session['active_userID']:
        return redirect('/index')
    data = {
        'userID':session['active_userID'],
        'otherID':request.json['otherID']
    }
    is_following = Follower.get_follow(data)
    if not is_following:
        Follower.create(data)
        return jsonify({'is_following':True})
    else:
        Follower.delete(data)
        return jsonify({'is_following':False})

# ADD_TRICK ______________________________________
@app.route('/add/trick')
def add_trick():
    if not session['active_userID']:
        return redirect('/index')
    data = {
        'userID':session['active_userID']
    }
    user = User.get_user_by_id(data)
    return render_template('add_trick.html', user=user)

@app.route('/create/trick', methods=['post'])
def create_trick():
    if not session['active_userID']:
        return redirect('/index')
    encoded_html = urllib.parse.quote(request.form['html_input'])
    encoded_css = urllib.parse.quote(request.form['css_input'])
    encoded_js = urllib.parse.quote(request.form['js_input'])
    Select = 'Select'
    select = 'select'
    encoded_html = encoded_html.replace(Select,'xyz956zyx')
    encoded_css = encoded_css.replace(Select,'xyz956zyx')
    encoded_js = encoded_js.replace(Select,'xyz956zyx')
    encoded_html = encoded_html.replace(select,'abc452cba')
    encoded_css = encoded_css.replace(select,'abc452cba')
    encoded_js = encoded_js.replace(select,'abc452cba')
    data = {
        'userID':session['active_userID'],
        'trick_name':request.form['trick_name'],
        'encoded_html':encoded_html,
        'encoded_css':encoded_css,
        'encoded_js':encoded_js,
        'scale':request.form['scale'],
        'description':request.form['description'],
        'is_private':request.form['is_private'],
        'num_views':request.form['num_views'],
        'is_authorized': int(request.form['is_authorized'])
    }
    msgs = []
    if not Trick.validate_trick(data):
        msgs = get_flashed_messages()
        return jsonify(msgs)
    Trick.create(data)
    return jsonify(msgs)

# EDIT_TRICK ______________________________________
@app.route('/edit/trick/<int:trickID>')
def edit_trick(trickID):
    if not session['active_userID']:
        return redirect('/index')
    data = {
        'userID':session['active_userID']
    }
    user = User.get_user_by_id(data)
    trick_data = {
        'trickID':trickID
    }
    trick = Trick.get_trick_by_trickID(trick_data)
    if session['active_userID'] != trick.user_id and user.is_admin == 0:
        return redirect('/logout')
    trick.html = urllib.parse.unquote(trick.html)
    trick.css = urllib.parse.unquote(trick.css)
    trick.js = urllib.parse.unquote(trick.js)
    Select = 'xyz956zyx'
    select = 'abc452cba'
    trick.html = trick.html.replace(Select,'Select')
    trick.css = trick.css.replace(Select,'Select')
    trick.js = trick.js.replace(Select,'Select')
    trick.html = trick.html.replace(select,'select')
    trick.css = trick.css.replace(select,'select')
    trick.js = trick.js.replace(select,'select')
    return render_template('edit_trick.html', user=user, trick=trick)

@app.route('/update/trick', methods=['post'])
def update_trick():
    if not session['active_userID']:
        return redirect('/index')
    encoded_html = urllib.parse.quote(request.form['html_input'])
    encoded_css = urllib.parse.quote(request.form['css_input'])
    encoded_js = urllib.parse.quote(request.form['js_input'])
    Select = 'Select'
    select = 'select'
    encoded_html = encoded_html.replace(Select,'xyz956zyx')
    encoded_css = encoded_css.replace(Select,'xyz956zyx')
    encoded_js = encoded_js.replace(Select,'xyz956zyx')
    encoded_html = encoded_html.replace(select,'abc452cba')
    encoded_css = encoded_css.replace(select,'abc452cba')
    encoded_js = encoded_js.replace(select,'abc452cba')
    data = {
        'trickID':request.form['trickID'],
        'userID':session['active_userID'],
        'trick_name':request.form['trick_name'],
        'encoded_html':encoded_html,
        'encoded_css':encoded_css,
        'encoded_js':encoded_js,
        'scale':request.form['scale'],
        'description':request.form['description'],
        'is_private':request.form['is_private'],
        'num_views':request.form['num_views'],
    }
    Trick.update(data)
    return redirect('/home')

@app.route('/trick/delete/<int:trickID>')
def delete_trick(trickID):
    if not session['active_userID']:
        return redirect('/index')
    data = {
        'trickID':trickID,
        'userID': session['active_userID']
    }
    trick = Trick.get_trick_by_trickID(data)
    user = User.get_user_by_id(data)
    if session['active_userID'] != trick.user_id and user.is_admin == 0:
        return redirect('/logout')
    Favorite.delete_favorite(data)
    Comment.delete_by_trickID(data)
    Reply.delete_by_trickID(data)
    Trick.delete(data)
    return redirect('/home')

# VIEW TRICK _____________________________________
@app.route('/view/trick/<int:trickID>')
def view_trick(trickID):
    if not session['active_userID']:
        return redirect('/index')
    data = {
        'trickID':trickID
    }
    trick = Trick.get_trick_and_creator_by_trickID(data)
    num_views = trick['num_views'] + 1
    data = {
        'userID':session['active_userID'],
        'otherID':trick['user_id'],
        'trickID':trickID,
        'num_views': num_views
    }
    Trick.add_views(data)
    user = User.get_user_by_id(data)
    trick['html'] = urllib.parse.unquote(trick['html'])
    trick['css'] = urllib.parse.unquote(trick['css'])
    trick['js'] = urllib.parse.unquote(trick['js'])
    Select = 'xyz956zyx'
    select = 'abc452cba'
    trick['html'] = trick['html'].replace(Select,'Select')
    trick['css'] = trick['css'].replace(Select,'Select')
    trick['js'] = trick['js'].replace(Select,'Select')
    trick['html'] = trick['html'].replace(select,'select')
    trick['css'] = trick['css'].replace(select,'select')
    trick['js'] = trick['js'].replace(select,'select')
    is_favorited = Favorite.get_favorite(data)
    is_following = Follower.get_follow(data)
    comments = Comment.get_comments_by_trickID(data)
    replies = Reply.get_replies_by_trickID(data)
    return render_template('view_trick.html', user=user, trick=trick, is_favorited=is_favorited, is_following=is_following, comments=comments, replies=replies)

@app.route('/create/comment', methods=['post'])
def create_comment():
    data = {
        'userID':session['active_userID'],
        'trickID':request.form['trickID'],
        'content':request.form['content']
    }
    Comment.create(data)
    return redirect(f"/view/trick/{data['trickID']}")

@app.route('/delete/comment/<int:trickID>/<int:commentID>')
def delete_comment(trickID, commentID):
    data = {
        'commentID':commentID,
        'userID':session['active_userID']
    }
    comment=Comment.get_comment_and_creator(data)
    user = User.get_user_by_id(data)
    if session['active_userID'] != comment['user_id'] and user.is_admin == 0:
        return redirect('/logout')
    Reply.delete_by_commentID(data)
    Comment.delete(data)
    return redirect(f"/view/trick/{trickID}")

@app.route('/create/reply', methods=['post'])
def create_reply():
    data = {
        'userID':session['active_userID'],
        'trickID':request.form['trickID'],
        'commentID':request.form['commentID'],
        'content':request.form['content']
    }
    Reply.create(data)
    return redirect(f"/view/trick/{data['trickID']}")

@app.route('/delete/reply/<int:replyID>/<int:trickID>')
def delete_reply(replyID, trickID):
    data = {
        'replyID':replyID,
        'trickID':trickID,
        'userID': session['active_userID']
    }
    reply=Reply.get_reply_and_creator(data)
    user = User.get_user_by_id(data)
    if session['active_userID'] != reply['user_id'] and user.is_admin == 0:
        return redirect('/logout')
    Reply.delete_by_replyID(data)
    return redirect(f"/view/trick/{data['trickID']}")

@app.route('/guest/view/trick/<int:trickID>')
def guest_view_trick(trickID):
    data = {
        'trickID':trickID
    }
    trick = Trick.get_trick_and_creator_by_trickID(data)
    num_views = trick['num_views'] + 1
    data = {
        'otherID':trick['user_id'],
        'trickID':trickID,
        'num_views': num_views
    }
    Trick.add_views(data)
    trick['html'] = urllib.parse.unquote(trick['html'])
    trick['css'] = urllib.parse.unquote(trick['css'])
    trick['js'] = urllib.parse.unquote(trick['js'])
    Select = 'xyz956zyx'
    select = 'abc452cba'
    trick['html'] = trick['html'].replace(Select,'SelectSelect')
    trick['css'] = trick['css'].replace(Select,'Select')
    trick['js'] = trick['js'].replace(Select,'Select')
    trick['html'] = trick['html'].replace(select,'select')
    trick['css'] = trick['css'].replace(select,'select')
    trick['js'] = trick['js'].replace(select,'select')
    comments = Comment.get_comments_by_trickID(data)
    replies = Reply.get_replies_by_trickID(data)
    return render_template('guest_view_trick.html', trick=trick, comments=comments, replies=replies)




# SIGNUP ______________________________________
@app.route('/signup')
def sign_up():
    return render_template('sign_up.html')

@app.route('/create/user', methods=['post'])
def create_user():
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'username':request.form['username'],
        'email':request.form['email'],
        'password':request.form['password'],
        'confirm_password':request.form['confirm_password'],
    }
    msgs = []
    if not User.validate_signup(data):
        msgs = get_flashed_messages()
        return jsonify(msgs)
    data['password'] = bcrypt.generate_password_hash(data['password'])
    session['active_userID'] = User.create(data) #returns user id
    return jsonify(msgs)

# LOGIN ______________________________________
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/user', methods=['post'])
def login_user():
    data = {
        'email':request.form['email'],
        'password':request.form['password']
    }
    user = User.validate_login(data)
    msgs = []
    if not user:
        msgs = get_flashed_messages()
        return jsonify(msgs)
    data['userID'] = user.id
    User.last_login(data)
    Login.login_stamp(data)
    session['active_userID'] = user.id
    return jsonify(msgs)

# GLOBAL ________________________
@app.route('/logout')
def logout():
    session['active_userID'] = False
    return redirect('/login')

@app.route('/get/tricks')
def get_tricks():
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return 'Forbidden', 403
    return jsonify(Trick.get_all())

@app.route('/get/favorite_tricks')
def get_favorite():
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        # Handle direct browser access, return an error response or redirect to a different page
        return 'Forbidden', 403
    data = {
        'userID': session['active_userID']
    }
    favorites = Trick.get_all_favorited_by_active_user(data)
    return jsonify(favorites)


# ADMIN ________________________
@app.route('/users')
def all_users():
    if not session['active_userID']:
        return 'Forbidden', 403
    users = User.get_all_formatted_date()
    data={
        'userID':session['active_userID']
    }
    user = User.get_user_by_id(data)
    if user.is_admin == 0:
        return redirect('/logout')
    return render_template('users.html', user=user, users=users)

@app.route('/authorize/<int:userID>')
def authorize(userID):
    if not session['active_userID']:
        return 'Forbidden', 403
    data = {
        'userID':session['active_userID']
    }
    user = User.get_user_by_id(data)
    if user.is_admin == 0:
        return 'Forbidden', 403
    data = {
        'userID':userID
    }
    other = User.get_user_by_id(data)
    if other.is_authorized == 0:
        data['is_authorized'] = 1
    else:
        data['is_authorized'] = 0
    User.authorize(data)
    return redirect('/users')

@app.route('/ban/<int:userID>')
def ban(userID):
    if not session['active_userID']:
        return 'Forbidden', 403
    data = {
        'userID':session['active_userID']
    }
    user = User.get_user_by_id(data)
    if user.is_admin == 0:
        return 'Forbidden', 403
    data = {
        'userID':userID
    }
    other = User.get_user_by_id(data)
    if other.is_banned == 0:
        data['is_banned'] = 1
    else:
        data['is_banned'] = 0
    User.ban(data)
    return redirect('/users')

@app.route('/admin/<int:userID>')
def admin(userID):
    if not session['active_userID']:
        return 'Forbidden', 403
    data = {
        'userID':session['active_userID']
    }
    user = User.get_user_by_id(data)
    if user.is_admin == 0:
        return 'Forbidden', 403
    data = {
        'userID':userID
    }
    other = User.get_user_by_id(data)
    if other.is_admin == 0:
        data['is_admin'] = 1
    else:
        data['is_admin'] = 0
    User.admin(data)
    return redirect('/users')

@app.route('/logins')
def logins():
    if not session['active_userID']:
        return 'Forbidden', 403
    data = {
        'userID':session['active_userID']
    }
    user = User.get_user_by_id(data)
    if user.is_admin == 0:
        return 'Forbidden', 403
    logins = Login.get_all_formatted_date()
    return render_template('logins.html', user=user, logins=logins)