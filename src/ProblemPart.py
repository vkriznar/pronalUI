import re


class CheckEqual:
    def __init__(self, expression, result):
        self.expression = expression
        self.result = result

    def __repr__(self):
        return "Check.equal({0}, {1})".format(self.expression, self.result)
        
    
    
class ProblemPart:
    def __init__(self, part_id, description, precode, solution, tests):
        self.part_id = part_id
        self.description = description
        self.precode = precode
        self.solution = solution
        self.tests = tests
        ## {"check_equal":[...], "other": "STRING OF OTHER TESTS"}


    def __repr__(self):
        lines = []
        lines.append("# "+"="*69+"@{0:06d}=\n".format(self.part_id))        # beginning of part header
        lines.append("# "+self.description.replace("\n", "\n# ")+"\n")      # description
        lines.append("# "+"-"*77+"\n")                                      # optional beginning of template 
        lines.append("# "+self.precode.replace("\n", "\n# ")+"\n")          # precode (solution tamplate)
        lines.append("# "+"="*77+"\n")                                      # boarder between description and precode
        lines.append(self.solution+"\n\n")                                  # solution

        ## TODO remove this in future
        if self.tests is None:
            return "".join(lines)
        
        lines.append("Check.part()\n")                                      # beginning of validation

        for test_equal_connected_with_and in self.tests["check_equal"]:
            for test_equal in test_equal_connected_with_and:
                if test_equal_connected_with_and.index(test_equal)==len(test_equal_connected_with_and)-1:
                    lines.append(str(test_equal) + "\n")
                else:
                    lines.append(str(test_equal) + " and \\ \n")

        lines.append(self.tests["other"])

        return "".join(lines)

    @staticmethod
    def parse(problem_part_string):
        def strip_hashes(description):
            if description is None:
                return ''
            else:
                lines = description.strip().splitlines()
                return "\n".join(line[line.index('#')+2:] for line in lines)

        ## TODO add meta data
        def classify_tests(validation):
            def classify_check_equal(check_equal_string):
                ## TODO maybe use: from ast import literal_eval
                ## evaluates the right part of touple wich for now is OK?
                ## posible problem: ("15", [0, 15, 2][1])
                ## as it can not evaluate such complex expresions
                ## but this is ok: ("(12, [3, 5])", (12, [3, 5]))

                check_equal_string=check_equal_string.strip().strip("Check.equal(").strip()

                # expression=re.search(r"'['|\"|\"""]\w+(\(([^\(\)]*,)*([^\(\)])*\))*['|\"|\"""]", check_equal_string).group(0)
                quotation_mark_type=check_equal_string[0]
                expression=re.search(r"{0}([^{0}])+{0}".format(quotation_mark_type), check_equal_string).group(0)
                result=check_equal_string[len(expression)+1:].strip().strip(",").strip(")").strip()
        
                return expression, result     
                
            lines = validation.split("\n")
            other_lines = []
            check_equals = []
            search_equal=False

            def check_parentheses(line):
                stevec=0
                for char in line:
                    if char=="(": stevec+=1
                    elif char==")": stevec-=1 
                if stevec==0: return True
                else: return False

            def reshape_lines(lines):
                """
                funkcija, ki vse dele testov, ki so zapisni v več vrstičnih tuplih, zapiše v enovrstične tuple
                """
                lines2=[]
                lines_inside_tuple=[]
                inside_tuple=False
                
                for line in lines:
                    if line.startswith("("):
                        if not check_parentheses(line): # če se število oklepajev in zaklepajev v tej vrstici ne ujema, nadaljujem v naslednji vrstici
                            inside_tuple=True
                            lines_inside_tuple.append(line.strip())
                            continue
                        else:
                            inside_tuple=False # če se tuple zaključi v isti vrstici, se delam kot da nisem v tuplu in vrstico na koncu le dodam na lines2
                    
                    if not inside_tuple: # če nisem znotraj tupla samo dodam line na iine2
                        lines2.append(line)
                        
                    elif inside_tuple: # če sem znotraj tupla, dodam trenutno vrstico na pomožne in preverim, če se tuple v tej vrstici zakluči
                        lines_inside_tuple.append(line.strip())
                        
                        if not check_parentheses(line): # če se število oklepajev in zaklepajev v tej vrstici ne ujema, se je tuple zaključil
                            inside_tuple=False
                            lines2.append(" ".join(lines_inside_tuple))
                            lines_inside_tuple=[]
                        
                return lines2

                
            for line in reshape_lines(lines):
                if line.startswith("Check.equal"):
                    # line lahko predstavlja le en Check.equal stavek npr.: "Check.equal('zmnozi(7, 7)', 49)\n"
                    # lahko pa jih je več povezanih z and npr.: "Check.equal('zmnozi(7, 7)', 49) and Check.equal('zmnozi(5, 4)', 20)\n"
                    
                    list_of_check_equals=line.split("and") # preverimo, če je v vrstici več check.equal stavkov povezanih z and
                    check_equals_connected_with_and=[]
                    
                    for check_equal_string in list_of_check_equals:
                        expression, result = classify_check_equal(check_equal_string)
                        check_equals_connected_with_and.append(CheckEqual(expression,  result))
                        
                    check_equals.append(check_equals_connected_with_and)
                    
                elif line.startswith("("):
                    print("line: ", line)
                    print()
                    line=line[1:-1].strip()
                    print(line)
                    print()
                    # če je sedaj line oblike: "Check.equal('zmnozi(9, 9)', 25 ), Check.equal('zmnozi(88, 18)', 100)" stvar ne dela ok
                    
                    list_of_check_equals=line.split("and") # preverimo, če je v vrstici več check.equal stavkov povezanih z and
                    check_equals_connected_with_and=[]
                    
                    for check_equal_string in list_of_check_equals:
                        expression, result = classify_check_equal(check_equal_string)
                        check_equals_connected_with_and.append(CheckEqual(expression,  result))
                        
                    check_equals.append(check_equals_connected_with_and)
                
                else:
                    other_lines.append(line)

            return check_equals, other_lines

        match = re.search(
            r'# ===+@(?P<part>\d+)=\s*\n'             # beginning of part header
            r'(?P<description>(\s*#( [^\n]*)?\n)+?)'  # description
            r'(\s*# ---+\s*\n'                        # optional beginning of template
            r'(?P<template>(\s*#( [^\n]*)?\n)*))?'    # solution template
            r'\s*# ===+\s*?\n'                        # end of part header
            r'(?P<solution>.*?)'                      # solution
            r'^Check\s*\.\s*part\s*\(\s*\)\s*?(?=\n)' # beginning of validation
            r'(?P<validation>.*?)'                    # validation
            r'\n -><-',
            problem_part_string + "\n -><-",
            flags=re.DOTALL | re.MULTILINE
        )
        part_id = int(match.group('part'))
        description = strip_hashes(match.group('description'))
        precode = strip_hashes(match.group('template'))
        solution = match.group('solution').strip()
        validation = match.group('validation').strip()
        check_equals, other_lines = classify_tests(validation)

        print("\nCHECK_EQUALS: ", check_equals)
        print("\nOTHER_LINES: ", other_lines)

        tests = {"check_equal" : check_equals, "other": "\n".join(other_lines)}

        # TODO validation (check part), problem_id
        return ProblemPart(part_id, description, precode, solution, tests)

    

    def write_on_file(self, file):
        with open(file, "w", encoding="utf-8") as f:
            f.write(str(self))













def parse_test(problem_part_string):
    problem_part = ProblemPart.parse(problem_part_string)

    # print("ID podnaloge:","problem_part.part_id")
    # print(problem_part.part_id)
    # print()
    # print("Navodila podnaloge:","problem_part.description")
    # print(problem_part.description)
    # print()
    # print("Prekoda naloge:","problem_part.precode")
    # print(problem_part.precode)
    # print()
    # print("Rešitev naloge:","problem_part.solution")
    # print(problem_part.solution)
    # print()
    # TODO:
    # print("Za teste moramo še določiti strukturo:")
    # print("problem_part.tests", problem_part.tests)
    # print()

    return problem_part


def napisi_na_dat(file_name, problem_part_string):
    problem_part = ProblemPart.parse(problem_part_string)
    problem_part.write_on_file(file_name)

    

if __name__ == "__main__":
    problem_part_string = """

# =====================================================================@015027=
# Na spletni strani `https://www.ncbi.nlm.nih.gov/guide/howto/dwn-genome/`
# poišči genski zapis z oznako KT232076.1 in v obliki niza povej za
# katero vrsto bakterije gre.
# 
#     # Resitev bo oblike:
#     "Enterobacteria *** lambda"
#     # kjer tri zvezdice zamenjaj za ustrezno ime.
# -----------------------------------------------------------------------------
# # Resitev bo oblike:
# "Enterobacteria *** lambda"
# # kjer tri zvezdice zamenjaj za ustrezno ime.
# =============================================================================
def zmnozi(x, y):
    return x*y
Spremenljivka="Nek string, ki je enak spremenljivki"

(( CE and CE) and ( CE and CE))

Check.part()
Check.equal('zmnozi((2, 88), 2)', 4) and \
Check.equal('zmnozi(3, 3)', 9)
Check.equal('zmnozi(4, 4)', 16, clean=clean, env=env)
Check.equal('zmnozi(5, 5)', 25 ) and \
Check.equal('zmnozi("10", "10")', 100) and \
Check.equal("zmnozi(20, 20)", 400) and \
Check.equal("zmnozi('20', 20)", 400) and \
Check.equal('x', 50 // 6)

(   Check.equal('odstej(8, 8)', 25 ) and 
    Check.equal('odstej(88, 18)', 100) and 
    Check.equal("odstej(20, 20)", 400)
)

(
    Check.equal('sestej(81, 81)', 25 ) and 
    Check.equal('sestej(88, 18)', 100) and 
    Check.equal("sestej(20, 20)", 400)
)



Check.equal('Spremenljivka', "Nek string, ki je enak spremenljivki")
Check.secret(zmnozi(100, 100))
Check.secret(zmnozi(500, 123))

resitev = eval(Check.current_part['solution'])
if not isinstance(resitev, str):
    Check.error('Rešitev mora biti niz. Nizi se pisejo takole "TUKAJ JE BESEDILO"')

if "Enterobacteria phage lambda" not in resitev:
    Check.error('Napisati morate pravilen niz. Namig resitev je: "Enterobacteria phage lambda"')

"""
    
    def instructions_string(problem_part_string):
        return problem_part_string.split("Check.part()")[0].strip()
    
    problem_part = parse_test(problem_part_string)
    # print(str(problem_part))
    assert instructions_string(problem_part_string) == instructions_string(str(problem_part))
    
    napisi_na_dat("podnaloga.py", problem_part_string)

