# mining-covid
mining covid data from WHO

creating and using virtual environment:
python3 -m venv venv
source venv/bin/activate


commands:
'python manage.py dowload': download report files from WHO's page and save them in /reports
'python manage.py populate': populate database reading files from /reports
    extra:
        '--delete': empty database before populating