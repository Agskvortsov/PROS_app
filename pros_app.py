import datetime
from flask import Flask, request, render_template, redirect, flash, url_for, \
                    session
from passlib.hash import sha256_crypt
from models.models import ParkingModel, RentalModel, UserModel
from forms.forms import ParkingForm, RentalForm, RegisterForm, LoginForm
from functools import wraps




app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['POST_PER_PAGE'] = 5
app.secret_key = 'Alex'



def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/add_parking', methods=('GET', 'POST'))
@is_logged_in
def add_new_parking():
    form = ParkingForm(request.form)

    if form.validate_on_submit():
        name = request.form['name']
        address = request.form['address']
        price = request.form['price']
        parking = ParkingModel(name, address, price)
        parking.save_to_db()
        flash(f'Parking {name} was sucsesfully created!')
        return redirect(url_for('add_new_parking'))
    return render_template('new_parking.html', form=form)


@app.route('/parkings/<string:name>')
def parkig_detail(name):
    parking = ParkingModel.find_by_name(name)
    return render_template('parking_detail.html', parking=parking)


@app.route('/parkings/update/<string:name>', methods=('GET', 'POST'))
def parking_update(name):
    parking = ParkingModel.find_by_name(name)
    form = ParkingForm(**parking.json())

    if request.method == 'GET':
        return render_template('update.html', form=form, name1=name)
    else:
        parking.name = request.form['name']
        parking.address = request.form['address']
        parking.price = request.form['price']
        parking.update()
        flash(f'Parking {parking.name} was sucsesfully updated!')
        return redirect(url_for('parkig_detail', name=parking.name))


@app.route('/parkings/delete/<string:name>')
def delete_parking(name):
    parking = ParkingModel.find_by_name(name)
    parking.delete_from_db()
    flash(f'Parking {parking.name} was sucsesfully deleted!')
    return redirect(url_for('parkings_list'))


@app.route('/parkings')
def parkings_list():
    page = request.args.get('page', 1, type=int)
    parkings_list = ParkingModel.parking_list(page)
    next_url = url_for('parkings_list', page=parkings_list.next_num) \
                if parkings_list.has_next else None
    prev_url = url_for('parkings_list', page=parkings_list.prev_num) \
                if parkings_list.has_prev else None
    paginator = parkings_list.iter_pages(left_edge=2, left_current=2,
                                        right_current=5, right_edge=2)
    return render_template('parking_list.html', parkings_list=parkings_list,
                            paginator=paginator, next_url=next_url,
                            prev_url=prev_url)


@app.route('/add_rental', methods=('GET', 'POST'))
def add_new_rental():
    form = RentalForm(request.form)

    if form.validate_on_submit():
        parking = ParkingModel.find_by_name(request.form['parking_name'])
        pythonic_date = [int(x) for x in request.form['beg_date'].split('-')]
        beg_date = datetime.datetime(*pythonic_date)
        price = request.form['price']
        renter_name = request.form['renter_name']
        renter_mob_num = request.form['renter_mob_num']
        rental = RentalModel(beg_date, price, renter_name, renter_mob_num,
                            parking.id)
        rental.save_to_db()
        flash(f'Rental of parking {parking.name} was sucsesfully created!')
        return redirect(url_for('parkings_list'))
    return render_template('new_rental.html', form=form)


@app.route('/rental/<int:id>')
def rental_detail(id):
    rental = RentalModel.find_by_id(id)
    parking_name = ParkingModel.find_by_id(rental.parking_id)
    return render_template('rental_detail.html', rental=rental,
                            parking_name=parking_name.name)


@app.route('/rentals')
def rentals_list():
    page = request.args.get('page', 1, type=int)
    rentals_list = RentalModel.rental_list(page)
    next_url = url_for('rentals_list', page=rentals_list.next_num) \
                if rentals_list.has_next else None
    prev_url = url_for('rentals_list', page=rentals_list.prev_num) \
                if rentals_list.has_prev else None
    paginator = rentals_list.iter_pages(left_edge=2, left_current=2,
                                        right_current=5, right_edge=2)
    return render_template('rentals_list.html', rentals_list=rentals_list,
                            paginator=paginator, next_url=next_url,
                            prev_url=prev_url)


@app.route('/active-rentals')
def active_rentals_list():
    page = request.args.get('page', 1, type=int)
    rentals_list = RentalModel.list_of_active_rentals(page)
    next_url = url_for('rentals_list', page=rentals_list.next_num) \
                if rentals_list.has_next else None
    prev_url = url_for('rentals_list', page=rentals_list.prev_num) \
                if rentals_list.has_prev else None
    paginator = rentals_list.iter_pages(left_edge=2, left_current=2,
                                        right_current=5, right_edge=2)
    return render_template('rentals_list.html', rentals_list=rentals_list,
                            paginator=paginator, next_url=next_url,
                            prev_url=prev_url)


@app.route('/rentals/update/<int:id>', methods=('GET', 'POST'))
def rental_update(id):
    rental = RentalModel.find_by_id(id)
    parking = ParkingModel.find_by_id(rental.parking_id)
    form = RentalForm(**rental.json(), parking_name=parking.name)
    if request.method == 'GET':
        return render_template('rental_update.html', form=form, id=id)
    else:
        pythonic_date = [int(x) for x in request.form['beg_date'].split('-')]
        beg_date = datetime.datetime(*pythonic_date)
        rental.beg_date = beg_date
        rental.price = request.form['price']
        rental.renter_name = request.form['renter_name']
        rental.renter_mob_num = request.form['renter_mob_num']
        rental.update()
        flash(f'Rental of parking - {parking.name} was sucsesfully updated!')
        return redirect(url_for('rental_detail', id=rental.id))


@app.route('/renters')
def renters_list():
    renters = RentalModel.renters_list()
    return render_template('renters_list.html', renters=renters)


@app.route('/add_user', methods=('GET', 'POST'))
def add_user():
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        user = UserModel(username, password)
        user.save_to_db()
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        user = UserModel.find_by_username(username)
        if user:
            password = user.password
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('parkings_list'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error, form=form)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html', form=form)


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=8000, debug=True)
