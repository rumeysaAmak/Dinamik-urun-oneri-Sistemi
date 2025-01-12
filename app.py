import pandas as pd
import numpy as np
from flask import Flask, request
from flask import jsonify  #hata yönetimi için oldukça önemli
from sqlalchemy import create_engine
import psycopg2

app = Flask(__name__)

# PostgreSQL bağlantı bilgileri
db_config = {
    'dbname': 'recommendation_db',
    'user': 'postgres',
    'password': '455410',
    'host': 'localhost',
    'port': 5433
}
db_url = "postgresql://postgres:455410@localhost:5433/recommendation_db"
engine = create_engine(db_url)

# Model yüklenmesi
import joblib
model = joblib.load('nmf_model.pkl')
W = joblib.load('W_matrix.pkl')
H = joblib.load('H_matrix.pkl')

# PostgreSQL bağlantı fonksiyonu
def get_db_connection():
    return psycopg2.connect(**db_config)

@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    user_id = request.args.get('user_id', type=int)
    
    if user_id is None:
        return jsonify({'error': 'user id is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        select i.user_id, i.product_id, i.rating, u.preferences, p.category, p.price
        from interactions as i
        join users as u on i.user_id = u.id
        join products as p on i.product_id = p.id
        where i.user_id = %s
        """
        cursor.execute(query, (user_id,))
        data = cursor.fetchall()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
    
    if not data:
        return jsonify({'error'}), 404

    columns = ['user_id', 'product_id', 'rating', 'preferences', 'category', 'price']
    user_data = pd.DataFrame(data, columns=columns)
    return jsonify(user_data.to_dict(orient='records'))

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    user_id = request.args.get('user_id', type=int)

    if user_id is None:
        return jsonify({'error': 'user id is required'}), 400

    query = """
    select i.user_id, i.product_id, i.rating, u.preferences, p.category, p.price
    from interactions as i
    join users as u on i.user_id = u.id
    join products as p on i.product_id = p.id
    where i.user_id = %s
    """
    
    #öneri kontroller
    try:
        df = pd.read_sql_query(query, engine, params=(user_id,))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if df.empty:
        return jsonify({'error': 'no ratings found for this user'}), 404

    if 'preferences' not in df.columns:
        return jsonify({'error': 'preferences column is missing in the data'}), 400

    # Preferences kolonunu onehotencoder uygula
    from sklearn.preprocessing import MultiLabelBinarizer
    preferences_list = df['preferences'].fillna('').str.split(',')
    mlb = MultiLabelBinarizer()
    preferences_encoded = mlb.fit_transform(preferences_list)
    preferences_encoded_df = pd.DataFrame(preferences_encoded, columns=mlb.classes_)
    df = pd.concat([df, preferences_encoded_df], axis=1)

    # Kategoriyi sayısal değere çevirme
    df['category'] = df['category'].astype('category').cat.codes

    # Kullanıcı-ürün matrisini oluşturma
    user_product_matrix = df.pivot(index='user_id', columns='product_id', values='rating')
    user_product_matrix = user_product_matrix.apply(lambda x: x.fillna(x.mean()), axis=1)

    predicted_ratings = np.dot(W, H) #matris çarpımı

    # Boyut uyumsuzluğu kontrolü(HATA)
    if predicted_ratings.shape[1] != user_product_matrix.shape[1]:
        return jsonify({'error': 'matrisler uyuşmuyor'}), 500


    recommendations = pd.DataFrame(predicted_ratings, columns=user_product_matrix.columns)

    try:
        user_index = user_product_matrix.index.get_loc(user_id)
        top_recommendations = recommendations.iloc[user_index].nlargest(5).index.tolist()
    except KeyError:
        return jsonify({'error'}), 404

    return jsonify({'user_id': user_id, 'recommended_products': top_recommendations})

if __name__ == '__main__':
    app.run(debug=True)
