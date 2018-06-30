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
"Enterobacteria phage lambda"

Check.part()
resitev = eval(Check.current_part['solution'])
if not isinstance(resitev, str):
    Check.error('Rešitev mora biti niz. Nizi se pisejo takole "TUKAJ JE BESEDILO"')

if "Enterobacteria phage lambda" not in resitev:
    Check.error('Napisati morate pravilen niz. Namig resitev je: "Enterobacteria phage lambda"')