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

Check.part()
Check.equal('zmnozi((2, 88), 2)', 4) and \ 
Check.equal('zmnozi(3, 3)', 9)
Check.equal('zmnozi(4, 4)', 16, clean=clean, env=env)
Check.equal('zmnozi(5, 5)', 25) and \ 
Check.equal('zmnozi("10", "10")', 100) and \ 
Check.equal("zmnozi(20, 20)", 400) and \ 
Check.equal('x', 50 // 6)
Check.equal('odstej(8, 8)', 25) and \ 
Check.equal('odstej(88, 18)', 100) and \ 
Check.equal("odstej(20, 20)", 400) and \ 
Check.equal("odstej(20, 20)", 400)
Check.equal('sestej(81, 81)', 25) and \ 
Check.equal('sestej(88, 18)', 100) and \ 
Check.equal("sestej(20, 20)", 400)
Check.equal('Spremenljivka', "Nek string, ki je enak spremenljivki")





Check.secret(zmnozi(100, 100))
Check.secret(zmnozi(500, 123))

resitev = eval(Check.current_part['solution'])
if not isinstance(resitev, str):
    Check.error('Rešitev mora biti niz. Nizi se pisejo takole "TUKAJ JE BESEDILO"')

if "Enterobacteria phage lambda" not in resitev:
    Check.error('Napisati morate pravilen niz. Namig resitev je: "Enterobacteria phage lambda"')