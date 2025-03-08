import random
import pygame
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PowerUp:
    def __init__(self, name, icon):
        self.name = name
        self.icon = pygame.image.load(resource_path(os.path.join("weapons", icon)))
        self.used = False

    def apply(self, game_state):
        raise NotImplementedError("Această metodă trebuie implementată de subclase.")

class GreatSword(PowerUp):
    def __init__(self):
        super().__init__("Great Sword", "gs.png")

    def apply(self, game_state):
        if self.used:
            return game_state, "Power-up deja folosit!"
        self.used = True
        game_state["scor_multiplier"] = 1.5
        print("Great Sword aplicat: Scorul rundei va fi înmulțit cu 1.5!")
        return game_state, "Great Sword: Scorul rundei va fi înmulțit cu 1.5!"

class LongSword(PowerUp):
    def __init__(self):
        super().__init__("Long Sword", "ls.png")

    def apply(self, game_state):
        if self.used:
            return game_state, "Power-up deja folosit!"
        self.used = True
        outcome = random.random()
        if outcome < 0.55:
            game_state["scor_multiplier"] = 2
            print("Long Sword aplicat: Scorul rundei va fi înmulțit cu 2!")
            return game_state, "Long Sword: Scorul rundei va fi înmulțit cu 2!"
        elif outcome < 0.85:
            print("Long Sword aplicat: Niciun efect.")
            return game_state, "Long Sword: Niciun efect."
        else:
            game_state["scor_multiplier"] = 0.8
            print("Long Sword aplicat: Ai pierdut 1000 de puncte din scorul rundei!")
            return game_state, "Long Sword: Ai pierdut 1000 de puncte din scorul rundei!"

class InsectGlaive(PowerUp):
    def __init__(self):
        super().__init__("Insect Glaive", "ig.png")

    def apply(self, game_state):
        if self.used:
            return game_state, "Power-up deja folosit!"
        self.used = True
        # Elimină jumătate din zonele greșite, fără a elimina zona corectă
        zona_corecta = game_state["zona_corecta"]
        zone_gresite = [zona for zona in game_state["zone_posibile"] if zona != zona_corecta]
        zone_ramase = [zona_corecta] + random.sample(zone_gresite, len(zone_gresite) // 2)
        game_state["zone_posibile"] = zone_ramase
        print("Insect Glaive aplicat: Jumătate din zonele greșite au fost eliminate!")
        return game_state, "Insect Glaive: Jumătate din zonele greșite au fost eliminate!"

class SwordAndShield(PowerUp):
    def __init__(self):
        super().__init__("Sword and Shield", "sns.png")

    def apply(self, game_state):
        if self.used:
            return game_state, "Power-up deja folosit!"
        self.used = True
        game_state["numar_puncte_harta"] = 3
        game_state["scor_multiplier"] = 0.75
        print("Sword and Shield aplicat: Poți plasa 3 puncte pe hartă, dar vei primi 75% din valoare!")
        return game_state, "Sword and Shield: Poți plasa 3 puncte pe hartă, dar vei primi 75% din valoare!"

class ChargeBlade(PowerUp):
    def __init__(self):
        super().__init__("Charge Blade", "cb.png")

    def apply(self, game_state):
        if self.used:
            return game_state, "Power-up deja folosit!"
        self.used = True
        game_state["locatii_extra"] += 1
        print("Charge Blade aplicat: Dacă greșești de 3 ori, vei primi o locație în plus!")
        return game_state, "Charge Blade: Dacă greșești de 3 ori, vei primi o locație în plus!"

class SwitchAxe(PowerUp):
    def __init__(self):
        super().__init__("Switch Axe", "saxe.png")

    def apply(self, game_state):
        if self.used:
            return game_state, "Power-up deja folosit!"
        self.used = True
        game_state["diametru_zona_perfecta"] = 20  # Extinde aria de punctaj perfect
        print("Switch Axe aplicat: Zona pentru un scor perfect s-a dublat (diametru 20px)!")
        return game_state, "Switch Axe: Zona pentru un scor perfect s-a dublat (diametru 20px)!"

class DualBlades(PowerUp):
    def __init__(self):
        super().__init__("Dual Blades", "db.png")

    def apply(self, game_state):
        if self.used:
            return game_state, "Power-up deja folosit!"
        self.used = True
        game_state["numar_puncte_harta"] = 2
        print("Dual Blades aplicat: Poți plasa 2 puncte pe hartă!")
        return game_state, "Dual Blades: Poți plasa 2 puncte pe hartă!"

class HuntingHorn(PowerUp):
    def __init__(self):
        super().__init__("Hunting Horn", "hh.png")

    def apply(self, game_state):
        if self.used:
            return game_state, "Power-up deja folosit!"
        self.used = True
        game_state["scor_bonus"] = 150
        print("Hunting Horn aplicat: Pentru următoarele 3 locații, vei primi 150 de puncte bonus!")
        return game_state, "Hunting Horn: Pentru următoarele 3 locații, vei primi 150 de puncte bonus!"

class Bow(PowerUp):
    def __init__(self):
        super().__init__("Bow", "bow.png")

    def apply(self, game_state):
        if self.used:
            return game_state, "Power-up deja folosit!"
        self.used = True
        game_state["numar_puncte_harta"] = 3
        game_state["timer_powerup"] = 15
        print("Bow aplicat: Poți plasa 3 puncte pe hartă în 15 secunde!")
        return game_state, "Bow: Poți plasa 3 puncte pe hartă în 15 secunde!"

class LightBowgun(PowerUp):
    def __init__(self):
        super().__init__("Light Bowgun", "lbg.png")

    def apply(self, game_state):
        if self.used:
            return game_state, "Power-up deja folosit!"
        self.used = True
        game_state["elimina_platforme_gresite"] = True
        print("Light Bowgun aplicat: Dacă selectezi zona corectă, platformele greșite vor fi eliminate!")
        return game_state, "Light Bowgun: Dacă selectezi zona corectă, platformele greșite vor fi eliminate!"

class HeavyBowgun(PowerUp):
    def __init__(self):
        super().__init__("Heavy Bowgun", "hbg.png")

    def apply(self, game_state):
        if self.used:
            return game_state, "Power-up deja folosit!"
        self.used = True
        game_state["diametru_zona_perfecta"] = 10  # Înjumătățește aria de punctaj perfect
        game_state["scor_multiplier"] = 1.7  # Înmulțește scorul rundei cu 1.7
        print("Heavy Bowgun aplicat: Zona pentru un scor perfect s-a înjumătățit (diametru 10px), dar scorul se înmulțește cu 1.7!")
        return game_state, "Heavy Bowgun: Zona pentru un scor perfect s-a înjumătățit (diametru 10px), dar scorul se înmulțește cu 1.7!"

class Lance(PowerUp):
    def __init__(self):
        super().__init__("Lance", "lance.png")

    def apply(self, game_state):
        if self.used:
            return game_state, "Power-up deja folosit!"
        self.used = True
        game_state["locatii_extra"] += 1
        print("Lance aplicat: Dacă greșești, vei primi o locație în plus!")
        return game_state, "Lance: Dacă greșești, vei primi o locație în plus!"

class Gunlance(PowerUp):
    def __init__(self):
        super().__init__("Gunlance", "gl.png")

    def apply(self, game_state):
        if self.used:
            return game_state, "Power-up deja folosit!"
        self.used = True
        game_state["scor_bonus"] = 2000
        print("Gunlance aplicat: Dacă ghicești corect 3 locații consecutive, vei primi 2000 de puncte bonus!")
        return game_state, "Gunlance: Dacă ghicești corect 3 locații consecutive, vei primi 2000 de puncte bonus!"

class Hammer(PowerUp):
    def __init__(self):
        super().__init__("Hammer", "hammer.png")

    def apply(self, game_state):
        if self.used:
            return game_state, "Power-up deja folosit!"
        self.used = True
        outcome = random.random()
        if outcome < 0.95:
            game_state["sari_locatie"] = True
            game_state["locatii_extra"] += 1
            print("Hammer aplicat: Ai sărit peste locația curentă și ai primit o locație în plus!")
            return game_state, "Hammer: Ai sărit peste locația curentă și ai primit o locație în plus!"
        else:
            game_state["sari_locatie"] = True
            game_state["scor_bonus"] = 2500
            game_state["locatii_extra"] += 1
            print("Hammer aplicat: Ai sărit peste locația curentă, ai primit 2500 de puncte și o locație în plus!")
            return game_state, "Hammer: Ai sărit peste locația curentă, ai primit 2500 de puncte și o locație în plus!"

def get_random_powerup():
    powerups = [
        GreatSword(),
        LongSword(),
        InsectGlaive(),
        SwordAndShield(),
        ChargeBlade(),
        SwitchAxe(),
        DualBlades(),
        HuntingHorn(),
        Bow(),
        LightBowgun(),
        HeavyBowgun(),
        Lance(),
        Gunlance(),
        Hammer()
    ]
    return random.choice(powerups)