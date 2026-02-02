# Utilise l'image officielle Python
FROM python:3.12

# Définit le répertoire de travail
WORKDIR /app

# Empêche Python de stocker les fichiers pyc et active le log direct
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installe les dépendances système nécessaires à psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc

# Copie les fichiers du projet
COPY . .

# Installe pip et les dépendances Python
RUN pip install --upgrade pip
RUN pip install -r requirements_API.txt

# Expose le port 8000
EXPOSE 8000

# Démarre le serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
