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

    chunks = build_chunks(DATA_DIR)
    print(f"Toplam {len(chunks)} parça oluşturuldu.\n")

    # Tüm parçaların metinlerini bir listeye al
    texts = [chunk["text"] for chunk in chunks]

    # Hepsini vektöre çevir
    vectors = embed_texts(texts)

    print(f"{len(vectors)} adet embedding üretildi.")
    print(f"Her vektörün boyutu: {len(vectors[0])} sayı.")
    print(f"\nİlk parçanın ilk 5 sayısı örnek olarak:")
    print(vectors[0][:5])