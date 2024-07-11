import psycopg2
from dotenv import load_dotenv
import os
from contextlib import contextmanager

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE =  os.getenv('DATABASE')
HOST = os.getenv('HOST')
USERSERVER = os.getenv('USERSERVER')
PASSWORD = os.getenv('PASSWORD')
PORT = os.getenv('PORT')

@contextmanager
def instance_cursor():
    connection = psycopg2.connect(database=DATABASE_URL)
                                  
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print('Conexão com PostgreeSQL fechada')


def consulta_geral():
    with instance_cursor() as cursor:
        query = '''
        SELECT *
        FROM REGISTROS
        '''
        cursor.execute(query,)
        request = cursor.fetchall()
        return request
    
def consulta_nome(user):
    with instance_cursor() as cursor:
        query = '''
            SELECT nome, usuario, senha
            FROM REGISTROS
            WHERE usuario = %s
            
            '''
        cursor.execute(query, (user,))
        request = cursor.fetchall()
        return request
    
def criar_tabela():
    connection = psycopg2.connect(database=DATABASE_URL)
    cursor = connection.cursor()

    query = '''
            CREATE TABLE REGISTROS (
                nome varchar(255),
                usuario varchar(255),
                senha varchar(255)
            )
            '''
    cursor.execute(query)
    connection.commit()
    print('Tabela Criada')

    if(connection):
        cursor.close()
        connection.close()
        print('Conexão com PostgreSQL fechada')


def add_registro(nome, user, senha):
    connection = psycopg2.connect(database=DATABASE_URL)
    cursor = connection.cursor()

    query = f'''
            INSERT INTO REGISTROS VALUES
            {nome, user, senha}
            '''

    cursor.execute(query)
    connection.commit()
    
    if(connection):
        cursor.close()
        connection.close()
        print('Conexão com PostgreSQL fechada')
            
