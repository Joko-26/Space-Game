
from time import sleep
import pgzrun
import random

WIDTH = 1200
HEIGHT = 800

hight_score = None
score = 0
number_of_score_updates = 0
game_over = True
raumschiff_bild = 0
number_of_raumschiff_updates = 0
meteor_bild = 0
number_of_meteor_updates = 0
ufo_bild = 0
number_of_ufo_updates = 0

game_over_screen = Actor('game over2')
game_over_screen.pos = 600, 400
main_screen = Actor('main menü')
main_screen.pos = 600, 400
raumschiff = Actor('raumschiff')
raumschiff.pos = 400, 500
ufo1 = Actor('ufo')
ufo1.pos = random.randint(20, 1200), random.randint(-800, -50)
ufo2 = Actor('ufo')
ufo2.pos = random.randint(20, 1200), random.randint(-800, -50)
ufo3 = Actor('ufo')
Ufos = [ufo1,  ufo2]
meteor1 = Actor('meteor')
meteor1.pos = random.randint(20, 1200), random.randint(-800, -50)
meteor2 = Actor('meteor')
meteor2.pos = random.randint(20, 1200), random.randint(-800, -50)
meteor3 = Actor('meteor')
meteor3.pos = random.randint(20, 1200), random.randint(-800, -50)
meteor4 = Actor('meteor')
meteor4.pos = random.randint(20, 1200), random.randint(-800, -50)
meteore = [meteor1, meteor2, meteor3, meteor4]
meteore2 = [meteor1, meteor2]

def get_hightscore():
    with open('hightscore.txt', 'r') as hight_scores:
        hightscore = hight_scores.read()
        return hightscore

def save_hightscore(new_hightscore):
    open('path of hightscore.txt', 'w').close()
    with open('path of hightscore.txt', 'a') as hight_scores:
        hight_scores.write(str(new_hightscore))


def musik_player():
    if not game_over:
        music.play('background')
    else:
        music.play('background2')

musik_player()

def restart():
    global score, game_over, number_of_raumschiff_updates, number_of_meteor_updates, meteor_bild, number_of_ufo_updates,  ufo_bild, hight_score
    score = 0
    game_over = False
    life = 4
    number_of_meteor_updates = 0
    number_of_raumschiff_updates = 0
    number_of_ufo_updates = 0
    ufo_bild = 0
    meteor_bild = 0
    hight_score = get_hightscore()
    game_over_screen.image = 'game over2'
    music.play_once('übergang')
    music.queue('background')
    sleep(0.6)
    for meteor in meteore:
        meteor.pos = random.randint(20, 1200), random.randint(-800, -50)
    for ufo in Ufos:
        ufo.pos = random.randint(20, 1200), random.randint(-800, -100)

def game_over_funktion():
    global game_over, hight_score, score
    game_over_screen.image = 'game over'
    music.play_once('game over')
    game_over = True
    music.queue('background2')
    if int(hight_score) < int(score):
        save_hightscore(score)

def raumschiff_animation():
    global raumschiff_bild
    if raumschiff_bild == 0:
        raumschiff.image = 'raumschiff2'
        raumschiff_bild = 1
    elif raumschiff_bild == 1:
        raumschiff.image = 'raumschiff3'
        raumschiff_bild = 2
    elif raumschiff_bild == 2:
        raumschiff.image = 'raumschiff'
        raumschiff_bild = 0

def draw():
    global score, hight_score
    screen.clear()
    screen.blit('space', (200, 0))
    game_over_screen.draw()
    if not game_over:
        screen.draw.text(str(score) + ' / ' + str(hight_score), color='green',  topleft=(1000, 60), fontsize=60)
        raumschiff.draw()
        for ufo in Ufos:
            ufo.draw()
        for meteor in meteore:
            meteor.draw()
    elif game_over:
        main_screen.draw()
        


def update():
    global game_over, number_of_raumschiff_updates, number_of_meteor_updates, meteor_bild, number_of_ufo_updates,  ufo_bild, score,  number_of_score_updates
    if game_over:
        if keyboard.space:
            restart()
    elif not game_over:
        if keyboard.left:
            raumschiff.x -= 10
            if raumschiff.x < 0:
                raumschiff.pos = 1150,  500

        if keyboard.right:
            raumschiff.x += 10
            if raumschiff.x > 1200:
                raumschiff.pos = 10, 500
        
        if number_of_score_updates == 60:
            score += 1
            number_of_score_updates = 0
        else:
            number_of_score_updates += 1

        if number_of_ufo_updates == 20:
            if ufo_bild == 0:
                for ufo in Ufos:
                    ufo.image = 'ufo'
                ufo_bild = 1
                number_of_ufo_updates = 0
            elif ufo_bild == 1:
                if score > 50:
                    for ufo in Ufos:
                        ufo.image = 'ufo mit strahl'
                    ufo_bild = 0
                    number_of_ufo_updates = 0
        else:
            number_of_ufo_updates += 1

        if number_of_meteor_updates == 5:
            if meteor_bild == 2:
                for meteor in meteore:
                    meteor.image = 'meteor3'
                meteor_bild = 1
                number_of_meteor_updates = 0
            elif meteor_bild == 1:
                for meteor in meteore:
                    meteor.image = 'meteor2'
                meteor_bild = 0
                number_of_meteor_updates = 0
            elif meteor_bild == 0:
                for meteor in meteore:
                    meteor.image = 'meteor'
                meteor_bild = 2
                number_of_meteor_updates = 0           
        else:
            number_of_meteor_updates += 1

        if number_of_raumschiff_updates == 5:
            raumschiff_animation()
            number_of_raumschiff_updates = 0
        else:
            number_of_raumschiff_updates += 1

        if score < 50:
            for meteor in meteore:
                if meteor.y < 800:
                    meteor.y += 3         
                else:
                    meteor.pos = random.randint(20, 1200), random.randint(-800, -50)
                if meteor.colliderect(raumschiff):
                   game_over_funktion()
        elif score > 50:
            for meteor in meteore2:
                if meteor.y < 800:
                    meteor.y += 3         
                else:
                    meteor.pos = random.randint(20, 1200), random.randint(-800, -50)
                    if meteor.colliderect(raumschiff):
                        game_over_funktion()

        if score > 5:
            for Ufo in Ufos:
                if Ufo.y < 800:
                    Ufo.y += 3
                else:
                    Ufo.pos = random.randint(20, 1200), random.randint(-800, -100)

                if Ufo.colliderect(raumschiff):
                    game_over_funktion()

pgzrun.go()