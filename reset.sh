psql -c "drop database djbp;" &&
psql -c "create database djbp;" &&
rm main/migrations/* &&
touch main/migrations/__init__.py &&
./manage.py makemigrations &&
./manage.py migrate &&
./manage.py init
