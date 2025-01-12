import psycopg2
import pandas as pd
import numpy as np
from sklearn.decomposition import NMF
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import precision_score, recall_score, accuracy_score
import joblib

# PostgreSQL bağlantı bilgileri
db_config = {
    'dbname': 'recommendation_db',
    'user': 'postgres',
    'password': '455410',
    'host': 'localhost',
    'port': 5433
}

# Veritabanına bağlanma
try:
    conn = psycopg2.connect(**db_config)
    print("Veritabanına başarıyla bağlanıldı.")
except Exception as e:
    print("Bağlantı hatası oluştu:", e)
    exit()

# Veriyi SQL sorgusu ile çekme
query = """
select i.user_id, i.product_id, i.rating, 
       u.preferences, p.category, p.price
from interactions as i
join users as u on i.user_id = u.id
join products as p on i.product_id = p.id;
"""
try:
    df = pd.read_sql_query(query, conn)
    print("Veriler başarıyla çekildi.")
except Exception as e:
    print("Sorgu hatası:", e)
    conn.close()
    exit()

# Kullanıcı tercihlerinin One-Hot Encoding ile dönüştürülmesi
preferences_list = df['preferences'].str.split(',').apply(lambda x: x if isinstance(x, list) else [])
mlb = MultiLabelBinarizer()
preferences_encoded = mlb.fit_transform(preferences_list)
df_preferences = pd.DataFrame(preferences_encoded, columns=mlb.classes_)
df = pd.concat([df, df_preferences], axis=1)

# Kategori sütununu sayısal hale getirme
df['category'] = df['category'].astype('category').cat.codes

# Kullanıcı-Ürün matrisi oluşturma
user_product_matrix = df.pivot(index='user_id', columns='product_id', values='rating')

# Eksik değerleri doldurma
user_product_matrix = user_product_matrix.apply(lambda x: x.fillna(x.mean()), axis=1)

# NMF modeli ile faktörizasyon
model = NMF(n_components=10, random_state=42, max_iter=500)
W = model.fit_transform(user_product_matrix)
H = model.components_

# Tahmin edilen derecelendirmeler
predicted_ratings = np.dot(W, H)

# Öneri sonuçlarını pandas DataFrame'e dönüştürme
recommendations = pd.DataFrame(predicted_ratings, index=user_product_matrix.index, columns=user_product_matrix.columns)

# Her kullanıcı için en iyi 5 ürün önerisi
top_recommendations = recommendations.apply(lambda row: row.nlargest(5).index.tolist(), axis=1)

# Öneri sonuçlarını PostgreSQL'e kaydetme
try:
    with conn.cursor() as cursor:
        cursor.execute("drop table if exists recommendations2;")
        cursor.execute(""" 
            create table recommendations2 (
                user_id int,
                product_id int,
                predicted_rating float
            );
        """)
        for user_id, products in top_recommendations.items():
            for product_id in products:
                predicted_rating = float(recommendations.at[user_id, product_id])
                cursor.execute("""
                    insert into recommendations2 (user_id, product_id, predicted_rating)
                    values (%s, %s, %s);
                """, (user_id, product_id, predicted_rating))
        conn.commit()
    print("Öneri sonuçları veritabanına kaydedildi.")
except Exception as e:
    print("Kaydetme hatası:", e)


# Performans metriklerini hesaplama
threshold = recommendations.mean().mean()
df_nonnull = df.dropna(subset=['rating'])
y_true = df_nonnull['rating'].values
y_pred = predicted_ratings[
    df_nonnull['user_id'].values - 1, 
    df_nonnull['product_id'].values - 1
]

y_true_binary = (y_true >= threshold).astype(int)
y_pred_binary = (y_pred >= threshold).astype(int)

precision = precision_score(y_true_binary, y_pred_binary, zero_division=1)
recall = recall_score(y_true_binary, y_pred_binary, zero_division=1)
accuracy_value = accuracy_score(y_true_binary, y_pred_binary)

# Performans çıktısı
print("***Evaluation Metrics***\n")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"Accuracy: {accuracy_value:.2f}")

# Modeli ve matrisleri kaydetme
joblib.dump(model, 'nmf_model.pkl')
joblib.dump(W, 'W_matrix.pkl')
joblib.dump(H, 'H_matrix.pkl')

conn.close()
print("Bağlantı kapatıldı.")
