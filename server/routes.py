from server import app, login, db
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from server.forms import LoginForm, CompanyForm, OrderForm, ArticleForm
from server.models import User, Company, Order, Article


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return render_template('index.html', form=form)
        else:
            return redirect(url_for('landing_page'))
    elif form.validate_on_submit():
        print(form.username.data)
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return jsonify({'message': 'Invalid password or username'})
        login_user(user)
        return redirect(url_for('landing_page'))


@app.route('/landing_page', methods=['GET'])
@login_required
def landing_page():
    articles = Article.query.filter_by(author_id=current_user.id).order_by(Article.timestamp.desc()).all()
    total_time = 0
    for a in articles:
        total_time += a.time
    return render_template('landing_page.html', articles=articles, total_time=total_time)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
@app.route('/add_company', methods=['GET', 'POST'])
def add_company():
    form = CompanyForm()
    if request.method == 'GET':
        return render_template('add_company.html', form=form)
    else:
        if form.validate_on_submit():
            company = Company(name=form.company_name.data)
            db.session.add(company)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return jsonify({'message': 'Something went wrong'})


@login_required
@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    form = OrderForm()
    companies = db.session.query(Company).all()
    company_names = [(i.id, i.name) for i in companies]
    form.company.choices = company_names
    if form.validate_on_submit():
        order = Order(company_id=form.company.data, reference=form.order_reference.data)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('add_order.html', form=form)


@login_required
@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    form = ArticleForm()
    orders = db.session.query(Order).all()
    order_refs = [(i.id, f"{i.reference} ({i.get_company_name()})") for i in orders]
    form.order.choices = order_refs
    if form.validate_on_submit():
        article = Article(time=form.time.data, author_id=current_user.id, order_id=form.order.data)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('add_article.html', form=form)


@login_required
@app.route('/company_overview')
def company_overview():
    companies = Company.query.order_by(Company.name.desc()).all()
    total_time = 0
    for c in companies:
        total_time += c.calc_time()
    return render_template('company_overview.html', companies=companies, total_time=total_time)


@login_required
@app.route('/company_overview/<int:company_id>')
def single_company_overview(company_id):
    company = Company.query.filter_by(id=company_id).first()
    orders = Order.query.filter_by(company_id=company_id).all()
    num_orders = len(orders)
    return render_template('single_company_overview.html', orders=orders, company=company, num_orders=num_orders)


@login_required
@app.route('/order_overview')
def order_overview():
    orders = Order.query.all()
    total_time = 0
    for o in orders:
        total_time += o.calc_time()
    return render_template('order_overview.html', orders=orders, total_time=total_time)


@login_required
@app.route('/order_overview/<int:order_id>')
def single_order_overview(order_id):
    order = Order.query.filter_by(id=order_id).first()
    articles = Article.query.filter_by(order_id=order_id).order_by(Article.timestamp.desc()).all()
    return render_template('single_order_overview.html', order=order, articles=articles)


@login_required
@app.route('/article_overview/<int:article_id>')
def article_overview(article_id):
    article = Article.query.filter_by(id=article_id).first()
    order = Order.query.filter_by(id=article.order_id).first()
    return render_template('article_overview.html', article=article, order=order)
