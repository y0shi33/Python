import random

class Player:
    def __init__(self, name, dmg, HP, exp, item) -> None:
        self.HP = HP
        self.item = item
        self.name = name
        self.exp = exp
        self.dmg = dmg

    def ShowStats(self):
        print(self.name, end=" * ")
        print("dmg",self.dmg, end=" * ")
        print("HP",self.HP, end=" * ")
        print("exp",self.exp, end=" * ")
        
        self.item.ShowStats()
    
#Moves_______________________________________________________________

    def Attack(self):
        return self.dmg + self.item.Use() + self.exp
    
    def Heal(self):
        if self.HP > 100:
            self.HP = 100

        return random.randint(20, 50)
    
#HP__________________________________________________________________

    def DecreaseHP(self, mod):
        self.HP -= mod

    def IncreaseHP(self, mod):
        self.HP += mod

#LVL__________________________________________________________________

    def level_up(self):
        self.exp += 1