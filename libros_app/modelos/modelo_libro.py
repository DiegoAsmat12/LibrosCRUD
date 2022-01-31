from libros_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from libros_app.modelos import modelo_autor

class Libro:
    def __init__(self,id,titulo, num_paginas, created_at, updated_at):
        self.id = id
        self.titulo = titulo
        self.num_paginas = num_paginas
        self.created_at =created_at
        self.updated_at= updated_at
        self.autores:list[modelo_autor.Autor] = [] 
    
    def añadirAutor(self, autor):
        self.autores.append(autor)

    @classmethod
    def crearLibro( cls, libro):
        query = '''
                    INSERT INTO libros(titulo,num_paginas,created_at,updated_at)
                    VALUES (%(titulo)s,%(num_paginas)s, NOW(), NOW())
                '''
        resultado = connectToMySQL("esquema_libros").query_db(query,libro)

        return resultado
    
    @classmethod
    def obtenerLibros(cls):
        query = '''
                    SELECT * FROM libros
                '''
        resultado = connectToMySQL("esquema_libros").query_db(query)
        listaLibros = []
        for libro in resultado:
            listaLibros.append(cls(libro["id"], libro["titulo"],libro["num_paginas"], libro["created_at"], libro["updated_at"]))
        return listaLibros

    @classmethod
    def obtenerLibroFavoritoConAutor(cls, libro):
        query = '''
                    SELECT * FROM libros
                    LEFT JOIN favoritos on libros.id = favoritos.libro_id
                    LEFT JOIN autores on autores.id = favoritos.autor_id
                    WHERE libros.id = %(id)s
                '''
        resultado = connectToMySQL("esquema_libros").query_db(query,libro)
        libroObtenido = cls(resultado[0]["id"], resultado[0]["titulo"], resultado[0]["num_paginas"],resultado[0]["created_at"], resultado[0]["updated_at"])

        for row in resultado:
            libroObtenido.añadirAutor(modelo_autor.Autor(row["autores.id"],row["nombre"], 
                row["autores.created_at"], row["autores.updated_at"]))

        return libroObtenido

    @classmethod
    def obtenerLibrosNoFavoritos(cls, autor):
        query = '''
                    SELECT * FROM libros
                    WHERE libros.id NOT IN 
                    (SELECT libro_id FROM favoritos WHERE autor_id = %(id)s)
                '''
        
        resultado = connectToMySQL("esquema_libros").query_db(query,autor)
        listaLibros = []
        for libro in resultado:
            listaLibros.append(cls(libro["id"], libro["titulo"],libro["num_paginas"], libro["created_at"], libro["updated_at"]))
        
        return listaLibros