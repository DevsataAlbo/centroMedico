from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Comuna(db.Model):
    __tablename__ = 'comunas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    rut = db.Column(db.String(12), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    nacionalidad = db.Column(db.String(50), nullable=False)
    especialidad = db.Column(db.String(50))
    sexo = db.Column(db.String(10), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    comuna_id = db.Column(db.Integer, db.ForeignKey('comunas.id'))
    comuna = db.relationship('Comuna', backref=db.backref('usuarios', lazy=True))
    imagen_perfil = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())

class Horario(db.Model):
    __tablename__ = 'horarios'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    dia = db.Column(db.String(10), nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('horarios', lazy=True))

class Administrativo(db.Model):
    __tablename__ = 'administrativos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('administrativos', uselist=False))
    puesto = db.Column(db.String(50))

class Profesional(db.Model):
    __tablename__ = 'profesionales'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('profesionales', uselist=False))
    especialidad = db.Column(db.String(50))

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('pacientes', uselist=False))
    historial_medico = db.Column(db.Text)
