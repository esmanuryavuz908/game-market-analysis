import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import scipy.stats as stats
df = pd.read_csv('../data/Video_Games_Sales_as_at_22_Dec_2016.csv')
print(df.head())
print(df.shape)
print(df.columns)
print(df.info())
print(df.isnull().sum())
print("Farklı Platform Sayısı:", df['Platform'].nunique())
print("Farklı Oyun Türü Sayısı:", df['Genre'].nunique())
print(df.duplicated().sum())
df['User_Score'] = pd.to_numeric(df['User_Score'], errors='coerce')
print(df['User_Score'].dtype)
df = df.dropna(subset=['Name', 'Genre', 'Year_of_Release'])
games_clean = df.copy()
print(games_clean.info())
print(games_clean.isnull().sum())
print(games_clean.shape)
games_clean['Main_Market'] =games_clean[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].idxmax(axis=1)
games_clean['Sales_Category'] = pd.cut(games_clean['Global_Sales'], bins=[0, 1, 5, 20, 100], labels=['Low', 'Medium', 'High', 'Blockbuster'])
games_clean['Era'] = pd.cut(games_clean['Year_of_Release'], bins=[1979, 1989, 1999, 2009, 2019, 2025], labels=['1980-1989', '1990-1999', '2000-2009', '2010-2019', '2020+'])
print(games_clean[['Name', 'Year_of_Release', 'Era']].head(10))
print("--- Global Satış İstatistikleri ---")
print("Ortalama (Mean):", np.mean(games_clean['Global_Sales']))
print("Medyan (Median):", np.median(games_clean['Global_Sales']))
print("Standart Sapma (Std):", np.std(games_clean['Global_Sales']))
print("Varyans (Var):", np.var(games_clean['Global_Sales']))
print("Minimum Satış:", np.min(games_clean['Global_Sales']))
print("Maksimum Satış:", np.max(games_clean['Global_Sales']))
yuzdelikler = np.percentile(games_clean['Global_Sales'], [25, 50, 75, 90])
print("25. Yüzdelik (Q1):", yuzdelikler[0])
print("50. Yüzdelik (Q2 - Medyan):", yuzdelikler[1])
print("75. Yüzdelik (Q3):", yuzdelikler[2])
print("90. Yüzdelik:", yuzdelikler[3])
istenen = len(games_clean[games_clean['Global_Sales'] > 1])
tumu = len(games_clean)
olasilik_1 = istenen / tumu

print("1 Milyon üzeri satma olasılığı:", olasilik_1)
action_oyunlari = games_clean[games_clean['Genre'] == 'Action']
tumu = len(action_oyunlari)
istenen = len(action_oyunlari[action_oyunlari['Global_Sales'] > 1])
olasilik_2 = istenen / tumu
print("Aksiyon oyunlarının 1 milyon üzeri satma olasılığı:", olasilik_2)
jp_basarili = games_clean[games_clean['JP_Sales'] > 1]
tumu_jp = len(jp_basarili)
istenen_rpg = len(jp_basarili[jp_basarili['Genre'] == 'Role-Playing'])
olasilik_3 = istenen_rpg / tumu_jp
print("Japonya'da başarılıysa RPG olma olasılığı:", olasilik_3)
tumu_genel = len(games_clean)
istenen_kaliteli_coksatan = len(games_clean[(games_clean['Critic_Score'] >= 80) & (games_clean['Global_Sales'] >= 1)])
olasilik_4 = istenen_kaliteli_coksatan / tumu_genel
print("Hem kaliteli hem çok satan olma olasılığı:", olasilik_4)
sns.histplot(games_clean['Global_Sales'], bins=50)
plt.show()
sns.histplot(games_clean['Critic_Score'], bins=50)
plt.show()
sns.histplot(games_clean['JP_Sales'], bins=50)
plt.show()
sns.histplot(games_clean['EU_Sales'], bins=50)
plt.show()
sns.histplot(games_clean['NA_Sales'], bins=50)
plt.show()
sns.histplot(games_clean['User_Score'], bins=50)
plt.show()
ortalama_puan = games_clean['Critic_Score'].mean()
sapma_puan = games_clean['Critic_Score'].std()
alt_sinir_1 = ortalama_puan - sapma_puan
ust_sinir_1 = ortalama_puan + sapma_puan
alt_sinir_2 = ortalama_puan - (2 * sapma_puan)
ust_sinir_2 = ortalama_puan + (2 * sapma_puan)
toplam_puanli_oyun = games_clean['Critic_Score'].notna().sum()
sapma_1_oyunlari = len(games_clean[(games_clean['Critic_Score'] >= alt_sinir_1) & (games_clean['Critic_Score'] <= ust_sinir_1)])
sapma_2_oyunlari = len(games_clean[(games_clean['Critic_Score'] >= alt_sinir_1) & (games_clean['Critic_Score'] <= ust_sinir_2)])
print("1 Sapma Aralığı Oranı:", sapma_1_oyunlari / toplam_puanli_oyun)
print("2 Sapma Aralığı Oranı:", sapma_2_oyunlari / toplam_puanli_oyun)
global_satis_ortalamasi = games_clean['Global_Sales'].mean()
global_satis_sapması = games_clean['Global_Sales'].std()
games_clean['Sales_Z_Score'] = (games_clean['Global_Sales'] - global_satis_ortalamasi) / global_satis_sapması
extraordinary_games = games_clean[games_clean['Sales_Z_Score'] > 3]
olağanustu_oyun_sayisi = len(extraordinary_games)
print("Z-Skoru 3'ten büyük olan olağanüstü oyun sayısı:", olağanustu_oyun_sayisi)
print(extraordinary_games[['Name', 'Global_Sales', 'Sales_Z_Score']].sort_values(by='Global_Sales', ascending=False).head(10))
print("\n---  Korelasyon Analizi ---")
korelasyon_matrisi = games_clean[['Critic_Score', 'User_Score', 'Global_Sales']].corr()
print(korelasyon_matrisi)
sns.scatterplot(data=games_clean, x='Critic_Score', y='Global_Sales', alpha=0.5)
plt.show()
print("\n--- Hipotez Testi 1 ---")
grup_yuksek_puan = games_clean[games_clean['Critic_Score'] >= 80]['Global_Sales'].dropna()
grup_dusuk_puan = games_clean[games_clean['Critic_Score'] < 80]['Global_Sales'].dropna()
t_degeri, p_degeri = stats.ttest_ind(grup_yuksek_puan, grup_dusuk_puan, alternative='greater')
print("P-Değeri (p-value):", p_degeri)
print("\n--- Hipotez Testi 2 ---")
grup_rpg = games_clean[games_clean['Genre'] == 'Role-Playing']['JP_Sales'].dropna()
grup_diger = games_clean[games_clean['Genre'] != 'Role-Playing']['JP_Sales'].dropna()
t_degeri_jp, p_degeri_jp = stats.ttest_ind(grup_rpg, grup_diger)
print("Japonya RPG Testi P-Değeri:", p_degeri_jp)
print("\n--- Hipotez Testi 3 ---")
grup_action = games_clean[games_clean['Genre'] == 'Action']['Global_Sales'].dropna()
grup_sports = games_clean[games_clean['Genre'] == 'Sports']['Global_Sales'].dropna()
t_degeri_son, p_degeri_son = stats.ttest_ind(grup_action, grup_sports)
print("Action ve Sports Testi P-Değeri:", p_degeri_son)
print("\n--- SQL Database Oluştur ---")
baglanti = sqlite3.connect('games.db')
games_clean.to_sql('games', baglanti, if_exists='replace', index=True, index_label='id')
print("Veri seti başarıyla games.db veritabanına 'games' tablosu olarak kaydedildi!")
print("\n--- SQL Analizleri ---")
sorgu_1 = "SELECT Name, Global_Sales FROM games ORDER BY Global_Sales DESC LIMIT 10"
print("\n1. En Çok Satan 10 Oyun:\n", pd.read_sql(sorgu_1, baglanti))
sorgu_2 = "SELECT Genre, SUM(Global_Sales) AS Toplam_Satis FROM games GROUP BY Genre ORDER BY Toplam_Satis DESC"
print("\n2. En Çok Satan Türler:\n", pd.read_sql(sorgu_2, baglanti))
sorgu_3 = "SELECT Platform, SUM(Global_Sales) AS Toplam_Satis FROM games GROUP BY Platform ORDER BY Toplam_Satis DESC LIMIT 10"
print("\n3. En Çok Satan 10 Platform:\n", pd.read_sql(sorgu_3, baglanti))
sorgu_4 = "SELECT Publisher, AVG(Global_Sales) AS Ortalama_Satis FROM games GROUP BY Publisher ORDER BY Ortalama_Satis DESC LIMIT 10"
print("\n4. En Yüksek Ortalama Satışa Sahip 10 Yayıncı:\n", pd.read_sql(sorgu_4, baglanti))
sorgu_5 = "SELECT Name, Year_of_Release, Global_Sales FROM games WHERE Year_of_Release >= 2010 ORDER BY Global_Sales DESC LIMIT 10"
print("\n5. 2010 Sonrası Çıkan En İyi 10 Oyun:\n", pd.read_sql(sorgu_5, baglanti))
sorgu_6 = "SELECT Name, Critic_Score, Global_Sales FROM games WHERE Critic_Score > 80 ORDER BY Global_Sales DESC LIMIT 10"
print("\n6. Eleştirmen Puanı 80 Üzeri Olan En Çok Satan 10 Oyun:\n", pd.read_sql(sorgu_6, baglanti))
sorgu_7 = "SELECT Name, EU_Sales, NA_Sales, Genre FROM games WHERE EU_Sales > NA_Sales ORDER BY EU_Sales DESC LIMIT 10"
print("\n7. Avrupa'da Amerika'dan Fazla Satan İlk 10 Oyun:\n", pd.read_sql(sorgu_7, baglanti))
print("\n--- SQL ile Daha İlginç Sorular ---")
sorgu__1 = "SELECT Genre, Name, MAX(Global_Sales) AS Maksimum_Satis FROM games GROUP BY Genre"
print("\n1. Her Türün En Çok Satan Oyunu:\n", pd.read_sql(sorgu__1, baglanti))
sorgu__2 = "SELECT Platform, COUNT(Name) AS Oyun_Sayisi FROM games GROUP BY Platform ORDER BY Oyun_Sayisi DESC LIMIT 10"
print("\n2. Platformlardaki Toplam Oyun Sayıları (İlk 10):\n", pd.read_sql(sorgu__2, baglanti))
sorgu__3 = "SELECT Publisher, COUNT(Name) AS Yayinlanan_Oyun FROM games GROUP BY Publisher ORDER BY Yayinlanan_Oyun DESC LIMIT 10"
print("\n3. En Üretken 10 Yayıncı (Publisher):\n", pd.read_sql(sorgu__3, baglanti))
sorgu__4 = "SELECT Genre, AVG(Global_Sales) AS Ortalama_Satis FROM games GROUP BY Genre ORDER BY Ortalama_Satis DESC LIMIT 5"
print("\n4. Ortalama Satışta En Başarılı İlk 5 Tür:\n", pd.read_sql(sorgu__4, baglanti))
sorgu__5 = "SELECT Genre, SUM(JP_Sales) AS Japonya_Toplam_Satis FROM games GROUP BY Genre ORDER BY Japonya_Toplam_Satis DESC LIMIT 5"
print("\n5. Japonya'nın En Sevdiği 5 Tür:\n", pd.read_sql(sorgu__5, baglanti))
sorgu__6 = "SELECT Genre, SUM(EU_Sales) AS Avrupa_Satis, SUM(NA_Sales) AS Amerika_Satis FROM games GROUP BY Genre ORDER BY Amerika_Satis DESC"
print("\n6. Amerika vs Avrupa Tür Tercihleri (Kıyaslama):\n", pd.read_sql(sorgu__6, baglanti))
sorgu__7 = """
SELECT 
    CASE 
        WHEN Year_of_Release BETWEEN 2000 AND 2009 THEN '2000-2009 Dönemi'
        WHEN Year_of_Release BETWEEN 2010 AND 2020 THEN '2010-2020 Dönemi'
    END AS Donem,
    SUM(Global_Sales) AS Toplam_Satis,
    COUNT(Name) AS Cikan_Oyun_Sayisi
FROM games 
WHERE Year_of_Release BETWEEN 2000 AND 2020
GROUP BY Donem
"""
print("\n7. 2000'ler ve 2010'lar Dönem Karşılaştırması:\n", pd.read_sql(sorgu__7, baglanti))
baglanti.close()

print("\n--- Matplotlib Analizleri ---")
yillik_satis = games_clean.groupby('Year_of_Release')['Global_Sales'].sum()
plt.figure(figsize=(10, 5))
plt.plot(yillik_satis.index, yillik_satis.values, marker='o', color='b')
plt.title('1. Yıllara Göre Global Oyun Satışları')
plt.xlabel('Yıl')
plt.ylabel('Toplam Global Satış (Milyon)')
plt.grid(True)
tur_satislari = games_clean.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 5))
plt.bar(tur_satislari.index, tur_satislari.values, color='skyblue', edgecolor='black')
plt.title('2. En Çok Satan 10 Oyun Türü')
plt.xlabel('Oyun Türü')
plt.ylabel('Toplam Satış (Milyon)')
plt.xticks(rotation=45)
plt.figure(figsize=(10, 5))
plt.hist(games_clean['Global_Sales'], bins=50, color='purple', edgecolor='black')
plt.title('3. Global Satış Dağılımı')
plt.xlabel('Satış (Milyon)')
plt.ylabel('Oyun Sayısı (Frekans)')
bolgeler = ['Kuzey Amerika (NA)', 'Avrupa (EU)', 'Japonya (JP)']
bolge_satislari = [games_clean['NA_Sales'].sum(), games_clean['EU_Sales'].sum(), games_clean['JP_Sales'].sum()]
plt.figure(figsize=(8, 5))
plt.bar(bolgeler, bolge_satislari, color=['blue', 'green', 'red'], edgecolor='black')
plt.title('4. Bölgesel Satış Dağılımları')
plt.ylabel('Toplam Satış (Milyon)')
yillik_oyun_sayisi = games_clean.groupby('Year_of_Release')['Name'].count()
plt.figure(figsize=(10, 5))
plt.plot(yillik_oyun_sayisi.index, yillik_oyun_sayisi.values, marker='s', color='orange')
plt.title('5. Yıllara Göre Çıkan Oyun Sayısı')
plt.xlabel('Yıl')
plt.ylabel('Piyasaya Sürülen Oyun Adedi')
plt.grid(True)
plt.show()
print("\n--- Seaborn Analizleri ---")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=games_clean, x='Critic_Score', y='Global_Sales', alpha=0.5, color='darkred')
plt.title('1. Eleştirmen Puanı ve Global Satış İlişkisi')
plt.xlabel('Critic Score')
plt.ylabel('Global Satış (Milyon)')
plt.figure(figsize=(12, 6))
sns.boxplot(data=games_clean, x='Genre', y='Global_Sales', hue='Genre', legend=False)
plt.title('2. Oyun Türlerine Göre Satış Dağılımı ve Outlier Değerler')
plt.xticks(rotation=45)
plt.xlabel('Oyun Türü (Genre)')
plt.ylabel('Global Satış (Milyon)')
plt.figure(figsize=(10, 8))
heatmap_kolonlari = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales', 'Critic_Score', 'User_Score']
korelasyon_matrisi = games_clean[heatmap_kolonlari].corr()
sns.heatmap(korelasyon_matrisi, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('3. Değişkenler Arası Korelasyon Isı Haritası')
plt.show()
print("\n--- Bölgesel Oyuncu Davranışı ---")
na_top5 = games_clean.groupby('Genre')['NA_Sales'].sum().sort_values(ascending=False).head(5)
eu_top5 = games_clean.groupby('Genre')['EU_Sales'].sum().sort_values(ascending=False).head(5)
jp_top5 = games_clean.groupby('Genre')['JP_Sales'].sum().sort_values(ascending=False).head(5)
print("\nNorth America (Kuzey Amerika) En Sevilen 5 Tür:")
for i, (tur, satis) in enumerate(na_top5.items(), 1):
    print(f"{i}. {tur}")

print("\nEurope (Avrupa) En Sevilen 5 Tür:")
for i, (tur, satis) in enumerate(eu_top5.items(), 1):
    print(f"{i}. {tur}")

print("\n--- 23. AŞAMA: Publisher Analizi ---")

hedef_yayincilar = [
    'Nintendo',
    'Electronic Arts',
    'Activision',
    'Ubisoft',
    'Sony Computer Entertainment',
    'Take-Two Interactive'
]

dev_sirketler_data = games_clean[games_clean['Publisher'].isin(hedef_yayincilar)]
yayinci_gruplari = dev_sirketler_data.groupby('Publisher')

for isim, data in yayinci_gruplari:
    game_count = data['Name'].count()
    total_sales = data['Global_Sales'].sum()
    average_sales = data['Global_Sales'].mean()

    most_successful_genre = data.groupby('Genre')['Global_Sales'].sum().idxmax()

    bolgeler = {
        'North America (NA)': data['NA_Sales'].sum(),
        'Europe (EU)': data['EU_Sales'].sum(),
        'Japan (JP)': data['JP_Sales'].sum()
    }
    most_successful_region = max(bolgeler, key=bolgeler.get)

    print(f"\n[{isim.upper()}]")
    print(f"- Game Count: {game_count}")
    print(f"- Total Sales: {total_sales:.2f} Milyon")
    print(f"- Average Sales: {average_sales:.2f} Milyon")
    print(f"- Most Successful Genre: {most_successful_genre}")
    print(f"- Most Successful Region: {most_successful_region}")

print("\nJapan (Japonya) En Sevilen 5 Tür:")
for i, (tur, satis) in enumerate(jp_top5.items(), 1):
    print(f"{i}. {tur}")

print("\n--- 22. AŞAMA: Platform Savaşları ---")

def platform_grupla(p):
    p = str(p)
    if p.startswith('PS'):
        return 'PlayStation'
    elif p.startswith('X'):
        return 'Xbox'
    elif p in ['Wii', 'WiiU', 'NES', 'SNES', 'N64', 'GC', 'GB', 'GBA', 'DS', '3DS']:
        return 'Nintendo'
    elif p == 'PC':
        return 'PC'
    else:
        return 'Other'

games_clean['Platform_Group'] = games_clean['Platform'].apply(platform_grupla)
platform_gruplari = games_clean.groupby('Platform_Group')

for isim, data in platform_gruplari:
    toplam_satis = data['Global_Sales'].sum()
    oyun_sayisi = data['Name'].count()
    ort_satis = data['Global_Sales'].mean()

    en_guclu_tur = data.groupby('Genre')['Global_Sales'].sum().idxmax()

    bolgeler = {
        'North America (NA)': data['NA_Sales'].sum(),
        'Europe (EU)': data['EU_Sales'].sum(),
        'Japan (JP)': data['JP_Sales'].sum()
    }
    en_guclu_bolge = max(bolgeler, key=bolgeler.get)

    print(f"\n[{isim.upper()}]")
    print(f"- Toplam Satış: {toplam_satis:.2f} Milyon")
    print(f"- Oyun Sayısı: {oyun_sayisi}")
    print(f"- Ortalama Satış: {ort_satis:.2f} Milyon")
    print(f"- En Güçlü Tür: {en_guclu_tur}")
    print(f"- En Güçlü Bölge: {en_guclu_bolge}")
    