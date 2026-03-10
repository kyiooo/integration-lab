# Laboratorium nr 2
**Temat:** Lokalna aplikacja Django - System Blodowy (praca z gałęziami)

## Dane autora
* **Imię i nazwisko:** [Małgorzata Andrzejewska]
* **Kierunek:** [Informatyka]
* **Grupa:** [235IC A2]
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

Otworzyłam plik *blog/models.py* gdzie wklęilam zawartość z instrukcji:

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
