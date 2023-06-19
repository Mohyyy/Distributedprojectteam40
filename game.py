import random
from time import sleep
import threading
import pygame
import socket


HEADER = 64
FORMAT = 'utf-8'


class CarRacing:



    def game_over(self):
        print(f"Game Over!")
        print(f"Your score: {self.count}")
        print(f"Opponent's score: {self.opponent_score}")
        while True:
            play_again = input("Do you want to play again? (Y/N): ").lower()
            if play_again in ["y", "n"]:
                return play_again == "y"

    def __init__(self, client):

        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None

        self.initialize()


    def initialize(self):

        self.crashed = False

        self.carImg = pygame.image.load('car.png')
        self.car_x_coordinate = (self.display_width * 0.45)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49

        # enemy_car
        self.enemy_car = pygame.image.load('enemy_car_1.png')
        self.enemy_car_startx = random.randrange(310, 450)
        self.enemy_car_starty = -600
        self.enemy_car_speed = 5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        # Background
        self.bgImg = pygame.image.load("back_ground.jpg")
        self.bg_x1 = (self.display_width / 500) - (360 / 500)
        self.bg_x2 = (self.display_width / 500) - (360 / 500)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Dodge')
        self.run_car()



    def run_car(self):

        while not self.crashed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                # print(event)

                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_LEFT):
                        self.car_x_coordinate -= 50
                        print("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    if (event.key == pygame.K_RIGHT):
                        self.car_x_coordinate += 50
                        print("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    print("x: {x}, y: {y}".format(x=self.car_x_coordinate, y=self.car_y_coordinate))

            self.gameDisplay.fill(self.black)
            self.back_ground_raod()

            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.randrange(160, 660)

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.randrange(160, 660)

            self.car(self.car_x_coordinate, self.car_y_coordinate)
            self.highscore(self.count)
            self.count += 1
            if (self.count % 100 == 0):
                self.enemy_car_speed += 1
                self.bg_speed += 1

            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if (self.car_x_coordinate > self.enemy_car_startx and self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width) or (self.car_x_coordinate + self.car_width > self.enemy_car_startx and self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width):
                    self.crashed = True
            if self.car_x_coordinate > 660:
                self.crashed= True
            if self.car_x_coordinate < 160:
                self.crashed = True
            pygame.display.flip()
            self.clock.tick(60)

        self.gameDisplay.fill(self.black)
        self.message_display('You crashed!')

    def display_play_again_message(self):
        font = pygame.font.Font(None, 50)
        text = font.render("Play again? Y/N", True, self.white)
        self.gameDisplay.blit(text, (250, 300))
        pygame.display.flip()

    def game_over(self):
        print(f"Game Over!")
        print(f"Your score: {self.count}")

        self.display_scores()

        while True:
            self.display_play_again_message()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return True
                    elif event.key == pygame.K_n:
                        return False
            sleep(0.1)

    def display_scores(self):
        font = pygame.font.Font(None, 50)
        your_score_text = font.render(f"Your score: {self.count}", True, self.white)
        self.gameDisplay.blit(your_score_text, (400, 400))
        pygame.display.flip()

    def message_display(self, message):
        font = pygame.font.Font(None, 75)
        text = font.render(message, True, self.white)
        self.gameDisplay.blit(text, (200, 250))
        pygame.display.flip()
        sleep(2)
        play_again = self.game_over()
        if play_again:
            self.initialize()
            self.run_car()


    def back_ground_raod(self):

        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def highscore(self, count):
        font = pygame.font.Font(None, 30)
        text = font.render("Score: " + str(count), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    car_racing = CarRacing(client)
    car_racing.racing_window()
