# Tatil Yeri Öneri Platformu

Bu proje, kullanıcı tercihlerine göre Google Gemini API kullanarak kişiselleştirilmiş tatil yeri önerileri sunan ve bu yerleri görseller ve harita üzerinde gösteren bir web uygulamasıdır.

## 🌟 Özellikler

- **Kişiselleştirilmiş Tatil Önerileri**: Bütçe, aktivite türü, sezon, bölge vb. tercihlerinize göre özel öneriler
- **Görsel Zenginleştirme**: Önerilen tatil yerleri için Unsplash API ile otomatik görsel gösterim
- **Harita Entegrasyonu**: Önerilen yerlerin Google Haritalar üzerinde görselleştirilmesi
- **Kullanıcı Tercih Formu**: Kapsamlı ve kullanıcı dostu tercih formu
- **Responsive Tasarım**: Mobil cihazlar dahil tüm ekranlarda uyumlu görünüm

## 🛠️ Teknolojiler

### Backend
- **Django**: Web uygulaması çatısı
- **Python**: Ana programlama dili
- **Google Gemini API**: Yapay zeka destekli öneri motoru
- **PostgreSQL**: Veritabanı (opsiyonel, şu anda SQLite kullanılmakta)

### Frontend
- **HTML/CSS/JavaScript**: Web arayüzü
- **Bootstrap**: Responsive tasarım
- **Google Maps API**: Harita görselleştirme
- **AJAX**: Arka plan sunucu istekleri

## 🚀 Kurulum

1. Repoyu klonlayın:
   ```bash
   git clone https://github.com/your-username/tatil-yeri-oneri-platformu.git
   cd tatil-yeri-oneri-platformu
   ```

2. Sanal ortam oluşturun ve aktifleştirin:
   ```bash
   python -m venv venv
   # Windows için
   venv\Scripts\activate
   # macOS/Linux için
   source venv/bin/activate
   ```

3. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

4. `.env` dosyası oluşturun ve gerekli API anahtarlarını ekleyin:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   MAPS_API_KEY=your_google_maps_api_key
   UNSPLASH_API_KEY=your_unsplash_api_key
   ```

5. Veritabanı migrasyonlarını uygulayın:
   ```bash
   python manage.py migrate
   ```

6. Geliştirme sunucusunu başlatın:
   ```bash
   python manage.py runserver
   ```

7. Tarayıcınızda `http://127.0.0.1:8000` adresine gidin

## 📸 Ekran Görüntüleri

*Bu bölüme uygulama arayüzünden ekran görüntüleri ekleyebilirsiniz.*

## 📝 Kullanım

1. Ana sayfada "Tatil Önerisi Al" butonuna tıklayın
2. Tercihlerinizi belirtin:
   - Ülke seçimi
   - Konaklama tercihi
   - Bütçe aralığı
   - İlgilendiğiniz aktiviteler
   - Tercih ettiğiniz sezon
   - Coğrafi tercihler
   - Yemek ve eğlence tercihleri
   - Seyahat tarihleri
3. "Öneri Al" butonuna tıklayın
4. Yapay zeka tarafından oluşturulan kişiselleştirilmiş önerileri görüntüleyin
5. Önerilen yerleri harita üzerinde inceleyin ve görsellerle keşfedin

## 🤝 Katkıda Bulunma

1. Bu repoyu forklayın
2. Yeni bir özellik dalı oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commitleyin (`git commit -m 'Add some amazing feature'`)
4. Dalınıza pushlayın (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📜 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

## 🙏 Teşekkürler

- [Google Gemini API](https://ai.google.dev/) - Yapay zeka tabanlı içerik üretimi için
- [Unsplash API](https://unsplash.com/developers) - Yüksek kaliteli görseller için
- [Google Maps API](https://developers.google.com/maps) - Harita görselleştirmeleri için
- [Bootstrap](https://getbootstrap.com/) - Responsive tasarım için
