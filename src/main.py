from bottle import *
import webbrowser
from Problem import Problem
from ProblemPart import ProblemPart, CheckEqual, CheckSecret
import time

static_directory = "./static"
active_test = "chkeql"
testi = False

webbrowser.open('http://localhost:8080/index/')
    
@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_directory)

@get("/")
def blank():
    redirect('/index/')

@post('/upload')
def upload():
    global file_name
    file = request.files.get('file')
    # only allow upload of text files
    if file.content_type != "text/plain":
        return HTTPResponse("Uspelo ti ni!")
    file_name = file.filename
    "Z file.file dostopamo do nase datoteke, npr."
    for line in file.file:
        "moramo dekodirati, ker je zapisana v bitih"
        print(line.decode().rstrip('\n'))
    "redirect na obstojeco, ki je zaenkrat tako, da ne uposteva uploadanga fila, ker je treba spremeniti Problem.py"
    return redirect("/index/obstojeca")

@get("/index/")
def index():
    return template("index.html")

"Zacetna stran kjer uporabnik izbire, ali bo ustvaril novo datoteko ali bo vnesel ze obstojeco datoteko za urejanje"
@get("/index/<izbira>")
def nova_naloga(izbira):
    global problem
    global file_name
    if izbira == "nova":
        #tukaj se ustvari nov Problem ki ima prazne atribute
        redirect("/index/naloga/")
    elif izbira == "obstojeca":
        file_name = "../edit_files/naloga"
        problem = Problem.load_file(file_name + "_in.py")
        for i in range(len(problem.parts)):
            time.sleep(0.05)
            webbrowser.open('http://localhost:8080/index/naloga/podnaloga{}/'.format(i + 1))
        redirect("/index/naloga/")

@get("/index/naloga/")
def naloga():
    global problem
    adress = problem.title
    description = problem.description
    
    return template("naloga.html", napaka=None, adress=adress, description=description, code="")

@post("/index/naloga/")
def naloga_post():
    if request.forms.naslov:
        problem.title = request.forms.naslov
        problem.description = request.forms.opis
        return template("naloga.html", napaka=None, adress=problem.title, description=problem.description)
    else:
        return HTTPResponse("Uspelo ti ni!")

@get("/index/naloga/podnaloga<part_num>/")
def podnaloga(part_num):
    global problem
    part_num = int(part_num)
    global active_test
    active_test = "chkeql"

    problem_part = problem.parts[part_num-1]
    
    description = problem_part.description
    solution = problem_part.solution
    precode = problem_part.precode
    tests = problem_part.tests

    tests_equal = tests["check_equal"]
    tests_secret = tests["check_secret"]
    test_other = tests["other"]

    tests_equal = [[str(i+1), z.expression, z.output] for i in range(len(tests_equal)) for z in tests_equal[i]]
    tests_secret = [[str(i+1), z.expression, z.other] for i in range(len(tests_secret))for z in tests_secret[i]]
    test_other = [test_other]
    tests_data = [tests_equal, tests_secret, test_other]
    
    return template("podnaloga.html", napaka=None,
                    description=description, code=solution,
                    precode=precode, rows=tests_data, testi=testi,
                    active_test=active_test, title="Podnaloga {}".format(part_num))


@get("/index/naloga/podnaloga/")
def podnaloga_get_def():
    global problem
    part_num = len(problem.parts)
    problem.new_problem_part()
    redirect("/index/naloga/podnaloga{}/".format(part_num + 1))

@post("/index/naloga/podnaloga<part_num>/")
def podnaloga_post(part_num):
    global problem
    global testi
    testi = False
    part_num = int(part_num)
    problem_part = problem.parts[part_num-1]
    tests = problem_part.tests

    if request.forms.opis:
        problem_part.description = request.forms.opis
        problem_part.solution = request.forms.koda
        problem_part.precode = request.forms.prekoda

    else:
        global active_test
        testi = True
        if request.forms.tipTesta == "chkeql":
            # in python format (0 starts)
            test_num = int(request.forms.stevilka) - 1
            check_equal_test = CheckEqual(request.forms.niz, request.forms.rezultat)
            if test_num == len(tests["check_equal"]):
                tests["check_equal"].append([check_equal_test])
            elif test_num > len(tests["check_equal"]):
                return HTTPResponse("Uspelo ti ni!")
            else:
                tests["check_equal"][test_num].append(check_equal_test)
            active_test = "chkeql"

        elif request.forms.tipTesta == "chksct":
            # in python format (0 starts)
            test_num = int(request.forms.stevilka) - 1
            check_secret_test = CheckSecret(request.forms.niz1, request.forms.niz2)
            if test_num == len(tests["check_secret"]) + 1:
                tests["check_secret"].append([check_secret_test])
            elif test_num > len(tests["check_secret"]):
                return HTTPResponse("Uspelo ti ni!")
            else:
                tests["check_secret"][test_num].append(check_secret_test)

            active_test = "chksct"
        else:
            tests["other"] += (request.forms.other)
    redirect("/index/naloga/podnaloga{}/".format(part_num))


@get("/pretvori/")
def pretvori():
    problem.write_on_file(file_name + "_out.py")
    return HTTPResponse("Uspelo ti je!")

"""def zamenjaj(string):
    chars = list(string)
    for i in range(0, len(chars)):
        if chars[i] == "\n":
            chars[i] = "<br>"
        if chars[i] == " ":
            chars[i] = "&nbsp"
        if chars[i] == "\r":
            chars[i] = ""
    return "".join(chars)"""


run(host='localhost', port=8080, debug=True)
