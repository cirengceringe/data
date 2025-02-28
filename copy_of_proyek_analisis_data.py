# -*- coding: utf-8 -*-
"""Copy of Proyek Analisis Data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BFJ5oSB7gvJMO9j9jGNXS3lsNk8ACA3T

# Proyek Analisis Data: [Input Nama Dataset]
- **Nama:** Farah Trijayanti
- **Email:** leesunsheng11@gmail.com
- **ID Dicoding:** [Input Username]

## Menentukan Pertanyaan Bisnis

- Pertanyaan 1: Wilayah mana yang menghasilkan omset paling besar?
- Pertanyaan 2: Bagaimana pengaruh ulasan pada banyaknya produk yang terjual?

## Import Semua Packages/Library yang Digunakan
"""

import pandas as pd
import numpy as np
from google.colab import drive
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

"""## Data Wrangling

### Gathering Data
"""

drive.mount('/content/drive')
customers_path = '/content/drive/MyDrive/E-Commerce Public Dataset/customers_dataset.csv'
orders_path = '/content/drive/MyDrive/E-Commerce Public Dataset/orders_dataset.csv'
rating_path = '/content/drive/MyDrive/E-Commerce Public Dataset/order_reviews_dataset.csv'
item_path = '/content/drive/MyDrive/E-Commerce Public Dataset/order_items_dataset.csv'

customers_df = pd.read_csv(customers_path)
print(customers_df.head())
orders_df = pd.read_csv(orders_path)
rating_df = pd.read_csv(rating_path)
item_df = pd.read_csv(item_path)

#merge data customer + order + rating + item
dataset_df = customers_df.merge(orders_df, on='customer_id').merge(rating_df, on='order_id').merge(item_df, on='order_id')
dataset_df.head()

"""**Insight:**
- karena saya akan menganalisa wilayah mana yang potensial untuk penempatan cabang toko baru, saya membutuhkan data customer dan order, jadi saya gabungkan keduanya.
- untuk menganalisa apakah rating itu memengaruhi banyaknya order, maka pada tabel saya gabungkan tabel rating juga.

### Assessing Data
"""

#mengecek apakah ada data yang kosong, duplikat dan outlier
dataset_df.info()
dataset_df.isnull().sum()
dataset_df.duplicated().sum()

"""**Insight:**
Missing Value
- terdapat 15 buah missing value pada kolom tanggal pesanan diterima (order_approved_at)
- terdapat 1184 missing value pada kolom tanggal pemesanan dikirim (order_delivered_carrier_date)
- terdapat 2360 missing value pada kolom tanggal pesanan diterima oleh pelanggan (order_delivered_customer_date)
- terdapat 98938 missing value pada kolom judul komentar review (review_comment_title)
- terdapat 64730 missing value pada kolom komemtar review (review_comment_message)

Duplicated
- terdapat 0 duplicated pada seluruh dataset

### Cleaning Data
"""

#mengisi missing value dengan tanggal yang sama
dataset_df['order_approved_at'] = dataset_df['order_approved_at'].fillna(pd.Timestamp('2017-02-03 01:00:00'))
dataset_df['order_delivered_carrier_date'] = dataset_df['order_delivered_carrier_date'].fillna(pd.Timestamp('2017-02-03 01:00:00'))
dataset_df['order_delivered_customer_date'] = dataset_df['order_delivered_customer_date'].fillna(pd.Timestamp('2017-02-03 01:00:00'))

#mengisi missing value pada judul kolom komentar review
dataset_df['review_comment_title'] = dataset_df['review_comment_title'].fillna("No Title")
dataset_df['review_comment_message'] = dataset_df['review_comment_message'].fillna("No Comment")

"""**Insight:**
- untuk missing value yang berupa tanggal, saya tidak mengisi dengan mean atau median dan quartil tanggal, tetapi mengisinya dengan tanggal default. Hal ini karena fokus pada analisis saya tidak memerlukan data berupa waktu.
- untuk missing value judul dan komentar saya mengisinya dengan "No Title" dan "No Comment"

## Exploratory Data Analysis (EDA)

### Explore ...
"""

dataset_df.describe(include="all")
#menghitung jumlah pelanggan per kota
pelanggan_per_kota = dataset_df.groupby('customer_city')['customer_id'].nunique().reset_index()

#mengurutkan pelanggan per kota dari tertinggi ke terendah
pelanggan_per_kota = pelanggan_per_kota.sort_values(by='customer_id', ascending=False)

print(pelanggan_per_kota)

#mengurutkan jumlah rating per order
rating_per_product = dataset_df.groupby('review_score')['product_id'].nunique().reset_index()
rating_per_product = rating_per_product.sort_values(by='product_id', ascending=False)
print(rating_per_product)

#mencari korelasi
label_encoder = LabelEncoder()
dataset_df['product_id'] = label_encoder.fit_transform(dataset_df['product_id'])
mapping = {1: 1, 2: 2, 3: 3, 4:4, 5: 5}
dataset_df['review_score'] = dataset_df['review_score'].map(mapping)
#dataset_df['review_score'] = label_encoder.fit_transform(dataset_df['review_score'])
correlation = dataset_df['review_score'].corr(dataset_df['product_id'])
print(correlation)

"""**Insight:**
- Dari describe didapat bahwa rata-rata skor ualasan adalah 4. dari data terendah 1 dan tertinggi 5.
- Wilayah dengan pelanggan terbanyak ada di Sao Paulo dengan jumlah pelanggan 15.291
- Produk dengan skor  ulasan 5 memiliki penjualan produk terbanyak yaitu sebanyak 23.212, disusul dengan skor ulasan 4 dengan penjualan produk sebanyak 10.542. tetapi urutan produk terjual terbanyak ketiga yaitu dengan skor ulasan 1 yaitu 7.484
- Korelasi antara ulasan dan produk terjual memiliki nilai 0.00196, hal ini menandakan bahwa korelasi antara ulasan dengan banyaknya produk yang terjual sangat lemah.

## Visualization & Explanatory Analysis

### Pertanyaan 1:
"""

#Wilayah mana yang potensial akan menghasilkan omzet baru? / Di wilayah mana toko ini ideal untuk ditempatkan?

#membuat bar chart perbandingan jumlah pelanggan per wilayah
pelanggan_per_kota_sorted = pelanggan_per_kota.sort_values(by='customer_id', ascending=False)
top_10_pelanggan = pelanggan_per_kota_sorted.head(10)
Wilayah_top_10 = top_10_pelanggan['customer_city']
jumlah_pelanggan_top_10 = top_10_pelanggan['customer_id']
plt.bar(Wilayah_top_10, jumlah_pelanggan_top_10)
plt.xlabel('Wilayah')
plt.ylabel('Jumlah Pelanggan')
plt.title('Jumlah Pelanggan per Wilayah')
plt.xticks(rotation=90)
plt.show()

"""### Pertanyaan 2:"""

#Bagaimana pengaruh ulasan pada banyaknya produk yang terjual?

#menghitung berapa jumlah produk yang terjual di setiap order
print(dataset_df.columns)
total_units_sold = dataset_df.groupby('product_id')['order_item_id'].count().reset_index()
total_units_sold.rename(columns={'order_item_id': 'total_units_sold'}, inplace=True)

print(dataset_df.head())

print(dataset_df['review_score'].unique())

#memvisualisasikan dengan scatter plot
plt.scatter(dataset_df['review_score'], dataset_df['total_units_sold'], alpha=0.6)

plt.xticks([1,2,3,4,5])
plt.xlabel('Ulasan Produk')
plt.ylabel('Jumlah Terjual')
plt.title('Perbandingan Ulasan Produk dan Jumlah Terjual')

plt.show()

#memvisualisasikan dengan boxplot
sns.boxplot(x='review_score', y='total_units_sold', data=dataset_df)
plt.xlabel('Ulasan Produk')
plt.ylabel('Jumlah Terjual')
plt.title('Perbandingan Ulasan Produk dan Jumlah Terjual')
plt.show()

"""**Insight:**
- jumlah produk yang terjual dibandingkan dengan ulasan semuanya tersebar merata
- tidak ada pola yang jelas antara ulasan dan penjualan. Beberapa produk tetap terjual tinggi meskipun ulasannya rendah.
- ulasan tidak menjadi tolok ukur apakah penjualan akan tinggi dan rendah jika ulasannya tinggi atau rendah.

## Analisis Lanjutan (Opsional)
"""



"""## Conclusion

Pertanyaan 1: Wilayah mana yang menghasilkan omzet paling besar?
- Berdasarkan analisis data di atas, wilayah yang menghasilkan omzet paling besar adalah kota Sao Paulo yaitu sekitar 15.000. Kemudian disusul oleh kota Rio de Jeneiro dengan pelanggan sebanyak 7000 dan kota Belo Horizonte sebanyak 3000.
- Perbandingan jumlah pelanggan kota Sao Paulo dengan kota lainnya memiliki gap yang cukup jauh. Artinya produk yang dijual belum tersebar merata ke seluruh kota, atau ada faktor lain yang menyebabkan mengapa gap omzet tersebut terlalu jauh.
- Menggunakan Bar Chart untuk menentukan kota yang menghasilkan omzet terbesar sangat ideal dan informatif.


Pertanyaan 2: Bagaimana pengaruh ulasan pada banyaknya produk yang terjual?
- Dari scatter plot dan boxplot di atas disimpulkan bahwa jumlah penjualan dan review cukup tersebar merata.
- Ulasan 1 terdapat banyak penjualan, hampir sama banyaknya dengan ulasan 2,3,4, dan 5
- Ulasan tidak menjadi faktor penentu apakah produk akan laris atau tidak. Ada faktor lain yang menentukan sebuah produk akan laris dan tidak.
"""