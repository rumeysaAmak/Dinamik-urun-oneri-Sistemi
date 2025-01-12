import pandas as pd
data = pd.read_csv('fetch_data.csv')
print("ilk 5 satır:")
print(data.head())  # ilk 5 satır

print("eksik değerler:")
print(data.isnull().sum())  # eksik veri sayısı

# kategorik verilerin sayısı
print("preferences kategorisi:")
print(data['preferences'].value_counts())

print("category kategorisi:")
print(data['category'].value_counts())

# sayısal verilere dönüştürme
new_preferences = data['preferences'].str.split(',', expand=True)
new_preferences = new_preferences.apply(lambda x: x.str.strip()).stack().str.get_dummies()

# veri setine dönüştürülen verileri ekleme
new_preferences = new_preferences.groupby(level=0).sum()

data = pd.concat([data, new_preferences], axis=1)

data['category'] = data['category'].astype('category').cat.codes

# yeni verilerin gösterilmesi
print(data.head())

print(data.describe())#istatiksel özelliklerin incelenmesi

#normalizasyon yapma işlemi(price)
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler() #verileri 0-1 aralığında sınırlandırır.
data['price'] = scaler.fit_transform(data[['price']])

print(data.head())