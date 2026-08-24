from fastapi import FastAPI
from fastapi.responses import FileResponse
import psycopg2
import os

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "gpu_inventory")
DB_USER = os.getenv("DB_USER", "gpu_admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "gpu_password")


def get_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.get("/")
def dashboard():
    return FileResponse("static/index.html")


@app.get("/gpus")
def get_gpus():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT hostname, gpu_model, gpu_count, status, rack
        FROM gpu_nodes
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "hostname": row[0],
            "gpu_model": row[1],
            "gpu_count": row[2],
            "status": row[3],
            "rack": row[4]
        }
        for row in rows
    ]


@app.post("/provision/{hostname}")
def provision_gpu_node(hostname: str):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT status FROM gpu_nodes WHERE hostname = %s",
        (hostname,)
    )

    node = cursor.fetchone()

    if not node:
        cursor.close()
        conn.close()

        return {
            "status": "error",
            "message": "GPU node not found"
        }

    if node[0] != "available":
        cursor.close()
        conn.close()

        return {
            "status": "error",
            "message": "GPU node is not available"
        }

    cursor.execute(
        """
        UPDATE gpu_nodes
        SET status = 'provisioned'
        WHERE hostname = %s
        """,
        (hostname,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "status": "provisioned",
        "hostname": hostname,
        "message": "GPU node provisioned successfully"
    }
