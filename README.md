# Global Video Game Market Intelligence

Performed data cleaning, missing-value analysis and datatype transformations using Pandas.
## Hipotez Testi 1 (Eleştirmen Puanı ve Satış İlişkisi)

**Araştırma Sorusu:** Eleştirmenlerden yüksek puan alan oyunların satışları gerçekten daha yüksek mi?

- **Grup 1:** Critic Score >= 80
- **Grup 2:** Critic Score < 80[cite: 4]

İki grubun satış ortalamaları arasında Bağımsız Çift Örneklem T-Testi (Independent T-Test) uygulanmış ve P-Değeri (p-value) `1.09e-116` (p < 0.05) olarak bulunmuştur. 

**Değerlendirme:**
Sonuç, eleştirmen değerlendirmesi ile ticari başarı arasında istatistiksel olarak anlamlı bir ilişki bulunduğunu göstermektedir.[cite: 4]

##  Hipotez Testi 2 (Japonya Pazarında RPG Etkisi)

**Araştırma Sorusu:** RPG oyunlarının Japonya satışları diğer türlerden farklı mı?

- **Grup 1:** RPG (Role-Playing)[cite: 4]
- **Grup 2:** Non-RPG (Diğer Türler)[cite: 4]

Japonya satışları (JP_Sales) üzerinden yapılan Bağımsız Çift Örneklem T-Testi sonucunda P-Değeri `7.42e-97` (p < 0.05) olarak bulunmuştur.

**Değerlendirme:**
Sonuç, Japonya pazarında RPG oyunlarının satışları ile diğer oyun türlerinin satışları arasında istatistiksel olarak anlamlı çok net bir fark bulunduğunu kanıtlamaktadır.

##  Hipotez Testi 3 (Action ve Sports Karşılaştırması)

**Araştırma Sorusu:** Action ve Sports oyunlarının ortalama global satışları arasında anlamlı fark var mı?[cite: 4]

- **H0:** $\mu_{action} = \mu_{sports}$[cite: 4]
- **H1:** $\mu_{action} \neq \mu_{sports}$[cite: 4]

Global satışlar (Global_Sales) üzerinden yapılan Bağımsız Çift Örneklem T-Testi sonucunda P-Değeri `0.26` (p > 0.05) olarak bulunmuştur.

**Değerlendirme:**
Sonuç, Action ve Sports türündeki oyunların küresel satış ortalamaları arasında istatistiksel olarak anlamlı bir fark bulunmadığını göstermektedir. İki türün pazardaki ticari başarı potansiyeli birbirine benzerlik göstermektedir.
## Veritabanı Entegrasyonu (SQL + Python)

Projenin son aşamasında temizlenmiş veri seti `SQLite` kullanılarak `games.db` adında bir ilişkisel veritabanına aktarılmıştır. Ardından gelişmiş SQL sorguları doğrudan Python üzerinden çalıştırılmış ve sonuçlar `Pandas DataFrame` formatına dönüştürülerek entegre bir veri boru hattı (data pipeline) kurulmuştur.

**Öne Çıkan SQL Analizleri:**
- `CASE WHEN` yapısı kullanılarak 2000'ler ve 2010'lar dönemlerinin satış hacmi ve oyun üretim adetleri bakımından karşılaştırılması.
- Amerika (NA) ve Avrupa (EU) oyuncu tercihlerinin bölgesel bazda kıyaslanması.
- Tüm zamanların en üretken 10 yayıncısının (Publisher) ve en çok satan konsollarının tespit edilmesi.
- Her oyun türünün (Genre) kendi içindeki maksimum (`MAX`) satış yapan lider oyunlarının bulunması.

*Not: Bu aşama, analiz süreçlerinde Python (Pandas) ve SQL teknolojilerinin entegre kullanımını (Python to SQL Connection) sergilemek amacıyla kurgulanmıştır.*
##  Veri Görselleştirme ve Bölgesel Oyuncu Davranışı

Projenin son safhasında `Matplotlib` ve `Seaborn` kütüphaneleri kullanılarak verinin görsel analizi (Scatter Plot, Box Plot, Heatmap) gerçekleştirilmiştir.

**Bölgesel Pazar Analizi Sonuçları:**
Üç ana pazarın (Kuzey Amerika, Avrupa ve Japonya) favori oyun türleri analiz edildiğinde, Kuzey Amerika ve Avrupa (Batı) pazarlarında **Action, Sports ve Shooter** türlerinin baskın olduğu tespit edilmiştir. Buna karşılık Japonya pazarında **Role-Playing (RPG)** türü açık ara lider konumdadır.

**Sonuç:**
Japonya pazarı ile Batı pazarlarında oyun türü tercihlerinin ciddi şekilde farklılaştığı görülmektedir.[cite: 7]

## Yönetsel Tavsiyeler

Yeni bir oyun projesine yatırım yapacak bir oyun stüdyosu için veri setinden çıkarılan stratejik eylem planı aşağıdadır:

- **Hedef Tür (Genre):** Küresel gelir maksimizasyonu için **Action** veya **Sports** türü seçilmelidir.
- **Hedef Platform:** Satış hacmi ve pazar penetrasyonu en yüksek olan **PlayStation** ekosistemi önceliklendirilmelidir.
- **Hedef Pazar:** Gelirin çok büyük bir kısmını oluşturan **Kuzey Amerika (NA)** ve **Avrupa (EU)** pazarları hedeflenmelidir (Ancak Japonya pazarına özel bir giriş yapılacaksa tür kesinlikle Role-Playing olarak değiştirilmelidir).
- **Kalite Hedefi (Critic Score):** Oyunun eleştirmen puanının **80 ve üzeri** olması hedeflenmelidir. Veriler, 80 üzeri puanların satışları istatistiksel olarak anlamlı ölçüde artırdığını kanıtlamaktadır.

---

##  Key Findings (Özet Bulgular)

Tüm veri temizliği, istatistiksel analizler, SQL sorguları ve görselleştirmeler sonucunda elde edilen temel bulgular:

* Küresel oyun satışları (Global_Sales) güçlü bir şekilde sağa çarpık (right-skewed) dağılım göstermektedir; pazarın büyük bir kısmı %1'lik hit oyunlar tarafından domine edilmektedir.
* Japon oyuncuların tür tercihleri (özellikle RPG hakimiyeti), Kuzey Amerika ve Avrupa pazarlarından istatistiksel olarak tamamen farklı (izole) bir yapıdadır.
* Aksiyon ve Spor oyunlarının küresel satış ortalamaları arasında istatistiksel olarak anlamlı bir fark yoktur (İkisi de benzer risk/ödül profiline sahiptir).
* Electronic Arts, Nintendo ve Activision gibi dev yayıncılar, hem piyasaya sürülen oyun hacmini hem de toplam satış gelirlerini ezici bir şekilde domine etmektedir.
* Yüksek eleştirmen puanı (Critic Score) ile küresel satışlar arasında pozitif yönlü, matematiksel olarak kanıtlanmış bir ilişki bulunmaktadır.