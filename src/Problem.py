import re
from ProblemPart import ProblemPart
import numpy as np

def strip_hashes(description):
    """Removes hash and space sings form each line in description."""
    
    if description is None:
        return ''
    else:
        lines = description.strip().splitlines()
        return "\n".join(line[line.index('#')+2:] for line in lines)

class Problem:
    """
    Defines Problem class in wich we store abstract representation of problem
    string. This class implements all necesery method for problem manipulation.
    For example we can create problem object from string. We can also save
    given problem when we are done with editing it.
    """
    def __init__(self, title, description, parts, lib_string, head_string):
        self.head_string = head_string # header lines at the beginning of file
        self.title = title.strip()
        self.description = description.strip()
        self.parts = parts
        self.lib_string = lib_string # template and library
        

    @staticmethod
    def parse(file_string):
        """Transforms the string representing problem into Problem object."""
        
##        DO NOT DELETE THIS ! (we will use this if they don't fix problem on TOMO)
##        maybe better if we look for:
##        # ===========================================================================@=
##        # Ne spreminjajte te vrstice ali česarkoli pod njo.
##        # =============================================================================
##        because we don't always want template

        # Mitja: I would like to delate above messege.

        split_index = file_string.find(
"""# # =====================================================================@000000=
# # This is a template for a new problem part. To create a new part, uncomment
# # the template and fill in your content.""")
        if split_index==-1: # if there is no english tempalate, then we try to find slovene template
            split_index = file_string.find(
"""# # =====================================================================@000000=
# # To je predloga za novo podnalogo. Če želite ustvariti novo podnalogo,
# # pobrišite komentarje ter vsebino zamenjajte s svojo.""")
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
        """
        String representation of problem. Same as on Tomo,
        can be read in object with parse method.
        """
        def remove_unnecessary_lines(text):
            return "\n".join([line.rstrip() for line in text.splitlines()])
        
        self.title = remove_unnecessary_lines(self.title)
        self.description = remove_unnecessary_lines(self.description)
        
        blocks = []
        blocks.append(self.head_string)
        blocks.append("\n# "+ "=" * 77)
        blocks.append("# " + "\n# ".join(self.title.split("\n"))+ "\n#")
        blocks.append("# "+"\n# ".join(self.description.split("\n")))
        
        for part in self.parts:
            blocks.append(str(part))

        # Mitja: TODO better explanation of below messege.
        
##        # DO NOT DELETE ! (we will use this if they don't fix problem on TOMO)
##        # if there are no parts on the file, we don't write template, because it appears weird on TOMO
##        if len(self.parts)==0:
##            print("ni podnalog")
##            self.lib_string = self.lib_string[self.lib_string.find("\n\n")+1:]
        blocks.append(self.lib_string)

    
        return "\n".join(blocks).replace("\\ \n","\\\n")


    def write_on_file(self, file_name):
        """Writes the problem string representation in given file."""
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(str(self))


    @staticmethod
    def load_file(file_path):
        """Reads the problem from file, given by file_path string."""
        with open(file_path, "r", encoding="utf-8") as f:
            file_string = f.read()
            
        return Problem.parse(file_string)

##    # Mitja: TODO: Why do we need this? If needed convert to static and comment it.
##    def read_filefile(filefile):
##        file_string = ""
##        for line in filefile:
##            file_string += line.decode().rstrip()+"\n"
##            
##        return Problem.parse(file_string)


    def new_problem_part(self, i=-1):
        """Creates default problem part, given for later modifications."""
        # TODO: Rethink if this method realy needs to load new file
        # as default problem
        # part could be also read from given file
        try:
            def_problem = ProblemPart.load_file("parameters/default_part.py")
        except:
            print("Error loading the default_part file.")
            
        if 0 <= i < len(self.parts):
            self.parts.insert(i, def_problem)
        else:
            self.parts.append(def_problem)

        return def_problem


    def remove_problem_part(self, problem_part):
        """Removes given problem part."""
        if problem_part in self.parts:
            self.parts.remove(problem_part)
        else:
            print("[ERROR] in remove_problem_part.")


    
    def renumbering_parts(self, new_numbers):
        """Renumbers the problem part with respect to new_numbers list."""
        parts = np.array(self.parts)
        self.parts = parts[new_numbers].tolist()
        
        


if __name__ == "__main__":
    file_name =   "../edit_files/naloga"
    problem = Problem.load_file(file_name + "_in.py")
    # testing test deletion
    # test = problem.parts[0].tests["check_equal"][9][0]
    # print(test)
    # problem.parts[0].remove_test(test)
    
    # print(problem.parts)
    problem.write_on_file(file_name + "_out.py")

        
