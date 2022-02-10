from flask_login import login_user
from flask_login import login_required, logout_user,current_user
from flask import request, render_template,flash,redirect,url_for
from watchlist import app,db
from watchlist.models import User, Movie

@app.route('/settings',methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) >20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        
        current_user.name =name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))
    return render_template('settings.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    app.config['SECRET_KEY'] = 'dev' 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    movies =Movie.query.all()
    app.config['SECRET_KEY'] = 'dev' 
    if request.method == 'POST': # 判断是否是 POST 请求
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
    # 获取表单数据
        title = request.form.get('title') # 传入表单对应输入字段的name值
        year = request.form.get('year')
    # 验证数据
        if not title or not year or len(year) > 4 or len(title)> 60:
            flash('Invalid input.') # 显示错误提示
            return redirect(url_for('index')) # 重定向回主页
            # 保存表单数据到数据库
        movie = Movie(title=title, year=year) # 创建记录
        db.session.add(movie) # 添加到数据库会话
        db.session.commit() # 提交数据库会话
        flash('Item created.') # 显示成功创建的提示
        return redirect(url_for('index')) # 重定向回主页
    return render_template('index.html',movies=movies)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required # 登录保护
def edit(movie_id):
    app.config['SECRET_KEY'] = 'dev' 
    movie=Movie.query.get_or_404(movie_id)
    if request.method == 'POST': # 判断是否是 POST 请求
    # 获取表单数据
        title = request.form.get('title') # 传入表单对应输入字段的name值
        year = request.form.get('year')
    # 验证数据
        if not title or not year or len(year) > 4 or len(title)> 60:
            flash('Invalid input.') # 显示错误提示
            return redirect(url_for('index')) # 重定向回主页
            # 保存表单数据到数据库
        movie = Movie(title=title, year=year) # 创建记录
        db.session.add(movie) # 添加到数据库会话
        db.session.commit() # 提交数据库会话
        flash('Item updated.') # 显示成功创建的提示
        return redirect(url_for('index')) # 重定向回主页
    return render_template('edit.html',movie=movie)
@app.route('/movie/delete/<int:movie_id>', methods=['POST']) #限定只接受 POST 请求
@login_required # 登录保护
def delete(movie_id):
    app.config['SECRET_KEY'] = 'dev' 
    movie = Movie.query.get_or_404(movie_id) # 获取电影记录
    db.session.delete(movie) # 删除对应的记录
    db.session.commit() # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))