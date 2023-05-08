from flask import *
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app=Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)

app.secret_key="aksara"

uri = "mongodb+srv://user:user123@mycluster.lboyezu.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db=client.member_system
collection=db.member_data


@app.route("/")
def home():
    if session:
        return redirect("/member")
    else:
        return render_template("Homepage.html")

    

@app.route("/error")
def error():
    error_message=request.args.get("em", "發生錯誤，請聯繫客服")
    return render_template("Errorpage.html", em=error_message)

@app.route("/signin", methods=["POST"])
def signin():
    email=request.form.get("email")
    password=request.form.get("password")
    comfirm=collection.find_one({
        "$and":[{"email":email},
        {"password":password}
    ]})
    if comfirm:
        session["name"]=comfirm["name"]
        return redirect("/")
    else:
        return render_template("Errorpage.html",em="密碼錯誤或信箱未註冊")
    
@app.route("/member")
def member():
    if session:
        return render_template("Memberpage.html",name=session["name"])
    else:
        return redirect("/")

@app.route("/signup")
def signup():
    return render_template("Signup.html")

@app.route("/signup_success", methods=["POST"])
def ss():
    name=request.form.get("name")
    email=request.form.get("email")
    password=request.form.get("password")

    com=collection.find_one({
        "email":email
    })
    if com:
        return render_template("Errorpage.html",em="信箱已經註冊")
    session["name"]=name
    comfirm=collection.insert_one({
        "name":name,
        "email":email,
        "password":password
    })
    if  comfirm:
        return render_template("Memberpage.html",name=name)
    else:
        return render_template("Errorpage.html")
    
@app.route("/signout")
def signout():
    del session["name"]
    return redirect("/")

app.run(port=3000)