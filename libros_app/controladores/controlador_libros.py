from flask import render_template, request, redirect
from libros_app import app
from libros_app.modelos.modelo_autor import Autor
from libros_app.modelos.modelo_libro import Libro

@app.route("/books", methods=["GET"])
def paginaLibros():
    libros = Libro.obtenerLibros()
    return render_template("libros.html", libros = libros)

@app.route("/books/create",methods=["POST"])
def agregarLibro():
    libro = {
        "titulo" : request.form["titulo"],
        "num_paginas":request.form["num_paginas"]
    }
    resultado = Libro.crearLibro(libro)
    if(type(resultado) is bool and not resultado):
        print("Algo salio mal")
    return redirect("/books")

@app.route("/books/<int:id>", methods=["GET"])
def muestraLibro(id):
    libro = {
        "id":id
    }
    libroConAutor = Libro.obtenerLibroFavoritoConAutor(libro)
    autores = Autor.obtenerLibrosNoFavoritos(libro)

    return render_template("libro.html", libro = libroConAutor, autores = autores)

@app.route("/books/favorite",methods=["POST"])
def agregaFavoritosDesdeLibro():
    autor_libro={
        "autor_id":request.form["autor_id"],
        "libro_id":request.form["libro_id"]
    }

    resultado = Autor.añadeFavoritos(autor_libro)
    if(type(resultado) is bool and not resultado):
        print("Algo salio mal")
    return redirect("/books/"+ autor_libro["libro_id"])