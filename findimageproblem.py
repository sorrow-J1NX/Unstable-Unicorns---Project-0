import copy
import math
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

# IMAGES
IMAGE_FOLDER = r"C:\Users\benjarth\PycharmProjects\Unstable-Unicorns---Project-0\Card Images"
IMAGE_EXTENSION = ".png"
CARD_BACK = IMAGE_FOLDER + "card_back" + IMAGE_EXTENSION


class BabyCorns:
    path = IMAGE_FOLDER
    def __init__(self, type, name, amount, image):
        self.name = name
        self.type = type
        self.amount = amount
        self.ability = None
        self.image = type + "_" + image + IMAGE_EXTENSION


red = BabyCorns("bby", "Red Baby Unicorn", 1, "red")

print(red.path)
print(red.image)