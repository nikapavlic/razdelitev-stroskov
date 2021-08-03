import bottle
from model import Model, Skupina, Udelezenec, Placilo
from datetime import date

IME_DATOTEKE = "stanje.json"
try:
    moj_model = Model.preberi_iz_datoteke(IME_DATOTEKE)
except FileNotFoundError:
    moj_model = Model()

@bottle.get("/")
def osnovna_stran():
    skupine = moj_model.skupine
    skupina = moj_model.aktualna_skupina
    stevilo_udelezencev = Skupina.stevilo_udelezencev(skupina)
    skupno_placilo = Skupina.skupni_strosek(skupina)
    strosek_enega = Skupina.strosek_enega(skupina)
    return bottle.template(
        "osnovna_stran.html",
        skupine = skupine,
        aktualna_skupina = skupina,
        stevilo_udelezencev = stevilo_udelezencev,
        skupno_placilo = skupno_placilo,
        strosek_enega = strosek_enega,
    )

@bottle.get("/dodaj-skupino/")
def dodaj_skupino_get():
    return bottle.template("dodaj_skupino.html", napake = {}, polja = {})

@bottle.post("/dodaj-skupino/")
def dodaj_skupino_post():
    ime = bottle.request.forms.getunicode("ime")
    polja = {"ime": ime}
    napake = moj_model.preveri_podatke_nove_skupine(ime)
    if napake:
        return bottle.template("dodaj_skupino.html", napake = napake, polja = polja)
    else:
        nova_skupina = Skupina(ime)
        moj_model.dodaj_skupino(nova_skupina)
        moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")

#@bottle.post("/pobrisi-skupino/")
#def pobrisi_skupino():
#    skupina = 

#@bottle.get("/dodaj_udelezenca/")
#def dodaj_udelezenca_get():
#    skupina = bottle.request.forms.getunicode("skupina")    

@bottle.post("/dodaj-udelezenca/")
def dodaj_udelezenca_post():
    ime = bottle.request.forms.getunicode("ime")
    polja = {"ime": ime}
    skupina = moj_model.aktualna_skupina
    napake = Skupina.preveri_podatke_novega_udelezenca(skupina, ime)
    if napake:
        return bottle.template("dodaj_udelezenca.html", napake = napake, polja = polja)
    else:
        nov_udelezenec = Udelezenec(ime)
        placal = nov_udelezenec.placal()
        dolg = Skupina.strosek_enega(skupina) - float(Udelezenec.placal(nov_udelezenec ))
        Skupina.dodaj_udelezenca(skupina, nov_udelezenec)
        moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")

@bottle.post("/dodaj-placilo/")
def dodaj_placilo():
    znesek = float(bottle.request.forms.getunicode("znesek"))
    if bottle.request.forms["datum"]:
        datum = date.fromisoformat(bottle.request.forms["datum"])
    else:
        datum = None
    opis = bottle.request.forms.getunicode("opis")
    skupina = moj_model.aktualna_skupina
    print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    udelezenec = skupina.udelezenci[int(indeks)]
    Udelezenec.dodaj_placilo(udelezenec, znesek, datum, opis)
    moj_model.shrani_v_datoteko(IME_DATOTEKE)

@bottle.post("/zamenjaj-aktualno-skupino/")
def zamenjaj_aktualno_skupino():
    print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    skupina = moj_model.skupine[int(indeks)]
    moj_model.aktualna_skupina = skupina
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")

@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"

bottle.run(reloader = True, debug = True)