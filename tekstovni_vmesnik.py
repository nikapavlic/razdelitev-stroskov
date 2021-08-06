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


def prikaz_udelezenca(oseba):
    skupina = moj_model.aktualna_skupina
    dolg = Skupina.strosek_enega(skupina) - float(Udelezenec.placal(oseba))
    #dolg = Udelezenec.še_dolzen(oseba)
    return f"{oseba.ime}: plačal/-a {Udelezenec.placal(oseba)}, dolžen/-a še {round(dolg,2)}"


def prikaz_placila(placilo):
    return f"{placilo.znesek},{placilo.opis}"


def izberi_skupino(model):
    return izberi_moznost([(skupina, prikaz_skupine(skupina)) for skupina in model.skupine])


def izberi_udelezenca(skupina):
    return izberi_moznost([(oseba, prikaz_udelezenca(oseba)) for oseba in skupina.udelezenci])


def izberi_placilo(udelezenec):
    return izberi_moznost([(placilo, prikaz_placila(placilo)) for placilo in udelezenec.placila])


def tekstovni_vmesnik():
    pozdravno_sporocilo()
    while True:
        prikazi_aktualne_skupine()
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


def prikazi_aktualne_skupine():
    if moj_model.aktualna_skupina:
        for skupina in moj_model.skupine:
            print(f"{skupina.ime}: {skupina.stevilo_udelezencev()} udeležencev, {Skupina.skupni_strosek(skupina)} plačano, {Skupina.strosek_enega(skupina)} na enega")


def dodaj_skupino():
    print("Vnesite podatke nove skupine.")
    ime = input("Ime> ")
    if ime == "":
        print("Vnesti morate ime skupine.")
        dodaj_skupino()
    else:
        if ime.upper() in moj_model.imena_skupin():
            print("Skupina s takšnim imenom že obstaja.")
        else:
            nova_skupina = Skupina(ime)
            moj_model.dodaj_skupino(nova_skupina)


def pobrisi_skupino():
    skupina = izberi_skupino(moj_model)
    moj_model.pobrisi_skupino(skupina)


def zamenjaj_skupino():
    if moj_model.skupine == []:
        print("Ni aktivnih skupin, zato preklop ni mogoč.")
    else:
        print("Izberite skupino, na katero bi preklopili.")
        skupina = izberi_skupino(moj_model)
        moj_model.zamenjaj_skupino(skupina)


def dodaj_udelezenca():
    if moj_model.skupine == []:
        print("Najprej je potrebno dodati skupino.")
    else:
        skupina = moj_model.aktualna_skupina
        print("Vnesite podatke novega udeleženca.")
        ime = input("Ime> ")
        if ime.upper() in skupina.imena_udelezencev():
            print("Udeleženec s takšnim imenom že obstaja.")
        else:
            nov_udelezenec = Udelezenec(ime)
            Skupina.dodaj_udelezenca(skupina, nov_udelezenec)


def pobrisi_udelezenca():
    skupina = moj_model.aktualna_skupina
    if skupina.udelezenci == []:
        print("Skupina je brez udeležencev.")
    else:
        oseba = izberi_udelezenca(skupina)
        Skupina.zbrisi_udelezenca(skupina, oseba)


def dodaj_znesek():
    znesek = input("Znesek> ")
    # if not znesek.isdecimal():
    #    dodaj_znesek()
    # else:
    #    return float(znesek)
    try:
        print(znesek)
        return float(znesek)
    except ValueError:
        print("Vnesti morate število.")
        dodaj_znesek()


def dodaj_placilo():
    if moj_model.skupine == []:
        print("Ni vpisanih skupin.")
    else:
        skupina = moj_model.aktualna_skupina
        if skupina.udelezenci == []:
            print("V skupini ni udeležencev.")
        else:
            print("Izberite komu želite dodati plačilo.")
            udelezenec = izberi_udelezenca(skupina)
            print("Vnesite podatke plačila.")
            znesek = dodaj_znesek()
            #znesek = input("Znesek> ")
            # try:
            #    return int(znesek)
            # except ValueError:
            #    print("Vnesti morate število.")
            opis = input("Opis> ")
            Udelezenec.dodaj_placilo(udelezenec, znesek, opis)


def pobrisi_placilo():
    if moj_model.skupine == []:
        print("Ni vpisanih skupin")
    else:
        skupina = moj_model.aktualna_skupina
        if skupina.udelezenci == []:
            print("V skupini ni udeležnecev")
        else:
            oseba = izberi_udelezenca(skupina)
            placilo = izberi_placilo(oseba)
            Udelezenec.zbrisi_placilo(oseba, placilo)


tekstovni_vmesnik()
# dodaj_znesek()
