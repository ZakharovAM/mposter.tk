# mposter.tk


Установка
Проверяем открытые порты для ubuntu
ufw status

Если какой-то порт не открыть - открыть можно вот так

ufw allow ssh
ufw allow http
ufw allow https
ufw allow imap
ufw allow порт <хоста_на_которой_проброшен_контейнер>  -- в бою не нужно тьак делать, нужно проксировать через nginx, но для тестов норм

Разработка шла под Windows, так что для корректной работы надо немного поправить файл mposter/boot.sh этой утилитой 

apt-get install dos2unix 


git clone https://github.com/ZakharovAM/mposter.tk

cd mposter.tk/
dos2unix mposter/boot.sh
docker build -t mposter_test .

docker run --name mposter -d -p <хоста_на_которой_проброшен_контейнер>:<порт_контейнера> mposter (вместо mposter можно указать другое имя для контейнера)


