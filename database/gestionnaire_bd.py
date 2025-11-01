import sqlite3
from pathlib import Path
from config.parametres import DB_PATH #importer le chemin défini

class Database:
    def __init__(self,db_path=DB_PATH):
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True,exist_ok=True)

    def connect(self):
        try:
            conn = sqlite3.connect(self.db_path,timeout=5.0)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            raise

    def execute(self,sql:str,params=()):
        if params is None:
            params =()
        
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            return cur
    def executemany(self, sql, seq_of_params):
        with self.connect() as conn:
            cur = conn.cursor()
            cur.executemany(sql,seq_of_params)
            return cur