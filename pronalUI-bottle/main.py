from bottle import *
import webbrowser

static_directory = "./static"
adress = None
description = None
code = None

webbrowser.open('http://localhost:8080/index/')

@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_directory)

@get("/")
def blank():
    redirect('/index/')

@get("/index/")
def index():
    return template("index.html", napaka=None)

@post("/index/")
def index_post():
    naslov = request.forms.naslov
    opis = request.forms.opis
    koda = request.forms.koda
    print(naslov, opis, koda)
    if all([naslov, opis, koda]):
        adress = naslov
        description = opis
        code = koda
        redirect("/index/")
    else:
        return template("index.html", napaka="Vsa polja morajo biti izpolnjena")


run(host='localhost', port=8080, debug=True)