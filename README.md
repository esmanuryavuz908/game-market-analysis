# 🎮 Global Video Game Market Intelligence & İstatistiksel Analiz

Bu proje, küresel video oyunu satış verilerini analiz ederek oyun pazarındaki başarı faktörlerini, bölgesel oyuncu davranışlarını, eleştirmen puanlarının ticari etkiye katkısını ve platform dinamiklerini inceleyen uçtan uca bir **Veri Analitiği ve İstatistiksel Modelleme** çalışmasıdır.

 Proje; veri temizleme (data cleaning), keşifçi veri analizi (EDA), SQL veritabanı yönetimi, hipotez testleri ve veri görselleştirme süreçlerinin tamamını kapsar.

---

## 📌 Proje Senaryosu ve İş Hedefleri

**Rol:** Junior Data Analyst / Data Scientist  
**Amaç:** Sektöre yeni girecek veya yeni bir oyun geliştirmeyi planlayan bir oyun stüdyosuna veri odaklı stratejik kararlar almasında rehberlik etmek.

### Yanıt Aranan Temel İş Soruları:
1. Hangi oyun türleri ve platformlar küresel ve bölgesel ölçekte en yüksek geliri sağlıyor?
2. Kuzey Amerika (NA), Avrupa (EU) ve Japonya (JP) pazarlarındaki oyuncu tercihleri nasıl farklılaşıyor?
3. Eleştirmen puanı (**Critic Score**) ile satış başarısı arasında istatistiksel olarak anlamlı bir ilişki var mı?
4. Farklı türlerin (ör. Action vs. Sports) satış ortalamaları arasında istatistiksel bir fark bulunuyor mu?
5. Hangi yayıncı (Publisher) ve platform kombinasyonları pazara hakim durumdadır?

---

## 🗂️ Proje Klasör Yapısı

```text
game_market_analysis/
│
├── data/
│   └── video_games.csv           # Kaggle'dan indirilen ham veri seti
│
├── database/
│   └── games.db                  # Temizlenmiş verilerden oluşturulan SQLite veritabanı
│
├── notebooks/
│   └── analysis.ipynb            # Detaylı EDA ve Hipotez Testlerinin yer aldığı Jupyter Notebook
│
├── src/
│   └── main.py                   # Veri işleme, ETL ve SQL aktarımını sağlayan Python betiği
│
├── outputs/
│   ├── charts/                   # Üretilen grafikler (PNG formatında)
│   └── reports/                  # İstatistiksel özet raporlar
│
└── README.md                     # Proje dokümantasyonu
```

---

## 🛠️ Kullanılan Teknolojiler ve Yöntemler

| Aşama | Araç / Kütüphane | Gerçekleştirilen İşlemler |
| :--- | :--- | :--- |
| **Veri Temizleme** | `Pandas` | Eksik veri analizi, veri tipi dönüşümleri, mükerrer (duplicate) kayıt ayıklama |
| **Değişken Mühendisliği** | `Pandas` | `Main_Market` (Ana Pazar), `Sales_Category` (Satış Seviyesi), `Era` (Dönem) sütunları oluşturma |
| **Tanımlayıcı İstatistik** | `NumPy`, `SciPy` | Ortalama, medyan, standart sapma, IQR, çarpıklık (skewness) ve Z-Score analizi ($Z > 3$) |
| **Olasılık Analizi** | `Python`, `SciPy` | Koşullu olasılık hesaplamaları $P(\text{Yüksek Satış} \mid \text{Tür})$ |
| **Hipotez Testleri** | `SciPy.stats` | İki örneklem t-testi ve ANOVA ile p-değeri ($p$-value) analizi |
| **Veritabanı & SQL** | `SQLite3`, `Pandas` | Veri tabanı şeması oluşturma, karmaşık SQL sorguları, GROUP BY, JOIN ve filtrelemeler |
| **Veri Görselleştirme** | `Matplotlib`, `Seaborn` | Çizgi, sütun, histogram, kutu (box plot) grafikleri ve korelasyon ısı haritası (heatmap) |

---

## 🔬 Analitik ve İstatistiksel Süreç

### 1. Veri Temizleme & Yeni Değişkenler
* `Year`, `Publisher`, `Critic_Score` ve `User_Score` alanlarındaki eksik veriler incelendi ve uygun yöntemlerle işlendi.
* Yeni değişkenler türetildi:
  * **`Main_Market`**: Oyunun en çok sattığı bölge (North America, Europe, Japan, Other).
  * **`Sales_Category`**: Satış hacmine göre segmentasyon (`Low`, `Medium`, `High`, `Blockbuster`).
  * **`Era`**: Çıkış yıllarına göre dönem kategorizasyonu (1980s, 1990s, 2000s, 2010s+).

### 2. İstatistiksel Dağılım ve Hipotez Testleri
* **Dağılım Analizi:** Oyun satışlarının sağa çarpık (right-skewed) olduğu belirlendi. Birkaç popüler oyunun (Blockbuster) ortalamayı ciddi şekilde yukarı çektiği görüldü.
* **Hipotez Testi 1 (Eleştirmen Puanı vs. Satış):**
  * $H_0$: Yüksek eleştirmen puanına sahip oyunlar ($\text{Score} \ge 80$) ile düşük puanlı oyunların satış ortalamaları arasında fark yoktur.
  * $H_1$: Yüksek eleştirmen puanına sahip oyunların satış ortalaması daha yüksektir.
  * **Sonuç:** $p < 0.05$ bulunarak $H_0$ reddedildi. Eleştirmen değerlendirmesi ile ticari başarı arasında istatistiksel olarak anlamlı bir ilişki vardır.
* **Hipotez Testi 2 (Bölgesel Oyuncu Tercihleri):**
  * Japonya pazarındaki RPG (Role-Playing) oyunlarının satış oranları Batı pazarlarıyla karşılaştırıldı ve bölgesel farkın istatistiksel olarak anlamlı olduğu doğrulandı.

### 3. SQL Veritabanı ve Sorgular
Temizlenen veri seti SQLite `games.db` veritabanına Aktarıldı ve şu sorgular çalıştırıldı:
* En çok satan ilk 10 oyun ve tür bazlı toplam satışlar.
* Platformların yıllara göre pazar payı değişimleri.
* Eleştirmen puanı 80 üzeri olup Avrupa satışı Amerika satışından yüksek olan oyunlar.

```sql
-- Tür Bazında Küresel Satış İstatistikleri Sorgusu
SELECT 
    Genre,
    COUNT(*) AS Total_Games,
    ROUND(SUM(Global_Sales), 2) AS Total_Global_Sales,
    ROUND(AVG(Global_Sales), 2) AS Avg_Sales_Per_Game
FROM games
GROUP BY Genre
ORDER BY Total_Global_Sales DESC;
```

---

## 📈 Öne Çıkan Bulgular ve Stratejik Öneriler

1. **Bölgesel Tercihler:** Kuzey Amerika ve Avrupa pazarlarında **Action**, **Sports** ve **Shooter** türleri baskınken; Japonya pazarında **Role-Playing (RPG)** ve el konsolu platformları açık ara liderdir.
2. **Kalite Etkisi:** `Critic_Score >= 80` olan oyunların ortalama satışı, ortalama puanlı oyunlara kıyasla katlanarak artmaktadır.
3. **Pazar Yoğunlaşması:** Satışların büyük çoğunluğu $Z \ge 3$ Z-skoruna sahip az sayıda hit oyun tarafından üretilmektedir.

---

## 🚀 Kurulum ve Kullanım

### Ön Koşullar
* Python 3.9 veya üzeri bir sürümün yüklü olması gerekmektedir.

### Adımlar

1. Bu depoyu klonlayın:
   ```bash
  git clone https://github.com/esmanuryavuz908/game-market-analysis.git
cd game-market-analysis
   ```

2. Sanal ortam oluşturun ve aktif edin (Opsiyonel):
   ```bash
   python -m venv venv
   # Windows için:
   venv\Scripts\activate
   # macOS/Linux için:
   source venv/bin/activate
   ```

3. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install pandas numpy matplotlib seaborn scipy
   ```

4. Ana analiz betiğini çalıştırın:
   ```bash
   python src/main.py
   ```

---


