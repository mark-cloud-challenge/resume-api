from connect import connect_with_connector
from flask import Flask, request
import sqlalchemy 

app = Flask(__name__)

@app.before_first_request
def init_db() -> sqlalchemy.engine.base.Engine:
    global db
    db = connect_with_connector()
    return db

@app.route("/hits", methods=["GET", "POST"])
def get_hits():
    if request.method == "POST":
        ip = request.remote_addr
        ip2int = lambda ip: reduce(lambda a, b: (a << 8) + b, map(int, ip.split('.')), 0)
        ip = ip2int(ip)
        
        query = sqlalchemy.text("INSERT INTO visitors VALUES (:ip, 1)")
        conn.execute(query, ip=ip)
    else:
        with db.connect() as conn:
            query = sqlalchemy.text("SELECT COUNT(visits) FROM visitors")
            hits = conn.execute(query).fetchone()

        return { "unique-visitors": hits[0]}

if __name__ == '__main__':
    app.run(port=8080, debug=True)
