# Laboratorium nr 1
**Temat:** Konfiguracja środowiska i praca z systemem kontroli wersji.

## Dane autora
* **Imię i nazwisko:** [Małgorzata Andrzejewska]
* **Kierunek:** [Informatyka]
* **Grupa:** [235IC A2]

----
### Punkt 1
1. Instalacja Git oraz Python  - done
2. Konfiguracja nazwy użytkownika i emaila w Git:\
Skonfigurowałam git'a wpisując w terminalu następujące komendy:
```
git config --global user.name "Malgorzata Andrzejewska" 
git config --global user.email "gosik123-01@wp.pl"
```
1. Generowanie kluczy SSH:\
Wpisałam komendę `ssh-keygen -t ed25519 -C "gosik123-01@wp.pl`
i wygenerowałam klucz ssh, akceptując domyślną scieżkę.


![Generowanie klucza ssh](https://i.postimg.cc/bJBDJNRt/ssh-lepsze.png) 

Następnie skopiowałam zawartość klucza publicznego za pomocą komendy `type %USERPROFILE%\.ssh\id_ed25519.pub` ,ponieważ operuję w systemie Windows. Przeszłam na swoje konto Github, następnie w zakładkę Settings, kolejno SSH and GPG Keys, utworzyłam nowy klucz ssh i wkleiłam tam wartość klucza publicznego, którego skopiowałam wcześniej. Dla upewnienia, że dobrze skonfigurowałam połączenie z Github wykonałam komendę: `ssh -T git@github.com`.

![Generowanie klucza ssh](https://i.postimg.cc/3NY6kYJx/ssh-test.png)

1. Zadanie Markdown:\
Utworzyłam plik README.md w folderze roboczym Lab1-Andrzejewska\
Następnie w terminalu wpisałam następujące komendy:
```
python -m venv venv
.\venv\Scripts\activate
pip install django
```
W trakcie musiałam się posłużyć komendą:\
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`\
gdyż trafiłam na SecurityError, ponieważ Windows domyślnie blokuje uruchamianie skryptów w PowerShellu.

Po utworzeniu i aktywacji środowiska przeszłam do instalacji framework'a Django - done

----
#### Dokumentacja i źródła
* [Oficjalna dokumentacja Django](https://docs.djangoproject.com/en/6.0/)
* [Dokumentacja modułu venv](https://docs.python.org/3/library/venv.html)
* [Tutorial Markdown na GitHubie](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

----

## Punkt 2

Zainicjalizowałam projekt komendą: `django-admin startproject core .`\
Aktualnie mój folder roboczy jest kompletny i prezentuje się następująco:

![Generowanie klucza ssh](https://i.postimg.cc/y6rRvncQ/Zrzut-ekranu-2026-03-04-113348.png)

