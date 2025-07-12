from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Ad')
    last_name = forms.CharField(max_length=30, required=True, label='Soyad')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    pass

class PreferenceForm(forms.Form):
    COUNTRY_CHOICES = [
        ('turkiye', 'Türkiye'),
        ('yunanistan', 'Yunanistan'),
        ('italya', 'İtalya'),
        ('ispanya', 'İspanya'),
        ('fransa', 'Fransa'),
        ('almanya', 'Almanya'),
        ('baska', 'Başka'),
    ]
    ACCOMMODATION_CHOICES = [
        ('otel', 'Otel'),
        ('pansiyon', 'Pansiyon'),
        ('butik', 'Butik Otel'),
        ('villa', 'Kiralık Villa/Ev'),
        ('apart', 'Apart Otel'),
        ('hostel', 'Hostel'),
        ('kamp', 'Kamp Alanı'),
        ('karavan', 'Karavan Parkı'),
        ('tatil_koyu', 'Tatil Köyü'),
    ]
    BUDGET_CHOICES = [
        ('ekonomik', 'Ekonomik'),
        ('orta', 'Orta Seviye'),
        ('luk', 'Lüks'),
        ('aralik', 'Belirli Aralık (örn: 0-1000 TL, 1001-3000 TL, 3000+ TL)'),
    ]
    ACTIVITY_CHOICES = [
        ('beach', 'Plaj/Deniz'),
        ('ski', 'Kayak/Snowboard'),
        ('trekking', 'Doğa Yürüyüşü/Trekking'),
        ('history', 'Tarihi Yerleri Gezme'),
        ('museum', 'Müze/Sanat Galerisi'),
        ('shopping', 'Alışveriş'),
        ('eating food', 'Yeme İçme'),
        ('spa', 'Dinlenme/Spa'),
        ('adventure', 'Macera Sporları'),
        ('gastronomy', 'Gastronomi Turları'),
        ('photography', 'Fotoğrafçılık'),
        ('festival', 'Festival/Etkinlikler'),
    ]
    SEASON_CHOICES = [
        ('yaz', 'Yaz'),
        ('kis', 'Kış'),
        ('ilkbahar', 'İlkbahar'),
        ('sonbahar', 'Sonbahar'),
    ]
    GEO_CHOICES = [
        ('deniz', 'Deniz/Sahil'),
        ('dag', 'Dağlık'),
        ('gol', 'Göl Kenarı'),
        ('orman', 'Ormanlık'),
        ('col', 'Çöl'),
        ('kirsal', 'Kırsal'),
        ('sehir', 'Şehir Merkezi'),
    ]
    FOOD_CHOICES = [
        ('yerel', 'Yerel Mutfağı Deneme'),
        ('deniz_urunleri', 'Deniz Ürünleri'),
        ('vejetaryen', 'Vejetaryen'),
        ('vegan', 'Vegan'),
        ('glutensiz', 'Glutensiz'),
        ('italyan', 'İtalyan Mutfağı'),
        ('asya', 'Asya Mutfağı'),
        ('sokak', 'Sokak Lezzetleri'),
        ('fine_dining', 'Fine Dining'),
    ]
    ENTERTAINMENT_CHOICES = [
        ('muzik', 'Canlı Müzik'),
        ('tiyatro', 'Tiyatro/Konser'),
        ('tema_park', 'Tema Parkları'),
        ('kulturel', 'Kültürel Etkinlikler'),
        ('avm', 'Alışveriş Merkezleri'),
        ('farketmez', 'Fark Etmez'),
    ]

    country = forms.ChoiceField(choices=COUNTRY_CHOICES, label='Ülke', required=True)
    accommodation = forms.ChoiceField(choices=ACCOMMODATION_CHOICES, label='Konaklama Türü', required=True)
    budget = forms.ChoiceField(choices=BUDGET_CHOICES, label='Bütçe', required=True)
    budget_range = forms.CharField(label='Bütçe Aralığı (örn: 0-1000 TL, 1001-3000 TL, 3000+ TL)', required=False)
    activities = forms.MultipleChoiceField(choices=ACTIVITY_CHOICES, widget=forms.CheckboxSelectMultiple, label='Aktiviteler', required=False)
    season = forms.ChoiceField(choices=SEASON_CHOICES, label='Mevsim', required=True)
    geo = forms.MultipleChoiceField(choices=GEO_CHOICES, widget=forms.CheckboxSelectMultiple, label='Coğrafi Özellikler', required=False)
    food = forms.MultipleChoiceField(choices=FOOD_CHOICES, widget=forms.CheckboxSelectMultiple, label='Yemek Tercihleri', required=False)
    entertainment = forms.MultipleChoiceField(choices=ENTERTAINMENT_CHOICES, widget=forms.CheckboxSelectMultiple, label='Eğlence Olanakları', required=False)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Başlangıç Tarihi', required=True)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Bitiş Tarihi', required=True)
    include_travel_time = forms.BooleanField(label='Ulaşım süreleri dahil edilsin mi?', required=False)

    