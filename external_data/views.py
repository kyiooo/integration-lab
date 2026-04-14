import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64
from django.shortcuts import render
import datetime
from random import randint
import json

def weather_view(request):
    coordinates = {"Seul": ("37.56", "126.97")}
    place = "Seul"
    
    weather_url = (f"[https://api.open-meteo.com/v1/forecast](https://api.open-meteo.com/v1/forecast)"
                   f"?latitude={coordinates[place][0]}&longitude={coordinates[place][1]}"
                   f"&hourly=temperature_2m&current_weather=true&timezone=auto")

    try:
        response = requests.get(weather_url, timeout=10)
        response.raise_for_status()
        seul_weather = response.json() 

        # 2. Obróbka danych
        hourly_data = seul_weather['hourly']
        godziny_raw = hourly_data['time'][:24]
        temperatury_wykres = hourly_data['temperature_2m'][:24]
        aktualna_temp = seul_weather['current_weather']['temperature']
        godziny_short = [g[-5:] for g in godziny_raw]

        # 3. Wizualizacja 
        plt.figure(figsize=(10, 5))
        plt.plot(godziny_short, temperatury_wykres, color='#efa7cb', marker='o', linewidth=3)
        plt.ylabel('Temperatura (°C)', color='#666', fontsize=12) 
        plt.xlabel('Godzina (czas lokalny)', color='#666')
        plt.xticks(rotation=45)
        plt.grid(True, axis='y', linestyle='--', alpha=0.3)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()

        return render(request, 'external_data/weather.html', {
            'place': place,
            'lat': coordinates[place][0],
            'lon': coordinates[place][1],
            'temp': aktualna_temp,
            'chart': chart_base64,
            'success': True
        })
    except Exception as e:
        return render(request, 'external_data/weather.html', {'success': False, 'error': str(e)})

def json_photo_view(request):
    PHOTOS_URL = "https://jsonplaceholder.typicode.com/photos"
    
    try:
        response = requests.get(PHOTOS_URL, timeout=10)
        response.raise_for_status()
        photos_data = response.json()

        # 1. FILTRACJA
        relevant_albums_ids = range(1,6) 
        filtered_data = [p for p in photos_data if p['albumId'] in relevant_albums_ids]

        # 2. LICZENIE STATYSTYK
        processed_list = []
        for a_id in relevant_albums_ids:
            album_photos = [p for p in filtered_data if p['albumId'] == a_id]
            count = len(album_photos)
            avg_len = sum(len(p['title']) for p in album_photos) / count if count > 0 else 0
            
            processed_list.append({
                'album_id': a_id,
                'photo_count': count,
                'average_title_length': round(avg_len, 2)
            })

        # 3. LOSOWANIE
        photo = photos_data[randint(0, len(photos_data) - 1)]
        
        plt.figure(figsize=(4, 4))
        random_color = [randint(150, 255)/255, randint(150, 255)/255, randint(150, 255)/255]
        plt.imshow([[random_color]]) 
        
        plt.title(f"Photo ID: {photo['id']}", color='#b05a84', fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.text(0, 0, f"Album {photo['albumId']}", ha='center', va='center', fontsize=20, color='white', fontweight='bold')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        photo_plot = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()
            
        return render(request, 'external_data/photo_list.html', {
            'processed_items': processed_list,
            'random_photo': photo,
            'generated_image': photo_plot, 
            'success': True
        })
        
    except Exception as e:
        return render(request, 'external_data/photo_list.html', {'success': False, 'error': str(e)})



def weather_summary_api(request):
    # Dane do WeatherAPI
    city = "Gdansk"
    api_key = "719d36e7886a4701980124316241410"
    url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=1&aqi=no"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # AGREGACJA (Punkt 5 zadania)
        hourly_data = data['forecast']['forecastday'][0]['hour']
        temps = [h['temp_c'] for h in hourly_data]
        
        # Obliczamy średnią temperaturę
        avg_temp = sum(temps) / len(temps)
        
        # Przygotowujemy dane do formatu JSON
        summary = {
            "city": city,
            "average_temp": round(avg_temp, 2),
            "max_temp": max(temps),
            "min_temp": min(temps),
            "status": "Success"
        }
        
        # Konwertujemy na tekst, żeby render mógł go wysłać
        json_output = json.dumps(summary, indent=4)
        
        # Używamy render, ale z typem application/json
        return render(request, 'external_data/api_response.html', {
            'json_data': json_output
        }, content_type='application/json')
        
    except Exception as e:
        error_json = json.dumps({"error": str(e)})
        return render(request, 'external_data/api_response.html', {'json_data': error_json}, content_type='application/json')
    
def weather_summary_api(request):
    coordinates = {"Gdansk": ("54.35", "18.64")}
    place = "Gdansk"
    
    weather_url = (f"https://api.open-meteo.com/v1/forecast"
                   f"?latitude={coordinates[place][0]}&longitude={coordinates[place][1]}"
                   f"&hourly=temperature_2m,precipitation&timezone=auto&forecast_days=1")
    
    try:
        response = requests.get(weather_url, timeout=10)
        data = response.json()
        
        hourly_temps = data['hourly']['temperature_2m'][:24]
        hourly_precip = data['hourly']['precipitation'][:24]
        
        # Agregacja 
        avg_temp = sum(hourly_temps) / len(hourly_temps)
        total_precip = sum(hourly_precip)
        
        return render(request, 'external_data/weather_summary.html', {
            'place': place,
            'avg_temp': round(avg_temp, 2),
            'total_precip': round(total_precip, 2),
            'success': True
        })
    except Exception as e:
        return render(request, 'external_data/weather_summary.html', {
            'success': False, 
            'error': str(e)
        })
        

