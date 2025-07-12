from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import PreferenceForm
from .services import get_gemini_completion
from django.utils.safestring import mark_safe
import markdown
import json
import os
import random
import requests
import urllib.parse
from django.views.decorators.csrf import csrf_exempt # AJAX POST için
from django.views.decorators.http import require_POST # Sadece POST isteklerini kabul etmek için
from django.shortcuts import render

# Unsplash API yardımcı fonksiyonu
def get_unsplash_image(query, count=1):
    """Unsplash API'den verilen arama sorgusu için resim URL'leri döndürür"""
    try:
        # Unsplash API Anahtarı - çevre değişkeninden al
        api_key = os.getenv('UNSPLASH_API_KEY')
        
        # Sorgu için ek anahtar kelimeler ekle
        enhanced_query = f"{query} travel destination landmark"
        print(f"[DEBUG] Gelişmiş Unsplash sorgusu: {enhanced_query}")
        
        # Sorguyu URL için formatla
        formatted_query = urllib.parse.quote(enhanced_query)
        
        # Unsplash API endpoint'i - daha alakalı sonuçlar için content_filter=high ekle
        url = f"https://api.unsplash.com/search/photos?query={formatted_query}&per_page={count}&orientation=landscape&content_filter=high"
        
        # API isteği
        headers = {
            "Authorization": f"Client-ID {api_key}"
        }
        
        response = requests.get(url, headers=headers)
        
        # Yanıtı kontrol et
        if response.status_code == 200:
            data = response.json()
            if data and data.get('results'):
                # Sonuç resimlerinin URL'lerini al
                image_urls = []
                for photo in data['results']:
                    if photo.get('urls') and photo.get('urls').get('regular'):
                        image_urls.append({
                            'url': photo['urls']['regular'],
                            'thumb': photo['urls']['thumb'],
                            'user_name': photo['user']['name'],
                            'user_link': photo['user']['links']['html']
                        })
                return image_urls
        
        # Sonuç yoksa, sadece yer ismini kullanarak tekrar dene
        if not image_urls:
            basic_query = urllib.parse.quote(query)
            url = f"https://api.unsplash.com/search/photos?query={basic_query}&per_page={count}&orientation=landscape"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data and data.get('results'):
                    image_urls = []
                    for photo in data['results']:
                        if photo.get('urls') and photo.get('urls').get('regular'):
                            image_urls.append({
                                'url': photo['urls']['regular'],
                                'thumb': photo['urls']['thumb'],
                                'user_name': photo['user']['name'],
                                'user_link': photo['user']['links']['html']
                            })
                    return image_urls
        
        # Hala sonuç yoksa, genel "tourist destination" aramasi yap
        if not image_urls:
            fallback_query = urllib.parse.quote("scenic tourist destination")
            url = f"https://api.unsplash.com/search/photos?query={fallback_query}&per_page={count}&orientation=landscape"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data and data.get('results'):
                    image_urls = []
                    for photo in data['results']:
                        if photo.get('urls') and photo.get('urls').get('regular'):
                            image_urls.append({
                                'url': photo['urls']['regular'],
                                'thumb': photo['urls']['thumb'],
                                'user_name': photo['user']['name'],
                                'user_link': photo['user']['links']['html']
                            })
                    return image_urls
                    
        return []
    except Exception as e:
        print(f"[ERROR] Unsplash API hatası: {e}")
        return []

@require_POST
@csrf_exempt # Geliştirme aşamasında CSRF'yi geçici olarak devre dışı bırakıyoruz, production'da düzgün CSRF handling eklenmeli
def ajax_get_recommendation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Yeni userSelections objesinden gelen veriler
            country = data.get('country', 'Türkiye')
            accommodation = data.get('accommodation', 'Fark Etmez')
            budget = data.get('budget', 'Fark Etmez')
            activities = data.get('activities', [])
            season = data.get('season', 'Fark Etmez')
            geo = data.get('geo', [])
            food = data.get('food', [])
            entertainment = data.get('entertainment', [])
            start_date = data.get('start_date', '')
            end_date = data.get('end_date', '')
            include_travel_time = data.get('include_travel_time', False)

            # Anket sorularına göre kapsamlı prompt oluşturma
            prompt_parts = []
            
            # Ülke bilgisi (her zaman eklenir)
            prompt_parts.append(f"Ülke: {country}")
            
            # Konaklama tercihi
            if accommodation and accommodation != 'Fark Etmez':
                prompt_parts.append(f"Konaklama tipi: {accommodation}")
            
            # Bütçe tercihi
            if budget and budget != 'Fark Etmez':
                prompt_parts.append(f"Bütçe: {budget}")
                
            # Aktiviteler (dizi) - çoklu seçim
            if activities and len(activities) > 0:
                activities_str = ", ".join(activities)
                prompt_parts.append(f"Tercih edilen aktiviteler: {activities_str}")
                
            # Mevsim tercihi
            if season and season != 'Fark Etmez':
                prompt_parts.append(f"Mevsim: {season}")
                
            # Coğrafi tercihler (dizi) - çoklu seçim
            if geo and len(geo) > 0:
                geo_str = ", ".join(geo)
                prompt_parts.append(f"Coğrafi özellikler: {geo_str}")
                
            # Yemek tercihleri (dizi) - çoklu seçim
            if food and len(food) > 0:
                food_str = ", ".join(food)
                prompt_parts.append(f"Yemek tercihleri: {food_str}")
                
            # Eğlence tercihleri (dizi) - çoklu seçim
            if entertainment and len(entertainment) > 0:
                entertainment_str = ", ".join(entertainment)
                prompt_parts.append(f"Eğlence tercihleri: {entertainment_str}")
                
            # Seyahat tarihleri
            if start_date and end_date:
                prompt_parts.append(f"Seyahat tarihleri: {start_date} - {end_date}")
                
            # Ulaşım süresi önemli mi?
            prompt_parts.append(f"Ulaşım süresi önemli mi: {'Evet' if include_travel_time else 'Hayır'}")

            # Prompt'u oluştur - 4 öneri için
            prompt = f"{', '.join(prompt_parts)}. -TÜRKÇE DİLİNDE ÖNERİ VER.- Bu tercihler ışığında, belirtilen ülkede 4 FARKLI tatil yeri öner. Önerilerini numara sırasıyla liste halinde ver. Her öneri için yer adı ve hakkında kısa bir açıklama olsun. Format şöyle olmalı: '\n1. [Yer Adı]: [Kısa açıklama]\n2. [Yer Adı]: [Kısa açıklama]' şeklinde. Örneğin: '\n1. Bodrum, Muğla: Ege'nin incisi Bodrum, canlı gece hayatı ve güzel plajlarıyla ünlüdür.\n2. Antalya: Turkuaz renkli denizi ve tarihi kalıntılarıyla...' gibi. MUTLAKA TAM OLARAK 4 ÖNERİ ver ve formatı koruyarak temiz bir yanıt döndür. Her öneri birbirinden farklı olmalı."

            print(f"[DEBUG] Oluşturulan Prompt: {prompt}") # Konsolda prompt'u görmek için

            ai_response = get_gemini_completion(prompt)

            if ai_response and ai_response.get('choices') and ai_response['choices'][0].get('message'):
                content = ai_response['choices'][0]['message']['content'].strip()
                # Yanıtı ayrıştırmaya çalışalım (4 öneri)
                try:
                    # \n karakterini kaldır
                    if content.startswith('\n'):
                        content = content[1:]
                    
                    # Başlık cümlesi ile önerileri ayırmak için
                    summary_title = ""
                    recommendations = []
                    
                    import re
                    
                    # İlk olarak, eğer varsa giriş/açıklama cümlesini belirle
                    # Genellikle "İşte [yer] için [x] öneri" formatında olur
                    # veya listeleme başlamadan önceki herhangi bir metin
                    intro_match = re.search(r'^(.*?)(?=\s*1\.\s+)', content, re.DOTALL)
                    
                    if intro_match:
                        summary_title = intro_match.group(1).strip()
                        # Giriş cümlesini içerikten çıkar
                        content = content[len(summary_title):].strip()
                    
                    # '1.', '2.' gibi numaraları bul ve parçala
                    recommendation_parts = re.split(r'\d+\.\s+', content)
                    # İlk eleman genellikle boş olur (split 'öncesindeki' kısım)
                    recommendation_parts = [part.strip() for part in recommendation_parts if part.strip()]
                    
                    for part in recommendation_parts:
                        # [Yer Adı]: [Açıklama] formatını ayrıştır
                        loc_parts = part.split(':', 1)
                        if len(loc_parts) == 2:
                            location_full = loc_parts[0].strip()  # Türkçe ve orijinal isimleri içerir
                            description = loc_parts[1].strip()
                            
                            # "Türkçe Ad (Orijinal Ad)" formatından isimleri çıkar
                            # Örneğin: "Bodrum (Bodrum)" veya "Roma (Rome)" veya "Venedik (Venice)"
                            original_name = ""
                            turkish_name = location_full
                            
                            # Parantez içindeki orijinal/İngilizce ismi ayrıştır
                            name_match = re.search(r'(.+?)\s*\(([^)]+)\)', location_full)
                            if name_match:
                                turkish_name = name_match.group(1).strip()
                                original_name = name_match.group(2).strip()
                                print(f"[DEBUG] Ayrıştırılan Türkçe isim: '{turkish_name}', Orijinal isim: '{original_name}'")
                            else:
                                # Orijinal isim bulunamadı, Türkçe ismi kullan
                                original_name = turkish_name
                                print(f"[DEBUG] Orijinal isim bulunamadı, Türkçe isim kullanılıyor: {turkish_name}")
                            
                            # Konum ismini temizle ve hazırla
                            location_clean = original_name.replace(',', ' ').replace('-', ' ').strip()
                            
                            # Daha spesifik ve alakalı bir arama sorgusu oluştur
                            # Sadece yer adı yerine turistik ve landmark terimlerini de ekle
                            image_query = location_clean
                            print(f"[DEBUG] Unsplash sorgu ismi: {image_query}")
                            
                            # Unsplash API'den öneri için 3 resim al (ilki ana resim, diğerleri yedek)
                            # Gelişmiş arama stratejisi get_unsplash_image fonksiyonunda uygulanıyor
                            unsplash_images = get_unsplash_image(image_query, count=3)
                            
                            # Eğer hiç resim bulunamazsa, Unsplash'te doğrudan yer adıyla arama yap
                            if not unsplash_images:
                                print(f"[DEBUG] İlk denemede hiç resim bulunamadı, sadece yer adıyla deneniyor")
                                generic_image_query = f"scenic {location_clean}"
                                unsplash_images = get_unsplash_image(generic_image_query, count=3)
                            
                            # Sonuçları hazırla
                            rec_data = {
                                'location_name': turkish_name,
                                'description': description,
                                'image_query': image_query,
                            }
                            
                            # Eğer Unsplash'ten resimler bulunursa, tüm resimleri ekle
                            if unsplash_images and len(unsplash_images) > 0:
                                rec_data['images'] = unsplash_images  # Tüm resimleri gönder
                            
                            recommendations.append(rec_data)
                    
                    # Eğer hiç öneri bulunamadıysa, tüm içeriği tek öneri olarak işle
                    if not recommendations:
                        recommendations.append({
                            'location_name': 'Öneri',
                            'description': content.strip()
                        })
                    
                    print(f"[DEBUG] Ayrıştırılan öneri sayısı: {len(recommendations)}")
                    print(f"[DEBUG] Özet başlık: {summary_title}")
                    
                    return JsonResponse({
                        'success': True,
                        'summary_title': summary_title,
                        'recommendations': recommendations
                    })
                except Exception as e:
                    print(f"AI yanıtı ayrıştırma hatası: {e}")
                    return JsonResponse({'success': False, 'error': 'AI yanıtı işlenirken bir hata oluştu.', 'details': str(e)})
            elif ai_response and ai_response.get('error'):
                 return JsonResponse({'success': False, 'error': 'Yapay zeka servisinden hata alındı.', 'details': ai_response.get('detail', 'Bilinmeyen API hatası')})
            else:
                return JsonResponse({'success': False, 'error': 'Yapay zeka servisinden geçerli bir yanıt alınamadı.'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Geçersiz JSON formatı.'}, status=400)
        except Exception as e:
            print(f"ajax_get_recommendation Hata: {e}")
            return JsonResponse({'success': False, 'error': 'Sunucu hatası.', 'details': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Sadece POST istekleri kabul edilir.'}, status=405)


# Create your views here.
def home(request):
    # Ana sayfa görünümü
    context = {}
    return render(request, "index.html", context)

# Create your views here.

def about_view(request):
    # Hakkımızda sayfası görünümü
    return render(request, 'about.html')

def dashboard_view(request):
    # Tatil paketleri sayfası görünümü
    return render(request, 'dashboard.html')

def recommendation_quiz_view(request):
    # Tatil öneri formu görünümü - CSRF token ve gerekli context ile
    context = {
        'title': 'Tatil Önerisi',
        'page': 'recommendation'
    }
    
    # Eğer template içinde static dosyaları kullanılıyorsa
    # ve CSS kısmında loading spinner tanımlı değilse CSS dosyasını güncelle
    # Bu aşamada loading spinner CSS'i style.css'e eklenebilir veya inline olarak verilebilir
    return render(request, 'recommendation-quiz.html', context)

def search_destinations(request):
    # Arama fonksiyonu
    query = request.GET.get('q', '')
    # Burada arama işlemleri yapılabilir
    # Şimdilik ana sayfaya yönlendirelim
    return redirect('index')

def past_recommendations(request):
    """Kullanıcının daha önce aldığı önerileri gösteren sayfa"""
    # Bu sayfa, localStorage'dan geçmiş önerileri gösterecek JavaScript içerecek
    return render(request, 'past_recommendations.html')


def preference_view(request):
    openrouter_result = None
    openrouter_result_markdown = None
    if request.method == 'POST':
        form = PreferenceForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            prompt = (
                f"Ülke: {cleaned.get('country', '')}, "
                f"Konaklama: {cleaned.get('accommodation', '')}, "
                f"Bütçe: {cleaned.get('budget', '')}, "
                f"Aktiviteler: {', '.join(cleaned.get('activities', []))}, "
                f"Mevsim: {cleaned.get('season', '')}, "
                f"Coğrafya: {', '.join(cleaned.get('geo', []))}, "
                f"Yemek: {', '.join(cleaned.get('food', []))}, "
                f"Eğlence: {', '.join(cleaned.get('entertainment', []))}, "
                f"Tarih: {cleaned.get('start_date', '')} - {cleaned.get('end_date', '')}, "
                f"Ulaşım dahil mi: {'Evet' if cleaned.get('include_travel_time') else 'Hayır'}; "
                "Kısa, net ve gerçekçi bir tatil yeri önerisi ver. Gereksiz açıklama ekleme."
            )
            openrouter_result = get_openrouter_completion(prompt)
            # AI cevabını markdown olarak HTML'e çevir
            if openrouter_result and openrouter_result.get('choices'):
                ai_content = openrouter_result['choices'][0]['message']['content']
                openrouter_result_markdown = mark_safe(markdown.markdown(ai_content))
            return render(request, 'preference_form.html', {
                'form': form,
                'openrouter_result': openrouter_result,
                'openrouter_result_markdown': openrouter_result_markdown,
                'submitted': True
            })
    else:
        form = PreferenceForm()
    return render(request, 'preference_form.html', {
        'form': form,
        'openrouter_result': openrouter_result,
        'openrouter_result_markdown': openrouter_result_markdown
    })
