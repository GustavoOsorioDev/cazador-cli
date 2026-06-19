import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Resuelve desde la raíz del proyecto sin importar el directorio de trabajo.
            # Si ejecutas desde src/ o desde cazador-cli/, la DB siempre se crea en cazador-cli/db/cazador.db
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, "db", "cazador.db")
        self.db_path = db_path
        self._ensure_dir()
        self._init_db()

    def _ensure_dir(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS oportunidades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fuente TEXT NOT NULL,
                    titulo TEXT NOT NULL,
                    comentarios INTEGER DEFAULT 0,
                    votos INTEGER DEFAULT 0,
                    enlace TEXT NOT NULL UNIQUE,
                    dolor TEXT,
                    score_gap REAL,
                    fecha TEXT NOT NULL
                )
            """)
            conn.commit()

    def guardar_oportunidad(self, op):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR IGNORE INTO oportunidades 
                    (fuente, titulo, comentarios, votos, enlace, dolor, score_gap, fecha)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (op.fuente, op.titulo, op.comentarios, op.votos, op.enlace, op.dolor, op.score_gap, op.fecha))
                conn.commit()
        except Exception as e:
            print(f"Error al guardar en DB: {e}")

    def obtener_mejores(self, limit: int = 10):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM oportunidades ORDER BY score_gap DESC LIMIT ?", (limit,))
            return [dict(row) for row in cursor.fetchall()]
