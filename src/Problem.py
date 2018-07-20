import re
from ProblemPart import ProblemPart

def strip_hashes(description):
    if description is None:
        return ''
    else:
        lines = description.strip().splitlines()
        return "\n".join(line[line.index('#')+2:] for line in lines)

class Problem:
    def __init__(self, title, description, parts, lib_string, head_string):
        self.head_string = head_string # header lines at the beginning of file
        self.title = title.strip()
        self.description = description.strip()
        self.parts = parts
        self.lib_string = lib_string # template and library
        

    @staticmethod
    def parse(file_string):  
        split_index = file_string.find(
"""
# # =====================================================================@000000=
# # This is a template for a new problem part. To create a new part, uncomment
# # the template and fill in your content.
""")
        if split_index==-1: # if there is no english tempalate, then we try to find slovene template
            split_index = file_string.find(
"""
# # =====================================================================@000000=
# # To je predloga za novo podnalogo. Če želite ustvariti novo podnalogo,
# # pobrišite komentarje ter vsebino zamenjajte s svojo.
""")
        #print(split_index)
        # for regex to work we add first template line
        problem_string = file_string[:split_index + 100]
        lib_string = file_string[split_index:]
        #print(problem_string)
        #print(lib_string)
        problem_match = re.search(
            r'(?P<head>.*?)'                         # head of file
            r'^\s*# =+\s*\n'                         # beginning of header
            r'^\s*# (?P<title>[^\n]*)\n'             # title
            r'(?P<description>(^\s*#( [^\n]*)?\n)*)' # description
            r'(?=\s*(# )?# =+@)',                    # beginning of first part
            problem_string, flags=re.DOTALL | re.MULTILINE)

        part_regex = re.compile(
            r'# ===+@(?P<part>\d+)=\s*\n'             # beginning of part header
            r'(?P<description>(\s*#( [^\n]*)?\n)+?)'  # description
            r'(\s*# ---+\s*\n'                        # optional beginning of template
            r'(?P<template>(\s*#( [^\n]*)?\n)*))?'    # solution template
            r'\s*# ===+\s*?\n'                        # end of part header
            r'(?P<solution>.*?)'                      # solution
            r'^Check\s*\.\s*part\s*\(\s*\)\s*?(?=\n)' # beginning of validation
            r'(?P<validation>.*?)'                    # validation
            r'(?=\n\s*(# )?# =+@)',                   # beginning of next part
            flags=re.DOTALL | re.MULTILINE
        )

        parts = [(
            ProblemPart(
                int(match.group('part')),                   # part_id
                strip_hashes(match.group('description')),   # description
                strip_hashes(match.group('template')),      # precode
                match.group('solution').strip(),            # solution
                match.group('validation').strip())          # tests (string form)
        ) for match in part_regex.finditer(file_string)]
        
        #print(parts)
        head =problem_match.group('head').strip()
        title = problem_match.group('title').strip()
        description = strip_hashes(problem_match.group('description'))
        

        return Problem(title, description, parts, lib_string, head)

    def __repr__(self):
        blocks = []
        blocks.append(self.head_string)
        blocks.append("\n# "+ "=" * 77)
        blocks.append("# " + "\n# ".join(self.title.split("\n"))+ "\n#")
        blocks.append("# "+"\n# ".join(self.description.split("\n")))
        for part in self.parts:
            blocks.append(str(part))

        blocks.append(self.lib_string)

        return "\n".join(blocks)


    def write_on_file(self, file_name):
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(str(self))


    @staticmethod
    def load_file(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            file_string = f.read()

        return Problem.parse(file_string)


    def new_problem_part(self):
        self.parts.append(ProblemPart.load_file("parameters/default_part.py"))
        return self.parts[-1]


    def remove_problem_part(self, problem_part):
        if problem_part in self.parts:
            self.parts.remove(problem_part)
        else:
            print("[ERROR] in remove_problem_part.")
        
        


if __name__ == "__main__":
    file_name =   "../edit_files/naloga"
    problem = Problem.load_file(file_name + "_in.py")
    test = problem.parts[0].tests["check_equal"][9][0]
    print(test)
    problem.parts[0].remove_test(test)
    # print(problem.parts)
    problem.write_on_file(file_name + "_out.py")

        
