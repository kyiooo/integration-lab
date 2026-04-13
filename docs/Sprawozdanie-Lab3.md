# Laboratorium nr 3
**Temat:** Tworzenie REST API w Django i integracja z zewnętrznymi usługami

## Dane autora
* **Imię i nazwisko:** [Małgorzata Andrzejewska]
* **Kierunek:** [Informatyka]
* **Grupa:** [235IC A2]
* **Link do repo na github:** [https://github.com/kyiooo/integration-lab]
----

### Punkt 1 - Praca na gałęziach

1. Stworzenie nowej gałęzi `git checkout -b feature/external-api-integration` - done

---
### Punkt 2 - Przygotowanie struktury

**Stworzenie nowej aplikacji oraz zainstalowanie potrzebnych bibliotek.**

1. Utworzyłam nową aplikację za pomocą komendy:
`python manage.py startapp external_data`

2. Następnie dodałam ją do _settings.py_ w sekcji **INSTALLED_APPS**:
`'external_data',`

3. Zainstalowałam niezbędne biblioteki: `requests`, `matplotlib`
`pip install requests matplotlib`

4. Dodałam zainstalowane biblioteki do pliku zależności `requirements.txt`
`pip freeze > requirements.txt`

![requirements](https://i.postimg.cc/Vk3JLm2t/obraz-2026-04-13-144630182.png)

5. Wykonałam commit aby zapisać zmiany w konfiguracji:
```
git add .
git commit -m "update requirements.txt with requests and matplotlib"
git push origin feature/external-api-integration
```
----

### Punkt 3 - Integracja z Open-Meteo API

1. Musiałam utworzyć ścieżkę, po której dojdę do strony z pogodą:

W liście `urlpatterns` w pliku _core/urls.py_ dodałam nową linijkę:
`path('external/', include('external_data.urls')),`

Stworzyłam nowy plik _external_data/urls.py_ oraz uzupełniłam jego zawartość:
```
from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.weather_view, name='weather_view'),
]
```
1. Napisz logikę pobierającą prognozę pogody dla wybranego miasta(Seul: [szerokość: 37°56′N, długość: 126°97′E] jako wpółrzędne centrum)

W pliku _external_data/views.py_ uzupełniłam:
```
import requests
from django.shortcuts import render

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
        
        return render(request, 'external_data/weather.html', {
            'place': place,
            'lat': coordinates[place][0],
            'lon': coordinates[place][1],
            'raw_data': data,
            'success': True
        })
        
    except Exception as e:
        return render(request, 'external_data/weather.html', {'success': False, 'error': str(e)})
```

Uzupełniłam kod o `try-except` w celu obsłużenia błędów połączenia oraz `response.raise_for_status()` dla sprawdzania kodu statusu HTTP.

2. Obróbka danych

Dopisałam logikę wycinania danych do mojego widoku:
```
        hourly_data = seul_weather['hourly']
        godziny_raw = hourly_data['time'][:24]
        temperatury_wykres = hourly_data['temperature_2m'][:24]
        aktualna_temp = seul_weather['current_weather']['temperature']
        godziny_short = [g[-5:] for g in godziny_raw]
```
Następnie zmieniłam `return render` na:
```
return render(request, 'external_data/weather.html', {
            'place': place,
            'lat': coordinates[place][0],
            'lon': coordinates[place][1],
            'temp': aktualna_temp,
            'success': True
        })
```

3. Wizualizacja

Dodałam odpowiednie importy:
```
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64
import datetime
```
`matplotlib.use('Agg') ` - pozwala tworzyć wykresy bez otwierania okien na serwerze

Następnie dodałam wizualizację z użyciem matplotlib oraz Base64 
```
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
```
Następnie do render dodałam:
`'chart': chart_base64,`

4. Wyświetlenie

Utworzyłam nowy szablon: `external_data/templates/external_data/weather.html` oraz uzupełniłam go o daną treść dodając Bootstrapa dla estetyki:

```
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Pogoda: {{ place }}</title>
    <style>
        body { background-color: #fff5f7; }
        .navbar-custom { background-color: #ffdae9; }
        .article-container { background-color: white; border-radius: 20px; padding: 40px; }
        h1 { color: #efa7cb; }
        .temp-box { background-color: #ffdae9; padding: 15px; border-radius: 10px; display: inline-block; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-10">
                <div class="article-container shadow-sm text-center">
                    {% if success %}
                        <h1>Prognoza dla: {{ place }}</h1>
                        <p class="text-muted">Współrzędne: {{ lat }}, {{ lon }}</p>

                        <div class="temp-box">
                            <strong>Aktualna temperatura: {{ temp }}°C</strong>
                        </div>

                        <div class="mt-4">
                            <img src="data:image/png;base64,{{ chart }}" class="img-fluid border shadow-sm" alt="Wykres">
                        </div>
                    {% else %}
                        <div class="alert alert-danger">Błąd: {{ error }}</div>
                    {% endif %}

                    <hr class="mt-5">
                    <a href="/" class="btn btn-outline-secondary">← Wróć</a>
                </div>
            </div>
        </div>
    </div>

</body>
</html>
```

5. Efekt końcowy z Open-Meteo API:

* Dane zostały poddane obróbce
* Zaimplementowano jedną formę wizualizacji danych (wykres)
* Zostały zrobione zrzuty ekranu działającej integracji oraz wygenerowanego wykresu 

Aktualna temperatura generowana na godzinę 01:00(UTC+9)
![Dzialajaca integracja](https://i.postimg.cc/RVwDg2Yx/obraz-2026-04-13-183755344.png)
![Dzialajaca integracja2](https://i.postimg.cc/pdvx0DCQ/obraz-2026-04-13-184521254.png)
![Wygenerowany wykres](https://i.postimg.cc/tRxSgLpq/obraz-2026-04-13-183846799.png)

6. Commit

```
git add .
git commit -m "Add weather data processing and charts"
git push origin main
```

----

### Punkt 4 