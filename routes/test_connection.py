from flask import Flask, jsonify   
import psycopg2
import os
from flask import Blueprint
from ..db import get_connection
 
test_bp = Blueprint('test_connection', __name__, url_prefix='/')

@test_bp.route("/db-test")
def db_test():
    try:
        conn = psycopg2.connect(os.getenv("PG_URI"))
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({"database_time": result[0].isoformat()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500    