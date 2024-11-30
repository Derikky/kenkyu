from django.shortcuts import render
from django.http import JsonResponse
import requests
import pandas as pd
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import japanize_matplotlib
from django.conf import settings
import os




def get_solar_data(request):
    # さいたま市の緯度経度
    latitude = 35.8616
    longitude = 139.6455

    # 現在の日付を取得
    today = datetime.now().strftime('%Y-%m-%d')
    
    # APIエンドポイントとパラメータを設定
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'shortwave_radiation,direct_normal_irradiance,diffuse_radiation',
        'start_date': today,
        'end_date': today,
        'timezone': 'Asia/Tokyo'
    }

    # APIリクエストを送信
    response = requests.get('https://api.open-meteo.com/v1/forecast', params=params)
    data = response.json()

    # データフレームに変換
    results = pd.DataFrame({
        '時間': [datetime.fromisoformat(t).strftime('%H:%M') for t in data['hourly']['time']],
        '短波日射量(W/m2)': data['hourly']['shortwave_radiation'],
        '直接日射量(W/m2)': data['hourly']['direct_normal_irradiance'],
        '散乱日射量(W/m2)': data['hourly']['diffuse_radiation']
    })

    # グラフ化
    plt.figure(figsize=(10,5))
    plt.plot(results['時間'], results['短波日射量(W/m2)'], label='短波日射量(W/m2)', color='orange')
    plt.xlabel('時間')
    plt.ylabel('短波日射量(W/m2)')
    plt.title('さいたま市の日射量予報')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    # グラフを画像ファイルとして保存
    media_dir = settings.MEDIA_ROOT
    os.makedirs(media_dir, exist_ok=True)
    image_path = os.path.join(media_dir, 'sunlight_forecast.png')
    plt.savefig(image_path)
    plt.close()

    image_url = settings.MEDIA_URL + 'sunlight_forecast.png'
    return render(request, 'expect/look.html', {'data': results.to_html(index=False),  'image_url': image_url})

# Create your views here.
