from libros_app import app
from libros_app.controladores import controlador_autores,controlador_libros

if(__name__ == "__main__"):
    app.run(debug=True)