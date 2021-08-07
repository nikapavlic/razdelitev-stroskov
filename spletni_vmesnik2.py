import bottle
from model import Model, Skupina, Udelezenec, Placilo

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
        "osnovna_stran2.html",
        skupine=skupine,
        aktualna_skupina=skupina,
        stevilo_udelezencev=stevilo_udelezencev,
        skupno_placilo=skupno_placilo,
        strosek_enega=strosek_enega,
    )
# VEZANO NA SKUPINO:


@bottle.get("/dodaj-skupino/")
def dodaj_skupino_get():
    return bottle.template("dodaj_skupino.html", napake={}, polja={})


@bottle.post("/dodaj-skupino/")
def dodaj_skupino_post():
    ime = bottle.request.forms.getunicode("ime")
    polja = {"ime": ime}
    napake = moj_model.preveri_podatke_nove_skupine(ime)
    if napake:
        return bottle.template("dodaj_skupino.html", napake=napake, polja=polja)
    else:
        nova_skupina = Skupina(ime)
        moj_model.dodaj_skupino(nova_skupina)
        moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")


@bottle.get("/pobrisi-skupino/")
def pobrisi_skupino_get():
    skupine = moj_model.skupine
    return bottle.template("pobrisi_skupino.html", skupine=skupine)


@bottle.post("/pobrisi-skupino/")
def pobrisi_skupino():
    skupina = moj_model.aktualna_skupina
    moj_model.pobrisi_skupino(skupina)
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")


@bottle.post("/zamenjaj-aktualno-skupino/")
def zamenjaj_aktualno_skupino():
    print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    skupina = moj_model.skupine[int(indeks)]
    moj_model.aktualna_skupina = skupina
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")


@bottle.post("/zakljuci-belezenje/")
def zakljuci_belezenje():
    skupina = moj_model.aktualna_skupina
    moj_model.zakljuci_belezenje(skupina)
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")


# VEZANO NA UDELEŽENCA:


@bottle.get("/dodaj_udelezenca/")
def dodaj_udelezenca_get():
    #skupina = bottle.request.forms.getunicode("skupina")
    return bottle.template("dodaj_udelezenca.html", napake={}, polja={})


@bottle.post("/dodaj-udelezenca/")
def dodaj_udelezenca_post():
    ime = bottle.request.forms.getunicode("ime")
    polja = {"ime": ime}
    skupina = moj_model.aktualna_skupina
    napake = Skupina.preveri_podatke_novega_udelezenca(skupina, ime)
    if napake:
        return bottle.template("dodaj_udelezenca.html", napake=napake, polja=polja)
    else:
        nov_udelezenec = Udelezenec(ime)
        #placal = nov_udelezenec.placal()
        #dolg = Skupina.strosek_enega(skupina) - float(Udelezenec.placal(nov_udelezenec ))
        Skupina.dodaj_udelezenca(skupina, nov_udelezenec)
        moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")


@bottle.post("/pobrisi-udelezenca/")
def pobrisi_udelezenca():
    print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    skupina = moj_model.aktualna_skupina
    udelezenec = skupina.udelezenci[int(indeks)]
    Skupina.zbrisi_udelezenca(skupina, udelezenec)
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")


# VEZANO NA PLAČILO


@bottle.post("/dodaj-placilo/")
def dodaj_placilo():
    znesek = bottle.request.forms.getunicode("znesek")
    opis = bottle.request.forms.getunicode("opis")
    skupina = moj_model.aktualna_skupina
    print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    udelezenec = skupina.udelezenci[int(indeks)]
    Udelezenec.dodaj_placilo(udelezenec, znesek, opis)
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")


@bottle.post("/pobrisi-placilo/")
def pobrisi_placilo():
    #print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    skupina = moj_model.aktualna_skupina
    udelezenec = skupina.udelezenci[int(indeks)]
    #print(dict(bottle.request.forms))
    st = bottle.request.forms.getunicode("st")
    placilo = udelezenec.placila[int(st)]
    Udelezenec.zbrisi_placilo(udelezenec, placilo)
    moj_model.shrani_v_datoteko(IME_DATOTEKE)
    bottle.redirect("/")


@bottle.get("/zgodovina/")
def zgodovina():
    skupine = moj_model.moja_zgodovina
    return bottle.template("zgodovina.html", skupine = skupine,)


@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"


bottle.run(reloader=True, debug=True)
