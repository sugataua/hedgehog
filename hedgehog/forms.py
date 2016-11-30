from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import TextField, PasswordField, SelectField, StringField, DecimalField, RadioField,BooleanField
from wtforms.fields.html5 import EmailField 
from wtforms.validators import Required, DataRequired
from wtforms.widgets import TextArea
from hedgehog.model import MODE_BUS, MODE_TRAIN, TYPE_STOP, TYPE_STATION


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[Required()])
    email = EmailField('email', validators=[Required()])
    password = PasswordField('password', validators=[Required()])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])    
    

class LocalitySearchForm(FlaskForm):
    locality_name = StringField('locality_name', validators=[Required()])
    
class LocalityCreateForm(FlaskForm):
    name = StringField('locality_name', validators=[DataRequired()])
    region = SelectField('region',
                         choices=[('Закарпатська', 'Закарпатська'),
                                  ('Чернівецька', 'Чернівецька'),
                                  ('Івано-Франківська', 'Івано-Франківська'),
                                  ('Львівська', 'Львівська')],
                         validators=[DataRequired()])
    district = StringField('district', validators=[DataRequired()])
    locality_type = SelectField('type',
                                choices=[('н.п.', 'населений пункт'),
                                         ('с.', 'село'),
                                         ('с-ще', 'селище'),
                                         ('смт', 'селище міського типу'),
                                         ('м', 'місто')],
                                validators=[DataRequired()])

    coordinate_lat = DecimalField('coordinate_lat',validators=[DataRequired()])
    coordinate_lon = DecimalField('coordinate_lon', validators=[DataRequired()])


class LocalityEditForm(FlaskForm):
    locality_name = StringField('locality_name', validators=[Required()])


class LocalityDeleteForm(FlaskForm):
    pass

    
class StationCreateForm(FlaskForm):
    name = StringField('Назва', validators=[DataRequired()])
    locality_id = SelectField('Населений пункт', coerce=int, validators=[DataRequired()])
    transport_mode = RadioField('Вид транспорту',
                                choices=[(MODE_BUS,'Автобус'),
                                         (MODE_TRAIN,'Залізниця')],
                                default=MODE_BUS,
                                coerce=int)
    station_type = RadioField('Тип',
                                choices=[(TYPE_STOP,'Зупинка'),
                                         (TYPE_STATION,'Станція')],
                                default=TYPE_STOP,
                                coerce=int)
    luggage_storage = BooleanField('Камери схову багажу')
    toilet = BooleanField('Туалет')
    ticket_office = BooleanField('Квиткові каси')

    address = StringField('Адреса')
    phone_number = StringField('Номер телефону')
    
    
class PhotoTimetableAddForm(FlaskForm):
    station_id = SelectField('station', coerce=int)
    image_url = StringField('image_url', validators=[DataRequired()])
    comment = StringField('comment', widget=TextArea())


class PhotoTimetableUploadForm(FlaskForm):
    station_id = SelectField('station', coerce=int)
    file = FileField("Фото розкладу", validators=[
        FileRequired()#,
        #FileAllowed(['jpg', 'png', 'jpeg', 'gif'], "Лише зображення у форматах 'jpg', 'png', 'jpeg' та 'gif'")
    ])
    comment = StringField('comment', widget=TextArea())



