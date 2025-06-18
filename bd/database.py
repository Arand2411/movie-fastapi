import os  # Módulo para interactuar con el sistema operativo, ideal para manejo de rutas.
from sqlalchemy import create_engine  # Función para configurar la conexión a la base de datos :contentReference[oaicite:1]{index=1}
from sqlalchemy.orm.session import sessionmaker  # Fábrica de sesiones para manejar transacciones ORM :contentReference[oaicite:2]{index=2}
from sqlalchemy.ext.declarative import declarative_base  # Genera una clase base para definir modelos declarativamente :contentReference[oaicite:3]{index=3}

# Nombre del archivo SQLite donde se almacenarán los datos
sqliteName = 'movies.sqlite'

# Directorio donde se encuentra este script, para construir rutas absolutas de manera segura
base_dir = os.path.dirname(os.path.realpath(__file__))

# Construcción de la URL de conexión para SQLite. 
databaseUrl = f"sqlite:///{os.path.join(base_dir, sqliteName)}"

# Crea el engine, que gestiona la conexión y el pool. echo=True activa el registro de sentencias SQL en consola :contentReference[oaicite:4]{index=4}
engine = create_engine(databaseUrl, echo=True)

# Crea una clase Session configurada para usar este engine. Se utiliza para abrir sesiones transaccionales :contentReference[oaicite:5]{index=5}
Session = sessionmaker(bind=engine)

# Base es la clase desde la cual heredan los modelos ORM; contiene metadatos de las tablas :contentReference[oaicite:6]{index=6}
Base = declarative_base()
