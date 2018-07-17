from bottle import *
import webbrowser

static_directory = "./static"
sklop = []
active_test = "chkeql"



webbrowser.open('http://localhost:8080/index/')

@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_directory)

@get("/")
def blank():
    redirect('/index/')

@get("/index/")
def index():
    return template("index.html", napaka=None, adress="", description="", code="")

@post("/index/")
def index_post():
    naslov = request.forms.naslov
    opis = request.forms.opis
    if naslov:
        sklop.append([naslov, opis])
        return template("index.html", napaka=None, adress=naslov, description=opis)

@get("/index/podnaloga/")
def podnaloga():
    global active_test
    active_test = "chkeql"
    return template("podnaloga.html", napaka=None, description="", code="", precode="", rows=None, testi=False, active_test=active_test, title="Podnaloga")

@post("/index/podnaloga/")
def podnaloga_post():
    opis = request.forms.opis
    koda = request.forms.koda
    prekoda = request.forms.prekoda
    if all([opis, koda, prekoda]):
        sklop.append([opis, prekoda, koda, [[], [], []]])
        redirect("/index/podnaloga/testi/")
    else:
        return template("podnaloga.html", napaka="Vsa polja morajo biti izpolnjena")


@get("/index/podnaloga/testi/")
def podnaloga_testi():
    print(sklop[-1][3][2])
    return template("podnaloga.html", description=sklop[-1][0], precode=sklop[-1][1],
                    code=sklop[-1][2], napaka=None, rows=sklop[-1][3], testi=True, active_test=active_test, title="Podnaloga")

@post("/index/podnaloga/testi/")
def podnaloga_testi_post():
    "Če test nima določenega atributa vrne None namest praznega niza"
    global active_test
    if request.forms.tipTesta == "chkeql":
        sklop[-1][3][0].append([request.forms.stevilka, request.forms.niz, request.forms.rezultat])
        active_test = "chkeql"
    elif request.forms.tipTesta == "chksct":
        sklop[-1][3][1].append([request.forms.stevilka, request.forms.niz1, request.forms.niz2])
        active_test = "chksct"
    else:
        sklop[-1][3][2].append(zamenjaj(request.forms.other))
        active_test = "other"
    redirect("/index/podnaloga/testi/")

@get("/pretvori/")
def pretvori():
    "Tukej se bo zej v ozadju poklicalo in vsi bomo srecni"
    for array in sklop:
        print(array)
    return HTTPResponse("Uspelo ti je!")

def zamenjaj(string):
    chars = list(string)
    for i in range(0, len(chars)):
        if chars[i] == "\n":
            chars[i] = "<br>"
        if chars[i] == " ":
            chars[i] = "&nbsp"
        if chars[i] == "\r":
            chars[i] = ""
    return "".join(chars)


run(host='localhost', port=8080, debug=True)
