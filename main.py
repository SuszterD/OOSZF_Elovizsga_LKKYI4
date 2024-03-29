from abc import ABC, abstractmethod
from datetime import datetime

class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar
        self.foglalasok = []

    def szabad_e(self, kezdo_datum, veg_datum):
        return all(foglalas['veg_datum'] < kezdo_datum or foglalas['kezdo_datum'] > veg_datum for foglalas in self.foglalasok)

    def foglalas_lemond(self, kezdo_datum):
        self.foglalasok = [foglalas for foglalas in self.foglalasok if foglalas['kezdo_datum'] != kezdo_datum]

    def foglal(self, kezdo_datum, veg_datum):
        if self.szabad_e(kezdo_datum, veg_datum):
            self.foglalasok.append({'kezdo_datum': kezdo_datum, 'veg_datum': veg_datum})
            return f"Szoba {self.szobaszam} foglalva lett {kezdo_datum.strftime('%Y-%m-%d')} - {veg_datum.strftime('%Y-%m-%d')}."
        else:
            return f"Szoba {self.szobaszam} már foglalt ebben az időszakban."

    def foglalas_datumok(self):
        return ", ".join(f"{foglalas['kezdo_datum'].strftime('%Y-%m-%d')} - {foglalas['veg_datum'].strftime('%Y-%m-%d')}" for foglalas in self.foglalasok)

    @abstractmethod
    def tipus(self):
        pass

    def __str__(self):
        foglalasok_str = self.foglalas_datumok()
        return f"{self.tipus()} szoba. A szoba száma: {self.szobaszam}, Ár: {self.ar}, Foglalások: {foglalasok_str if foglalasok_str else 'Nincsenek foglalások'}"

class EgyagyasSzoba(Szoba):
    def tipus(self):
        return "Egyágyas"

class KetagyasSzoba(Szoba):
    def tipus(self):
        return "Kétágyas"

class Szalloda:
    def __init__(self):
        self.szobak = []

    def szoba_hozzaadas(self, szoba):
        self.szobak.append(szoba)

    def adatfeltoltes(self):
        self.szoba_hozzaadas(EgyagyasSzoba(101, 50000))
        self.szoba_hozzaadas(KetagyasSzoba(102, 60000))

    def foglalasok_lekerdezes(self):
        return '\n'.join(str(szoba) for szoba in self.szobak)

    def foglalas(self, szobaszam, kezdo_datum, veg_datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                return szoba.foglal(kezdo_datum, veg_datum)
        return "Szoba nem található."

def foglalasi_folyamat(szalloda):
    szalloda.adatfeltoltes()

    while True:
        valasztas = input("Mit szeretne tenni? (foglalasok, foglal, kilep): ")
        if valasztas == "foglalasok":
            print(szalloda.foglalasok_lekerdezes())
        elif valasztas == "foglal":
            szobaszam = int(input("Adja meg a szobaszámot: "))
            kezdo_datum_str = input("Adja meg a kezdő dátumot (yyyy-mm-dd): ")
            veg_datum_str = input("Adja meg a végső dátumot (yyyy-mm-dd): ")
            kezdo_datum = datetime.strptime(kezdo_datum_str, '%Y-%m-%d')
            veg_datum = datetime.strptime(veg_datum_str, '%Y-%m-%d')
            print(szalloda.foglalas(szobaszam, kezdo_datum, veg_datum))
        elif valasztas == "kilep":
            print("Viszlát!")
            break
        else:
            print("Érvénytelen választás.")

szalloda = Szalloda()
foglalasi_folyamat(szalloda)
