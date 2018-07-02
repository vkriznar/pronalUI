from tkinter import *

def vmesnik():
    
    root = Tk()
    
    w = 770 # width for the Tk root
    h = 800 # height for the Tk root
    
    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    
    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    
    # set the dimensions of the screen and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #root.geometry("840x600") #širina, višina
    
    def napisi_naslov():
        data_naslov = text_naslov.get("1.0", 'end')
        data_opis=text_opis.get("1.0", 'end')
        data_resitev = text_resitev.get("1.0", 'end')
        data_testi=text_testi.get("1.0", 'end')
        
        with open("naslov.txt", "w") as f:
            f.write(data_naslov)
        with open("opis.txt", "w") as f:
            f.write(data_opis)
        with open("resitev.txt", "w") as f:
            f.write(data_resitev)
        with open("testi.txt", "w") as f:
            f.write(data_testi)
            
        root.destroy()



    ## narejeno isto kot spodaj, le da z grid
    """
    Label(root, text="Dodaj nalogo", font='Helvetica 14 bold').grid(row=0)
    separator = Frame(height=2, bd=1, relief=SUNKEN)
    separator.grid(row=1, sticky="we")

    # okno za naslov naloge
    Label(root, text="Naslov naloge",font='Helvetica 12').grid(row=2)
    text_naslov = Text(root, width=80, height=8, bg='white')
    text_naslov.grid(row=3)

    # okno za opis naloge
    Label(root, text="Opis naloge", font='Helvetica 12').grid(row=4)
    text_opis = Text(root, width=80, height=8, bg='white', bd=5, relief=SUNKEN)
    text_opis.grid(row=5, sticky="we")

    # okno za rešitev naloge
    Label(root, text="Rešitev naloge", font='Helvetica 12').grid(row=6)
    text_resitev = Text(root, width=80, height=8, bg='white', bd=5, relief=SUNKEN)
    text_resitev.grid(row=7, sticky="we")

    # okno za teste
    Label(root, text="Testi", font='Helvetica 12').grid(row=8)
    text_testi = Text(root, width=80, height=8, bg='white', bd=5, relief=SUNKEN)
    text_testi.grid(row=9, sticky="we")

    gumb_preklici = Button(root, text="prekliči", command=root.destroy, height=1, width=8, relief=RAISED, font='Helvetica 12')
    gumb_preklici.grid(row=10, sticky="e")
    
    gumb_dodaj = Button(root, text="dodaj", command=napisi_naslov)
    gumb_dodaj.grid(row=10)
    """

    
    ## narejeno isto kot zgoraj, le da s pack
    Label(root, text="Dodaj nalogo", font='Helvetica 14 bold').pack(anchor=W, padx=25)
    separator = Frame(height=2, bd=1, relief=SUNKEN)
    separator.pack(fill=X)

    # okno za naslov naloge
    Label(root, text="Naslov naloge",font='Helvetica 12').pack(anchor=W, padx=25)
    text_naslov = Text(root, width=90, height= 2, bg='white', bd=5, relief=SUNKEN)

    # okno za opis naloge
    # v = StringVar(root, value='default text')
    # text_naslov.insert('end', "naslov")
    text_naslov.pack()
    # text_naslov.config(foreground="green")
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
    
    gumb_preklici = Button(root, text="prekliči", command=root.destroy, height=1, width=8, relief=RAISED, font='Helvetica 12')
    gumb_preklici.pack(side=RIGHT, padx=25)
    
    gumb_dodaj = Button(root, text="dodaj", command=napisi_naslov, height=1, width=8, relief=RAISED, bg="royalblue", font='Helvetica 12')
    gumb_dodaj.pack(side=RIGHT)
    
    root.mainloop()

vmesnik()
