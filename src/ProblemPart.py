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
        lines.append(("# "+self.precode.replace("\n", "\n# ")+"\n"))        # precode (solution tamplate)
        lines.append("# "+"="*77+"\n")                                      # boarder between description and precode # tega ni ?
        lines.append(self.solution+"\n\n")                                  # solution

        ## TODO remove this in future
        if self.tests is None:
            return "".join(lines)
        
        lines.append("Check.part()\n")                                      # beginning of validation

        for test_equal in self.tests["check_equal"]:
            lines.append(str(test_equal) + "\n")

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
            def classify_check_equal(line):
                data = line.strip("Check.equal(")

                ## TODO maybe use: from ast import literal_eval
                ## evaluates the right part of touple wich for now is OK?
                ## posible problem: ("15", [0, 15, 2][1])
                ## as it can not evaluate such complex expresions
                ## but this is ok: ("(12, [3, 5])", (12, [3, 5]))
                counter = 1
                element_chars = []
                touple_elements = []
                for z in data:
                    if z == "(":
                        counter += 1
                        
                    elif z == ")":
                        counter -= 1
                        if counter == 0:
                            touple_elements.append("".join(element_chars))
                            break
                            
                    elif z == "," and counter == 1:
                        touple_elements.append("".join(element_chars))
                        element_chars = []

                    element_chars.append(z)

                return touple_elements
                        
                
            lines = validation.split("\n")
            other_lines = []
            check_equals = []

            for line in lines:
                if line.startswith("Check.equal"):
                    x, y = classify_check_equal(line)
                    check_equals.append(CheckEqual(x,y))
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

        tests = {"check_equal" : check_equals, "other": "\n".join(other_lines)}

        # TODO validation (check part), problem_id

        return ProblemPart(part_id, description, precode, solution, tests)

    

    def write_on_file(self, file):
        with open(file, "w", encoding="utf-8") as f:
            f.write(str(self))













def parse_test(problem_part_string):
    problem_part = ProblemPart.parse(problem_part_string)

    print("ID podnaloge:","problem_part.part_id")
    print(problem_part.part_id)
    print()
    print("Navodila podnaloge:","problem_part.description")
    print(problem_part.description)
    print()
    print("Prekoda naloge:","problem_part.precode")
    print(problem_part.precode)
    print()
    print("Rešitev naloge:","problem_part.solution")
    print(problem_part.solution)
    print()
    # TODO:
    print("Za teste moramo še določiti strukturo:")
    print("problem_part.tests", problem_part.tests)
    print()

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
"Enterobacteria phage lambda"

Check.part()
resitev = eval(Check.current_part['solution'])
if not isinstance(resitev, str):
    Check.error('Rešitev mora biti niz. Nizi se pisejo takole "TUKAJ JE BESEDILO"')

if "Enterobacteria phage lambda" not in resitev:
    Check.error('Napisati morate pravilen niz. Namig resitev je: "Enterobacteria phage lambda"')

"""
    def instructions_string(problem_part_string):
        return problem_part_string.split("Check.part()")[0].strip()
    
    problem_part = parse_test(problem_part_string)
    print(str(problem_part))
    assert instructions_string(problem_part_string) == instructions_string(str(problem_part))
    
    napisi_na_dat("podnaloga.py", problem_part_string)
