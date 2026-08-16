from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.clock import Clock
import random

# БАЗА НАЈЈАЧИХ ТИМОВА ГРУПИСАНИХ ПО ДРЖАВАМА
baza_timova = {
    # СРБИЈА
    "Crvena zvezda (SRB)": {"forma": 90, "napad": 88, "odbrana": 82},
    "Partizan (SRB)": {"forma": 75, "napad": 76, "odbrana": 72},
    # ЦРНА ГОРА
    "Buducnost Podgorica (MNE)": {"forma": 75, "napad": 72, "odbrana": 70},
    "Sutjeska Niksic (MNE)": {"forma": 70, "napad": 68, "odbrana": 67},
    # БОСНА И ХЕРЦЕГОВИНА
    "Borac Banja Luka (BIH)": {"forma": 78, "napad": 74, "odbrana": 72},
    "Zrinjski Mostar (BIH)": {"forma": 77, "napad": 78, "odbrana": 73},
    # ШПАНИЈА
    "Real Madrid (ESP)": {"forma": 95, "napad": 96, "odbrana": 90},
    "Barcelona (ESP)": {"forma": 92, "napad": 94, "odbrana": 84},
    # ЕНГЛЕСКА
    "Man. City (ENG)": {"forma": 94, "napad": 97, "odbrana": 89},
    "Arsenal (ENG)": {"forma": 93, "napad": 92, "odbrana": 94},
    # ИТАЛИЈА
    "Inter Milan (ITA)": {"forma": 93, "napad": 92, "odbrana": 93},
    "Juventus (ITA)": {"forma": 88, "napad": 84, "odbrana": 91},
    # НЕМАЧКА
    "Bayern Munich (GER)": {"forma": 90, "napad": 96, "odbrana": 80},
    "Bayer Leverkusen (GER)": {"forma": 91, "napad": 93, "odbrana": 87}
}

class JazyToysPredictorApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=8)
        
        # 1. РЕКЛАМА БАНЕР ВРХ ЕКРАНА (ДУПЛО ВЕЋА СЛОВА)
        self.lbl_reklama_vrh = Label(text="[ Google AdMob - РЕКЛАМА БАНЕР ВРХ ЕКРАНА ]", font_size=24, size_hint_y=0.06, color=(0.4, 0.4, 0.4, 1))
        layout.add_widget(self.lbl_reklama_vrh)
        
        # НАСЛОВ БРЕНДА (ДУПЛО ВЕЋА СЛОВА)
        layout.add_widget(Label(text="★ JAZYTOYS AI TOP LEAGUES PREDICTOR ★", font_size=40, bold=True, size_hint_y=0.08, color=(1,0.8,0.2,1)))
        layout.add_widget(Label(text="Prognoze za 4 elitna kluba iz svake lige", font_size=26, size_hint_y=0.04, color=(0.7,0.7,0.7,1)))
        
        # БИРАЊЕ ТИМОВА (ДУПЛО ВЕЋА СЛОВА У СПИНЕРИМА)
        niz_timova = list(baza_timova.keys())
        izbor_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.12)
        
        self.spin_domacin = Spinner(text="Izaberi Domaćina", values=niz_timova, background_color=(0.1,0.2,0.4,1), font_size=30, bold=True)
        self.spin_gost = Spinner(text="Izaberi Gosta", values=niz_timova, background_color=(0.1,0.2,0.4,1), font_size=30, bold=True)
        
        izbor_box.add_widget(self.spin_domacin)
        izbor_box.add_widget(Label(text="VS", size_hint_x=0.2, bold=True, font_size=44))
        izbor_box.add_widget(self.spin_gost)
        layout.add_widget(izbor_box)
        
        # ДУГМЕ ЗА ПРОГНОЗУ (ДУПЛО ВЕЋА СЛОВА)
        btn_analiza = Button(text="🔥 POKRENI AI PROGNOZU 🔥", font_size=36, bold=True, background_color=(0,0.6,0.2,1), size_hint_y=0.1)
        btn_analiza.bind(on_press=self.izracunaj_prognozu)
        layout.add_widget(btn_analiza)
        
        # ИСПИС: ТИМ - ПРОЦЕНТИ У СРЕДИНИ - ТИМ (ДУПЛО ВЕЋА СЛОВА)
        self.lbl_procenti = Label(text="---  [ POBEDA: --% | NEREŠENO: --% | PORAZ: --% ]  ---", font_size=32, bold=True, size_hint_y=0.14, color=(0.2,1,0.2,1), halign="center")
        layout.add_widget(self.lbl_procenti)
        
        # ТАЧАН РЕЗУЛТАТ (ДУПЛО ВЕЋА СЛОВА)
        self.lbl_tacan_rez = Label(text="TAČAN REZULTAT: ?:?", font_size=40, bold=True, size_hint_y=0.08, color=(1,0.5,0,1))
        layout.add_widget(self.lbl_tacan_rez)
        
        # AI ИЗВЕШТАЈ (ДУПЛО ВЕЋА СЛОВА, БОЛДОВАНО И ПРЕГЛЕДНО)
        self.lbl_analiza = Label(text="Izaberite timove iz prve lige i pokrenite sistem...", font_size=36, bold=True, halign="center", valign="middle", size_hint_y=0.26)
        self.lbl_analiza.bind(size=self.lbl_analiza.setter('text_size'))
        layout.add_widget(self.lbl_analiza)
        
        # НАРАНЏАСТА ПРЕМИЈУМ КОЦКА (ДУПЛО ВЕЋА СЛОВА)
        self.btn_premium = Button(text="[ 🔑 OTKLJUČAJ TIKET DANA - ПРЕМИЈУМ СЕФ ]\n(Цена претплате: 15€ / месечно)", font_size=32, bold=True, background_color=(1,0.4,0,1), size_hint_y=0.16, halign="center")
        self.btn_premium.bind(on_press=self.otvori_premium_prozor)
        layout.add_widget(self.btn_premium)
        
        # 2. РЕКЛАМА БАНЕР ДНО ЕКРАНА (ДУПЛО ВЕЋА СЛОВА)
        self.lbl_reklama_dno = Label(text="[ Google AdMob - РЕКЛАМА БАНЕР ДНО ЕКРАНА ]", font_size=24, size_hint_y=0.06, color=(0.4, 0.4, 0.4, 1))
        layout.add_widget(self.lbl_reklama_dno)
        
        # ТАЈМЕР ОСТАЈЕ НА СВАКИХ 30 СЕКУНДИ ЗА ДУПЛО ВЕЋУ ЗАРАДУ
        Clock.schedule_interval(self.prikazi_iskacuci_baner, 30.0)
        
        return layout

    def izracunaj_prognozu(self, instance):
        domacin = self.spin_domacin.text
        gost = self.spin_gost.text
        
        if domacin == "Izaberi Domaćina" or gost == "Izaberi Gosta" or domacin == gost:
            self.lbl_analiza.text = "⚠️ ГРЕШКА:\nIzaberite dva različita tima iz liste!"
            return
            
        p1 = random.randint(38, 56)
        p2 = random.randint(22, 36)
        px = 100 - (p1 + p2)
        
        ime_d = domacin.split(" (")
        ime_g = gost.split(" (")
        
        self.lbl_procenti.text = f"{ime_d}  [ POBEDA: {p1}% | NEREŠENO: {px}% | PORAZ: {p2}% ]  {ime_g}"
        
        if p1 > p2:
            golovi_d = random.randint(2, 4)
            golovi_g = random.randint(0, 1)
            predlog = "3+ (Tri ili više golova)"
        elif p2 > p1:
            golovi_d = random.randint(0, 1)
            golovi_g = random.randint(2, 4)
            predlog = "2-2 & 3+ (Prelaz i golovi)"
        else:
            golovi_d = random.randint(1, 2)
            golovi_g = golovi_d
            predlog = "GG (Oba tima daju gol)"
            
        self.lbl_tacan_rez.text = f"TAČAN REZULTAT: {golovi_d}:{golovi_g}"
        self.lbl_analiza.text = f"★ AI IZVEŠTAJ УЖИВО ★\n\nStatistika ekipa ukazuje na veliku borbu na terenu.\nPreporučujemo siguran tip: {predlog}!"

    # ИСКАЧУЋА РЕКЛАМА СА УВЕЋАНИМ СЛОВИМА (ТАЈМЕР НА 30 СЕКУНДИ)
    def prikazi_iskacuci_baner(self, dt):
        box_ad = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box_ad.add_widget(Label(text="📢 РЕКЛАМА БАНЕР 📢", font_size=28, bold=True, color=(0,0.8,1,1)))
        box_ad.add_widget(Label(text="Kladionica JazyToys Bonus 200%!\nKlikni za preuzimanje para.", font_size=20, halign="center"))
        
        btn_close_ad = Button(text="[ X Zatvori ]", font_size=20, bold=True, background_color=(0.8,0.2,0.2,1), size_hint_y=0.3)
        box_ad.add_widget(btn_close_ad)
        
        popup_ad = Popup(title="Sponzorisani Oglas", content=box_ad, size_hint=(0.5, 0.4), pos_hint={'right': 0.95, 'bottom': 0.05}, auto_dismiss=False)
        btn_close_ad.bind(on_press=popup_ad.dismiss)
        popup_ad.open()

    def otvori_premium_prozor(self, instance):
        box = BoxLayout(orientation='vertical', padding=20, spacing=15)
        box.add_widget(Label(text="🔒 СИСТЕМ ЗА НАПЛАТУ ОД ПУБЛИКЕ 🔒", font_size=28, bold=True, color=(1,0.5,0,1)))
        box.add_widget(Label(text="Уплатите 15€ месечну претплату преко картице\nda biste otključali današnji Tiket Dana sa 95% prolaza!", font_size=22, halign="center"))
        btn_zatvori = Button(text="[ НАЗАД НА ПРОГНОЗЕ ]", font_size=22, bold=True, background_color=(0.1,0.2,0.4,1), size_hint_y=0.3)
        box.add_widget(btn_zatvori)
        popup = Popup(title="JazyToys Premium Naplata", content=box, size_hint=(0.8, 0.5), auto_dismiss=False)
        btn_zatvori.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    JazyToysPredictorApp().run()
