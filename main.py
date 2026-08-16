from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import random

# МАТРИЧНА БАЗА ОД 16 ПИТАЊА (ИДЕНТИЧНА КАО ПРЕ!)
pitanja_baza = [
    {"tekst": "=== KVIZ MIKSER ===\n\nMujo kupio psa koji ujutru donese novine. Haso kaze?", "opcije": ["Video sam na Samsungu", "Moj pas mi donese dorucak", "Ali ti se ne pretplacujes na novine!"], "tacan": 2},
    {"tekst": "=== KVIZ MIKSER ===\n\nMujo kod doktora: 'Boli me ruka kad je dignem ovako!' Doktor?", "opcije": ["'Pa nemoj je dizati, idiote!'", "'Promeni Wi-Fi lozinku!'", "'Moramo da je secemo!'"], "tacan": 0},
    {"tekst": "=== KVIZ MIKSER ===\n\nKojom zemljom je vladala cuvena vladarka Kleopatra?", "opcije": ["Grcka", "Rim", "Egipat"], "tacan": 2},
    {"tekst": "=== KVIZ MIKSER ===\n\nKoliko se u narodu veruje da macke imaju zivota?", "opcije": ["1 zivot", "7 zivota", "9 zivota"], "tacan": 2},
    {"tekst": "=== KVIZ MIKSER ===\n\nZasto plavusa jede novine na klupi u parku?", "opcije": ["Gladna je a nema para", "Kako bi mogla da cita u sebi!", "Da proveri sta ima novo na lokalu"], "tacan": 1},
    {"tekst": "=== KVIZ MIKSER ===\n\nZasto je plavusa pala kroz prozor sa drugog sprata?", "opcije": ["Gledala je ptice", "Peglala je zavese dok su visile na prozoru!", "Pokvario joj se Samsung tablet"], "tacan": 1},
    {"tekst": "=== KVIZ MIKSER ===\n\nSta radi Kraljevcanin kad mu pukne internet na mobilnom?", "opcije": ["Zove tehnicku podršku", "Ide biciklom na Ibar da hvata signal kod vrbe", "Kupuje novu masinu za ves"], "tacan": 1},
    {"tekst": "=== KVIZ MIKSER ===\n\nSta kaze Beogradanin kad ga pitas za sifru za Wi-Fi?", "opcije": ["'Evo ti sifra, JazyToys123!'", "'Ne znam brate, to mi placa infostan na Dedinju!'", "'Kradem signal iz Panceva'"], "tacan": 1},
    {"tekst": "=== KVIZ MIKSER ===\n\nComo Sapcanin proverava da li mu ruter radi u punoj brzini?", "opcije": ["Ako mu ucitava KupujemProdajem za sekundu, ruter je full!", "Meri brzinu lenjirom na stolu", "Gleda u nebo i ceka znak"], "tacan": 0},
    {"tekst": "=== KVIZ MIKSER ===\n\nSta kaze Novosadin kad mu u ruter uneses paket od 500 GB?", "opcije": ["'Malo je to, daj jos!'", "'Jaooo, pa di cu ja sa tol'kim gigabajtima, polako...' ", "'Obrisacu Pydroid odmah'"], "tacan": 1},
    {"tekst": "=== KVIZ MIKSER ===\n\nSta kaze Kragujevcanka drugarici kad resi da kupi novu torbu?", "opcije": ["'Kupicu je preko Konzole'", "'Mora da bude veca od komsijinog auta, da pukne od muke!'", "'Kupicu najmanju na svetu'"], "tacan": 1},
    {"tekst": "=== KVIZ MIKSER ===\n\nSta kaze Pancevka kad ude u parfimeriju i trazi najjaci parfem?", "opcije": ["'Dajte neki koji mirise na cist planinski vazduh, da promenim sredinu!'", "'Dajte mi onaj sa mirisom sive pozadine'", "'Dajte mi miris benzina'"], "tacan": 0},
    {"tekst": "=== KVIZ MIKSER ===\n\nZasto Cacanin parkira auto preko dva parking mesta?", "opcije": ["Da mu niko ne ogrebe besnu masinu", "Da pokaze svima da je on gazda", "Zuri na svadbu pa ne gleda crte"], "tacan": 0},
    {"tekst": "=== KVIZ MIKSER ===\n\nUciteljica pita: 'Perice, ako ti tata da 100 dinara i brat ti da 100 dinara, koliko imas?'", "opcije": ["'Imam 200 dinara.'", "'Imam 100 dinara jer mi je brat oteo moj deo!'", "'Imam ruter od 500 GB.'"], "tacan": 1},
    {"tekst": "=== KVIZ MIKSER ===\n\nPandur pise kaznu klincu na biciklu: 'Reci Deda Mrazu da stavi svetlo!' Klinac kaze?", "opcije": ["Vazi ciko, kupicu ruter", "Pa ciko, reci i ti Deda Mrazu da ti je doneo magarca umesto konja!", "Obrisacu ti Pydroid odmah"], "tacan": 1},
    {"tekst": "=== KVIZ MIKSER ===\n\nUhvatio Ciga zlatnu ribicu za jednu zelju. Sta joj Ciga trazi?", "opcije": ["Da mu popravi Wi-Fi lozinku", "Da mu kuca bude od cistog zlata", "Daj mi ribice jedan ruter, ali da komsija placa pretplatu!"], "tacan": 2}
]

class JazyToysKvizApp(App):
    def build(self):
        self.evri, self.trenutno_pitanje, self.tockak_zavrten, self.broj_dzokera, self.preostalo_vreme = 0, 0, False, 0, 10
        self.pitanja = list(pitanja_baza)
        self.promesaj_sve()
        
        # ГЛАВНИ ЕКРАН
        glavni_layout = BoxLayout(orientation='vertical', padding=15, spacing=8, canvas_bg="#2b1654")
        
        # БАНЕР ГОРЕ
        glavni_layout.add_widget(Label(text="[ REKLAMA BANER VRH ]", size_hint_y=0.08, color=(0.5,0.5,0.5,1)))
        
        # НАСЛОВ И БИЛАНС
        glavni_layout.add_widget(Label(text="★ JAZYTOYS CASH SYSTEM ★", font_size=20, bold=True, size_hint_y=0.08))
        self.lbl_bilans = Label(text="BILANS: 0 €", font_size=24, bold=True, size_hint_y=0.08, color=(0,0,0,1))
        glavni_layout.add_widget(self.lbl_bilans)
        
        # ТОЧАК СРЕЋЕ ОКВИР
        tockak_box = BoxLayout(orientation='vertical', size_hint_y=0.2, spacing=3)
        tockak_box.add_widget(Label(text="[ DNEVNI TOČAK SREĆE ]", font_size=12))
        self.lbl_tockak = Label(text="[ Zavrti i osvoji Evre ]", font_size=16, bold=True, color=(1,0.8,0.2,1))
        tockak_box.add_widget(self.lbl_tockak)
        self.btn_spin = Button(text="[ ZAVRTI TOČAK ]", font_size=14, bold=True, background_color=(1,0.8,0.2,1))
        self.btn_spin.bind(on_press=self.zavrti_tocak)
        tockak_box.add_widget(self.btn_spin)
        glavni_layout.add_widget(tockak_box)
        
        # ТАЈМЕР И ПИТАЊЕ
        self.lbl_tajmer = Label(text="⏱️ Vreme: 10s", font_size=16, bold=True, size_hint_y=0.06)
        glavni_layout.add_widget(self.lbl_tajmer)
        self.lbl_pitanje = Label(text="", font_size=14, halign="center", size_hint_y=0.15)
        glavni_layout.add_widget(self.lbl_pitanje)
        
        # ДУГМИЋИ А, Б, Ц
        self.dugmici = []
        for i in range(3):
            btn = Button(text="", font_size=14, bold=True, background_color=(0.1,0.15,0.3,1))
            btn.bind(on_press=lambda instance, idx=i: self.klik_na_odgovor(idx))
            glavni_layout.add_widget(btn)
            self.dugmici.append(btn)
            
        # БАНЕР ДОЛЕ
        glavni_layout.add_widget(Label(text="[ REKLAMA BANER DNO ]", size_hint_y=0.08, color=(0.5,0.5,0.5,1)))
        
        # ДОЊИ МЕНИ
        donji_meni = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=5)
        btn_restart = Button(text="[ 🔄 RESTART ]", font_size=11, bold=True, background_color=(1,0.8,0.2,1))
        btn_restart.bind(on_press=self.resetuj_kviz)
        donji_meni.add_widget(btn_restart)
        
        self.btn_dzoker = Button(text="[ 📞 POMOĆ ]", font_size=11, bold=True, background_color=(0,0.5,1,1))
        self.btn_dzoker.bind(on_press=self.iskoristi_dzokera)
        donji_meni.add_widget(self.btn_dzoker)
        
        donji_meni.add_widget(Label(text="30€ za 15€", font_size=10))
        
        btn_withdraw = Button(text="WITHDRAW", font_size=11, bold=True, background_color=(0.1,0.6,0.2,1))
        btn_withdraw.bind(on_press=self.withdraw)
        donji_meni.add_widget(btn_withdraw)
        glavni_layout.add_widget(donji_meni)
        
        self.osvezi_pitanje_ekran()
        return glavni_layout

    def promesaj_sve(self):
        random.shuffle(self.pitanja)
        for p in self.pitanja:
            txt = p["opcije"][p["tacan"]]
            random.shuffle(p["opcije"])
            p["tacan"] = p["opcije"].index(txt)

    def zavrti_tocak(self, instance):
        if self.tockak_zavrten: return
        opcije = ["1 EUR", "2 EUR", "3 EUR", "Pomoc Prijatelja", "Vise srece"]
        rez = random.choice(opcije)
        self.lbl_tockak.text = f"=== {rez} ==="
        self.tockak_zavrten = True
        if "1 EUR" in rez: self.evri += 1
        elif "2 EUR" in rez: self.evri += 2
        elif "3 EUR" in rez: self.evri += 3
        elif "Pomoc" in rez: self.broj_dzokera += 1
        self.lbl_bilans.text = f"BILANS: {self.evri} €"

    def iskoristi_dzokera(self, instance):
        if self.broj_dzokera > 0:
            self.broj_dzokera -= 1
            p = self.pitanja[self.trenutno_pitanje]
            self.lbl_pitanje.text = f"BRANKO KAŽE: Tačno je pod {['A', 'B', 'C'][p['tacan']]}!\n\n" + p["tekst"]
        else:
            self.lbl_tockak.text = "❌ Nemaš džokera!"

    def klik_na_odgovor(self, idx):
        p = self.pitanja[self.trenutno_pitanje]
        if idx == p["tacan"]: self.evri += 1
        self.trenutno_pitanje += 1
        self.osvezi_pitanje_ekran()

    def osvezi_pitanje_ekran(self):
        self.lbl_bilans.text = f"BILANS: {self.evri} €"
        if self.trenutno_pitanje < len(self.pitanja):
            p = self.pitanja[self.trenutno_pitanje]
            self.lbl_pitanje.text = p["tekst"]
            oznake = ["A) ", "B) ", "C) "]
            for i in range(3): self.dugmici[i].text = oznake[i] + p["opcije"][i]
        else:
            self.lbl_pitanje.text = f"KRAJ KVIZA! Skupio si {self.evri}€."

    def resetuj_kviz(self, instance):
        self.evri, self.trenutno_pitanje, self.tockak_zavrten, self.broj_dzokera = 0, 0, False, 0
        self.promesaj_sve()
        self.lbl_tockak.text = "[ Zavrti i osvoji Evre ]"
        self.osvezi_pitanje_ekran()

    def withdraw(self, instance):
        pass

if __name__ == '__main__':
    JazyToysKvizApp().run()
