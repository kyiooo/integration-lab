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

---

### Punkt 3 - Orkiestracja z Docker Compose

Zanim przeszłam do Docker Compose dorzuciłam jeszcze plik _.dockerignore_ do głównego katalogu projektu, dzięki niemu Docker nie będzie kopiował do obrazu śmieci z Pythona, `db.sqlite3` czy ustawień vs code.

1. Stwórz plik `docker-compose.yml` zawierający serwis `web` (Twoja aplikacja) oraz `db` (PostgreSQL lub MongoDB).

W głównym katalogu projektu utworzyłam plik `docker-compose.yml` a w nim uzupełniłam listę rzeczy, które Docker ma uruchomić czyli _services_.

Najpierw dodałam bazę danych: 
```
  db:
    image: postgres:15
```

Kolejno dodałam konfigurację serwisu `db` żeby baza wiedziała jak ma się nazywać, jakiego użytkownika utworzyć, jakie mieć hasło.

```
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
```
Następnie zdefiniowałam wolumeny, dzięki czemu dane są zapisywane "na zewnątrz", dzięki czemu nie tracę ich po restarcie kontenera.
```
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

Na samym końcu pliku poza _services_ zadefiniowalam moje _volumes_:
```
volumes:
  postgres_data:
```

Przeszłam do dodanie serwisu `web`
W sekcji _services_ pod `db` dopisałam:
```
  web:
    build: .
```
Dzięki temu `db` bierze gotowy PostgreSQL i `web` buduje moją własną aplikację Django a nie bierze gotowego obrazu z internetu. Buduje mój lokalny obraz używając `Dockerfile`.

Kolejno dodałam polecenie startowe kontenera `web`:
`    command: python manage.py runserver 0.0.0.0:8000`
Pod nim dodałam mapowanie by móc w przeglądarce wejść w `http://localhost:8000`:
```
    ports:
      - "8000:8000"
```
Następnie dodałam :
```
    depends_on:
      - db
```
aby Docker najpierw uruchomił bazę a potem aplikację.

2. Skonfiguruj zmienne środowiskowe (Environment Variables) dla połączenia z bazą danych.

W pliku `docker-compose.yml` w sekcji `web` pod _depends_on_ dodałam:
```
    environment:
      DB_NAME: mydatabase
      DB_USER: myuser
      DB_PASSWORD: mypassword
      DB_HOST: db
      DB_PORT: 5432
```

Najważniejszą linijką jest `DB_HOST: db`, która definiuje nazwę serwisu z docker-compose, nie jest localhostem.

W pliku `core/settings.py` miałam dalej lokalną bazę plikową:

![zmiana database](https://i.postimg.cc/8PZkvfsm/obraz-2026-04-20-183345745.png)

Dodałam `import os` a następnie zmieniłam sekcję **DATABASES** tak, aby Django brał dane z `docker-compose.yml`:

![zmiana database2](https://i.postimg.cc/yYMQvvJY/obraz-2026-04-20-183710972.png)

1. Uruchom cały stos.

Podjęłam próbę uruchomienia za pomocą komendy `docker-compose up`
W między czasie otworzyłam nowy terminal i wpisałam `docker-compose exec web python manage.py migrate`, czyli zrobiłam migrację/utworzyłam nowe tabele w PostgreSQL:
![migracja](https://i.postimg.cc/9fQcQmcJ/obraz-2026-04-20-185043477.png)

Komenda `migrate` połączyła się z PostgreSQL w kontenerze, utworzyła wszystkie tabele i zastosowała migracje dla `admin`,`auth`,`blog`,`session`

Proces komendy `docker-compose up`
![compose-up](https://i.postimg.cc/7PG0LD6P/obraz-2026-04-20-185914937.png)
Ze zrzutu ekranu mogę potwierdzić, że PostgreSQL działa, Django działa, strona główna się otworzyła, `localhost:8000` odpowiada poprawnie.
![compose-up2](https://i.postimg.cc/fLxsHJCB/obraz-2026-04-20-190322341.png)

Dodatkowe zrzuty ekranu z Docker Desktop:
![Docker-desktop1](https://i.postimg.cc/YqF6dkKP/obraz-2026-04-20-190921709.png)
![Docker-desktop2](https://i.postimg.cc/yd5RTpfW/obraz-2026-04-20-190959054.png)
![Docker-desktop3](https://i.postimg.cc/NjwVgB1z/obraz-2026-04-20-191040135.png)
![Docker-desktop4](https://i.postimg.cc/SNcT13wV/obraz-2026-04-20-191132946.png)

4. Commit:

```
git add .
git commit -m "Add docker-compose for app and database orchestration"
git push origin feature/dockerization
```
----

### Podsumowanie realizacji zadań:

 * Stworzono i wykorzystano nową gałąź feature/dockerization
 * Plik zależności requirements.txt zawiera wszystkie niezbędne biblioteki
 * Dockerfile bazuje na oficjalnym obrazie odpowiednim dla technologii `python:slim`
 * Dockerfile poprawnie kopiuje pliki źródłowe i instaluje zależności
 * W Dockerfile zdefiniowano odpowiednią komendę startową (CMD)
 * Obraz Dockera buduje się bez błędów
 * Plik docker-compose.yml zawiera dwa serwisy: web (aplikacja) i db (baza danych)
 * Zmienne środowiskowe (host, port, user, password) są poprawnie przekazywane do aplikacji w docker-compose.yml
 * W kodzie aplikacji baza danych jest skonfigurowana do łączenia się z nazwą serwisu zdefiniowaną w Compose: db zamiast localhost
 * Wolumeny dla bazy danych są poprawnie zdefiniowane
 * Aplikacja uruchamia się poprawnie za pomocą komendy docker-compose up i jest dostępna w przeglądarce
 * Wykonano migracje bazy danych wewnątrz kontenera
 * Sprawozdanie w formacie PDF zostało przygotowane
 * Ostatnim commitem jest sprawozdanie