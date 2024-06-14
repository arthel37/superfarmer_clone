import pygame
import random
import math
import copy

#This function generates two random numbers from 0 to 11 - those represent the result of 2 12 sided dice roll
def roll_dice():
    return die1[random.randint(0, 11)], die2[random.randint(0, 11)] 

#This function checks if mouse cursor is inside of button borders
def check_border(button_name):
    (x,y) = pygame.mouse.get_pos()  #x, y - mouse cursor coordinates
    return x >= button_name.x1 and x <= (button_name.x1 + button_name.x2) and y >= button_name.y1 and y <= (button_name.y1 + button_name.y2)    #True if in borders

#This function does basically the same as the function above, however is designed specifically for barter screen, which contains a lot of similar buttons. It returns the id of a button, if it was clicked.
def check_barter_borders(button_list):
    (x,y) = pygame.mouse.get_pos()  #x, y - mouse cursor coordinates
    for i in range(len(button_list)):
        if x >= button_list[i].x and x <= (button_list[i].x + 25) and y >= button_list[i].y and y <= (button_list[i].y + 50): #True if cursor is in borders
            return i    #Returns the id of a button
    return -1

#This function takes the result of the roll from roll_dice() function and calculates if and how many animals should the player get
def breeding(ind1, ind2):
    if ind1 == ind2:                                #If both dice show the same image
        temp_player.farm[ind1] += 2                 #Temporary object of the player class used to calculate the increase of animals
        if math.floor(temp_player.farm[ind1]/2) < bank.farm[ind1]:              #True if the rounded down result of halving sum of player's animals and their dice roll is smaller than the bank's reserves. This is done to ensure no player gets more tokens than possible.
            bank.farm[ind1] -= math.floor(temp_player.farm[ind1]/2)             #Calculated amount of animals gets subtracted from the bank
            active_player.farm[ind1] += math.floor(temp_player.farm[ind1]/2)    #And then added to the player's farm
        else:
            active_player.farm[ind1] += bank.farm[ind1] #If calculated amount of animals is higher than the bank reserves, player only gets the bank reserves
            bank.farm[ind1] = 0                         #And then bank reserves are set to 0
    else:
        if (ind1 < 6):                  #Rolls higher than 5 represent a Wolf and a Fox, both processed in separate functions
            temp_player.farm[ind1] += 1 #As in lines 26:32, but for different rolls, so done twice
            if math.floor(temp_player.farm[ind1]/2) < bank.farm[ind1]:
                bank.farm[ind1] -= math.floor(temp_player.farm[ind1]/2)
                active_player.farm[ind1] += math.floor(temp_player.farm[ind1]/2)
            else:
                active_player.farm[ind1] += bank.farm[ind1]
                bank.farm[ind1] = 0
        if (ind2 < 6):    
            temp_player.farm[ind2] += 1
            if math.floor(temp_player.farm[ind2]/2) < bank.farm[ind2]:
                bank.farm[ind2] -= math.floor(temp_player.farm[ind2]/2)
                active_player.farm[ind2] += math.floor(temp_player.farm[ind2]/2)
            else:
                active_player.farm[ind2] += bank.farm[ind2]
                bank.farm[ind2] = 0

#This function is responsible for dealing with a Wolf roll
def wolf():
    if active_player.farm[6] != 0:              #If the player has a Large Dog 
        active_player.farm[6] -= 1              #They lose only the large dog
        bank.farm[6] += 1                       #And the dog gets back to the bank
    else:
        bank.farm[1] += active_player.farm[1]   #Otherwise every sheep, pig and cow is returned to the bank
        bank.farm[2] += active_player.farm[2]
        bank.farm[3] += active_player.farm[3]

        active_player.farm[1] = 0
        active_player.farm[2] = 0
        active_player.farm[3] = 0

#This function deals with the Fox roll
def fox():
    if active_player.farm[5] != 0:              #If the player has a Small Dog
        active_player.farm[5] -= 1              #They lose only the Small Dog
        bank.farm[5] += 1                       #And the dog gets back to the bank
    else:
        bank.farm[0] += active_player.farm[0]   #Otherwise every rabbit, except one,  is returned to the bank
        active_player.farm[0] = 1

#This function resets players animal counts and gets rid of tokens
def reset():
    for player in list_of_players:
        player.farm = [1, 0, 0, 0, 0, 0, 0]
    bank.farm = [60, 24, 20, 12, 6, 4, 2]
    tokens.empty()

#This function deals with the bartering mechanic with current offered and wanted animals being stored in bartering inventories
def barter(turn, barter_ind):
    temp1 = sum([x*y for x, y in zip(barter_players_inv[turn+1], value_list)])  #First, the appropriate value of all offered animals is calculated
    if barter_ind < turn+1:         #This is done because the active player is removed from the player's list so they can't barter with themselves. If selected player/ bank has index lower than active player, nothing changes, otherwise the index is increased by 1.
        temp2 = sum([x*y for x, y in zip(barter_players_inv[barter_ind], value_list)]) #The appropriate value of all wanted animals is calculated
    else:
        temp2 = sum([x*y for x, y in zip(barter_players_inv[barter_ind+1], value_list)])
    if temp1 == temp2:              #If calculated values of offered and wanted animals are equal
        if barter_ind < turn + 1:   #Same as before, due to the removal of active player's index, if selected player/bank's index is lower, nothing happens, otherwise bartering index is increased
            active_player.farm = [x + y for x, y in zip(active_player.farm, barter_players_inv[barter_ind])]                            #Active player gets all wanted animals
            active_player.farm = [x - y for x, y in zip(active_player.farm, barter_players_inv[turn+1])]                                #In exchange for all of their offered animals
            list_of_players[barter_ind].farm = [x + y for x, y in zip(list_of_players[barter_ind].farm, barter_players_inv[turn+1])]    #Which are added to the bartering partners farm
            list_of_players[barter_ind].farm = [x - y for x, y in zip(list_of_players[barter_ind].farm, barter_players_inv[barter_ind])]
        else:
            active_player.farm = [x + y for x, y in zip(active_player.farm, barter_players_inv[barter_ind+1])]                          #Same as before, but barteting index is increased
            active_player.farm = [x - y for x, y in zip(active_player.farm, barter_players_inv[turn+1])]
            list_of_players[barter_ind+1].farm = [x + y for x, y in zip(list_of_players[barter_ind+1].farm, barter_players_inv[turn+1])]
            list_of_players[barter_ind+1].farm = [x - y for x, y in zip(list_of_players[barter_ind+1].farm, barter_players_inv[barter_ind+1])]
    for x in range(len(barter_players_inv)):
        barter_players_inv[x] = [0, 0, 0, 0, 0, 0, 0] #This clears the bartering inventories

#This function checks if the active player fulfills the winning conditions
def score_check(player):
    for animal in player.farm[:5]: 
        if animal < 1:              #If at least one of the first five (6 and 7 are small and large dogs respectively and do not count towards winning) animal counts is 0, function returns False
            return False
    return True

#This is a screen class
class Screen():
    def __init__(self, width, height):
        self.width = width      #variables for window dimensions
        self.height = height

    def init_window(self):
        self.display = pygame.display.set_mode((self.width, self.height))   #Sets the window dimensions for the current screen
        return self.display

#This is a button class
class Button():
    def __init__(self, x1, x2, y1, y2, text):
        self.x1 = x1        #x1 and y1 are start point cooridantes, they dictate where the upper left corner of the button is to be located
        self.x2 = x2        #x2 and y2 represent width and height of the button
        self.y1 = y1
        self.y2 = y2
        self.button_colour = (255, 255, 255)            #All buttons are white unless stated otherwise
        self.font = pygame.font.SysFont("impact", 30)   #All buttons have their description in the impact font, size 30
        self.font_colour = (0, 0, 0)                    #All buttons' descriptions are black
        self.text = text    #Button's description

    def draw_button(self, display): #This method draws the button on the selected screen
        pygame.draw.rect(display, self.button_colour, (self.x1, self.y1, self.x2, self.y2))                         #First, the method draws a rectangle on a selected screen, of selected colour and in selected place
        text_surface = self.font.render(self.text, False, self.font_colour)                                         #Then, the method creates a text surface with button's description
        display.blit(text_surface, ((self.x1 + (self.x2/2) - 15*len(self.text)/2, (self.y1 + (self.y2/2) - 15))))   #Lastly, the method draws the text surface on top of the button

#This class represents the decrease buttons for offers in bartering
class BarterOfferLessButton():
    def __init__(self, index):
        self.index = index                                      #This index is used for in-loop generation, as well as for identifying which counter should get decreased after click event
        self.text = "<"                                         #These buttons have < (substitute for left arrow) as description
        self.button_colour = (230, 230, 230)                    #These buttons are all light grey
        self.font = pygame.font.SysFont("impact", 30)           #Their "descriptions" are in the impact font, size 30
        self.font_colour = (0, 0, 0)                            #And thesea arrows are all black
        self.x = barter_coordinates_list[self.index][0] + 55    #As for coordinates, these are loaded from a list containing all positions for bartering
        self.y = barter_coordinates_list[self.index][1]
    
    def draw_button(self, display):                                                 #This is the same method as in Button class
        pygame.draw.rect(display, self.button_colour, (self.x , self.y, 25, 50))    #The only difference being here dx and dy are constant
        text_surface = self.font.render(self.text, False, self.font_colour)
        display.blit(text_surface, (self.x + 12 - 15*len(self.text)/2, self.y + 5))

#This class represents the decrease buttons for recipient, this was done to differentiate between positions of both parties buttons, everything else is the same. For reference go to line 136
class BarterRecipLessButton():
    def __init__(self, index):
        self.index = index
        self.text = "<"
        self.button_colour = (230, 230, 230)
        self.font = pygame.font.SysFont("impact", 30)
        self.font_colour = (0, 0, 0)
        self.x = barter_coordinates_list[self.index][0] - 135
        self.y = barter_coordinates_list[self.index][1]
    
    def draw_button(self, display):
        pygame.draw.rect(display, self.button_colour, (self.x, self.y, 25, 50))
        text_surface = self.font.render(self.text, False, self.font_colour)
        display.blit(text_surface, (self.x + 12 - 15*len(self.text)/2, self.y + 5))

#This class represents the increase button for offers in bartering. For reference go to line 136
class BarterOfferMoreButton():
    def __init__(self, index):
        self.index = index
        self.text = ">"
        self.button_colour = (230, 230, 230)
        self.font = pygame.font.SysFont("impact", 30)
        self.font_colour = (0, 0, 0)
        self.x = barter_coordinates_list[self.index][0] + 160
        self.y = barter_coordinates_list[self.index][1]

    def draw_button(self, display):
        pygame.draw.rect(display, self.button_colour, (self.x, self.y, 25, 50))
        text_surface = self.font.render(self.text, False, self.font_colour)
        display.blit(text_surface, (self.x + 12 - 15*len(self.text)/2, self.y + 5))

#This class represents the increase button for recipient. For reference go to line 136
class BarterRecipMoreButton():
    def __init__(self, index):
        self.index = index
        self.text = ">"
        self.button_colour = (230, 230, 230)
        self.font = pygame.font.SysFont("impact", 30)
        self.font_colour = (0, 0, 0)
        self.x = barter_coordinates_list[self.index][0] - 30  
        self.y = barter_coordinates_list[self.index][1]

    def draw_button(self, display):
        pygame.draw.rect(display, self.button_colour, (self.x, self.y, 25, 50))
        text_surface = self.font.render(self.text, False, self.font_colour)
        display.blit(text_surface, (self.x +15 - 15*len(self.text)/2, self.y + 5))

#The Token class serves to innitialize tokens
class Token(pygame.sprite.Sprite):
    def __init__(self, image, location):        
        pygame.sprite.Sprite.__init__(self)     #These tokens are pygame's sprites
        self.image = pygame.image.load(image)   #They consist of an image
        self.rect = self.image.get_rect()       #Of which this function creates a rect type object
        self.rect.x, self.rect.y = location     #And it's location

#This class is primarily used for displaying counters, ultimately it can be used for displaying static text as well.
class Counter():
    def __init__(self, x, y, count):
        self.x = x                                      #Firstly, x and y represent coordinates for displaying the counter
        self.y = y
        self.count = str(count)                         #Count is the displayed text
        self.font = pygame.font.SysFont("impact", 30)   #Text in font impact, size 30
        self.font_colour = (0, 0, 0)                    #And in black

    def write_counter(self, display, count):            #This method displays the counter just like the draw_button() method does, however without displaying the rectangle underneath. See line 131
        text_surface = self.font.render(str(count), True, self.font_colour) 
        display.blit(text_surface, (self.x + 25 - 15*len(str(count))/2, self.y + 50))

#These next two classes serve as counters for the offering and recipients party. See line 209 for reference
class BarterOfferCounter():
    def __init__(self, index, count):
        self.index = index                                      #The difference is that this class does not take in coordinates, instead taking in the appropriate animal index
        self.count = str(count)
        self.font = pygame.font.SysFont("impact", 30)
        self.font_colour = (0, 0, 0)
        self.x, self.y = barter_coordinates_list[self.index]   #Coordinates are loaded from the barter coordinates list
    
    def write_counter(self, display, count):
        text_surface = self.font.render(str(count), False, self.font_colour)
        display.blit(text_surface, (self.x + 120 - 15*len(str(count))/2, self.y + 5))

#As stated above
class BarterRecipCounter():
    def __init__(self, index, count):
        self.index = index
        self.count = str(count)
        self.font = pygame.font.SysFont("impact", 30)
        self.font_colour = (0, 0, 0)
        self.x, self.y = barter_coordinates_list[self.index]

    def write_counter(self, display, count):
        text_surface = self.font.render(str(count), False, self.font_colour)
        display.blit(text_surface, (self.x - 70 - 15*len(str(count))/2, self.y + 5))

#PLayer class is quite self explanatory. Every player, including temporary objects used for calculation and a bank, have a farm, which is represented by a list.
class Player():
    def __init__(self):
        self.farm = [1, 0, 0, 0, 0, 0, 0]   #Inside the list, number of each animal is stored. See line 252 for reference which animal is which index.

animal_list = ["Rabbit", "Sheep", "Pig", "Cow", "Horse", "Small Dog", "Large Dog", "", "Fox", "Wolf"]   #List of all animals in the game with their correlation to indices used in player.farm and dice rolls
value_list = [1, 6, 12, 36, 72, 6, 36]                                                                  #List of every animal's value taken from the games rules.

die1 = [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 3, 9] #These two lists represent the 12 sides of each dice. For refererence (which animal is which index) see line 252
die2 = [0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 4, 8]

player1 = Player()  #Declaring all players
player2 = Player()
player3 = Player()
player4 = Player()
bank = Player()

list_of_players = [bank, player1, player2, player3, player4]    #Combining players into a list used for reference in loops
active_player = list_of_players[1]                              #For clarity, player in his turn is refered to as active_player
temp_player = Player()                                          #Player object used for calculation

barter_options_full = ["Bank", "Player 1", "Player 2", "Player 3", "Player 4"]  #Players' names for reference in bartering menu
barter_ind = 0                                                                  #This index is used to refer to bartering partner during bartering
barter_players_inv = []                                                         #Declaring an empty list. This will later contain every players' inventory during bartering

scoreboard = [] #Declaring an empty list to later store scores

pygame.init()           #Next three lines of code initialize the pygame module itself,
pygame.font.init()      #the pygame font module (for displaying text)
pygame.mixer.init()     #and the pygame mixer module (for playing sounds)

farmer_song = pygame.mixer.Sound("images/farmer.mp3")  #The song is loaded as an Sound object
farmer_song.set_volume(0.3)                     #It's volume is set to 30%
farmer_song.play(-1)                            #And it is played on repeat

main_menu = Screen(1280, 720)                   #Next 6 lines of code create screen objects for every screen in the game. Main menu
game_screen = Screen(1280, 720)                 #Core gameplay screen
pause_screen = Screen(1280, 720)                #Pause screen during gameplay
rules_screen = Screen(1280, 720)                #Rules screen accessed in the menu
barter_screen = Screen(1280, 720)               #Barter screen for bartering mechanic
score_screen = Screen(1280, 720)                #Score screen for displaying scoreboard at the end of the game

players_coordinates = [(game_screen.width/2 - 135, game_screen.height/3 + 10), (game_screen.width/2 - 135, 2*game_screen.height/3 + 10), (game_screen.width/2 - 135, 10), (game_screen.width/6 - 135, game_screen.height/3 + 10), (5*game_screen.width/6 - 135, game_screen.height/3 + 10)]
bank_coordinates = players_coordinates[0]       #The player coordinates are used for displaying each player's tokens
player1_coordinates = players_coordinates[1]
player2_coordinates = players_coordinates[2]
player3_coordinates = players_coordinates[3]
player4_coordinates = players_coordinates[4]

barter_coordinates_list = []    #barter coordinates are used for displaying each animal's token during bartering
for i in range(2):
    for n in range(7):
        barter_coordinates_list.append((barter_screen.width/5 + i*3*barter_screen.width/5 - 25, barter_screen.height/2 - 190 + n*55))

number_of_players = 4           #declaring variables for number of players and turn choosing
turn = 0

#Declaring the main menu buttons
quit_button = Button(main_menu.width/2 - 75, 150, main_menu.height/2 + 185, 75, "Quit")                     #Exit the game
play_button = Button(main_menu.width/2 - 75, 150, main_menu.height/2 - 60, 75, "New game")                  #Start new game
continue_button = Button(main_menu.width/2 - 235, 150, main_menu.height/2 - 60, 75, "Continue")             #Continue current game
number_button = Button(main_menu.width/2 + 200, 75, main_menu.height/2 - 60, 75, str(number_of_players))    #Unclickable button for displaying no of players
less_button = Button(main_menu.width/2 + 120, 60, main_menu.height/2 - 60, 75, "<")                         #Button for decreasing no of players
less_button.button_colour = (230, 230, 230)                                                                 #and it's light grey colour declaration
more_button = Button(main_menu.width/2 + 295, 60, main_menu.height/2 - 60, 75, ">")                         #Button for increasing no of players
more_button.button_colour = (230, 230, 230)                                                                 #and it's colour
rules_button = Button(main_menu.width/2 - 75, 150, main_menu.height/2 + 60, 75, "Rules")                    #Display rules button

#Declaring the gameplay screen buttons
pause_button = Button(0, 100, 0, 50, "Pause")                                                               #Pause
end_turn_button = Button(game_screen.width - 150, 150, game_screen.height - 50, 50, "End turn")             #End turn
roll_dice_button = Button(0, 150, game_screen.height - 50, 50, "Roll dice")                                 #Roll the dice
barter_button = Button(160, 150, game_screen.height - 50, 50, "Barter")                                     #Open bartering menu
turn_background = Button(game_screen.width - 230, 165, 0, 40, "")                                           #Unclickable button for displaying current player's turn

#Declaring the pause menu buttons
resume_button = Button(pause_screen.width/2 - 75, 150, pause_screen.height/2 - 60, 75, "Resume")            #Resume current game
back_to_menu_button = Button(pause_screen.width/2 - 75, 150, pause_screen.height/2 + 60, 75, "Main menu")   #Go back to main menu

#Declaring the rules menu button
back_button = Button(rules_screen.width/2 - 75, 150, rules_screen.height - 75, 75, "Back")                  #Go back to main menu

#Declaring the bartering menu buttons
prev_player_button = Button(barter_screen.width/2 - 160, 50, 100, 75, "<")                                  #Change recipient to the previous player
prev_player_button.button_colour = (230, 230, 230)
next_player_button = Button(barter_screen.width/2 + 110, 50, 100, 75, ">")                                  #Change recipient to the next player
next_player_button.button_colour = (230, 230, 230)
id_button = Button(barter_screen.width/2 - 100, 200, 100, 75, barter_options_full[barter_ind])              #Display current recipient 
accept_button = Button(barter_screen.width/2 - 75, 150, barter_screen.height - 160, 75, "Barter")           #Make an offer
recip_accept_button = Button(barter_screen.width - 210, 200, barter_screen.height/2 + 10, 75, "Accept offer")#Accept (for recipient if not bank)

#Declaring the bartering menu buttons lists
less_buttons1 = []
less_buttons2 = []
more_buttons1 = []
more_buttons2 = []
barter_counters1 = []
barter_counters2 = []
for k in range(7):  #These are done in a loop due to the amount of repeating buttons
    less_buttons1.append(BarterOfferLessButton(k))
    less_buttons2.append(BarterRecipLessButton(7+k))
    more_buttons1.append(BarterOfferMoreButton(k))
    more_buttons2.append(BarterRecipMoreButton(7+k))
    barter_counters1.append(BarterOfferCounter(k, "0"))
    barter_counters2.append(BarterRecipCounter(7+k, "0"))

#Loading images
bckg_anim1 = pygame.image.load("images/bckg1.jpg")  #Main menu animation 1st frame
bckg_anim2 = pygame.image.load("images/bckg2.jpg")  #2nd frame
bckg_anim3 = pygame.image.load("images/bckg3.jpg")  #3rd frame
rules = pygame.image.load("images/rules.png")       #rules are displayed as an image due to pygame's inability to display multi-line text
rates = pygame.image.load("images/rates.png")       #same as before, rates of exchange are displayed as an image
title = pygame.image.load("images/title.png")       #Title of the game

#Scaling main menu animations to fit the screen
bckg_anim1 = pygame.transform.scale(bckg_anim1, (main_menu.width, main_menu.height))
bckg_anim2 = pygame.transform.scale(bckg_anim2, (main_menu.width, main_menu.height))
bckg_anim3 = pygame.transform.scale(bckg_anim3, (main_menu.width, main_menu.height))

pressed_last_state = False  #Declaring variables for mouse click detection
pressed_state = False

tokens = pygame.sprite.Group()          #Declaring sprite groups for in-game tokens
barter_tokens = pygame.sprite.Group()   #and for bartering

#Declaring players' animal counters
players_counters = [[0 for x in range(7)] for y in range(5)] #Declaring an 5x7 array of 0s
for i in range(5):
    for j in range(7):
        if j < 5:
            players_counters[i][j] = Counter(players_coordinates[i][0] + j*55, players_coordinates[i][1], str(list_of_players[i].farm[j]))                                  #For the first five animals, their respective counters are placed every 55 pixels from 
        else:                                                                                                                                                               #the player's base coordinates
            players_counters[i][j] = Counter(players_coordinates[i][0] + (j-5)*55, players_coordinates[i][1]+game_screen.height/3 - 160, str(list_of_players[i].farm[j]))   #The other two are spaced alike, however starting over in x directory and a tad lower 
                                                                                                                                                                            #on the screen

#Next 3 are declaration of captions
num_of_play_text = Counter(main_menu.width/2 + 220, main_menu.height/2 - 30, "Players") #Of the number of players in main menu
turn_text = Counter(game_screen.width - 150, - 50, "Player "+str(turn)+" turn")         #Of the current player's turn
curr_roll_text = Counter(200, game_screen.height - 100, "Rolled: ")                     #Of the current dice roll results

#These 5 captions show where each player's farm is located
player1_caption = Counter(game_screen.width/2 + 100, game_screen.height - 100, "Farm I")
player2_caption = Counter(game_screen.width/2 + 90, 130, "Farm II")
player3_caption = Counter(player3_coordinates[0] + 245, game_screen.height/3 + 130, "Farm III")
player4_caption = Counter(player4_coordinates[0] + 245, game_screen.height/3 + 130, "Farm IV")
bank_caption = Counter(game_screen.width/2 + 90, game_screen.height/3 + 130, "Bank")

accept_text = Counter(barter_screen.width - 120, barter_screen.height/2 - 100, "Do you accept?") #This caption is a text message for bartering offer recipient

scoreboard_text = Counter(score_screen.width/2 - 10, 100, "Scoreboard")             #These are captions for scoreboard
score1 = Counter(score_screen.width/2, score_screen.height/2 - 200, "1. Player ")
score2 = Counter(score_screen.width/2, score_screen.height/2 - 150, "2. Player ")
score3 = Counter(score_screen.width/2, score_screen.height/2 - 100, "3. Player ")
score4 = Counter(score_screen.width/2, score_screen.height/2 - 50, "4. Player ")

pygame.display.set_caption("Superfarmer")   #Setting the window name
display = main_menu.init_window()           #Initializing main menu screen
curr_screen = 0                             #Declaring variable for current screen detection
clock = pygame.time.Clock()                 #Starting the game's clock
running = True                              #Setting game's state to running
anim_counter = 0                            #Declaring main menu animation counter
already_rolled = False                      #Declaring a variable to check if the current player has already rolled the dice
game_in_progress = False                    #Declraing a variable to check if a game has already been started (for continuing from main menu)
barter_recip_accept = False                 #Declaring a variable to check if the offer's recipient accepts the offer
has_won = False                             #Declaring a variable to check if the current players has met the winning conditions
turns = []                                  #Declaring an empty list to store possible player turns. This is useful because the game continues after there's only one player left. Players that have already won cannot however take actions.

while running:
    for event in pygame.event.get():                                    #Event handling
        if event.type == pygame.QUIT:                                   #Quitting the game
            running = False
        if not pygame.mouse.get_pressed()[0] and pressed_last_state:    #Checking for mouse click. This actually works when the lpm gets unclicked - it feels better
            pressed_state = True
        else:
            pressed_state = False
        if curr_screen == 0 and pressed_state:                          #Checking if something was clicked in the main menu
            if check_border(quit_button):                               #Exit button
                running = False                                         #Stops the game
            if check_border(rules_button):                              #Rules button
                curr_screen = 3                                         #Opens the rules menu
                rules_screen.init_window()
            if check_border(play_button):                               #Start new game button
                curr_screen = 1                                         #Opens the gameplay screen
                game_in_progress = True                                 #Sets that the game is now in progress
                reset()                                                 #Resets game state. For reference see line 75
                turn = 0                                                #Sets turn list index to 0
                active_turn = turn                                      #Sets active turn to 0
                scoreboard.clear()                                      #Clears both the scoreboard and the possible turns list
                turns.clear()
                for i in range(number_of_players):                      #Creates turns list based off of the number of players set by the user
                    turns.append(i)
                already_rolled = False                                  #Unchecks if the player has already rolled the dice
                bank.farm[0] -= number_of_players                       #Because there can be no more than 60 rabbits and each player starts with 1, 
                barter_players_inv.clear()                              #Clears bartering inventories
                barter_players_inv.append([0, 0, 0, 0, 0, 0, 0])        #Then adds bank's inventory
                for n in range(number_of_players):                      #And participating players' inventories
                    barter_players_inv.append([0, 0, 0, 0, 0, 0, 0])

                for player_coordinates in players_coordinates[:number_of_players+1]:    #Creates sprites for every animal for every player, including bank
                    rabbit_token = Token("images/rabbit_token_r.jpg", (player_coordinates[0], player_coordinates[1]))
                    tokens.add(rabbit_token)
                    sheep_token = Token("images/sheep_token_r.jpg", (player_coordinates[0] + 55, player_coordinates[1]))
                    tokens.add(sheep_token)
                    pig_token = Token("images/pig_token_r.jpg", (player_coordinates[0] + 110, player_coordinates[1]))
                    tokens.add(pig_token)
                    cow_token = Token("images/cow_token_r.jpg", (player_coordinates[0] + 165, player_coordinates[1]))
                    tokens.add(cow_token)
                    horse_token = Token("images/horse_token_r.jpg", (player_coordinates[0] + 220, player_coordinates[1]))
                    tokens.add(horse_token)
                    small_dog_token = Token("images/s_dog_token_r.jpg", (player_coordinates[0], player_coordinates[1] + game_screen.height/3 - 70))
                    tokens.add(small_dog_token)
                    large_dog_token = Token("images/l_dog_token_r.jpg", (player_coordinates[0] + 55, player_coordinates[1] + game_screen.height/3 - 70))
                    tokens.add(large_dog_token)


                game_screen.init_window()
            if check_border(continue_button):                           #If a game is in progress, changes the screen to the gameplay screen
                curr_screen = 1
                game_screen.init_window()
            if check_border(less_button) and number_of_players > 2:     #Decreases number of players to no less than 2
                number_of_players -= 1
                number_button.text = str(number_of_players)
            if check_border(more_button) and number_of_players < 4:     #Increases number of players to no more than 4
                number_of_players += 1
                number_button.text = str(number_of_players)
        elif curr_screen == 1 and pressed_state:                                #Checks for clicks on the gameplay screen
            if check_border(pause_button):                                      #Pauses the game and displays pause menu
                curr_screen = 2
                pause_screen.init_window()
            if check_border(end_turn_button) and (already_rolled or has_won):   #Ends the current player's turn if they have already rolled the dice or met the winning conditions
                if has_won:                                                     #If the current player has met the winning conditions:
                    scoreboard.append(active_turn+1)                            #-His number gets added to the topmost place on the scoreboard
                    turns.pop(turn)                                             #-His turn gets deleted from possible turns
                    turn -= 1                                                   #-Turn counter decreases
                    has_won = False                                             #-Unchecks winning condition
                if len(turns) < 2:                                              #If there is only one player left:
                    curr_screen = 5                                             #-Displays scoreboard screen 
                    scoreboard.append(active_turn)                              #-Adds the last player's number to the last place on the scoreboard
                    game_in_progress = False                                    #-Unchecks game in progress (ends the game)
                    score_screen.init_window()
                else:    
                    turn += 1                                                   #Turn counter moves to the next player
                    if turn > len(turns) - 1:                                   #From the last player to the first player
                        turn = 0
                    active_turn = turns[turn]                                   #Active turn is chosen from possible turns. This is done to exclude players that have already finished the game
                    active_player = list_of_players[active_turn+1]              #Active player is set
                    already_rolled = False                                      #Unchecks if active player has already rolled
            if check_border(roll_dice_button) and not already_rolled and not has_won:   #If the player tries to roll the dice and haven't already done rolled or met the winning conditions
                temp_player.farm = copy.copy(active_player.farm)                        #Temporary player farm gets copied from active player's farm
                curr_roll = roll_dice()                                                 #Dice roll function call. For reference see the line 7
                breeding(curr_roll[0], curr_roll[1])                                    #Breeding function call. For reference see the line 24
                if curr_roll[0] == 9:                                                   #If the player has rolled the wolf, calls the function wolf. For reference see the line 52
                    wolf()
                elif curr_roll[1] == 8:                                                 #If the player has rolled the fox, calls the fox function. For reference see the line 66
                    fox()
                already_rolled = True                                                   #Checks that the player has already rolled
            if check_border(barter_button):                                     #If bartering button was clicked
                curr_screen = 4                                                 #Displays bartering screen

                for i in range(2):                                              #Creates the bartering menu sprites
                    rabbit_token = Token("images/rabbit_token_r.jpg", barter_coordinates_list[0+7*i])
                    barter_tokens.add(rabbit_token)
                    sheep_token = Token("images/sheep_token_r.jpg", barter_coordinates_list[1+7*i])
                    barter_tokens.add(sheep_token)
                    pig_token = Token("images/pig_token_r.jpg", barter_coordinates_list[2+7*i])
                    barter_tokens.add(pig_token)
                    cow_token = Token("images/cow_token_r.jpg", barter_coordinates_list[3+7*i])
                    barter_tokens.add(cow_token)
                    horse_token = Token("images/horse_token_r.jpg", barter_coordinates_list[4+7*i])
                    barter_tokens.add(horse_token)
                    small_dog_token = Token("images/s_dog_token_r.jpg", barter_coordinates_list[5+7*i])
                    barter_tokens.add(small_dog_token)
                    large_dog_token = Token("images/l_dog_token_r.jpg", barter_coordinates_list[6+7*i])
                    barter_tokens.add(large_dog_token)

                barter_screen.init_window()
        elif curr_screen == 2 and pressed_state:                #Checks for clicks on the pause screen 
            if check_border(resume_button):                     #Resumes the game
                curr_screen = 1                                 #Displays gameplay screen
                game_screen.init_window()
            if check_border(back_to_menu_button):               #Goes back to main menu
                curr_screen = 0                                 #Displays the main menu
                main_menu.init_window()
        elif curr_screen == 3 and pressed_state:                #Checks for clicks in the rules menu
            if check_border(back_button):                       #Goes back to main menu
                curr_screen = 0
                main_menu.init_window()
        elif curr_screen == 4 and pressed_state:                #Checks for clicks in the bartering menu
            if check_border(prev_player_button):                #If the player changes the player to the left
                barter_options = copy.copy(barter_options_full) #Barter options are possible bartering partners. They are copied from a list of all player names
                barter_options.pop(turn+1)                      #Current player's name gets removed from the list
                barter_ind -= 1                                 #Current bartering partner index is decreased
                if barter_ind < 0:                              #Decreasing from bank leads to the last possible player
                    barter_ind = number_of_players - 1
                id_button.text = barter_options[barter_ind]     #Displays the current bartering partner
            if check_border(next_player_button):                #Same as before but for the next bartering partner
                barter_options = copy.copy(barter_options_full)
                barter_options.pop(turn+1)
                barter_ind += 1
                if barter_ind > number_of_players - 1:
                    barter_ind = 0
                id_button.text = barter_options[barter_ind]
            if check_border(back_button):                       #Goes back to the gameplay screen
                curr_screen = 1
                game_screen.init_window()
            if check_border(recip_accept_button):               #Checks if the recipient accepts
                barter_recip_accept = True
            if check_border(accept_button):                     #Checks if the offer is made
                if barter_ind == 0:                             #For the bank calls barter function immediately. For reference see the line 82
                    barter(turn, barter_ind)
                elif barter_recip_accept == True:               #As for other players, additionally checks if the recipient accepts before calling the barter function
                    barter(turn, barter_ind)
                barter_recip_accept = False                     #Unchecks the recipient' accept


            less_button_id1 = check_barter_borders(less_buttons1)                                                                               #Gets the index of clicked bartering decrease buttons
            if less_button_id1 != -1 and barter_players_inv[turn+1][less_button_id1] > 0:                                                       #If a button was clicked and current amount in the active players inventory is bigger than 0
                barter_players_inv[turn+1][less_button_id1] -= 1                                                                                #Decreases the amount of an animal respective to the clicked button index in the active player's inventory
            more_button_id1 = check_barter_borders(more_buttons1)                                                                               #Same for the increase buttons
            if more_button_id1 != -1 and barter_players_inv[turn+1][more_button_id1] < active_player.farm[more_button_id1]:                     #This time checks if the amount in the bartering inventory does not exceed the actual farm amount
                barter_players_inv[turn+1][more_button_id1] += 1

            less_button_id2 = check_barter_borders(less_buttons2)                                                                               #This is the same as before, but for the recipient's side
            if less_button_id2 != -1:
                if barter_ind < turn+1 and barter_players_inv[barter_ind][less_button_id2] > 0:                                                 #This is done beacuse of the removal of the players that have already won
                    barter_players_inv[barter_ind][less_button_id2] -= 1
                elif barter_players_inv[barter_ind+1][less_button_id2] > 0:
                    barter_players_inv[barter_ind+1][less_button_id2] -= 1

            more_button_id2 = check_barter_borders(more_buttons2)
            if more_button_id2 != -1 :
                if barter_ind < turn+1 and barter_players_inv[barter_ind][more_button_id2] < list_of_players[barter_ind].farm[more_button_id2]: 
                    barter_players_inv[barter_ind][more_button_id2] += 1
                elif barter_players_inv[barter_ind+1][more_button_id2] < list_of_players[barter_ind + 1].farm[more_button_id2]:
                    barter_players_inv[barter_ind+1][more_button_id2] += 1

        elif curr_screen == 5 and pressed_state:                #Checks for clicks on the scoreboard screen
            if check_border(back_to_menu_button):               #Goes back to main menu
                curr_screen = 0
                main_menu.init_window()

    if curr_screen == 0:                                        #Displays items on the main menu screen
        display.fill((255, 255, 255))                           #Fills the screen with white (this is a background and gets drawn over)
        if anim_counter <= 20:                                  #Changes the current background animation frames
            display.blit(bckg_anim1, (0,0))
        elif anim_counter <= 40:
            display.blit(bckg_anim2, (0,0))
        elif anim_counter <= 60:
            display.blit(bckg_anim3, (0,0))

        display.blit(title, (main_menu.width/2 - 500, 100))     #Displays the title

        quit_button.draw_button(display)                        #Displays buttons and captions for: quitting,
        play_button.draw_button(display)                        #starting new game,
        number_button.draw_button(display)                      #no of players background,
        less_button.draw_button(display)                        #no of players decrease,
        more_button.draw_button(display)                        #no of players increase,
        num_of_play_text.write_counter(display, "Players")      #no of players,
        rules_button.draw_button(display)                       #displaying rules,
        if game_in_progress:
            continue_button.draw_button(display)                #and if game is already in progress - for continuing.

    elif curr_screen == 1:                                                                                                                      #Displays items on the gameplay screen
        display.fill("green")
        pygame.draw.line(display, (0, 0, 0), (0, 0), (game_screen.width/3, game_screen.height/3), 2)                                            #These lines divide the gameplay screen to 5 zones (1 for each player and a bank)
        pygame.draw.line(display, (0, 0, 0), (game_screen.width/3, game_screen.height/3), (2*game_screen.width/3, game_screen.height/3), 2)
        pygame.draw.line(display, (0, 0, 0), (2*game_screen.width/3, game_screen.height/3), (game_screen.width, 0), 2)
        pygame.draw.line(display, (0, 0, 0), (2*game_screen.width/3, game_screen.height/3), (2*game_screen.width/3, 2*game_screen.height/3), 2)
        pygame.draw.line(display, (0, 0, 0), (2*game_screen.width/3, 2*game_screen.height/3), (game_screen.width, game_screen.height), 2)
        pygame.draw.line(display, (0, 0, 0), (2*game_screen.width/3, 2*game_screen.height/3), (game_screen.width/3, 2*game_screen.height/3), 2)
        pygame.draw.line(display, (0, 0, 0), (game_screen.width/3, 2*game_screen.height/3), (game_screen.width/3, game_screen.height/3), 2)
        pygame.draw.line(display, (0, 0, 0), (game_screen.width/3, 2*game_screen.height/3), (0, game_screen.height), 2)

        pause_button.draw_button(display)                           #Pause button
        end_turn_button.draw_button(display)                        #End turn button
        if not already_rolled:
            roll_dice_button.draw_button(display)                   #If the active player didn't roll the dice, roll and barter buttons
            barter_button.draw_button(display)
        else:
            curr_roll_text.write_counter(display, "Rolled: "+animal_list[curr_roll[0]]+" and "+animal_list[curr_roll[1]])   #if the active player has already rolled this displays the results

        tokens.update()                                             #Updates and draws the animals tokens
        tokens.draw(display)

        bank_caption.write_counter(display, "Bank")                 #These next 5 captions specify which zone belongs to which player
        player1_caption.write_counter(display, "Farm I")
        player2_caption.write_counter(display, "Farm II")
        if number_of_players > 2:
            player3_caption.write_counter(display, "Farm III")
            if number_of_players > 3:
                player4_caption.write_counter(display, "Farm IV")

        for i in range(number_of_players+1):                        #This loop draws animal counters for each player
            for j in range(7):
                players_counters[i][j].write_counter(display, list_of_players[i].farm[j])

        turn_background.draw_button(display)                        #Draws background for the turn counter   
        turn_text.write_counter(display, "Player "+str(active_turn+1)+" turn")  #Draws the turn counter

        has_won = score_check(active_player)                        #Checks if the active player has won the game. For reference see the line 103

    elif curr_screen == 2:                                          #Displays items on pause screen
        display.fill("green")

        resume_button.draw_button(display)                          #Resume button
        back_to_menu_button.draw_button(display)                    #Back to main menu button

    elif curr_screen == 3:                                          #Displays items on the rules screen
        display.fill("green")
        display.blit(rules, (rules_screen.width/2 - 500, 100))      #Rules are displayed as an image due to pygame's inability for multi-line text displaying
        back_button.draw_button(display)                            #Back to main menu button

    elif curr_screen == 4:                                          #Displays items on the bartering screen
        display.fill((0, 200, 0))                              
        next_player_button.draw_button(display)                     #Next player button
        prev_player_button.draw_button(display)                     #Previous player button
        id_button.draw_button(display)                              #Background for displaying the bartering partner's name
        back_button.draw_button(display)                            #Back to the game screen
        display.blit(rates, (barter_screen.width/2 - 110, barter_screen.height/2 - 110))    #Displays the bartering partner's name
        accept_button.draw_button(display)                          #Make an offer button
        if barter_ind != 0:                                         #If the offer recipient is not the bank, displays prompt and button for accepting the offer
            recip_accept_button.draw_button(display)                
            accept_text.write_counter(display, "Do you accept?")

        
        barter_tokens.draw(display)                                 #Displays the animals tokens for the bartering screen

        for k in range(7):                                          #This loop draws buttons for increasing and decreasing bartering inventory numbers
            less_buttons1[k].draw_button(display)
            less_buttons2[k].draw_button(display)
            more_buttons1[k].draw_button(display)
            more_buttons2[k].draw_button(display)
            barter_counters1[k].write_counter(display, str(barter_players_inv[turn+1][k])+"/"+str(active_player.farm[k]))   #as well as displaying the bartering inventory values in reference to offering or receiving player's farm
            if barter_ind < turn+1:
                barter_counters2[k].write_counter(display, str(barter_players_inv[barter_ind][k])+"/"+str(list_of_players[barter_ind].farm[k]))
            else:
                barter_counters2[k].write_counter(display, str(barter_players_inv[barter_ind+1][k])+"/"+str(list_of_players[barter_ind+1].farm[k]))

    elif curr_screen == 5:                                          #Displays items for the scoreboard screen
        display.fill((0, 200, 0))

        back_to_menu_button.draw_button(display)                    #Back to main menu button
        scoreboard_text.write_counter(display, "Scoreboard")        #Scoreboard captions

        score1.write_counter(display,"1. Player "+str(scoreboard[0]))   #2 places for 2 players
        score2.write_counter(display,"2. Player "+str(scoreboard[1]))
        if number_of_players > 2:
            score3.write_counter(display,"3. Player "+str(scoreboard[2]))   #3 for 3 and so on
            if number_of_players > 3:
                score4.write_counter(display,"4. Player "+str(scoreboard[3]))
        
    pygame.display.flip()                                           #This function updates the screen

    clock.tick(60)                                                  #This function sets the fps to 60

    pressed_last_state = pygame.mouse.get_pressed()[0]              #Reads LPM pressed state
    anim_counter += 1                                               #Increases and resets animation counter
    if anim_counter > 60:
        anim_counter = 0

pygame.quit()