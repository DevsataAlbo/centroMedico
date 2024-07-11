from flask import Blueprint, request, jsonify
from models import db, Usuario, Horario

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = Usuario(
        nombre=data['nombre'],
        apellido=data['apellido'],
        rut=data['rut'],
        fecha_nacimiento=data['fecha_nacimiento'],
        nacionalidad=data['nacionalidad'],
        perfil=data['perfil'],
        especialidad=data.get('especialidad'),
        sexo=data['sexo'],
        direccion=data['direccion'],
        comuna=data['comuna'],
        telefono=data.get('telefono'),
        email=data['email'],
        comentarios=data.get('comentarios')
    )
    db.session.add(new_user)
    db.session.commit()

    # Guardar horarios
    for horario in data['horarios']:
        new_horario = Horario(
            usuario_id=new_user.id,
            dia=horario['dia'],
            hora_inicio=horario['hora_inicio'],
            hora_fin=horario['hora_fin']
        )
        db.session.add(new_horario)
    
    db.session.commit()
    return jsonify({'message': 'Usuario creado exitosamente'}), 201

@user_bp.route('/list', methods=['GET'])
def list_users():
    users = Usuario.query.all()
    user_list = [{
        'id': user.id,
        'nombre': user.nombre,
        'apellido': user.apellido,
        'rut': user.rut,
        'fecha_nacimiento': str(user.fecha_nacimiento),
        'nacionalidad': user.nacionalidad,
        'perfil': user.perfil,
        'especialidad': user.especialidad,
        'sexo': user.sexo,
        'direccion': user.direccion,
        'comuna': user.comuna,
        'telefono': user.telefono,
        'email': user.email,
        'fecha_creacion': str(user.fecha_creacion),
        'comentarios': user.comentarios
    } for user in users]
    return jsonify(user_list), 200

@user_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = Usuario.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
