#import locale

from flask import request, session, g, redirect, url_for, abort, \
    render_template, flash, send_from_directory
from hedgehog import app
from hedgehog.model import User, db, Locality, Station, PhotoTimetable
from hedgehog.forms import RegisterForm, LoginForm, LocalitySearchForm,\
    LocalityCreateForm, StationCreateForm, PhotoTimetableAddForm, LocalityDeleteForm, \
    PhotoTimetableUploadForm

# File Uploading
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = app.root_path + "\\" + "static" + "\\" + "images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
# File Uploading end



    
#locale.setlocale(locale.LC_ALL, "")


@app.route('/', methods =['GET', 'POST'])
def show_main_page():
    form = LocalitySearchForm()
    if form.validate_on_submit():
        localities = Locality.query.filter_by(name=form.locality_name.data, deleted=False).all()
        if localities is None:
            pass
        elif len(localities) > 1:
            flash('Знайдено більше ніж один населений пункт з назвою "' + form.locality_name + '" в системі', 'error')
        elif len(localities) == 0:
            flash('Населений пункт "' + form.locality_name.data + '" не знайдено!', 'warning')
        else:
            return redirect(url_for('show_locality', locality_id = localities[0].id))
        pass    
    localitiesCounter = len(Locality.query.filter_by(deleted=False).filter(Locality.stations.any()).all())
    photoCounter = len(PhotoTimetable.query.all())
    localitiesPopular = Locality.query.filter_by(deleted=False).filter(Locality.stations.any()).\
        order_by(Locality.visit_counter.desc()).limit(10).all()
    #lastPhotoTimetables = PhotoTimetable.query.filter_by(deleted=False).order_by(PhotoTimetable.created_dt.desc()).limit(3)
    lastPhotoTimetables = db.session.query(Locality, Station, PhotoTimetable)\
        .join(Station).join(PhotoTimetable)\
        .order_by(PhotoTimetable.created_dt.desc()).limit(3).all()
    # current_user = User.query.get(session['user_id'])


    from sqlalchemy import func
    p_localities_if = db.session.query(Locality.name, Locality.id,
                                       func.count(PhotoTimetable.id).label("counted"))\
        .filter_by(region='Івано-Франківська', deleted=False)\
        .join(Station)\
        .join(PhotoTimetable)\
        .group_by(Locality.id)\
        .order_by(Locality.visit_counter.desc())\
        .limit(5)\
        .all()

    """
    p_localities_if = Locality.query.filter_by(deleted=False).filter(Locality.stations.any()).\
        filter_by(region='Івано-Франківська').order_by(Locality.visit_counter.desc()).limit(5).all()
    """
    p_localities_ch = db.session.query(Locality.name, Locality.id,
                                       func.count(PhotoTimetable.id).label("counted"))\
        .filter_by(region='Чернівецька', deleted=False)\
        .join(Station)\
        .join(PhotoTimetable)\
        .group_by(Locality.id)\
        .order_by(Locality.visit_counter.desc())\
        .limit(5)\
        .all()
    p_localities_zk = db.session.query(Locality.name, Locality.id,
                                       func.count(PhotoTimetable.id).label("counted"))\
        .filter_by(region='Закарпатська', deleted=False)\
        .join(Station)\
        .join(PhotoTimetable)\
        .group_by(Locality.id)\
        .order_by(Locality.visit_counter.desc())\
        .limit(5)\
        .all()
    p_localities_lv = db.session.query(Locality.name, Locality.id,
                                       func.count(PhotoTimetable.id).label("counted"))\
        .filter_by(region='Львівська', deleted=False)\
        .join(Station)\
        .join(PhotoTimetable)\
        .group_by(Locality.id)\
        .order_by(Locality.visit_counter.desc())\
        .limit(5)\
        .all()

    return render_template("main_page.html", photoCounter=photoCounter,
                localitiesCounter = localitiesCounter,
                p_localities_if = p_localities_if,
                p_localities_ch = p_localities_ch,
                p_localities_zk = p_localities_zk,
                p_localities_lv = p_localities_lv,
                lastPhotos = lastPhotoTimetables,
                form = form)


@app.route('/stations')
def show_stations():
    stations = Station.query.filter_by(deleted=False).all()
    return render_template("show_stations.html", stations=stations)


@app.route('/stations/add', methods=['GET','POST'])
def add_station():
    form = StationCreateForm()
        
    localities = Locality.query.filter_by(deleted=False).all()
    form.locality_id.choices = [(local.id, local.name) for local in Locality.query.order_by('name').all()]

    
    target_locality_id = request.args.get('locality', None)
    if target_locality_id is not None:
        try:
            locality_id_int = int(target_locality_id)
            if locality_id_int > 9223372036854775807:
                raise ValueError
        except ValueError:
            locality_id_int = None
        if locality_id_int is not None:
            #t_local = Locality.query.filter_by(id=locality_id_int).one()
            if Locality.query.get(locality_id_int) is not None:
                form.locality_id.default=int(target_locality_id)
                if request.method == 'GET':
                    form.process()        
    
    print("Before validation")
    if form.validate_on_submit():
        print('Validated!!!!')
        new_station = Station(form.name.data, form.locality_id.data)
        db.session.add(new_station)
        db.session.commit()
        flash('Автостанція/зупинка в населеному пункті додана', 'success')
    print("After validation")
    return render_template('add_station.html', form=form, localities=localities)

"""

def old_show_stations():
    db = get_db()
    cur = db.execute('select * from stations order by name asc')
    stations = cur.fetchall()
    return render_template("show_stations.html", stations=stations)
"""


"""
@app.route('/station/<station_id>')
def show_station(station_id):
    db = get_db()
    cur = db.execute('select * from photo_schedule WHERE station_id = ? ', (station_id,))
    schedules = cur.fetchall()
    
    
    return render_template("show_station.html", schedules=schedules, station_id=station_id)

"""


@app.route('/stations/<station_id>/edit')
def edit_station(station_id):
    try:
        station = Station.query.get(station_id)
        if station is None or station.deleted:
            abort(404)
    except OverflowError:
        abort(404)

    form = StationCreateForm(obj=station)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(station)
        station.save()
        return redirect(url_for("show_locality",locality_id=station.locality_id))
    #print(form.region.data)
    return render_template('add_station.html', form = form)




"""
@app.route('/photo_schedules/add', methods=['GET','POST'])
def add_photo_schedule():
    if request.method == 'POST':
        print('Received post photo request.')
        db = get_db()
        cur = db.execute('select id from towns WHERE name = ? ', (request.form['townName'],))
        print("Stage 1 pass")
        towns = cur.fetchall();
        print("Stage 1,4 pass")
        if len(towns) != 1:
            print("duplicates")
            return "Multiple towns with the same name"        
        print("Stage 2 pass")
        db.execute('insert into photo_schedule(town_id, image_link, user_comment) values(?, ?, ?)',
        [towns[0][0],request.form['imageLink'],request.form['userComment']])
        print("Stage 3 pass")
        db.commit()

        flash('Фото розкладу успішно додане')
        return redirect(url_for('show_main_page'))
    return render_template('add_new_photo_schedule.html')
"""
@app.route('/about')
def about_page():
    return  render_template('about.html')

    
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
    
    
    
    
    
    
    
    
@app.route('/localities')
def show_localities():
    localities = Locality.query.filter_by(deleted=False).filter(Locality.stations.any()).order_by(Locality.name).all()
    return render_template('localities.html', localities = localities)

@app.route('/localities/add', methods = ['GET','POST'])
def add_locality():
    form = LocalityCreateForm()
    if form.validate_on_submit():
        if Locality.query.filter_by(name=form.name.data, deleted=False).first() is None:
            new_locality = Locality(form.name.data)
            form.populate_obj(new_locality)
            new_locality.save()
            db.session.add(Station("зупинка", new_locality.id))
            db.session.commit()
            flash('Населений пункт "' + form.name.data + '" додано', 'success')
        else:
            flash('Населений пункт вже є в системі', 'error')
    return render_template('add_locality.html', form = form)


@app.route('/localities/<int:locality_id>')
def show_locality(locality_id):    
    locality = Locality.query.get(locality_id)

    if locality.deleted:
        return abort(404)

#   Register visit
    if locality.visit_counter is not None:
        locality.visit_counter += 1
    else:
        locality.visit_counter = 1

    db.session.commit()

    return render_template('locality.html', locality = locality)
@app.route('/localities/<int:locality_id>/edit', methods=['GET', 'POST'])
def edit_locality(locality_id):
    try:
        locality = Locality.query.get(locality_id)
        if locality is None or locality.deleted:
            abort(404)
    except OverflowError:
        pass

    form = LocalityCreateForm(obj=locality)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(locality)
        locality.save()
        return redirect(url_for("show_locality",locality_id=locality.id))
    #print(form.region.data)
    return render_template('add_locality.html', form = form)


@app.route('/localities/<int:locality_id>/delete', methods=['GET', 'POST'])
def delete_locality(locality_id):
    try:
        locality = Locality.query.get(locality_id)
    except OverflowError:
        pass
    if locality is None or locality.deleted:
        abort(404)

    form = LocalityDeleteForm()

    if request.method == 'POST' and form.validate_on_submit():
        locality.delete()
        locality.save()
        flash("Населений пункт '" + locality.name + "' видалено з системи!", "warning")
        return redirect(url_for("show_main_page"))
    else:
        return render_template("delete_locality.html", form=form, locality=locality)


@app.route('/timetables')
def show_photo_timetables():
    return "List of timetables"

def get_extension(filename):
	ext = ""
	dot_place = filename.find('.',len(filename) - 4)
	if dot_place > 0:
	    ext = filename[dot_place:len(filename)]
	return ext


@app.route('/timetables/upload', methods=['GET','POST'])
def upload_photo_timetable():
    form = PhotoTimetableUploadForm()

    stations = Station.query.filter_by(deleted=False).all()

    unsorted_list = [( st.id, st.name, Locality.query.get(st.locality_id).name) for st in stations]
    sorted_by_locality = sorted(unsorted_list, key = lambda tup: tup[2])
    station_choices = [(ch[0], ch[2] + ", " + ch[1]) for ch in sorted_by_locality]


    form.station_id.choices = station_choices
    if form.validate_on_submit():


        import uuid
        unique_filename = str(uuid.uuid4()) + get_extension(form.file.data.filename)


        form.file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
        photo = PhotoTimetable(form.station_id.data, "/uploads/" + unique_filename, form.comment.data)
        db.session.add(photo)
        db.session.commit()
        flash("Фото розкладу успішно додано!", 'success')
        target_station = Station.query.get(form.station_id.data)

        return redirect(url_for("show_locality", locality_id=target_station.locality_id))


    return render_template('upload_photo_timetable.html', form=form)

@app.route('/timetables/add', methods=['GET', 'POST'])
def add_photo_timetable():
    form = PhotoTimetableAddForm()
    stations = Station.query.filter_by(deleted=False).all()

    unsorted_list = [( st.id, st.name, Locality.query.get(st.locality_id).name) for st in stations]
    sorted_by_locality = sorted(unsorted_list, key = lambda tup: tup[2])
    station_choices = [(ch[0], ch[2] + ", " + ch[1]) for ch in sorted_by_locality]
    
    
    form.station_id.choices = station_choices#[( st.id, st.name + ", " + Locality.query.get(st.locality_id).name) for st in stations]
    if form.validate_on_submit():
        photo = PhotoTimetable(form.station_id.data, form.image_url.data, form.comment.data)
        db.session.add(photo)
        db.session.commit()
        flash("Фото розкладу успішно додано!", 'success')
        target_station = Station.query.get(form.station_id.data)
        
        return redirect(url_for("show_locality", locality_id=target_station.locality_id))
    return render_template("add_photo_timetable.html", form=form)
    
@app.route('/timetables/<int:photo_timetable_id>')
def show_photo_timetable(photo_timetable_id):
    return "Timetable " + str(photo_timetable_id)

    
"""
/localities/add
/localities/<int:id>/edit
/localities/<int:id>/delete
"""    
    
    
    
    
#################################


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is not None:
            if user.check_password(form.password.data):
                session['logged_in'] = True    
                session['user_id'] = user.id                
                flash("Доброго дня," + form.username.data + "! Ви успішно увійшли в систему.", 'success')
                return redirect(url_for('show_main_page'))
            else:
                flash("Не вірний пароль!", 'warning')
        else:
            flash("Користувач з іменем," + form.username.data + " не зареєстрований в системі.", 'error')    
                
    return render_template("login.html",
                        form = form)




def old_ogin():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True            
            flash('Congratulations! You are loged in!')
            return redirect(url_for('show_main_page'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You were logged out!', 'warning')
    return redirect(url_for('show_main_page'))
    
    
@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()
    
    if form.validate_on_submit():
                
        username_duplicate = User.query.filter_by(username=form.username.data).first()
        email_duplicate = User.query.filter_by(email=form.email.data).first()
                
        if username_duplicate is not None:
            flash("Користувач з таким іменем вже зареєстрований в системі. ", 'error')
        elif email_duplicate is not None:
            flash("Користувач з такою електронною поштою вже зареєстрований в системі. ", 'error')
        else:            
            
            new_user = User(form.username.data,form.email.data,form.password.data)
                
            
            db.session.add(new_user)
            db.session.commit()
            flash('Hello,' + form.username.data + ", your account is created!", 'success')
            return redirect(url_for('show_main_page'))

    return render_template('register.html',
                    form = form)