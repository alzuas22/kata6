from mi_cartera import app
from flask import render_template, request, redirect
import csv

#Punto de entrada 
@app.route("/")
def index():
    
    f = open("movements.dat", "r")
    reader = csv.DictReader(f, delimiter=",",quotechar='"')
    movements = list(reader)
    return render_template("index.html", the_movements=movements)

@app.route("/new_movement", methods= ["GET", "POST"])
def new_mov():
    if request.method == "GET":
        return render_template("new.html")
    else: 
        data=request.form 
        f = open("movements.dat", "a")
        writer = csv.DictReader(f, fieldnames=data.keys())
        writer.writerow(data)
        return redirect("/")
