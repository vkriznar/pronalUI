import re


class ProblemPart:
    def __init__(self, part_id, description, precode, solution, tests):
        self.part_id = part_id
        self.description = description
        self.precode = precode
        self.solution = solution
        self.tests = tests


    def __repr__(self):
        repr_string = ""
        # TODO 1 make part without validation
        # TODO 2 add validation

        return repr_string

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













def parse_test():
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

if __name__ == "__main__":
    problem_part = parse_test()
