#
# from Web import db, login_manger
# from flask_login import UserMixin
#
# @login_manger.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
#
# class User(db.Model, UserMixin):
#     id_cliente= db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
#     nombre_empresa = db.Column(db.String(20), nullable=False)
#     rnc = db.Column(db.String(20), nullable=False)
#     direccion= db.Column(db.String(15), nullable=False)
#     correo = db.Column(db.String(20), nullable=False)
#     passw = db.Column(db.String(100), nullable=False)
#     telefono = db.Column(db.String(100), nullable=True)
#     createdon= db.Column(db.DateTime, nullable=True)
#
#     def __repr__(self):
#         return f"User('{self.id_cliente}','{self.nombre_empresa}','{self.rnc}',{self.direccion}, '{self.correo}', '{self.telefono}', '{self.createdon}')"
#
#
# class Servicio(db.Model):
#     id = db.Column(db.Integer, primary_key=True,unique=True, nullable=False)
#     id_cliente = db.Column(db.Integer, db.ForeignKey('user.id_cliente'), nullable=False)
#     tipo_servicio = db.Column(db.String(20), nullable=False)
#     location_a = db.Column(db.String(20), nullable=False)
#     location_b = db.Column(db.String(20), nullable=False)
#     up_bw = db.Column(db.Integer, nullable=False)
#     dw_bw = db.Column(db.Integer, nullable=False)
#     active = db.Column(db.Boolean, nullable=False)
#     in_progress = db.Column(db.Boolean, nullable=False)
#     createdon = db.Column(db.DateTime, nullable=True)
#     ip_loc_a = db.Column(db.String(50), nullable=False)
#     ip_loc_b = db.Column(db.String(50), nullable=False)
#
#     def __repr__(self):
#         return f"Service('{self.id}', '{self.id_cliente}','{self.tipo_servicio}', '{self.location_a}', '{self.location_b}', '{self.up_bw}', '{self.dw_bw}', '{self.active}', '{self.in_progress}', '{self.createdon}', '{self.ip_loc_a}', '{self.ip_loc_b}')"
#
# class Notificacion(db.Model):
#     id = db.Column(db.Integer, primary_key=True,unique=True, nullable=False)
#     id_servicio = db.Column(db.Integer, db.ForeignKey('servicio.id'), nullable=True)
#     tipo_not = db.Column(db.String(20), nullable=False)
#     des = db.Column(db.String(50), nullable=False)
#     checked = db.Column(db.Boolean, nullable=False)
#     fecha= db.Column(db.String(50), nullable=False)
#
#     def __repr__(self):
#         return f"Notificacion('{self.id}', '{self.id_servicio}','{self.tipo_not}', '{self.des}', '{self.checked}', '{self.fecha}')"
#
#
#
#
#
