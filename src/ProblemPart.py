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

        lines.append(tests["other"])

        return "".join(lines)

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
            r'(?P<validation>.*?)',                   # validation
            problem_part_string,
            flags=re.DOTALL | re.MULTILINE
        )
        part_id = int(match.group('part'))
        description = strip_hashes(match.group('description'))
        precode = strip_hashes(match.group('template'))
        solution = match.group('solution').strip()
        # TODO validation (check part), problem_id

        return ProblemPart(part_id, description, precode, solution, None)

    

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
    assert instructions_string(problem_part_string) == instructions_string(str(problem_part))
    
    napisi_na_dat("podnaloga.py", problem_part_string)
