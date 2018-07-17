from bottle import *
import webbrowser
from Problem import Problem
from ProblemPart import ProblemPart, CheckEqual, CheckSecret

static_directory = "./static"
active_test = "chkeql"
problem  = None
part_num = 1


webbrowser.open('http://localhost:8080/index/')

@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_directory)

@get("/")
def blank():
    redirect('/index/')

@get("/index/")
def index():
    global problem
    file_name = "../edit_files/naloga" + "_in.py"
    problem = Problem.load_file(file_name)
    adress = problem.title
    description = problem.description
    
    return template("index.html", napaka=None, adress=adress, description=description, code="")

@post("/index/")
def index_post(): 
    naslov = request.forms.naslov
    opis = request.forms.opis
    if naslov:
        sklop.append([naslov, opis])
        return template("index.html", napaka=None, adress=naslov, description=opis)

@get("/index/podnaloga/")
def podnaloga():
    global problem
    global part_num
    global active_test
    active_test = "chkeql"

    problem_part = problem.parts[part_num-1]
    
    description = problem_part.description
    solution =  problem_part.solution
    precode = problem_part.precode
    tests = problem_part.tests

    tests_equal = tests["check_equal"]
    tests_secret = tests["check_secret"]
    test_other = tests["other"]

    

                   
    tests_equal = [[str(i+1), z.expression, z.output] for i in range(len(tests_equal)) for z in tests_equal[i]]
    tests_secret = [[str(i+1), z.expression, z.other] for i in range(len(tests_secret))for z in tests_secret[i]]
    test_other = [zamenjaj(test_other)]
    tests_data = [tests_equal, tests_secret, test_other]
    
    return template("podnaloga.html", napaka=None,
                    description=description, code=solution,
                    precode=precode, rows=tests_data, testi=True,
                    active_test=active_test, title="Podnaloga")

@post("/index/podnaloga/")
def podnaloga_post():
    global problem
    global part_num
    ##problem_part = problem.parts[part_num]
    problem_part = problem.parts[0]
    tests = problem_part.tests
    
    opis = request.forms.opis
    koda = request.forms.koda
    prekoda = request.forms.prekoda

    print("problem.parts")
    print(problem.parts)
    print("""problem.parts[part_num]""")
    print(problem.parts[part_num])
    print("""tests["check_equal"]""")
    print(tests["check_equal"])
    
    global active_test
    if request.forms.tipTesta == "chkeql":
        test_num = int(request.forms.stevilka)
        check_equal_test = CheckEqual(request.forms.niz, request.forms.rezultat)
        if test_num == len(tests["check_equal"]):
            tests["check_equal"].append([check_equal_test])
        elif test_num > len(tests["check_equal"]):
            return HTTPResponse("Uspelo ti ni!") 
        else:
            tests["check_equal"][test_num - 1].append(check_equal_test)
        active_test = "chkeql"
        
    elif request.forms.tipTesta == "chksct":
        test_num = int(request.forms.stevilka)
        check_secret_test = CheckSecret(request.forms.niz1, request.forms.niz2)
        if test_num == len(tests["check_secret"]):
            tests["check_secret"].append([check_secret_test])
        elif test_num > len(tests["check_secret"]):
            return HTTPResponse("Uspelo ti ni!")
        else:
            tests["check_secret"][test_num - 1].append(check_secret_test)
            
        active_test = "chksct"
    else:
        tests["other"] += zamenjaj(request.forms.other)
        active_test = "other"
    redirect("/index/podnaloga/")



@get("/index/podnaloga/testi/")
def podnaloga_testi():
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
        sklop[-1][3][2][0] += zamenjaj(request.forms.other)
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
