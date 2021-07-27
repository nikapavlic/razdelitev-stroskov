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

    def zakljuci_belezenje(self, skupina):
        self.skupine.remove(skupina)
        self.moja_zgodovina.append(skupina)

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
        return sum([udelezenec.placano for udelezenec in self.udelezenci]) 

    def strosek_enega(self):
        return Skupina.skupni_strosek() / Skupina.stevilo_udelezencev()
    

class Udelezenec:
    def __init__(self, ime):
        self.ime = ime
        self.placano = 0

    def dodaj_placilo(self, placilo):
        self.placano += placilo

    def zbrisi_placilo(self, placilo):
        self.placano -= placilo

    def še_dolzen(self):
        return Skupina.strosek_enega() - self.placano





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