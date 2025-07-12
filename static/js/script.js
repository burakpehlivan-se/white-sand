document.addEventListener('DOMContentLoaded', () => {

    // Navigasyonlardaki aktif linki belirleme
    const currentPath = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('.navbar nav ul li a');

    navLinks.forEach(link => {
        // 'active' sınıfını temizle
        link.classList.remove('active');

        // Geçerli sayfaya göre 'active' sınıfını ekle
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
        // Profil sayfasındaysak, "Tatil Paketleri" linkinin aktifliğini kaldır
        if (currentPath === 'profile.html' && link.getAttribute('href') === '{% url "dashboard" %}' && link.textContent.includes('Tatil Paketleri')) {
            link.classList.remove('active');
        }
    });

    // Çıkış Yap butonu tüm sayfalarda çalışabilir
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (confirm('Çıkış yapmak istediğinizden emin misiniz?')) {
                alert('Çıkış yapıldı!');
                window.location.href = 'index.html'; // Giriş sayfasına yönlendir
            }
        });
    }

    // index.html için özel kodlar (slideshow ve modal)
    if (document.querySelector('.slideshow-container')) {
        const slideshowContainer = document.querySelector('.slideshow-container');
        const slideImages = document.querySelectorAll('.slide-image');

        const slideshowImageUrls = [];
        for (const key in slideshowContainer.dataset) {
            if (key.startsWith('imageUrl')) {
                slideshowImageUrls.push(slideshowContainer.dataset[key]);
            }
        }

        // Sort the URLs if they are not in order (e.g., imageUrl1, imageUrl10, imageUrl2)
        // This assumes keys are like 'imageUrl0', 'imageUrl1', etc.
        slideshowImageUrls.sort((a, b) => {
            const numA = parseInt(Object.keys(slideshowContainer.dataset).find(k => slideshowContainer.dataset[k] === a).replace('imageUrl', ''), 10);
            const numB = parseInt(Object.keys(slideshowContainer.dataset).find(k => slideshowContainer.dataset[k] === b).replace('imageUrl', ''), 10);
            return numA - numB;
        });

        let currentIndex = 0;
        let preloadedImages = [];

        function preloadAllImages() {
            slideshowImageUrls.forEach((src, index) => {
                const img = new Image();
                img.src = src;
                img.onload = () => {
                    // console.log(`Resim yüklendi: ${src}`);
                };
                img.onerror = () => {
                    console.error(`Resim yüklenemedi: ${src}`);
                };
                preloadedImages.push(img);
            });
        }

        function changeSlide() {
            const currentSlide = document.querySelector('.slideshow-container .active-slide');
            const nextSlide = currentSlide === slideImages[0] ? slideImages[1] : slideImages[0];

            const nextImageIndex = (currentIndex + 1) % slideshowImageUrls.length;
            const nextImageUrl = slideshowImageUrls[nextImageIndex];

            nextSlide.style.backgroundImage = `url('${nextImageUrl}')`;

            nextSlide.classList.add('active-slide');
            currentSlide.classList.remove('active-slide');

            currentIndex = nextImageIndex;
        }

        preloadAllImages();

        if (slideImages.length > 0 && slideshowImageUrls.length > 0) { // Check if slideshowImageUrls has items
            slideImages[0].style.backgroundImage = `url('${slideshowImageUrls[0]}')`;
            slideImages[0].classList.add('active-slide');
            setTimeout(() => {
                changeSlide();
                setInterval(changeSlide, 5000);
            }, 2000);
        }

        const authModal = document.getElementById('authModal');
        const openAuthModalBtn = document.getElementById('openAuthModal');
        const closeButton = document.querySelector('.close-button');

        const loginForm = document.getElementById("login");
        const registerForm = document.getElementById("register");
        const toggleBtnIndicator = document.getElementById("btn");

        // Sayfa yüklendiğinde login formunu aktif yap (varsayılan)
        if (loginForm) {
            loginForm.classList.add('active');
        }

        if (openAuthModalBtn) {
            openAuthModalBtn.addEventListener('click', () => {
                if (authModal) {
                    authModal.style.display = 'flex';
                }
            });
        }

        if (closeButton) {
            closeButton.addEventListener('click', () => {
                if (authModal) {
                    authModal.style.display = 'none';
                }
            });
        }

        window.addEventListener('click', (event) => {
            if (event.target == authModal) {
                authModal.style.display = 'none';
            }
        });

        // Toggle fonksiyonları (global olarak tanımlanmalı)
        window.register = function() {
            if (loginForm && registerForm && toggleBtnIndicator) {
                loginForm.classList.remove('active');
                registerForm.classList.add('active');
                toggleBtnIndicator.style.left = "140px";
            }
        }

        window.login = function() {
            if (loginForm && registerForm && toggleBtnIndicator) {
                registerForm.classList.remove('active');
                loginForm.classList.add('active');
                toggleBtnIndicator.style.left = "0";
            }
        }

        // Form submit olayları
        const loginFormElement = document.getElementById('login');
        if (loginFormElement) {
            loginFormElement.addEventListener('submit', function(e) {
                e.preventDefault();
                alert('Giriş yapılıyor...');
                if (authModal) {
                    authModal.style.display = 'none';
                }
                window.location.href = '{% url "dashboard" %}';
            });
        }

        const registerFormElement = document.getElementById('register');
        if (registerFormElement) {
            registerFormElement.addEventListener('submit', function(e) {
                e.preventDefault();
                alert('Kaydolunuyor...');
                if (typeof window.login === 'function') { // login fonksiyonunun varlığını kontrol et
                    window.login(); // Kayıttan sonra giriş formuna dön
                }
            });
        }

        const mainSearchInput = document.getElementById('mainSearchInput');
        const mainSearchBtn = document.getElementById('mainSearchBtn');

        if (mainSearchBtn && mainSearchInput) {
            mainSearchBtn.addEventListener('click', () => {
                const searchTerm = mainSearchInput.value.trim();
                if (searchTerm) {
                    alert(`"${searchTerm}" için tatil aranıyor...`);
                    window.location.href = 'dashboard.html';
                } else {
                    alert('Lütfen bir tatil yeri girin.');
                }
            });
        }
    } // End of index.html specific code


    // dashboard.html sayfası için özel kodlar (varsa)
    if (window.location.pathname.includes('{% url "dashboard" %}')) {
        // Arama ve filtreleme mantığı (eğer dashboard.html'de varsa)
        // Buraya dashboard'a özel arama ve filtreleme JS kodları gelecek
        const dashboardSearchInput = document.getElementById('dashboardSearchInput'); // Dashboard'daki arama inputu
        const dashboardSearchBtn = document.getElementById('dashboardSearchBtn'); // Dashboard'daki arama butonu
        const destinationFilter = document.getElementById('destinationFilter');
        const budgetFilter = document.getElementById('budgetFilter');
        const applyFiltersBtn = document.getElementById('applyFiltersBtn');
        const vacationCardsContainer = document.querySelector('.vacation-cards');

        // Örnek tatil verileri
        const allVacations = [
            { id: 1, name: 'Kapadokya Balon Turu', description: 'Sıcak hava balonlarıyla Kapadokya’nın eşsiz güzelliğini keşfedin.', price: '₺3.500', destination: 'Türkiye', budget: 'orta', image: 'images/cappadocia.jpg' },
            { id: 2, name: 'Paris Romantik Kaçamak', description: 'Eyfel Kulesi’nde romantik akşam yemeği.', price: '₺6.000', destination: 'Fransa', budget: 'yüksek', image: 'images/paris.jpg' },
            { id: 3, name: 'Maldivler Rüya Tatili', description: 'Hint Okyanusu’nun berrak sularında huzur bulun.', price: '₺12.000', destination: 'Maldivler', budget: 'lüks', image: 'images/maldives.jpg' },
            { id: 4, name: 'Antalya Yaz Eğlencesi', description: 'Akdeniz’in tadını çıkarın, otellerde eğlenin.', price: '₺4.200', destination: 'Türkiye', budget: 'orta', image: 'images/antalya.jpg' },
            { id: 5, name: 'Roma Tarih Turu', description: 'Antik Roma’nın büyüleyici tarihi ve sanatını keşfedin.', price: '₺5.200', destination: 'İtalya', budget: 'orta', image: 'images/rome.jpg' },
            { id: 6, name: 'Tayland Doğa Keşfi', description: 'Palmiye ağaçları ve egzotik tapınaklar arasında unutulmaz bir macera.', price: '₺7.500', destination: 'Tayland', budget: 'yüksek', image: 'images/thailand.jpg' }
        ];

        function displayVacationCards(vacations) {
            if (!vacationCardsContainer) return; // Element yoksa çık

            vacationCardsContainer.innerHTML = ''; // Mevcut kartları temizle
            if (vacations.length === 0) {
                vacationCardsContainer.innerHTML = '<p class="no-data-message" style="grid-column: 1 / -1;">Aradığınız kriterlere uygun tatil bulunamadı.</p>';
                return;
            }

            vacations.forEach(vacation => {
                const cardHtml = `
                    <div class="vacation-card">
                        <img src="${vacation.image}" alt="${vacation.name}">
                        <div class="card-info">
                            <h3>${vacation.name}</h3>
                            <p>${vacation.description}</p>
                            <div class="card-footer">
                                <span class="price"><i class="fas fa-lira-sign"></i> ${vacation.price.replace('₺', '')}</span>
                                <a href="detail.html?id=${vacation.id}" class="detail-btn"><i class="fas fa-info-circle"></i> Detay</a>
                            </div>
                        </div>
                    </div>
                `;
                vacationCardsContainer.insertAdjacentHTML('beforeend', cardHtml);
            });
        }

        function applyFiltersAndSearch() {
            const searchTerm = dashboardSearchInput ? dashboardSearchInput.value.toLowerCase() : '';
            const selectedDestination = destinationFilter ? destinationFilter.value : 'all';
            const selectedBudget = budgetFilter ? budgetFilter.value : 'all';

            const filteredVacations = allVacations.filter(vacation => {
                const matchesSearch = vacation.name.toLowerCase().includes(searchTerm) ||
                                      vacation.description.toLowerCase().includes(searchTerm) ||
                                      vacation.destination.toLowerCase().includes(searchTerm);
                const matchesDestination = selectedDestination === 'all' || vacation.destination.toLowerCase() === selectedDestination;
                const matchesBudget = selectedBudget === 'all' || vacation.budget === selectedBudget;

                return matchesSearch && matchesDestination && matchesBudget;
            });
            displayVacationCards(filteredVacations);
        }

        // Event Listener'lar
        if (dashboardSearchBtn) {
            dashboardSearchBtn.addEventListener('click', applyFiltersAndSearch);
        }
        if (applyFiltersBtn) {
            applyFiltersBtn.addEventListener('click', applyFiltersAndSearch);
        }
        if (dashboardSearchInput) {
            dashboardSearchInput.addEventListener('keyup', (e) => {
                if (e.key === 'Enter') {
                    applyFiltersAndSearch();
                }
            });
        }

        // Sayfa yüklendiğinde tüm kartları göster
        displayVacationCards(allVacations);
    } // End of dashboard.html specific code


    // recommendation-quiz.html sayfası için özel kodlar
    if (window.location.pathname.includes('recommendation-quiz.html')) {
        const quizBox = document.querySelector('.quiz-box');
        const quizSteps = document.querySelectorAll('.quiz-step');
        const progress = document.querySelector('.quiz-progress-bar .progress');
        const prevStepBtn = document.querySelector('.prev-step-btn');
        const nextStepBtn = document.querySelector('.next-step-btn');
        const startOverBtn = document.querySelector('.start-over-btn');
        const viewDetailBtn = document.querySelector('.view-detail-btn'); // Quiz sonucundaki detay butonu
        const recommendedVacationDiv = document.getElementById('recommendedVacation');

        let currentStep = 0;
        let userAnswers = {}; // Kullanıcının cevaplarını tutacak obje

        const quizQuestions = [
            // Soru 1: Seyahat Tercihi (tek seçim)
            {
                type: 'single',
                question: 'Seyahat tarzınız daha çok hangisine uygun?',
                name: 'travelStyle',
                options: [
                    { value: 'macera', text: 'Macera ve Keşif', icon: 'fas fa-mountain' },
                    { value: 'dinlence', text: 'Dinlence ve Huzur', icon: 'fas fa-umbrella-beach' },
                    { value: 'kultur', text: 'Kültür ve Tarih', icon: 'fas fa-archway' },
                    { value: 'eglence', text: 'Eğlence ve Sosyalleşme', icon: 'fas fa-cocktail' }
                ]
            },
            // Soru 2: Mevsim Tercihi (tek seçim)
            {
                type: 'single',
                question: 'Hangi mevsimde tatile çıkmayı tercih edersiniz?',
                name: 'season',
                options: [
                    { value: 'yaz', text: 'Yaz (Güneş & Deniz)', icon: 'fas fa-sun' },
                    { value: 'kis', text: 'Kış (Kar & Kayak)', icon: 'fas fa-snowflake' },
                    { value: 'ilkbahar', text: 'İlkbahar (Doğa & Canlılık)', icon: 'fas fa-leaf' },
                    { value: 'sonbahar', text: 'Sonbahar (Sakinlik & Renkler)', icon: 'fas fa-tree' }
                ]
            },
            // Soru 3: Aktivite Tercihleri (çoklu seçim)
            {
                type: 'multiple',
                question: 'Tatilinizde hangi aktiviteleri yapmaktan hoşlanırsınız? (Birden fazla seçilebilir)',
                name: 'activities',
                options: [
                    { value: 'yuruyus', text: 'Doğa Yürüyüşleri', icon: 'fas fa-hiking' },
                    { value: 'su_sporlari', text: 'Su Sporları', icon: 'fas fa-water' },
                    { value: 'muze_gezisi', text: 'Müze ve Sanat Galerisi Ziyaretleri', icon: 'fas fa-paint-brush' },
                    { value: 'alisveris', text: 'Alışveriş', icon: 'fas fa-shopping-bag' },
                    { value: 'yemek', text: 'Yöresel Lezzetleri Deneme', icon: 'fas fa-utensils' },
                    { value: 'yeme_içme', text: 'Yeme İçme', icon: 'fas fa-cocktail' }
                ]
            },
            // Soru 4: Bütçe Tercihi (tek seçim)
            {
                type: 'single',
                question: 'Tatil için ayırdığınız bütçe aralığı nedir?',
                name: 'budget',
                options: [
                    { value: 'ekonomik', text: 'Ekonomik (Uygun Fiyatlı)', icon: 'fas fa-wallet' },
                    { value: 'orta', text: 'Orta (Makul Fiyatlı)', icon: 'fas fa-dollar-sign' },
                    { value: 'yuksek', text: 'Yüksek (Konforlu ve Lüks)', icon: 'fas fa-hand-holding-usd' }
                ]
            }
        ];

        function updateQuizUI() {
            quizSteps.forEach((step, index) => {
                step.classList.remove('active-step');
                // Adım geçiş efektini korumak için transform değerini güncelle
                if (index < currentStep) {
                    step.style.transform = 'translateX(-100%)'; // Soldan dışarı
                } else if (index > currentStep) {
                    step.style.transform = 'translateX(100%)'; // Sağdan dışarı
                } else {
                    step.style.transform = 'translateX(0)'; // Ortada
                    step.classList.add('active-step');
                }
            });

            // Sonuç ekranını göstermek için
            if (currentStep === quizQuestions.length) {
                document.getElementById('resultStep').classList.add('active-step');
                displayRecommendation();
                nextStepBtn.style.display = 'none';
                prevStepBtn.style.display = 'none';
                startOverBtn.style.display = 'inline-flex';
            } else {
                document.getElementById('resultStep').classList.remove('active-step');
                nextStepBtn.style.display = 'inline-flex';
                // İlk adımda geri butonu gizli
                prevStepBtn.style.display = currentStep === 0 ? 'none' : 'inline-flex';
                startOverBtn.style.display = 'none';
            }

            updateProgressBar();
        }

        function updateProgressBar() {
            const progressPercentage = (currentStep / quizQuestions.length) * 100;
            progress.style.width = `${progressPercentage}%`;
        }

        function generateQuizSteps() {
            const quizStepsContainer = document.querySelector('.quiz-steps');
            quizQuestions.forEach((q, qIndex) => {
                const stepDiv = document.createElement('div');
                stepDiv.className = 'quiz-step';
                stepDiv.dataset.step = qIndex;

                let optionsHtml = '';
                if (q.type === 'single') {
                    optionsHtml = `<div class="options-grid">`;
                    q.options.forEach(opt => {
                        optionsHtml += `
                            <button class="option-btn" data-name="${q.name}" data-value="${opt.value}">
                                <i class="${opt.icon}"></i>
                                <span>${opt.text}</span>
                            </button>
                        `;
                    });
                    optionsHtml += `</div>`;
                } else if (q.type === 'multiple') {
                    optionsHtml = `<div class="options-grid checkbox-options">`;
                    q.options.forEach(opt => {
                        optionsHtml += `
                            <label class="option-checkbox">
                                <input type="checkbox" data-name="${q.name}" value="${opt.value}">
                                <i class="${opt.icon}"></i>
                                <span>${opt.text}</span>
                            </label>
                        `;
                    });
                    optionsHtml += `</div>`;
                }

                stepDiv.innerHTML = `
                    <h3>${q.question}</h3>
                    ${optionsHtml}
                `;
                quizStepsContainer.insertBefore(stepDiv, document.getElementById('resultStep'));
            });

            // Option butonları ve checkboxlar için event listener'lar
            document.querySelectorAll('.option-btn').forEach(button => {
                button.addEventListener('click', (e) => {
                    const name = e.currentTarget.dataset.name;
                    const value = e.currentTarget.dataset.value;

                    // Tekli seçimde aynı soruya ait diğer seçenekleri de-select yap
                    document.querySelectorAll(`.option-btn[data-name="${name}"]`).forEach(btn => {
                        btn.classList.remove('selected');
                    });
                    e.currentTarget.classList.add('selected');

                    userAnswers[name] = value;
                    console.log(userAnswers);
                });
            });

            document.querySelectorAll('.option-checkbox input[type="checkbox"]').forEach(checkbox => {
                checkbox.addEventListener('change', (e) => {
                    const name = e.currentTarget.dataset.name;
                    const value = e.currentTarget.value;
                    const label = e.currentTarget.closest('label');

                    if (!userAnswers[name]) {
                        userAnswers[name] = [];
                    }

                    if (e.currentTarget.checked) {
                        if (!userAnswers[name].includes(value)) {
                            userAnswers[name].push(value);
                        }
                        label.classList.add('selected'); // Checkbox etiketi için de selected sınıfı
                    } else {
                        userAnswers[name] = userAnswers[name].filter(item => item !== value);
                        label.classList.remove('selected');
                    }
                    console.log(userAnswers);
                });
            });
        }

        function displayRecommendation() {
            // Basit bir öneri algoritması
            let recommendation = {
                title: 'Harika Bir Tatil Sizi Bekliyor!',
                description: 'Cevaplarınıza göre size özel bir tatil paketi önerimiz var:',
                vacation: null // Önerilen tatil bilgisi
            };

            const style = userAnswers.travelStyle;
            const season = userAnswers.season;
            const activities = userAnswers.activities || [];
            const budget = userAnswers.budget;

            if (style === 'macera' && season === 'yaz' && budget !== 'ekonomik') {
                recommendation.vacation = {
                    name: 'Kapadokya Macera Paketi',
                    details: 'Balon turları, ATV safarileri ve yer altı şehirleri keşfi ile dolu unutulmaz bir macera.',
                    image: 'images/cappadocia.jpg'
                };
            } else if (style === 'dinlence' && season === 'yaz' && budget === 'yuksek') {
                recommendation.vacation = {
                    name: 'Maldivler Lüks Balayı',
                    details: 'Kristal berraklığında sular, özel villalar ve eşsiz su altı deneyimleri.',
                    image: 'images/maldives.jpg'
                };
            } else if (style === 'kultur' && (season === 'ilkbahar' || season === 'sonbahar')) {
                recommendation.vacation = {
                    name: 'Roma Tarih ve Lezzet Turu',
                    details: 'Antik Roma’nın büyüleyici tarihi ve sanatını keşfedin.',
                    image: 'images/rome.jpg'
                };
            } else if (style === 'eglence' && season === 'yaz' && activities.includes('gece_hayatı')) {
                recommendation.vacation = {
                    name: 'Mykonos Parti Tatili',
                    details: 'Canlı gece hayatı, plaj partileri ve Ege Denizi’nin keyfini çıkarın.',
                    image: 'https://via.placeholder.com/300x200/F0F2F5/666666?text=Mykonos'
                };
            } else if (style === 'dinlence' && season === 'kis') {
                recommendation.vacation = {
                    name: 'Uludağ Kayak Tatili',
                    details: 'Beyazların içinde huzur dolu bir kış kaçamağı.',
                    image: 'https://via.placeholder.com/300x200/F0F2F5/666666?text=Uludağ'
                };
            } else {
                recommendation.vacation = {
                    name: 'Size Özel Bir Tatil',
                    details: 'Cevaplarınıza göre en uygun tatili bulmak için daha fazla seçenek sunabiliriz. Lütfen bizimle iletişime geçin veya ana sayfadaki paketlerimize göz atın.',
                    image: 'https://via.placeholder.com/300x200/F0F2F5/666666?text=Tatil+Önerisi'
                };
            }

            recommendedVacationDiv.innerHTML = `
                <h4>${recommendation.vacation.name}</h4>
                <img src="${recommendation.vacation.image}" alt="${recommendation.vacation.name}" class="recommended-img">
                <p>${recommendation.vacation.details}</p>
                <a href="dashboard.html" class="view-detail-btn"><i class="fas fa-search"></i> Diğer Paketleri İncele</a>
            `;
        }

        nextStepBtn.addEventListener('click', () => {
            // Mevcut adımın cevaplarının seçili olup olmadığını kontrol et
            const currentQuestion = quizQuestions[currentStep];
            let isValid = true;

            if (currentQuestion.type === 'single') {
                if (!userAnswers[currentQuestion.name]) {
                    isValid = false;
                    alert('Lütfen bir seçim yapın.');
                }
            } else if (currentQuestion.type === 'multiple') {
                if (!userAnswers[currentQuestion.name] || userAnswers[currentQuestion.name].length === 0) {
                    isValid = false;
                    alert('Lütfen en az bir seçim yapın.');
                }
            }

            if (isValid) {
                currentStep++;
                updateQuizUI();
            }
        });

        prevStepBtn.addEventListener('click', () => {
            currentStep--;
            updateQuizUI();
        });

        startOverBtn.addEventListener('click', () => {
            currentStep = 0;
            userAnswers = {}; // Cevapları sıfırla
            document.querySelectorAll('.option-btn.selected').forEach(btn => btn.classList.remove('selected'));
            document.querySelectorAll('.option-checkbox input[type="checkbox"]').forEach(cb => {
                cb.checked = false;
                cb.closest('label').classList.remove('selected');
            });
            updateQuizUI();
        });

        // Quiz adımlarını oluştur
        generateQuizSteps();
        // İlk adımda UI'ı güncelle
        updateQuizUI();
    } // End of recommendation-quiz.html specific code


    // Profil Sayfası İşlevselliği
    if (window.location.pathname.includes('profile.html')) {
        const profileImage = document.getElementById('profileImage');
        const avatarUpload = document.getElementById('avatarUpload');
        const editButtons = document.querySelectorAll('.profile-details .edit-btn');
        const saveButton = document.querySelector('.profile-details .save-btn');
        const cancelButton = document.querySelector('.profile-details .cancel-btn');
        const changePasswordButton = document.querySelector('.change-password-btn');

        let originalValues = {}; // Alanların orijinal değerlerini saklamak için

        // Profil resmi yükleme
        if (avatarUpload && profileImage) {
            avatarUpload.addEventListener('change', function() {
                const file = this.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        profileImage.src = e.target.result;
                    };
                    reader.readAsDataURL(file);
                    alert('Profil resmi güncellendi!');
                }
            });
        }

        // Düzenleme butonları için event listener
        editButtons.forEach(button => {
            button.addEventListener('click', function() {
                const fieldId = this.dataset.field;
                const inputField = document.getElementById(fieldId);

                if (inputField) {
                    // Orijinal değeri sakla
                    originalValues[fieldId] = inputField.value;

                    inputField.removeAttribute('readonly');
                    inputField.focus();
                    this.style.display = 'none'; // Düzenle butonunu gizle

                    // Kaydet ve İptal butonlarını göster
                    if (saveButton) saveButton.style.display = 'inline-flex';
                    if (cancelButton) cancelButton.style.display = 'inline-flex';
                }
            });
        });

        // Kaydet butonu
        if (saveButton) {
            saveButton.addEventListener('click', function() {
                // Değişiklikleri kaydetme mantığı buraya gelecek (örneğin AJAX ile sunucuya gönderme)
                alert('Profil bilgileri kaydedildi!');

                // Tüm inputları tekrar readonly yap
                document.querySelectorAll('.profile-details input').forEach(input => {
                    input.setAttribute('readonly', true);
                });

                // Butonları gizle/göster
                editButtons.forEach(btn => btn.style.display = 'inline-flex');
                saveButton.style.display = 'none';
                cancelButton.style.display = 'none';
            });
        }

        // İptal butonu
        if (cancelButton) {
            cancelButton.addEventListener('click', function() {
                // Değişiklikleri geri al
                for (const fieldId in originalValues) {
                    const inputField = document.getElementById(fieldId);
                    if (inputField) {
                        inputField.value = originalValues[fieldId];
                    }
                }

                // Tüm inputları tekrar readonly yap
                document.querySelectorAll('.profile-details input').forEach(input => {
                    input.setAttribute('readonly', true);
                });

                // Butonları gizle/göster
                editButtons.forEach(btn => btn.style.display = 'inline-flex');
                saveButton.style.display = 'none';
                cancelButton.style.display = 'none';
                alert('Değişiklikler iptal edildi.');
            });
        }

        // Şifre Değiştirme Modalı İşlevselliği
        const changePasswordModal = document.getElementById('changePasswordModal');
        const openChangePasswordModalBtn = document.querySelector('.change-password-btn');
        const closeChangePasswordModalBtn = document.getElementById('closePasswordModal');
        const passwordChangeForm = document.getElementById('passwordChangeForm');

        if (openChangePasswordModalBtn) {
            openChangePasswordModalBtn.addEventListener('click', () => {
                if (changePasswordModal) {
                    changePasswordModal.style.display = 'flex'; // Modalı görünür yap
                }
            });
        }

        if (closeChangePasswordModalBtn) {
            closeChangePasswordModalBtn.addEventListener('click', () => {
                if (changePasswordModal) {
                    changePasswordModal.style.display = 'none'; // Modalı gizle
                }
                if (passwordChangeForm) {
                    passwordChangeForm.reset(); // Formu sıfırla
                }
            });
        }

        // Modal dışına tıklayınca kapatma
        window.addEventListener('click', (event) => {
            if (event.target == changePasswordModal) {
                changePasswordModal.style.display = 'none';
                if (passwordChangeForm) {
                    passwordChangeForm.reset();
                }
            }
        });

        // Şifre değiştirme formu submit olduğunda
        if (passwordChangeForm) {
            passwordChangeForm.addEventListener('submit', function(e) {
                e.preventDefault();

                const currentPassword = this.querySelector('input[placeholder="Mevcut Şifre"]').value;
                const newPassword = this.querySelector('input[placeholder="Yeni Şifre"]').value;
                const confirmNewPassword = this.querySelector('input[placeholder="Yeni Şifre (Tekrar)"]').value;

                if (!currentPassword || !newPassword || !confirmNewPassword) {
                    alert('Lütfen tüm şifre alanlarını doldurun.');
                    return;
                }

                if (newPassword !== confirmNewPassword) {
                    alert('Yeni şifreler uyuşmuyor. Lütfen kontrol edin.');
                    return;
                }

                if (newPassword.length < 6) {
                    alert('Yeni şifre en az 6 karakter olmalıdır.');
                    return;
                }

                alert('Şifreniz başarıyla güncellendi!');
                console.log('Mevcut Şifre:', currentPassword);
                console.log('Yeni Şifre:', newPassword);

                if (changePasswordModal) {
                    changePasswordModal.style.display = 'none';
                }
                this.reset();
            });
        }

        // Dummy rezervasyon verileri
        const dummyReservations = [
            {
                id: 1,
                destination: "Kapadokya Balon Turu",
                date: "2024-08-15 - 2024-08-17",
                guests: 2,
                status: "confirmed"
            },
            {
                id: 2,
                destination: "Paris Romantik Kaçamak",
                date: "2025-01-20 - 2025-01-24",
                guests: 1,
                status: "pending"
            },
            {
                id: 3,
                destination: "Maldivler Balayı Paketi",
                date: "2023-06-10 - 2023-06-17",
                guests: 2,
                status: "cancelled"
            }
        ];

        // Dummy favori paket verileri
        const dummyFavorites = [
            {
                id: 101,
                name: "Roma Tarih Turu",
                description: "Antik Roma’nın büyüleyici tarihi ve sanatını keşfedin.",
                price: "₺5.200",
                image: "https://via.placeholder.com/300x200/F0F2F5/666666?text=Roma"
            },
            {
                id: 102,
                name: "Bali Yoga Kampı",
                description: "Endonezya’nın huzurlu Bali adasında ruhunuzu dinlendirin.",
                price: "₺7.800",
                image: "https://via.placeholder.com/300x200/F0F2F5/666666?text=Bali"
            }
        ];

        // Rezervasyonları yükle
        const reservationsList = document.querySelector('.reservations-list');
        const noReservationsMessage = document.getElementById('noReservations');
        if (reservationsList && noReservationsMessage) {
            if (dummyReservations.length > 0) {
                noReservationsMessage.style.display = 'none';
                dummyReservations.forEach(reservation => {
                    const statusClass = reservation.status === 'confirmed' ? 'confirmed' :
                                        (reservation.status === 'pending' ? 'pending' : 'cancelled');
                    const reservationCard = `
                        <div class="reservation-card">
                            <h3>${reservation.destination}</h3>
                            <p><strong>Tarih:</strong> ${reservation.date}</p>
                            <p><strong>Misafir Sayısı:</strong> ${reservation.guests}</p>
                            <span class="status-badge ${statusClass}">${reservation.status === 'confirmed' ? 'Onaylandı' : (reservation.status === 'pending' ? 'Beklemede' : 'İptal Edildi')}</span>
                        </div>
                    `;
                    reservationsList.insertAdjacentHTML('beforeend', reservationCard);
                });
            } else {
                noReservationsMessage.style.display = 'block';
            }
        }

        // Favori paketleri yükle
        const favoritePackagesList = document.querySelector('.favorite-packages-list');
        const noFavoritesMessage = document.getElementById('noFavorites');
        if (favoritePackagesList && noFavoritesMessage) {
            if (dummyFavorites.length > 0) {
                noFavoritesMessage.style.display = 'none';
                dummyFavorites.forEach(favPackage => {
                    const favoriteCard = `
                        <div class="favorite-package-card">
                            <h3>${favPackage.name}</h3>
                            <p>${favPackage.description}</p>
                            <div class="fav-actions">
                                <span class="price">${favPackage.price}</span>
                                <a href="#" class="view-detail-btn"><i class="fas fa-info-circle"></i> Detay</a>
                                <button class="remove-fav-btn" data-id="${favPackage.id}"><i class="fas fa-times-circle"></i> Favorilerden Kaldır</button>
                            </div>
                        </div>
                    `;
                    favoritePackagesList.insertAdjacentHTML('beforeend', favoriteCard);
                });

                // Favorilerden Kaldır butonları için event listener
                document.querySelectorAll('.remove-fav-btn').forEach(button => {
                    button.addEventListener('click', function() {
                        const packageId = this.dataset.id;
                        if (confirm(`ID'si ${packageId} olan paketi favorilerden kaldırmak istediğinizden emin misiniz?`)) {
                            this.closest('.favorite-package-card').remove();
                            alert('Paket favorilerden kaldırıldı.');
                            // Burada favori listesinden gerçek kaldırma işlemi yapılmalı
                            if (favoritePackagesList.children.length === 0 || (favoritePackagesList.children.length === 1 && favoritePackagesList.children[0].id === 'noFavorites')) {
                                noFavoritesMessage.style.display = 'block';
                            }
                        }
                    });
                });
            } else {
                noFavoritesMessage.style.display = 'block';
            }
        }
    } // End of profile.html specific code

}); // End of DOMContentLoaded