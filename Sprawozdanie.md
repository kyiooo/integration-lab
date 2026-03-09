# Laboratorium nr 1
**Temat:** Konfiguracja środowiska i praca z systemem kontroli wersji.

## Dane autora
* **Imię i nazwisko:** [Małgorzata Andrzejewska]
* **Kierunek:** [Informatyka]
* **Grupa:** [235IC A2]

----
### Punkt 1 - Konfiguracja środowiska i Markdown

1. Instalacja Git oraz Python  - done
2. Konfiguracja nazwy użytkownika i emaila w Git:\
Skonfigurowałam git'a wpisując w terminalu następujące komendy:
```
git config --global user.name "Malgorzata Andrzejewska" 
git config --global user.email "gosik123-01@wp.pl"
```
3. Generowanie kluczy SSH:\
Wpisałam komendę `ssh-keygen -t ed25519 -C "gosik123-01@wp.pl`
i wygenerowałam klucz ssh, akceptując domyślną scieżkę.


![Generowanie klucza ssh](https://i.postimg.cc/bJBDJNRt/ssh-lepsze.png) 

Następnie skopiowałam zawartość klucza publicznego za pomocą komendy `type %USERPROFILE%\.ssh\id_ed25519.pub` ,ponieważ operuję w systemie Windows. Przeszłam na swoje konto Github, następnie w zakładkę Settings, kolejno SSH and GPG Keys, utworzyłam nowy klucz ssh i wkleiłam tam wartość klucza publicznego, którego skopiowałam wcześniej. Dla upewnienia, że dobrze skonfigurowałam połączenie z Github wykonałam komendę: `ssh -T git@github.com`.

![Generowanie klucza ssh](https://i.postimg.cc/3NY6kYJx/ssh-test.png)

4. Zadanie Markdown:\
Utworzyłam plik README.md w folderze roboczym Lab1-Andrzejewska\ oraz wypełniłam go odpowiednią treścią.

-----
### Punkt 2 - Inicjalizacja projektu i Git

1. Wirtualne Środowisko:
   
W terminalu wpisałam następujące komendy, w celu stworzenia i aktywacji środowiska:
```
python -m venv venv
.\venv\Scripts\activate
pip install django
```
W trakcie musiałam się posłużyć komendą:\
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`\
gdyż trafiłam na SecurityError, ponieważ Windows domyślnie blokuje uruchamianie skryptów w PowerShellu.

Poprawnie aktywowane środowisko potwierdza mi zielony (venv) na początku lini w terminalu:

![Środkowisko](https://i.postimg.cc/mk0svN9w/Zrzut-ekranu-2026-03-05-083131.png)


2. Instalacja frameworka:
   
Po utworzeniu i aktywacji środowiska przeszłam do instalacji framework'a Django - done


3. Utworzenie struktury projektu:

Zainicjalizowałam projekt komendą: `django-admin startproject core .`\
Aktualnie mój folder roboczy jest kompletny i prezentuje się następująco:

![Folder Roboczy](https://i.postimg.cc/y6rRvncQ/Zrzut-ekranu-2026-03-04-113348.png)

4. Inicjalizacja Git:

W terminalu wpisałam komendę `git init` co spowodowało, że mój folder roboczy przekształcił się w **lokalne repozytorium** a w nim pojawił się niewidoczny folder _.git_ gdzie Git przechowuję calą historię zmian. Aktualnie część plików jest zaznaczona z prawej strony jako _U_ czyli **"Untracked"**. Oznacza to, że Git wie o istnieniu takiego pliku ale nie zapisał jeszcze żadnej jego wersji.

5. Zarządzanie zależnościami:

Tworzę listę bibliotek za pomocą komendy `pip freeze > requirements.txt`\
Spowodowało to utworzenie się pliku _requirements.txt_ w moim folderze roboczym.

6. Stworzenie pliku _.gitignore_

Utworzyłam w moim folderze roboczym plik _.gitignore_ oraz dodałam do niego odpowiednią zawartosć.

![gitignore](https://i.postimg.cc/sDL2970m/Zrzut-ekranu-2026-03-05-085409.png)

7. Pierwszy commit

Sprawdzam status: `git status`
Terminal wyświetla mi pliki **Untracked**, które muszę dodać następną komendą `git add .`, jeśli chcę żeby znalazły się w commicie.

Następnie robię commita za pomocą komendy:\
 `git commit -m "Initial commit: Django project structure"`

 ----
 ### Punkt 3 - Praca z gałęziami i podstawowa logika

 1. Tworzenie gałęzi funkcjonalnej:

Wpisuję do terminala `git checkout -b feature/initial-setup` dzięki czemu tworzę nową gałąź i od razu na nią przechodzę.

2. Stworzenie aplikacji(modułu):

Dzięki komendzie `python manage.py startapp base` tworzę folder _base/_ z aplikacjami.

3. Rejestracja aplikacji:

Znajduję i otwieram plik _core/settings.py_, następnie szukam listy `INSTALLED_APPS` oraz dodaje `'base',` na końcu listy. Powstaje mi zółty znaczek M przy pliku, co oznacza, że plik został zmodyfikowany.

4. Zapisanie zmian na gałęzi:

Dodaję zmiany dzięki `git add .` oraz zatwierdzam commita komendą:
`git commit -m "Add base application and register it in settings"`

5. Scalanie zmian (Merge):

Teraz muszę przenieść te zmiany do głównej gałęzi, ale zachować gałąź pomocniczą:
Przechodzę na gałąź główną `git checkout main`, kolejno scalam zmiany z gałęzi feature `git merge feature/initial-setup`

6. Tworzenie dodatkowych gałęzi typu _feature_ lub pomocniczych:

Przeszłam na nową gałąź feature:

`git checkout -b feature/docs`

W pliku _README.md_ dodałam zdanie **"Projekt zawiera dwie wymagane gałęzie typu feature."** oraz uzupełniałam dalej moje sprawozdanie. Zmiany dodałam `git add .` oraz wykonałam commita `git commit -m "Update documentation and README on feature branch"`, kolejno przeszłam na gałąź _main_ `git checkout main`
oraz wykonałam marge'a `git merge feature/docs`

Na końcu sprawdziłam swoje gałęzie za pomocą komendy: `git branch`

![git branch](https://i.postimg.cc/zB0kd86Z/Zrzut-ekranu-2026-03-05-094157.png)

W repozytorium znajdują się 3 gałęzie w tym 2 o typie _feature_.

---
### Punkt 4 - Współpraca z GitHub

1. Tworzenie zdalnego repozytorium na GitHub

Zgodnie z instrukcją utworzyłam nowe repozytorium na GitHubie.

![GitHub repo](https://i.postimg.cc/Kvw4nw9N/Zrzut-ekranu-2026-03-05-095633.png)

2. Połączenie lokalnego repozytorium ze zdalnym:

Skopiowałam adres SSH repozytorium: \
`git@github.com:kyiooo/integration-lab-1.git`

Następnie w terminalu wpisałam :\
`git remote add origin git@github.com:kyiooo/integration-lab-1.git`

3. Pierwsze wypchnięcie kodu:

`git push -u origin main`  
![git push main](https://i.postimg.cc/j51CZ1s1/Zrzut-ekranu-2026-03-05-100508.png)

4. Wypchnięcie pozostałych gałęzi:
```
git push origin feature/initial-setup
git push origin feature/docs
```
![git push features](https://i.postimg.cc/brvWN6kP/Zrzut-ekranu-2026-03-05-100954.png)

5. Wykorzystanie GitHub Issues:

Na moim repozytorium na GitHubie utworzyłam 2 przykładowe zadanka do wykonania na kolejnych laboratoriach.

![issues](https://i.postimg.cc/13WLb1qH/Zrzut-ekranu-2026-03-05-102210.png)

-------

### Punkt 5 - Symulacja konfliktu

1. Krok 1 (GitHub):

Zmieniam linijkę:

>Czas trwania - 6h

Na linijkę:

>Czas trwania - 6h - |||praca indywidualna|||

![Github](https://i.postimg.cc/W4dbHnhM/Zrzut-ekranu-2026-03-05-102915.png)

oraz zatwierdziłam zmiany.

2. Krok 2 (Lokalnie): 

Zmieniam linijkę:

>Czas trwania - 6h

Na linijkę:

>Czas trwania - 6h - praca samodzielna

![Lokalnie](https://i.postimg.cc/PqWFTGpd/Zrzut-ekranu-2026-03-05-103302.png)

3. Krok 3 (Błąd): 

Wykonuję poniższe polecenia w terminalu:

```
git add README.md
git commit -m "Local change to README"
git push origin main
```
Tak jak powinno się wydarzyć, Git odrzucił operację, zgodnię z tym, że wersja na serwerze zawiera zmiany, których nie posiadam lokalnie.

![Błąd](https://i.postimg.cc/LXny5WJz/obraz-2026-03-09-150741601.png)

4. Krok 4 (Rozwiązanie):
   
Po wykonaniu polecenia `git pull origin main` wyskoczył komunikat o konflikcie, mówiący, żeby najpierw naprawić błędy a następnie zcommitować. 

Plik *README* na podglądzie zmienił kolor na niebieski a przy nim znajduję się ikonka _↓MD,!_. Po wejściu w dany plik pojawiły się nowe znaczniki.

![Znaczniki](https://i.postimg.cc/FR6hkwGZ/obraz-2026-03-09-152409986.png)

Usunęłam je, wybrałam jedną opcję i zcommitowałam zmianę:
```
git add README.md
git commit -m "Fix merge conflict in README"
git push origin main
```
---

### Punkt 6 - Automatyzacja z Github Actions

1. Przygotowywanie struktury:
   
Wykonuję polecenie:
`mkdir -p .github/workflows`

![struktura](https://i.postimg.cc/fyCWT5kj/obraz-2026-03-09-160344930.png)

Po wykonaniu w folderze głównym powstał folder _.github_ a wnim podfolder _workflows_.

2. Stworzenie pliku workflow:

Utworzyłam w podfolderze _workflows_ plik *.github/workflows/django_check.yml*

3. Skopiowałam podaną treść w zadaniu do utworzonego pliku -done

4. Test automatyzacji:

Po zapisaniu pliku wypchęłam go do Github'a

```
git add .github/workflows/django_check.yml
git commit -m "Add GitHub Actions workflow"
git push
```
Następnie sprawdziłam na Github zakładkę Actions, gdzie powstał nowy uruchomiony proces.
![Actions](https://i.postimg.cc/pd7MC450/obraz-2026-03-09-161819683.png)

5. Symulacja błędu:

Aby sprawdzić czy moja "sprawdzarka" działa, otworzyłam plik _core/urls.py_ gdzie usunęłam nawias `]` na końcu listy `urlpatterns`

Plik _urls.py_ poświetla się na czerwono podkreślając 2 błędy oraz pokazuje znacznik *M* czyli modified.

W takim stanie spróbowałam wypchnąć zmianę oraz sprawdzić czy Github Actions zgłosi błąd. 

```
git add core/urls.py
git commit -m "Introduce intentional syntax error"
git push origin main
```
![Actions/bląd](https://i.postimg.cc/ZKTYWk8X/obraz-2026-03-09-162727391.png)

Na stronie Actions został zgłoszony błąd poprzez czerwony ptaszek przy ostatniej akcji. Oznacza to, że test okazał się sukcesem i moja "sprawdzarka" działa poprawnie.

Kolejno przeszłam do naprawienia błędu.
Wrócilam się do pliku  _urls.py_ oraz zwróciłam brakujący `]` na końcu listy `urlpatterns`
Następnie wypchęnłam zmiany do Github.
```
git add .
git commit -m "Fix syntax error"
git push origin main
```
![Actions/naprawa](https://i.postimg.cc/59QK8j3Y/Zrzut-ekranu-2026-03-09-163459.png)

---

### Podsumowanie realizacji zadań:

* Wszystkie punkty z instrukcji (1-6) zostały zrealizowane pomyślnie:
* Środowisko: Skonfigurowałam Git (SSH), Python oraz wirtualne środowisko venv. Plik .gitignore poprawnie filtruje zbędne pliki.
* Projekt Django: Zainicjalizowałam strukturę projektu i stworzyłan aplikację base.
* Markdown: Plik README.md zawiera wymagane formatowanie (nagłówki, listy, linki, kod).
* Git & Branching: Praca odbywała się na gałęziach feature/. W repozytorium znajdują się co najmniej dwie dodatkowe gałęzie.
* Konflikt: Przetestowałam i rozwiązałam konflikt wersji w pliku README.md (synchronizacja lokalna vs GitHub).
* GitHub Actions: Skonfigurowałam automatyczny test składni (flake8). Pomyślnie przetestowałam scenariusz błędu (Czerwony X) oraz poprawnego przejścia (Zielony ptaszek).
* Repozytorium: Projekt jest publiczny, posiada czytelną historię commitów i poprawny plik requirements.txt.
* Ostatnim commitem jest pełny plik sprawozdania.