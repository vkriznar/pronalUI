from tkinter import *
from Problem import Problem
from ProblemPart import ProblemPart, CheckEqual

st_naloge=1

def okno_sklop(file_name):
    root = Tk()

    with open(file_name + "_in.py", "r", encoding="utf-8") as f:
        file_string = f.read()
    global problem
    problem = Problem.parse(file_string)
    
    w = 740 # width for the Tk root
    h = 500 # height for the Tk root
    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/6) - (h/6)
    # set the dimensions of the screen and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #root.geometry("840x600") #širina, višina

    def napisi_vsebino_dat_na_vmesnik():
        global problem
        global st_naloge
        text_opis.insert('end', problem.description)
        text_naslov.insert('end', problem.title)
        

    def napisi_vsebino_vmesnika_na_dat():
        global problem
        global st_naloge
        lib_string_kopija=problem.lib_string # ker ga hočm zapisat na koncu in ne pri dodajanju trenutnega sklopa
        lib_string=""
        head_string=problem.head_string
        title = text_naslov.get("1.0", 'end')
        description=text_opis.get("1.0", 'end')
        parts_kopija=problem.parts#.copy()
        parts=[]
        problem=Problem(title, description, parts, lib_string, head_string)
        
        problem.write_on_file(file_name + "_out.py")
        problem.parts=parts_kopija
        problem.lib_string=lib_string_kopija

    def naprej_na_dodajanje_nalog():
        global problem
        global st_naloge
        okno_naloga()
        
    # text zapisan na vrhu okna
    Label(root, text="Dodaj Sklop", font='Helvetica 14 bold').grid(row=0, column=0, columnspan=3, sticky="w")
    # separator
    separator = Frame(height=2, bd=1, relief=SUNKEN)
    separator.grid(row=1, column=0, columnspan=3, sticky="we")

    # napis in okno za naslov naloge
    Label(root, text="Naslov sklopa",font='Helvetica 12').grid(row=2, column=0, columnspan=3, sticky="w")
    text_naslov = Text(root, width=90, height= 2, bg='white', bd=5, relief=SUNKEN)
    # v = StringVar(root, value='default text')         ## na ta način v okno dodaš default text
    # text_naslov.insert('end', "naslov")               ## na ta način v okno dodaš default text
    text_naslov.grid(row=3, column=0, columnspan=3, sticky="we")
    # text_naslov.config(foreground="green")            ## na ta način nastaviš barvo default texta

    # napis in okno za opis naloge
    Label(root, text="Opis sklopa", font='Helvetica 12').grid(row=4, column=0, columnspan=3, sticky="w")
    text_opis = Text(root, width=90, height=20, bg='white', bd=5, relief=SUNKEN)
    text_opis.grid(row=5, column=0, columnspan=3, sticky="we")

    napisi_vsebino_dat_na_vmesnik()

    # gumbi
    gumb_dodaj = Button(root, text="dodaj", command=napisi_vsebino_vmesnika_na_dat, height=1, width=10, relief=RAISED, font='Helvetica 14')
    gumb_dodaj.grid(row=6, column=0, sticky="w")
    
    gumb_naprej_na_dodajanje_nalog = Button(root, text="naprej na dodajanje nalog", command=naprej_na_dodajanje_nalog, height=1, width=22, relief=RAISED, font='Helvetica 14')
    gumb_naprej_na_dodajanje_nalog.grid(row=6, column=1, sticky="w")
    
    gumb_zapri_okno = Button(root, text="zapri okno", command=root.destroy, height=1, width=10, relief=RAISED, font='Helvetica 14')
    gumb_zapri_okno.grid(row=6, column=2, sticky="e")

    root.mainloop()
    

    
    
def okno_naloga():
    global st_naloge
    global problem
    root = Tk()

    if st_naloge-1>=len(problem.parts):
        problem.parts.append(ProblemPart(0, "", "", "", ""))
    #print("id:", problem.parts[st_naloge-1].part_id)
    
    w = 1075 # width for the Tk root
    h = 750 # height for the Tk root
    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/6) - (h/6)
    # set the dimensions of the screen and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #root.geometry("840x600") #širina, višina
    
    def napisi_vsebino_dat_na_vmesnik():
        global problem
        global st_naloge
        
        text_opis.insert('end', problem.parts[st_naloge-1].description)
        text_resitev.insert('end', problem.parts[st_naloge-1].solution)
        text_prekoda.insert('end', problem.parts[st_naloge-1].precode)
        
        check_equal_testi=problem.parts[st_naloge-1].tests['check_equal']
        #print(check_equal_testi)

        okna_check_equal=[(text_testi_check_equal_st1, text_testi_check_equal_expression1, text_testi_check_equal_output1),
                          (text_testi_check_equal_st2, text_testi_check_equal_expression2, text_testi_check_equal_output2),
                          (text_testi_check_equal_st3, text_testi_check_equal_expression3, text_testi_check_equal_output3),
                          (text_testi_check_equal_st4, text_testi_check_equal_expression4, text_testi_check_equal_output4),
                          (text_testi_check_equal_st5, text_testi_check_equal_expression5, text_testi_check_equal_output5),
                          (text_testi_check_equal_st6, text_testi_check_equal_expression6, text_testi_check_equal_output6)]
        
        equal_ki_ne_grejo_v_okna=[]
        equal_st_okna=0
        equal_st_testa=0
        for equal_test in range(0, len(check_equal_testi)):
            equal_st_testa+=1
            
            if len(check_equal_testi[equal_test])>1: # imamo povezavo z and
                if equal_st_okna-1+len(check_equal_testi[equal_test])>=len(okna_check_equal):
                    # zmanjkalo je check.equal oken za vse teste povezane z and
                    # da ne prekinem and povezave, vse check.equal povezane z and (če ne grejo vsi v posebna okenca) napišem pod ostale teste
                    for test in check_equal_testi[equal_test]:
                            if check_equal_testi[equal_test].index(test)==len(check_equal_testi[equal_test])-1:
                                text_testi_ostali.insert('end', str(test)+"\n")
                            else: text_testi_ostali.insert('end', str(test)+" and \ \n")
                    
                else:
                    for test in check_equal_testi[equal_test]:
                        okna_check_equal[equal_st_okna][0].insert("end", equal_st_testa)
                        okna_check_equal[equal_st_okna][1].insert("end", test.expression[3:-3] if test.expression[0]==test.expression[1] else test.expression[1:-1])
                        okna_check_equal[equal_st_okna][2].insert("end", test.output)
                        equal_st_okna+=1
                    
            else: # nimamo povezave z and
                test=check_equal_testi[equal_test][0]
                if equal_st_okna>=len(okna_check_equal): # zmanjako je check.equal oken, preostali check.equal testi gredo med ostale
                        text_testi_ostali.insert('end', str(test)+"\n")
                else:
                    okna_check_equal[equal_st_okna][0].insert("end", equal_st_testa)
                    okna_check_equal[equal_st_okna][1].insert("end", test.expression[3:-3] if test.expression[0]==test.expression[1] else test.expression[1:-1])
                    okna_check_equal[equal_st_okna][2].insert("end", test.output)
                    equal_st_okna+=1
                    
        text_testi_ostali.insert("end", "\n".join([" and \ \n".join([str(i) for i in sez]) for sez in problem.parts[st_naloge-1].tests['check_secret']]))
        text_testi_ostali.insert("end", "\n")        
        text_testi_ostali.insert("end", problem.parts[st_naloge-1].tests['other'])
        
    
    def napisi_vsebino_podnaloge_na_dat():
        global problem
        global st_naloge

        part_id=problem.parts[st_naloge-1].part_id
        description=text_opis.get("1.0", 'end')
        precode=text_prekoda.get("1.0", 'end')
        solution=text_resitev.get("1.0", 'end')

        tests = ProblemPart.parse_tests(text_testi_ostali.get("1.0", 'end'))
        #print("OSTALI:", tests)

        # teste v okni za check.equal je potrebno dodati k ostalim check.equal testom
        okna_check_equal=[(text_testi_check_equal_st1, text_testi_check_equal_expression1, text_testi_check_equal_output1),
                          (text_testi_check_equal_st2, text_testi_check_equal_expression2, text_testi_check_equal_output2),
                          (text_testi_check_equal_st3, text_testi_check_equal_expression3, text_testi_check_equal_output3),
                          (text_testi_check_equal_st4, text_testi_check_equal_expression4, text_testi_check_equal_output4),
                          (text_testi_check_equal_st5, text_testi_check_equal_expression5, text_testi_check_equal_output5),
                          (text_testi_check_equal_st6, text_testi_check_equal_expression6, text_testi_check_equal_output6)]
        
        okna_check_equal.reverse()
        inside_and_connection=False
        
        for equal_st_okna in range(1, len(okna_check_equal)+1):
            expression="'{0}'".format(okna_check_equal[equal_st_okna-1][1].get("1.0", 'end').strip())
            output=okna_check_equal[equal_st_okna-1][2].get("1.0", 'end').strip()
            #print(expression, output)
            if expression=="''": continue

            if equal_st_okna==len(okna_check_equal) and inside_and_connection==False:
                tests['check_equal'].insert(0, [CheckEqual(expression, output)])
                
            elif equal_st_okna==len(okna_check_equal) and inside_and_connection==True:
                check_equals_connected_with_and.insert(0, CheckEqual(expression, output))
                tests['check_equal'].insert(0, check_equals_connected_with_and)
            else:

                if inside_and_connection==False and okna_check_equal[equal_st_okna-1][0].get("1.0", 'end')==okna_check_equal[equal_st_okna][0].get("1.0", 'end'):
                    inside_and_connection=True
                    check_equals_connected_with_and=[CheckEqual(expression, output)]
                elif inside_and_connection==True and okna_check_equal[equal_st_okna-1][0].get("1.0", 'end')==okna_check_equal[equal_st_okna][0].get("1.0", 'end'):
                    check_equals_connected_with_and.insert(0, CheckEqual(expression, output))
                elif inside_and_connection==True and okna_check_equal[equal_st_okna-1][0].get("1.0", 'end')!=okna_check_equal[equal_st_okna][0].get("1.0", 'end'):
                    inside_and_connection=False
                    check_equals_connected_with_and.insert(0, CheckEqual(expression, output))
                    tests['check_equal'].insert(0, check_equals_connected_with_and)
                elif inside_and_connection==False and okna_check_equal[equal_st_okna-1][0].get("1.0", 'end')!=okna_check_equal[equal_st_okna][0].get("1.0", 'end'):
                    tests['check_equal'].insert(0, [CheckEqual(expression, output)])
                
   
        #print("VSI:", tests)

        problem_part=ProblemPart(part_id, description, precode, solution, tests)
        with open(file_name+'_out.py', "a", encoding="utf-8") as f:
            f.write(str(problem_part)+"\n")
        
    def naslednja_naloga(): # kle se more vsebina naslednje naloge napisat na vmesnik
        global st_naloge
        global problem
        st_naloge+=1
        root.destroy()
        okno_naloga()
                                  
    def napisi_lib_string_na_dat():
        global problem
        with open(file_name+'_out.py', "a", encoding="utf-8") as f:
            f.write("\n"+problem.lib_string)
        root.destroy()
                                  
        
    # text zapisan na vrhu okna
    Label(root, text="Dodaj nalogo {0}".format(st_naloge), font='Helvetica 14 bold').grid(row=0, column=0, columnspan=6, sticky="w")
    # separator
    separator = Frame(height=2, bd=1, relief=SUNKEN)
    separator.grid(row=1, column=0, columnspan=6, sticky="we")

    # napis in okno za opis naloge
    Label(root, text="Opis naloge",font='Helvetica 12').grid(row=2, column=0, columnspan=6, sticky="w")
    text_opis = Text(root, width=80, height=8, bg='white', bd=5, relief=SUNKEN)
    text_opis.grid(row=3, column=0, columnspan=6, sticky="we")

    # napis in okno za prekodo naloge
    Label(root, text="Prekoda naloge", font='Helvetica 12').grid(row=4, column=0, columnspan=6, sticky="w")
    text_prekoda = Text(root, width=65, height=10, bg='white', bd=5, relief=SUNKEN)
    text_prekoda.grid(row=5, column=0, columnspan=3, sticky="w")

    # napis in okno za rešitev naloge
    Label(root, text="Rešitev naloge", font='Helvetica 12').grid(row=4, column=3, columnspan=6, sticky="w")
    text_resitev = Text(root, width=65, height=10, bg='white', bd=5, relief=SUNKEN)
    text_resitev.grid(row=5, column=3, columnspan=3, sticky="e")

    # napis za teste check equal
    Label(root, text="Testi check equal", font='Helvetica 12').grid(row=8, column=0, columnspan=3, sticky="w")

    # okno za check equal 1
    text_testi_check_equal_st1 = Text(root, width=4, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_st1.grid(row=9, column=0, sticky="w")

    text_testi_check_equal_expression1 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_expression1.grid(row=9, column=1, sticky="w")

    text_testi_check_equal_output1 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_output1.grid(row=9, column=2, sticky="w")

    # okno za check equal 2
    text_testi_check_equal_st2 = Text(root, width=4, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_st2.grid(row=10, column=0, sticky="w")

    text_testi_check_equal_expression2 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_expression2.grid(row=10, column=1, sticky="w")

    text_testi_check_equal_output2 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_output2.grid(row=10, column=2, sticky="w")

    # okno za check equal 3
    text_testi_check_equal_st3 = Text(root, width=4, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_st3.grid(row=11, column=0, sticky="w")

    text_testi_check_equal_expression3 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_expression3.grid(row=11, column=1, sticky="w")

    text_testi_check_equal_output3 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_output3.grid(row=11, column=2, sticky="w")

    # okno za check equal 4
    text_testi_check_equal_st4 = Text(root, width=4, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_st4.grid(row=12, column=0, sticky="w")

    text_testi_check_equal_expression4 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_expression4.grid(row=12, column=1, sticky="w")

    text_testi_check_equal_output4 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_output4.grid(row=12, column=2, sticky="w")

    # okno za check equal 5
    text_testi_check_equal_st5 = Text(root, width=4, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_st5.grid(row=13, column=0, sticky="w")

    text_testi_check_equal_expression5 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_expression5.grid(row=13, column=1, sticky="w")

    text_testi_check_equal_output5 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_output5.grid(row=13, column=2, sticky="w")

    # okno za check equal 6
    text_testi_check_equal_st6 = Text(root, width=4, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_st6.grid(row=14, column=0, sticky="w")

    text_testi_check_equal_expression6 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_expression6.grid(row=14, column=1, sticky="w")

    text_testi_check_equal_output6 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_output6.grid(row=14, column=2, sticky="w")

    # napis in okno za preostale teste
    Label(root, text="Ostali testi", font='Helvetica 12').grid(row=8, column=3, columnspan=3, sticky="w")
    text_testi_ostali = Text(root, width=65, height=17, bg='white', bd=5, relief=SUNKEN)# font='Helvetica 12')
    text_testi_ostali.grid(row=9, column=3, columnspan=3, rowspan=6, sticky="e")

    if st_naloge-1<len(problem.parts): napisi_vsebino_dat_na_vmesnik()

    # gumbi
    
    gumb_dodaj = Button(root, text="dodaj nalogo", command=napisi_vsebino_podnaloge_na_dat, height=1, width=20, relief=RAISED, font='Helvetica 14')
    gumb_dodaj.grid(row=15, column=1, sticky="e")

    gumb_naslednja_naloga = Button(root, text="ustvari naslednjo nalogo", command=naslednja_naloga, height=1, width=20, relief=RAISED, font='Helvetica 14')
    gumb_naslednja_naloga.grid(row=15, column=2, sticky="e")
                                     
    gumb_dodaj_sklop = Button(root, text="dodaj celoten sklop", command=napisi_lib_string_na_dat, height=1, width=20, relief=RAISED, font='Helvetica 14')
    gumb_dodaj_sklop.grid(row=15, column=4, columnspan=1, sticky="e")

    gumb_zapri_okno = Button(root, text="zapri okno", command=root.destroy, height=1, width=20, relief=RAISED, font='Helvetica 14')
    gumb_zapri_okno.grid(row=15, column=5, columnspan=1, sticky="e")
    
    root.mainloop()

if __name__ == "__main__":
    file_name="../edit_files/naloga"
    okno_sklop(file_name)

