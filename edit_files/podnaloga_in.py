# =====================================================================@015027=
# Na spletni strani `https://www.ncbi.nlm.nih.gov/guide/howto/dwn-genome/`
# poišči genski zapis z oznako KT232076.1 in v obliki niza povej za
# katero vrsto bakterije gre.
# 
#     # Resitev bo oblike:
#     "Enterobacteria *** lambda"
#     # kjer tri zvezdice zamenjaj za ustrezno ime.
# -----------------------------------------------------------------------------
# # Resitev bo oblike:
# "Enterobacteria *** lambda"
# # kjer tri zvezdice zamenjaj za ustrezno ime.
# =============================================================================
def zmnozi(x, y):
    return x*y
Spremenljivka="Nek string, ki je enak spremenljivki"
(( CE and CE) and ( CE and CE))

Check.part()

Check.equal('odstej(4, 4)', 21 )
Check.equal('odstej(4, 4)', 22 )

Check.equal('odstej(4, 4)', 22 ) and Check.equal('odstej(4, 4)', 22 )

Check.equal("odstej(4, 4)", 16 ) and \
Check.equal('odstej(4, 4)', 18 ) and \
Check.equal('odstej(4, 4)', 20 )

Check.secret(zmnozi(100, 100), """lala""")
Check.secret(zmnozi(500, 123), '''lalalallaa''')

Check.secret(zmnozi(11, 11), 'sporočilo: """neko sporočilo"""') and \
Check.secret(zmnozi(33, 33))
                 

(   Check.equal('''odstej(8, 8)''', 25 ) and
    Check.equal('odstej(int("""88"""), 18)', 100) and 
    Check.equal("odstej(20, 20)", 400) and
    Check.equal("odstej(20, 20)", 400)
    
)

(
    Check.equal('''odstej(8, 8)''', 335 ) and
    Check.equal("odstej(int('88'), 18)", 1300) and 
    Check.equal("odstej(20, 20)", 4300) and
    Check.equal("odstej(20, 20)", 4030)
    
)

Check.equal("odstej(1, 1)", 1 ) and \
Check.equal('odstej(2, 2)', 2 ) or \
Check.equal('odstej(3, 3)', 3 )

(
    Check.secret(odstej(1, 1)) or
    Check.secret(odstej(2, 2)) and
    Check.secret(odstej(3, 3))
    
)

(   Check.secret(odstej(8, 8)) and
    Check.secret(odstej(6, 6)) and
    Check.secret(odstej(1, 1))
    
)





for i in range(1, 10):
    Check.secret(zmnozi(i, i+1))
    

resitev = eval(Check.current_part['solution'])
if not isinstance(resitev, str):
    Check.error('Rešitev mora biti niz. Nizi se pisejo takole "TUKAJ JE BESEDILO"')

if "Enterobacteria phage lambda" not in resitev:
    Check.error('Napisati morate pravilen niz. Namig resitev je: "Enterobacteria phage lambda"')



print('\n\n' + '*' * 15 + ' POZOR - naloga nima testa! ' +  '*' * 10)
print('Zato bo vsaka rešitev označena kot pravilna. ')
print('\nZagotovo si oglej tudi uradno rešitvo (žarnica)')
print('in jo primerjaj s svojo.')
print('\n' + '*' * 50)
