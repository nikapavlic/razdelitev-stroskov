from datetime import date
import json

class Model:
    def __init__(self):
        self.skupine = []
        self.aktualna_skupina = None
        self.moja_zgodovina = []

    def dodaj_skupino(self, skupina):
        self.skupine.append(skupina)
        if not self.aktualna_skupina:
            self.aktualna_skupina = skupina
    
    def pobrisi_skupino(self, skupina):
        self.skupine.remove(skupina)

    def zamenjaj_skupino(self, skupina):
        self.aktualna_skupina = skupina

    def zakljuci_belezenje(self, skupina):
        self.skupine.remove(skupina)
        self.moja_zgodovina.append(skupina)

    def dodaj_udelezenca(self, ime):
        self.aktualna_skupina.dodaj_udelezenca(ime)
    
    def pobrisi_udelezenca(self, ime):
        self.aktualna_skupina.zbrisi_udelezenca(ime)

    def dodaj_placilo(self, placilo):
        self.aktualna_skupina.dodaj_placilo(placilo)

    def v_slovar(self):
        return {
            "skupine": [skupina.v_slovar() for skupina in self.skupine],
            "aktualna_skupina": self.skupine.index(self.aktualna_skupina)
            if self.aktualna_skupina
            else None,
        }

    @staticmethod
    def iz_slovarja(slovar):
        model = Model()
        model.skupine = [
            Skupina.iz_slovarja(sl_skupine) for sl_skupine in slovar["skupine"]
        ]
        if slovar["aktualna_skupina"] is not None:
            model.aktualna_skupina = model.skupine[slovar["aktualna_skupina"]]
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




class Skupina:
    def __init__(self, ime):
        self.ime = ime
        self.udelezenci = []

    def dodaj_udelezenca(self, udelezenec):
        self.udelezenci.append(udelezenec)

    def zbrisi_udelezenca(self, udelezenec):
        self.udelezenci.remove(udelezenec)

    def stevilo_udelezencev(self):
        return len(self.udelezenci)

    def skupni_strosek(self):
        return sum([oseba.placano for oseba in self.udelezenci]) 

    def strosek_enega(self):
        return round(Skupina.skupni_strosek() / Skupina.stevilo_udelezencev(), 2) 

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




class Udelezenec:
    def __init__(self, ime):
        self.ime = ime
        self.placano = 0
        self.placila = []

    def dodaj_placilo(self, placilo):
        self.placano += placilo
        self.placila.append(placilo)

    def zbrisi_placilo(self, placilo):
        self.placano -= placilo

    def še_dolzen(self):
        return Skupina.strosek_enega() - self.placano

    def v_slovar(self):
        return {
            "ime": self.ime,
            "plačila": [placilo.v_slovar() for placilo in self.placila]
        }

    @staticmethod
    def iz_slovarja(slovar):
        udelezenec = Udelezenec(slovar["ime"])
        udelezenec.placila = [Placilo.iz_slovarja(sl_placila) for sl_placila in slovar["plačila"]]
        return udelezenec


class Placilo:
    def __init__(self, znesek, datum, opis):
        self.znesek = znesek
        self.datum = datum
        self.opis = opis
    
    def v_slovar(self):
        return {
            "znesek": self.znesek,
            "datum": date.isoformat(self.datum) if self.datum else None,
            "opis": self.opis,
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Placilo(
            slovar["znesek"],
            date.isoformat(slovar["datum"]) if slovar["datum"] else None,
            slovar["opis"]
        )