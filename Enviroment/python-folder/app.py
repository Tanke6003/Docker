from fastapi import FastAPI, HTTPException
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
@app.get("/getLastMessage")
def getLastMessage():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Modificar la consulta para obtener el último mensaje de la base de datos
        query = "SELECT Text FROM SYS_Message ORDER BY PKMessage DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result:
            return {"last_message": result[0]}
        else:
            return {"last_message": "No hay mensajes"}

    except mysql.connector.Error as err:
        # Manejo de la excepción en caso de error en la base de datos
        return HTTPException(status_code=500, detail="Error al obtener el último mensaje de la base de datos")
@app.post("/saveMessage")
def save_message(oMessage: dict):
    try:
        message = oMessage.get("message")
        if not message:
            raise HTTPException(status_code=422, detail="El campo 'message' es requerido")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Modificar la consulta para insertar el mensaje en la base de datos
        query = "INSERT INTO SYS_Message (Text) VALUES (%s)"
        values = (message,)
        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return {"message": "Mensaje guardado exitosamente"}
    except mysql.connector.Error as err:
        # Manejo de la excepción en caso de error en la base de datos
        return HTTPException(status_code=500, detail="Error al guardar el mensaje en la base de datos")