from flask import Flask,render_template , request
import sqlite3
import uuid
import json


#open cart file to sho

# configure the SQLite database, relative to the app instance folder
connctin_to_db =sqlite3.connect("pizzaApp.db",check_same_thread=False)
db_curser = connctin_to_db.cursor()
db_curser .execute("CREATE TABLE IF NOT EXISTS USERS(EMAIL TEXT , PASSWORD TEXT, cart_id TEXT)")

login = 0
signup =0
user_cart_id = tuple()
try:
    with open("cart.json") as f:
        cart = json.load(f)
except Exception as e:
    with open("cart.json","w") as f:
        json.dump(dict(), f)
cartid=None

# initialize the app with the extension



app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def homepage():
    
    global  db_curser
    global user_cart_id
    global cartid
    

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user_cart_id =tuple ( connctin_to_db.execute(f"SELECT cart_id FROM USERS WHERE EMAIL = '{email}'"))
        
        for i in user_cart_id:
            for j in i:
                cartid =str(j)
               
        if cartid !=None:
            if cartid in cart:
                mycart = cart[cartid]
                global login,signup
                login =1
                signup =1
        else:
            new_card_id = str(uuid.uuid1())
            db_curser.execute("insert into users values(?,?,?)",(email,password,new_card_id))
            cart[new_card_id] = []
            with open("cart.json","w") as f:
                json.dump(cart,f)

            connctin_to_db.commit()
    return render_template("index.html")
@app.route("/pizzaDetails/<slug>")
def pizza_details(slug):
    if signup==1 and login ==1:
        if slug == "cheez":
            return render_template("cheez.html")
        elif slug == "vege":
            return render_template("vege.html")
        elif slug == "mash":
            return render_template("mash.html")        
        
        
    else:
        return "Login first"

@app.route("/payments/<pizza>",methods=["POST"])
def payments(pizza):
    purchase = ""
    if pizza == "cheez":
        purchase = "chez pizza"
    elif  pizza == "vege":
        purchase = "vegetable pizza"
    elif pizza == "mash":
        purchase = "mushroom pizza"
    cart[cartid].append(purchase)
    with open("cart.json","w") as f:
            json.dump(cart, f)
    return render_template("payments.html")
@app.route("/history")
def history ():
    if login ==1 and signup ==1:
        return render_template("his.html", items = cart[cartid])
    else:
        return "login first"
 
@app.route("/logout")
def logout():
    global signup,login
    signup,login =0,0
    return "YOU ARE LOGGED OUT"
        


    

    

app.run()