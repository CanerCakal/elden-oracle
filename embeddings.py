from sentence_transformers import SentenceTransformer

# Kullanacağımız embedding modeli.
# "all-MiniLM-L6-v2": küçük, hızlı, kaliteli — RAG için popüler bir başlangıç modeli.
MODEL_NAME = "all-MiniLM-L6-v2"

# Modeli bir kez yükleyip tekrar tekrar kullanacağız.
# (İlk çalıştırmada internetten indirilir, sonra offline çalışır.)
_model = None


def get_model():
    """Embedding modelini yükler (bir kez), sonraki çağrılarda hazır olanı döndürür."""
    global _model
    if _model is None:
        print(f"Embedding modeli yükleniyor: {MODEL_NAME} ...")
        _model = SentenceTransformer(MODEL_NAME)
        print("Embedding modeli hazır.")
    return _model


def embed_text(text):
    """Tek bir metni vektöre çevirir. Sonuç: sayılardan oluşan bir liste."""
    model = get_model()
    vector = model.encode(text)
    return vector.tolist()  # numpy dizisini normal Python listesine çeviriyoruz


def embed_texts(texts):
    """Birden çok metni tek seferde vektöre çevirir (daha verimli)."""
    model = get_model()
    vectors = model.encode(texts)
    return [v.tolist() for v in vectors]