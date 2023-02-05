from connect import connect_with_connector
from flask import Flask, request
import sqlalchemy
from functools import reduce

table = "visitors"
ip_column = "ip"
visits_column = "visits"

app = Flask(__name__)

@app.before_first_request
def init_db() -> sqlalchemy.engine.base.Engine:
    global db
    db = connect_with_connector()
    return db

@app.route("/hits", methods=["GET", "POST"])
def get_hits():
    with db.connect() as conn:
        if request.method == "POST":
            ip = request.remote_addr
            ip2int = lambda ip: reduce(lambda a, b: (a << 8) + b, map(int, ip.split('.')), 0)
            ip = ip2int(ip)

            if is_unique(ip, conn):
                query = sqlalchemy.text("INSERT INTO visitors VALUES (:ip, 1)")
            else:
                query = sqlalchemy.text("UPDATE visitors SET visits=visits+1 WHERE ip=:ip")

            result = conn.execute(query, {"ip": ip})
            return { "rows-affected": result.rowcount }
        else:
            query = sqlalchemy.text("SELECT COUNT(ip) FROM visitors")
            hits = conn.execute(query).fetchone()

            return { "unique-visitors": hits[0]}

def is_unique(value, conn):
    query = sqlalchemy.text("SELECT EXISTS(SELECT 1 FROM visitors WHERE ip=:value LIMIT 1)")
    isUnique = conn.execute(query, {"value": value}).fetchone()

    return isUnique[0]

if __name__ == '__main__':
    app.run(port=8080, debug=True)
