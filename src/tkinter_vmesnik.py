from tkinter import *
stevec=1


def sklop():
    root = Tk()
    
    w = 770 # width for the Tk root
    h = 600 # height for the Tk root
    
    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    
    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    
    # set the dimensions of the screen and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #root.geometry("840x600") #širina, višina

    def napisi_vsebino_na_dat():
        data_naslov = text_naslov.get("1.0", 'end')
        data_opis=text_opis.get("1.0", 'end')
        
        with open("Sklop_naslov.txt".format(stevec), "w") as f:
            f.write(data_naslov)
        with open("Sklop_opis.txt".format(stevec), "w") as f:
            f.write(data_opis)

    def naprej_na_dodajanje_nalog():
        naloga()
    
    Label(root, text="Dodaj Sklop", font='Helvetica 14 bold').pack(anchor=W, padx=25)
    separator = Frame(height=2, bd=1, relief=SUNKEN)
    separator.pack(fill=X)

    # okno za naslov naloge
    Label(root, text="Naslov sklopa",font='Helvetica 12').pack(anchor=W, padx=25)
    text_naslov = Text(root, width=90, height= 2, bg='white', bd=5, relief=SUNKEN)
    # v = StringVar(root, value='default text')         ## na ta način v okno dodaš default text
    # text_naslov.insert('end', "naslov")               ## na ta način v okno dodaš default text
    text_naslov.pack()
    # text_naslov.config(foreground="green")            ## na ta način nastaviš barvo default texta

    # okno za opis naloge
    Label(root, text="Opis sklopa", font='Helvetica 12').pack(anchor=W, padx=25)
    text_opis = Text(root, width=90, height= 10, bg='white', bd=5, relief=SUNKEN)
    text_opis.pack()

    
    gumb_dodaj_sklop = Button(root, text="dodaj sklop", command=napisi_vsebino_na_dat, height=1, width=10, relief=RAISED, bg="royalblue", font='Helvetica 14')
    gumb_dodaj_sklop.pack(side=LEFT)
    
    gumb_naprej_na_dodajanje_nalog = Button(root, text="naprej na dodajanje nalog", command=naprej_na_dodajanje_nalog, height=1, width=22, relief=RAISED, bg="red", font='Helvetica 14')
    gumb_naprej_na_dodajanje_nalog.pack(side=LEFT, padx=10)
    
    

    gumb_zapri_okno = Button(root, text="zapri okno", command=root.destroy, height=1, width=10, relief=RAISED, font='Helvetica 14')
    gumb_zapri_okno.pack(side=RIGHT)

    

    
    
def naloga():
    global stevec
    
    
    
    root = Tk()
    
    w = 770 # width for the Tk root
    h = 750 # height for the Tk root
    
    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    
    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    
    # set the dimensions of the screen and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #root.geometry("840x600") #širina, višina
    
    def napisi_vsebino_na_dat():
        data_naslov = text_naslov.get("1.0", 'end')
        data_opis=text_opis.get("1.0", 'end')
        data_resitev = text_resitev.get("1.0", 'end')
        data_testi=text_testi.get("1.0", 'end')
        
        with open("Naloga{0}_naslov.txt".format(stevec), "w") as f:
            f.write(data_naslov)
        with open("Naloga{0}_opis.txt".format(stevec), "w") as f:
            f.write(data_opis)
        with open("Naloga{0}_resitev.txt".format(stevec), "w") as f:
            f.write(data_resitev)
        with open("Naloga{0}_testi.txt".format(stevec), "w") as f:
            f.write(data_testi)
        
    def naslednja_naloga():
        global stevec
        stevec+=1
        naloga()
        

    Label(root, text="Dodaj nalogo {0}".format(stevec), font='Helvetica 14 bold').pack(anchor=W, padx=25)
    separator = Frame(height=2, bd=1, relief=SUNKEN)
    separator.pack(fill=X)

    # okno za naslov naloge
    Label(root, text="Naslov naloge",font='Helvetica 12').pack(anchor=W, padx=25)
    text_naslov = Text(root, width=90, height= 2, bg='white', bd=5, relief=SUNKEN)
    # v = StringVar(root, value='default text')         ## na ta način v okno dodaš default text
    # text_naslov.insert('end', "naslov")               ## na ta način v okno dodaš default text
    text_naslov.pack()
    # text_naslov.config(foreground="green")            ## na ta način nastaviš barvo default texta

    # okno za opis naloge
    Label(root, text="Opis naloge", font='Helvetica 12').pack(anchor=W, padx=25)
    text_opis = Text(root, width=90, height= 10, bg='white', bd=5, relief=SUNKEN)
    text_opis.pack()

    # okno za rešitev naloge
    Label(root, text="Rešitev naloge", font='Helvetica 12').pack(anchor=W, padx=25)
    text_resitev = Text(root, width=90, height= 10, bg='white', bd=5, relief=SUNKEN)
    text_resitev.pack()

    # okno za teste
    Label(root, text="Testi", font='Helvetica 12').pack(anchor=W, padx=25)
    text_testi = Text(root, width=90, height= 10, bg='white', bd=5, relief=SUNKEN)
    text_testi.pack()

    gumb_dodaj = Button(root, text="dodaj nalogo", command=napisi_vsebino_na_dat, height=1, width=10, relief=RAISED, bg="royalblue", font='Helvetica 14')
    gumb_dodaj.pack(side=LEFT)

    gumb_naslednja_naloga = Button(root, text="ustvari naslednjo nalogo", command=naslednja_naloga, height=1, width=20, relief=RAISED, bg="red", font='Helvetica 14')
    gumb_naslednja_naloga.pack(side=LEFT, padx=10)
    
    gumb_zapri_okno = Button(root, text="zapri okno", command=root.destroy, height=1, width=10, relief=RAISED, font='Helvetica 14')
    gumb_zapri_okno.pack(side=RIGHT)

    
    
    

    
    
    root.mainloop()
sklop()
#naloga()
