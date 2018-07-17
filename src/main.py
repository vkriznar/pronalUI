from bottle import *
import webbrowser
from Problem import Problem
from ProblemPart import ProblemPart, CheckEqual, CheckSecret
import time

static_directory = "./static"
active_test = "chkeql"
file_name = "../edit_files/naloga"
problem = Problem.load_file(file_name + "_in.py")



webbrowser.open('http://localhost:8080/index/')
for i in range(len(problem.parts)):
    time.sleep(0.05)
    webbrowser.open('http://localhost:8080/index/podnaloga{}/'.format(i+1))
    
@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_directory)

@get("/")
def blank():
    redirect('/index/')

@get("/index/")
def index():
    global problem
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

@get("/index/podnaloga<part_num>/")
def podnaloga(part_num):
    global problem
    part_num = int(part_num)
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
                    active_test=active_test, title="Podnaloga {}".format(part_num))


@get("/index/podnaloga/")
def podnaloga_post_def():
    global problem
    part_num = len(problem.parts)
    problem.new_problem_part()
    redirect("/index/podnaloga{}/".format(part_num + 1))

@post("/index/podnaloga<part_num>/")
def podnaloga_post(part_num):
    global problem
    
    part_num = int(part_num)
    print("ej")
    problem_part = problem.parts[part_num-1]
    tests = problem_part.tests
    
    opis = request.forms.opis
    koda = request.forms.koda
    prekoda = request.forms.prekoda
    
    global active_test
    if request.forms.tipTesta == "chkeql":
        print("type(request.forms.stevilka)")
        print(type(request.forms.stevilka))
        print(request.forms.stevilka)
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
        tests["other"] += zamenjaj(request.forms.other)
        active_test = "other"
    redirect("/index/podnaloga{}/".format(part_num))


@get("/pretvori/")
def pretvori():
    #"Tukej se bo zej v ozadju poklicalo in vsi bomo srecni"
    problem.write_on_file(file_name + "_out.py")
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
