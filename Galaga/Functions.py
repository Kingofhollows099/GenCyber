import pygame as pg
HS = open("Highscore.txt", "r+")

def Finish(score):
    coins += score // 10
    oldScore = score
    if score > HS.read():
        HS.write(score)
    score = 0
    