import sys
path = '/home/tuusuario/mi_app'  # Cambiará al subir a PythonAnywhere
if path not in sys.path:
    sys.path.append(path)

from app import app as application