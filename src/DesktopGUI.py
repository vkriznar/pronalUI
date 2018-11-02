import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from Problem import Problem
from ProblemPart import ProblemPart
from ProblemPart import CheckEqual
from ProblemPart import CheckSecret

try:
    import idlelib
    try:
        from idlelib.Percolator import Percolator
    except:
        from idlelib.percolator import Percolator
    try:
        from idlelib.ColorDelegator import ColorDelegator
        from idlelib.ColorDelegator import color_config
    except:
        from idlelib.colorizer import ColorDelegator
        from idlelib.colorizer import color_config

    def add_colors_to_text(text):
        color_config(text)
        p = Percolator(text)
        d = ColorDelegator()
        p.insertfilter(d)

except:
    print("WARNING: idlelib dependency needs to be fixed.")
    print("WARNING: runing program with no colors for code.")
    
    def add_colors_to_text(text):
        pass

# constants
STICKY_ALL = (tk.N, tk.S, tk.E, tk.W)
TITLE_STYLE = "TkHeadingFont"
PROGRAM_STYLE = "TkFixedFont"

# FramedEntryGUI
class FrEntGUI:
    def __init__(self, parent, text=None, height=4, column=0, **kwargs):
        self.parent = parent
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(column=column, sticky=STICKY_ALL, **kwargs)
        self.frame.grid_columnconfigure(column, weight=1)
        
        if text is not None:
            self.equal_label = ttk.Label(self.frame, text=text)
            self.equal_label.grid(row=0, column=0, sticky=STICKY_ALL)
            
        self.entryGUI = EntryGUI(self.frame, height=height, undo=True)
        self.entry = self.entryGUI.text


class EntryGUI:
    def __init__(self, parent, height=4, wrap="word", scroll=True, **kwargs):
        self.parent = parent
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=2, column=0, sticky=STICKY_ALL)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)

        self.text = tk.Text(self.frame)
        self.text.config(height=height, wrap=wrap, **kwargs)
        self.text.grid(row=2, column=2, sticky=STICKY_ALL)
        self.text.grid_columnconfigure(2, weight=1)

        if scroll:
            self.scrollbar = ttk.Scrollbar(self.frame, command=self.text.yview)
            self.scrollbar.grid(row=2, column=4, sticky=STICKY_ALL)
            self.text['yscrollcommand']  = self.scrollbar.set

        self.text.bind("<Tab>", self.func_tab)

    def func_tab(self, *args):
        self.text.insert(tk.INSERT, " " * 4)
        return 'break'


##class ActionsToWidget:
##    def __init__(self, widget, widget_type=None, text_var=""):
##        self.widget = widget
##        self.widget.bind("<FocusOut>", self.on_focus_out)
##        self.widget.bind("<FocusIn>", self.on_focus_in)
##
##        if widget_type is None:
##            return
##
##        if "test_entry" in widget_type:
##            self.widget.config(fg = "grey")
##            self.widget.delete("1.0", "end")
##            self.on_focus_out = self.on_focus_out_entry
##            self.on_focus_in = self.on_focus_in_entry
##            
##            if widget_type == "test_entry_input":
##                self.widget.insert("1.0", "input")
##                self.default_text = "input"
##
##            #elif widget_type="test_entry_output":
##            else:
##                self.widget.insert("1.0", "output")
##                self.default_text = "output"
##
##    def on_focus_out(self, event):
##        pass
##
##    def on_focus_in(self, event):
##        pass
##
##    def on_focus_out_entry(self, event):
##        print("as")
##        if text_var.get() == "":
##            self.widget.insert(0, self.default_text)
##            self.widget.config(fg = 'grey')
##        
##
##    def on_focus_in_entry(self, event):
##        print("safaf")
##        if text_var.get() == "":
##            self.widget.delete(0, "end")
##            self.widget.insert(0, "")
##
##        self.widget.config(fg = "black")
    

class TestEqualFrame:
    def __init__(self, parent, row=2, test=None):
        self.parent = parent
        self.chosen = False
        self.test = test
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=row, column=0, sticky=STICKY_ALL)

        self.check_pressed_str = tk.StringVar()
        self.check_button = ttk.Checkbutton(
            self.frame, command=self.flip_chosen,
            variable=self.check_pressed_str,
	    onvalue='True', offvalue='False')
        self.check_button.grid(row=2, column=2, sticky=STICKY_ALL)

        #self.input_entry = ttk.Entry(self.frame)
        #self.input_str = tk.StringVar()
        #self.input_entry = ttk.Entry(self.frame, textvariable=self.input_str)
        #self.input_entry = tk.Entry(self.frame, textvariable=self.input_str)
        #ActionsToWidget(self.input_entry, "test_entry_input", self.input_str)
        #self.input_entry.grid(row=2, column=4, sticky=STICKY_ALL)

        self.input_entry_gui = EntryGUI(self.frame, height=1, scroll=False, wrap=None)
        self.input_entry = self.input_entry_gui.text
        self.input_entry.config(font=PROGRAM_STYLE)
        self.input_entry_gui.frame.grid(column=4)
        self.input_entry.config(width=25)
        add_colors_to_text(self.input_entry)
        self.add_update_action(self.input_entry)

        self.input_entry.delete("1.0","end")
        self.input_entry.insert("1.0", test.expression)
        
        self.output_entry_gui = EntryGUI(self.frame, height=1, scroll=False, wrap=None)
        self.output_entry = self.output_entry_gui.text
        self.output_entry.config(font=PROGRAM_STYLE)
        self.output_entry_gui.frame.grid(column=6)
        self.output_entry.config(width=25)
        add_colors_to_text(self.output_entry)
        self.add_update_action(self.output_entry)

        self.output_entry.delete("1.0","end") 
        self.output_entry.insert("1.0", test.output)

        #self.output_entry = ttk.Entry(self.frame)
        #self.output_str = tk.StringVar()
        #self.output_entry = ttk.Entry(self.frame, textvariable=self.output_str)
        #self.output_entry = tk.Entry(self.frame, textvariable=self.output_str)
        #ActionsToWidget(self.output_entry, "test_entry_output", self.output_str)
        #self.output_entry.grid(row=2, column=6, sticky=STICKY_ALL)

    def flip_chosen(self, event=None):
        self.chosen = not self.chosen
        print("flip_chosen", self.chosen)

    def save_all(self, event=None):
        self.update_field(self.input_entry, "test_input")
        self.update_field(self.output_entry, "test_output")

    def update_field(self, entry, field_name):
        field_data = entry.get("1.0", "end")
        if field_name == "test_input":
            self.test.expression = field_data.strip()
        elif field_name == "test_output":
            self.test.output = field_data.strip()

    def add_update_action(self, entry, field_name=None):
        update_field = self.save_all
        entry.bind('<Enter>', update_field)
        entry.bind('<Leave>', update_field)
        entry.bind('<Return>', update_field)
        


class TestSecretFrame:
    def __init__(self, parent, row=2, test=None, expand_other=False):
        self.parent = parent
        self.chosen = False
        self.test = test
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=row, column=0, sticky=STICKY_ALL)
        
        self.check_pressed_str = tk.StringVar()
        self.check_button = ttk.Checkbutton(
            self.frame, command=self.flip_chosen,
            variable=self.check_pressed_str,
	    onvalue="True", offvalue="False")
        self.check_button.grid(row=2, column=2, sticky=STICKY_ALL)

        self.input_entry_gui = EntryGUI(self.frame, height=1, scroll=False, wrap=None)
        self.input_entry = self.input_entry_gui.text
        self.input_entry.config(font=PROGRAM_STYLE)
        self.input_entry_gui.frame.grid(column=4)
        self.input_entry.config(width=25)
        add_colors_to_text(self.input_entry)
        self.add_update_action(self.input_entry)

        self.input_entry.delete("1.0","end")
        self.input_entry.insert("1.0", test.expression)

        self.output_entry = None
        if (test.other is not None and len(test.other) > 0) or expand_other:
            self.output_entry_gui = EntryGUI(self.frame, height=1, scroll=False, wrap=None)
            self.output_entry = self.output_entry_gui.text
            self.output_entry.config(font=PROGRAM_STYLE)
            self.output_entry_gui.frame.grid(column=6)
            self.output_entry.config(width=25)
            add_colors_to_text(self.output_entry)
            self.add_update_action(self.output_entry)

            self.output_entry.delete("1.0","end") 
            self.output_entry.insert("1.0", test.other)
        

    def flip_chosen(self, event=None):
        self.chosen = not self.chosen
        print("flip_chosen", self.chosen)

    def save_all(self, event=None):
        self.update_field(self.input_entry, "test_input")
        if self.output_entry is not None:
            self.update_field(self.output_entry, "test_other")

    def update_field(self, entry, field_name):
        field_data = entry.get("1.0", "end")
        if field_name == "test_input":
            self.test.expression = field_data.strip()
        elif field_name == "test_other":
            self.test.other = field_data.strip()

    def add_update_action(self, entry, field_name=None):
        update_field = self.save_all
        entry.bind('<Enter>', update_field)
        entry.bind('<Leave>', update_field)
        entry.bind('<Return>', update_field)


class TestGroup:
    #def __init__(self, parent, group_name, group_tests, group_type="equal"):

    def __init__(self, parent, tests, group_type, group_num):
        self.parent = parent
        self.tests = tests
        self.group_type = group_type
        self.group_num = group_num

        if group_type=="check_equal":
            group_name = "Check equal {}".format(group_num + 1)
            
        elif group_type=="check_secret":
            group_name = "Check secret {}".format(group_num + 1)
        
        self.label_frame = ttk.Labelframe(self.parent, text=group_name)
        self.label_frame.grid(row=2, column=0, sticky=STICKY_ALL)
        
        
        self.frame = ttk.Frame(self.label_frame)
        self.frame.grid(row=0, column=0, sticky=STICKY_ALL)

        self.chosen = False
        self.check_pressed_str = tk.StringVar()
        self.check_button = ttk.Checkbutton(
            self.frame, command=self.flip_chosen,
            variable=self.check_pressed_str,
	    onvalue="True", offvalue="False")
        self.check_button.grid(row=0, column=2, sticky=STICKY_ALL)
        self.frame.grid_columnconfigure(0, weight=1)

        self.test_frames = []
        if group_type=="check_equal":
            group_tests = tests["check_equal"][group_num]
            self.label = ttk.Label(self.frame, text="Check.equal(input, output)")
            self.label.grid(row=0, column=0, sticky=STICKY_ALL)
            for i in range(len(group_tests)):
                test_frame = TestEqualFrame(self.label_frame, 2*i+2, group_tests[i])
                self.test_frames.append(test_frame)

        if group_type=="check_secret":
            group_tests = tests["check_secret"][group_num]
            self.label = ttk.Label(self.label_frame, text="Check.secret(input)")
            self.label.grid(row=0, column=0, sticky=STICKY_ALL)
            for i in range(len(group_tests)):
                test_frame = TestSecretFrame(self.label_frame, 2*i+2, group_tests[i])
                self.test_frames.append(test_frame)


    def flip_chosen(self, event=None):
        self.chosen = not self.chosen
        print("flip_chosen", self.chosen)


def count_objects(fin_container):
    count=0
    if isinstance(fin_container, dict):
        for k in fin_container:
            count += count_objects(fin_container[k])
    elif isinstance(fin_container, list) or isinstance(fin_container, set):
        for z in fin_container:
            count += count_objects(z)
    else:
        count = 1
        
    return count


class TestsGUI:
    def __init__(self, parent, part):
        self.parent = parent
        self.part = part
        
        self.tests = self.part.tests
        self.tests_other = self.tests["other"]
        self.tests_equal = self.tests["check_equal"]
        self.tests_secret = self.tests["check_secret"]
        
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=2, column=0, sticky=STICKY_ALL)
        self.frame.grid_columnconfigure(0, weight=1)

        number_of_tests = count_objects(self.tests)
        print("number_of_tests", number_of_tests)

        if number_of_tests > 10:
            # > scroled frame
            self.scroled_frame = ttk.Frame(self.frame)
            self.scroled_frame.grid(row=2, column=0, sticky=STICKY_ALL)
            self.scrollbar = ttk.Scrollbar(self.scroled_frame)
            self.scrollbar.grid(row=2, column=4, sticky=STICKY_ALL)
            self.canvas = tk.Canvas(self.scroled_frame, height=160, bd=0, highlightthickness=0)
            self.canvas['yscrollcommand']= self.scrollbar.set
            self.canvas.grid(row=2, column=2, sticky=STICKY_ALL)
            self.scrollbar.config(command=self.canvas.yview)

            self.canvas.xview_moveto(0)
            self.canvas.yview_moveto(0)

            self.frame_named = ttk.Frame(self.canvas)
            interior = self.frame_named
            interior_id = self.canvas.create_window(0, 0, window=interior, anchor=tk.NW)

            def _configure_interior(event):
                size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
                self.canvas.config(scrollregion="0 0 %s %s" % size)
                if interior.winfo_reqwidth() != self.canvas.winfo_width():
                    self.canvas.config(width=interior.winfo_reqwidth())
                    
            interior.bind('<Configure>', _configure_interior)

            def _configure_canvas(event):
                if interior.winfo_reqwidth() != self.canvas.winfo_width():
                    self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
                    
            self.canvas.bind('<Configure>', _configure_canvas)
            # < scroled frame
            
        else:
            self.frame_named = ttk.Frame(self.frame)
            self.frame_named.grid(row=2, column=0, sticky=STICKY_ALL)
        

        self.test_groups = []
        for i in range(len(self.tests_equal)):
            group_tests = self.tests_equal[i]
            test_group_frame = ttk.Frame(self.frame_named)
            a = 2+(i//3)
            b = 2*(i%3)+2
            test_group_frame.grid(row=a, column=b)
            test_group = TestGroup(
                test_group_frame,
                self.tests,
                "check_equal", i)
##            test_group = TestGroup(
##                test_group_frame,
##                "Check equal " + str(i+1),
##                group_tests,
##                group_type="equal")
            self.test_groups.append(test_group)

        n = len(self.tests_equal)
        for j in range(len(self.tests_secret)):
            i = n + j
            group_tests = self.tests_secret[j]
            test_group_frame = ttk.Frame(self.frame_named)
            a = 2+(i//3)
            b = 2*(i%3)+2
            test_group_frame.grid(row=a, column=b)
            test_group = TestGroup(
                test_group_frame,
                self.tests,
                "check_secret", j)
##            test_group = TestGroup(
##                test_group_frame,
##                "Check secret " + str(j+1),
##                group_tests,
##                group_type="secret")
            self.test_groups.append(test_group)
        
        self.equal_frent = FrEntGUI(self.frame, "Other tests", height=6, row=4)
        self.equal_entry = self.equal_frent.entry
        self.equal_entry.config(font=PROGRAM_STYLE)
        add_colors_to_text(self.equal_entry)

        self.add_context()


    def add_context(self):
        self.equal_entry.delete("1.0", "end")
        self.equal_entry.insert("1.0", self.tests_other)
        
class PartMenu:
    def __init__(self, partGUI):
        ## def __init__(self, partGUI, part=None):
        self.partGUI = partGUI
        self.parent = self.partGUI.parent

        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=2, column=2, sticky=STICKY_ALL)

        self.part_frame = ttk.Frame(self.frame)
        self.part_frame.grid(row=2, column=0, sticky=STICKY_ALL)

        self.part_label = ttk.Label(self.part_frame, text="Problem")
        self.part_label.grid(row=0, column=0, sticky=STICKY_ALL)

        self.add_new_part = ttk.Button(self.part_frame, text="Load file", command=self.load_file)
        self.add_new_part.grid(row=2, column=0, sticky=STICKY_ALL)

        self.add_new_part = ttk.Button(self.part_frame, text="Save file", command=self.save_file)
        self.add_new_part.grid(row=4, column=0, sticky=STICKY_ALL)

        self.add_new_part = ttk.Button(self.part_frame, text="Save file as", command=self.save_file_as)
        self.add_new_part.grid(row=6, column=0, sticky=STICKY_ALL)

        self.add_new_part = ttk.Button(self.part_frame, text="Add new part", command=self.add_new_part_func)
        self.add_new_part.grid(row=8, column=0, sticky=STICKY_ALL)


        self.precode_frame = ttk.Frame(self.frame)
        self.precode_frame.grid(row=4, column=0, sticky=STICKY_ALL)

        self.part_label = ttk.Label(self.precode_frame, text="Description and code")
        self.part_label.grid(row=0, column=0, sticky=STICKY_ALL)

        self.description_precode_button = ttk.Button(self.precode_frame, text="Prc. to description", command=self.precode_to_description)
        #self.description_precode_button = ttk.Button(self.precode_frame, text="Prc. to desc.", command=self.precode_to_description)
        self.description_precode_button.grid(row=2, column=0, sticky=STICKY_ALL)

        self.test_frame = ttk.Frame(self.frame)
        self.test_frame.grid(row=6, column=0, sticky=STICKY_ALL)

        self.test_label = ttk.Label(self.test_frame, text="Test")
        self.test_label.grid(row=0, column=0, sticky=STICKY_ALL)

        self.create_group_button = ttk.Button(self.test_frame, text="Create group", command=self.create_group)
        self.create_group_button.grid(row=10, column=0, sticky=STICKY_ALL)

        self.create_test_button = ttk.Button(self.test_frame, text="Create t. eq.", command=self.create_test)
        self.create_test_button.grid(row=12, column=0, sticky=STICKY_ALL)

        self.chose_test_group_button = ttk.Button(self.test_frame, text="Change t. gr.", command=self.change_test_group)
        self.chose_test_group_button.grid(row=14, column=0, sticky=STICKY_ALL)

        self.switch_button = ttk.Button(self.test_frame, text="Switch test/group", command=self.switch_action)
        self.switch_button.grid(row=16, column=0, sticky=STICKY_ALL)
        
        self.remove_tests_button = ttk.Button(self.test_frame, text="Remove tests", command=self.remove_tests)
        self.remove_tests_button.grid(row=18, column=0, sticky=STICKY_ALL)

        self.to_secret_button = ttk.Button(self.test_frame, text="Gr. to secret", command=self.convert_to_secret)
        self.to_secret_button.grid(row=20, column=0, sticky=STICKY_ALL)
        
        #self.chose_from_group = ttk.Button(self.test_frame, text="Con. to equal", command=self.select_from_groups)
        #self.chose_from_group.grid(row=22, column=0, sticky=STICKY_ALL)

        self.description_tests_button = ttk.Button(self.test_frame, text="To description", command=self.tests_to_description)
        self.description_tests_button.grid(row=24, column=0, sticky=STICKY_ALL)

        #self.expand_secret = ttk.Button(self.test_frame, text="Expand secret", command=self.expand_secret)
        #self.expand_secret.grid(row=26, column=0, sticky=STICKY_ALL)

    def remove_tests(self):
        self.partGUI.remove_chosen_tests()

    def tests_to_description(self):
        self.partGUI.add_chosen_tests_to_description()

    def precode_to_description(self):
        self.partGUI.add_precode_to_description()

    def add_new_part_func(self):
        self.partGUI.add_new_part(i=self.partGUI.i)

    def load_file(self):
        self.partGUI.gui.command_load()

    def save_file(self):
        self.partGUI.gui.command_save()

    def save_file_as(self):
        self.partGUI.gui.command_save_as()

    def select_from_groups(self):
        self.partGUI.gui.select_from_groups()

    def create_group(self):
        self.partGUI.create_group()

    def create_test(self):
        self.partGUI.create_test()

    def change_test_group(self):
        self.partGUI.change_test_group()

    def switch_action(self):
        self.partGUI.switch_action()

    def convert_to_secret(self):
        self.partGUI.convert_to_secret()


##    def expand_secret(self):
##        pass


    

class PartGUI:
    def __init__(self, gui, parent, i=-1):
        self.parent = parent
        self.gui = gui
        self.problem = self.gui.curent_problem
        self.part = self.problem.parts[i] if i >= 0 else None
        self.i = i
        
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=2, column=0, sticky=STICKY_ALL)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        if self.part is None:
            try:
                ## self.part = self.load_default_part()
                self.new_part_button = ttk.Button(self.frame, text="Add new part", command=self.add_new_part)
                self.new_part_button.grid(row=2, column=0, sticky=STICKY_ALL)
                return
            except:
                return
        
        self.part_menu = PartMenu(self)
        
        self.desc_frent = FrEntGUI(self.frame, "Part description", height=6, row=4)
        self.desc_entry = self.desc_frent.entry
        self.desc_entry.config(font=TITLE_STYLE)
        self.add_update_action(self.desc_entry, "part_description")
        
        self.prec_frent = FrEntGUI(self.frame, "Precode", height=6, row=6)
        self.prec_entry = self.prec_frent.entry
        self.prec_entry.config(font=PROGRAM_STYLE)
        add_colors_to_text(self.prec_entry)
        self.add_update_action(self.prec_entry, "part_precode")
        
        self.solut_frent = FrEntGUI(self.frame, "Solution", height=12, row=8)
        self.solut_entry = self.solut_frent.entry
        self.solut_entry.config(font=PROGRAM_STYLE)
        add_colors_to_text(self.solut_entry)
        self.add_update_action(self.solut_entry, "part_solution")

        self.frame.bind('<Control-Key-r>', self.remove_chosen_tests)
        self.frame.bind('<Control-Key-R>', self.remove_chosen_tests)
        self.frame.bind('<Key-r>', self.remove_chosen_tests)
        self.frame.bind('<Key-R>', self.remove_chosen_tests)
        self.frame.bind('<Enter>', lambda e: print("ENTER"))
        self.frame.bind('<Key-a>', lambda e: print("a"))
        self.frame.bind('<Key-A>', lambda e: print("A"))

        self.add_context()
        self.define_bind_methods()
        self.make_tests_frame()

    def make_tests_frame(self):
        self.tests_frame = ttk.Frame(self.frame)
        self.tests_frame.grid(row=10, column=0, sticky=STICKY_ALL)
        self.tests_frame.grid_columnconfigure(0, weight=1)    

        self.test_gui = TestsGUI(self.tests_frame, self.part)
        if self.part != None:
            self.test_gui.add_context()

        
    def add_context(self):
        if self.part != None:
            self.desc_entry.delete("1.0", "end")
            self.desc_entry.insert("1.0", self.part.description)

            self.prec_entry.delete("1.0", "end")
            self.prec_entry.insert("1.0", self.part.precode)

            self.solut_entry.delete("1.0", "end")
            self.solut_entry.insert("1.0", self.part.solution)


    def add_new_part(self, event=None, i=-1):
        self.problem.new_problem_part()
        if i>=0:
            parts = self.problem.parts
            parts.insert(i, parts[-1])
            parts.pop()
        self.gui.redefine_notebook()

##    @staticmethod
##    def load_default_part():
##        return ProblemPart.load_file("parameters/default_part.py")


    def update_field(self, field_name, entry):
        field_data = entry.get("1.0", "end")
        if field_name == "part_description":
            self.part.description = field_data
        elif field_name == "part_precode":
            self.part.precode = field_data
        elif field_name == "part_solution":
            self.part.solution = field_data

        print("update_field", field_name)


    def add_update_action(self, entry, field_name):
        def update_field(event):
            self.update_field(field_name, entry)
            
        entry.bind('<Enter>', update_field)
        entry.bind('<Leave>', update_field)
        entry.bind('<Return>', update_field)

    def save_all(self):
        self.update_field(self.desc_entry, "part_description")
        self.update_field(self.prec_entry, "part_precode")
        self.update_field(self.solut_entry, "part_solution")

    def define_bind_methods(self):
        self.frame.bind('<Control-Key-r>', self.remove_chosen_tests)
        self.frame.bind('<Control-Key-R>', self.remove_chosen_tests)

    def remove_chosen_tests(self, event=None):
        for test_group in self.test_gui.test_groups:
            if test_group.chosen:
                print("remove test group", test_group.group_type, i)
                del self.tests[test_group.group_type][test_group.group_num]
                    
            for test_frame in test_group.test_frames:
                if test_frame.chosen:
                    print("remove", test_frame.test)
                    self.part.remove_test(test_frame.test)


        del self.tests_frame
        self.make_tests_frame()

        
    def create_group(self):
        self.part.tests["check_equal"].append([CheckEqual("Input", "Output")])
        del self.tests_frame
        self.make_tests_frame()


    def create_test(self):
        for i, test_group in enumerate(self.test_gui.test_groups):
            if test_group.chosen:
                if test_group.group_type == "check_equal":
                    self.part.tests["check_equal"][test_group.group_num].append(CheckEqual("Input", "Output"))

                elif test_group.group_type == "check_secret":
                    self.part.tests["check_secret"][test_group.group_num].append(CheckSecret("Input", "Msg."))

        del self.tests_frame
        self.make_tests_frame()


    def convert_to_secret(self):
        for i, test_group in enumerate(self.test_gui.test_groups):
            if test_group.chosen:
                if test_group.group_type == "check_equal":
                    tests = self.part.tests["check_equal"].pop(i)
                    new_tests = [z.to_secret() for z in tests]

        self.part.tests["check_secret"].append(new_tests)


        del self.tests_frame
        self.make_tests_frame()


    def change_test_group(self):
        for i, test_group in enumerate(self.test_gui.test_groups):
            if test_group.chosen:
                tests = self.part.tests[test_group.group_type]
                a = i
                b = test_group.group_type
                break

        for i, test_group in enumerate(self.test_gui.test_groups):
            if a != i and b == test_group.group_type:
                for test_frame in test_group.test_frames:
                    if test_frame.chosen:
                        self.part.remove_test(test_frame.test)
                        tests[a].append(test_frame.test)
                        
        del self.tests_frame
        self.make_tests_frame()


    def switch_action(self):
        count = 0
        for i, test_group in enumerate(self.test_gui.test_groups):
            if test_group.chosen:
                tests = self.part.tests[test_group.group_type]
                count += 1
                if count == 2:
                    if test_group.group_type != b:
                        return
                    tests[a], tests[i] = tests[i], tests[a]

                    del self.tests_frame
                    self.make_tests_frame()
                    return
                
                a = i
                b = test_group.group_type


        count = 0
        for i, test_group in enumerate(self.test_gui.test_groups):
            for test_frame in test_group.test_frames:
                if test_frame.chosen:
                    count += 1
                    if count == 2:
                        self.part.switch_tests(test1, test_frame.test)
                    test1 = test_frame.test

        del self.tests_frame
        self.make_tests_frame()
            
     

    def add_chosen_tests_to_description(self, event=None):
        chosen_tests = []
        for test_group in self.test_gui.test_groups:
            for test_frame in test_group.test_frames:
                if test_frame.chosen:
                    chosen_tests.append(test_frame.test)

        self.part.check_equals_to_description(chosen_tests)

        del self.tests_frame
        self.make_tests_frame()
        self.add_context()


    def add_precode_to_description(self, event=None):
        self.part.precode_to_description()
        self.add_context()

    
        
        

class ProblemGUI:
    def __init__(self, parent, problem):
        self.parent = parent
        self.problem = problem
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=2, column=0, sticky=STICKY_ALL)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)

        self.title_frent = FrEntGUI(self.frame, "Problem title", height=1, row=2)
        self.title_entry = self.title_frent.entry
        self.title_entry.config(font=TITLE_STYLE)
        self.add_update_action(self.title_entry, "problem_title")
        
        self.desc_frent = FrEntGUI(self.frame, "Problem description", height=None, row=4)
        self.desc_entry = self.desc_frent.entry
        self.desc_entry.config(font=TITLE_STYLE)
        self.add_update_action(self.desc_entry, "problem_description")

        self.add_context()

    def add_context(self):
        if self.problem != None:
            self.title_entry.delete("1.0", "end")
            self.title_entry.insert("1.0", self.problem.title)
            
            self.desc_entry.delete("1.0", "end")
            self.desc_entry.insert("1.0", self.problem.description)

    def update_field(self, field_name, entry):
        field_data = entry.get("1.0", "end")
        if field_name == "problem_title":
            self.problem.title = field_data
        elif field_name == "problem_description":
            self.problem.description = field_data

        print("update_field", field_name)

    def add_update_action(self, entry, field_name):
        def update_field(event):
            self.update_field(field_name, entry)
            
        entry.bind('<Enter>', update_field)
        entry.bind('<Leave>', update_field)
        entry.bind('<Return>', update_field)

    def save_all(self):
        self.update_field(self.title_entry, "problem_title")
        self.update_field(self.desc_entry, "problem_description")
        for part in problem.parts:
            part.save_all()


class PrototypeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ProNal PrototypeGUI")
        # self.root.option_add('*tearOff', False)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # fileMenu = tk.Menu(self.root, tearoff=False)
        # fileMenu.add_cascade(label="File",underline=0, menu=fileMenu)

        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, sticky=STICKY_ALL)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)

        self.curent_problem = None

        self.notebook = None
        self.problem_parts = []

        self.root.bind("<Control-Key-l>", self.command_load)
        self.root.bind("<Control-Key-L>", self.command_load)
        self.root.bind("<Control-Key-s>", self.command_save)
        self.root.bind("<Control-Key-S>", self.command_save)
        self.root.bind("<Control-Shift-KeyPress-s>", self.command_save_as)
        self.root.bind("<Control-Shift-KeyPress-S>", self.command_save_as)

        self.command_load()
        if self.curent_problem is None:
            print("Last chanse for valid file choice.")
            self.command_load()

        if self.curent_problem is None:
            self.quit()
            
        # self.redefine_notebook()

    def quit(self):
        self.root.destroy()

    def redefine_notebook(self):
        if self.notebook is not None:
            self.notebook.destroy()
            
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.grid(row=2, column=0, sticky=STICKY_ALL)

        self.problem_frame = tk.Frame(self.notebook)
        self.notebook.add(self.problem_frame, text="Problem")
        self.problem_frame.grid_columnconfigure(0, weight=1)
        self.problem_frame.grid_rowconfigure(2, weight=1)
        self.problemGUI = ProblemGUI(self.problem_frame, self.curent_problem)
        
        for i in range(len(self.problem_parts)):
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Part "+str(i+1))
            frame.grid_columnconfigure(0, weight=1)
            PartGUI(self, frame, i)

        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="New part")
        frame.grid_columnconfigure(0, weight=1)
        PartGUI(self, frame)

    def command_load(self, event=None):
        filetypes=(("Python files", "*.py"),
                   ("Text files", "*.txt"),
                   ("All files", "*.*") )
        self.file_name = filedialog.askopenfilename(filetypes=filetypes)

        try:
            self.curent_problem = Problem.load_file(self.file_name)
            self.problem_parts = self.curent_problem.parts
            print("Load done.")
        except:
            self.curent_problem = None
            print("Not a valid problem file.")
            return

        self.redefine_notebook()

    def command_save(self, file=None):
        if file==None:
            file = self.file_name

        print("writing on file", file)
        self.curent_problem.write_on_file(file)

    def command_save_as(self, event=None):
        file = filedialog.asksaveasfilename()
        self.command_save(file)

            


def main():
    root = tk.Tk()
    prototype = PrototypeGUI(root)
    root.mainloop()
    #input("Press ENTER to save.")
    #prototype.command_save(prototype.file_name.replace("_in", "").strip(".py") + "_out.py")

if __name__ == "__main__":
    main()
