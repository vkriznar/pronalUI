import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from Problem import Problem
from ProblemPart import ProblemPart


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


class ActionsToWidget:
    def __init__(self, widget, widget_type=None, text_var=""):
        self.widget = widget
        self.widget.bind("<FocusOut>", self.on_focus_out)
        self.widget.bind("<FocusIn>", self.on_focus_in)

        if "test_entry" in widget_type:
            self.widget.config(fg = "grey")
            self.widget.delete(0, "end")
            self.on_focus_out = self.on_focus_out_entry
            self.on_focus_in = self.on_focus_in_entry
            
            if widget_type == "test_entry_input":
                self.widget.insert(0, "input")
                self.default_text = "input"

            #elif widget_type="test_entry_output":
            else:
                self.widget.insert(0, "output")
                self.default_text = "output"

    def on_focus_out(self, event):
        pass

    def on_focus_in(self, event):
        pass

    def on_focus_out_entry(self, event):
        print("as")
        if text_var.get() == "":
            self.widget.insert(0, self.default_text)
            self.widget.config(fg = 'grey')
        

    def on_focus_in_entry(self, event):
        print("safaf")
        if text_var.get() == "":
            self.widget.delete(0, "end")
            self.widget.insert(0, "")

        self.widget.config(fg = "black")
    

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

        self.input_entry = ttk.Entry(self.frame)
        #self.input_str = tk.StringVar()
        #self.input_entry = ttk.Entry(self.frame, textvariable=self.input_str)
        #self.input_entry = tk.Entry(self.frame, textvariable=self.input_str)
        #ActionsToWidget(self.input_entry, "test_entry_input", self.input_str)
        self.input_entry.grid(row=2, column=4, sticky=STICKY_ALL)


        self.output_entry = ttk.Entry(self.frame)
        #self.output_str = tk.StringVar()
        #self.output_entry = ttk.Entry(self.frame, textvariable=self.output_str)
        #self.output_entry = tk.Entry(self.frame, textvariable=self.output_str)
        #ActionsToWidget(self.output_entry, "test_entry_output", self.output_str)
        self.output_entry.grid(row=2, column=6, sticky=STICKY_ALL)


        self.input_entry.delete(0,'end') 
        self.output_entry.delete(0,'end') 
        self.input_entry.insert(0, test.expression)
        self.output_entry.insert(0, test.output)

    def flip_chosen(self, event=None):
        self.chosen = not self.chosen
        print("flip_chosen", self.chosen)


class TestSecretFrame:
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

        # self.input_str = tk.StringVar()
        # self.input_entry = ttk.Entry(self.frame, textvariable=self.input_str)
        self.input_entry = ttk.Entry(self.frame)
        self.input_entry.grid(row=2, column=4, sticky=STICKY_ALL)

        self.input_entry.delete(0,'end') 
        self.input_entry.insert(0, test.expression)

    def flip_chosen(self, event=None):
        self.chosen = not self.chosen
        print("flip_chosen", self.chosen)


class TestGroup:
    def __init__(self, parent, group_name, group_tests, group_type="equal"):
        self.parent = parent
        self.label_frame = ttk.Labelframe(self.parent, text=group_name)
        self.label_frame.grid(row=2, column=0, sticky=STICKY_ALL)

        self.test_frames = []
        if group_type=="equal":
            self.label = ttk.Label(self.label_frame, text="Check.equal(input, output)")
            self.label.grid(row=0, column=0, sticky=STICKY_ALL)
            
            for i in range(len(group_tests)):
                test_frame = TestEqualFrame(self.label_frame, 2*i+2, group_tests[i])
                self.test_frames.append(test_frame)
                # test_frame.input_entry.set(group_tests[i].expression)
                # test_frame.output_entry.set(group_tests[i].output)
                #test_frame.input_entry.delete(0,'end') 
                #test_frame.output_entry.delete(0,'end') 
                #test_frame.input_entry.insert(0, group_tests[i].expression)
                #test_frame.output_entry.insert(0, group_tests[i].output)

        if group_type=="secret":
            self.label = ttk.Label(self.label_frame, text="Check.secret(input)")
            self.label.grid(row=0, column=0, sticky=STICKY_ALL)
            for i in range(len(group_tests)):
                test_frame = TestSecretFrame(self.label_frame, 2*i+2, group_tests[i][0])
                self.test_frames.append(test_frame)
                # test_frame.input_entry.set(group_tests[i][0].expression)
                #test_frame.input_entry.delete(0,'end')
                # test_frame.input_entry.insert(0, group_tests[i][0].expression)

        
            

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

        self.frame_named = ttk.Frame(self.frame)
        self.frame_named.grid(row=2, column=0, sticky=STICKY_ALL)


        self.test_groups = []
        i = 0
        #print("TESTS")
        #print(self.tests_equal)
        #print(self.tests_secret)
        for i in range(len(self.tests_equal)):
            group_tests = self.tests_equal[i]
            test_group_frame = ttk.Frame(self.frame_named)
            test_group_frame.grid(row=2, column=2*i+2)
            test_group = TestGroup(
                test_group_frame,
                "Check equal " + str(i+1),
                group_tests,
                group_type="equal")
            self.test_groups.append(test_group)

        if len(self.tests_secret) > 0:
            test_group_frame = ttk.Frame(self.frame_named)
            test_group_frame.grid(row=2, column=2*i+4)
            test_group = TestGroup(
                test_group_frame,
                "Check secret",
                self.tests_secret,
                group_type="secret")
            self.test_groups.append(test_group)
        
        self.equal_frent = FrEntGUI(self.frame, "Other tests", height=6, row=4)
        self.equal_entry = self.equal_frent.entry
        self.equal_entry.config(font=PROGRAM_STYLE)

        self.add_context()


    def add_context(self):
        self.equal_entry.delete("1.0", "end")
        self.equal_entry.insert("1.0", self.tests_other)
        
class PartMenu:
    def __init__(self, partGUI):
        self.partGUI = partGUI
        self.parent = self.partGUI.parent

        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=2, column=2, sticky=STICKY_ALL)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        
        self.remove_tests_button = ttk.Button(self.frame, text='Remove tests', command=self.remove_tests)
        self.remove_tests_button.grid(row=2, column=0, sticky=STICKY_ALL)

        self.description_tests_button = ttk.Button(self.frame, text='To description', command=self.tests_to_description)
        self.description_tests_button.grid(row=4, column=0, sticky=STICKY_ALL)

    def remove_tests(self):
        self.partGUI.remove_chosen_tests()

    def tests_to_description(self):
        self.partGUI.add_chosen_tests_to_description()
    

class PartGUI:
    def __init__(self, parent, part=None):
        self.parent = parent
        self.part = part
        self.part_menu = PartMenu(self)

        if self.part == None:
            try:
                self.part = self.load_default_part()
            except:
                return
        
        self.frame = ttk.Frame(self.parent)
        self.frame.grid(row=2, column=0, sticky=STICKY_ALL)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        
        self.desc_frent = FrEntGUI(self.frame, "Part description", height=6, row=4)
        self.desc_entry = self.desc_frent.entry
        self.desc_entry.config(font=TITLE_STYLE)
        self.add_update_action(self.desc_entry, "part_description")
        
        self.prec_frent = FrEntGUI(self.frame, "Precode", height=6, row=6)
        self.prec_entry = self.prec_frent.entry
        self.prec_entry.config(font=PROGRAM_STYLE)
        self.add_update_action(self.prec_entry, "part_precode")
        
        self.solut_frent = FrEntGUI(self.frame, "Solution", height=12, row=8)
        self.solut_entry = self.solut_frent.entry
        self.solut_entry.config(font=PROGRAM_STYLE)
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


    @staticmethod
    def load_default_part():
        return ProblemPart.load_file("parameters/default_part.py")


    def update_field(self, field_name, entry):
        field_data = entry.get('1.0', 'end')
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
        print("bla bla 123")
        for test_group in self.test_gui.test_groups:
            print("ahhaha")
            print(type(test_group))
            print(test_group.test_frames)
            for test_frame in test_group.test_frames:
                print("lalalal")
                if test_frame.chosen:
                    print("remove", test_frame.test)
                    self.part.remove_test(test_frame.test)


        del self.tests_frame
        self.make_tests_frame()

    def add_chosen_tests_to_description(self, event=None):
        print("bla bla 123")
        chosen_tests = []
        for test_group in self.test_gui.test_groups:
            for test_frame in test_group.test_frames:
                if test_frame.chosen:
                    chosen_tests.append(test_frame.test)

        self.part.check_equals_to_description(chosen_tests)

        del self.tests_frame
        self.make_tests_frame()
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
        field_data = entry.get('1.0', 'end')
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
        self.redefine_notebook()

    def redefine_notebook(self):
        if self.notebook is not None:
            self.notebook.destroy()
            
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.grid(row=2, column=0, sticky=STICKY_ALL)

        self.problem_frame = tk.Frame(self.notebook)
        self.notebook.add(self.problem_frame, text="Problem")
        self.problem_frame.grid_columnconfigure(0, weight=1)
        self.problem_frame.grid_rowconfigure(2, weight=1)
        self.problem_frame = ProblemGUI(self.problem_frame, self.curent_problem)
        
        for i in range(len(self.problem_parts)):
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Part "+str(i+1))
            frame.grid_columnconfigure(0, weight=1)
            PartGUI(frame, self.problem_parts[i])

        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="New part")
        frame.grid_columnconfigure(0, weight=1)
        PartGUI(frame)

    def command_load(self, event=None):
        self.file_name = filedialog.askopenfilename()

        # self.curent_problem = Problem.load_file(self.file_name)
        try:
            self.curent_problem = Problem.load_file(self.file_name)
            self.problem_parts = self.curent_problem.parts
            # print(self.curent_problem)
        except:
            self.curent_problem = None
            print("Not a valid problem file.")

        
        self.redefine_notebook()
        print("Load done.")

    def command_save(self, event=None, file=None):
        if file==None:
            file = self.file_name

        print("writing on file", file)
        self.curent_problem.write_on_file(file)
        
        # print("TODO command_save")

    def command_save_as(self, event):
        file = filedialog.asksaveasfilename()
        self.command_save()

            


def main():
    root = tk.Tk()
    prototype = PrototypeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
