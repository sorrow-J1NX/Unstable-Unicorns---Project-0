import copy
import math
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

# IMAGES
IMAGE_FOLDER = r"C:\Users\benjarth\PycharmProjects\Unstable-Unicorns---Project-0\Card Images"
IMAGE_EXTENSION = ".png"
CARD_BACK = IMAGE_FOLDER + "card_back" + IMAGE_EXTENSION


#players (stables)

p1 = []
p2 = []
p3 = []
p4 = []
p5 = []
p6 = []
p7 = []
p8 = []

#players (hands)

h1 = []
h2 = []
h3 = []
h4 = []
h5 = []
h6 = []
h7 = []
h8 = []

root = tk.Tk()
root.title("Unstable Unicorns")

#How many players are playing?
players = simpledialog.askinteger("Players", "How many players? (2-8)",
                                  minvalue=2, maxvalue=8, parent=root)
if players is None:
    root.destroy()
    raise SystemExit

stables = [p1, p2, p3, p4, p5, p6, p7, p8][:players]
hands = [h1, h2, h3, h4, h5, h6, h7, h8][:players]

WIN_UNICORNS = 7      #win condition
START_HAND = 4
HAND_LIMIT = 7


#create cards and decks

class BabyCorns:
    path = IMAGE_FOLDER
    def __init__(self, type, name, amount, image):
        self.name = name
        self.type = type
        self.amount = amount
        self.ability = None
        self.image = self.path + "\\" + type + "_" + image + IMAGE_EXTENSION

class BasicCorns:
    path = IMAGE_FOLDER
    def __init__(self, type, name, amount, image):
        self.name = name
        self.type = type
        self.amount = amount
        self.ability = None
        self.image = self.path + "\\" + type + "_" + image + IMAGE_EXTENSION

class MagicCorns:
    path = IMAGE_FOLDER
    def __init__(self, type, name, amount, ability, image):
        self.name = name
        self.type = type
        self.amount = amount
        self.ability = ability
        self.image = self.path + "\\" + type + "_" + image + IMAGE_EXTENSION

class MagicSpell:
    path = IMAGE_FOLDER
    def __init__(self, type, name, amount, ability, image):
        self.name = name
        self.type = type
        self.amount = amount
        self.ability = ability
        self.image = self.path + "\\" + type + "_" + image + IMAGE_EXTENSION


class Interrupts:
    path = IMAGE_FOLDER
    def __init__(self, type, name, amount, ability, image):
        self.name = name
        self.type = type
        self.amount = amount
        self.ability = ability
        self.image = self.path + "\\" + type + "_" + image + IMAGE_EXTENSION


class Upgrades:
    path = IMAGE_FOLDER
    def __init__(self, type, name, amount, ability, image):
        self.name = name
        self.type = type
        self.amount = amount
        self.ability = ability
        self.image = self.path + "\\" + type + "_" + image + IMAGE_EXTENSION


class Downgrades:
    path = IMAGE_FOLDER
    def __init__(self, type, name, amount, ability, image):
        self.name = name
        self.type = type
        self.amount = amount
        self.ability = ability
        self.image = self.path + "\\" + type + "_" + image + IMAGE_EXTENSION


UNICORN_TYPES = ("bby", "bsc", "mgc")

def is_unicorn(card):
    return card.type in UNICORN_TYPES


# GAME STATE
nursery = []
deck = []
discard_pile = []
current = 0          # whose turn it is
actions_left = 0
hidden = True        # hides the hand while passing the screen around
game_over = False


# CARD ABILITIES

def draw_card(p):
    global deck, discard_pile
    if len(deck) == 0 and len(discard_pile) > 0:
        deck = discard_pile[:]
        discard_pile.clear()
        random.shuffle(deck)
    if len(deck) > 0:
        hands[p].append(deck.pop())

def discard_from_hand(p, prompt):
    if len(hands[p]) == 0:
        return
    i = choose_card(prompt, hands[p])
    discard_pile.append(hands[p].pop(i))

def protected(owner):
    # an upgrade with the "shield" tag protects the whole stable
    for c in stables[owner]:
        if c.ability == "shield":
            return True
    return False

def enemy_unicorns(p):
    found = []
    for owner in range(players):
        if owner != p and not protected(owner):
            for c in stables[owner]:
                if is_unicorn(c):
                    found.append((owner, c))
    return found

def send_away(owner, card):
    # babies go home to the nursery, everything else gets discarded
    stables[owner].remove(card)
    if card.type == "bby":
        nursery.append(card)
    else:
        discard_pile.append(card)

def rhinocorn(p):
    # destroy a unicorn in another stable
    targets = enemy_unicorns(p)
    if len(targets) == 0:
        messagebox.showinfo("Rhinocorn", "No unicorns can be destroyed.")
        return
    i = choose_card("Rhinocorn: destroy which unicorn?",
                    [t[1] for t in targets],
                    ["Player " + str(t[0] + 1) for t in targets])
    send_away(targets[i][0], targets[i][1])

def llamacorn(p):
    # draw 2 cards, then discard 1
    draw_card(p)
    draw_card(p)
    discard_from_hand(p, "Llamacorn: discard a card")


def card_surge(p):
    draw_card(p)
    draw_card(p)

def seductive_unicorn(p):
    # steal a unicorn from another stable
    targets = enemy_unicorns(p)
    if len(targets) == 0:
        messagebox.showinfo("Borrow", "No unicorns can be taken.")
        return
    i = choose_card("Borrow: take which unicorn?",
                    [t[1] for t in targets],
                    ["Player " + str(t[0] + 1) for t in targets])
    stables[targets[i][0]].remove(targets[i][1])
    stables[p].append(targets[i][1])

def second_chance(p):
    # put a unicorn from the discard pile into your stable
    options = [c for c in discard_pile if is_unicorn(c)]
    if len(options) == 0:
        messagebox.showinfo("Second Chance", "No unicorns in the discard pile.")
        return
    i = choose_card("Second Chance: revive which unicorn?", options)
    card = options[i]
    discard_pile.remove(card)
    stables[p].append(card)
    if card.type == "mgc" and card.ability is not None:
        card.ability(p)


# THE CARDS

#nursery cards
red = BabyCorns("bby", "Red Baby Unicorn", 1, "red")
pink = BabyCorns("bby", "Pink Baby Unicorn", 1, "pink")
orange = BabyCorns("bby", "Orange Baby Unicorn", 1, "orange")
yellow = BabyCorns("bby", "Yellow Baby Unicorn", 1, "yellow")
green = BabyCorns("bby", "Green Baby Unicorn", 1, "green")
blue = BabyCorns("bby", "Blue Baby Unicorn", 1, "blue")
purple = BabyCorns("bby", "Purple Baby Unicorn", 1, "purple")
black = BabyCorns("bby", "Black Baby Unicorn", 1, "black")
white = BabyCorns("bby", "White Baby Unicorn", 1, "white")
brown = BabyCorns("bby", "Brown Baby Unicorn", 1, "brown")
rainbow = BabyCorns("bby", "Rainbow Baby Unicorn", 1, "rainbow")
death = BabyCorns("bby", "Death Baby Unicorn", 1, "death")
narwhal = BabyCorns("bby", "Baby Narwhal", 1, "narwhal")

nursery_templates = [red, pink, orange, yellow, green, blue, purple,
                     black, white, brown, rainbow, death, narwhal]


#main deck

#basics
Red = BasicCorns("bsc", "Red Unicorn", 3, "red")
Orange = BasicCorns("bsc", "Orange Unicorn", 3, "orange")
Yellow = BasicCorns("bsc", "Yellow Unicorn", 3, "yellow")
Green = BasicCorns("bsc", "Green Unicorn", 3, "green")
Blue = BasicCorns("bsc", "Blue Unicorn", 3, "blue")
Indigo = BasicCorns("bsc", "Indigo Unicorn", 3, "indigo")
Purple = BasicCorns("bsc", "Purple Unicorn", 3, "purple")
Narwhal = BasicCorns("bsc", "Narwhal", 3, "narwhal")


#magics
Rhinocorn = MagicCorns("mgc", "Rhinocorn", 1, rhinocorn, "rhinocorn")
Llamacorn = MagicCorns("mgc", "Llamacorn", 2, llamacorn, "llamacorn")

#spells
CardSurge = MagicSpell("spl", "Card Surge", 3, card_surge, "cardsurge")

#interrupts (play one on another player's turn to cancel the card they play)
Neigh = Interrupts("ins", "Neigh", 6, None, "neigh")

#upgrades
RainbowAura = Upgrades("upg", "Rainbow Aura", 2, "shield", "rainbowaura")
DoubleDutch = Upgrades("upg", "Double Dutch", 2, "extra_draw", "doubledutch")

#downgrades
Pandamonium = Downgrades("dwn", "Pandamonium", 100, "blind", "pandamonium")

main_templates = [Red, Orange, Yellow, Green, Blue, Indigo, Purple, Narwhal,
                  Rhinocorn, Llamacorn, CardSurge,
                  Neigh, RainbowAura, DoubleDutch,
                  Pandamonium]


def build_pile(templates):
    pile = []
    for template in templates:
        for i in range(template.amount):
            pile.append(copy.copy(template))
    return pile


# GUI HELPERS
BIG = (96, 134)       # card size in your hand
SMALL = (62, 87)      # card size in stables
COLORS = {"bby": "#f8b4d9", "bsc": "#c9b8f5", "mgc": "#8fd3f4",
          "spl": "#ffd479", "int": "#ff8a80", "upg": "#a5e8a0", "dwn": "#b0b0b0"}

image_cache = {}   # keeps pictures alive

def load_image(path, size):
    key = (path, size)
    if key in image_cache:
        return image_cache[key]
    try:
        img = tk.PhotoImage(file=path)
        shrink = max(math.ceil(img.width() / size[0]),
                     math.ceil(img.height() / size[1]), 1)
        if shrink > 1:
            img = img.subsample(shrink)
    except tk.TclError:
        img = None   # creates placeholder if not found
    image_cache[key] = img
    return img


def card_widget(parent, card, size, command=None, label=None):
    w, h = size
    c = tk.Canvas(parent, width=w, height=h, highlightthickness=1,
                  highlightbackground="#333")
    img = load_image(card.image, size)
    if img is not None:
        c.create_image(w // 2, h // 2, image=img)
    else:
        c.create_rectangle(0, 0, w, h, fill=COLORS[card.type], outline="")
        c.create_text(w // 2, h // 2, text=card.name, width=w - 8,
                      font=("Arial", 8 if w < 80 else 10, "bold"))
    if label:
        c.create_rectangle(0, h - 14, w, h, fill="#222", outline="")
        c.create_text(w // 2, h - 7, text=label, fill="white", font=("Arial", 8))
    if command is not None:
        c.bind("<Button-1>", lambda e: command())
        c.configure(cursor="hand2")
    return c

def choose_card(title, cards, labels=None):
    # pop-up that makes the player click one card; returns its index
    result = []
    win = tk.Toplevel(root)
    win.title(title)
    win.transient(root)
    win.protocol("WM_DELETE_WINDOW", lambda: None)
    tk.Label(win, text=title, font=("Arial", 12, "bold")).pack(padx=10, pady=6)
    frame = tk.Frame(win)
    frame.pack(padx=10, pady=6)

    def pick(i):
        result.append(i)
        win.destroy()

    for i, card in enumerate(cards):
        lab = labels[i] if labels else None
        w = card_widget(frame, card, BIG, command=lambda i=i: pick(i), label=lab)
        w.grid(row=i // 6, column=i % 6, padx=3, pady=3)
    win.grab_set()
    root.wait_window(win)
    return result[0]

def ask_yes(title, text):
    return messagebox.askyesno(title, text, parent=root)


# GAME LOGIC

def unicorn_count(p):
    return len([c for c in stables[p] if is_unicorn(c)])

def can_win(p):
    for c in stables[p]:
        if c.ability == "blind":
            return False
    return unicorn_count(p) >= WIN_UNICORNS

def hand_limit(p):
    for c in stables[p]:
        if c.ability == "hand5":
            return 5
    return HAND_LIMIT

def neigh_check(p, card):
    # every other player (in order) holding a Neigh may cancel the card
    for step in range(1, players):
        q = (p + step) % players
        neighs = [c for c in hands[q] if c.type == "int"]
        if len(neighs) > 0:
            if ask_yes("Player " + str(q + 1) + " - Neigh?",
                       "Player " + str(p + 1) + " is playing " + card.name +
                       ".\nPlayer " + str(q + 1) + ", play a Neigh to cancel it?"):
                hands[q].remove(neighs[0])
                discard_pile.append(neighs[0])
                return True
    return False

def play_card(i):
    global actions_left
    if hidden or game_over or actions_left < 1:
        return
    p = current
    card = hands[p][i]

    if card.type == "int":
        messagebox.showinfo("Interrupt", "Neigh can only be played on someone else's turn.")
        return

    hands[p].pop(i)
    if neigh_check(p, card):
        discard_pile.append(card)
        messagebox.showinfo("Neigh!", card.name + " was cancelled.")
        actions_left -= 1
        finish_action()
        return

    if is_unicorn(card):
        stables[p].append(card)
        if card.type == "mgc" and card.ability is not None:
            card.ability(p)
    elif card.type == "spl":
        card.ability(p)
        discard_pile.append(card)
    elif card.type == "upg":
        stables[p].append(card)
    elif card.type == "dwn":
        others = [q for q in range(players) if q != p]
        names = ["Player " + str(q + 1) for q in others]
        dummy_cards = [stables_label_card(q) for q in others]
        k = choose_card("Give " + card.name + " to which player?", dummy_cards, names)
        stables[others[k]].append(card)

    actions_left -= 1
    finish_action()

def stables_label_card(q):
    # a little stand-in card used when choosing a player
    return BasicCorns("bsc", "Player " + str(q + 1), 0, "player")

def draw_action():
    global actions_left
    if hidden or game_over or actions_left < 1:
        return
    draw_card(current)
    actions_left -= 1
    finish_action()

def finish_action():
    global game_over
    refresh()
    # win condition
    for p in range(players):
        if can_win(p):
            game_over = True
            refresh()
            messagebox.showinfo("Game over", "Player " + str(p + 1) + " wins with " +
                                str(unicorn_count(p)) + " unicorns!")
            return
    end_turn()

def end_turn():
    global current, hidden
    #end phase: discard down to the hand limit
    p = current
    while len(hands[p]) > hand_limit(p):
        refresh()
        discard_from_hand(p, "Player " + str(p + 1) + ": discard down to " +
                          str(hand_limit(p)) + " cards")
    current = (current + 1) % players
    hidden = True
    refresh()

def begin_turn():
    global hidden, actions_left
    if game_over:
        return
    hidden = False
    p = current
    #beginning / draw phase
    draw_card(p)
    for c in stables[p]:
        if c.ability == "extra_draw":
            draw_card(p)
    #action phase
    actions_left = 1
    refresh()


# DRAW THE BOARD
status = tk.Label(root, font=("Arial", 13, "bold"))
status.pack(pady=4)

board_outer = tk.Frame(root)
board_outer.pack(fill="both", expand=True, padx=6)
board_canvas = tk.Canvas(board_outer, height=360)
scroll = tk.Scrollbar(board_outer, orient="vertical", command=board_canvas.yview)
board_canvas.configure(yscrollcommand=scroll.set)
scroll.pack(side="right", fill="y")
board_canvas.pack(side="left", fill="both", expand=True)
board = tk.Frame(board_canvas)
board_canvas.create_window((0, 0), window=board, anchor="nw")
board.bind("<Configure>", lambda e: board_canvas.configure(scrollregion=board_canvas.bbox("all")))

piles_label = tk.Label(root, font=("Arial", 10))
piles_label.pack(pady=2)

hand_frame = tk.Frame(root, bd=2, relief="groove")
hand_frame.pack(fill="x", padx=6, pady=6)

def refresh():
    for w in board.winfo_children():
        w.destroy()
    for w in hand_frame.winfo_children():
        w.destroy()

    # stables
    for p in range(players):
        bg = "#fff3b0" if p == current else "#f0f0f0"
        row = tk.Frame(board, bg=bg, bd=1, relief="solid")
        row.pack(fill="x", pady=2)
        text = "Player " + str(p + 1) + "\n" + str(unicorn_count(p)) + "/" + str(WIN_UNICORNS)
        tk.Label(row, text=text, bg=bg, width=9, font=("Arial", 10, "bold")).pack(side="left")
        for card in stables[p]:
            card_widget(row, card, SMALL).pack(side="left", padx=2, pady=2)

    piles_label.config(text="Deck: " + str(len(deck)) + "   Discard: " +
                       str(len(discard_pile)) + "   Nursery: " + str(len(nursery)))

    # hand
    if game_over:
        status.config(text="Game over!")
        return
    if hidden:
        status.config(text="Pass to Player " + str(current + 1))
        tk.Button(hand_frame, text="Player " + str(current + 1) + " is ready - start turn",
                  font=("Arial", 12), command=begin_turn).pack(pady=20)
        return

    status.config(text="Player " + str(current + 1) + "'s turn - play a card or draw one")
    tk.Button(hand_frame, text="Draw a card\n(use your action)", command=draw_action).pack(side="left", padx=8)
    for i, card in enumerate(hands[current]):
        card_widget(hand_frame, card, BIG, command=lambda i=i: play_card(i)).pack(side="left", padx=3, pady=4)


# SET UP
nursery = build_pile(nursery_templates)
deck = build_pile(main_templates)
random.shuffle(deck)

#baby unicorn choosing
order = 0
while order != players:
    i = choose_card("Player " + str(order + 1) + ": choose your baby unicorn", nursery)
    stables[order].append(nursery.pop(i))
    order += 1

#deal starting hands
for p in range(players):
    for n in range(START_HAND):
        draw_card(p)

# TURN LOOP is handled by the buttons:
refresh()
root.mainloop()
