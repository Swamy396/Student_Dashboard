import tornado.ioloop
import tornado.web
import json
import pymysql
from decimal import Decimal

host = "127.0.0.1"
duser = 'root'
dname = 'practice'
dpassword = 'Swamy@1234'

def get_connection():
    return pymysql.connect(
        host=host, user=duser, password=dpassword, db=dname,
        cursorclass=pymysql.cursors.DictCursor
    )

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

class Enter(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()

    def post(self):
        data = json.loads(self.request.body)
        name = data.get("name")
        year = data.get("year")
        fee = data.get("fee")
        paid = data.get("paid")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO student (name, year, fee, paid) VALUES (%s, %s, %s, %s)",
            (name, year, fee, paid)
        )
        conn.commit()
        conn.close()
        self.write({"status": "Value inserted"})

class Printing(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()

    def get(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        self.write(json.dumps(result, cls=CustomJsonEncoder))

class paying(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "PATCH, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()

    def patch(self):
        data = json.loads(self.request.body)
        id = data.get("id")
        amount = data.get("amount")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE student SET paid = paid + %s WHERE id = %s", (amount, id)) 
        conn.commit()
        conn.close()
        self.write({"status": "Updated"})

class Deleting(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "DELETE, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()

    def delete(self):
        data = json.loads(self.request.body)
        id = data.get("id")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        self.write({"status": "Deleted the record"})

def make_app():
    return tornado.web.Application([
        (r"/enter", Enter),
        (r"/print", Printing),
        (r"/pay", paying),
        (r"/delete", Deleting)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server started at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
