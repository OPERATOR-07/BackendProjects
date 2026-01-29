from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
import sqlite3 as db
import hashlib

conn = db.connect("Mydatabase.db")
cursor = conn.cursor()
    
cursor.execute("""create table Users(
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Email TEXT UNIQUE,
        Password TEXT
    );""")
conn.commit()
conn.close()
#print("Database created"))

app = Flask(__name__)

app.secret_key = "mysecretkey3"

@app.route("/register", methods=["POST","GET"])
def Register():  
    if request.method == "POST":  
        email = request.form["email"]
        name = request.form["username"]
        password = hashlib.sha256(request.form["password"].encode()).hexdigest()

        with db.connect("Mydatabase.db") as conn:
            cursor = conn.cursor()
            cursor.execute("select Email from Users where Email = ?;", (email,))
            check = cursor.fetchone()
            if check == None:
                cursor.execute("insert into Users(Name, Email, Password) values(?,?,?)", (name, email, password))
                conn.commit()
            else:
                flash("Email already Exist!!", "error")
                return render_template("register.html")
            
            # conn.close()  
    else:
        return render_template("register.html")
    
    return redirect(url_for("index")) 

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        password = hashlib.sha256(request.form["password"].encode()).hexdigest() # <--- i know using sha256 is not safe but im just learing

        with db.connect("Mydatabase.db") as conn:
            cursor = conn.cursor()
            cursor.execute("select Email from Users where Email = ?;", (email,))
            e = cursor.fetchall()
            # emails = [i[0] for i in cursor.execute("select Email from Users;")]
            cursor.execute("select Password from Users where Password = ?;", (password,))
            p = cursor.fetchall()
        

        if e == [] or p == []:
            flash("incorrect Login", "error")
            return render_template("index.html")
        else:
            session["email"] = email   
            return redirect(url_for("Home"))  
    else:
        return render_template("index.html") 
    
@app.route("/home")
def Home():
    if "email" not in session:
        abort(400)
        # return redirect(url_for("index"))
    with db.connect("Mydatabase.db") as conn:
        email = session["email"]
        cursor = conn.cursor()
        cursor.execute("select Name from Users where Email = ?;", (email,))
        nm = cursor.fetchone()
        
    flash("Successful Login!!","success")    
    return render_template("Home.html", name = nm[0])

    

if __name__ == "__main__":
    app.run(debug = True)

# i just love python

