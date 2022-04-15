import arcade
import gameConstants as gConst
import math as mt
from Objects import Domino

class GameTable: # Objeto Game (Lista de objetos dominos)

    def __init__(self, breakLength, currentPlayer, centerX, centerY):
        self.breakLength = breakLength
        self.currentPlayer = currentPlayer
        self.centerX = centerX
        self.centerY = centerY
        self.gameRound = 1
        self.gamePlay = 0
        self.tableList = arcade.SpriteList()

    def add_dom_to_end(self, domino):
        self.tableList.append(domino)
        self.readjustment_table_position()

    def add_dom_to_start(self, domino):
        self.tableList.insert(0, domino)
        Atualiza = Domino.Domino("Atualiza", 1000, "Atualiza", 1000)
        self.tableList.append(Atualiza)
        self.tableList.remove(Atualiza)
        self.readjustment_table_position()

    def set_scale(self, value):
        for dom in self.tableList:
            dom.scale = value

    def print_list(self):
        print("-----------------------")
        print("Jogada: " + str(self.gamePlay))
        for dom in self.tableList:
            print(dom.leftFaceNum)
        print("-----------------------")

    def readjustment_table_position(self):
        for i, dom in enumerate(self.tableList):
            dom.scale = 0.07
            if len(self.tableList) % 2 == 0: # par
                dom_at_enter = ((len(self.tableList) / 2) + .5) - 1
                if i < dom_at_enter:
                    dom.position = self.centerX - ((dom.width + 10) * (dom_at_enter - i)), self.centerY
                elif i > dom_at_enter:
                    dom.position = self.centerX + ((dom.width + 10) * (i - dom_at_enter)), self.centerY
            else: # impar
                dom_at_enter = (mt.ceil(len(self.tableList) / 2) - 1)
                if i == dom_at_enter:
                    dom.position = self.centerX, self.centerY
                elif i < dom_at_enter:
                    dom.position = self.centerX - ((dom.width + 10) * (dom_at_enter - i)), self.centerY
                elif i > dom_at_enter:
                    dom.position = self.centerX + ((dom.width + 10) * (i - dom_at_enter)), self.centerY