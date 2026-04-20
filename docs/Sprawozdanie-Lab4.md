# Laboratorium nr 4
**Temat:** Konteneryzacja aplikacji Django za pomocą Dockera

## Dane autora
* **Imię i nazwisko:** [Małgorzata Andrzejewska]
* **Kierunek:** [Informatyka]
* **Grupa:** [235IC A2]
* **Link do repo na github:** [https://github.com/kyiooo/integration-lab]
----

### Punkt 1 - Przygotowanie środowiska

1. Stworzyć nową gałąź - `feature/dockerization` - done
2. Upewnij się, że masz plik zależności: requirements.txt dla Pythona:

W pliku brakowało mi biblioteki PostgreSQL, więc ją dodałam na końcu listy:
`psycopg2-binary==2.9.9`

W celu zapisania zmian wykonałam commita:
```
git add requirements.txt
git commit -m "Add PostgreSQL driver to requirements"
git push origin feature/dockerization
```
----

### Punkt 2 - Tworzenie Dockerfile

1. Przygotuj plik _Dockerfile_ dla swojej aplikacji - Python

W głównym katalogu projektu utworzyłam nowy plik _Dockerfile_.
Następnie uzupełniłam go o następujące linijki:
```
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```
gdzie 
`WORKDIR /app` ustawia katalog roboczy w kontenerze,
`COPY requirements.txt .` kopiuje listę bibliotek,
`RUN pip install --no-cache-dir -r requirements.txt` instaluje zależności
`COPY . .` kopiuje cały projekt
`CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]` odpala Django na porcie 8000 oraz `0.0.0.0`, żeby było dostępne z kontenera.

2. Zbuduj obraz:

Odpaliłam **Docker Desktop**
Zapisałam plik i zbudowałam obraz za pomocą komendy `docker build -t app-test .`

Zauważyłam błąd na poziomie `RUN pip install --no-cache-dir -r requirements.txt`, ze względu że mam w requirements.txt `Django==6.0.3` a mój Dockerfile używa `FROM python:3.11-slim`

Django 6.0.x wymaga Pythona 3.12+ a ja mam Pythona 3.11, przez co musiałam w pliku `requirements.txt` zmienić Django na `Django==5.2.7`

Ponowiłam zbudowanie obrazu `docker build -t app-test .`
![Budowa obrazu test](https://i.postimg.cc/SsYxZg5g/obraz-2026-04-19-145741368.png)
![Budowa obrazu test2](https://i.postimg.cc/8Cr29xpJ/obraz-2026-04-19-150011617.png)
![Budowa obrazu test3](https://i.postimg.cc/JhJFPJxk/obraz-2026-04-19-150108229.png)
![Budowa obrazu test4](https://i.postimg.cc/9XxLPJVV/obraz-2026-04-19-150240489.png)

3. Commit:

Wykonałam commita:
```
git add .
git commit -m "Add Dockerfile for the application"
git push origin feature/dockerization
```

### Punkt 3 - Orkiestracja z Docker Compose

