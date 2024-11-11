import requests
import pandas as pd

# Dictionary untuk menerjemahkan deskripsi cuaca dari Bahasa Inggris ke Bahasa Indonesia
deskripsi_cuaca_id = {
    'clear sky': 'cerah',
    'few clouds': 'berawan',
    'overcast clouds': 'mendung',
    'moderate rain': 'hujan sedang',
    'light rain': 'hujan ringan',
    'shower rain': 'hujan gerimis',
    'rain': 'hujan',
    'thunderstorm': 'badai petir',
    'snow': 'salju',
    'mist': 'kabut'
}

def ambil_data_cuaca(kota, api_key):
    """
    Mengambil data cuaca dari API OpenWeather berdasarkan nama kota dan API key.
    
    Args:
        kota (str): Nama kota untuk mencari data cuaca.
        api_key (str): Kunci API untuk mengakses layanan OpenWeather.
        
    Returns:
        dict: Data cuaca dalam format JSON jika berhasil, None jika gagal.
    """
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={kota}&appid={api_key}&units=metric'  # Menambahkan units=metric
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f'Error {response.status_code}: {response.text}')
        return None
# Menganalisis data cuaca untuk menghasilkan DataFrame dengan informasi harian.
def analisis_cuaca(data): 
    """
    Args:
        data (dict): Data cuaca dalam format JSON.
        
    Returns:
        pd.DataFrame: DataFrame yang berisi tanggal, temperatur rata-rata, kelembapan rata-rata, dan deskripsi cuaca.
    """
    if data is None:
        return None
    
    forecast_list = data.get('list', [])
    dates = []
    temperatures = []
    humidities = []
    weather_descriptions = []

    for item in forecast_list:
        date = item['dt_txt'].split(' ')[0]  # Mengambil tanggal dari format datetime
        dates.append(date)
        temperatures.append(item['main']['temp'])  # Temperatur dalam Celsius
        humidities.append(item['main']['humidity'])
        desc = item['weather'][0]['description']
        weather_descriptions.append(deskripsi_cuaca_id.get(desc, desc))  # Menerjemahkan deskripsi cuaca

    df = pd.DataFrame({
        'Tanggal': dates,
        'Temperatur (°C)': temperatures,
        'Kelembapan (%)': humidities,
        'Deskripsi Cuaca': weather_descriptions
    })

    # Agregasi harian
    df_daily = df.groupby('Tanggal').agg({
        'Temperatur (°C)': 'mean',  # Menghitung rata-rata temperatur
        'Kelembapan (%)': 'mean',    # Menghitung rata-rata kelembapan
        'Deskripsi Cuaca': lambda x: x.mode()[0]  # Mengambil deskripsi cuaca yang paling umum
    }).reset_index()

    df_daily.index = df_daily.index + 1  # Memulai indeks dari 1
    return df_daily

def main():
    """
    Fungsi utama yang meminta input nama kota dan menampilkan hasil analisis cuaca.
    """
    kota = input('Masukkan nama kota: ')
    api_key = 'f3d2740ccb9189a6da2b17a3f0152dbd'  # Ganti dengan kunci API Anda

    data = ambil_data_cuaca(kota, api_key)  # Mengambil data cuaca
    df = analisis_cuaca(data)  # Menganalisis data cuaca

    if df is not None:
        print("Hasil Analisis Cuaca:")
        print(df.head())  # Menampilkan 5 baris pertama dari DataFrame

if __name__== '_main':
    main()