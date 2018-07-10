with open(__file__, encoding='utf-8') as f:
    source = f.read()
exec(source[source.find("# =L=I=B=""R=A=R=Y=@="):])
problem = extract_problem(__file__)
Check.initialize(problem['parts'])

# =============================================================================
# Biopython
#
# Oglej si naslednji spletni strani in sledi navodilom v nadaljevanju:
# 
# http://biopython.org/
# 
# https://www.ncbi.nlm.nih.gov/sra
# =====================================================================@015026=
# Iz spletne strani `http://biopython.org/` si inštaliraj modul Biopython.
# 
# Nato izvedi spodnjo kodo (pritisni F5), ki ti prikaže pomoč:
# 
#     import Bio
#     print(help(Bio))
# -----------------------------------------------------------------------------
# # Ta stavek nalozi modul Bio:
# import Bio
# # Ta stavek ti izpise pomoc za ta modul:
# print(help(Bio))
# =============================================================================
import Bio
print(help(Bio))

Check.part()
(   Check.equal('odstej(8, 8)', 25 ) and 
    Check.equal('odstej(88, 18)', 100) and 
    Check.equal("odstej(20, 20)", 400)
)

(
    Check.equal('sestej(81, 81)', 25 ) and 
    Check.equal('sestej(88, 18)', 100) and 
    Check.equal("sestej(20, 20)", 400)
)

Check.equal('zmnozi((2, 88), 2)', 4) and \
Check.equal('zmnozi(3, 3)', 9)
Check.equal('zmnozi(4, 4)', 16, clean=clean, env=env)
Check.equal('zmnozi(5, 5)', 25 )
Check.equal('zmnozi(int("10"), 10)', int('100'))

Check.equal("zmnozi(int('10'), 10)", 100)
Check.equal("zmnozi(int('''10'''), int('10'))", int('100'))

Check.equal('''zmnozi(int('10'), int("10"))''', 100)

Check.equal("zmnozi(20, 20)", 400) and \
Check.equal("zmnozi('20', 20)", 400) and \
Check.equal('x', 50 // 6)


print('\n\n' + '*' * 15 + ' POZOR - naloga nima testa! ' +  '*' * 10)
print('Zato bo vsaka rešitev označena kot pravilna. ')
print('\nZagotovo si oglej tudi uradno rešitvo (žarnica)')
print('in jo primerjaj s svojo.')
print('\n' + '*' * 50)


# =====================================================================@015027=
# Na spletni strani `https://www.ncbi.nlm.nih.gov/guide/howto/dwn-genome/`
# poišči genski zapis z oznako KT232076.1 in v obliki niza povej za
# katero vrsto bakterije gre.
# 
#     # Resitev bo oblike:
#     "Enterobacteria *** lambda"
#     # kjer tri zvezdice zamenjaj za ustrezno ime.
# =============================================================================
"Enterobacteria phage lambda"

Check.part()
resitev = eval(Check.current_part['solution'])
if not isinstance(resitev, str):
    Check.error('Rešitev mora biti niz. Nizi se pisejo takole "TUKAJ JE BESEDILO"')

if "Enterobacteria phage lambda" not in resitev:
    Check.error('Napisati morate pravilen niz. Namig resitev je: "Enterobacteria phage lambda"')


# =====================================================================@015028=
# Uporabi kodo:
# 
#     from Bio import Entrez
#     from Bio import SeqIO
#     Entrez.email = "tvoj.email@student.uni-lj.si"
#     handle = Entrez.efetch(db="nucleotide", id="KT232076.1", rettype="gb")
#     podatki = SeqIO.read(handle, "genbank")
#     sekvenca = podatki.seq
#     x = len(podatki.seq)
# -----------------------------------------------------------------------------
# from Bio import Entrez
# from Bio import SeqIO
# 
# Entrez.email = "tvoj.email@student.uni-lj.si"
# handle = Entrez.efetch(db="nucleotide", id="KT232076.1", rettype="gb")
# podatki = SeqIO.read(handle, "genbank")
# sekvenca = podatki.seq
# x = len(podatki.seq)
# # V spremenljivki x je shranjena dolzina Enterobacterie.
# # V spremenljivki sekvenca pa imas niz, ki predstavlja
# # genski zapis te bakterije.
# # Vse kar ta naloga zahteva je da vpises svoj email namesto
# # tvoj.email@student.uni-lj.si in poženeš kodo z F5.
# #
# # Sedaj lahko na realnih podatkih preiskusis funkcije iz prejsne naloge.
# =============================================================================
x = 49205

Check.part()
Check.equal('x', 49205)


# # =====================================================================@000000=
# # This is a template for a new problem part. To create a new part, uncomment
# # the template and fill in your content.
# #
# # Define a function `multiply(x, y)` that returns the product of `x` and `y`.
# # For example:
# #
# #     >>> multiply(3, 7)
# #     21
# #     >>> multiply(6, 7)
# #     42
# # =============================================================================
#
# def multiply(x, y):
#     return x * y
#
# Check.part()
#
# Check.equal('multiply(3, 7)', 21)
# Check.equal('multiply(6, 7)', 42)
# Check.equal('multiply(10, 10)', 100)
# Check.secret(multiply(100, 100))
# Check.secret(multiply(500, 123))


# ===========================================================================@=
# Do not change this line or anything below it.
# =============================================================================


if __name__ == '__main__':
    _validate_current_file()

# =L=I=B=R=A=R=Y=@=

import io, json, os, re, sys, shutil, traceback, urllib.error, urllib.request

from contextlib import contextmanager

class Check:
    @staticmethod
    def has_solution(part):
        return part['solution'].strip() != ''

    @staticmethod
    def initialize(parts):
        Check.parts = parts
        for part in Check.parts:
            part['valid'] = True
            part['feedback'] = []
            part['secret'] = []
        Check.current_part = None
        Check.part_counter = None

    @staticmethod
    def part():
        if Check.part_counter is None:
            Check.part_counter = 0
        else:
            Check.part_counter += 1
        Check.current_part = Check.parts[Check.part_counter]
        return Check.has_solution(Check.current_part)

    @staticmethod
    def feedback(message, *args, **kwargs):
        Check.current_part['feedback'].append(message.format(*args, **kwargs))

    @staticmethod
    def error(message, *args, **kwargs):
        Check.current_part['valid'] = False
        Check.feedback(message, *args, **kwargs)

    @staticmethod
    def clean(x, digits=6, typed=False):
        t = type(x)
        if t is float:
            x = round(x, digits)
            # Since -0.0 differs from 0.0 even after rounding,
            # we change it to 0.0 abusing the fact it behaves as False.
            v = x if x else 0.0
        elif t is complex:
            v = complex(Check.clean(x.real, digits, typed), Check.clean(x.imag, digits, typed))
        elif t is list:
            v = list([Check.clean(y, digits, typed) for y in x])
        elif t is tuple:
            v = tuple([Check.clean(y, digits, typed) for y in x])
        elif t is dict:
            v = sorted([(Check.clean(k, digits, typed), Check.clean(v, digits, typed)) for (k, v) in x.items()])
        elif t is set:
            v = sorted([Check.clean(y, digits, typed) for y in x])
        else:
            v = x
        return (t, v) if typed else v

    @staticmethod
    def secret(x, hint=None, clean=None):
        clean = clean or Check.clean
        Check.current_part['secret'].append((str(clean(x)), hint))

    @staticmethod
    def equal(expression, expected_result, clean=None, env={}):
        local_env = locals()
        local_env.update(env)
        clean = clean or Check.clean
        actual_result = eval(expression, globals(), local_env)
        if clean(actual_result) != clean(expected_result):
            Check.error('Izraz {0} vrne {1!r} namesto {2!r}.',
                        expression, actual_result, expected_result)
            return False
        else:
            return True

    @staticmethod
    def run(statements, expected_state, clean=None, env={}):
        code = "\n".join(statements)
        statements = "  >>> " + "\n  >>> ".join(statements)
        s = {}
        s.update(env)
        clean = clean or Check.clean
        exec(code, globals(), s)
        errors = []
        for (x, v) in expected_state.items():
            if x not in s:
                errors.append('morajo nastaviti spremenljivko {0}, vendar je ne'.format(x))
            elif clean(s[x]) != clean(v):
                errors.append('nastavijo {0} na {1!r} namesto na {2!r}'.format(x, s[x], v))
        if errors:
            Check.error('Ukazi\n{0}\n{1}.', statements,  ";\n".join(errors))
            return False
        else:
            return True

    @staticmethod
    @contextmanager
    def in_file(filename, content, encoding=None):
        with open(filename, 'w', encoding=encoding) as f:
            for line in content:
                print(line, file=f)
        old_feedback = Check.current_part['feedback'][:]
        yield
        new_feedback = Check.current_part['feedback'][len(old_feedback):]
        Check.current_part['feedback'] = old_feedback
        if new_feedback:
            new_feedback = ['\n    '.join(error.split('\n')) for error in new_feedback]
            Check.error('Pri vhodni datoteki {0} z vsebino\n  {1}\nso se pojavile naslednje napake:\n- {2}', filename, '\n  '.join(content), '\n- '.join(new_feedback))

    @staticmethod
    @contextmanager
    def input(content, encoding=None):
        old_stdin = sys.stdin
        old_feedback = Check.current_part['feedback'][:]
        sys.stdin = io.StringIO('\n'.join(content))
        try:
            yield
        finally:
            sys.stdin = old_stdin
        new_feedback = Check.current_part['feedback'][len(old_feedback):]
        Check.current_part['feedback'] = old_feedback
        if new_feedback:
            new_feedback = ['\n  '.join(error.split('\n')) for error in new_feedback]
            Check.error('Pri vhodu\n  {0}\nso se pojavile naslednje napake:\n- {1}', '\n  '.join(content), '\n- '.join(new_feedback))

    @staticmethod
    def out_file(filename, content, encoding=None):
        with open(filename, encoding=encoding) as f:
            out_lines = f.readlines()
        equal, diff, line_width = Check.difflines(out_lines, content)
        if equal:
            return True
        else:
            Check.error('Izhodna datoteka {0}\n  je enaka{1}  namesto:\n  {2}', filename, (line_width - 7) * ' ', '\n  '.join(diff))
            return False

    @staticmethod
    def output(expression, content, use_globals=False):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            def visible_input(prompt):
                inp = input(prompt)
                print(inp)
                return inp
            exec(expression, globals() if use_globals else {'input': visible_input})
        finally:
            output = sys.stdout.getvalue().strip().splitlines()
            sys.stdout = old_stdout
        equal, diff, line_width = Check.difflines(output, content)
        if equal:
            return True
        else:
            Check.error('Program izpiše{0}  namesto:\n  {1}', (line_width - 13) * ' ', '\n  '.join(diff))
            return False

    @staticmethod
    def difflines(actual_lines, expected_lines):
        actual_len, expected_len = len(actual_lines), len(expected_lines)
        if actual_len < expected_len:
            actual_lines += (expected_len - actual_len) * ['\n']
        else:
            expected_lines += (actual_len - expected_len) * ['\n']
        equal = True
        line_width = max(len(actual_line.rstrip()) for actual_line in actual_lines + ['Program izpiše'])
        diff = []
        for out, given in zip(actual_lines, expected_lines):
            out, given = out.rstrip(), given.rstrip()
            if out != given:
                equal = False
            diff.append('{0} {1} {2}'.format(out.ljust(line_width), '|' if out == given else '*', given))
        return equal, diff, line_width

    @staticmethod
    def generator(expression, expected_values, should_stop=False, further_iter=0, env={}, clean=None):
        from types import GeneratorType
        local_env = locals()
        local_env.update(env)
        clean = clean or Check.clean
        gen = eval(expression, globals(), local_env)
        if not isinstance(gen, GeneratorType):
            Check.error("Izraz {0} ni generator.", expression)
            return False

        try:
            for iteration, expected_value in enumerate(expected_values):
                actual_value = next(gen)
                if clean(actual_value) != clean(expected_value):
                    Check.error("Vrednost #{0}, ki jo vrne generator {1} je {2!r} namesto {3!r}.",
                                iteration, expression, actual_value, expected_value)
                    return False
            for _ in range(further_iter):
                next(gen)  # we will not validate it
        except StopIteration:
            Check.error("Generator {0} se prehitro izteče.", expression)
            return False
        
        if should_stop:
            try:
                next(gen)
                Check.error("Generator {0} se ne izteče (dovolj zgodaj).", expression)
            except StopIteration:
                pass  # this is fine
        return True

    @staticmethod
    def summarize():
        for i, part in enumerate(Check.parts):
            if not Check.has_solution(part):
                print('{0}. podnaloga je brez rešitve.'.format(i + 1))
            elif not part['valid']:
                print('{0}. podnaloga nima veljavne rešitve.'.format(i + 1))
            else:
                print('{0}. podnaloga ima veljavno rešitev.'.format(i + 1))
            for message in part['feedback']:
                print('  - {0}'.format('\n    '.join(message.splitlines())))


def extract_problem(filename):
    def strip_hashes(description):
        if description is None:
            return ''
        else:
            lines = description.strip().splitlines()
            return "\n".join(line[line.index('#')+2:] for line in lines)

    with open(filename, encoding='utf-8') as f:
        source = f.read()
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
    parts = [{
        'part': int(match.group('part')),
        'description': strip_hashes(match.group('description')),
        'solution': match.group('solution').strip(),
        'template': strip_hashes(match.group('template')),
        'validation': match.group('validation').strip(),
        'problem': 5618
    } for match in part_regex.finditer(source)]
    problem_match = re.search(
        r'^\s*# =+\s*\n'                         # beginning of header
        r'^\s*# (?P<title>[^\n]*)\n'             # title
        r'(?P<description>(^\s*#( [^\n]*)?\n)*)' # description
        r'(?=\s*(# )?# =+@)',                    # beginning of first part
        source, flags=re.DOTALL | re.MULTILINE)
    return {
        'title': problem_match.group('title').strip(),
        'description': strip_hashes(problem_match.group('description')),
        'parts': parts,
        'id': 5618,
        'problem_set': 1380
    }

def _validate_current_file():
    def backup(filename):
        backup_filename = None
        suffix = 1
        while not backup_filename or os.path.exists(backup_filename):
            backup_filename = '{0}.{1}'.format(filename, suffix)
            suffix += 1
        shutil.copy(filename, backup_filename)
        return backup_filename

    def submit_problem(problem, url, token):
        for part in problem['parts']:
            part['secret'] = [x for (x, _) in part['secret']]
            if part['part']:
                part['id'] = part['part']
            del part['part']
            del part['feedback']
            del part['valid']
        data = json.dumps(problem).encode('utf-8')
        headers = {
            'Authorization': token,
            'content-type': 'application/json'
        }
        request = urllib.request.Request(url, data=data, headers=headers)
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode('utf-8'))

    Check.summarize()
    if all(part['valid'] for part in problem['parts']):
        print('The problem is correctly formulated.')
        if input('Should I save it on the server [yes/NO]') == 'yes':
            print('Saving problem to the server...', end="")
            try:
                url = 'https://www.projekt-tomo.si/api/problems/submit/'
                token = 'Token 19a8b1042389a925da13551cc632fc7cc402a3d8'
                response = submit_problem(problem, url, token)
                if 'update' in response:
                    print('Updating file... ', end="")
                    backup_filename = backup(__file__)
                    with open(__file__, 'w', encoding='utf-8') as f:
                        f.write(response['update'])
                    print('Previous file has been renamed to {0}.'.format(backup_filename))
                    print('If the file did not refresh in your editor, close and reopen it.')
            except urllib.error.URLError as response:
                message = json.loads(response.read().decode('utf-8'))
                print('\nAN ERROR OCCURED WHEN TRYING TO SAVE THE PROBLEM!')
                if message:
                    print('  ' + '\n  '.join(message.splitlines()))
                print('Please, try again.')
            else:
                print('Problem saved.')
        else:
            print('Problem was not saved.')
    else:
        print('The problem is not correctly formulated.')
