import sqlite3
import json

# Veritabanı dosyasının adı. Program bunu proje klasöründe oluşturacak.
DB_PATH = "elden_oracle.db"


def get_connection():
    """Veritabanına bağlantı açar."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Veritabanını ve 'chunks' tablosunu oluşturur (yoksa)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            text TEXT NOT NULL,
            embedding TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("Veritabanı hazır.")


def clear_chunks():
    """Tablodaki tüm kayıtları siler (yeniden yükleme için)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chunks")
    conn.commit()
    conn.close()


def insert_chunk(source, text, embedding):
    """Tek bir parçayı veritabanına ekler.
    embedding bir sayı listesidir; JSON metnine çevirip saklıyoruz."""
    conn = get_connection()
    cursor = conn.cursor()
    embedding_json = json.dumps(embedding)  # liste -> metin
    cursor.execute(
        "INSERT INTO chunks (source, text, embedding) VALUES (?, ?, ?)",
        (source, text, embedding_json)
    )
    conn.commit()
    conn.close()


def get_all_chunks():
    """Tüm parçaları okur. embedding'i metinden tekrar listeye çevirir."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, source, text, embedding FROM chunks")
    rows = cursor.fetchall()
    conn.close()

    chunks = []
    for row in rows:
        chunk_id, source, text, embedding_json = row
        chunks.append({
            "id": chunk_id,
            "source": source,
            "text": text,
            "embedding": json.loads(embedding_json)  # metin -> liste
        })
    return chunks