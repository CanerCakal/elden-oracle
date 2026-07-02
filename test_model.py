from foundry_local_sdk import Configuration, FoundryLocalManager

# 1) Foundry Local'i başlat
config = Configuration(app_name="elden-oracle")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

# 2) Kataloğundan modeli seç
model = manager.catalog.get_model("phi-3.5-mini")

# 3) Modeli indir (zaten indirildiyse hızlıca geçer)
print("Model indiriliyor (gerekirse)...")
model.download(lambda p: print(f"\rİndirme: {p:.1f}%", end="", flush=True))
print()

# 4) Modeli belleğe yükle
model.load()
print("Model yüklendi.")

# 5) Sohbet istemcisi al ve soru gönder
client = model.get_chat_client()
response = client.complete_chat([
    {"role": "user", "content": "Answer in one sentence: what is Elden Ring?"}
])

# 6) Cevabı yazdır
print(response.choices[0].message.content)

# 7) Modeli bellekten boşalt
model.unload()