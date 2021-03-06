import json


def isfloat(x):
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True


class Model:
    def __init__(self):
        self.skupine = []
        self.aktualna_skupina = None
        self.moja_zgodovina = []

    def dodaj_skupino(self, skupina):
        self.skupine.append(skupina)
        if not self.aktualna_skupina:
            self.aktualna_skupina = skupina
        else:
            self.aktualna_skupina = skupina

    def pobrisi_skupino(self, skupina):
        self.skupine.remove(skupina)
        if self.skupine == []:
            self.aktualna_skupina = None
        else:
            self.aktualna_skupina = self.skupine[0]

    def zamenjaj_skupino(self, skupina):
        self.aktualna_skupina = skupina

    def zakljuci_belezenje(self, skupina):
        self.skupine.remove(skupina)
        self.moja_zgodovina.append(skupina)
        if self.skupine == []:
            self.aktualna_skupina = None
        else:
            self.aktualna_skupina = self.skupine[0]

    def imena_skupin(self):
        """Vrne seznam imen skupin napisanih z velikimi tiskanimi črkami."""
        seznam = [str(skupina.ime) for skupina in self.skupine]
        povecan_seznam = []
        for ime in seznam:
            povecan_seznam.append(ime.upper())
        return povecan_seznam

    def v_slovar(self):
        return {
            "skupine": [skupina.v_slovar() for skupina in self.skupine],
            "aktualna_skupina": self.skupine.index(self.aktualna_skupina)
            if self.aktualna_skupina
            else None,
            "zgodovina": [skupina.v_slovar() for skupina in self.moja_zgodovina],
        }

    @staticmethod
    def iz_slovarja(slovar):
        model = Model()
        model.skupine = [
            Skupina.iz_slovarja(sl_skupine) for sl_skupine in slovar["skupine"]
        ]
        if slovar["aktualna_skupina"] is not None:
            model.aktualna_skupina = model.skupine[slovar["aktualna_skupina"]]
        model.moja_zgodovina = [Skupina.iz_slovarja(
            sl_skupine) for sl_skupine in slovar["zgodovina"]]
        return model

    def shrani_v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, "w", encoding='utf-8') as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat)

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        with open(ime_datoteke, encoding='utf-8') as dat:
            slovar = json.load(dat)
            return Model.iz_slovarja(slovar)

    def preveri_podatke_nove_skupine(self, ime):
        napake = {}
        if not ime:
            napake["ime"] = "Ime mora biti neprazno."
        for skupina in self.skupine:
            if skupina.ime == ime:
                napake["ime"] = "Ime je že zasedeno."
        return napake


class Skupina:
    def __init__(self, ime):
        self.ime = ime
        self.udelezenci = []

    def dodaj_udelezenca(self, udelezenec):
        if udelezenec in self.udelezenci:
            raise ValueError("Udeleženec s takšnim imenom že obstaja")
        else:
            self.udelezenci.append(udelezenec)

    def zbrisi_udelezenca(self, udelezenec):
        self.udelezenci.remove(udelezenec)

    def stevilo_udelezencev(self):
        return len(self.udelezenci)

    def skupni_strosek(self):
        return round(sum([float(Udelezenec.placal(oseba)) for oseba in self.udelezenci]), 2)

    def strosek_enega(self):
        if self.stevilo_udelezencev() == 0:
            return 0
        else:
            return round(self.skupni_strosek() / self.stevilo_udelezencev(), 2)

    def imena_udelezencev(self):
        """Vrne seznam imen udeležencev v skupini napisanih z velikimi tiskanimi črkami."""
        seznam = [str(udelezenec.ime) for udelezenec in self.udelezenci]
        povecan_seznam = []
        for ime in seznam:
            povecan_seznam.append(ime.upper())
        return povecan_seznam

    def v_slovar(self):
        return {
            "ime_skupine": self.ime,
            "udeleženci": [oseba.v_slovar() for oseba in self.udelezenci]
        }

    @staticmethod
    def iz_slovarja(slovar):
        skupina = Skupina(slovar["ime_skupine"])
        skupina.udelezenci = [
            Udelezenec.iz_slovarja(sl_udelezenca) for sl_udelezenca in slovar["udeleženci"]
        ]
        return skupina

    def preveri_podatke_novega_udelezenca(self, ime):
        napake = {}
        if not ime:
            napake["ime"] = "Ime mora biti neprazno"
        else:
            for udelezenec in self.udelezenci:
                if udelezenec.ime == ime:
                    napake["ime"] = "Ime je že zasedeno"
        return napake


class Udelezenec:
    def __init__(self, ime):
        self.ime = ime
        self.placano = 0
        self.placila = []

    def dodaj_placilo(self, znesek, opis):
        if not isfloat(znesek):
            ValueError("Znesek mora biti število")
        else:
            novo_placilo = Placilo(znesek, opis)
            self.placila.append(novo_placilo)

    def zbrisi_placilo(self, placilo):
        self.placila.remove(placilo)

    def placal(self):
        """Vrne koliko je udeleženec že plačal."""
        return round(sum([float(placilo.znesek) for placilo in self.placila]), 2)

    def še_dolzen(self):
        """Vrne koliko je udeleženec še dolžen."""
        skupina = Model().aktualna_skupina
        return float(Skupina.strosek_enega(skupina)) - float(self.placal())

    def v_slovar(self):
        return {
            "ime": self.ime,
            "plačila": [placilo.v_slovar() for placilo in self.placila]
        }

    @staticmethod
    def iz_slovarja(slovar):
        udelezenec = Udelezenec(slovar["ime"])
        udelezenec.placila = [Placilo.iz_slovarja(
            sl_placila) for sl_placila in slovar["plačila"]]
        return udelezenec


class Placilo:
    def __init__(self, znesek, opis):
        self.znesek = znesek
        self.opis = opis

    def v_slovar(self):
        return {
            "znesek": self.znesek,
            "opis": self.opis,
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Placilo(
            slovar["znesek"],
            slovar["opis"]
        )
