'''
SQL Introducción [Python]
Ejercicios de Profundización
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripción:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase.
'''

__author__ = "Emmanuel Oscar Torres Molina"
__email__ = "emmaotm@gmail.com"
__version__ = "1.1"


import sqlite3
import csv


def insert_author(author):
    conn = sqlite3.connect('libreria.db')
    conn.execute("""PRAGMA foreing_keys = 1""")

    c = conn.cursor()

    c.execute("""
                INSERT INTO autor (name)
                VALUES (?);
    """, (author,))

    conn.commit()
    conn.close() 


def insert_libro (item):
    conn = sqlite3.connect('libreria.db')
    conn.execute("""PRAGMA foreing_keys = 1""")
    c = conn.cursor()

    try:
        c.execute("""
                    INSERT INTO libro (title, pags, fk_author_id)
                    SELECT ?, ?, a.id
                    FROM autor AS a
                    WHERE a.name = ?;""", item)
    
    except sqlite3.Error as err:
        print('\n\n{}\n\n'.format(err))

    conn.commit()
    conn.close()


def insert_group_libro(items):
    conn = sqlite3.connect('libreria.db')
    conn.execute("""PRAGMA foreing_keys = 1""")
    c = conn.cursor()


    try:
        c.executemany("""
                    INSERT INTO libro (title, pags, fk_author_id)
                    SELECT ?, ?, a.id
                    FROM autor AS a
                    WHERE a.name = ?;""", items) 

    except sqlite3.Error as err:
        print('\n\n{}\n\n'.format(err))

    conn.commit()
    conn.close()


def create_schema( ):
    conn = sqlite3.connect('libreria.db')
    c = conn.cursor()
    c.execute(""" DROP TABLE IF EXISTS libro;
            """)

    c.execute(""" DROP TABLE IF EXISTS autor;
        """)

    c.execute("""
                CREATE TABLE autor(
                    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                    [name] TEXT NOT NULL
                );
    """)

    c.execute("""
                CREATE TABLE libro(
                    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                    [title] TEXT NOT NULL,
                    [pags] INTEGER NOT NULL,
                    [fk_author_id] INTEGER NOT NULL REFERENCES [id]
                );
    """)        

    conn.commit()
    conn.close()


def fill ( ):
    # Obtengo los autores del archivo csv
    with open('libreria_autor.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            insert_author(row.get('autor'))

    # Obtengo los libros del archivo csv
    with open('libreria_libro.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item = (row.get('titulo'), int(row.get('cantidad_paginas')), row.get('autor'))
            insert_libro(item)


def fill_chunk(chunksize=2):

    with open('libreria_autor.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            autor = row.get('autor') 
            insert_author(autor)

    with open('libreria_libro.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        chunk = []

        for row in reader:
            item = (row.get('titulo'), int(row.get('cantidad_paginas')), row.get('autor'))
            chunk.append(item)
            if len(chunk) == chunksize:
                insert_group_libro(chunk)
                chunk.clear()

        if chunk:
            insert_group_libro(chunk)


def fetch (id=0):
    conn = sqlite3.connect('libreria.db')
    conn.execute("""PRAGMA foreing_keys = 1""")
    c = conn.cursor()

    if id == 0:
        c.execute("""
                    SELECT l.id, l.title, l.pags, a.name
                    FROM libro AS l
                    INNER JOIN autor AS a ON l.fk_author_id = a.id;
        """)

    elif id > 0:
        c.execute("""
                    SELECT l.id, l.title, l.pags, a.name
                    FROM libro AS l
                    INNER JOIN autor AS a ON a.id = l.fk_author_id
                    WHERE l.id = ?;""", (id,))

    print('\n\n(id, title, pags, author)')

    for row in c:
        print(row)

    conn.close()


def search_author(book_title):
    conn = sqlite3.connect('libreria.db')
    conn.execute("""PRAGMA foreing_keys = 1""")
    c = conn.cursor()

    c.execute("""
                SELECT a.name
                FROM libro AS l
                INNER JOIN autor AS a ON a.id = l.fk_author_id
                WHERE l.title = ?;""", (book_title,))

    autor = c.fetchone()
    conn.close()
    return autor[0]        


if __name__ == '__main__':
    # Create DB
    create_schema()

    # Completar la DB con el CSV
    fill()
    #fill_chunk(chunksize=2)

    # Leer filas
    fetch()  # Ver todo el contenido de la DB
    fetch(3)  # Ver la fila 3
    fetch(20)  # Ver la fila 20

    # Buscar autor
    print('\n\n{}\n\n'.format(search_author('Relato de un naufrago')))
