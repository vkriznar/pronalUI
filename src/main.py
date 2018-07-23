from bottle import *
import webbrowser
from Problem import Problem
from ProblemPart import ProblemPart, CheckEqual, CheckSecret
import time
import re

static_directory = "./static"
active_test = "chkeql"
testi = False
je_bila_izbrisana = False
podnaloge_za_osvezit = []

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
    print(file)
    # only allow upload of text files
    # if file.content_type != "text/plain":
    #    return HTTPResponse("Uspelo ti ni!")
    file_name = file.filename
    print(file_name)
    
    "Z file.file dostopamo do nase datoteke, npr."
##    for line in file.file:
##        "moramo dekodirati, ker je zapisana v bitih"
##        # print(line.decode().rstrip('\n'))
    "redirect na obstojeco, ki je zaenkrat tako, da ne uposteva uploadanga fila, ker je treba spremeniti Problem.py"
    return redirect("/index/obstojeca")

@get("/index/")
def index():
    return template("index.html")

## tole spodi ni ok !!
"Zacetna stran kjer uporabnik izbire, ali bo ustvaril novo datoteko ali bo vnesel ze obstojeco datoteko za urejanje"
@get("/index/<izbira>")
def nova_naloga(izbira):
    global problem
    global file_name
    if izbira == "nova":
        
        #tukaj se ustvari nov Problem ki ima prazne atribute
        redirect("/index/naloga/")
    elif izbira == "obstojeca":
        file_name = "../edit_files/"+file_name
        problem = Problem.load_file(file_name)
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


@get("/index/naloga/podnaloga_izbrisi<part_num>/")
def podnaloga_izbrisi(part_num):
    global problem
    global je_bila_izbrisana
    global naloge_za_osvezit
    global podnaloge_za_osvezit
    part_num = int(part_num)
    del problem.parts[part_num-1]
    je_bila_izbrisana = True
    podnaloge_za_osvezit = [i for i in range(part_num+1, len(problem.parts)+2)]

    return HTTPResponse("Uspelo ti je izbrisati nalogo {0}!".format(part_num))


@get("/index/naloga/podnaloga<part_num>/")
def podnaloga(part_num):
    global problem
    part_num = int(part_num)
    global active_test
    global je_bila_izbrisana
    global podnaloge_za_osvezit
    active_test = "chkeql"

    if part_num > len(problem.parts):
        problem_part = problem.parts[part_num - 2]
    else:
        problem_part = problem.parts[part_num-1]
    
    description = problem_part.description
    solution = problem_part.solution
    precode = problem_part.precode
    tests = problem_part.tests

    if je_bila_izbrisana:
        if part_num in podnaloge_za_osvezit:
            podnaloge_za_osvezit.remove(part_num)
            if not podnaloge_za_osvezit:
                je_bila_izbrisana = False
            redirect("/index/naloga/podnaloga{}/".format(part_num-1))

    return template("podnaloga.html", napaka=None,
                    description=description, code=solution,
                    precode=precode, tests=tests, testi=testi,
                    active_test=active_test, changes=None, title="Podnaloga {}".format(part_num), part_num=part_num)







##@get("/index/naloga/podnaloga<part_num>/prekoda/")
##def podnaloga(part_num):
##    global problem
##    part_num = int(part_num)
##    global active_test
##    active_test = "chkeql"
##
##    problem_part = problem.parts[part_num-1]
##    
##    description = problem_part.description
##    solution = problem_part.solution
##    precode = problem_part.precode
##    tests = problem_part.test
##    
##    redirect("/index/naloga/podnaloga{}/".format(part_num))

@get("/index/naloga/podnaloga<part_num>/<test_type>-<edit><group_id><i>/")
def delete_from_table(part_num, test_type, edit, group_id, i):
    part_num = int(part_num)
    group_id = int(group_id)
    i = int(i)

    global problem
    problem_part = problem.parts[part_num-1]
    tests = problem_part.tests
    
    if test_type == "chkeql":
        test = tests["check_equal"][group_id][i]
    elif test_type == "chksct":
        test = tests["check_secret"][group_id][i]
        
    if edit == "delete":
        problem_part.remove_test(test)
    elif edit == "move":
        problem_part.description += "\n\n    >>> " + test.expression + "\n    " + test.output
    
    testi = True
    redirect("/index/naloga/podnaloga{}/".format(part_num))


@get("/index/naloga/podnaloga/")
def podnaloga_get_def():
    global problem
    part_num = len(problem.parts)
    problem.new_problem_part()
    redirect("/index/naloga/podnaloga{}/".format(part_num +1 ))

@post("/index/naloga/podnaloga<part_num>/")
def podnaloga_post(part_num):
    global problem
    global testi
    changes = []
    testi = False
    part_num = int(part_num)
    problem_part = problem.parts[part_num-1]
    tests = problem_part.tests

    if request.forms.opis:
        problem_part.description = request.forms.opis
        problem_part.solution = request.forms.koda
        problem_part.precode = request.forms.prekoda

    if request.forms.prekoda_gor:
        problem_part.precode_to_description()


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

            
            
            if test_num == len(tests["check_secret"]):
                tests["check_secret"].append([check_secret_test])
            elif test_num > len(tests["check_secret"]):
                return HTTPResponse("Uspelo ti ni!")
            else:
                tests["check_secret"][test_num].append(check_secret_test)

            active_test = "chksct"
        else:
            tests["other"] += (request.forms.other)


    if request.forms.changes:
        print(request.forms.changes)
        array = re.split(r',\s*(?![^()]*\))', request.forms.changes)
        print(array)

        
        
        for i in range (0, len(array)//4):
            changes.append([array[0+i*4], int(array[1+i*4])-1, int(array[2+i*4]), array[3+i*4]])
            print(array[0+i*4])
            print(int(array[1+i*4])-1)
            print(int(array[2+i*4])-1)
            print(array[3+i*4])
            
            print(changes)
            
        testi = True

    redirect("/index/naloga/podnaloga{}/".format(part_num))


@get("/pretvori/")
def pretvori():
    problem.write_on_file(file_name[:-6] + "_out.py")
    print(problem)
    return HTTPResponse("Uspelo ti je!")



run(host='localhost', port=8080, debug=True)
