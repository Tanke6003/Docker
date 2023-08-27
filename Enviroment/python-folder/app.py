from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
config = {
    'user': 'tanke',
    'password': 'tanke',
    'host': 'STG_MariaDB',
    'database': 'Test',
}

app = FastAPI()
# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Esto permite cualquier origen, pero no es seguro para producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/my-first-api")
def hello():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    query = "SELECT Text FROM Sys_Message LIMIT 1"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return "{"+str(results)+"}"
