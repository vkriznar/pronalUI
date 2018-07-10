import re
def check_parentheses(line):
    counter=0
    
    for char in line:
        if char=="(":
            counter += 1
        elif char==")":
            counter -= 1
            
    return counter==0

def make_one_line_tuples(lines):
    """
    INPUT: validation lines
    OUTPUT: validation lines where all multiline tuples are transformed in one line tuples
    """
    lines2 = []
    lines_inside_tuple = []
    inside_tuple=False
    
    for line in lines:
        if line.startswith("("):
            # if number of parantheses -> ( , ) doesn't match, we continue in another line
            if not check_parentheses(line): 
                inside_tuple=True
                lines_inside_tuple.append(line.strip())
                continue
            
        if not inside_tuple:
            # if tuple ends in the same line no need for changes, we just append this line on lines2 in the bottom
            lines2.append(line.rstrip())
            
        elif inside_tuple:
            # if we are inside tuple, we append curent line on lines_inside_tuple and we check if tuple ends in this line
            lines_inside_tuple.append(line)
            
            if not check_parentheses(line):
                # if number of parantheses in this line doesn't match, this means tuple has ended
                inside_tuple=False
                lines2.append(" ".join(lines_inside_tuple))
                lines_inside_tuple=[]
            
    return lines2

class CheckEqual:
    def __init__(self, expression, output):
        self.expression = expression
        self.output = output

    def __repr__(self):
        return "Check.equal({0}, {1})".format(self.expression, self.output)
        
class CheckSecret:
    def __init__(self, expression, other):
        self.expression = expression
        self.ther = ther

    def __repr__(self):
        return "Check.secret({0}, {1})".format(self.expression, self.other)  
    
class ProblemPart:
    def __init__(self, part_id, description, precode, solution, tests):
        self.part_id = part_id
        # we use strip, because the user can input only white space and we don't want to save that
        self.description = description.strip()
        self.precode = precode.strip() 
        self.solution = solution.strip()
        if isinstance(tests, str):
            tests = ProblemPart.parse_tests(tests)
            
        self.tests = tests
        ## {"check_equal":[[...],[...],...], "other": "STRING OF OTHER TESTS"}


    def __repr__(self):
        string_list = []
        string_list.append("# "+"="*69+"@{0:06d}=\n".format(self.part_id))                        # beginning of part header
        string_list.append("# "+self.description.replace("\n", "\n# ")+"\n")                      # description
        # we don't want precode section if there is no precode
        if len(self.precode)>0:
            string_list.append("# "+"-"*77+"\n")                                                  # optional beginning of template
        if len(self.precode)>0:
            string_list.append("# "+self.precode.replace("\n", "\n# ")+"\n")                      # precode (solution tamplate)  
        string_list.append("# "+"="*77+"\n")                                                      # boarder between description and precode
        string_list.append(self.solution+"\n\n")                                                  # solution

        ## TODO remove this in future
        if self.tests is None:
            return "".join(string_list)
        
        string_list.append("Check.part()\n")                                                      # beginning of validation

        def add_check_equal_tests_to_string_list(string_list, check_equal_tests):
            for test_equal_connected_with_and in check_equal_tests:
                for test_equal in test_equal_connected_with_and:
                    if test_equal_connected_with_and.index(test_equal)==len(test_equal_connected_with_and)-1:
                        string_list.append(str(test_equal) + "\n")
                    else:
                        string_list.append(str(test_equal) + " and \\ \n")
                        

        add_check_equal_tests_to_string_list(string_list, self.tests["check_equal"])
        
        string_list.append(self.tests["other"])

        return "".join(string_list)

    @staticmethod
    def parse_tests(validation):
        ## TODO add meta data (for now we have double list for and conection, maybe use dict?)
        def classify_tests(validation):
            def classify_check_equal(check_equal_string):
                """
                Check.equal tests are: Check.equal(expression, output), type(expression) = str
                we find expression so that we first look for quotation mark (' or ''' or  " or \""")
                which marks begining and end of expression

                expression: the shortest text that matches expression format
                output: all other text from Check.equal arguments
                """
                ## TODO maybe use: from ast import literal_eval
                ## evaluates the right part of touple wich for now is OK?
                ## posible problem: ("15", [0, 15, 2][1])
                ## as it can not evaluate such complex expresions
                ## but this is ok: ("(12, [3, 5])", (12, [3, 5]))

                check_equal_string=check_equal_string.strip().strip("Check.equal(").strip() 

                quotation_mark_type_expression = check_equal_string[0] # can be ' or ''' or " or """
                triple_quotation_mark_expression = check_equal_string[0]==check_equal_string[1] # True if ''' or """
                
                if not triple_quotation_mark_expression:
                    expression=re.match(r"({0}(.*?)[^{0}]{0})[^{0}]".format(quotation_mark_type_expression), check_equal_string).group(1)
                    
                else:
                    expression=re.match(r"{0}{0}{0}(.*?){0}{0}{0}".format(quotation_mark_type_expression), check_equal_string).group(0)
                    
                output=check_equal_string[len(expression)+1:].strip().strip(",")[:-1].strip()
 
                return expression, output     
            

            
            
            validation=re.sub(r"and\s*", r"and ", validation)
            lines = validation.split("\n")
            
            other_lines = []
            check_equals = []

            # for i in make_tuples_for_and_connected(make_one_line_tuples(lines)): print(i)
            
            for line in make_one_line_tuples(lines):
                if line.startswith("Check.equal"):
                    expression, output = classify_check_equal(line.strip())
                    check_equals.append([CheckEqual(expression,  output)])
                    
                elif line.startswith("("):
                    line=line[1:-1].strip()
                    
                    list_of_check_equals=line.split("and")
                    check_equals_connected_with_and=[]
                    
                    for check_equal_string in list_of_check_equals:
                        expression, output = classify_check_equal(check_equal_string)
                        check_equals_connected_with_and.append(CheckEqual(expression,  output))
                        
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
    file_name="../edit_files/podnaloga"
    with open(file_name + "_in.py", "r", encoding="utf-8") as f:
        problem_part_string = f.read()
    
    def instructions_string(problem_part_string):
        return problem_part_string.split("Check.part()")[0].strip()
    
    problem_part = parse_test(problem_part_string)
    # print(str(problem_part))
    assert instructions_string(problem_part_string) == instructions_string(str(problem_part))
    
    napisi_na_dat(file_name+"_out.py", problem_part_string)

