# mining-covid
Extracting COVID data from PDFs found in WHO's website


Commands
- `python -m venv venv`: create virtual environment
- `source venv/bin/activate`: start using virtual environment
- `pip install -r requirements.txt`: install packages listed in requirements.txt
- `python manage.py <command>`
  - `makemigrations`: load model changes
  - `migrate`: execute model changes
  - `download` : download report files from WHO's page and save them in /reports
  - `populate` : populate database reading files from /reports
    - `--delete`: empty database before populating
