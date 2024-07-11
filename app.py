from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from config import Config
from models import db, Usuario, Horario, Comuna, Administrativo, Profesional, Paciente
from routes.user_routes import user_bp
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'supersecretkey'  # Necesario para usar mensajes flash

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

app.register_blueprint(user_bp, url_prefix='/users')

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear el directorio de carga si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    users = Usuario.query.all()
    return render_template('dashboard.html', users=users)

@app.route('/dashboard-my-listings')
def dashboard_my_listings():
    users = Usuario.query.all()
    return render_template('dashboard-my-listings.html', users=users)

@app.route('/dashboard-add-listing', methods=['GET', 'POST'])
def dashboard_add_listing():
    if request.method == 'POST':
        data = request.form.to_dict()
        horarios = []
        dias_validos = {
            'lunes': 'Lunes',
            'martes': 'Martes',
            'miercoles': 'Miercoles',
            'jueves': 'Jueves',
            'viernes': 'Viernes',
            'sabado': 'Sabado',
            'domingo': 'Domingo'
        }
        for day in dias_validos.keys():
            inicio = request.form.get(f'horario_{day}_inicio')
            fin = request.form.get(f'horario_{day}_fin')
            if inicio and fin:
                horarios.append({'dia': dias_validos[day], 'hora_inicio': inicio, 'hora_fin': fin})

        imagen_perfil = request.files['imagen_perfil']
        if imagen_perfil:
            filename = secure_filename(imagen_perfil.filename)
            imagen_perfil.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imagen_perfil_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            imagen_perfil_url = None

        # Verificar si el rut ya existe
        if Usuario.query.filter_by(rut=data['rut']).first():
            flash("El RUT ya existe", "error")
            return redirect(url_for('dashboard_add_listing'))

        # Verificar si el email ya existe
        if Usuario.query.filter_by(email=data['email']).first():
            flash("El Email ya existe", "error")
            return redirect(url_for('dashboard_add_listing'))

        comuna_id = int(data['comuna'])
        comuna = db.session.get(Comuna, comuna_id)
        if not comuna:
            flash("Comuna no valida", "error")
            return redirect(url_for('dashboard_add_listing'))

        new_user = Usuario(
            nombre=data['nombre'],
            apellido=data['apellido'],
            rut=data['rut'],
            fecha_nacimiento=data['fecha_nacimiento'],
            nacionalidad=data['nacionalidad'],
            especialidad=data.get('especialidad'),
            sexo=data['sexo'],
            direccion=data['direccion'],
            comuna_id=comuna_id,
            imagen_perfil=imagen_perfil_url,
            telefono=data.get('telefono'),
            email=data['email']
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            flash("Error al agregar el usuario: " + str(e.orig), "error")
            return redirect(url_for('dashboard_add_listing'))

        # Guardar horarios
        try:
            for horario in horarios:
                new_horario = Horario(
                    usuario_id=new_user.id,
                    dia=horario['dia'],
                    hora_inicio=horario['hora_inicio'],
                    hora_fin=horario['hora_fin']
                )
                db.session.add(new_horario)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            flash("Error al agregar el horario: " + str(e.orig), "error")
            return redirect(url_for('dashboard_add_listing'))

        # Crear registros en tablas específicas según el perfil
        perfil = data.get('perfil')
        try:
            if perfil == 'Administrativo':
                new_administrativo = Administrativo(
                    usuario_id=new_user.id,
                    puesto=data.get('puesto')
                )
                db.session.add(new_administrativo)
            elif perfil == 'Profesional':
                new_profesional = Profesional(
                    usuario_id=new_user.id,
                    especialidad=data.get('especialidad')
                )
                db.session.add(new_profesional)
            elif perfil == 'Paciente':
                new_paciente = Paciente(
                    usuario_id=new_user.id,
                    historial_medico=data.get('historial_medico')
                )
                db.session.add(new_paciente)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            flash("Error al agregar datos del perfil: " + str(e.orig), "error")
            return redirect(url_for('dashboard_add_listing'))

        flash("Usuario agregado exitosamente", "success")
        return redirect(url_for('dashboard'))
    return render_template('dashboard-add-listing.html')

@app.route('/dashboard-my-profile')
def dashboard_my_profile():
    return render_template('dashboard-my-profile.html')

@app.route('/pages-user-profile')
def pages_user_profile():
    return render_template('pages-user-profile.html')

@app.route('/pages-404')
def pages_404():
    return render_template('pages-404.html')

if __name__ == '__main__':
    app.run(debug=True)
