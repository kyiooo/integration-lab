# Laboratorium nr 5
**Temat:** Automatyzacja CI/CD z Github Actions i wdrożenie PaaS

## Dane autora
* **Imię i nazwisko:** [Małgorzata Andrzejewska]
* **Kierunek:** [Informatyka]
* **Grupa:** [235IC A2]
* **Link do repo na github:** [https://github.com/kyiooo/integration-lab]
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