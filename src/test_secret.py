import re

a="Check.secret(zmnozi(3, 5) )"
b="Check.secret(zmnozi(int('3'), 6), 'sporočilo o, napaki' )"
c="Check.secret([koren(i) for i in range(2, 7)] )"
d="Check.secret([koren(i) for i in range(2, 7)], 'sporočilo, o napaki' )"

for i in [a, b, c, d]:
    print(i)
    check_secret_string=i.strip().strip("Check.secret(").strip()[:-1].strip()
    #odstranim Check.secret( in oklepaj na koncu
    # pri recimo b primeru ostane torej: "zmnozi(int('3'), 6), 'sporočilo o, napaki'"


    quotation_mark_type=check_secret_string[-1] # pogledam kakšen narekovaj je na koncu
    if quotation_mark_type=="'" or quotation_mark_type=='"': # preverjanje ali check.secret sploh ima drugi argument
        
        triple_quotation_mark=check_secret_string[-1]==check_secret_string[-2] # prevrjanje če je trojni narekovaj
        # morda bo tu problem, če arg ne bo dovolj dolg ? 
        if triple_quotation_mark==False: # nimamo trojnih narekovajev
            
            drugi_arg=re.match(r"({0}(.*?)[^{0}]{0})".format(quotation_mark_type), check_secret_string[::-1]) #iščem ujemanje na obrnjenem nizu
            if drugi_arg!=None: # check.secret ni nujno, da ima drugi argument
                drugi_arg=drugi_arg.group(1)[::-1] # ga obrnem, da je spet prav            
        else:
            drugi_arg=re.search(r"{0}{0}{0}(.*?){0}{0}{0}".format(quotation_mark_type), check_secret_string[::-1])
            if drugi_arg!=None:
                drugi_arg=drugi_arg.group(0)[::-1]
            
        if drugi_arg!=None:
            prvi_arg=check_secret_string[0:-len(drugi_arg)].strip().strip(",").strip() # prvi argument je tisto kar ostane
        else: # če drugega arg ni potem je vse le prvi arg
            prvi_arg=check_secret_string

    else:
        prvi_arg=check_secret_string
        drugi_arg=None

    
    print(prvi_arg)
    print(drugi_arg)
    print("\n")
