import google.generativeai as genai
import os # Ortam değişkenlerinden API anahtarı almak için

# 1. API Anahtarınızı Yapılandırma
# Güvenlik için API anahtarınızı doğrudan koda yazmak yerine,
# ortam değişkeni olarak ayarlamanız şiddetle tavsiye edilir.
# Örneğin, Linux/macOS'ta: export GOOGLE_API_KEY="YOUR_API_KEY"
# Windows'ta: set GOOGLE_API_KEY="YOUR_API_KEY"
# Eğer ortam değişkeni kullanmak istemiyorsanız, doğrudan koda yazabilirsiniz:
# genai.configure(api_key="YOUR_API_KEY")

try:
    api_key = "AIzaSyDkv-spVuy31T4yi-tSdq4iecyi-dfSJ4o"
    if not api_key:
        raise ValueError("GOOGLE_API_KEY ortam değişkeni ayarlanmamış.")
    genai.configure(api_key=api_key)
except ValueError as e:
    print(f"Hata: {e}")
    print("Lütfen GOOGLE_API_KEY ortam değişkenini ayarladığınızdan veya genai.configure() içinde API anahtarınızı doğrudan belirttiğinizden emin olun.")
    exit() # API anahtarı olmadan devam etmeyin

print("Kullanılabilir modeller listeleniyor...")

# 2. Modelleri Listeleme ve Filtreleme
# generateContent metodunu destekleyen modelleri listeliyoruz.
# Bu, metin veya içerik oluşturma yeteneğine sahip modelleri gösterir.
for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(f"--------------------------------------------------")
        print(f"Model Adı: {model.name}")
        print(f"Görüntü Adı: {model.display_name}")
        print(f"Açıklama: {model.description}")
        print(f"Desteklenen Üretim Metotları: {model.supported_generation_methods}")
        print(f"Giriş Fiyat Birimi: {model.input_token_limit}")
        print(f"Çıkış Fiyat Birimi: {model.output_token_limit}")
        # Modelin desteklediği ek özellikler veya kısıtlamalar da burada olabilir
        # print(f"Versiyon: {model.version}")
        # print(f"Çıkış Kodlama: {model.output_encoding}")
        print(f"--------------------------------------------------\n")

print("Model listeleme tamamlandı.")