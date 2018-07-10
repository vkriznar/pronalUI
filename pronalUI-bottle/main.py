from bottle import *
import webbrowser

static_directory = "./static"
tmp=[]



webbrowser.open('http://localhost:8080/index/')

@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_directory)

@get("/")
def blank():
    redirect('/index/')

@get("/index/")
def index():
    return template("index.html", napaka=None, adress="", description="", code="", rows=None, testi=False)

@post("/index/")
def index_post():
    naslov = request.forms.naslov
    opis = request.forms.opis
    koda = request.forms.koda
    global adress
    global description
    global code
    if all([naslov, opis, koda]):
        adress = naslov
        description = opis
        code = koda
        redirect("/index/testi/")
    else:
        return template("index.html", napaka="Vsa polja morajo biti izpolnjena")


@get("/index/testi/")
def index_testi():
    return template("index.html", adress=adress, description=description, code=code, napaka=None, rows=tmp, testi=True)

@post("/index/testi/")
def index_testi_post():
    "Če test nima določenega atributa vrne None namest praznega niza"
    rezultat = request.forms.rezultat if request.forms.rezultat != "" else "None"
    tmp.append([len(tmp)+1, request.forms.tipTesta, request.forms.niz, rezultat])
    redirect("/index/testi/")

run(host='localhost', port=8080, debug=True)