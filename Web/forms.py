from flask_wtf import FlaskForm
from idna import unicode
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators, SelectField, IntegerField, RadioField,SelectMultipleField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email, email, ValidationError, InputRequired, number_range
# from Web.Database import User
#

class CreateFWInfo(FlaskForm):
    version = StringField('Version',
                           validators=[DataRequired()])
    typ = SelectField('FilterType',
                             choices=[('FW', 'FW'), ('UI', 'UI'), ('RCU', 'RCU')],validators=[DataRequired()])
    env = SelectField('FilterType',
                             choices=[('PROD', 'PROD'), ('LAB', 'LAB'), ('PROD/LAB', 'PROD/LAB')],validators=[DataRequired()])
    improv = StringField('Improvements',
                      validators=[DataRequired()])
    rn = FileField('Release Notes')
    ht = FileField('Headend test')
    submit = SubmitField('Create')

    #def validate_username(self, username):

     #   user = User.query.filter_by(username = username.data).first()
      #  if user:
       #     raise ValidationError('That username is taken. Please choose another')


class VODForm(FlaskForm):
    filter = StringField('Casn',validators=[DataRequired()])
    filtertype = SelectField('API Call',
                             choices=[('Nodes', 'Nodes'), ('Editorials', 'Editorials')],validators=[DataRequired()])

    submit = SubmitField('Call')


class AddMLAccForm(FlaskForm):
    accnum = StringField('Account Number',
                            validators=[DataRequired()])

    firstname = StringField('First Name',
                        validators=[DataRequired()])
    lastname = StringField('Last Name',
                        validators=[DataRequired()])
    pwd = StringField('Password',
                        validators=[DataRequired()])

    npvrprofile = SelectField('NPVRProfile',
                         choices=[('NPVR_SUSPENDED', 'NPVR_SUSPENDED'), ('NPVR_MEDIUM', 'NPVR_MEDIUM'),
                                  ('NPVR_UNLIMITED', 'NPVR_UNLIMITED'), ('NPVR_UNLIMITED', 'NPVR_UNLIMITED'),
                                  ('NPVR_DISABLED', 'NPVR_DISABLED'), ('NPVR_CANCELLED', 'NPVR_CANCELLED'),
                                  ('NPVR_SMALL', 'NPVR_SMALL'), ('NPVR_PLUS', 'NPVR_PLUS'),
                                  ('NPVR_SUPERIOR', 'NPVR_SUPERIOR'), ('NPVR_SUPERIORPLUS', 'NPVR_SUPERIORPLUS'),
                                  ('NPVR_MAX', 'NPVR_MAX'), ('NPVR_HEAVYUSER_PLUS', 'NPVR_HEAVYUSER_PLUS'),
                                  ('NPVR_HEAVYUSER_SUPERIOR', 'NPVR_HEAVYUSER_SUPERIOR')], validators=[DataRequired()])
    credlimit = StringField('Cred limit',
                      validators=[DataRequired()])

    submit = SubmitField('Create')


class AddSSPAccForm(FlaskForm):
    accid = StringField('Account ID',
                           validators=[DataRequired()])

    submit = SubmitField('Create')

    #def validate_username(self, username):

     #   user = User.query.filter_by(username = username.data).first()
      #  if user:
       #     raise ValidationError('That username is taken. Please choose another')


class AdddeviceForm(FlaskForm):
    ide = StringField('ID',
                           validators=[DataRequired()])
    casn = StringField('CaSN',
                           validators=[DataRequired()])
    account = StringField('AccountId',
                           validators=[DataRequired()])

    submit = SubmitField('Add Device')

    #def validate_username(self, username):

     #   user = User.query.filter_by(username = username.data).first()
      #  if user:
       #     raise ValidationError('That username is taken. Please choose another')


class AddMLdeviceForm(FlaskForm):
    casn = StringField('CaSN',
                           validators=[DataRequired(),Length(min=10),Length(max=10)])
    account = StringField('Account Number',
                           validators=[DataRequired()])

    submit = SubmitField('Add Device')

    #def validate_username(self, username):

     #   user = User.query.filter_by(username = username.data).first()
      #  if user:
       #     raise ValidationError('That username is taken. Please choose another')

#     def validate_email(self, correo):
#
#         user = User.query.filter_by(correo = correo).first()
#         if user:
#             return True
#

class DeviceForm(FlaskForm):
    filter= StringField('Filter')
    filtertype = SelectField('FilterType',
                             choices=[('CaSN', 'CaSN'), ('AccountId', 'AccountId')],validators=[DataRequired()])

class AccountMLForm(FlaskForm):
    filter= StringField('Filter')
    filtertype = SelectField('FilterType',
                             choices=[('CASN', 'CASN'), ('Acc Num', 'Acc Num')],validators=[DataRequired()])

#
# class InfoForm(FlaskForm):
#     nombre_empresa = StringField('Name',
#                        validators=[DataRequired(), Length(min=2, max=30)])
#     apellido = StringField('LastName',
#                            validators=[DataRequired(), Length(min=2, max=30)])
#     correo = StringField('Email',
#                         validators=[DataRequired()])
#     wtid = StringField('wtid',
#                        validators=[DataRequired()])
#     balance = StringField('balance')
#
#     submit = SubmitField('Edit')
#
class AddproductForm(FlaskForm):
    casn = StringField('CaSN',
                            validators=[DataRequired()])
    product = StringField('Product Id',
                            validators=[DataRequired()])
    producttype = SelectField('Product Type',
                             choices=[('SUBSCRIPTION', 'SUBSCRIPTION'), ('FREE', 'FREE'), ('TRANSACTIONAL', 'TRANSACTIONAL'), ('CAPABILITY', 'CAPABILITY')],validators=[DataRequired()])

    submit = SubmitField('Add')

#
# class NewInternetServiceForm(FlaskForm):
#     location_a = SelectField('Localidad A',
#                            choices=[('Norte', 'Norte'), ('Sur', 'Sur')],validators=[InputRequired()])
#     up_bw = IntegerField('Ancho de banda de subida (en Mb)',
#                              validators=[DataRequired(),number_range(1,200,"Ingrese un valor entre 1-200") ])
#     dw_bw = IntegerField('Ancho de banda de bajada (en Mb)',
#                         validators=[DataRequired(),number_range(1,200,"Ingrese un valor entre 1-200")])
#     submit = SubmitField('Crear')
#
class UpdateDeviceForm(FlaskForm):
    account= StringField('Actual device owner ',
                        validators=[DataRequired()])

    submit = SubmitField('Update')
