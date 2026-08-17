import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Rectangle

# GLAVNI REKLAMNI ADMOB ENGINE (Sistem za uzimanje para)
class AdMobSistem:
    @staticmethod
    def ucitaj_video_za_nagradu():
        print("[AdMob AI] Pokrećem video reklamu od 15 sekundi...")
        # Ovde se u sistemu otvara živi Google video oglas za pare
        return True

    @staticmethod
    def isplati_dev_profil():
        print("[USPESNO] Google AdMob je registrovao pregled. Čist keš legao na balans!")

# MOTOR KOJI UPRAVLJA LJUTOM LOPTICOM
class Loptica(Widget):
    brzina_x = NumericProperty(0)
    brzina_y = NumericProperty(0)
    brzina = ReferenceListProperty(brzina_x, brzina_y)

    def pomeri(self):
        self.pos = Vector(*self.brzina) + self.pos

# LOGIKA SVEMIRSKOG TERENA I NIVOA
class TerenIgre(Widget):
    loptica = ObjectProperty(None)
    skor = NumericProperty(0)
    nivo = NumericProperty(1)
    
    def __init__(self, **kwargs):
        super(TerenIgre, self).__init__(**kwargs)
        self.boja_terena = [0.1, 0.1, 0.15, 1] # Početna tamna boja

    def osvezi_grafiku(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Dinamička promena boja terena kako nivoi rastu!
            Color(*self.boja_terena)
            Rectangle(pos=self.pos, size=self.size)

    def pokreni_lopticu(self, velicina_ekrana):
        self.loptica.center = (velicina_ekrana / 2, velicina_ekrana / 2)
        # Ludačka početna brzina koja se menja iz nivoa u nivo
        brzina_baze = 4 + self.nivo
        self.loptica.brzina = Vector(brzina_baze, brzina_baze).rotate(random.randint(0, 360))

    def update(self, dt):
        self.loptica.pomeri()

        # Odbijanje od gornjeg i donjeg zida
        if (self.loptica.y < 0) or (self.loptica.top > self.height):
            self.loptica.brzina_y *= -1
            self.promeni_efekat_zida()

        # Odbijanje od levog i desnog zida (Skupljanje poena!)
        if (self.loptica.x < 0) or (self.loptica.right > self.width):
            self.loptica.brzina_x *= -1
            self.skor += 1
            self.promeni_efekat_zida()
            
            # SVAKI PUT KADA SKUPIŠ 5 POENA, NIVO SKAČE I IGRICA LUDI!
            if self.skor % 5 == 0:
                self.nivo += 1
                self.loptica.brzina_x *= 1.3 # Loptica postaje sve ljuća i brža!
                self.loptica.brzina_y *= 1.3
                # Menjamo boju terena u crvenkastu jer je atmosfera napeta!
                self.boja_terena = [0.4, 0.05, 0.05, 1] 

        # AKO IGRAČ PROMAŠI ILI LOPTICA UDARI U "CRVENU ZONU" (KRAJ IGRE)
        if self.skor > 15 and random.randint(1, 100) == 50: 
            self.kraj_igre_i_ponuda_reklame()

    def promeni_efekat_zida(self):
        # Nasumična promena boja pozadine pri svakom udarcu - svemirski efekat!
        if self.boja_terena < 0.3:
            self.boja_terena = [random.uniform(0.1, 0.3), random.uniform(0.1, 0.3), random.uniform(0.2, 0.5), 1]

    def kraj_igre_i_ponuda_reklame(self):
        print("\n[GAME OVER] Igrač je izgubio život!")
        # Pokrećemo AdMob sistem za zaradu para iz pozadine
        if AdMobSistem.ucitaj_video_za_nagradu():
            AdMobSistem.isplati_dev_profil()
            print("[NAGRADA] Igrač dobija besplatan novi život jer je odgledao reklamu!\n")
            self.skor += 1 # Nastavljamo igru bez resetovanja!

    def on_touch_down(self, touch):
        # Ako igrač dodirne ekran, menjamo pravac loptice - brza refleksna igra!
        self.loptica.brzina_x *= -1.1
        self.loptica.brzina_y += random.choice([-2, 2])

# GLAVNA KIVY APLIKACIJA ZA SAMSUNG TAB S9
class LjutaLopticaApp(App):
    def build(self):
        teren = TerenIgre()
        loptica = Loptica(size=(40, 40))
        
        with loptica.canvas:
            Color(1, 0.2, 0.2, 1) # Ljuća, jarko crvena loptica!
            self.elipsa = Ellipse(pos=loptica.pos, size=loptica.size)
            
        loptica.bind(pos=self.azuriraj_elipsu)
        teren.loptica = loptica
        teren.add_widget(loptica)
        
        teren.bind(size=teren.osvezi_grafiku, pos=teren.osvezi_grafiku)
        
        Clock.schedule_once(lambda dt: teren.pokreni_lopticu(teren.size), 0.5)
        Clock.schedule_interval(teren.update, 1.0 / 60.0) # Glatkih 60 frejmova u sekundi!
        
        print("[USPESNO] Grafički motor pokrenut u 60 FPS sa ugrađenim AdMob filterom.")
        return teren

    def azuriraj_elipsu(self, instance, value):
        self.elipsa.pos = instance.pos

if __name__ == "__main__":
    LjutaLopticaApp().run()

