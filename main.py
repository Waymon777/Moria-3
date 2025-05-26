import pygame
import sys
import random
import math
import traceback
import json
import os
import logging
logging.basicConfig(level=logging.DEBUG)
import cv2

def play_intro_video(video_path):
    global screen

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Erreur : impossible de lire la vidéo.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = int(700 / fps)

    # ✅ Fondu AVANT la vidéo
    fade(screen, fade_in=True)

    playing = True
    skip = False

    while playing and not skip:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                cap.release()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    skip = True

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, screen.get_size())
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        screen.blit(frame_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(frame_delay)

    cap.release()

    # ✅ Fondu APRÈS la vidéo
    fade(screen, fade_in=False)

    # Restaure la fenêtre de jeu
    screen = pygame.display.set_mode((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE + HUD_HEIGHT))
    resize_assets()



# === CONFIGURATION ===
TILE_SIZE = 24
MAP_WIDTH = 72
MAP_HEIGHT = 43
HUD_HEIGHT = 48
ASSETS_DIR = "assets/"

# === INITIALISATION DE PYGAME (doit être AVANT tout convert_alpha) ===
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE + HUD_HEIGHT))
pygame.display.set_caption("MORIA 3")
clock = pygame.time.Clock()
pygame.mixer.music.load(ASSETS_DIR + "musiquelugubre.mp3")
pygame.mixer.music.set_volume(0.5)  # 0.0 à 1.0
pygame.mixer.music.play(-1)  # -1 = boucle infinie


# === CHARGEMENT ASSETS ===
def load_scaled(filename):
    return pygame.transform.scale(pygame.image.load(ASSETS_DIR + filename), (TILE_SIZE, TILE_SIZE))

def load_button(name, file, size=(200, 50)):
    image = pygame.image.load(ASSETS_DIR + file).convert_alpha()
    return pygame.transform.scale(image, size)

# === BACKGROUNDS (ces images sont plein écran donc pas scalées avec TILE_SIZE) ===
background_img = pygame.image.load(ASSETS_DIR + 'fonddecranmoria3.png')
background_img = pygame.transform.scale(background_img, (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE + HUD_HEIGHT))
gameover_img = pygame.image.load(ASSETS_DIR + 'gameover_image.png')
gameover_img = pygame.transform.scale(gameover_img, (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE + HUD_HEIGHT))
instructions_img = pygame.image.load(ASSETS_DIR + 'instructionz_image.png')
instructions_img = pygame.transform.scale(instructions_img, (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE + HUD_HEIGHT))

# === BOUTONS ===
button_images = {
    "start_game": load_button("start_game", "button_start_game.png"),
    "instructions": load_button("instructions", "button_instructions.png"),
    "scores": load_button("scores", "button_scores.png"),
    "quit": load_button("quit", "button_quit.png"),
    "return": load_button("return", "return_button.png")
}

# ===== SONS ======
sounds = {
    "hit": pygame.mixer.Sound(ASSETS_DIR + "hit.mp3"),
    "miss": pygame.mixer.Sound(ASSETS_DIR + "miss.mp3"),
    "pickup": pygame.mixer.Sound(ASSETS_DIR + "pickup.mp3"),
    "Castarspickup": pygame.mixer.Sound(ASSETS_DIR + "moneypickup.mp3"),
    "drink": pygame.mixer.Sound(ASSETS_DIR + "drink.mp3"),
    "scroll": pygame.mixer.Sound(ASSETS_DIR + "lectureparchemin.mp3"),
    "changementniveau": pygame.mixer.Sound(ASSETS_DIR + "changementniveau.mp3"),
    "lancementfleche": pygame.mixer.Sound(ASSETS_DIR + "lancementfleche.mp3"),
    "entreedansmine": pygame.mixer.Sound(ASSETS_DIR + "entreedansmine.mp3"),
}

# === CURSEUR GANTELET ===
cursor_img = pygame.image.load("assets/cursor_gauntlet.png").convert_alpha()
cursor_img = pygame.transform.scale(cursor_img, (64, 64))  # selon taille voulue
pygame.mouse.set_visible(False)

# === JOUEUR ===
player_up = load_scaled('player_up.png')
player_down = load_scaled('player_down.png')
player_left = load_scaled('player_left.png')
player_right = load_scaled('player_right.png')

# === SERPENT ===
serpent_up = load_scaled('serpent_up.png')
serpent_down = load_scaled('serpent_down.png')
serpent_left = load_scaled('serpent_left.png')
serpent_right = load_scaled('serpent_right.png')

# === LOUP ===
loup_up = load_scaled('loup_up.png')
loup_down = load_scaled('loup_down.png')
loup_left = load_scaled('loup_left.png')
loup_right = load_scaled('loup_right.png')

# === ARAIGNÉE ===
araignee_up = load_scaled('araignee_up.png')
araignee_down = load_scaled('araignee_down.png')
araignee_left = load_scaled('araignee_left.png')
araignee_right = load_scaled('araignee_right.png')

# === RAT ===
rat_up = load_scaled('rat_up.png')
rat_down = load_scaled('rat_down.png')
rat_left = load_scaled('rat_left.png')
rat_right = load_scaled('rat_right.png')

# === ORC ===
orc_up = load_scaled('orc_up.png')
orc_down = load_scaled('orc_down.png')
orc_left = load_scaled('orc_left.png')
orc_right = load_scaled('orc_right.png')

# === GOBELIN ===
gobelin_up = load_scaled('gobelin_up.png')
gobelin_down = load_scaled('gobelin_down.png')
gobelin_left = load_scaled('gobelin_left.png')
gobelin_right = load_scaled('gobelin_right.png')

# === URUKHAI ===
urukhai_up = load_scaled('urukhai_up.png')
urukhai_down = load_scaled('urukhai_down.png')
urukhai_left = load_scaled('urukhai_left.png')
urukhai_right = load_scaled('urukhai_right.png')

# === WHARG ===
wharg_up = load_scaled('wharg_up.png')
wharg_down = load_scaled('wharg_down.png')
wharg_left = load_scaled('wharg_left.png')
wharg_right = load_scaled('wharg_right.png')


# === ENVIRONNEMENT ===
floor_img = load_scaled('floor.png')
wall_img = load_scaled('wall.png')
treasure_img = load_scaled('treasure.png')
stairs_img = load_scaled('stairs.png')
floorsquelette_img = pygame.image.load("assets/floorsquelette.png").convert_alpha()
floorsquelette_img = pygame.transform.scale(floorsquelette_img, (TILE_SIZE, TILE_SIZE))

floorautel_img = pygame.image.load("assets/floorautel.png").convert_alpha()
floorautel_img = pygame.transform.scale(floorautel_img, (TILE_SIZE, TILE_SIZE))


# === ARMES ===
epeecourte_img = load_scaled('epeecourte.png')
hache_img = load_scaled('hache.png')
sabre_img = load_scaled('sabre.png')
epeelongue_img = load_scaled('epeelongue.png')
arc_img = load_scaled('arc.png')
fleche_img = load_scaled('fleche.png')

# === ARMURES ===
armurecuir_img = load_scaled('armuredecuir.png')
cottemaille_img = load_scaled('cottedemaille.png')
armurefer_img = load_scaled('armureenfer.png')
armureacier_img = load_scaled('armureenacier.png')
mithril_img = load_scaled('armuredemithril.png')

# === DIVERS ===
ration_img = load_scaled('ration.png')
parchemin_img = load_scaled('parchemin.png')


# === IMAGES ITEMS ===
item_images = {
    "Épée courte": epeecourte_img,
    "Hache": hache_img,
    "Sabre": sabre_img,
    "Épée longue": epeelongue_img,
    "Armure de cuir": armurecuir_img,
    "Cotte de maille": cottemaille_img,
    "Armure en fer": armurefer_img,
    "Armure en acier": armureacier_img,
    "Armure de mithril": mithril_img,
    "Ration Alimentaire": ration_img,
    "Arc": arc_img,
    "Flèche": fleche_img,
    "Parchemin": parchemin_img,
    "Dague rouillée": epeecourte_img,
}

item_images.update({
    "Potion bleue": load_scaled("potion.png"),
    "Potion rouge": load_scaled("potion.png"),
    "Potion jaune": load_scaled("potion.png"),
    "Potion grise": load_scaled("potion.png"),
    "Potion mordorée": load_scaled("potion.png"),
    "Potion verte": load_scaled("potion.png"),
})


font_big = pygame.font.Font("assets/fonts/EnchantedLand.otf", 70)
font_small = pygame.font.Font("assets/fonts/EnchantedLand.otf", 45)
font_mini = pygame.font.SysFont(None, 24)
hud_font = pygame.font.Font("assets/fonts/EnchantedLand.otf", 32)
hud_bg_img = pygame.image.load(ASSETS_DIR + 'hud_wood.png')
hud_bg_img = pygame.transform.scale(hud_bg_img, (MAP_WIDTH * TILE_SIZE, HUD_HEIGHT))



# === OBJETS DISPONIBLES ===
scroll_effects = {
    "Zan Eth": "reveal_map",
    "Mok Ra": "confusion",
    "Tur Gul": "strength",
    "Fel Dra": "teleport",
    "Ra Mok": "summon",
    "Xi Zan": "identify",
}
identified_scrolls = set()
waiting_for_scroll_input = False
scroll_input_mode = False

# === POTIONS ===
potion_names = [
    "Potion bleue",
    "Potion rouge",
    "Potion jaune",
    "Potion grise",
    "Potion mordorée",
    "Potion verte"
]

potion_possible_effects = [
    "heal",
    "burn",
    "paralyze",
    "weaken",
    "strength_boost",
    "poison"
]

# Ce dictionnaire sera rempli aléatoirement à chaque partie
potion_effect_map = {}
identified_potions = set()


item_pool = [
    {"name": "Épée courte", "type": "weapon", "atk": 5},
    {"name": "Hache", "type": "weapon", "atk": 7},
    {"name": "Sabre", "type": "weapon", "atk": 10},
    {"name": "Épée longue", "type": "weapon", "atk": 12},
    {"name": "Arc", "type": "weapon", "atk": 2, "range": 5},
    {"name": "Flèche", "type": "ammo", "amount": 1},  # ramassable

    {"name": "Armure de cuir", "type": "armor", "def": 2},
    {"name": "Cotte de maille", "type": "armor", "def": 4},
    {"name": "Armure en fer", "type": "armor", "def": 6},
    {"name": "Armure en acier", "type": "armor", "def": 8},
    {"name": "Armure de mithril", "type": "armor", "def": 10},
    {"name": "Ration Alimentaire", "type": "food", "amount": 200},
]
for name in scroll_effects:
    item_pool.append({"name": name, "type": "scroll", "effect": scroll_effects[name]})

def get_monster_types_for_level(level):
    types = [
        {
            "name": "serpent",
            "hp": 50,
            "dmg": 30,
            "images": {
                "up": serpent_up, "down": serpent_down,
                "left": serpent_left, "right": serpent_right
            }
        },
        {
            "name": "rat",
            "hp": 50,
            "dmg": 25,
            "images": {
                "up": rat_up, "down": rat_down,
                "left": rat_left, "right": rat_right
            }
        },
        {
            "name": "araignée",
            "hp": 50,
            "dmg": 35,
            "images": {
                "up": araignee_up, "down": araignee_down,
                "left": araignee_left, "right": araignee_right
            }
        },
        {
            "name": "loup",
            "hp": 70,
            "dmg": 35,
            "images": {
                "up": loup_up, "down": loup_down,
                "left": loup_left, "right": loup_right
            }
        }
    ]

    if level >= 2:
        types.extend([
            {
                "name": "orc",
                "hp": 80,
                "dmg": 40,
                "images": {
                    "up": orc_up, "down": orc_down,
                    "left": orc_left, "right": orc_right
                }
            },
            {
                "name": "gobelin",
                "hp": 60,
                "dmg": 30,
                "images": {
                    "up": gobelin_up, "down": gobelin_down,
                    "left": gobelin_left, "right": gobelin_right
                }
            }
        ])

    if level >= 3:
        types.extend([
            {
                "name": "uruk-hai",
                "hp": 120,
                "dmg": 50,
                "images": {
                    "up": urukhai_up, "down": urukhai_down,
                    "left": urukhai_left, "right": urukhai_right
                }
            },
            {
                "name": "wharg",
                "hp": 100,
                "dmg": 45,
                "images": {
                    "up": wharg_up, "down": wharg_down,
                    "left": wharg_left, "right": wharg_right
                }
            }
        ])
    return types


# === VARIABLES GLOBALES ===
game_state = "start"
player_name = ""
input_active = False
intro_text = [
    "                                                                       Bienvenue, téméraire Aventurier.",
    "                                                                        Vous allez entrer dans le labyrinthe de la Moria.",
    "                                                                         Mais avant, entrez votre nom, il me sera utile pour écrire sur votre tombe..."
]
intro_display_text = ""
intro_char_index = 0
intro_timer = 0
intro_speed = 2
instruction_line_index = 0
instruction_timer = 0
instruction_interval = 1  # millisecondes entre chaque ligne

player_x = player_y = 1
player_max_health = 200
player_health = player_max_health
steps_since_last_heal = 0
next_heal_threshold = random.randint(10, 14)
player_strength = 5
player_hit_chance = 0.7
enemy_hit_chance = 0.7
current_direction = "down"
current_level = 1
stairs_position = None
show_inventory = False
inventory = []
hud_message = ""
hud_message_timer = 0
last_action_message = ""
visibility_map = []
treasures = []
arrow_count = 0
is_aiming = False
items_on_map = []
player_items = []
current_weapon = {"name": "Dague rouillée", "atk": 0}
current_armor = {"name": "Chemise de rôdeur", "def": 0}
selection_mode = None  # "weapon", "armor", etc.
selected_item_letter = None
enemies = []
is_dead = False
cause_de_mort = "Mort inconnue"
player_hunger = 400  # Valeur actuelle de faim (max 400)
player_max_hunger = 400  # Faim maximale
turns_since_last_meal = 0
move_counter = 0  # Pour suivre combien de déplacements sans manger
game_over_fade_alpha = 255
game_over_fade_timer = 0
transition_alpha = 255
transition_target = None
transition_in_progress = False
temporary_strength = 0
strength_turns = 0
confused_turns = 0
last_monster_spawn_time = 0
max_enemies_on_map = 10
player_kill_count = 0
next_hp_bonus = random.randint(3, 6)
turn_messages = []
waiting_for_potion_input = False
potion_input_mode = False
potion_handler = None  # pour stocker le gestionnaire
special_floor_decor = []
fullscreen = False
windowed_size = (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE + HUD_HEIGHT)

def fade(surface, fade_in=True, speed=10, delay=20):
    fade_surface = pygame.Surface(surface.get_size())
    fade_surface.fill((0, 0, 0))

    if fade_in:
        alpha_range = range(255, -1, -speed)
    else:
        alpha_range = range(0, 256, speed)

    for alpha in alpha_range:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        fade_surface.set_alpha(alpha)
        surface.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(delay)


def toggle_fullscreen():
    global fullscreen, screen, TILE_SIZE, background_img, hud_bg_img

    fullscreen = not fullscreen
    if fullscreen:
        info = pygame.display.Info()
        screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)

        # Calcul d'un nouveau TILE_SIZE adapté à la résolution
        new_tile_w = info.current_w // MAP_WIDTH
        new_tile_h = (info.current_h - HUD_HEIGHT) // MAP_HEIGHT
        TILE_SIZE = min(new_tile_w, new_tile_h)

    else:
        screen = pygame.display.set_mode(windowed_size)
        TILE_SIZE = 24  # Valeur par défaut

    # Recaler les assets à la nouvelle taille
    resize_assets()

def resize_assets():
    global floor_img, wall_img, treasure_img, stairs_img
    global floorsquelette_img, floorautel_img
    global background_img, hud_bg_img
    global player_up, player_down, player_left, player_right
    global player_health, font_big, font_small, font_mini, hud_font

    def rescale(img):
        return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

    floor_img = rescale(pygame.image.load(ASSETS_DIR + 'floor.png'))
    wall_img = rescale(pygame.image.load(ASSETS_DIR + 'wall.png'))
    treasure_img = rescale(pygame.image.load(ASSETS_DIR + 'treasure.png'))
    stairs_img = rescale(pygame.image.load(ASSETS_DIR + 'stairs.png'))
    floorsquelette_img = rescale(pygame.image.load(ASSETS_DIR + 'floorsquelette.png'))
    floorautel_img = rescale(pygame.image.load(ASSETS_DIR + 'floorautel.png'))

    player_up = rescale(pygame.image.load(ASSETS_DIR + 'player_up.png'))
    player_down = rescale(pygame.image.load(ASSETS_DIR + 'player_down.png'))
    player_left = rescale(pygame.image.load(ASSETS_DIR + 'player_left.png'))
    player_right = rescale(pygame.image.load(ASSETS_DIR + 'player_right.png'))

    hud_bg_img = pygame.transform.scale(pygame.image.load(ASSETS_DIR + 'hud_wood.png'),
                                        (MAP_WIDTH * TILE_SIZE, HUD_HEIGHT))
    background_img = pygame.transform.scale(pygame.image.load(ASSETS_DIR + 'fonddecranmoria3.png'),
                                            (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE + HUD_HEIGHT))



# ----------------------------
# Tableau des scores
# ----------------------------
def save_score():
    global player_name, current_level, inventory, cause_de_mort

    total_castars = sum(item["amount"] for item in inventory if isinstance(item, dict) and item.get("type") == "gold")

    score_entry = {
        "nom": player_name,
        "cause": cause_de_mort,
        "niveau": current_level,
        "castars": total_castars
    }

    # Charger les scores existants
    if os.path.exists("scores.json"):
        with open("scores.json", "r", encoding="utf-8") as f:
            scores = json.load(f)
    else:
        scores = []

    # Ajouter le nouveau score
    scores.append(score_entry)

    # Sauvegarder
    with open("scores.json", "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=4, ensure_ascii=False)

def draw_scores():
    screen.blit(background_img, (0, 0))

    title = font_big.render("Tableau des héros défunts", True, (255, 255, 255))
    screen.blit(title, ((MAP_WIDTH * TILE_SIZE) // 2 - title.get_width() // 2, 60))

    try:
        with open("scores.json", "r", encoding="utf-8") as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []

    scores = sorted(scores, key=lambda s: s.get("castars", 0), reverse=True)[:20]

    # Titres des colonnes
    screen.blit(hud_font.render("#", True, (255, 215, 0)), (60, 130))
    screen.blit(hud_font.render("Nom", True, (255, 215, 0)), (100, 130))
    screen.blit(hud_font.render("Niveau", True, (255, 215, 0)), (330, 130))
    screen.blit(hud_font.render("Castars", True, (255, 215, 0)), (440, 130))
    screen.blit(hud_font.render("Cause de la mort", True, (255, 215, 0)), (580, 130))

    for i, score in enumerate(scores):
        y = 170 + i * 26
        screen.blit(font_mini.render(f"{i+1}", True, (255, 255, 255)), (60, y))
        screen.blit(font_mini.render(score.get("nom", "???")[:20], True, (255, 255, 255)), (100, y))
        screen.blit(font_mini.render(str(score.get("niveau", "?")), True, (255, 255, 255)), (330, y))
        screen.blit(font_mini.render(str(score.get("castars", 0)), True, (255, 255, 255)), (440, y))
        screen.blit(font_mini.render(score.get("cause", "???")[:40], True, (255, 255, 255)), (580, y))

    draw_image_button("return", MAP_WIDTH * TILE_SIZE - 160, 20, "back_to_menu")



# ---------------------------------

def place_items_on_map(game_map):
    global items_on_map
    items_on_map = []
    attempts = 0

    weapons = [item for item in item_pool if item["type"] == "weapon"]
    armors = [item for item in item_pool if item["type"] == "armor"]
    golds = [item for item in item_pool if item["type"] == "gold"]
    foods = [item for item in item_pool if item["type"] == "food"]
    scrolls = [item for item in item_pool if item["type"] == "scroll"]
    potions = [item for item in item_pool if item["type"] == "potion"]

    def place_random(item_list, count):
        nonlocal attempts
        for _ in range(count):
            item = random.choice(item_list).copy()
            if item["type"] == "potion":
                base_name = item["name"].split(" +")[0].split(" -")[0]
                item["effect"] = potion_effect_map[base_name]

            # Ajoute un modificateur entre -1 et +2
            modifier = random.randint(-1, 2)

            if item["type"] not in ["scroll", "ammo", "food", "potion"]:
                modifier = random.randint(-1, 2)  # pour ne pas modifier les parchemins

            # Applique à atk ou def selon le type
            if "atk" in item:
                item["atk"] += modifier
            elif "def" in item:
                item["def"] += modifier

            # Ajoute le modificateur au nom de l'objet
            # Ajoute le modificateur au nom de l'objet, sauf pour les potions
            if item["type"] != "potion" and modifier != 0:
                signe = "+" if modifier > 0 else "-"
                item["name"] += f" {signe}{abs(modifier)}"

            placed = False
            while not placed and attempts < 1000:
                x = random.randint(1, MAP_WIDTH - 2)
                y = random.randint(1, MAP_HEIGHT - 2)
                if game_map[y][x] == '.' and not any(obj['x'] == x and obj['y'] == y for obj in items_on_map):
                    item["x"], item["y"] = x, y
                    items_on_map.append(item)
                    placed = True
                attempts += 1

    place_random(weapons, 2)
    place_random(armors, 1)
    # place_random(golds, 3)
    place_random(foods, random.randint(1, 2))  # 🍽️ place entre 0 et 1 ration alimentaire
    ammos = [item for item in item_pool if item["type"] == "ammo"]
    place_random(ammos, random.randint(1, 4))  # nombre de flèches à faire apparaître dans la map
    place_random(scrolls, random.randint(3, 5))  # 1 à 3 parchemins
    print("[DEBUG] Parchemins placés :", [i for i in items_on_map if i["type"] == "scroll"])
    place_random(potions, random.randint(3, 6))  # ← par exemple 3 à 6 potions par niveau


def draw_items_on_map():
    for item in items_on_map:
        if visibility_map[item['y']][item['x']] > 0:
            if item["type"] == "scroll":
                img = parchemin_img
            else:
                base_name = item['name'].split(" +")[0].split(" -")[0]
                img = item_images.get(base_name, treasure_img)
            screen.blit(img, (item['x'] * TILE_SIZE, item['y'] * TILE_SIZE))


# === FONCTION POUR EQUIPEMENT SELECTIONNE ===
def equip_selected_item(item_type):
    global selected_item_letter, current_weapon, current_armor, last_action_message

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if selected_item_letter:
        index = letters.find(selected_item_letter.upper())
        if 0 <= index < len(player_items):
            item = player_items[index]
            print(f"[DEBUG] Sélection lettre {selected_item_letter} → {item['name']} (type: {item['type']})")
            if item["type"] == item_type:
                if item_type == "weapon":
                    current_weapon = item
                    last_action_message = f"⚔️ Vous avez maintenant {item['name']} en main"
                elif item_type == "armor":
                    current_armor = item
                    last_action_message = f"🛡️ Vous portez maintenant {item['name']}"
                elif item["type"] == "potion":
                    base_name = item["name"].split(" +")[0].split(" -")[0]
                    if "effect" not in item:
                        item["effect"] = potion_effect_map.get(base_name, "unknown")

                    identified_potions.add(item["name"])

                    apply_potion_effect(item)  # ➜ L'effet affichera son propre message

                    player_items.pop(index)
            else:
                last_action_message = "Cette lettre ne correspond pas au bon type d'objet"
        else:
            last_action_message = "Lettre invalide"

        selected_item_letter = None






# === FONCTION POUR RAMASSER LES OBJETS ===
def pickup_item():
    global items_on_map, arrow_count
    for i, item in enumerate(items_on_map):
        if item['x'] == player_x and item['y'] == player_y:
            item_type = item["type"]

            # === SON en premier selon le type ===
            if item_type == "gold":
                sounds["Castarspickup"].play()
            else:
                sounds["pickup"].play()

            # === Ajout dans l’inventaire ou effet ===
            if item_type == "scroll":
                known = item['name'] in identified_scrolls
                player_items.append(item)
                if known:
                    show_message(f"Vous reconnaissez le parchemin '{item['name']}'")
                else:
                    show_message("Vous trouvez un mystérieux parchemin...")
            elif item_type == "gold":
                inventory.append({"type": "gold", "amount": item["amount"]})
                show_message(f"Vous avez trouvé {item['amount']} castars !")
                sounds["Castarspickup"].play()
            elif item_type == "food":
                inventory.append(item)
                show_message("Vous avez trouvé une ration alimentaire !")
            elif item_type == "ammo":
                arrow_count += item.get("amount", 1)
                show_message(f"Flèche ramassée ! (+{item.get('amount', 1)})")
            else:
                player_items.append(item)
                show_message(f"{item['name']} ramassé !")

            del items_on_map[i]
            break


def finalize_turn_message():
    global last_action_message, turn_messages

    if turn_messages:
        final_msg = " ".join(turn_messages)
        last_action_message = final_msg
        show_message(final_msg, duration=2500)
    else:
        last_action_message = ""

    turn_messages.clear()




# === AFFICHER INVENTAIRE ===
def draw_inventory_panel():
    panel = pygame.Surface((250, 250))
    panel.fill((30, 30, 30))
    pygame.draw.rect(panel, (200, 200, 200), (0, 0, 250, 250), 2)
    panel.blit(font_mini.render("Inventaire :", True, (255, 255, 255)), (10, 10))

    y_offset = 30
    total_castars = sum(item['amount'] for item in inventory if isinstance(item, dict) and item.get("type") == "gold")
    panel.blit(font_mini.render(f"Castars : {total_castars}", True, (255, 215, 0)), (10, y_offset))
    y_offset += 30
    panel.blit(font_mini.render(f"Flèches : {arrow_count}", True, (255, 255, 255)), (10, y_offset))
    y_offset += 30

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i, item in enumerate(player_items):
        if i >= len(letters):
            break
        extra = ""
        if item["type"] == "scroll":
            if item["name"] in identified_scrolls:
                effect = item.get("effect", "inconnu").replace("_", " ").capitalize()
                extra = f" (parchemin – {effect})"
            else:
                extra = " (parchemin)"

        if item["type"] == "potion":
            if item["name"] in identified_potions:
                effect = item.get("effect", "inconnu").replace("_", " ").capitalize()
                extra = f" (potion – {effect})"
            else:
                extra = " (potion)"

        if "atk" in item:
            extra = f" (ATK {item['atk']})"
        elif "def" in item:
            extra = f" (DEF {item['def']})"

        label = f"[{letters[i]}] {item['name']}{extra}"
        panel.blit(font_mini.render(label, True, (255, 255, 255)), (10, y_offset))
        y_offset += 20

    screen.blit(panel, (10, 10))


# === AJOUT DE LA FONCTION POUR UTILISER LES PARCHEMINS ===
def read_scroll():
    global selected_item_letter, waiting_for_scroll_input
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    scrolls = [(i, item) for i, item in enumerate(player_items) if item["type"] == "scroll"]

    if not scrolls:
        show_message("Aucun parchemin à lire")
        return

    show_message("Quelle lettre pour lire un parchemin ?")
    waiting_for_scroll_input = True

    def handle_scroll_input(event):
        global scroll_input_mode
        global waiting_for_scroll_input
        if event.type == pygame.KEYDOWN and hasattr(event, "unicode"):
            selected = event.unicode.upper()
            idx = letters.find(selected)
            if idx != -1 and idx < len(player_items):
                item = player_items[idx]
                if item["type"] == "scroll":
                    apply_scroll_effect(item)
                    identified_scrolls.add(item["name"])
                    player_items.pop(idx)
                    waiting_for_scroll_input = False
                    scroll_input_mode = False  # Reset input mode après lecture

    return handle_scroll_input


def drink_potion():
    global waiting_for_potion_input
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    potions = [(i, item) for i, item in enumerate(player_items) if item["type"] == "potion"]

    if not potions:
        show_message("Aucune potion à boire.")
        return

    show_message("Quelle potion boire ? Appuie sur une lettre (A-Z)")
    waiting_for_potion_input = True

    def handle_potion_input(event):
        global waiting_for_potion_input, potion_input_mode, potion_handler
        if event.type == pygame.KEYDOWN and hasattr(event, "unicode"):
            selected = event.unicode.upper()
            idx = letters.find(selected)
            if idx != -1 and idx < len(player_items):
                item = player_items[idx]
                if item["type"] == "potion":
                    base_name = item["name"].split(" +")[0].split(" -")[0]
                    if "effect" not in item:
                        item["effect"] = potion_effect_map.get(base_name, "unknown")
                    apply_potion_effect(item)
                    identified_potions.add(item["name"])
                    player_items.pop(idx)
                    waiting_for_potion_input = False
                    potion_input_mode = False
                    potion_handler = None  # reset
        elif event.type == pygame.KEYDOWN:
            # Si mauvaise touche, sortir du mode pour éviter blocage
            waiting_for_potion_input = False
            potion_input_mode = False
            potion_handler = None

    return handle_potion_input


# === EFFETS DES PARCHEMINS ===
def apply_scroll_effect(scroll):
    global player_x, player_y, confused_turns
    effect = scroll.get("effect")
    sounds["scroll"].play()

    if effect == "reveal_map":
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                visibility_map[y][x] = 255
        show_message("Toute la carte se dévoile !")

    elif effect == "confusion":
        confused_turns = 10  # Durée de la confusion
        show_message("Vous vous sentez confus... Vos contrôles sont inversés !")

    elif effect == "strength":
        show_message("Une force surnaturelle vous emplit...")

    elif effect == "teleport":
        while True:
            x = random.randint(1, MAP_WIDTH - 2)
            y = random.randint(1, MAP_HEIGHT - 2)
            if game_map[y][x] == '.':
                player_x, player_y = x, y
                update_visibility(player_x, player_y)
                show_message("🌀 Vous êtes téléporté !")
                break

    elif effect == "summon":
        spawned = 0
        for dx in [-1, 1, 0, 0]:
            for dy in [-1, 1, 0, 0]:
                if spawned >= 2:
                    break
                x, y = player_x + dx, player_y + dy
                if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and game_map[y][x] == '.':
                    monster = random.choice(get_monster_types_for_level(current_level))
                    enemies.append(
                        Enemy(monster["name"], x, y, monster["hp"], monster["dmg"], "down", monster["images"]))
                    spawned += 1
        show_message("Deux créatures apparaissent autour de vous !")

    elif effect == "identify":
        unknown_scrolls = [item for item in player_items if
                           item["type"] == "scroll" and item["name"] not in identified_scrolls]
        if unknown_scrolls:
            target = random.choice(unknown_scrolls)
            identified_scrolls.add(target["name"])
            show_message(f"🔎 Le parchemin '{target['name']}' est désormais identifié.")
        else:
            show_message("🔎 Aucun parchemin inconnu à identifier.")

def apply_potion_effect(potion):
    global player_health, player_strength, temporary_strength, strength_turns
    global is_dead, cause_de_mort, game_state
    show_message(f"[DEBUG] Appliquer effet potion : {potion.get('name')} → {potion.get('effect')}")
    sounds["drink"].play()

    effect = potion.get("effect")
    if effect == "heal":
        healed = min(player_max_health - player_health, 30)
        player_health += healed
        show_message(f"🧪 Vous buvez la potion : vous récupérez {healed} PV !")

    elif effect == "burn":
        player_health -= 20
        if player_health <= 0:
            player_health = 0
            is_dead = True
            cause_de_mort = "Mort par brûlure de potion"
            game_state = "game_over"
            save_score()
        else:
            show_message("🔥 Vous buvez une potion brûlante ! (-20 PV)")

    elif effect == "paralyze":
        global confused_turns
        confused_turns += 5
        show_message("😵 Vous buvez une potion paralysante ! Contrôles inversés pendant 5 tours.")

    elif effect == "weaken":
        temporary_strength -= 10
        strength_turns = 20
        show_message("💔 Vous buvez une potion affaiblissante ! (-10 Force pendant 5 tours)")

    elif effect == "strength_boost":
        temporary_strength += 10
        strength_turns = 5
        show_message("💪 Vous buvez une potion de puissance ! (+10 Force pendant 5 tours)")

    elif effect == "poison":
        player_health -= 10
        show_message("☠️ Vous buvez une potion empoisonnée ! (-10 PV)")



# === ÉTAT ÉQUIPEMENT ===
current_weapon = {"name": "Poings", "atk": 3}
current_armor = {"name": "Rien", "def": 1}


def unequip_item(item_type):
    global current_weapon, current_armor
    if item_type == "weapon":
        current_weapon = {"name": "Poings", "atk": 0}
        show_message("⚔️ Arme retirée !")
    elif item_type == "armor":
        current_armor = {"name": "Rien", "def": 0}
        show_message("🛡️ Armure retirée !")


def equip_item(item_type):
    global current_weapon, current_armor
    for item in inventory:
        if item["type"] == item_type:
            if item_type == "weapon":
                current_weapon = item
                show_message(f"Vous portez maintenant {item['name']} ({item_type}).")

            elif item_type == "armor":
                current_armor = item
                show_message(f"Vous portez maintenant {item['name']} ({item_type}).")

            break


def unequip_item(item_type):
    global current_weapon, current_armor
    if item_type == "weapon":
        current_weapon = {"name": "Poings", "atk": 0}
        show_message("⚔️ Arme retirée !")
    elif item_type == "armor":
        current_armor = {"name": "Rien", "def": 0}
        show_message("🛡️ Armure retirée !")


def draw_image_button(name, x, y, action):
    img = button_images.get(name)
    if not img:
        return
    rect = img.get_rect(topleft=(x, y))

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    screen.blit(img, rect)

    if rect.collidepoint(mouse):
        # Effet de survol (optionnel) : éclaircissement
        highlight = pygame.Surface(rect.size, pygame.SRCALPHA)
        highlight.fill((255, 255, 255, 30))  # léger voile blanc
        screen.blit(highlight, rect.topleft)

        if click[0] == 1:
            pygame.time.wait(200)
            handle_button(action)



def handle_button(action):
    global game_state, instruction_line_index, instruction_timer
    if action == "start_game":
        sounds["entreedansmine"].play()
        global player_health, inventory, player_items, current_level, is_dead, last_action_message
        player_health = player_max_health
        inventory.clear()
        player_items.clear()
        current_level = 1
        last_action_message = ""
        is_dead = False
        reset_game()  # ← redémarre une nouvelle carte avec tout réinitialisé
        # ⏯️ Lecture de la vidéo d’intro après appui sur le bouton
        play_intro_video("assets/intro.mp4")
        start_transition("playing")

    elif action == "show_scores":
        start_transition("scores")
    elif action == "instructions":
        instruction_line_index = 0
        instruction_timer = pygame.time.get_ticks()
        start_transition("instructions")
    elif action == "back_to_menu":
        start_transition("start")
    elif action == "quit":
        pygame.quit()
        sys.exit()


def draw_instructions():
    global instruction_line_index, instruction_timer

    screen.blit(instructions_img, (0, 0))
    title = font_big.render("Instructions", True, (0, 0, 0))
    screen.blit(title, ((MAP_WIDTH * TILE_SIZE) // 2 - title.get_width() // 2, 50))

    instructions = [
        "Déplace-toi avec les flèches directionnelles.",
        "Appuie sur A pour attendre un tour.",
        "Appuie sur I pour ouvrir l'inventaire.",
        "Appuie sur M pour afficher toute la carte.",
        "Ramasse les trésors en marchant dessus.",
        "Descends les escaliers avec W quand tu es dessus.",
        "But : Explore, ramasse et SURVIS !"
    ]

    now = pygame.time.get_ticks()
    if instruction_line_index < len(instructions):
        if now - instruction_timer > instruction_interval:
            instruction_line_index += 1
            instruction_timer = now

    for i in range(instruction_line_index):
        text = font_small.render(instructions[i], True, (0, 0, 0))
        text_rect = text.get_rect(center=((MAP_WIDTH * TILE_SIZE) // 2, 150 + i * 70))

        screen.blit(text, text_rect)

    draw_image_button("return", MAP_WIDTH * TILE_SIZE - 160, 20, "back_to_menu")



class Enemy:
    def __init__(self, name, x, y, hp, dmg, direction, images):
        self.name = name
        self.x = x
        self.y = y
        self.hp = hp
        self.dmg = dmg
        self.direction = direction
        self.images = images
        self.alerted = False  # ← nouveau comportement

    def draw(self):
        img = self.images.get(self.direction, self.images["down"])
        screen.blit(img, (self.x * TILE_SIZE, self.y * TILE_SIZE))


def generate_map(width, height):
    def create_empty_grid():
        return [['#' for _ in range(width)] for _ in range(height)]

    def carve_maze(grid):
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        visited = [[False for _ in range(width)] for _ in range(height)]

        def in_bounds(x, y):
            return 0 < x < width - 1 and 0 < y < height - 1

        def shuffle_dirs():
            dirs = directions[:]
            random.shuffle(dirs)
            return dirs

        def carve(x, y):
            visited[y][x] = True
            grid[y][x] = '.'
            for dx, dy in shuffle_dirs():
                nx, ny = x + dx * 2, y + dy * 2
                if in_bounds(nx, ny) and not visited[ny][nx]:
                    grid[y + dy][x + dx] = '.'
                    carve(nx, ny)

        start_x = random.randrange(1, width - 2, 2)
        start_y = random.randrange(1, height - 2, 2)
        carve(start_x, start_y)
        return start_x, start_y

    def add_tiny_corridors():
        for _ in range(90):  # Nombre d’interconnexions
            x = random.randint(1, width - 2)
            y = random.randint(1, height - 2)
            if grid[y][x] == '#' and (
                    (grid[y - 1][x] == '.' and grid[y + 1][x] == '.') or
                    (grid[y][x - 1] == '.' and grid[y][x + 1] == '.')
            ):
                grid[y][x] = '.'

    grid = create_empty_grid()
    px, py = carve_maze(grid)

    # === Ajouter une grande salle ===
    room_w = random.randint(6, 25)
    room_h = random.randint(4, 25)
    room_x = random.randint(1, width - room_w - 1)
    room_y = random.randint(1, height - room_h - 1)

    for y in range(room_y, room_y + room_h):
        for x in range(room_x, room_x + room_w):
            grid[y][x] = '.'

    add_tiny_corridors()

    # === Placer les escaliers ===
    global stairs_position
    placed = False
    while not placed:
        x = random.randint(1, width - 2)
        y = random.randint(1, height - 2)
        if grid[y][x] == '.' and (x, y) != (px, py):
            stairs_position = (x, y)
            placed = True

    return grid, (px, py), (room_x, room_y, room_w, room_h)


def place_treasures(game_map, num=None):
    if num is None:
        num = random.randint(3, 7)  # 🎲 Change ici la plage comme tu veux

    treasures = []
    attempts = 0
    while len(treasures) < num and attempts < 1000:
        x = random.randint(1, MAP_WIDTH - 2)
        y = random.randint(1, MAP_HEIGHT - 2)
        if game_map[y][x] == '.' and not any(t[0] == x and t[1] == y for t in treasures):
            treasures.append((x, y, random.randint(1, 45)))  # quantité aléatoire
        attempts += 1
    return treasures


def update_visibility(px, py, radius=10):
    global visibility_map

    def cast_ray(x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            if 0 <= x1 < MAP_WIDTH and 0 <= y1 < MAP_HEIGHT:
                if game_map[y1][x1] == '#':
                    visibility_map[y1][x1] = 255
                    break
                visibility_map[y1][x1] = 255
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    visibility_map[py][px] = 255
    for y in range(max(0, py - radius), min(MAP_HEIGHT, py + radius + 1)):
        for x in range(max(0, px - radius), min(MAP_WIDTH, px + radius + 1)):
            if math.sqrt((px - x) ** 2 + (py - y) ** 2) <= radius:
                cast_ray(px, py, x, y)


def fade_visibility():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if visibility_map[y][x] > 0 and game_map[y][x] != '#':
                visibility_map[y][x] = max(visibility_map[y][x] - 5, 100)

def draw_text_with_shadow(text, font, x, y, color, shadow_color=(0, 0, 0), offset=1):
    shadow = font.render(text, True, shadow_color)
    screen.blit(shadow, (x + offset, y + offset))
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_hud():
    hud_y = MAP_HEIGHT * TILE_SIZE
    screen.blit(hud_bg_img, (0, hud_y))

    stats_text = f"Vie : {player_health}/{player_max_health}   "
    stats_text += f"Force : {player_strength + temporary_strength + current_weapon.get('atk', 0)} ({current_weapon['name']})   "
    stats_text += f"Armure : {current_armor.get('def', 0)} ({current_armor['name']})   "
    stats_text += f"Niveau : {current_level} "
    stats_text += f"Flèches : {arrow_count}"
    total_castars = sum(item["amount"] for item in inventory if isinstance(item, dict) and item.get("type") == "gold")
    stats_text += f" Castars : {total_castars}"

    draw_text_with_shadow(stats_text, font_mini, 10, hud_y + 5, (255, 255, 255))

    # Priorité aux messages temporaires
    now = pygame.time.get_ticks()
    if hud_message and now < hud_message_timer:
        screen.blit(font_mini.render(hud_message, True, (255, 255, 0)), (10, hud_y + 25))
    elif last_action_message:
        screen.blit(font_mini.render(last_action_message, True, (255, 255, 0)), (10, hud_y + 25))



def show_message(text, duration=2000):
    global hud_message, hud_message_timer
    now = pygame.time.get_ticks()
    # Remplacer immédiatement l'ancien message
    hud_message = text
    hud_message_timer = now + duration


def draw_map():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if visibility_map[y][x] > 0:
                img = floor_img if game_map[y][x] == '.' else wall_img
                tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
                tile.blit(img, (0, 0))
                tile.set_alpha(visibility_map[y][x])
                screen.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))
            if (x, y) == stairs_position and visibility_map[y][x] > 0:
                screen.blit(stairs_img, (x * TILE_SIZE, y * TILE_SIZE))
            for tx, ty, _ in treasures:
                if (x, y) == (tx, ty) and visibility_map[y][x] > 0:
                    screen.blit(treasure_img, (x * TILE_SIZE, y * TILE_SIZE))

    for x, y, img in special_floor_decor:
        if visibility_map[y][x] > 0:
            screen.blit(img, (x * TILE_SIZE, y * TILE_SIZE))

    draw_items_on_map()


    for enemy in enemies:
        if visibility_map[enemy.y][enemy.x] > 0:
            enemy.draw()

    if current_direction == "up":
        player_image = player_up
    elif current_direction == "down":
        player_image = player_down
    elif current_direction == "left":
        player_image = player_left
    elif current_direction == "right":
        player_image = player_right
    else:
        player_image = player_down

    screen.blit(player_image, (player_x * TILE_SIZE, player_y * TILE_SIZE))
    draw_hud()


def tirer_une_fleche(dx, dy):
    global arrow_count, is_aiming
    sounds["lancementfleche"].play()
    range_max = current_weapon.get("range", 5)
    hit = False

    for step in range(1, range_max + 1):
        tx = player_x + dx * step
        ty = player_y + dy * step
        if not (0 <= tx < MAP_WIDTH and 0 <= ty < MAP_HEIGHT):
            break
        if game_map[ty][tx] == '#':
            break
        for enemy in enemies:
            if enemy.x == tx and enemy.y == ty:
                dmg = player_strength + current_weapon.get("atk", 0) + temporary_strength
                enemy.hp -= dmg
                if enemy.hp <= 0:
                    enemies.remove(enemy)
                    turn_messages.append(f"🏹 Tu as tué le {enemy.name} !")
                else:
                    turn_messages.append(f"🏹 Tu touches le {enemy.name} (-{dmg} PV)")
                hit = True
                break
        if hit:
            break

    if not hit:
        turn_messages.append("🏹 Tu rates ton tir...")

    arrow_count -= 1
    is_aiming = False  # Fin de la visée
    player_has_acted = True


def can_see_player(enemy_x, enemy_y):
    # Lance un rayon du monstre vers le joueur
    # Si un mur bloque, il ne le voit pas
    dx = player_x - enemy_x
    dy = player_y - enemy_y
    distance = math.hypot(dx, dy)
    if distance > 10:
        return False

    # Raycasting simplifié
    steps = int(distance)
    for i in range(1, steps + 1):
        x = int(enemy_x + dx * i / steps)
        y = int(enemy_y + dy * i / steps)
        if game_map[y][x] == '#':
            return False  # Un mur bloque la vue
    return True

def move_toward_player(enemy):
    best_dx, best_dy = 0, 0
    best_dist = abs(player_x - enemy.x) + abs(player_y - enemy.y)
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = enemy.x + dx, enemy.y + dy
        if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
            if game_map[ny][nx] == '.' and not any(e.x == nx and e.y == ny for e in enemies):
                dist = abs(player_x - nx) + abs(player_y - ny)
                if dist < best_dist:
                    best_dx, best_dy = dx, dy
                    best_dist = dist
    if best_dx == 1:
        enemy.direction = "right"
    elif best_dx == -1:
        enemy.direction = "left"
    elif best_dy == 1:
        enemy.direction = "down"
    elif best_dy == -1:
        enemy.direction = "up"

    enemy.x += best_dx
    enemy.y += best_dy

def move_randomly(enemy):
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = enemy.x + dx, enemy.y + dy
        if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
            if game_map[ny][nx] == '.' and not any(e.x == nx and e.y == ny for e in enemies):
                if dx == 1:
                    enemy.direction = "right"
                elif dx == -1:
                    enemy.direction = "left"
                elif dy == 1:
                    enemy.direction = "down"
                elif dy == -1:
                    enemy.direction = "up"

                enemy.x = nx
                enemy.y = ny
                break


def enemy_turn():
    global player_health, game_state, is_dead, last_action_message, cause_de_mort, game_over_fade_alpha
    for enemy in enemies:
        dx = int(player_x) - int(enemy.x)
        dy = int(player_y) - int(enemy.y)

        if abs(dx) + abs(dy) == 1:
            if random.random() <= enemy_hit_chance:
                dmg = enemy.dmg - current_armor.get("def", 0)
                dmg = max(dmg, 1)
                player_health -= dmg
                turn_messages.append(f"💥 Le {enemy.name} vous attaque ! (-{dmg} PV)")
                if player_health <= 0:
                    player_health = 0
                    is_dead = True
                    cause_de_mort = f"Tué par un {enemy.name}"
                    game_over_fade_alpha = 255
                    save_score()
                    game_state = "game_over"
                    return
            else:
                turn_messages.append(f"❌ Le {enemy.name} vous rate.")
        else:
            if can_see_player(enemy.x, enemy.y):
                enemy.alerted = True
            elif random.random() < 0.1:
                enemy.alerted = False

            if enemy.alerted:
                move_toward_player(enemy)
            else:
                move_randomly(enemy)

def show_game_over_screen():
    global game_over_fade_alpha
    screen.blit(gameover_img, (0, 0))
    title = font_big.render(" GAME OVER ", True, (255, 0, 0))
    subtitle = font_small.render(f"Dans les profondeurs des mines reposera pour toujours {player_name}...", True,
                                 (200, 200, 200))
    restart = font_mini.render("Appuie sur ESPACE pour recommencer", True, (255, 255, 255))
    screen.blit(title, ((MAP_WIDTH * TILE_SIZE) // 2 - title.get_width() // 2, 200))
    screen.blit(subtitle, ((MAP_WIDTH * TILE_SIZE) // 2 - subtitle.get_width() // 2, 270))
    screen.blit(restart, ((MAP_WIDTH * TILE_SIZE) // 2 - restart.get_width() // 2, 320))
    draw_image_button("return", 100, 400, "back_to_menu")
    # === FONDU ENTRANT ===
    if game_over_fade_alpha > 0:
        fade_surface = pygame.Surface((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE + HUD_HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(game_over_fade_alpha)
        screen.blit(fade_surface, (0, 0))
        game_over_fade_alpha = max(game_over_fade_alpha - 5, 0)  # diminue progressivement


def draw_intro():
    global intro_display_text, intro_char_index, intro_timer, input_active
    screen.blit(background_img, (0, 0))

    now = pygame.time.get_ticks()
    full_text = "\n".join(intro_text)
    if intro_char_index < len(full_text):
        if now - intro_timer > intro_speed:
            intro_display_text += full_text[intro_char_index]
            intro_char_index += 1
            intro_timer = now

    lines = intro_display_text.split("\n")
    line_height = font_small.get_height()

    # Affiche les lignes d'intro une à une
    for i, line in enumerate(lines):
        rendered = font_small.render(line, True, (200, 200, 200))
        screen.blit(rendered, (100, 100 + i * line_height))

    if intro_char_index >= len(full_text):
        base_y = 100 + len(lines) * line_height + 20
        input_box = pygame.Rect(500, base_y, 300, 40)

        # Curseur clignotant
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        name_surface = font_small.render(player_name, True, (255, 255, 255))
        text_y = input_box.y + (input_box.height - name_surface.get_height()) // 2
        screen.blit(name_surface, (input_box.x + 10, text_y))

        # Curseur clignotant
        if input_active:
            cursor_time = pygame.time.get_ticks() // 500 % 2
            if cursor_time:
                cursor_x = input_box.x + 10 + name_surface.get_width() + 2
                cursor_y = input_box.y + 5
                pygame.draw.line(screen, (255, 255, 255), (cursor_x, cursor_y), (cursor_x, cursor_y + 30), 2)

        # Boutons alignés sous le champ de texte
        y_base = 350
        spacing = 70

        draw_image_button("start_game", 500, y_base + 0 * spacing, "start_game")
        draw_image_button("instructions", 500, y_base + 1 * spacing, "instructions")
        draw_image_button("scores", 500, y_base + 2 * spacing, "show_scores")
        draw_image_button("quit", 500, y_base + 3 * spacing, "quit")


def show_start_screen():
    screen.blit(background_img, (0, 0))
    title = font_big.render("MORIA 3", True, (255, 255, 255))
    subtitle = font_small.render("Appuie sur ESPACE pour continuer", True, (200, 200, 200))
    screen.blit(title, ((MAP_WIDTH * TILE_SIZE) // 2 - title.get_width() // 2, 200))
    screen.blit(subtitle, ((MAP_WIDTH * TILE_SIZE) // 2 - subtitle.get_width() // 2, 270))


def reset_game():
    global game_map, player_x, player_y, treasures, enemies, visibility_map, stairs_position
    global inventory, player_items, current_weapon, current_armor, arrow_count
    global potion_effect_map, identified_potions
    identified_potions.clear()
    random.shuffle(potion_possible_effects)
    potion_effect_map = dict(zip(potion_names, potion_possible_effects))
    print("[DEBUG] Potions cette partie :", potion_effect_map)

    item_pool[:] = [item for item in item_pool if item.get("type") != "potion"]
    for name in potion_names:
        item_pool.append({"name": name, "type": "potion"})  # sans "effect", il sera ajouté dynamiquement

    game_map, (player_x, player_y), (room_x, room_y, room_w, room_h) = generate_map(MAP_WIDTH, MAP_HEIGHT)
    special_floor_decor.clear()
    for _ in range(random.randint(2, 4)):
        sx = random.randint(room_x + 1, room_x + room_w - 2)
        sy = random.randint(room_y + 1, room_y + room_h - 2)
        special_floor_decor.append((sx, sy, floorsquelette_img))

    #for _ in range(random.randint(1, 2)):
        #ax = random.randint(room_x + 1, room_x + room_w - 2)
        #ay = random.randint(room_y + 1, room_y + room_h - 2)
        #special_floor_decor.append((ax, ay, floorautel_img))

    treasures = place_treasures(game_map)

    visibility_map = [[0 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    enemies = []
    inventory.clear()
    player_items.clear()
    starting_dagger = {
        "name": "Dague rouillée",
        "type": "weapon",
        "atk": 15
    }
    player_items.append(starting_dagger)
    current_weapon = starting_dagger  # Équipée dès le départ

    current_armor = {"name": "Chemise de rôdeur", "def": 1}

    # 🎁 Ajout de départ : Arc + 3 flèches
    player_items.append({"name": "Arc", "type": "weapon", "atk": 2, "range": 5})
    arrow_count = 3

    for _ in range(5):

        monster = random.choice(get_monster_types_for_level(current_level))

        placed = False
        while not placed:
            x = random.randint(1, MAP_WIDTH - 2)
            y = random.randint(1, MAP_HEIGHT - 2)
            if game_map[y][x] == '.' and (x, y) != (player_x, player_y):
                enemies.append(Enemy(monster["name"], x, y, monster["hp"], monster["dmg"], "down", monster["images"]))
                placed = True

    update_visibility(player_x, player_y)
    place_items_on_map(game_map)


# === ENNEMI ASSETS POUR RESET ===
enemy_images = {"up": serpent_up, "down": serpent_down, "left": serpent_left, "right": serpent_right}
reset_game()

# === BOUCLE PRINCIPALE ===

running = True


def start_transition(target_state):
    global transition_alpha, transition_target, transition_in_progress
    transition_alpha = 255
    transition_target = target_state
    transition_in_progress = True


try:
    running = True
    while running:
        screen.fill((0, 0, 0))
        player_has_acted = False

        for event in pygame.event.get():

            if scroll_input_mode:
                if scroll_handler:
                    scroll_handler(event)
                continue  # On saute tout le reste du traitement d'event tant qu'on lit un parchemin

            if potion_input_mode:
                if potion_handler:
                    potion_handler(event)
                continue

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "intro":
                    line_height = font_small.get_height()
                    base_y = 100 + len(intro_text) * line_height + 20
                    if pygame.Rect(500, base_y, 300, 40).collidepoint(event.pos):
                        input_active = True
                    else:
                        input_active = False




            elif event.type == pygame.KEYDOWN:
                # Ne pas effacer immédiatement les messages persistants si une action vient d’être déclenchée (ex: potion)
                now = pygame.time.get_ticks()
                if not selection_mode and now > hud_message_timer:
                    hud_message = ""
                    hud_message_timer = 0
                    last_action_message = ""

                if selection_mode and hasattr(event, "unicode"):
                    selected_char = event.unicode.upper()
                    if selected_char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        selected_item_letter = selected_char
                        equip_selected_item(selection_mode)
                        selection_mode = None
                        show_message("")  # Réinitialiser HUD

                else:
                    if is_aiming:
                        dir_map = {
                            pygame.K_UP: (0, -1),
                            pygame.K_DOWN: (0, 1),
                            pygame.K_LEFT: (-1, 0),
                            pygame.K_RIGHT: (1, 0)
                        }
                        if event.key in dir_map:               # Tu tires une flèche dans la direction donnée
                            tirer_une_fleche(*dir_map[event.key])
                            is_aiming = False  # Fin du mode visée
                            player_has_acted = True
                            continue  # ⚡ Très important : ne PAS faire d'autres actions après un tir !
                    # --- Sinon comportement NORMAL ---
                    if game_state == "start" and event.key == pygame.K_SPACE:
                        start_transition("intro")
                    elif game_state == "game_over" and event.key == pygame.K_SPACE:
                        player_health = 100
                        inventory.clear()
                        current_level = 1
                        last_action_message = ""
                        is_dead = False
                        game_state = "playing"
                        reset_game()

                    elif game_state == "intro" and input_active:
                        if event.key == pygame.K_BACKSPACE:
                            player_name = player_name[:-1]
                        else:
                            player_name += event.unicode

                    elif game_state == "playing":
                        if event.key == pygame.K_y:
                            scroll_handler = read_scroll()
                            if scroll_handler:
                                scroll_input_mode = True

                        elif event.key == pygame.K_F11:
                            toggle_fullscreen()

                        elif event.key == pygame.K_u:
                            if not any(item["type"] == "potion" for item in player_items):
                                show_message("❌ Aucune potion à boire.")
                            else:
                                potion_handler = drink_potion()

                                if potion_handler:
                                    potion_input_mode = True
                                    show_message("🧪 Quelle potion boire ? Appuie sur une lettre (A-Z)")



                        elif event.key == pygame.K_b:
                            if not selection_mode:
                                hud_message = "Quelle arme voulez-vous brandir ? Appuie sur une lettre (A-Z)"
                                hud_message_timer = 999999999
                                selection_mode = "weapon"

                        elif event.key == pygame.K_l:
                            if current_weapon["name"].lower().startswith("arc") and arrow_count > 0:
                                is_aiming = True
                                show_message("Dans quelle direction tirer ?", duration=999999999)
                            else:
                                show_message("⚠️ Il vous faut un arc équipé et des flèches pour tirer !")

                        elif event.key == pygame.K_i:
                            show_inventory = not show_inventory

                        elif event.key == pygame.K_m:
                            for y in range(MAP_HEIGHT):
                                for x in range(MAP_WIDTH):
                                    visibility_map[y][x] = 255


                        elif event.key == pygame.K_w and (player_x, player_y) == stairs_position:
                            sounds["changementniveau"].play()
                            show_message(f"⬇Tu descends au niveau {current_level + 1}")
                            current_level += 1
                            reset_game()

                        elif event.key == pygame.K_t:
                            if not selection_mode:
                                hud_message = "Quelle armure veux-tu porter ? Appuie sur une lettre (A-Z)"
                                hud_message_timer = 999999999
                                selection_mode = "armor"


                        elif event.key == pygame.K_e:
                            unequip_item("weapon")
                            selection_mode = None

                        elif event.key == pygame.K_r:
                            unequip_item("armor")
                            selection_mode = None


                        elif event.key == pygame.K_a:

                            show_message("⏳ Tu attends un instant...", duration=999999)  # durée longue, sera effacée par touche suivante
                            enemy_turn()
                            finalize_turn_message()
                            pygame.time.wait(120)




                        elif event.key == pygame.K_p:
                            for i, item in enumerate(inventory):
                                if isinstance(item, dict) and item.get("type") == "food":
                                    player_hunger = min(player_max_hunger, player_hunger + item["amount"])
                                    show_message(f"Tu manges une ration (+{item['amount']} faim) !")
                                    del inventory[i]
                                    break
                            else:
                                show_message("Tu n'as rien à manger...")
        if player_has_acted:
            hud_message = ""  # Efface les anciens messages persistants (ex: "tu attends un instant")
            draw_map()
            if show_inventory:
                draw_inventory_panel()
            pygame.display.flip()
            clock.tick(60)
            continue

        # === AFFICHAGE EN FONCTION DE L'ÉTAT ===
        if game_state == "start":
            show_start_screen()
        elif game_state == "intro":
            draw_intro()
        elif game_state == "scores":
            draw_scores()
        elif game_state == "instructions":
            draw_instructions()
        elif game_state == "playing":
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if is_aiming:
                dx = dy = 0  # 🔥 Pendant qu'on vise : pas de déplacement possible
                draw_map()
                if show_inventory:
                    draw_inventory_panel()
                pygame.display.flip()
                clock.tick(60)
                continue
            if keys[pygame.K_UP]: dy = -1; current_direction = "up"
            if keys[pygame.K_DOWN]: dy = 1; current_direction = "down"
            if keys[pygame.K_LEFT]: dx = -1; current_direction = "left"
            if keys[pygame.K_RIGHT]: dx = 1; current_direction = "right"                  #BLOC DE DX DY 0 ou 1
            if confused_turns > 0:
                dx *= -1
                dy *= -1
            if dx != 0 or dy != 0:
                tx, ty = player_x + dx, player_y + dy
                has_acted = False
                action_msg = ""  # ✅ on l’initialise avant la boucle

                for enemy in enemies:
                    if enemy.x == tx and enemy.y == ty:
                        if random.random() <= player_hit_chance:
                            sounds["hit"].play()
                            dmg = player_strength + current_weapon.get("atk", 0) + temporary_strength
                            enemy.hp -= dmg
                            if enemy.hp <= 0:
                                enemies.remove(enemy)
                                turn_messages.append(f"☠️ Tu as tué le {enemy.name} !")
                            else:
                                turn_messages.append(f"🗡 Tu touches le {enemy.name} ! Il lui reste {enemy.hp} PV.")
                        else:
                            turn_messages.append(f"❌ Tu rates le {enemy.name} !")
                            sounds["miss"].play()

                        has_acted = True
                        break

                else:  # aucun ennemi touché → on essaie de se déplacer
                    if game_map[ty][tx] == '.' and not any(e.x == tx and e.y == ty for e in enemies):
                        player_x, player_y = tx, ty
                    # ⚠️ MODE NOCLIP ACTIVÉ
                    # Ignorer les murs pour les tests
                    #if not any(e.x == tx and e.y == ty for e in enemies):
                        #player_x, player_y = tx, ty

                        move_counter += 1
                        if move_counter >= 3:
                            player_hunger -= 1
                            move_counter = 0
                            print(f"[DEBUG] Faim actuelle : {player_hunger}")

                        steps_since_last_heal += 1
                        if steps_since_last_heal >= next_heal_threshold:
                            if player_health < player_max_health:
                                player_health += 1
                            steps_since_last_heal = 0
                            next_heal_threshold = random.randint(10, 14)

                        if player_hunger <= 0:
                            player_health = 0
                            last_action_message = "Vous êtes mort de faim..."
                            cause_de_mort = "Mort de faim"
                            game_over_fade_alpha = 255
                            save_score()
                            game_state = "game_over"
                            is_dead = True
                        elif player_hunger < 50:
                            show_message("Vous mourrez de faim. Vous êtes affaibli...")

                        fade_visibility()
                        update_visibility(player_x, player_y)
                        pickup_item()
                        has_acted = True

                        for i, (gx, gy, val) in enumerate(treasures):
                            if (player_x, player_y) == (gx, gy):
                                inventory.append({"type": "gold", "amount": val})
                                show_message(f"🎉 Castar ramassé : {val}")
                                del treasures[i]
                                break

                if has_acted:
                    enemy_turn()
                    finalize_turn_message()

                    # Apparition de monstres (régulée)
                    now = pygame.time.get_ticks()
                    if 'last_monster_spawn_time' not in globals():
                        last_monster_spawn_time = 0
                    if 'max_enemies_on_map' not in globals():
                        max_enemies_on_map = 10

                    if now - last_monster_spawn_time > 8000 and len(enemies) < max_enemies_on_map:
                        if random.random() < 0.4:
                            monster = random.choice(get_monster_types_for_level(current_level))
                            spawn_attempts = 0
                            while spawn_attempts < 50:
                                x = random.randint(1, MAP_WIDTH - 2)
                                y = random.randint(1, MAP_HEIGHT - 2)
                                distance = abs(player_x - x) + abs(player_y - y)
                                if game_map[y][x] == '.' and distance > 10 and not any(
                                        e.x == x and e.y == y for e in enemies):
                                    enemies.append(Enemy(monster["name"], x, y, monster["hp"], monster["dmg"], "down",
                                                         monster["images"]))
                                    last_monster_spawn_time = now
                                    break
                                spawn_attempts += 1

                    pygame.time.wait(120)

            draw_map()
            if show_inventory:
                draw_inventory_panel()

        if hud_message and pygame.time.get_ticks() > hud_message_timer:
            hud_message = ""
        elif game_state == "game_over":
            show_game_over_screen()

        # FONDU DE TRANSITION ENTRE LES ÉTATS (CORRIGÉ)
        if transition_in_progress:
            if transition_alpha == 255 and transition_target:
                # Dès que le fondu commence, on change d'écran !
                game_state = transition_target
                transition_target = None

            fade_surface = pygame.Surface((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE + HUD_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(transition_alpha)
            screen.blit(fade_surface, (0, 0))

            transition_alpha -= 10
            if transition_alpha <= 0:
                transition_alpha = 0
                transition_in_progress = False

        mouse_pos = pygame.mouse.get_pos()
        screen.blit(cursor_img, mouse_pos)

        pygame.display.flip()
        clock.tick(60)

except Exception as e:
    traceback.print_exc()
    pygame.quit()
    sys.exit()