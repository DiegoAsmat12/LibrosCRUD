from libros_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from libros_app.modelos import modelo_libro

class Autor:
    def __init__(self, id, nombre, created_at, updated_at):
        self.id = id
        self.nombre = nombre
        self.created_at = created_at
        self.updated_at = updated_at
        self.libros:list[modelo_libro.Libro] = []

    def agregaLibro(self,libro:modelo_libro.Libro):
        self.libros.append( libro )

    @classmethod
    def crearAutor(cls, autor):
        query = '''
                    INSERT INTO autores(nombre,created_at,updated_at)
                    VALUES (%(nombre)s, NOW(), NOW());
                '''
        resultado = connectToMySQL("esquema_libros").query_db(query,autor)
        return resultado

    @classmethod
    def obtenerAutores(cls):
        query = '''
                    SELECT * FROM autores;
                '''
        
        resultado = connectToMySQL("esquema_libros").query_db(query)
        listaAutores = []
        for autor in resultado:
            listaAutores.append(cls(autor["id"], autor["nombre"], autor["created_at"], autor["updated_at"]))
        return listaAutores

    @classmethod
    def obtenerAutoresYFavoritos(cls, autor):
        query = '''
                    SELECT * from autores
                    LEFT JOIN favoritos ON autores.id = favoritos.autor_id
                    LEFT JOIN libros ON favoritos.libro_id = libros.id
                    WHERE autores.id = %(id)s;
                '''
        resultado = connectToMySQL("esquema_libros").query_db(query,autor)
        autorObtenido = cls(resultado[0]["id"], resultado[0]["nombre"], resultado[0]["created_at"], resultado[0]["updated_at"])

        for row in resultado:
            autorObtenido.agregaLibro(modelo_libro.Libro(row["libros.id"],row["titulo"], 
                row["num_paginas"], row["libros.created_at"], row["libros.updated_at"]))
        
        return autorObtenido

    @classmethod
    def añadeFavoritos(cls, autor_libro):
        query = '''
                    INSERT INTO favoritos (autor_id,libro_id)
                    VALUES (%(autor_id)s, %(libro_id)s)
                '''
        resultado = connectToMySQL("esquema_libros").query_db(query,autor_libro)
        return resultado

    @classmethod
    def obtenerLibrosNoFavoritos(cls, libro):
        query = '''
                    SELECT * FROM autores 
                    WHERE autores.id NOT IN
                    (SELECT autor_id FROM favoritos WHERE libro_id =%(id)s);
                '''
        resultado = connectToMySQL("esquema_libros").query_db(query,libro)

        listaAutores = []
        for autor in resultado:
            listaAutores.append(cls(autor["id"], autor["nombre"], autor["created_at"], autor["updated_at"]))
        return listaAutores
