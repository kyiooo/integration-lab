# Laboratorium nr 5
**Temat:** Automatyzacja CI/CD z Github Actions i wdrożenie PaaS

## Dane autora
* **Imię i nazwisko:** [Małgorzata Andrzejewska]
* **Kierunek:** [Informatyka]
* **Grupa:** [235IC A2]
* **Link do repo na github:** [https://github.com/kyiooo/integration-lab]
* **Adres publiczny aplikacji:** [https://integration-lab.onrender.com]
----

Przed rozpoczęciem pracy nad laboratorium naprawiłam błąd z jednym nieprzechodzącym testem na GitHub Actions by nie sprawiał on problemów.

### Punkt 1 - Testy jednostkowe

Utworzyłam nową gałąź feature: `feature/ci-cd`

1. Napisz minimum 2 testy jednostkowe dla swoich widoków, modeli lub funkcji.

Zdecydowałam się napisać 1 test do widoku i 1 do modelu, zdecydowałam się na aplikację **blog**.

Najpierw w klasie _BlogLogicTests_ utworzyłam metodę `setUp()`, w której utworzył się użytkownik testowy `self.user`

```
def setUp(self):
        self.user = User.objects.create_user(
        username='tester',
        password='test123'
        )
```

Test 1: Test modelu: Sprawdza czy model posta poprawnie zwraca tytuł jako tekst

```
def test_post_string_representation_returns_title(self):
        """Test modelu: sprawdza, czy reprezentacja stringowa posta zwraca tytuł."""
        post = Post.objects.create(
        title='Moj testowy post',
        content='Tresć posta',
        author=self.user
        )
        self.assertEqual(str(post), 'Moj testowy post')
```
Test utworzył przykładowy obiekt `Post`, wywolał `str(post)` oraz sprawdził czy wynik jest równy tytułowi posta

Test 2: Test widoku: Sprawdza czy po utworzeniu posta pojawia się on w danych zwracanych przez widok listy postów

```
def test_post_list_view_contains_created_post(self):
        """Test widoku: sprawdza, czy strona listy postów zawiera utworzony wpis."""
        post = Post.objects.create(
            title='Widoczny post',
            content='Tresć',
            author=self.user
        )
        response = self.client.get(reverse('postList'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(post, response.context['postList'])
```
Test utworzył przykładowy post, wysłał żądanie _GET_ do widoku listy postów przez `reverse('postList')`, sprawdził czy odpowiedź ma kod **200** oraz sprawdził, czy utworzony post znajduje się w `response.context['postList']`

2. Uruchom testy:

Uruchomiłam testy za pomocą komendy `python manage.py test`

![Odpalenie testów](https://i.postimg.cc/dt2RgQ9S/obraz-2026-04-22-104155551.png)

Wynik uruchomienia pokazał utworzenie testowej bazy danych, wykonanie 4 testów (2 z laboratorium nr.2), brak błędów, status końcowy **OK**.

3. Commit:
```
git add .
git commit -m "Add unit tests for the application"
git push origin feature/ci-cd
```
----

### Punkt 2 - Konfiguracja GitHub Actions CI

1. Stwórz plik .github/workflows/main.yml - done
2. Skonfiguruj potok (pipeline), który po każdym push uruchamia: Lintera (flake8 dla Py) oraz testy jednostkowe.
```
name: Django CI
on:
  push:
  pull_request:
```
Przekazanie Gitowi, by odpalał workflow po każdym `push` i po każdym `pull request`.

```
jobs:
  ci:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install flake8

      - name: Run linter
        run: |
          flake8 .

      - name: Run tests
        run: |
          python manage.py test
```

Zadanie: Github uruchamia je na maszynie z ubuntu
Kroki:
+ Checkout repository - pobiera kod z repo do środowiska roboczego
+ Set up Python - ustawia wersję Pythona na 3.11
+ Install dependencies - instaluje zależności z `requirements.txt` oraz `flake8`
+ Run linter - sprawdza styl kodu przez `flake8 .`
+ Run tests - uruchamia `python manage.py test` czyli wszystkie testy Django

Wypchnięcie i sprawdzenie czy Action poprawnie się doda:
```
git add .
git commit -m "Add initial GitHub Actions workflow"
git push origin feature/ci-cd
```
![test workflow](https://i.postimg.cc/HxhxSNn6/obraz-2026-04-22-111756559.png)
Niestety jeden z kroków nie przeszedł, więc zabrałam się do naprawienia nieintencjonalnego błedu.
Po przejrzeniu kodu błędu wyszło na to że problem jest z krokiem `Run linter`, reszta pipelin'u działa poprawnie.
flake8 wykrył błędy stylu kodu w pliku `external_data/views.py`
Za pomocą komend:
```
pip install autopep8
autopep8 --in-place --aggressive --aggressive external_data/views.py
```
udało mi się część błędów usunąć automatycznie.
Ręcznie musiałam usunąć jednego duplikata funkcji.
Kolejno dodałam plik `.flake8` w głównym katalogu projektu:
```
[flake8]
exclude =
    .git,
    __pycache__,
    venv,
    .venv,
    migrations
max-line-length = 88
```
Dzięki niemu, przy komendzie `python -m flake8 .` wytnie śmieci i poluzuje trochę limit do 88 linii.
Odnośnie tego w pliku `main.yml` zmieniłam `flake8 .` na `python -m flake8 .`
Ostatnim czym zrobiłam to naprawiłam wszystkie błędy flake8. 

Po czyszczeniu wykonałam commita sprawdzającego czy tym razem wszystko działa poprawnie:
```
git add .
git commit -m "Fix linting issues detected by CI"
git push origin feature/ci-cd
```
![test workflow2](https://i.postimg.cc/bNv284K8/obraz-2026-04-22-120437472.png)

3. Zadanie: Celowo zepsuj test i sprawdź, czy GitHub Actions zgłosi błąd (czerwony status). Napraw błąd.

W pliku `blog/tests.py` w teście _test_post_string_representation_returns_title_, który sprawdza czy model poprawnie zwraca tytuł jako tekst zmieniam **celowo**
linijke:
> self.assertEqual(str(post), 'Moj testowy post')

na:
>self.assertEqual(str(post), 'Zly tytul')

![zlyTytultest](https://i.postimg.cc/pLbh8ymZ/obraz-2026-04-22-121311942.png)

Commit zepsutego testu:
```
git add blog/tests.py
git commit -m "Break tests to verify CI failure"
git push origin feature/ci-cd
```
![zlyTytultest1](https://i.postimg.cc/HLJkhgcz/obraz-2026-04-22-121658647.png)
![zlyTytultest2](https://i.postimg.cc/YCTHjm0Z/obraz-2026-04-22-121826721.png)
![zlyTytultest3](https://i.postimg.cc/QCYzPRWq/obraz-2026-04-22-121932709.png)

Kolejno przeszłam do naprawienia błędu i ponownego commita:
```
git add .
git commit -m "Configure GitHub Actions CI pipeline"
git push origin feature/ci-cd
```
![finalnyGithubActions](https://i.postimg.cc/kXBM4CwD/obraz-2026-04-22-122307153.png)

---

### Punkt 3 - Optymalizacja Workflow - Cashe

1. Dodaj krok `actions/cache` do swojego workflow, aby przyspieszyć instalację zależnosci

Pomiędzy krokiem _Set up Python_ oraz krokiem _Install dependencies_ dodałam krok _Cache pip dependencies_:
```
- name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
```

Następnie wykonałam commita:
```
git add .github/workflows/main.yml
git commit -m "Add dependency caching to CI workflow"
git push origin feature/ci-cd
```

2. Porównaj czas wykonania pipeline'u przed i po dodaniu cache

Przed dodaniem cache workflow Django CI wykonywał się w czasie około 22 sekund.
![czasWorkflowPrzed](https://i.postimg.cc/4xXXqDZ1/obraz-2026-04-28-150310403.png)

Po dodaniu cache workflow Django CI wykonywał się w czasie około 25 sekund.
Ale był to pierwszy run po dodaniu cache więc utworzenie zajęło trochę czasu
![czasWorkflowPo](https://i.postimg.cc/prqtHTP8/obraz-2026-04-28-151444241.png)

Wykonałam 2 run by porównać czas gdy już jest używany cache:
![czasWorkflowPo2](https://i.postimg.cc/yYMLNKWy/obraz-2026-04-28-151859452.png)

Czas wykonania pipeline'u z dodanym cachem jest widocznie większy, jest to spowodowane tym, że projekt jest na tyle mały, a czas instalacji zależności na tyle krótki, że narzut związany z obsługą cache może przewyższać potencjalne korzyści

---

### Punkt 4 - Wdrożenie na Render.com lub Leapcell.io

1. Połącz swoje repozytorium z wybraną platformą

Dodałam do `requirements.txt` "gunicorn" za pomocą komend:
```
pip install gunicorn
pip freeze > requirements.txt
```
Potrzebuję go, ponieważ Render dla aplikacji Python/Django urachamia serwer produkcyjny komendą stylu `gunicorn core.wsgi`

Następnie w `core/settings.py` poprawiłam ALLOWED_HOSTS z:
`ALLOWED_HOSTS = []` 
na:
```
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',
]
```
Bez tego Django może odrzucać stronę po deploy'u.
Kolejno wykonałam komendy, aby zrobić testy lokalnie:
```
python manage.py test
python -m flake8 .
```
![testyLokalnie](https://i.postimg.cc/nh50CQ23/obraz-2026-04-28-155341666.png)

Zrobiłam commita by zapisać zmiany: `git commit -m "Prepare Django app for Render deployment"`

Następnie działając już na renderze:
* Zalogowałam się
* Kliknęlam `New +`
* Wybrałam `Web Service`
* Wybrałam połączenie z Githubem
  ![łączeniezrenderem](https://i.postimg.cc/3J2LfZXm/obraz-2026-04-28-155923340.png)
* Uzupełniłam rubryki:
  ![łączeniezrenderem1](https://i.postimg.cc/52rWb3r1/obraz-2026-04-28-160803765.png)
  ![łączeniezrenderem2](https://i.postimg.cc/qvzWbK7M/obraz-2026-04-28-160835130.png)
* Kliknęłam `Deploy`
  ![deploy1](https://i.postimg.cc/DzsGcCkC/obraz-2026-04-28-162132459.png)
  ![deploy2](https://i.postimg.cc/9f3RzGRM/obraz-2026-04-28-162201597.png)
  ![deploy3](https://i.postimg.cc/MT3zfSPh/obraz-2026-04-28-162306686.png)

Adres publiczny https://integration-lab.onrender.com

2. Skonfiguruj "Deploy Hook" (Render)
   
W settings skopiowałam private URL Deploy Hook'a
![deployHook1](https://i.postimg.cc/8kW6QXjK/obraz-2026-04-28-162759011.png)
A następnie w GitHub w settings, secrets i actions kliknęłam `new repository secret`:
![deployHook2](https://i.postimg.cc/c1KVswWN/obraz-2026-04-28-163037723.png)
Kliknęłam `Add secret`
![deployHook3](https://i.postimg.cc/3JNWrLRY/obraz-2026-04-28-163251380.png)

3. Dodaj krok w GitHub Actions, który po udanych testach wyśle powiadomienie do platformy (Auto-deploy)
   
W pliku `main.yml` dodałam pod jobem `ci` nowy job `deploy`:
```
deploy:
    needs: ci
    runs-on: ubuntu-latest
    if: github.event_name == 'push'

    steps:
      - name: Trigger Render deploy
        run: curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK }}"

      - name: Wait for deploymentcurl -I https://integration-lab.onrender.com/
        run: sleep 60

      - name: Sanity check deployed application
        run: curl -f https://integration-lab.onrender.com/
```

4. Commit i weryfikacja:
  
```
git add .github/workflows/main.yml
git commit -m "Integrate CD with PaaS via Deploy Hook and sanity check"
git push origin feature/ci-cd
```
Niestety przez błędną wersję Django zwróciło mi czerwony pipeline
Poprawiłam blędy i spróbowałam ponownie z komendą:
`git commit -m "Fix Django version compatibility"`

Weryfikacja:
Po pomyślnym przejściu joba `ci`, job `deploy` wywołuje Deploy Hook Rendera za pomocą `curl -X POST`, co uruchamia automatyczne wdrożenie aplikacji. Następnie pipeline wykonuje sanity check komendą `curl -f https://integration-lab.onrender.com/`, która kończy się sukcesem tylko wtedy, gdy aplikacja odpowiada poprawnym statusem HTTP.
![weryfikacja1](https://i.postimg.cc/BbwBDvRW/obraz-2026-04-28-171455371.png)
![weryfikacja2](https://i.postimg.cc/Rh8whDJP/obraz-2026-04-28-171538924.png)
widać komendę `curl -X POST "***"` co oznacza, że GitHub Actions wysłał żądanie do Render Deploy Hooka
![weryfikacja3](https://i.postimg.cc/6QJJn6xP/obraz-2026-04-28-172301675.png)
![weryfikacja4](https://i.postimg.cc/HxtVFPtZ/obraz-2026-04-28-173254341.png)

---

### Podsumowanie realizacji zadań:
* Napisano i pomyślnie uruchomiono lokalnie co najmniej 2 testy jednostkowe
* Plik workflow (.github/workflows/main.yml) został stworzony i znajduje się w poprawnym folderze
* Workflow zawiera kroki do instalacji zależności, uruchomienia lintera oraz testów
* Dodano mechanizm cache dla zależności
* W historii commitów widać dowód na celowe popsucie testu i jego późniejszą naprawę
* Potok CI na GitHubie jest "zielony" dla najnowszego commita
* Testy są automatycznie uruchamiane przy każdym push i pull_request
* Aplikacja została połączona z platformą PaaS - Render.com
* Poprawnie skonfigurowano zmienne środowiskowe i Secrets na GitHubie
* Wdrożenie (deployment) na platformę zewnętrzną zakończyło się sukcesem
* W pipeline dodano krok weryfikujący działanie aplikacji po wdrożeniu
* Aplikacja jest dostępna pod publicznym adresem URL i działa poprawnie
* Sprawozdanie w formacie PDF zostało przygotowane (zawiera link do działającej aplikacji i zrzut ekranu z zielonego potoku CI)
* Ostatni commit dotyczny finalnego sprawozdania