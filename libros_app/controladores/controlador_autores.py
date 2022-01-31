from flask import render_template, request,redirect
from libros_app import app
from libros_app.modelos.modelo_autor import Autor
from libros_app.modelos.modelo_libro import Libro

@app.route("/", methods=["GET"])
def index(): 
    return redirect("/authors")

@app.route("/authors", methods=["GET"])
def paginaAutores():
    autores = Autor.obtenerAutores()
    return render_template("autores.html", autores= autores)

@app.route("/authors/create", methods=["POST"])
def agregarAutor():
    autor ={
        "nombre": request.form["nombre"]
    }
    resultado = Autor.crearAutor(autor)
    if(type(resultado) is bool and not resultado):
        print("Algo salio mal")
    return redirect("/")

@app.route("/authors/<int:id>", methods=["GET"])
def autorYFavoritos(id):
    autor = {
        "id": id
    }
    autorConLibros = Autor.obtenerAutoresYFavoritos(autor)
    libros = Libro.obtenerLibrosNoFavoritos(autor) 

    return render_template("autor.html", autor = autorConLibros, libros = libros)

@app.route("/authors/favorite",methods=["POST"])
def agregarFavoritos():
    autor_libro={
        "autor_id":request.form["autor_id"],
        "libro_id":request.form["libro_id"]
    }

    resultado = Autor.añadeFavoritos(autor_libro)
    if(type(resultado) is bool and not resultado):
        print("Algo salio mal")
    return redirect("/authors/"+ autor_libro["autor_id"])