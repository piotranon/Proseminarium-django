# Proseminarium-django

Pobranie danych do testów.  
https://drive.google.com/file/d/1SEDg_HJRCUarff1YMRXCHjv7mJhdrXFy/view?usp=sharing  
Pobrany plik trzeba wrzucić do folderu api pod nazwą dataset.csv

Pierwsze uruchomienie  
( docker wymagany do obsługi aplikacji )  
Pierwsze uruchomienie aplikacji w folderze z pobranym repozytorium trzeba wywołać :  
```
docker-compose build  
docker-compose up -d
```  
Następnie w obrazie clickhouse trzeba się połączyć przez konsolę dostępną w dockerze i wywołać polecenia:  
```su  
apt update  
apt install ssh  
adduser piotranon  
passwd piotranon
``` 
Następnie w projekcie w pliku znajdujacym się pod ścieżką :  
api/api/views.py w linii 15 należy zmienić adres ip na adres sieciowy wewnętrzny urządzenia na którym uruchomiona jest aplikacja.
