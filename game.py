# access to pygame library
import pygame

pygame.init()
# set window size and define basic colors
SCREEN_TITLE = 'Treasure Seeker'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
BACK = ('assets/images/Background.png')
# clock update for updating game events and frames
# Do this in your class too
clock = pygame.time.Clock()
pygame.font.init()

# These shouldn't be loaded here, they need to be in your Game class
font = pygame.font.SysFont('times new roman',75,True,False)
sc_font = pygame.font.SysFont('times new roman',30,True,True)
winner = pygame.mixer.Sound('assets/sounds/you_win.wav')
crashed = pygame.mixer.Sound('assets/sounds/crashed.wav')

class CachingMetaclass(type):
    def __getattr__(self, name):
        return self._fetch_from_cache(name)

class Sounds(metaclass=CachingMetaclass):
    _sound_cache = {}

    @classmethod
    def _fetch_from_cache(cls, name):
        if name not in cls._sound_cache:
            cls._sound_cache[name] = pygame.mixer.Sound('assets/sounds/%s.wav' % name)
        return cls._sound_cache[name]

class Game:
    # FPS - typical std rate is 60
    TICK_RATE = 60

    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        # create window of specific size and in white color
        self.game_window = pygame.display.set_mode((width, height))
        self.game_window.fill(WHITE_COLOR)
        pygame.display.set_caption(title)
        background_image = pygame.image.load(image_path)
        # "self.image" is not a good variable name. what is this image? what is it for? rename it
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self, level_speed, score):
        is_game_over = False
        did_win = False
        direction = 0
        self.score = score

        pygame.mixer.Sound.play(Sounds.treasure)

        pygame.mixer.music.load('assets/sounds/music_back.wav') # I think this works?
        pygame.mixer.music.play(-1)

        player_character = PlayerCharacter('assets/sprites/Knight1a.png', 375, 700, 50, 50)

        # Instead of listing these like this, why not create an EnemyManager class
        # which can help manage these.
        enemy_0 = EnemyCharacter('assets/sprites/bad_guy.png', 20, 600, 70, 70)
        enemy_0.SPEED *= level_speed

        enemy_1 = EnemyCharacter('assets/sprites/zombie.png', 600, 450, 70, 70)
        enemy_1.SPEED *= level_speed - 2.5

        enemy_2 = EnemyCharacter('assets/sprites/plaguey.png', 500, 300, 70, 70)
        enemy_2.SPEED *= level_speed - 4.5

        enemy_3 = EnemyCharacter('assets/sprites/grimmy.png', 150, 200, 100, 100)
        enemy_3.SPEED *= level_speed - 6.5

        # you've now reused this same variable name for something totally different
        treasure = GameObject('assets/sprites/treasure.png', 375, 20, 50, 50)

        # main game loop, updates for all actions until is_game_over equal True
        while not is_game_over:
            # a loop to get all events in pygame
            for event in pygame.event.get():
                # allows user to quit the game
                if event.type == pygame.QUIT:
                    is_game_over = True
                # detects when key is pressed down
                elif event.type == pygame.KEYDOWN:
                    # move up when up key is pressed
                    if event.key == pygame.K_UP:
                        direction = 1
                    # move down if down key is pressed
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                # detect when key is released
                elif event.type == pygame.KEYUP:
                    # stop moving when key is released
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0

            self.game_window.fill(WHITE_COLOR)
            self.game_window.blit(self.image, (0, 0))

            scoretext = sc_font.render(f"Score {score}", True, (BLACK_COLOR))
            self.game_window.blit(scoretext, (495, 10))

            treasure.draw(self.game_window)

            # Update player position
            player_character.move(direction, self.height)
            # redraws player at new position
            player_character.draw(self.game_window)

            enemy_0.move(self.width)
            enemy_0.draw(self.game_window)

            # Using that EnemyManager class you could just do
            # EnemyManager.get_enemy_for_level_speed(level_speed)
            # instead of having all these if statements
            if level_speed > 3:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_window)
            if level_speed > 5:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_window)
            if level_speed > 7:
                enemy_3.move(self.width)
                enemy_3.draw(self.game_window)

            # create a self.game_over() function that does all this, so you DRY
            if player_character.detect_collision(enemy_0) == True:
                is_game_over = True
                did_win = False
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(crashed)
                pygame.mixer.music.stop()
                text = font.render('You Were Caught!', True, BLACK_COLOR)
                self.game_window.blit(text, (110, 300))
                pygame.display.update()
                clock.tick(1)
                break

            if player_character.detect_collision(enemy_1) == True:
                is_game_over = True
                did_win = False
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(crashed)
                pygame.mixer.music.stop()
                text = font.render('You Were Caught!', True, BLACK_COLOR)
                self.game_window.blit(text, (110, 175))
                pygame.display.update()
                clock.tick(1)
                break

            if player_character.detect_collision(enemy_2) == True:
                is_game_over = True
                did_win = False
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(crashed)
                pygame.mixer.music.stop()
                text = font.render('You Were Caught!', True, BLACK_COLOR)
                self.game_window.blit(text, (110, 175))
                pygame.display.update()
                clock.tick()
                break

            if player_character.detect_collision(enemy_3) == True:
                is_game_over = True
                did_win = False
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(crashed)
                pygame.mixer.music.stop()
                text = font.render('You Were Caught!', True, BLACK_COLOR)
                self.game_window.blit(text, (110, 175))
                pygame.display.update()
                clock.tick(1)
                break

            elif player_character.detect_collision(treasure) == True:
                is_game_over = True
                did_win = True
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(winner)
                pygame.mixer.music.stop()
                text = font.render('WINNER!', True, BLACK_COLOR)
                self.game_window.blit(text, (245, 350))
                pygame.display.update()
                clock.tick(1)
                pygame.time.wait(900)
                break
            pygame.display.update()
            clock.tick(self.TICK_RATE)

        # a lot of this should be in your game_over() function instead
        while is_game_over == True and did_win == False:
            # self.game_window.fill(WHITE_COLOR)
            text = font.render("Press (C) to try again", True, BLACK_COLOR)
            text1 = font.render("or (Q) to quit", True, BLACK_COLOR)
            self.game_window.blit(text, (40, 390))
            self.game_window.blit(text1, (175, 485))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit()
                    if event.key == pygame.K_c:
                        self.run_game_loop(1,0)

        if did_win == True:
            self.run_game_loop(level_speed + 0.5, score + 1)

# a lot of the below would do well to be based on the Sprite class
# there are things like built-in collision detection functions, etc in those

class GameObject:

    def __init__(self, image_path, x, y, width, height):
        object_image = pygame.image.load(image_path)
        # transform image to desired scale
        self.image = pygame.transform.scale(object_image, (width, height))

        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))


# class to represent the character controlls by player
class PlayerCharacter(GameObject):
    # speed at which the char moves
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    # defines movement along the y axis
    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED
        # makes sure that the char never goes below 20 units
        if self.y_pos >= max_height - 40:
            self.y_pos = max_height - 40

    # determines if enemy and player char is on collision possible planes
    def detect_collision(self, enemy_body):
        if self.y_pos > enemy_body.y_pos + enemy_body.height:
            return False
        elif self.y_pos + self.height < enemy_body.y_pos:
            return False

        if self.x_pos > enemy_body.x_pos + enemy_body.width:
            return False
        elif self.x_pos + self.width < enemy_body.x_pos:
            return False

        return True


class EnemyCharacter(GameObject):
    # speed at which the char moves
    SPEED = 4

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    # defines movement along the y axis
    def move(self, max_width):
        if self.x_pos <= 10:
            self.SPEED = abs(self.SPEED)
            self.image = pygame.transform.flip(self.image, 1, 0)
        elif self.x_pos >= max_width - 40:
            self.SPEED = -abs(self.SPEED)
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.x_pos += self.SPEED

        if self.SPEED >= 14:
            self.SPEED = 14

if __name__ == '__main__':
    new_game = Game('assets/images/background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
    new_game.run_game_loop(1, 0)

    pygame.quit()
    quit()
