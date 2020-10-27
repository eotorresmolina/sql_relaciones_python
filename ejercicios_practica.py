#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de práctica
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Emmanuel Oscar Torres Molina"
__email__ = "emmaotm@gmail.com"
__version__ = "1.1"

import sqlite3

# https://extendsclass.com/sqlite-browser.html


def insert_tutors (tutors):
    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()

    c.executemany("""
                    INSERT INTO tutor (name)
                    VALUES (?);""", tutors)  

    conn.commit()
    conn.close( )    


def insert_group (group):
    conn = sqlite3.connect('secundaria.db')
    conn.execute(""" PRAGMA foreing_keys = 1 """)       # Activo las foreing_keys por si No Existe un id
    c = conn.cursor( )

    try:
        c.executemany("""
                    INSERT INTO estudiante AS e (name, age, grade, fk_tutor_id)
                    SELECT ?, ?, ?, t.id
                    FROM tutor AS t 
                    WHERE t.name = ?; """, group)

    except sqlite3.Error as err:
        print('\n{}\n'.format(err))

    conn.commit()
    conn.close()


def imprimir_tabla_tutor ( ):
    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()

    c.execute(""" 
                SELECT *
                FROM tutor AS t;
            """)

    print('Tabla de Tutores:\n')
    print('(id   name)')

    for row in c:
        print(row)

    conn.close()
        
    
def create_schema():

    # Conectarnos a la base de datos
    # En caso de que no exista el archivo se genera
    # como una base de datos vacia
    conn = sqlite3.connect('secundaria.db')

    # Crear el cursor para poder ejecutar las querys
    c = conn.cursor()

    # Ejecutar una query
    c.execute("""
                DROP TABLE IF EXISTS estudiante;
            """)

    c.execute("""
            DROP TABLE IF EXISTS tutor;
        """)

    # Ejecutar una query
    c.execute("""
        CREATE TABLE tutor(
            [id] INTEGER PRIMARY KEY AUTOINCREMENT,
            [name] TEXT NOT NULL
        );
        """)

    c.execute("""
            CREATE TABLE estudiante(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [name] TEXT NOT NULL,
                [age] INTEGER NOT NULL,
                [grade] INTEGER NOT NULL,
                [fk_tutor_id] INTEGER NOT NULL REFERENCES tutor(id)
            );
            """)

    # Para salvar los cambios realizados en la DB debemos
    # ejecutar el commit, NO olvidarse de este paso!
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()


def fill():
    print('Completemos esta tablita!\n\n')
    # Llenar la tabla de la secundaria con al menos 2 tutores
    # Cada tutor tiene los campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del tutor (puede ser solo nombre sin apellido)

    # Llenar la tabla de la secundaria con al menos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del estudiante (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante
    # grade --> en que año de la secundaria se encuentra (1-6)
    # fk_tutor_id --> id de su tutor

    # Se debe utilizar la sentencia INSERT.
    # Observar que todos los campos son obligatorios
    # Cuando se inserte los estudiantes sería recomendable
    # que utilice el INSERT + SELECT para que sea más legible
    # el INSERT del estudiante con el nombre del tutor

    # No olvidarse que antes de poder insertar un estudiante debe haberse
    # primero insertado el tutor.
    # No olvidar activar las foreign_keys!

    tutors = [('Franco Pessana',), 
            ('Mariano Llamedo Soria',),
            ('Ted Mosby',),
            ('Jirafales',), 
            ('Horacio Craiem',)
            ]

    group = [('Martín Miguel', 28, 2, 'Ted Mosby'), 
                ('Carlos Catán', 16, 1, 'Franco Pessana'), 
                ('Barney Stinson', 18, 3, 'Jirafales'), 
                ('Oscar Torres', 17, 2, 'Horacio Craiem'), 
                ('Mercedes Maldonado', 27, 6, 'Mariano Llamedo Soria'), 
                ('Victoria Rodriguez', 21, 5, 'Horacio Craiem'),
                ('Michael Corleone', 20, 5, 'Franco Pessana'), 
                ('Andrea Tattaglia', 19, 4, 'Jirafales')
            ]

    insert_tutors(tutors)
    insert_group(group)


def fetch():
    print('Comprobemos su contenido, ¿qué hay en la tabla?\n\n')
    # Utilizar la sentencia SELECT para imprimir en pantalla
    # todas las filas con todas sus columnas de la tabla estudiante.
    # No debe imprimir el id del tutor, debe reemplazar el id por el nombre
    # del tutor en la query, utilizando el concepto de INNER JOIN,
    # se puede usar el WHERE en vez del INNER JOIN.
    # Utilizar fetchone para imprimir de una fila a la vez

    # columnas que deben aparecer en el print:
    # id / name / age / grade / tutor_nombre

    imprimir_tabla_tutor ( )

    print('\n\nTabla de Estudiantes:\n')
    print('(id, name, age, grade, tutor_nombre)')

    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()

    c.execute("""
                SELECT e.id, e.name, e.age, e.grade, t.name
                FROM estudiante AS e
                INNER JOIN tutor AS t ON e.fk_tutor_id = t.id;
    """)

    for row in c:
        print(row) 

    conn.close()   


def search_by_tutor(tutor):
    print('\n\nOperación búsqueda!\n\n')
    # Esta función recibe como parámetro el nombre de un posible tutor.
    # Utilizar la sentencia SELECT para imprimir en pantalla
    # aquellos estudiantes que tengan asignado dicho tutor.

    # De la lista de esos estudiantes el SELECT solo debe traer
    # las siguientes columnas por fila encontrada:
    # id / name / age / tutor_nombre

    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()

    c.execute("""
                SELECT e.id, e.name, e.age, t.name
                FROM estudiante AS e
                INNER JOIN tutor AS t ON t.id = e.fk_tutor_id
                WHERE t.name = ?
        """, (tutor,))

    print('(id, name, age, tutor_nombre)')
    for row in c:
        print(row)

    conn.close()


def modify(id, name):
    print('\n\nModificando la tabla\n\n')
    # Utilizar la sentencia UPDATE para modificar aquella fila (estudiante)
    # cuyo id sea el "id" pasado como parámetro,
    # modificar el tutor asignado (fk_tutor_id --> id) por aquel que coincida
    # con el nombre del tutor pasado como parámetro

    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()
    rowcount = c.execute("""
                UPDATE estudiante
                SET fk_tutor_id = (SELECT t.id FROM tutor AS t WHERE t.name = ?)
                WHERE id = ?;""", (name, id)).rowcount

    print('Cantidad de Filas Actualizadas: {}\n\n'.format(rowcount))

    conn.commit()
    conn.close()


def count_grade(grade):
    print('\n\nEstudiante por grado\n\n')
    # Utilizar la sentencia COUNT para contar cuantos estudiantes
    # se encuentran cursando el grado "grade" pasado como parámetro
    # Imprimir en pantalla el resultado

    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor( )

    c.execute("""
                SELECT COUNT(e.id) AS count_grade
                FROM estudiante AS e
                INNER JOIN tutor AS t ON e.fk_tutor_id = t.id
                AND e.grade = ?;""", (grade,))

    result = c.fetchone()
    count = result[0]   # Tomo el 1er Elemento, ya que me devuelve una tupla
    print('Estudiantes de Grado {} Encontradas: {}\n\n'.format(grade, count))

    conn.close()


if __name__ == '__main__':
    print("\n\nBienvenidos a otra clase de Inove con Python\n\n")
    create_schema()   # create and reset database (DB)
    fill()
    fetch()

    tutor = 'Franco Pessana'
    search_by_tutor(tutor)

    nuevo_tutor = 'Jirafales'
    id = 2
    modify(id, nuevo_tutor)

    grade = 2
    count_grade(grade)
