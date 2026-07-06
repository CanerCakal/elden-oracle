import os

# Ham metin dosyalarının bulunduğu klasör
DATA_DIR = "data"


def load_documents(data_dir):
    """data klasöründeki tüm .txt dosyalarını okur.
    Her dosyayı (kaynak_adı, içerik) olarak döndürür."""
    documents = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            path = os.path.join(data_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # Kaynak adı olarak dosya adını (uzantısız) kullanıyoruz
            source = filename.replace(".txt", "")
            documents.append((source, content))
    return documents


def chunk_text(text):
    """Bir metni paragraflara böler.
    Boş satırları ayraç kabul eder, çok kısa parçaları eler."""
    # Çift satır atlamasına göre böl (paragraf ayrımı)
    raw_paragraphs = text.split("\n\n")
    chunks = []
    for para in raw_paragraphs:
        cleaned = para.strip()
        # 40 karakterden kısa parçaları (başlık, boşluk vb.) atla
        if len(cleaned) >= 40:
            chunks.append(cleaned)
    return chunks


def build_chunks(data_dir):
    """Tüm dosyaları okur, parçalar ve kaynak etiketiyle listeler."""
    documents = load_documents(data_dir)
    all_chunks = []
    for source, content in documents:
        chunks = chunk_text(content)
        for chunk in chunks:
            all_chunks.append({
                "source": source,
                "text": chunk
            })
    return all_chunks


# Bu dosya doğrudan çalıştırıldığında test amaçlı çıktı ver
if __name__ == "__main__":
    from embeddings import embed_texts
    from database import init_db, clear_chunks, insert_chunk, get_all_chunks

    # 1) Veritabanını hazırla ve eski kayıtları temizle
    init_db()
    clear_chunks()
    print("Eski kayıtlar temizlendi.")

    # 2) Parçaları oluştur
    chunks = build_chunks(DATA_DIR)
    print(f"{len(chunks)} parça oluşturuldu.")

    # 3) Tüm parçaların embedding'lerini üret
    texts = [chunk["text"] for chunk in chunks]
    vectors = embed_texts(texts)
    print(f"{len(vectors)} embedding üretildi.")

    # 4) Her parçayı veritabanına kaydet
    for chunk, vector in zip(chunks, vectors):
        insert_chunk(chunk["source"], chunk["text"], vector)
    print("Tüm parçalar veritabanına kaydedildi.")

    # 5) Kontrol: kaç kayıt var, örnek göster
    saved = get_all_chunks()
    print(f"\nVeritabanında {len(saved)} kayıt var.")
    print(f"Örnek kayıt -> Kaynak: {saved[0]['source']}, "
          f"Vektör boyutu: {len(saved[0]['embedding'])}")