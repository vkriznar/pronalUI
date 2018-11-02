from bottle import *
import webbrowser
from Problem import Problem
from ProblemPart import ProblemPart, CheckEqual, CheckSecret
import requests
import time
import json
import bottle
import os

static_directory = "./static"

"Global spremenljivke"
active_test = "chkeql"
je_bila_izbrisana = False
podnaloge_za_osvezit = []
preostevilcenje = []
trenutno_osvezena = None
popup = False
filename = ""

app = bottle.default_app()
BaseTemplate.defaults['get_url'] = app.get_url

webbrowser.open('http://localhost:8080/')

"Funckija ki redirecta iz '/' na zacetno stran"
@route('/')
def index():
    redirect('/index/')


"Staticni route za css in js file"
@route('/static/<filename:path>', name='static')
def serve_static(filename):
    return static_file(filename, root=static_directory)


"Zacetna stran kjer uporabnik izbire datoteko za urejanje"
@get("/index/")
def index():
    global popup
    return template("index.html", popup=popup)


##"Route kjer se iz izbrane datoteke parsa in se preveri ce je"
##@post('/upload')
##def upload():
##    global file
##    global popup
##    global problem
##    file = request.files.get('file')
##    "preverimo ce je vnesena datoteka res python datoteka"
##    if os.path.splitext(file.filename)[1] != ".py":
##        """ce ni, ga redirectamo nazaj na osnovno stran, ter na spletni strani se mu pojavi popup ki mu pove, da so
##         dovoljena samo python datoteke"""
##        popup = True
##        redirect("/index/")
##    else:
##        popup = False
##        problem = Problem.read_filefile(file.file)
##        "za vsako podnalogo se odpre zavihek z to podnalogo, time sleep je zato da se v pravilnem vrstnem redu odprejo"
##        for i in range(len(problem.parts)):
##            time.sleep(0.05)
##            webbrowser.open('http://localhost:8080/index/naloga/podnaloga{}/'.format(i + 1))
##
##        redirect("/index/naloga/")

@route('/upload', method='POST')
def do_upload():
    global popup
    global problem
    global filename
    upload = request.files.get('file')
    filename, ext = os.path.splitext(upload.filename)
    if ext not in ('.py','.txt'):
        popup = True
        redirect("/index/")

    file_path = "{path}/{file}".format(
        path="datoteke/uporabnik", file=upload.filename)

    with open(file_path, 'wb') as f:
        f.write(upload.file.read())
    
    popup = False
    problem = Problem.load_file(file_path)
    for i in range(len(problem.parts)):
        time.sleep(0.05)
        webbrowser.open('http://localhost:8080/index/naloga/podnaloga{}/'.format(i + 1))

    redirect("/index/naloga/")





"Funkcija ki preostevilci vrstni red podnalog"
@get('/preostevilci<part_num><num>')
def preostevilci(part_num, num):
    global preostevilcenje

    part_num = int(part_num)
    preostevilcenje.append({part_num, int(num)})

    redirect("/index/naloga/podnaloga{}/".format(part_num))


"stran, kjer uporabnik vpise naslov naloge, in opis naloge"
@get("/index/naloga/")
def naloga():
    global problem
    
    return template("naloga.html", napaka=None, adress=problem.title, description=problem.description, code="")


"Route, kjer se shrani kar je uporabnik vpisal za naslov in opis podnaloge. Naloga mora imeti naslov."
@post("/index/naloga/")
def naloga_post():
    if request.forms.naslov:
        "shrani si vpisan naslov in opis naloge"
        problem.title = request.forms.naslov
        problem.description = request.forms.opis
        return template("naloga.html", napaka=None, adress=problem.title, description=problem.description)
    else:
        return HTTPResponse("Spremembe niso shranjene. Naloga mora imeti naslov!")


"Funckija, ki izbrise izbrano podnalogo"
@get("/index/naloga/podnaloga_izbrisi<part_num>/")
def podnaloga_izbrisi(part_num):
    global problem
    global je_bila_izbrisana
    global podnaloge_za_osvezit
    "part_num dobimo v obliki stringa zato ga je najprej treba pretvoriti v intiger"
    part_num = int(part_num)
    del problem.parts[part_num-1]
    """ko smo zbrisali eno izmed podnalog moramo vse podnaloge z vecjim part_num, njihov part_num zmanjsati za ena
    to naredimo tako da shranimo vecje podnaloge v list in potem ko se stran osvezi preverimo, ce je ta stran v tem
    listu in ce je ji zmanjsamo part_num za ena"""
    podnaloge_za_osvezit = [i for i in range(part_num+1, len(problem.parts)+2)]

    return HTTPResponse("Izbrisali ste podnalogo {0}. Osvežite preostale podnaloge.".format(part_num))


"Stran s podnalogo, 'part_num' oznacuje specificno podnalogo na kateri se trenutno nahajamo"
@get("/index/naloga/podnaloga<part_num>/")
def podnaloga(part_num):
    global problem
    global active_test
    global trenutno_osvezena
    global podnaloge_za_osvezit

    part_num = int(part_num)
    active_test = "chkeql"

    if part_num > len(problem.parts):
        problem_part = problem.parts[-1]
    else:
        problem_part = problem.parts[part_num-1]

    if podnaloge_za_osvezit:
        if part_num in podnaloge_za_osvezit:
            if trenutno_osvezena != part_num:
                podnaloge_za_osvezit.remove(part_num)
                """da se nebi part_num 3 osvezil na 1(npr. ce izbrisemo podnalogo 1), moramo prepriciti da se prvic 
                osvezi podnaloga z part_num 2 zato to shranimo v trenutno_osvezena"""
                if podnaloge_za_osvezit:
                    trenutno_osvezena = part_num-1
                redirect("/index/naloga/podnaloga{}/".format(part_num-1))
            else:
                trenutno_osvezena = None
    return template("podnaloga.html", napaka=None,
                    description=problem_part.description, code=problem_part.solution,
                    precode=problem_part.precode, tests=problem_part.tests,
                    active_test=active_test, part_num=part_num)


"Funkcija ki procesira vsa urejanja na tocno dolocenem testu"
@get("/index/naloga/podnaloga<part_num>/<test_type>-<edit>-<group_id>-<i>/")
def edit_tests(part_num, test_type, edit, group_id, i):
    global problem

    part_num = int(part_num)
    group_id = int(group_id)
    i = int(i)

    problem_part = problem.parts[part_num-1]
    tests = problem_part.tests
    
    if test_type == "chkeql":
        test_group = tests["check_equal"][group_id]
        test = tests["check_equal"][group_id][i]
    elif test_type == "chksct":
        test_group = tests["check_secret"][group_id]
        test = tests["check_secret"][group_id][i]

    if edit == "delete":
        problem_part.remove_test(test)
    elif edit == "move":
        problem_part.description += "\n\n    >>> " + test.expression + "\n    " + test.output

    elif edit == "move_down":
        test_type = "check_equal" if test_type == "chkeql" else "check_secret"
        if i == len(test_group)-1:
            problem_part.move_test_group_down(test_type, group_id)
        else: 
            problem_part.move_test_within_group_down(test_type, group_id, i)
            
    elif edit == "move_up":
        test_type = "check_equal" if test_type == "chkeql" else "check_secret"
        if i == 0:
            problem_part.move_test_group_up(test_type, group_id)
        else: 
            problem_part.move_test_within_group_up(test_type, group_id, i)

    redirect("/index/naloga/podnaloga{}/".format(part_num))


"Route, ki je v pomoc zato, da ko se ustvari nova podnaloga ji funkcija dodeli pravi part_num"
@get("/index/naloga/podnaloga/")
def podnaloga_get_def():
    global problem

    part_num = len(problem.parts)
    problem.new_problem_part()
    redirect("/index/naloga/podnaloga{}/".format(part_num + 1))


"Fukcija, ki shrani vse vnesene spremembe za doloceno podnalogo"
@post("/index/naloga/podnaloga<part_num>/")
def podnaloga_post(part_num):
    global problem
    global preostevilcenje

    part_num = int(part_num)
    if part_num > len(problem.parts) and part_num in podnaloge_za_osvezit:
        problem_part = problem.parts[part_num-2]
    else:
        problem_part = problem.parts[part_num-1]
    tests = problem_part.tests

    if request.forms.opis:
        problem_part.description = request.forms.opis
        problem_part.solution = request.forms.koda
        problem_part.precode = request.forms.prekoda
    if request.forms.prekoda_gor == "True":     # To ni isto kot "boolean == True", ker je "True" string
        problem_part.precode_to_description()

    else:
        global active_test
        if request.forms.tipTesta == "chkeql":
            # in python format (0 starts)
            test_num = int(request.forms.stevilka) - 1
            check_equal_test = CheckEqual(request.forms.niz, request.forms.rezultat)
            if test_num == len(tests["check_equal"]):
                tests["check_equal"].append([check_equal_test])
            elif test_num > len(tests["check_equal"]):
                return HTTPResponse("Test ni dodan. Številka skupine mora biti med 1 in {0}!".format(len(tests["check_equal"])+1))
            else:
                tests["check_equal"][test_num].append(check_equal_test)
            active_test = "chkeql"

        elif request.forms.tipTesta == "chksct":
            # in python format (0 starts)
            test_num = int(request.forms.stevilka) - 1
            check_secret_test = CheckSecret(request.forms.niz1, request.forms.niz2)
            if test_num == len(tests["check_secret"]):
                tests["check_secret"].append([check_secret_test])
            elif test_num > len(tests["check_secret"]):
                return HTTPResponse("Test ni dodan. Številka skupine mora biti med 1 in {0}!".format(len(tests["check_secret"])+1))
            else:
                tests["check_secret"][test_num].append(check_secret_test)

            active_test = "chksct"
        else:
            tests["other"] = request.forms.other

    if request.forms.changes:
        json_dict = json.loads(request.forms.changes)

        for test_type in json_dict:
            print(json_dict)
            for test_data in json_dict[test_type]:
                group_id = int(test_data["group_id"]) - 1
                #group_id_stara = int(test_data["group_id"]) - 1
                i = int(test_data["index"]) - 1
                expression = test_data["expression"]
                output = test_data["output"] if test_type == "check_equal" else test_data["other"]
                problem_part.change_test_by_id(test_type, group_id, i, expression, output)

    redirect("/index/naloga/podnaloga{}/".format(part_num))


##"Route, ki odda nalogo in jo shrani na racunalnik"
##@get("/pretvori/")
##def pretvori():
##    global file
##    "shranimo nalogo na racunalnik. To je treba se spremeniti, zdaj je tocno doloceno mesto!"
##    file_name = "../edit_files/" + file.filename
##    problem.write_on_file(file_name[:-5] + "out.py")
##    url = "http://localhost:8080/index/"
##    files = {'file': open('neki.txt', 'rb')}
##    r = requests.post(url, files=files)
##    print(r.text)
##
##    return HTTPResponse("Naloga je shranjena.")

@get("/pretvori/")
def pretvori():
    global problem
    global filename
    filename_out = filename+"_out.py"
    problem.write_on_file("download/{file}".format(file=filename_out))
    redirect("/download/{file}".format(file=filename_out))

@route('/download/<filename:path>')
def download(filename):
    return static_file(filename, root="download", download=filename)


run(host='0.0.0.0', port=8080, debug=True)
