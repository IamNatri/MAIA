import random
import psycopg2
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

logging.basicConfig(filename='sync_log.txt', level=logging.INFO)


def connect_to_db():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn

def mark_as_synced(conn, leitura_id):
    with conn.cursor() as cursor:
        cursor.execute("UPDATE leitura_sensores SET sincronizado = TRUE WHERE id = %s", (leitura_id,))
        conn.commit()

def log_sync(status, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"{timestamp} - Status: {'Sucesso' if status else 'Erro'} - Mensagem: {message}")

def log_sync_to_db(conn, status, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO sincronizacao (status, mensagem, timestamp)
            VALUES (%s, %s, %s)
        """, (status, message, timestamp))
        conn.commit()

def synchronize_data():
    conn = connect_to_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT 
                    ls.id AS leitura_id,
                    ls.valor,
                    ls.timestamp,
                    s.id AS sensor_id,
                    s.nome AS sensor_nome,
                    s.tipo AS sensor_tipo,
                    s.unidade AS sensor_unidade,
                    s.localizacao AS sensor_localizacao
                FROM 
                    leitura_sensores ls
                JOIN 
                    sensores s ON ls.sensor_id = s.id
                WHERE 
                    ls.sincronizado = false;""")
            
            unsynced_records = cursor.fetchall()

            if unsynced_records:
                for register in unsynced_records:
                    leitura_id, valor, timestamp = register[0], register[1], register[2]
                    sensor_id, sensor_nome, sensor_tipo, sensor_unidade = register[3], register[4], register[5], register[6]
                    sensor_localizacao = register[7]
                    try:
                        print(f"Enviando dados para GCP: {leitura_id} - {valor} - {timestamp} - {sensor_id} - {sensor_nome} - {sensor_tipo} - {sensor_unidade} - {sensor_localizacao}")
                        # Simulate sending data to GCP
                        gcp_simulator()
                        with conn:
                            mark_as_synced(conn, leitura_id)
                            log_sync_to_db(conn, True, f"Dados do sensor {sensor_id} leitura {leitura_id} sincronizados com sucesso.")
                        log_sync(True, f"Dados do sensor {sensor_id} leitura {leitura_id} sincronizados com sucesso.")
                    except Exception as e:
                        conn.rollback()
                        log_sync_to_db(conn, False, f"Falha ao sincronizar o sensor {sensor_id} leitura {leitura_id}: {str(e)}")
                        log_sync(False, f"Falha ao sincronizar o sensor {sensor_id}: {str(e)}")
            else:
                print("Nenhum dado não sincronizado encontrado.")
    except Exception as e:
        log_sync(False, f"Erro ao buscar dados: {str(e)}")
    finally:
        # garante o fechamento da conexão mesmo com utilização de with
        conn.close()
        

def gcp_simulator():
    # Simulate sending data to GCP
    if random.choice([True, False]):
        raise Exception("Simulated GCP failure")
    time.sleep(1)
    

if __name__ == "__main__":
    while True:
        synchronize_data()
        time.sleep(60)
