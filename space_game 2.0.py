
from time import sleep
import pgzrun
import random
import math

WIDTH = 1200
HEIGHT = 800
METEOR_ANIMATION_SPEED = 5
UFO_ANIMATION_SPEED = 50
RAUMSCHIFF_ANIMATION_SPEED = 5

class Raumschiff(Actor):
    def __init__(self) -> None:
        super().__init__('raumschiff')
        self.hitbox_radius = 97
        self.hitbox_offset_x = 0
        self.hitbox_offset_y = 0
        self.animation_counter = 0
        self.animation_state = 0

    def update_image(self):
        if self.animation_state == 0:
            self.image = 'raumschiff2'
            self.animation_state = 1
        elif self.animation_state == 1:
            self.image = 'raumschiff3'
            self.animation_state = 2
        elif self.animation_state == 2:
            self.image = 'raumschiff'
            self.animation_state = 0


    def animate(self):
        self.animation_counter += 1
        if self.animation_counter == RAUMSCHIFF_ANIMATION_SPEED:
            self.update_image()
            self.animation_counter = 0


    def is_colliding(self, enemy):
        my_pos = self.center
        enemy_pos = enemy.center
        my_pos = (my_pos[0] + self.hitbox_offset_x, my_pos[1] + self.hitbox_offset_y)
        enemy_pos = (enemy_pos[0] + enemy.hitbox_offset_x, enemy_pos[1] + enemy.hitbox_offset_y)
        distance = math.dist(my_pos, enemy_pos)
        if distance <= self.hitbox_radius + enemy.hitbox_radius:
            return True
        else:
            return False

class Meteor(Actor):
    def __init__(self) -> None:
        super().__init__('meteor')
        self.pos = random.randint(20, 1200), random.randint(-800, -50)
        self.hitbox_radius = 71
        self.hitbox_offset_x = 0
        self.hitbox_offset_y = 60
        self.speed = 3
        self.animation_counter = 0
        self.animation_state = 0

    def update_image(self):
        if self.animation_state == 0:
            self.image = 'meteor2'
            self.animation_state = 1
        elif self.animation_state == 1:
            self.image = 'meteor'
            self.animation_state = 2
        elif self.animation_state == 2:
            self.image = 'meteor3'
            self.animation_state = 0


    def animate(self):
        self.animation_counter += 1
        if self.animation_counter == METEOR_ANIMATION_SPEED:
            self.update_image()
            self.animation_counter = 0

class Ufo(Actor):
    def __init__(self) -> None:
        super().__init__('meteor')
        self.pos = random.randint(20, 1200), random.randint(-800, -50)
        self.hitbox_radius = 120
        self.hitbox_offset_x = 0
        self.hitbox_offset_y = 0
        self.speed = 4
        self.animation_counter = 0
        self.animation_state = 0

    def update_image(self):
        if self.animation_state == 0:
            self.image = 'ufo'
            self.animation_state = 1
        elif self.animation_state == 1:
            self.image = 'ufo mit strahl'
            self.animation_state = 0

    def animate(self):
        self.animation_counter += 1
        if self.animation_counter == UFO_ANIMATION_SPEED:
            self.update_image()
            self.animation_counter = 0


hight_score = None
score = 0
number_of_score_updates = 0
game_over = True
game_over_screen = Actor('game over2')
game_over_screen.pos = 600, 400
main_screen = Actor('main menü')
main_screen.pos = 600, 400
raumschiff = Raumschiff()
raumschiff.pos = 400, 500

enemies = [Meteor() for _ in range(4)]

def get_hightscore():
    #you have to add the your hightscore txt
    with open('path of hightscore txt', 'r') as hight_scores:
        hightscore = hight_scores.read()
        return hightscore

def save_hightscore(new_hightscore):
    #you have to add the your hightscore txt
    open('path of hightscore txt', 'w').close()
    with open('path of hightscore txt', 'a') as hight_scores:
        hight_scores.write(str(new_hightscore))


def musik_player():
    if not game_over:
        music.play('background')
    else:
        music.play('background2')

musik_player()

def restart():
    global score, game_over, hight_score
    score = 0
    game_over = False
    hight_score = get_hightscore()
    game_over_screen.image = 'game over2'
    music.play_once('übergang')
    music.queue('background')
    sleep(0.6)
    for meteor in enemies:
        meteor.pos = random.randint(20, 1200), random.randint(-800, -50)

def game_over_funktion():
    global game_over, hight_score, score
    game_over_screen.image = 'game over'
    music.play_once('game over')
    game_over = True
    music.queue('background2')
    if int(hight_score) < int(score):
        save_hightscore(score)


def draw():
    global score, hight_score
    screen.clear()
    screen.blit('space', (200, 0))
    game_over_screen.draw()
    if not game_over:
        screen.draw.text(str(score) + ' / ' + str(hight_score), color='green',  topleft=(1000, 60), fontsize=60)
        raumschiff.draw()
        for meteor in enemies:
            meteor.draw()
    elif game_over:
        main_screen.draw()
        
def update():
    global game_over, score,  number_of_score_updates
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

        raumschiff.animate()

        for enemy in enemies:
            enemy.animate()
            if enemy.y < 800:
                enemy.y += enemy.speed        
            else:
                enemy.pos = random.randint(20, 1200), random.randint(-800, -50)
            if raumschiff.is_colliding(enemy):
                game_over_funktion()

        if score >= 10 and len(enemies) == 4:
            enemies.append(Ufo())

pgzrun.go()