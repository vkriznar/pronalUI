from tkinter import *

def okno_naloga():
    
    root = Tk()
    
    w = 1075 # width for the Tk root
    h = 690 # height for the Tk root
    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/6) - (h/6)
    # set the dimensions of the screen and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #root.geometry("840x600") #širina, višina
    
    def napisi_vsebino_na_dat():
        data_naslov = text_naslov.get("1.0", 'end')
        data_opis=text_opis.get("1.0", 'end')
        data_resitev = text_resitev.get("1.0", 'end')
        data_testi_ostali=text_testi_ostali.get("1.0", 'end')

        # check equal 1
        data_testi_check_equal_st1=text_testi_check_equal_st1.get("1.0", 'end')
        data_testi_check_equal_expression1=text_testi_check_equal_expression1.get("1.0", 'end')
        data_testi_check_equal_result1=text_testi_check_equal_result1.get("1.0", 'end')

        # check equal 2
        data_testi_check_equal_st2=text_testi_check_equal_st2.get("1.0", 'end')
        data_testi_check_equal_expression2=text_testi_check_equal_expression2.get("1.0", 'end')
        data_testi_check_equal_result2=text_testi_check_equal_result2.get("1.0", 'end')

        # check equal 3
        data_testi_check_equal_st3=text_testi_check_equal_st3.get("1.0", 'end')
        data_testi_check_equal_expression3=text_testi_check_equal_expression3.get("1.0", 'end')
        data_testi_check_equal_result3=text_testi_check_equal_result3.get("1.0", 'end')

        # check equal 4
        data_testi_check_equal_st4=text_testi_check_equal_st4.get("1.0", 'end')
        data_testi_check_equal_expression4=text_testi_check_equal_expression4.get("1.0", 'end')
        data_testi_check_equal_result4=text_testi_check_equal_result4.get("1.0", 'end')

        # check equal 5
        data_testi_check_equal_st5=text_testi_check_equal_st5.get("1.0", 'end')
        data_testi_check_equal_expression5=text_testi_check_equal_expression5.get("1.0", 'end')
        data_testi_check_equal_result5=text_testi_check_equal_result5.get("1.0", 'end')

        # check equal 6
        data_testi_check_equal_st6=text_testi_check_equal_st6.get("1.0", 'end')
        data_testi_check_equal_expression6=text_testi_check_equal_expression6.get("1.0", 'end')
        data_testi_check_equal_result6=text_testi_check_equal_result6.get("1.0", 'end')
        
        with open("Naloga_naslov.txt", "w") as f:
            f.write(data_naslov)
        with open("Naloga_opis.txt", "w") as f:
            f.write(data_opis)
        with open("Naloga_resitev.txt", "w") as f:
            f.write(data_resitev)
        with open("Naloga_testi_ostali.txt", "w") as f:
            f.write(data_testi_ostali)

        with open("Naloga_testi_equal_numbers.txt", "w") as f:
            f.write(data_testi_check_equal_st1)
            f.write("\n")
            f.write(data_testi_check_equal_st2)
            f.write("\n")
            f.write(data_testi_check_equal_st3)
            f.write("\n")
            f.write(data_testi_check_equal_st4)
            f.write("\n")
            f.write(data_testi_check_equal_st5)
            f.write("\n")
            f.write(data_testi_check_equal_st6)
        
        with open("Naloga_testi_equal_expressions.txt", "w") as f:
            f.write(data_testi_check_equal_expression1)
            f.write("\n")
            f.write(data_testi_check_equal_expression2)
            f.write("\n")
            f.write(data_testi_check_equal_expression3)
            f.write("\n")
            f.write(data_testi_check_equal_expression4)
            f.write("\n")
            f.write(data_testi_check_equal_expression5)
            f.write("\n")
            f.write(data_testi_check_equal_expression6)

        with open("Naloga_testi_equal_results.txt", "w") as f:
            f.write(data_testi_check_equal_result1)
            f.write("\n")
            f.write(data_testi_check_equal_result2)
            f.write("\n")
            f.write(data_testi_check_equal_result3)
            f.write("\n")
            f.write(data_testi_check_equal_result4)
            f.write("\n")
            f.write(data_testi_check_equal_result5)
            f.write("\n")
            f.write(data_testi_check_equal_result6)

    
    # text zapisan na vrhu okna
    Label(root, text="Dodaj nalogo", font='Helvetica 14 bold').grid(row=0, column=0, columnspan=6, sticky="w")
    # separator
    separator = Frame(height=2, bd=1, relief=SUNKEN)
    separator.grid(row=1, column=0, columnspan=6, sticky="we")

    # napis in okno za naslov naloge
    Label(root, text="Naslov naloge",font='Helvetica 12').grid(row=2, column=0, columnspan=6, sticky="w")
    text_naslov = Text(root, width=80, height=2, bg='white', bd=5, relief=SUNKEN)
    text_naslov.grid(row=3, column=0, columnspan=6, sticky="we")

    # napis in okno za opis naloge
    Label(root, text="Opis naloge", font='Helvetica 12').grid(row=4, column=0, columnspan=6, sticky="w")
    text_opis = Text(root, width=65, height=12, bg='white', bd=5, relief=SUNKEN)
    text_opis.grid(row=5, column=0, columnspan=3, sticky="w")

    # napis in okno za rešitev naloge
    Label(root, text="Rešitev naloge", font='Helvetica 12').grid(row=4, column=3, columnspan=6, sticky="w")
    text_resitev = Text(root, width=65, height=12, bg='white', bd=5, relief=SUNKEN)
    text_resitev.grid(row=5, column=3, columnspan=3, sticky="e")

    # napis za teste check equal
    Label(root, text="Testi check equal", font='Helvetica 12').grid(row=8, column=0, columnspan=3, sticky="w")

    # okno za check equal 1
    text_testi_check_equal_st1 = Text(root, width=4, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_st1.grid(row=9, column=0, sticky="w")

    text_testi_check_equal_expression1 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_expression1.grid(row=9, column=1, sticky="w")

    text_testi_check_equal_result1 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_result1.grid(row=9, column=2, sticky="w")

    # okno za check equal 2
    text_testi_check_equal_st2 = Text(root, width=4, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_st2.grid(row=10, column=0, sticky="w")

    text_testi_check_equal_expression2 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_expression2.grid(row=10, column=1, sticky="w")

    text_testi_check_equal_result2 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_result2.grid(row=10, column=2, sticky="w")

    # okno za check equal 3
    text_testi_check_equal_st3 = Text(root, width=4, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_st3.grid(row=11, column=0, sticky="w")

    text_testi_check_equal_expression3 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_expression3.grid(row=11, column=1, sticky="w")

    text_testi_check_equal_result3 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_result3.grid(row=11, column=2, sticky="w")

    # okno za check equal 4
    text_testi_check_equal_st4 = Text(root, width=4, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_st4.grid(row=12, column=0, sticky="w")

    text_testi_check_equal_expression4 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_expression4.grid(row=12, column=1, sticky="w")

    text_testi_check_equal_result4 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_result4.grid(row=12, column=2, sticky="w")

    # okno za check equal 5
    text_testi_check_equal_st5 = Text(root, width=4, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_st5.grid(row=13, column=0, sticky="w")

    text_testi_check_equal_expression5 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_expression5.grid(row=13, column=1, sticky="w")

    text_testi_check_equal_result5 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_result5.grid(row=13, column=2, sticky="w")

    # okno za check equal 6
    text_testi_check_equal_st6 = Text(root, width=4, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_st6.grid(row=14, column=0, sticky="w")

    text_testi_check_equal_expression6 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_expression6.grid(row=14, column=1, sticky="w")

    text_testi_check_equal_result6 = Text(root, width=29, height=2, bg='white', bd=5, relief=SUNKEN)
    text_testi_check_equal_result6.grid(row=14, column=2, sticky="w")

    # napis in okno za preostale teste
    Label(root, text="Ostali testi", font='Helvetica 12').grid(row=8, column=3, columnspan=3, sticky="w")
    text_testi_ostali = Text(root, width=65, height=17, bg='white', bd=5, relief=SUNKEN)# font='Helvetica 12')
    text_testi_ostali.grid(row=9, column=3, columnspan=3, rowspan=6, sticky="e")

    # gumbi
    gumb_zapri_okno = Button(root, text="zapri okno", command=root.destroy, height=1, width=20, relief=RAISED, font='Helvetica 14')
    gumb_zapri_okno.grid(row=15, column=5, columnspan=2, sticky="e")
    
    gumb_dodaj = Button(root, text="dodaj nalogo", command=napisi_vsebino_na_dat, height=1, width=20, relief=RAISED, font='Helvetica 14')
    gumb_dodaj.grid(row=15, column=3, columnspan=2, sticky="e")
    
    root.mainloop()

okno_naloga()
