import random
import os
import time
from item import *
from player import *

class Combat:
    def __init__(self):
        self.team1 = []
        self.team2 = []

#adding characters________________________________________________________________
    def add_player(self, player):
        self.team1.append(player)

    def add_opponent(self, player):
        self.team2.append(player)
    
#showing characters_______________________________________________________________

    def show_team(self, team):
        i = 0
        if team == 1:
            for player in self.team1:
                print(i, ": ", end="")
                player.ShowStats()
                i += 1
        else:
            for player in self.team2:
                print(i, ": ", end="")
                player.ShowStats()
                i += 1

#saving / loading_________________________________________________________________
    def save(self):
        with open("Gamesave.txt", "w") as file:
            file.write(f"{len(self.team1)} {len(self.team2)}\n")
            for player in self.team1:
                file.write(f"{player.name} {player.dmg} {player.HP} {player.exp} "
                           f"{player.item.name} {player.item.dmg} {player.item.critDMG} {player.item.critChance}\n")

            for opponent in self.team2:
                file.write(f"{opponent.name} {opponent.dmg} {opponent.HP} {opponent.exp} "
                           f"{opponent.item.name} {opponent.item.dmg} {opponent.item.critDMG} {opponent.item.critChance}\n")

        print("Game saved successfully")

    def load(self):
        if os.path.exists("Gamesave.txt") == False:
            print("No saved game found")

        with open("Gamesave.txt", "r") as file:
            lines = file.readlines()
            counts = [int(p) for p in lines[0].split()]
            player_count = counts[0]

            for line in lines[1:1+player_count]:
                player_data = line.split()
                name = player_data[0]
                dmg = int(player_data[1])
                HP = int(player_data[2])
                exp = int(player_data[3])
                item_name = player_data[4]
                item_dmg = float(player_data[5])
                item_critDMG = float(player_data[6])
                item_critChance = float(player_data[7])

                item = Item(item_name, item_dmg, item_critDMG, item_critChance)
                player = Player(name, dmg, HP, exp, item)
                self.team1.append(player)

            for line in lines[1+player_count:]:
                opponent_data = line.split()
                name = opponent_data[0]
                dmg = float(opponent_data[1])
                HP = float(opponent_data[2])
                exp = float(opponent_data[3])
                item_name = opponent_data[4]
                item_dmg = float(opponent_data[5])
                item_critDMG = float(opponent_data[6])
                item_critChance = float(opponent_data[7])

                item = Item(item_name, item_dmg, item_critDMG, item_critChance)
                opponent = Player(name, dmg, HP, exp, item)
                self.team2.append(opponent)

        print("Game loaded successfully")

#fighting________________________________________________________________

    def fight(self):
        while True:
            os.system("cls")
            self.show_team(1)
            print("-------------------------------")
            self.show_team(2)
            player_index = int(input("Pick Player: "))
            os.system("cls")
            self.team1[player_index].ShowStats()
            print("-------------------------------")
            self.show_team(2)
            opponent_index = int(input("Pick Opponent: "))
            os.system("cls")
            move_option = input("Do you want to attack or cast a healing spell? (attack (0) / cast healing (1)):")

            #attack__________________________________________________________________
            if move_option == "0":
                self.team1[player_index].ShowStats()
                print("-------------------------------")
                self.team2[opponent_index].ShowStats()
                print("Players fighting...")
                time.sleep(3)
                player_dmg = self.team1[player_index].Attack()
                self.team2[opponent_index].DecreaseHP(player_dmg)
                print("Player deals:", player_dmg, "damage to opponent")
                time.sleep(1)

                #spell casting________________________________________________________
            elif move_option == "1":
                if self.team1[player_index].HP >= 100:
                    print('Players HP is already maxed out')
                else:
                    self.team1[player_index].ShowStats()
                    print("-------------------------------")
                    self.team2[opponent_index].ShowStats()
                    print("Casting healing spell...")
                    time.sleep(3)
                    healed_hp = self.team1[player_index].Heal()
                    self.team1[player_index].IncreaseHP(healed_hp)
                    print("Player heals", healed_hp, "health to character.")
                    time.sleep(1)

            if self.team2[opponent_index].HP > 0:
                self.team1[player_index].DecreaseHP(self.team2[opponent_index].dmg)
                print("Opponent deals", self.team2[opponent_index].dmg)
            else:
                print("Opponent is dead")
                self.team2.pop(opponent_index)
                self.team1[player_index].level_up()
            
            option = input("Continue? (y/n): ")

            if option.lower() == "y":
                continue
            elif option.lower() == "n":
                self.save()
                break

c = Combat()

load_option = input("Do you want to start a new game or load a saved game? (new (0) / load (1)): ")
if load_option == "1":
    c.load()
else:
    c.add_player(Player("Andrzej", 10, 100, 0, Item("Sword", 30, 15, 30)))
    c.add_player(Player("Henio", 10, 100, 0, Item("Axe", 25, 20, 35)))
    c.add_opponent(Player("Julek", 10, 100, 0, Item("Keyboard", 10, 45, 60)))
    c.add_opponent(Player("Szymon", 10, 100, 0, Item("Axe", 25, 20, 35)))

c.fight()