ProNal
=================

Repozitorij za projekt ProNal v katerem bomo naredili uporabniški vmesnik za sestavljanje nalog v Pythonu.

Uporabniški vmestnik za urejanje Tomo datotek
=================

Navodila za uporabo
---------------

V nadaljevanju so navodila za uporabo spletnega in namiznega vmestnika za izdelavo 
edit.py Tomo datotek.

### Navodila za oznake znotraj opisa

Poznamo naslednje zelo uporabne oznake:
1. Matematični način: $ (znak dolar)
2. Programerski način: ´ (slo tipk: alt-gr-9)
3. Z uporabo vmestnika se lahko kodo v opis doda avtomatično, 
sicer uporabimo 4 presledke

### Navodila za pisanje rešitev in testov

Prepovedano je uporabljati:
1. Trojne enojne narekovaje (''')

TODO vzemi iz Tomo

### Navodila za uporabo spletnega vmestnika

Potek dela:
1. Naložite datoteko, ki jo želite urejati
2. Naredite spremembe na nalogi in jih shranite
3. Naredite spremembe na podnalogah in jih shranite
4. Oddajte nalogo

#### Nalaganje datotek na splet

Kliknite na gumb Izberite nalogo za urejanje in 
odprl se vam bo dialog za nalaganje datoteke na splet. 
Izberite datoteko, ki jo želite urejati (recimo datumi_edit.py).

#### Spreminjanje naloge (opis, osnovno besedilo)

##### Naslov

V sekciji naslov vnesite naslov naloge.
Idealno že naslov pove nekaj o vsebini naloge.

##### Opis

V opis dodajte daljše besedilo naloge, 
motivacijo za kaj se gre in po možnosti neko zgodbo.
Nakažite tudi osnovno vsebino, ki pove 
kakšne zahteve se v programerskem
delu naloge lahko pričakuje.
Za uporabo posebnih simbolov si oglejte sekcijo 
[Navodila za oznake znotraj opisa](#navodila-za-oznake-znotraj-opisa).

##### Pregled opisa

Oblikovno dodelan pregled opisa, ki ste ga napisali.

##### Shranjevanje

Po končanem spreminjanju naloge kliknite na gumb 
Shrani spremembe naslova in opisa.

##### Ustvarjanje nove podnaloge

Če želite ustvariti novo podnalogo pritisnite 
gumb Nova podanloga. Idealno bi moral gumb 
ustvariti nalogo na prvem mestu, kar pa za enkrat 
še ni implementirano. Spremembe postavitve naloge 
se lahko naredijo na koncu tudi ročno.

##### Oddaj nalogo

Oddaj nalogo na tem mestu pride malokrat v poštev 
razen, če ste naredili le popravke v naslovu in opisu, 
sicer morate še prej nadaljevati z 
poravljanjem nalog v zavihtkih.


#### Spreminjanje podnalog

##### Opis

V opis dodajte besedilo v katerem so navodila kakšen 
program mora reševalec v tem delu naloge napisati.
Za uporabo posebnih simbolov si oglejte sekcijo 
[Navodila za oznake znotraj opisa](#navodila-za-oznake-znotraj-opisa).

##### Pregled opisa

Oblikovno dodelan pregled opisa, ki ste ga napisali.

##### Pre-koda

Sem dodajte Python kodo, 
ki bo reševalcu že na začetku na voljo.
Ponavadi je ta del prazen, včasih pa se doda že 
delno rešena naloga ali pa kakšna uporabna pomožna funkcija.
Kadar je naloga tipa popravi kodo, sem dodate kodo, 
ki jo mora uporabnik popraviti ali dopolniti.

Če želite, da se koda pojavi v besedilu naloge pritisnite gumb
Pošlji Pre-kodo v opis. Včasih želite, da je koda na voljo le 
v opisu in ni že v naprej priravljena, v tem primeru 
po kliku izbrišite vsebino tega okna.

##### Rešitev

Sem dodate vašo rešitev naloge v obliki Python programa.
Poglejte še navodila pod Navodila za pisanje rešitev in testov.

##### Dodani testi - Check equal

V tem sklopu se vam pokažejo testi, 
za katere uporabnik dobi informacijo o rezultatu. 
Skupina označuje vrstni red izvedbe, 
najprej se izvede prvi test iz vsake skupine. 
Če eden izmed testov v skupini ni ispolnjen 
se ostali testi ne izvedejo.
Izraz je izraz, ki ga želite evalvirati 
(ponavadi klic vaše funkcije z nekimi argumeti), 
Razultat pa rezultat tega izraza.
Urejanje omogoča:
1. birsanje testa (x)
2. premik testa v besedilo naloge (rumena gor)
3. menjava testa ali skupine gor (zelena gor)
4. menjava testa ali skupine dol (zelena dol)

Dodatno je desno še številka, ki označuje vrstni red 
testa znotraj posamezne skupine testov.

##### Dodani testi - Check secret

Velja vse kot za Dodani testi - Check equal,
le da so to testi o katerih uporabnik ne dobi povratne 
informacije, kaj se je zmodtil, razen, če dodate 
Sporočilo, v katerem je lahko namig zakaj je prišlo do napake.
Ni tudi možnosti za premik testa v opis, 
saj test nima uradnega rezultata, ki bi ga lahko izkoristili za primer.

##### Dodajanje testov

Omogoča dodajanje testov Check equal in Check secret.
Check Equal - po solpcih so informacije:
1. skupina testa
2. izraz
3. rezultat
4. gumb za dodajanje testa

Check Secret - po solpcih so informacije:
1. skupina testa
2. izraz
3. sporočilo
4. gumb za dodajanje testa

Dodatna navodila za vse:
1. skupina testa: testi v isti skupini so vezani z and
2. izraz: brez zunanjih narekovajev
3. rezultat: brez zunanjih narekovajev (če rezultat niz ima normalno narekovaje)

Prepovedana je uporaba trojnih enojnih narekovajev (''').
Poglejte še navodila pod Navodila za pisanje rešitev in testov.

##### Preostali testi

Testi, ki niso standardne oblike so v skupini preostali testi. 
Tu se velikokrat napiše kakšen test, ki uporablja 
Check Secret in for zanko, da lahko za veliko primerov 
preverimo pravilnost rezultatov.
Omogoča še veliko dodatnih funkcionalnosti, ki 
so navedene v navodilih za uporabo sistema Tomo 
(prosojnice os sestavljanju testov; na primer preverjanje branja, pisanja).

##### Shrani spremembe

Po končanem spreminanju podnaloge pritisnite gumb 
Shrani spremembe v podnalogi, da se vnesene spremembe 
zapišejo v  sistem.

##### Izbriši podnalogo

Izbriše trenutno podnalogo iz sklopa te naloge.

##### Nova podnaloga

Ustvari novo podnalogo, privzeto se uporabi že 
v naprej pripravljena predloga, ki jo nato popravite.

##### Oddaj nalogo

Po končanem spreminju vseh nalog shranite vse naloge in 
jih oddajte z pritiskom na gumb Oddaj nalogo.

#### Oddaja naloge

Po končanem spreminjanju naloge in podnaloge je naloga 
v stanju kot jo želite. Shranite nalogo in podnaloge, 
ter jih oddajte s klikom na gumb Oddaj nalogo.

### Navodila za uporabo namiznega vmestnika (v angleščini)

#### Run Python program and chose file to edit

Run Python program with idle and chose file to upload 
in Open file dialog.

#### Problem

##### Problem title

Write the title of your problem.

##### Problem description

Write problem description; 
some motivation and overview 
of knowledge used in this problem.

#### Part

##### Part description

Description of what should be done in this problem part.

##### Precode

Code which will be available for students.

##### Solution

Your official solution of problem part.

##### Test section

Check equal an Check secret tests.
Test group and individual test 
can be chosen for manipulation (with use of buttons).
There are also other tests given in Python format.

#### New part

New part which was not yet added to problem. 
To add new part to problem press Add new part.

#### Buttons

##### Problem

###### Load file

Loads the problem_edit.py file.

###### Save file

Saves the chenges of editing into original file.

###### Save file as

Saves the chenges of editing into new file.

###### Add new part

##### Description and code

Adds new part to same number as curent problem part.

###### Precode to description

Adds precode to description.

##### Test

###### Create group

Creates new Check equal group with one empty test.

###### Create test equal

Creates test equal in chosen (by checkbox) test equal group.

###### Change test group

Moves chosen tests into chosen group.

###### Switch test or group

Switches the position of two groups 
or switches the position of two tests.

###### Remove tests

One of the most usefull functions.
Removes chosen tests or groups.

###### Group to secret

Transformes given check equal group of tests 
to check secret group of tests.

###### To description

Adds chosen test equal tests to description.


Navodila za programerje
---------------

1. Potrebno iti skozi kodo in odstraniti TODO.
2. Kako je z predogledom opisa? Želimo to imeti?
3. Nova podnaloga vedno ustvari nalogo na koncu, je to ok?
