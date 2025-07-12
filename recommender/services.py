import json
import requests
import os
from django.conf import settings

# Google AI importları
import google.generativeai as genai
from google.generativeai import types

def get_gemini_completion(user_message):


    """
    Google Gemini API kullanarak sohbet tamamlama işlemi yapar.
    """
    print("[DEBUG] Gemini API'ya gönderilen prompt:")
    print(user_message)

    # Gemini API anahtarı
    GEMINI_API_KEY = "AIzaSyDkv-spVuy31T4yi-tSdq4iecyi-dfSJ4o"
    
    print("İşlem Başlatıldı. Gemini'den Dönüş Bekleniyor...")
    
    try:
        # Gemini API'yi konfigüre et
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Kullanılacak model - standard gemini-pro modelini kullan (daha güvenilir)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Özel istek formatı - hem Türkçe hem orijinal isimleri içerecek
        if 'tatil yeri öner' in user_message.lower() or 'tatil önerisi' in user_message.lower():
            # Orijinal mesajı sakla
            original_message = user_message
            
            # Tatil önerisi formatını güncelle
            user_message += "\n\nLütfen her öneri için hem Türkçe hem orijinal yer isimlerini ver. Örnek format:\n"
            user_message += "1. [Türkçe Yer Adı] ([Orijinal/İngilizce Yer Adı]): [Açıklama]\n"
            user_message += "2. [Türkçe Yer Adı] ([Orijinal/İngilizce Yer Adı]): [Açıklama]\n"
            user_message += "Parantez içindeki orijinal isimler çok önemli, lütfen her yer için mutlaka orijinal/İngilizce ismini de ekle."
            
            print(f"[DEBUG] Güncellenmiş istek: {user_message}")
        
        # Yanıt konfigürasyonu
        generation_config = {
            "temperature": 0.7,
            "max_output_tokens": 800,
            "top_p": 0.95
        }

        
        # API isteği gönder
        try:
            response = model.generate_content(
                user_message,
                generation_config=generation_config
            )
            
            print(f"[DEBUG] Gemini API yanıt alındı.")
            print(f"[DEBUG] Yanıt tipi: {type(response)}")
            
            # Yanıt içeriğini güvenli bir şekilde al
            content = ""
            
            # response'un dict olarak temsil edilmesini dene
            try:
                response_dict = response.to_dict()
                print(f"[DEBUG] Response dict: {str(response_dict)[:200]}...")
            except Exception as e:
                print(f"[DEBUG] Response dict hatası: {e}")
            
            # Farklı response formatı stratejileri
            try:
                if hasattr(response, 'text'):
                    content = response.text
                    print(f"[DEBUG] response.text alındı: {content[:100]}...")
                elif hasattr(response, 'candidates') and response.candidates:
                    print(f"[DEBUG] Adaylar mevcut: {len(response.candidates)}")
                    for candidate in response.candidates:
                        if hasattr(candidate, 'content') and candidate.content and hasattr(candidate.content, 'parts'):
                            for part in candidate.content.parts:
                                if hasattr(part, 'text'):
                                    content += part.text
                                elif isinstance(part, dict) and 'text' in part:
                                    content += part['text']
                                else:
                                    content += str(part)
                elif isinstance(response, dict) and 'candidates' in response:
                    for candidate in response['candidates']:
                        if 'content' in candidate and 'parts' in candidate['content']:
                            for part in candidate['content']['parts']:
                                if 'text' in part:
                                    content += part['text']
                else:
                    # Raw response formatını döndür
                    content = str(response)
            except Exception as e:
                print(f"[DEBUG] İçerik çıkarma hatası: {e}")
                content = f"API yanıt verdi, ancak içeriği çıkarılamadı: {str(e)}"
        except Exception as e:
            print(f"[DEBUG] API isteği hatası: {e}")
            # Daha basit bir yaklaşım: Düz HTTP isteği gönder
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [{"parts": [{"text": user_message}]}],
                "generationConfig": generation_config
            }
            
            print("[DEBUG] Düz HTTP isteği deneniyor...")
            response = requests.post(url, headers=headers, json=data)
            print(f"[DEBUG] HTTP yanıt kodu: {response.status_code}")
            
            if response.status_code == 200:
                response_json = response.json()
                if 'candidates' in response_json and len(response_json['candidates']) > 0:
                    if 'content' in response_json['candidates'][0] and 'parts' in response_json['candidates'][0]['content']:
                        parts = response_json['candidates'][0]['content']['parts']
                        if len(parts) > 0 and 'text' in parts[0]:
                            content = parts[0]['text']
                        else:
                            content = str(parts)
                    else:
                        content = str(response_json['candidates'][0])
                else:
                    content = str(response_json)
            else:
                content = f"API hatası: {response.status_code} - {response.text}"
            
        print(f"[DEBUG] Çıkarılan içerik: {content[:100]}...")
        
        # Markdown işaretlerini temizle
        # ** bold işaretlerini kaldır
        content = content.replace('**', '')
        # * italic işaretlerini kaldır
        content = content.replace('*', '')
        # Markdown listelerini düzenle
        content = content.replace('- ', '\n- ')
        # Gereksiz boşlukları temizle
        content = content.strip()
        
        print(f"[DEBUG] Temizlenmiş içerik: {content[:100]}...")
        
        # views.py ile uyumlu formatta yanıt döndür
        formatted_response = {
            "choices": [
                {
                    "message": {
                        "content": content
                    }
                }
            ]
        }
        
        return formatted_response
        
    except Exception as e:
        print(f"[ERROR] Gemini API hatası: {str(e)}")
        return {
            "error": True,
            "message": f"Gemini API hatası: {str(e)}",
            "choices": [{"message": {"content": "Maalesef şu anda öneri oluşturulamadı. Lütfen daha sonra tekrar deneyin."}}]
        }
    


"""
Bu kısım eski OpenRouter kullanımını gösterir.
Yorum satırına alınmıştır ve artık kullanılmamaktadır.

def get_openrouter_completion(user_message):
    print("[DEBUG] Gemini API'ya gönderilen prompt:")
    print(user_message)

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    print("İşlem Başlatıldı. Yapay Zekadan Dönüş Bekleniyor...")
    data=json.dumps({
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "max_tokens": 500,
    "messages": [
      {
        "role": "user",
        "content": user_message
      }
    ],
    
  })

    response = requests.post(url, headers=headers, data=data)
    print(f"[DEBUG] API yanıt kodu: {response.status_code}")
    print(f"[DEBUG] API yanıt metni: {response.text}")
    # Eğer rate-limit ya da provider error geldiyse alternatif model ile tekrar dene
    if response.status_code == 200:
        return response.json()
    else:
        try:
            resp_json = response.json()
            if response.status_code == 429 or (resp_json.get('error') and 'rate-limited' in str(resp_json['error'])):
                print('[DEBUG] Ana model rate-limit oldu, alternatif modele geçiliyor...')
                data_alt = json.dumps({
                    "model": "deepseek/deepseek-chat-v3-0324:free",
                    "max_tokens": 500,
                    "messages": [
                        {
                            "role": "user",
                            "content": user_message
                        }
                    ],
                })
                response_alt = requests.post(url, headers=headers, data=data_alt)
                print(f"[DEBUG] Alternatif model yanıt kodu: {response_alt.status_code}")
                print(f"[DEBUG] Alternatif model yanıt metni: {response_alt.text}")
                if response_alt.status_code == 200:
                    return response_alt.json()
                else:
                    return {"error": response_alt.status_code, "detail": "Her iki model de şu anda yoğun. Lütfen daha sonra tekrar deneyin."}
            elif resp_json.get('error'):
                return {"error": response.status_code, "detail": resp_json['error'].get('message', 'Bilinmeyen hata')}
            else:
                return {"error": response.status_code, "detail": response.text}
        except Exception as e:
            return {"error": response.status_code, "detail": f"API yanıtı çözümlenemedi: {str(e)}"}            
"""