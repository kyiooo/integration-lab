# Laboratorium nr 2
**Temat:** Lokalna aplikacja Django - System Blodowy (praca z gałęziami)

## Dane autora
* **Imię i nazwisko:** [Małgorzata Andrzejewska]
* **Kierunek:** [Informatyka]
* **Grupa:** [235IC A2]
* **Link do repo na github:** [https://github.com/kyiooo/integration-lab]
----
__Quick Note__
Przed rozpoczęciem pracy nad laboratorium wykonałam commita wprowadzające małe zmiany na pliku _README_ oraz utworzyłam nowy folder _docs_, gdzie łatwiej będzie mi pracować na sprawozdaniach. Również w paru miejscach pozmieniałam nazwy, dlatego na nowo musiałam się połaczyć między repozytoriami za pomocą ssh:
`git@github.com:kyiooo/integration-lab.git`. Upewniłam się, że wszystko działa, czyli odzyskałam folder _base_, który gdzieś mi zaginął. 

---

### Punkt 1 - Praca na gałęziach (Git Workflow)

1. Stworzenie nowej gałęzi `git checkout -b feature/blog-app` -done
2. Upewnienie, że wszystkie zmiany w laboratorium będą trafiać na nową gałąź

---

### Punkt 2 - Inizjalizacja aplikacji

1. Stworzenie nowej aplikacji

Wpisałam komendę `python manage.py startapp blog` na mojej gałęzi _feature/blog-app_, dzięki czemu na lewym pasku powstał nowy folder _blog_.

2. Rejestracja aplikacji

W folderze _core_ w pliku _settings.py_ dodałam na końcu listy INSTALLED APPS pod `'base',` nową rejestrację `'blog',`. Plik zapisałam.

3. Commit:

Zcommitowałam moją pracę za pomocą komendy `git commit -m "Add blog app to projects and settings"`

---

### Punkt 3 - definicja modeli

1. Stworzenie modelu `Post` z polami: `title`,`content`,`authot` (ForeignKey do User),`created_at`,`published_at`:

oraz 

2. Implementacja metody `__srt__` dla modelu:

Otworzyłam plik *blog/models.py* gdzie wklęiłam zawartość z instrukcji:

```
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
```
![Definicja modeli](https://i.postimg.cc/pTKF2dr4/obraz-2026-03-10-122723166.png)

Plik zapisałam.

3. Commit

Sprawdziłam czy jestem na odpowiedniej gałęzi `git checkout feature/blog-app`
Dodałam wszystko `git add .`
Wykonałam commita `git commit -m "Define Post model"`

---

### Punkt 4 - Migracje i Panel Admina

Teraz "informujemy" bazę danych o nowym modelu i umożliwiamy edycję postów.

1. Wykonanie migracji: 
`python manage.py makemigrations`
`python manage.py migrate`

![Migracje](https://i.postimg.cc/1Xc7NPCj/obraz-2026-03-10-123637949.png)

2. Rejestracja modelu w _blog/admin.py_

Otworzyłam podany plik i dodałam do niego:

```
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```
![rejestracja-admin](https://i.postimg.cc/HxLkNsXg/obraz-2026-03-10-124140200.png)

Plik zapisałam.

3. Tworzenie superużytkownika (`createsuperuser`) i dodanie testowych postów:

Wpisałam w terminal komendę:
`python manage.py createsuperuser`

![createsuperuser](https://i.postimg.cc/gJ9PVzsJ/obraz-2026-03-10-124528415.png)

Podane dane:
```
Username: kyiooo
Email: gosik123-01@wp.pl
```

Odpaliłam server: `python manage.py runserver`
Następnie przeszłam na link: `http:/127.0.0.1:8000/admin`
![logowanie](https://i.postimg.cc/DwKYFx6J/obraz-2026-03-10-125123871.png)

Zalogowałam się za pomocą ustawionych przeze mnie danych przy tworzeniu superużytkownika.
Wita mnie strona administracyjna:
![strona administracyjna](https://i.postimg.cc/hG8ncJVR/obraz-2026-03-10-125528627.png)

Przeszłam zakładki _Posts_, następnie kliknęłam przy niej przycisk _+Add_:
![przykladowy post](https://i.postimg.cc/rpDhN7F7/obraz-2026-03-10-125924306.png)

Wypełniam rubryki z tytułem, treścią, autorem i tworzę kilka takich podstawowych postów.
![udalosie](https://i.postimg.cc/dVbCgfj4/obraz-2026-03-10-130154247.png)
![listapostow](https://i.postimg.cc/QNKFZmHt/obraz-2026-03-10-130530884.png)

Następnie zatrzymałam server kombinacją przycisków *CTRL + C*

4. Commit:

Wysłałam dokonane zmiany:
```
git add . 
git commit -m "Initialize database migrations and admin registration"
```

---

### Punkt 5 - Widoki i Szablony

Teraz sprawię, że posty z bazy danych trafią na ekran przeglądarki.

1. Stworzenie widoku listy postów (`ListView`) i szczegółów postu (`DetailView`)

Otworzyłam plik `blog/views.py` i uzupełniłam kod o odpowiednie widoki:
```
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from blog.models import Post

# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'blog/postList.html'
    context_object_name = 'postList'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/postDetail.html'
    context_object_name = 'postDetail'
```

`context_object_name` pozwoli mi się łatwiej do tych widoków odwoływać, jeśli będzie taka potrzeba. Plik zapisałam.

2. Konfiguracja URL-i w `blog/urls.py` oraz głównym `urls.py`

Utworzyłam plik `blog/urls.py`,ponieważ sam się nie utworzył.
W `blog/urls.py` zaznaczyłam, że moje widoki mają być pod konktretnymi adresami:

```
from django.urls import path
from .views import PostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='postList'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='postDetail'),
]
```
Zawarłam odnośnik do tego pliku w pliku głównym `core/urls.py`
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
```
Dodałam `include` w 2 linijce oraz `path('', include('blog.urls')),` jako odnośnik do pliku _blog/urls.py_

3. Tworzenie folderu `templates/blog/` i plików HTML:

Utworzyłam folder `blog/templates`, następnie w nim utworzyłam kolejny folder `templates/blog/` i już w nim utworzyłam 2 pliki: _postList.html_ i _postDetail.html_.

![templates](https://i.postimg.cc/02SpkxXB/obraz-2026-03-10-141818953.png)

Następnie uzupełniłam oba pliki:

+ postList:
```
<h1>Mój Blog</h1>
{% for post in postList %}
    <div>
        <h2><a href="{% url 'postDetail' post.pk %}">{{ post.title }}</a></h2>
        <p>{{ post.content|truncatewords:20 }}</p>
    </div>
{% endfor %}
```
+ postDetail:
```
<h1>{{ post.title }}</h1>
<p>Autor: {{ post.author }}</p>
<p>{{ post.content }}</p>
<a href="{% url 'postList' %}">Powrót</a>
```
Odpaliłam server `python manage.py runserver` i weszłam w link `http:/127.0.0.1:8000/`. Na stronie ukazały się utworzone wcześniej posty:

![view](https://i.postimg.cc/FRstyNBL/obraz-2026-03-10-142709767.png)

1. Commit:

