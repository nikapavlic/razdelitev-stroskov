from model import Model, Skupina, Udelezenec, Placilo

IME_DATOTEKE = "stanje.json"
try:
    moj_model = Model.preberi_iz_datoteke(IME_DATOTEKE)
except FileNotFoundError:
    moj_model = Model()

DODAJ_SKUPINO = 1
POBRISI_SKUPINO = 2
ZAMENJAJ_SKUPINO = 3
DODAJ_UDELEZENCA = 4
POBRISI_UDELEZENCA = 5
DODAJ_PLACILO = 6
POBRISI_PLACILO = 7
IZHOD = 8

def preberi_stevilo():
    while True:
        vnos = input("> ")
        try:
            return int(vnos)
        except ValueError:
            print("Vnesti morate število.")

def izberi_moznost(moznosti):
    for i, (_moznost, opis) in enumerate(moznosti, 1):
        print(f"{i}) {opis}")
    while True:
        i = preberi_stevilo()
        if 1 <= i <= len(moznosti):
            moznost, _opis = moznosti[i - 1]
            return moznost
        else:
            print(f"Vnesti morate število med 1 in {len(moznosti)}.")

def prikaz_skupine(skupina):
    return f"{skupina.ime}"

def prikaz_udelezenca(ime):
    oseba = ime
    placal = ime.placano
    dolg = Udelezenec.še_dolzen(ime)
    return f"{oseba}: plačal/-a {placal}, dolžen/-a še {dolg}"

def prikaz_placila(placilo):
    return f"{placilo.znesek},{placilo.datum}, {placilo.opis}"

def izberi_skupino(model):
    return izberi_moznost([(skupina, prikaz_skupine(skupina)) for skupina in model.skupine])

def izberi_udelezenca(model):
    return izberi_moznost([(oseba, prikaz_udelezenca(oseba)) for oseba in model.udelezenci])

def izberi_placilo(model):
    return izberi_moznost([(placilo, prikaz_placila(placilo)) for placilo in model.placila ])

def tekstovni_vmesnik():
    pozdravno_sporocilo()
    while True:
        #prikazi_aktualne_skupine()
        ukaz = izberi_moznost(
            [
                (DODAJ_SKUPINO, "dodaj novo skupino"),
                (POBRISI_SKUPINO, "pobriši skupino"),
                (ZAMENJAJ_SKUPINO, "prikaži drugo skupino"),
                (DODAJ_UDELEZENCA, "dodaj novega udeleženca"),
                (POBRISI_UDELEZENCA, "pobriši udeleženca"),
                (DODAJ_PLACILO, "dodaj novo plačilo"),
                (POBRISI_PLACILO, "pobriši plačilo"),
                (IZHOD, "zapri program"),
            ]
        )
        if ukaz == DODAJ_SKUPINO:
            dodaj_skupino()
        elif ukaz == POBRISI_SKUPINO:
            pobrisi_skupino()
        elif ukaz == ZAMENJAJ_SKUPINO:
            zamenjaj_skupino()
        elif ukaz == DODAJ_UDELEZENCA:
            dodaj_udelezenca()
        elif ukaz == POBRISI_UDELEZENCA:
            pobrisi_udelezenca()
        elif ukaz == DODAJ_PLACILO:
            dodaj_placilo()
        elif ukaz == POBRISI_PLACILO:
            pobrisi_placilo()
        elif ukaz == IZHOD:
            moj_model.shrani_v_datoteko(IME_DATOTEKE)
            print("Nasvidenje!")
            break



def pozdravno_sporocilo():
    print("Pozdravljeni!")

#def prikazi_aktualne_skupine():
#    if moj_model.aktualna_skupina:
#        for skupina in moj_model.skupine

def dodaj_skupino():
    print("Vnesite podatke nove skupine.")
    ime = input("Ime> ")
    nova_skupina = Skupina(ime)
    moj_model.dodaj_skupino(nova_skupina)

def pobrisi_skupino():
    skupina = izberi_skupino(moj_model)
    moj_model.pobrisi_skupino(skupina)

def zamenjaj_skupino():
    print("Izberite skupino, na katero bi preklopili.")
    skupina = izberi_skupino(moj_model)
    moj_model.zamenjaj_skupino(skupina)

def dodaj_udelezenca():
    print("Vnesite podatke novega udeleženca.")
    ime = input("Ime> ")
    nov_udelezenec = Udelezenec(ime)
    moj_model.dodaj_udelezenca(nov_udelezenec)

def pobrisi_udelezenca():
    oseba = izberi_udelezenca(moj_model)
    Skupina.zbrisi_udelezenca(oseba)

def dodaj_placilo():
    print("Vnesite podatke plačila.")
    znesek = input("Znesek> ")
    datum = input("Datum> ")
    opis = input("Opis> ")
    novo_placilo = Placilo(znesek, datum, opis)
    moj_model.dodaj_placilo(novo_placilo)

def pobrisi_placilo():
    placilo = izberi_placilo(moj_model)
    Udelezenec.zbrisi_placilo(placilo)

tekstovni_vmesnik()