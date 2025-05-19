from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload

DB_NAME = "tarea 2"
DB_USERNAME = "cc5002" #cc5002
DB_PASSWORD = "programacionweb" #programacionweb
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"   

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# Clases

class actividad(Base):
    __tablename__ = "actividad"
    id = Column(Integer, primary_key=True, autoincrement=True)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100), nullable=True)
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=True)
    dia_hora_inicio = Column(DateTime, nullable=False)
    dia_hora_termino = Column(DateTime, nullable=True)
    descripcion = Column(String(500), nullable=True)

    comuna = relationship("comuna", back_populates="actividades")
    fotos = relationship("foto", back_populates="actividad")
    contactos = relationship("contactar_por", back_populates="actividad")
    temas = relationship("actividad_tema", back_populates="actividad")

class actividad_tema(Base):
    __tablename__ = "actividad_tema"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tema = Column(Enum('música', 'deporte', 'ciencias', 'religión', 'política', 'tecnología', 'juegos', 'baile', 'comida', 'otro'), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)
    tema_id = Column(Integer, ForeignKey('tema.id'), nullable=False)

    actividad = relationship("actividad", back_populates="temas")

class comuna(Base):
    __tablename__ = "comuna"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

    region = relationship("region", back_populates="comunas")
    actividades = relationship("actividad", back_populates="comuna")

class contactar_por(Base):
    __tablename__ = "contactar_por"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=True)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

    actividad = relationship("actividad", back_populates="contactos")

class foto(Base):
    __tablename__ = "foto"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

    actividad = relationship("actividad", back_populates="fotos")

class region(Base):
    __tablename__ = "region"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    comunas = relationship("comuna", back_populates="region")


#Funciones

#---Actividad---
def crear_actividad(comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion):
    session = SessionLocal()
    nueva_actividad = actividad(
        comuna_id=comuna_id,
        sector=sector,
        nombre=nombre,
        email=email,
        celular=celular,
        dia_hora_inicio=dia_hora_inicio,
        dia_hora_termino=dia_hora_termino,
        descripcion=descripcion
    )
    session.add(nueva_actividad)
    session.commit()
    session.close()

def get_all_actividades():
    session = SessionLocal()
    actividades = session.query(actividad).options(
        joinedload(actividad.comuna),
        joinedload(actividad.temas),
        joinedload(actividad.fotos)).all()
    session.close()
    return actividades

def get_activity(comuna_id, sector, nombre, dia_hora_inicio):
    session = SessionLocal()
    actividad = session.query(actividad).filter_by(
        comuna_id=comuna_id, 
        sector=sector, 
        nombre=nombre,
        dia_hora_inicio=dia_hora_inicio
    ).first()
    session.close()
    return actividad

#---Actividad_tema---

def crear_tema(tema, glosa_otro, actividad_id):
    session = SessionLocal()
    nueva_actividad_tema = actividad_tema(
        tema=tema, 
        glosa_otro=glosa_otro, 
        actividad_id=actividad_id
    )
    session.add(nueva_actividad_tema)
    session.commit()
    session.close()

# ---Comuna---
def crear_comuna(nombre, region_id):
    session = SessionLocal()
    nueva_comuna = comuna(
        nombre=nombre,
        region_id=region_id
    )
    session.add(nueva_comuna)
    session.commit()
    session.close()

# ---Contactar por ---

def crear_contactar_por(nombre, identificador, actividad_id):
    session = SessionLocal()
    nuevo_contacto_por = contactar_por(
        nombre=nombre,
        identificador=identificador,
        actividad_id=actividad_id
    )
    session.add(nuevo_contacto_por)
    session.commit()
    session.close()

# ---Fotos---

def crear_foto(ruta_archivo, nombre_archivo, actividad_id):
    session = SessionLocal()
    nueva_foto = foto(
        ruta_archivo=ruta_archivo,
        nombre_archivo=nombre_archivo,
        actividad_id=actividad_id,
    )
    session.add(nueva_foto)
    session.commit()
    session.close()

# ---Región ---
def get_region_by_id(region_id):
    session = SessionLocal()
    region =session.query(region).filter(region.id == region_id).first()
    session.close()
    return region

def crear_region(nombre):
    session = SessionLocal()
    nueva_region = region(nombre=nombre)
    session.add(nueva_region)
    session.commit()
    session.close()



