python3.6 -m pip install -r requirements.txt
python3.6 manage.py collectstatic
python3.6 manage.py makemigrations --noinput
python3.6 manage.py migrate --noinput
