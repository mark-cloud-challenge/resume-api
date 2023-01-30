from connect import connect_with_connector
from flask import Flask
import sqlalchemy 

app = Flask(__name__)

@app.before_first_request
def init_db() -> sqlalchemy.engine.base.Engine:
    global db
    db = connect_with_connector()
    return db

@app.route("/hits", methods=["GET"])
def get_hits() -> int:
    with db.connect() as conn:
        query = sqlalchemy.text("SELECT hits IN counter")
        hits = conn.execute(query).fetchone()

    return hits

if __name__ == '__main__':
    app.run(port=8080, debug=True)
