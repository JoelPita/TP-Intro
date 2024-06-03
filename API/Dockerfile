FROM python:3.12-slim

# Instalar pipenv
RUN pip install pipenv

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos Pipfile y Pipfile.lock
COPY Pipfile Pipfile.lock /app/

# Instalar las dependencias del Pipfile
RUN pipenv install --deploy --ignore-pipfile

# Instalar Flask y otras dependencias manualmente
# RUN pipenv run pip install flask flask_sqlalchemy pymysql

# Listar los paquetes instalados para verificar que Flask está instalado
RUN pipenv run pip list

# Copiar el contenido del proyecto
COPY . .

# Exponer el puerto en el que correrá la aplicación
EXPOSE 5000

# Definir el comando por defecto
CMD ["pipenv", "run", "python", "app/app.py"]