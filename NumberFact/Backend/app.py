import tornado.ioloop
import tornado.web
import requests
import json
import pymysql
import datetime
import jwt

dbhost="localhost"
dbname="Collage"
user="root"
password="Swamy@1234"

key = "jwt_checking_1234"
algorithm = "HS256"

def create_jwt(payload):
    payload['exp']=datetime.datetime.utcnow()+datetime.timedelta(seconds=3600)
    token=jwt.encode(payload,key,algorithm)
    return token
def verify_jwt(token):
    try:
        payload=jwt.decode(token,key,algorithms=[algorithm])
        return payload
    except:
        return {"status":"Session Expired please login again"}


def get_connection():
    return pymysql.connect(host=dbhost,
    user=user,
    password=password,
    database=dbname,
    cursorclass=pymysql.cursors.DictCursor
    )

class Register(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", " Content-Type")
        self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()

    def post(self):
        data=json.loads(self.request.body)
        id=data.get("id")
        name=data.get("name")
        password=data.get("password")
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("select * from student_details where id=%s",(id,))
        responce=cursor.fetchone()
        if responce:
            self.write({"status":"User already exist"})
            cursor.close()
            conn.close()
            return
        cursor.execute("insert into student_details values(%s,%s,%s)",(id,name,password))
        conn.commit()
        cursor.close()
        conn.close()
        self.write({"status":"Registered successfully"})

class Login(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Authorization,Content-Type")
        self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()
    
    def post(self):
        data=json.loads(self.request.body)
        id=data.get("id")
        password=data.get("password")
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("select * from student_details where id=%s",(id,))
        result=cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            if password==result['password']:
                token=create_jwt({"id":id,"name":result['name']})
                self.write({"token":token,"status":"Token Generated successfully"})
            else:
                self.write({"status":"You have entered wrong username or password"})
        else:
            self.write({"status":"User Details Not found"})




class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Authorization,Content-Type")
        self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()
    def post(self):
        auth_header=self.request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            access=auth_header.split(" ")[1]
            result=verify_jwt(access)
            if "status" in result:
                self.write({"status":result['status']})
                return
            data = json.loads(self.request.body)
            month = data.get("month")
            day = data.get("day")

            url = f"https://numbersapi.p.rapidapi.com/{month}/{day}/date"

            headers = {
                'x-rapidapi-key': "37e2c0d968msh840a0ac2f384670p170f17jsn0f3545564fe0",
                'x-rapidapi-host': "numbersapi.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers)

            self.write({"result": response.text})


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/register",Register),
        (r"/login",Login),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server running at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()