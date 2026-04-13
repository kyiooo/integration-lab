import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64
from django.shortcuts import render
import datetime

def weather_view(request):
    coordinates = {
        "Seul": ("37.56", "126.97")
    }
    place = "Seul"
    
    weather_url = (f"https://api.open-meteo.com/v1/forecast"
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