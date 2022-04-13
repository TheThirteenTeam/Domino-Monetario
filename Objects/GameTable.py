import arcade
import gameConstants as gConst
import math as mt

class GameTable: # Objeto Game (Lista de objetos dominos)

    def __init__(self, breakLength, currentPlayer, centerX, centerY):
        self.breakLength = breakLength
        self.currentPlayer = currentPlayer
        self.centerX = centerX
        self.centerY = centerY
        self.gameRound = 1
        self.gamePlay = 1
        self.tableList = arcade.SpriteList()

    def add_domino(self, domino):
        self.tableList.append(domino)
        self.readjustment_table_position()

    def readjustment_table_position(self):
        for i, dom in enumerate(self.tableList):
            if len(self.tableList) % 2 == 0: # par
                dom_at_enter = (self.tableList / 2)
                dom.position = self.centerX + ((dom.width + 20) * i), self.centerY
            else: # impar
                print("impar")
                dom_at_enter = (mt.ceil(len(self.tableList) / 2) - 1)
                if i == dom_at_enter:
                    dom.position = self.centerX, self.centerY
                elif i < dom_at_enter:
                    dom.position = self.centerX - ((dom.width + 10) * (dom_at_enter - i)), self.centerY
                elif i > dom_at_enter:
                    dom.position = self.centerX + ((dom.width + 10) * (i - dom_at_enter)), self.centerY

