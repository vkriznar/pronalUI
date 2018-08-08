from bottle import *
import webbrowser
from Problem import Problem
from ProblemPart import ProblemPart, CheckEqual, CheckSecret
import time
import re
import json
import bottle

static_directory = "./static"
active_test = "chkeql"
testi = False
je_bila_izbrisana = False
podnaloge_za_osvezit = []
preostevilcenje = []
trenutno_osvezena = None

app = bottle.default_app()
BaseTemplate.defaults['get_url'] = app.get_url

# webbrowser.open('http://localhost:8080/index/')
webbrowser.open('http://localhost:8080/')

@route('/')
def index():
    return template('index')

@route('/static/<filename:path>', name='static')
def serve_static(filename):
    return static_file(filename, root=static_directory)
    
##@route("/static/<filename:path>")
##def static(filename):
##    return static_file(filename, root=static_directory)

##@get("/")
##def blank():
##    redirect('/index/')

@post('/upload')
def upload():
    global file_name
    global file
    file = request.files.get('file')
    file_name = file.filename
    print(os.path.splitext(file_name))

    "Z file.file dostopamo do nase datoteke, npr."
##    #for line in file.file:
##        "moramo dekodirati, ker je zapisana v bitih"
##        #print(line.decode().rstrip('\n'))
##        #print(type(line.decode().rstrip('\n')))
##        #print(len(line.decode().rstrip('\n')))
##        #print(type(line.decode().rstrip('\n')))
##        #print(str(line.decode().rstrip('\n')))
    "redirect na obstojeco, ki je zaenkrat tako, da ne uposteva uploadanga fila, ker je treba spremeniti Problem.py"
    return redirect("/index/obstojeca")

@get('/preostevilci<part_num><num>')
def preostevilci(part_num, num):
    global preostevilcenje
    part_num = int(part_num)
    preostevilcenje.append({part_num, int(num)})
    print(preostevilcenje)
    """global podnaloge_za_osvezit
    part_num = int(part_num)
    num = int(num)
    prvic = True
    print(podnaloge_za_osvezit)
    if part_num > num:
        if part_num in podnaloge_za_osvezit:
            podnaloge_za_osvezit.remove(part_num)
        for i in range(num+1, part_num):
            if i in podnaloge_za_osvezit:
                podnaloge_za_osvezit.remove(i)
            else:
                podnaloge_za_osvezit.append(-i)
    else:
        if num in podnaloge_za_osvezit:
            return HTTPResponse("Uspelo ti ni!")
        if num in podnaloge_za_osvezit:
            podnaloge_za_osvezit.remove(num)
            podnaloge_za_osvezit.append(str(num))
        for j in range(part_num+1, num+1):
            if j in podnaloge_za_osvezit:
                if prvic:
                    podnaloge_za_osvezit.remove(j-1)
                    prvic = False
                podnaloge_za_osvezit.remove(j)
                podnaloge_za_osvezit.append(str(j))
            else:
                if not prvic:
                    podnaloge_za_osvezit.append(str(j))
                else:
                    podnaloge_za_osvezit.append(j)
    print(podnaloge_za_osvezit)"""
    redirect("/index/naloga/podnaloga{}/".format(part_num))



@get("/index/")
def index():
    return template("index.html")

## tole spodi ni ok !!
"Zacetna stran kjer uporabnik izbire, ali bo ustvaril novo datoteko ali bo vnesel ze obstojeco datoteko za urejanje"
@get("/index/<izbira>")
def nova_naloga(izbira):
    global problem
    #global file_name # tega zdj ne rabimo več
    global file
    if izbira == "nova":
        
        #tukaj se ustvari nov Problem ki ima prazne atribute
        redirect("/index/naloga/")
    elif izbira == "obstojeca":

        #old version
        #file_name = "../edit_files/"+file_name
        #problem = Problem.load_file(file_name)
        
        problem = Problem.read_filefile(file.file)
        
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
    # je_bila_izbrisana = True
    podnaloge_za_osvezit = [i for i in range(part_num+1, len(problem.parts)+2)]

    return HTTPResponse("Uspelo ti je izbrisati nalogo {0}!".format(part_num))


@get("/index/naloga/podnaloga<part_num>/")
def podnaloga(part_num):
    global problem
    part_num = int(part_num)
    global active_test
    global trenutno_osvezena
    global podnaloge_za_osvezit
    active_test = "chkeql"

        
    if part_num > len(problem.parts):
        # problem_part = problem.parts[part_num - 2] # napaka
        problem_part = problem.parts[-1]
        # part_num = 1
    else:
        problem_part = problem.parts[part_num-1]
    
    description = problem_part.description
    solution = problem_part.solution
    precode = problem_part.precode
    tests = problem_part.tests
    # print(part_num, tests)

    if podnaloge_za_osvezit:
        if part_num in podnaloge_za_osvezit:
            if trenutno_osvezena != part_num:
                podnaloge_za_osvezit.remove(part_num)
                trenutno_osvezena = part_num-1
                redirect("/index/naloga/podnaloga{}/".format(part_num-1))
            else:
                trenutno_osvezena = None

        """if -part_num in podnaloge_za_osvezit:
            if trenutno_osvezena != part_num:
                podnaloge_za_osvezit.remove(-part_num)
                trenutno_osvezena = part_num+1
                redirect("/index/naloga/podnaloga{}/".format(part_num+1))
            else:
                trenutno_osvezena = None
        if str(part_num) in podnaloge_za_osvezit:
            if trenutno_osvezena != part_num:
                podnaloge_za_osvezit.remove(str(part_num))
                trenutno_osvezena = part_num-2
                redirect("/index/naloga/podnaloga{}/".format(part_num-2))
            else:
                trenutno_osvezena = None"""



    return template("podnaloga.html", napaka=None,
                    description=description, code=solution,
                    precode=precode, tests=tests, testi=testi,
                    active_test=active_test, changes=None, part_num=part_num)




@get("/index/naloga/podnaloga<part_num>/<test_type>-<edit><group_id><i>/")
def delete_from_table(part_num, test_type, edit, group_id, i):
    part_num = int(part_num)
    group_id = int(group_id)
    i = int(i)

    global problem
    global testi
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
    global preostevilcenje
    changes = []
    testi = False
    part_num = int(part_num)
    problem_part = problem.parts[part_num-1]
    tests = problem_part.tests

    if request.forms.opis:
        #print("OPIS vmesnik:", request.forms.opis)
        problem_part.description = request.forms.opis
        #print("OPIS description:", problem_part.description)
        problem_part.solution = request.forms.koda
        problem_part.precode = request.forms.prekoda
    if request.forms.prekoda_gor == "True":     #To ni isto kot boolean==True, ker je True string
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
        json_dict = json.loads(request.forms.changes)
        print(json_dict)

        for test_type in json_dict:
            for test_data in json_dict[test_type]:
                #print("spremembe: ", test_data)
                group_id = int(test_data["group_id"]) - 1
                i = int(test_data["index"]) - 1
                expression = test_data["expression"]
                output = test_data["output"] if test_type == "check_equal" else test_data["other"]
                problem_part.change_test_by_id(test_type, group_id, i, expression, output)
                #print("spremembe2: ", problem_part.tests[test_type][group_id][i])


    redirect("/index/naloga/podnaloga{}/".format(part_num)) # treba je returnat template, ki bo vrnu dano podnalogo s spremenjenimi testi



@get("/pretvori/")
def pretvori():
    global file_name
    file_name = "../edit_files/"+file_name
    problem.write_on_file(file_name[:-6] + "_out.py")
    #print(problem)
    return HTTPResponse("Uspelo ti je!")



run(host='localhost', port=8080, debug=True)
