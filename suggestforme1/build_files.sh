# build_files.sh
pip install -r requirements.txt
python makemigrations
python migrate
python manage.py collectstatic