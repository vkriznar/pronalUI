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
            lines_inside_tuple.append(line.lstrip())
            
            if not check_parentheses(line):
                # if number of parantheses in this line doesn't match, this means tuple has ended
                inside_tuple=False
                lines2.append(" ".join(lines_inside_tuple))
                lines_inside_tuple=[]
            
    return lines2

class CheckEqual:
    def __init__(self, expression, output):
        # TODO remove string tags in expresion
        # TODO when expresion is writen to file we should write it with triple " (""")
        # TODO split output on solution and clean, env
        expression = expression.replace('"""',"'''")
        self.expression = expression.strip()
        self.output = output.strip()

    def __repr__(self):
        return 'Check.equal("""{0}""", {1})'.format(self.expression, self.output)

    def example(self):
        return ">>> " + self.expression + "\n" + self.output

# TODO check secret should have only one parameter
# TODO as with check equal all other parameters can be saved in same string
# TODO because there sholud be only one fild in editor window
# TODO CheckEqual (4 args) -> (2 args; input, out);   out; res, clean, env
# TODO CheckSecret (3 args) -> (1 args; input)      input; exp, hint, clean
class CheckSecret:
    def __init__(self, expression, other=""):
        self.expression = expression
        other = other.replace('"""', "'''")
        self.other = other

    def __repr__(self):
        if len(self.other) > 0:
            return 'Check.secret({0}, """{1}""")'.format(self.expression, self.other)
        else:
            return "Check.secret({0})".format(self.expression)
    
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
        def remove_unnecessary_lines(text):
            return "\n".join([line.rstrip() for line in text.splitlines()])
        
        self.description = remove_unnecessary_lines(self.description)
        self.precode = remove_unnecessary_lines(self.precode)
        self.solution = remove_unnecessary_lines(self.solution)
        self.tests["other"] = remove_unnecessary_lines(self.tests["other"])
        
        string_list = []
        string_list.append("# "+"="*69+"@{0:06d}=\n".format(self.part_id))                        # beginning of part header
        string_list.append("# "+self.description.replace("\n", "\n# ")+"\n")                      # description
        # we don't want precode section if there is no precode
        if len(self.precode)>0:
            string_list.append("# "+"-"*77+"\n")                                                  # optional beginning of template
            string_list.append("# "+self.precode.replace("\n", "\n# ")+"\n")                      # precode (solution tamplate)  
        string_list.append("# "+"="*77+"\n")                                                      # boarder between description and precode
        string_list.append(self.solution+"\n\n")                                                  # solution

        ## TODO remove this in future
        if self.tests is None:
            return "".join(string_list)
        
        string_list.append("Check.part()\n")                                                      # beginning of validation

        def add_check_tests_to_string_list(string_list, check_tests):
            for test_connected_with_and in check_tests:
                for test in test_connected_with_and:
                    if test_connected_with_and.index(test)==len(test_connected_with_and)-1:
                        string_list.append(str(test) + "\n")
                    else:
                        string_list.append(str(test) + " and \\ \n")
                        

        add_check_tests_to_string_list(string_list, self.tests["check_equal"])
        add_check_tests_to_string_list(string_list, self.tests["check_secret"])
        
        string_list.append(self.tests["other"])

        return "".join(string_list)  

    @staticmethod
    def remove_test_type(test, test_type):
        for test_group in test_type:
            if test in test_group:
                if len(test_group) > 1:
                    test_group.remove(test)
                else:
                    test_type.remove(test_group)

                # cause we already find it
                return
        
    def remove_test(self, test):
        if isinstance(test, CheckEqual):
            ProblemPart.remove_test_type(test, self.tests["check_equal"])
        elif isinstance(test, CheckSecret):
            ProblemPart.remove_test_type(test, self.tests["check_secret"])
        else:
            print(type(test))
            print(test)
            print("Can not remove this test type.")

    def change_test_by_id(self, test_type, group_id, i, expression, output):
        if (test_type in self.tests and
            group_id < len(self.tests[test_type]) and
            i < len(self.tests[test_type][group_id])):
                test = self.tests[test_type][group_id][i]
            
        else:
            return False

        test.expression = expression
        if test_type == "check_equal":
            test.output = output
        else:
            test.other = output
        return True

    # moving check secret and equal test up and down
    # testiranje:
    #   poženi problem.py,
    #   for i in problem.parts[0].tests["check_equal"]:print(i)
    #   problem.parts[0].move_test_group_down('check_equal', 8)
    #   problem.parts[0].move_test_group_down('check_equal', 9)
    #   problem.parts[0].move_test_within_group_down('check_equal', 0, 1)
    #   problem.parts[0].move_test_within_group_up('check_equal', 0, 1)
    #
    def move_test_group_up(self, test_type, group_id):
        if not (test_type in self.tests and
            group_id>0 and group_id < len(self.tests[test_type]) and
                len(self.tests[test_type]) > 1 ):
                    print("group up:", test_type, group_id, "FALSE")
                    return False
            
        else:
            self.tests[test_type][group_id - 1], self.tests[test_type][group_id] = \
                self.tests[test_type][group_id], self.tests[test_type][group_id - 1]
            print("group up:", test_type, group_id, "TRUE")
            return True
                
    def move_test_group_down(self, test_type, group_id):
        if not (test_type in self.tests and
            group_id >= 0 and group_id < len(self.tests[test_type])-1 and
            len(self.tests[test_type]) > 1):
                print("group down:", test_type, group_id, "FALSE")
                return False
            
        else:
            self.tests[test_type][group_id + 1], self.tests[test_type][group_id] = \
                self.tests[test_type][group_id], self.tests[test_type][group_id + 1]
            print("group down:", test_type, group_id, "TRUE")
            return True

    def move_test_within_group_up(self, test_type, group_id, i):
##        if not (test_type in self.tests and
##            group_id < len(self.tests[test_type]) and
##            i>0 and i < len(self.tests[test_type][group_id]) and
##                len(self.tests[test_type][group_id]) > 1):
##            
##                print("test up:", test_type, group_id, i, "FALSE")
##                return False
##        else:
        self.tests[test_type][group_id][i-1], self.tests[test_type][group_id][i] = \
            self.tests[test_type][group_id][i], self.tests[test_type][group_id][i-1]
##            print("test up:", test_type, group_id, i, "TRUE")
##            return True
        
    def move_test_within_group_down(self, test_type, group_id, i):
        if not (test_type in self.tests and
            group_id < len(self.tests[test_type]) and
            i < len(self.tests[test_type][group_id]) - 1 and
                len(self.tests[test_type][group_id]) > 1):
                print("test down:", test_type, group_id, i, "FALSE")
                return False
        else:
            self.tests[test_type][group_id][i+1], self.tests[test_type][group_id][i] = \
                self.tests[test_type][group_id][i], self.tests[test_type][group_id][i+1]
            print("test down:", test_type, group_id, i, "TRUE")
            return True
        

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
                
                
                if not is_triple_quotation_mark(check_equal_string):
                    expression=re.match(r"({0}((.*?)[^{0}]){0})[^{0}]".format(quotation_mark_type_expression), check_equal_string).group(1)
                    output=check_equal_string[len(expression)+1:].strip().strip(",")[:-1].strip()
                    expression=expression[1:-1]
                    
                else:
                    expression=re.match(r"{0}{0}{0}(.*?){0}{0}{0}".format(quotation_mark_type_expression), check_equal_string).group(0)
                    output=check_equal_string[len(expression)+1:].strip().strip(",")[:-1].strip()
                    expression=expression[3:-3]
                    
                return CheckEqual(expression, output)

            def is_triple_quotation_mark(string):
                string = string.strip()
                # True if ''' or """
                return string[0] == string[1] if len(string) > 2 else False
                
            
            def classify_check_secret(check_secret_string):
                # TODO add clean option
                check_secret_string=check_secret_string.strip().strip("Check.secret(").strip()[:-1].strip()

                quotation_mark_type=check_secret_string[-1]
                if quotation_mark_type == "'" or quotation_mark_type == '"':
                    # check if there is hint argument
                    if not is_triple_quotation_mark(check_secret_string[::-1]):
                        # check if matches on reversed string
                        hint_msg=re.match(r"({0}(.*?)[^{0}]{0})[^{0}]".format(quotation_mark_type), check_secret_string[::-1]).group(1)[::-1]           
                    else:
                        hint_msg=re.search(r"{0}{0}{0}(.*?){0}{0}{0}".format(quotation_mark_type), check_secret_string[::-1]).group(0)[::-1]

                    expression=check_secret_string[0:-len(hint_msg)].strip().strip(",").strip()

                    if not is_triple_quotation_mark(check_secret_string[::-1]):
                        hint_msg=hint_msg[1:-1]
                    else:
                        hint_msg=hint_msg[3:-3]


                else:
                    expression=check_secret_string
                    hint_msg=""
                    
                return CheckSecret(expression, hint_msg)

            def decompose_and(line):
                list_of_check_equals=line.split(" and ")
                
                check_equals_connected_with_and = []
                check_secrets_connected_with_and = []
                
                for check_string in list_of_check_equals:
                    check_string=check_string.strip()
                    if check_string.startswith("Check.equal"):
                        check_equals_connected_with_and.append(classify_check_equal(check_string))
                    elif check_string.startswith("Check.secret"):
                        check_secrets_connected_with_and.append(classify_check_secret(check_string))
                
                return check_equals_connected_with_and, check_secrets_connected_with_and


            def split_validation(validation):
                """ INPUT: whole validation part
                    OUTPUT: validation part with ok tests (equal and secret tests connected with whatever) and
                            other lines (which starts where tests are not ok anymore)
                """
                def ok_line(line):
                    if line=="" or line.startswith(("(", ")", "Check.equal", "Check.secret")):
                        return True
                    return False
                
                lines = validation.split("\n")
                for i in range(len(lines)):
                    line = lines[i].strip()
                    if not ok_line(line):
                        # print("validation: \n", "\n".join(lines[:i]))
                        # print("other: \n", lines[i:])
                        return "\n".join(lines[:i]), lines[i:]
                    
                ## at this point we return empty list for other lines, because all lines are ok
                return "\n".join(lines), [] 
                    
                
            validation, bottom_other_lines = split_validation(validation)
            
            validation = re.sub(r"and\s*\\\s*", r"and ", validation)
            
            lines = validation.split("\n")
            
            check_equals = []
            check_secrets = []
            other_lines = []

            new_lines = make_one_line_tuples(lines)
            
            for i in range(len(new_lines)):
                line = new_lines[i].strip()
                if " or " in line:
                    ## we check if "or" is in line, if it is we add remanig lines to other_lines
                    other_lines.extend(new_lines[i:])
                    break
                
                elif line.startswith("Check.equal") or line.startswith("Check.secret"):
                    check_equals_with_and, check_secrets_with_and = decompose_and(line)
                    check_equals.append(check_equals_with_and)
                    check_secrets.append(check_secrets_with_and)
                    
                elif line.startswith("("):
                    line = line[1:-1].strip()

                    check_equals_with_and, check_secrets_with_and = decompose_and(line)
                    check_equals.append(check_equals_with_and)
                    check_secrets.append(check_secrets_with_and)
                    
                else:
                    ## if line is empty we still check for secret and equal tests
                    if line != "":
                        other_lines.extend(new_lines[i:])
                        break

            other_lines.extend(bottom_other_lines)
            check_equals = [z for z in check_equals if len(z) > 0]
            check_secrets = [z for z in check_secrets if len(z) > 0]
            
            return check_equals, check_secrets, other_lines
        
        check_equals, check_secrets, other_lines = classify_tests(validation)
        tests = {"check_equal" : check_equals, "other": "\n".join(other_lines), "check_secret" : check_secrets}

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
        
        return ProblemPart(part_id, description, precode, solution, tests)


    def code_to_description(self, code, line_num):
        if len(code.strip()) > 0:
            string_list = self.description.split("\n")
            insert_text = "\n    " + code.replace("\n", "\n    ")
            if line_num < 0:
                string_list.append(insert_text)
            else:
                string_list.insert(line_num, insert_text)

            self.description = "\n".join(string_list)

    def precode_to_description(self, line_num=-1):
        self.code_to_description(self.precode, line_num)

# no need for this function use check_equals_to_description
## TODO remove in future
    def check_equal_to_description(self, test, line_num=-1):
        code = test.example()
        self.code_to_description(code, line_num)

    def check_equals_to_description(self, tests, line_num=-1):
        tests = [test for test in tests if isinstance(test, CheckEqual)]
        code = "\n".join([z.example() for z in tests])
        self.code_to_description(code, line_num)

    def write_on_file(self, file):
        with open(file, "w", encoding="utf-8") as f:
            f.write(str(self))

    @staticmethod
    def load_file(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            file_string = f.read()

        return ProblemPart.parse(file_string)










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

    tests = problem_part.tests
    print("\nTESTI: ")
    for key in tests:
        print(key.upper())
        if not isinstance(tests[key], list):
            print(tests[key])
            continue
        
        for z in tests[key]:
            print(z)
    
    # print(str(problem_part))
    assert instructions_string(problem_part_string) == instructions_string(str(problem_part))
    
    napisi_na_dat(file_name+"_out.py", problem_part_string)

