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
        self.description = description.strip()
        self.precode = precode.strip() # če uporabnik v okno na vmesniku za prekodo ne napiše ničesar ali napiše le presledek,
        # verejtno ne želimo, da se na datoteko izpišejo črtkane črte in pod njimi prazen prostor (ker je prekoda le presledek) ?
        self.solution = solution.strip()
        if isinstance(tests, str):
            tests = ProblemPart.parse_tests(tests)
            
        self.tests = tests
        ## {"check_equal":[[...],[...],...], "other": "STRING OF OTHER TESTS"}


    def __repr__(self):
        lines = []
        lines.append("# "+"="*69+"@{0:06d}=\n".format(self.part_id))                        # beginning of part header
        lines.append("# "+self.description.replace("\n", "\n# ")+"\n")                      # description
        if len(self.precode)>0: lines.append("# "+"-"*77+"\n")                              # optional beginning of template (preverimo ali je prekoda le prazen prostor)
        if len(self.precode)>0: lines.append("# "+self.precode.replace("\n", "\n# ")+"\n")  # precode (solution tamplate) (preverimo ali je prekoda le prazen prostor)
        lines.append("# "+"="*77+"\n")                                                      # boarder between description and precode
        lines.append(self.solution+"\n\n")                                                  # solution

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
    def parse_tests(validation):
        ## TODO add meta data (for now we have double list for and conection, maybe use dict?)
        def classify_tests(validation):
            def classify_check_equal(check_equal_string):
                ## TODO maybe use: from ast import literal_eval
                ## evaluates the right part of touple wich for now is OK?
                ## posible problem: ("15", [0, 15, 2][1])
                ## as it can not evaluate such complex expresions
                ## but this is ok: ("(12, [3, 5])", (12, [3, 5]))

                check_equal_string=check_equal_string.strip().strip("Check.equal(").strip()

                quotation_mark_type_expression=check_equal_string[0] # preverim s kakšnim znakom je obdan niz - lahko je ' ali ''' ali " ali """, če so narekovaji trojni je to potrebno ugotoviti
                triple_quotation_mark_expression=check_equal_string[0]==check_equal_string[1] #preverjanje ali so narekovaji trojni (ali sta prvi in drugi znak enaka)
                
                if triple_quotation_mark_expression==False: # nimamo trojnih narekovajev
                    expression=re.match(r"({0}(.*?)[^{0}]{0})[^{0}]".format(quotation_mark_type_expression), check_equal_string).group(1)
                    
                else:
                    expression=re.match(r"{0}{0}{0}(.*?){0}{0}{0}".format(quotation_mark_type_expression), check_equal_string).group(0)
                    
                result=check_equal_string[len(expression)+1:].strip().strip(",")[:-1].strip()
 
                return expression, result     
                
            lines = validation.split("\n")
            

            def check_parentheses(line):
                counter=0
                for char in line:
                    if char=="(": counter+=1
                    elif char==")": counter-=1 
                if counter==0: return True
                else: return False

            def make_one_line_tuples(lines):
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
                        lines2.append(line.rstrip())
                        
                    elif inside_tuple: # če sem znotraj tupla, dodam trenutno vrstico na pomožne in preverim, če se tuple v tej vrstici zakluči
                        lines_inside_tuple.append(line)
                        
                        if not check_parentheses(line): # če se število oklepajev in zaklepajev v tej vrstici ne ujema, se je tuple zaključil
                            inside_tuple=False
                            lines2.append(" ".join(lines_inside_tuple))
                            lines_inside_tuple=[]
                        
                return lines2
            
            def make_tuples_for_and_connected(lines):
                # združi Check.equal('zmnozi((2, 88), 2)', 4) and \
                # Check.equal('zmnozi(3, 3)', 9) v en enovrstični tuple 
                lines2=[]
                lines_inside_and_connection=[]
                inside_and=False
                for line in lines:
                    line=line.rstrip().rstrip("\\").rstrip()
                    if inside_and==False and line.endswith("and"):
                        inside_and=True
                        lines_inside_and_connection.append("( "+line)
                    elif inside_and==True and line.endswith("and"):
                        lines_inside_and_connection.append(line)
                    elif inside_and==True and not line.endswith("and"):
                        lines_inside_and_connection.append(line+ " )")
                        inside_and=False
                        lines2.append(" ".join(lines_inside_and_connection))
                        lines_inside_and_connection=[]
                    else:
                        lines2.append(line)
                return lines2
                    
            other_lines = []
            check_equals = []

            # for i in make_tuples_for_and_connected(make_one_line_tuples(lines)): print(i)
            
            for line in make_tuples_for_and_connected(make_one_line_tuples(lines)):
                if line.startswith("Check.equal"):
                    expression, result = classify_check_equal(line.strip())
                        
                    check_equals.append([CheckEqual(expression,  result)])
                    
                elif line.startswith("("):
                    
                    line=line[1:-1].strip()
                    # če je sedaj line oblike: "Check.equal('zmnozi(9, 9)', 25 ), Check.equal('zmnozi(88, 18)', 100)"
                    # stvar ne dela ok, ampak to je itak napačen zapis in nima veze
                    
                    list_of_check_equals=line.split("and") # preverimo, če je v vrstici več check.equal stavkov povezanih z and
                    check_equals_connected_with_and=[]
                    
                    for check_equal_string in list_of_check_equals:
                        expression, result = classify_check_equal(check_equal_string)
                        check_equals_connected_with_and.append(CheckEqual(expression,  result))
                        
                    check_equals.append(check_equals_connected_with_and)
                
                else:
                    if line!="": other_lines.append(line)

            return check_equals, other_lines

        check_equals, other_lines = classify_tests(validation)
        tests = {"check_equal" : check_equals, "other": "\n".join(other_lines)}

        return tests
        

    @staticmethod
    def parse(problem_part_string):
        def strip_hashes(description):
            if description is None:
                return ''
            else:
                lines = description.strip().splitlines()
                return "\n".join(line[line.index('#')+2:] for line in lines)

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
        tests = ProblemPart.parse_tests(validation)

        print("\nTESTI: ", tests)
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
    file_name="podnaloga"
    with open(file_name + "_in.py", "r", encoding="utf-8") as f:
        problem_part_string = f.read()
    
    def instructions_string(problem_part_string):
        return problem_part_string.split("Check.part()")[0].strip()
    
    problem_part = parse_test(problem_part_string)
    # print(str(problem_part))
    assert instructions_string(problem_part_string) == instructions_string(str(problem_part))
    
    napisi_na_dat(file_name+"_out.py", problem_part_string)

