from bottle import *
import webbrowser
from Problem import Problem
from ProblemPart import ProblemPart, CheckEqual, CheckSecret



class WebGUI:
    def __init__(self):
        self.static_directory = "./static"  
        file_name = "../edit_files/naloga" + "_in.py"
        self.problem = Problem.load_file(file_name)
        self.active_test="chkeql"
        self.part_num = 0

        webbrowser.open('http://localhost:8080/index/')
        
##        for _ in range(len(self.problem.parts)):
##            print("self.part_num bajbdbdb")
##            print(self.part_num)
##            self.part_num += 1
##            webbrowser.open('http://localhost:8080/index/podnaloga/')
        
    @route("/static/<filename:path>") 
    def static(self, filename):
        return static_file(filename, root=static_directory)

    @get("/")
    def blank(self):
        redirect('/index/')

    @get("/index/")
    def index(self):
        adress = self.problem.title
        description = self.problem.description
        
        return template("index.html", napaka=None, adress=adress, description=description, code="")

    @post("/index/")
    def index_post(self): 
        naslov = request.forms.naslov
        opis = request.forms.opis
        if naslov:
            sklop.append([naslov, opis])
            return template("index.html", napaka=None, adress=naslov, description=opis)

    @get("/index/podnaloga/")
    def podnaloga(self):
        print("werg7gr83grgr3rg37gg38")
        self.active_test = "chkeql"
        
        problem_part = self.problem.parts[self.part_num-1]
        print("self.part_num")
        print(self.part_num)
        print("problem_part")
        print(problem_part)
        
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
    def podnaloga_post(self):
       
        problem_part = problem.parts[self.part_num]
        ##problem_part = self.problem.parts[0]
        tests = problem_part.tests
        
        opis = request.forms.opis
        koda = request.forms.koda
        prekoda = request.forms.prekoda

        print("problem.parts")
        print(self.problem.parts)
        print("""problem.parts[part_num]""")
        print(self.problem.parts[part_num])
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
    def podnaloga_testi(self):
        return template("podnaloga.html", description=sklop[-1][0], precode=sklop[-1][1],
                        code=sklop[-1][2], napaka=None, rows=sklop[-1][3], testi=True, active_test=active_test, title="Podnaloga")

    @post("/index/podnaloga/testi/")
    def podnaloga_testi_post(self):
        "Če test nima določenega atributa vrne None namest praznega niza"
        
        if request.forms.tipTesta == "chkeql":
            sklop[-1][3][0].append([request.forms.stevilka, request.forms.niz, request.forms.rezultat])
            self.active_test = "chkeql"
        elif request.forms.tipTesta == "chksct":
            sklop[-1][3][1].append([request.forms.stevilka, request.forms.niz1, request.forms.niz2])
            self.active_test = "chksct"
        else:
            sklop[-1][3][2][0] += zamenjaj(request.forms.other)
            self.active_test = "other"
        redirect("/index/podnaloga/testi/")

    @get("/pretvori/")
    def pretvori(self):
        "Tukej se bo zej v ozadju poklicalo in vsi bomo srecni"
        for array in sklop:
            print(array)
        return HTTPResponse("Uspelo ti je!")

    def zamenjaj(self, string):
        chars = list(string)
        for i in range(0, len(chars)):
            if chars[i] == "\n":
                chars[i] = "<br>"
            if chars[i] == " ":
                chars[i] = "&nbsp"
            if chars[i] == "\r":
                chars[i] = ""
        return "".join(chars)

def routeapp(app):
    for kw in dir(app):
        attr = getattr(app, kw)
        if hasattr(attr, 'route'):
            bottle.route(attr.route)(attr)

app = WebGUI()
bottle.route("/1")(app.index)
