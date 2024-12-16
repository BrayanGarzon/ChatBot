from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.String(80), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=True)
    cedula = db.Column(db.String(50), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    interes = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Usuario {self.nombre}>"
