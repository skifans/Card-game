#this code is designed to be used in python 3.2 with the pygame addon.
import pygame, time, sys, ctypes, os
from pygame.locals import *
import random

#set size of window
WINDOWWIDTH = 800
WINDOWHEIGHT = 800

#set colours
#             R    G    B
BLACK     = (  0,   0,   0)
DARKPINK  = (255,  20, 147)
GREEN     = (  0, 255,   0)
WHITE     = (255, 255, 255)
DARKGREEN = (  0, 155,   0)
GREY      = (211, 211, 211)
Red       = (255,   0,   0)
BGCOLOR = WHITE

#set up display
pygame.display.init()
global wn, BASICFONT
pygame.init()
wn = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) #set the width of the window
BASICFONT = pygame.font.SysFont('ActionIsShaded', 24) #set font to be used
pygame.display.set_caption('Card Fighter')
screen=pygame.display.set_mode((0,0))
mainDeck = []

def cont():
    global contvar, action
    contvar=0
    return contvar

def terminate():
    #code which closes the windows after the game is over
    #time.sleep(2)
    pygame.quit()
    sys.exit()

def drawGrid():
    global vertline
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines inbetween cells.
        pygame.draw.line(wn, WHITE, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines inbetween cells.
        vertline = pygame.draw.line(wn, WHITE, (0, y), (WINDOWWIDTH, y))
    pygame.display.update()

#draws grid after key press
wn.fill(BGCOLOR)

#-----------------------------------------------------------------------------------------------------------------------------------------------
#funtion to display text/buttons
def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour) #extact purpose unkown but seems to be needed
    return textSurface, textSurface.get_rect()

def message_display(text, x, y, font_size, colour):
    largeText = pygame.font.Font('freesansbold.ttf',font_size) #load font
    TextSurf, TextRect = text_objects(text, largeText, colour) #render text
    TextRect.center = ((x),(y)) #place text
    #screen=pygame.display.set_mode((0,0)) uncomenting this lets fixes the screen not defined bug - but also causes problems displaying text if let uncommented.
    screen.blit(TextSurf, TextRect) #send to screen, needs to be updated/fliped to be worked

#function for buttoms
#example syntax to call button("return",150,450,100,50,DARKGREEN,GREEN,BLACK,action,"") note the lack of brackets on action function. For no argument use "", otherwise type it.
def txt_button(msg,x,y,w,h,inactive_colour,active_colour,text_colour,name_of_function_to_call_when_clicked, argument):
    #need pygame.flip/update outside of function
    click = pygame.mouse.get_pressed() #get mouse state (clicked/not clicked)
    mouse = pygame.mouse.get_pos() #get mouse coords
    if x+w > mouse[0] > x and y+h > mouse[1] > y: #check if mouse is on button
        pygame.draw.rect(screen, active_colour,(x,y,w,h)) #change to active colour
        if click[0] == 1: #check click (above if checks mouse is on button)
            if argument=="":
                name_of_function_to_call_when_clicked() #do this when clicked (veriable needs not to have brackets)
            else:
                name_of_function_to_call_when_clicked(argument) #do this when clicked (veriable needs not to have brackets)
    else:
        pygame.draw.rect(screen, inactive_colour,(x,y,w,h)) #mouse not on button, switch to inactive colour

    smallText = pygame.font.SysFont("freesansbold.ttf", 30) #load font
    textSurf, textRect = text_objects(msg, smallText,text_colour) #place text in button through text funtion
    textRect.center = ( (x+(w/2)), (y+(h/2)) ) #location of text
    screen.blit(textSurf, textRect) #send to screen (but not update)

def img_button(x,y,w,h,name_of_function_to_call_when_clicked,filename):
    #need pygame.flip/update outside of function
    click = pygame.mouse.get_pressed() #get mouse state (clicked/not clicked)
    mouse = pygame.mouse.get_pos() #get mouse coords
    image = pygame.image.load(os.path.join("cards",filename))
    screen.blit(image, (x,y)) #the location of the image
    if x+w > mouse[0] > x and y+h > mouse[1] > y: #check if mouse is on button
        print("on card "+str(filename))
        if click[0] == 1: #check click (above if checks mouse is on button)
            name_of_function_to_call_when_clicked() #do this when clicked (veriable needs not to have brackets)

def set_cards(): #set up the cards function
    global cards, card_list
    cards = {}
#   cards['Name of card'] = name, health modifer, amour modifer, weapon modifer, duribility, card type
#   card types
#   0:  Heal
#   1:  Weapon
#   2:  Amour
#   3:  card type
    cards['0001'] = ['Iron Kettle',0,0,2,10,2]
    cards['0002'] = ['Sting',-1,0,1,10,1]
    cards['0003'] = ['Lambas Bread',5,0,0,1,0]

    card_list = [] #list of all card names
    for card_name in cards:
        card_list.append(card_name) #add card names to list

def menuFunction():
    global menu
    wn.fill(BGCOLOR)
    menu=1 #loop reacuent
    while menu==1:
        for event in pygame.event.get():
            txt_button("Single player",150,50,200,50,GREEN,DARKGREEN,BLACK,single, "") #make singplayer button
            txt_button("Muilti player",450,50,200,50,GREEN,DARKGREEN,BLACK,muilti, "") #make muiltiplayer button
            txt_button("Close",300,150,200,50,GREEN,DARKGREEN,BLACK,terminate, "") #make close button
            txt_button("Deck Builder", 300,250,200, 50,GREEN,DARKGREEN,BLACK, deckBuilderScreen, "") #make deck Builder screen button
            txt_button("Keyboard test", 300, 350, 200, 50, GREEN, DARKGREEN, BLACK, keyboard_example, "")
            pygame.display.flip() #update pygame
        time.sleep(0.1)

def single(): #single player function
    global menu
    menu=0
    turn_1()

def keyboard_example():
    b=keyboard(1, 2, "test input") #1=< charectors needed, 2=letters and numbers
    print(b)

def addletter(letter):
    global string
    string=string+letter #adds letter from argument to all the others
    print(string)
    pass

def keyboard(minlength, InputOn1, message):
    global string, InputOn
    InputOn=InputOn1
    string=""
    while InputOn!=0:
        for event in pygame.event.get():
            wn.fill(BGCOLOR)
            message_display(string,400.5,150,16,BLACK)
            message_display(message,400,100,16,BLACK)
            if event.type==KEYDOWN:
                key = pygame.key.get_pressed() #get key pressed
                if key[pygame.K_a]:
                    addletter("A")
                elif key[pygame.K_b]:
                    addletter("B")
                elif key[pygame.K_c]:
                    addletter("C")
                elif key[pygame.K_d]:
                    addletter("D")
                elif key[pygame.K_e]:
                    addletter("E")
                elif key[pygame.K_f]:
                    addletter("F")
                elif key[pygame.K_g]:
                    addletter("G")
                elif key[pygame.K_h]:
                    addletter("H")
                elif key[pygame.K_i]:
                    addletter("I")
                elif key[pygame.K_j]:
                    addletter("J")
                elif key[pygame.K_k]:
                    addletter("K")
                elif key[pygame.K_l]:
                    addletter("L")
                elif key[pygame.K_m]:
                    addletter("M")
                elif key[pygame.K_n]:
                    addletter("N")
                elif key[pygame.K_o]:
                    addletter("O")
                elif key[pygame.K_p]:
                    addletter("P")
                elif key[pygame.K_q]:
                    addletter("Q")
                elif key[pygame.K_r]:
                    addletter("R")
                elif key[pygame.K_s]:
                    addletter("S")
                elif key[pygame.K_t]:
                    addletter("T")
                elif key[pygame.K_u]:
                    addletter("U")
                elif key[pygame.K_v]:
                    addletter("V")
                elif key[pygame.K_w]:
                    addletter("W")
                elif key[pygame.K_x]:
                    addletter("X")
                elif key[pygame.K_y]:
                    addletter("Y")
                elif key[pygame.K_z]:
                    addletter("Z")
                elif key[pygame.K_CLEAR]:
                    if len(string)>0: #make sure there is something to clear/delete from/send off
                        clear()
                elif key[pygame.K_BACKSPACE]:
                    if len(string)>0:
                        backspace()
                elif key[pygame.K_RETURN]:
                    if len(string)>0:
                        closeinput(string)

                if InputOn==2:
                    if key[pygame.K_0]:
                        addletter("0")
                    elif key[pygame.K_1]:
                        addletter("1")
                    elif key[pygame.K_2]:
                        addletter("2")
                    elif key[pygame.K_3]:
                        addletter("3")
                    elif key[pygame.K_4]:
                        addletter("4")
                    elif key[pygame.K_5]:
                        addletter("5")
                    elif key[pygame.K_6]:
                        addletter("6")
                    elif key[pygame.K_7]:
                        addletter("7")
                    elif key[pygame.K_8]:
                        addletter("8")
                    elif key[pygame.K_9]:
                        addletter("9")
            else:
                txt_button('A',213.5,200,30,30,WHITE,GREY,BLACK,addletter, "A") #have a button with a letter, which calls a function with the argument of that letter.
                txt_button('B',244.5,200,30,30,WHITE,GREY,BLACK,addletter, "B")
                txt_button('C',275.5,200,30,30,WHITE,GREY,BLACK,addletter, "C")
                txt_button('D',306.5,200,30,30,WHITE,GREY,BLACK,addletter, "D")
                txt_button('E',337.5,200,30,30,WHITE,GREY,BLACK,addletter, "E")
                txt_button('F',368.5,200,30,30,WHITE,GREY,BLACK,addletter, "F")
                txt_button('G',399.5,200,30,30,WHITE,GREY,BLACK,addletter, "G")
                txt_button('H',430.5,200,30,30,WHITE,GREY,BLACK,addletter, "H")
                txt_button('I',461.5,200,30,30,WHITE,GREY,BLACK,addletter, "I")
                txt_button('J',492.5,200,30,30,WHITE,GREY,BLACK,addletter, "J")
                txt_button('K',523.5,200,30,30,WHITE,GREY,BLACK,addletter, "K")
                txt_button('L',554.5,200,30,30,WHITE,GREY,BLACK,addletter, "L")
                txt_button('M',585.5,200,30,30,WHITE,GREY,BLACK,addletter, "M")

                txt_button('N',213.5,230,30,30,WHITE,GREY,BLACK,addletter, "N")
                txt_button('O',244.5,230,30,30,WHITE,GREY,BLACK,addletter, "O")
                txt_button('P',275.5,230,30,30,WHITE,GREY,BLACK,addletter, "P")
                txt_button('Q',306.5,230,30,30,WHITE,GREY,BLACK,addletter, "Q")
                txt_button('R',337.5,230,30,30,WHITE,GREY,BLACK,addletter, "R")
                txt_button('S',368.5,230,30,30,WHITE,GREY,BLACK,addletter, "S")
                txt_button('T',399.5,230,30,30,WHITE,GREY,BLACK,addletter, "T")
                txt_button('U',430.5,230,30,30,WHITE,GREY,BLACK,addletter, "U")
                txt_button('V',461.5,230,30,30,WHITE,GREY,BLACK,addletter, "V")
                txt_button('W',492.5,230,30,30,WHITE,GREY,BLACK,addletter, "W")
                txt_button('X',523.5,230,30,30,WHITE,GREY,BLACK,addletter, "X")
                txt_button('Y',554.5,230,30,30,WHITE,GREY,BLACK,addletter, "Y")
                txt_button('Z',585.5,230,30,30,WHITE,GREY,BLACK,addletter, "Z")
                if len(string)>minlength-1: #make sure that at least one letter has been entered (0 letters was also causing a crash)
                    txt_button('Finished',213.5,260,402,30,WHITE,GREY,BLACK,closeinput, string) #calls close input function
                else:
                    message_display("You need to enter "+str(minlength)+" or more charectors",399.5,275,16,BLACK)
                if len(string)>0:
                    txt_button('Clear',213.5,320,201,30,WHITE,GREY,BLACK,clear, "")
                    txt_button('Backspace',404.5,320,201,30,WHITE,GREY,BLACK,backspace, "")


                if InputOn==2:
                    txt_button('0',213.5,170,30,30,WHITE,GREY,BLACK,addletter, "0") #have a button with a letter, which calls a function with the argument of that letter.
                    txt_button('1',244.5,170,30,30,WHITE,GREY,BLACK,addletter, "1")
                    txt_button('2',275.5,170,30,30,WHITE,GREY,BLACK,addletter, "2")
                    txt_button('3',306.5,170,30,30,WHITE,GREY,BLACK,addletter, "3")
                    txt_button('4',337.5,170,30,30,WHITE,GREY,BLACK,addletter, "4")
                    txt_button('5',368.5,170,30,30,WHITE,GREY,BLACK,addletter, "5")
                    txt_button('6',399.5,170,30,30,WHITE,GREY,BLACK,addletter, "6")
                    txt_button('7',430.5,170,30,30,WHITE,GREY,BLACK,addletter, "7")
                    txt_button('8',461.5,170,30,30,WHITE,GREY,BLACK,addletter, "8")
                    txt_button('9',492.5,170,30,30,WHITE,GREY,BLACK,addletter, "9")
                pygame.display.flip()
    wn.fill(BGCOLOR)
    pygame.display.flip()
    return string

def clear():
    global string
    string=""

def backspace():
    global string
    string=string[:-1]

def closeinput(string):
    global InputOn
    InputOn=0 #loop controlling buttons will not run
    pass

def muilti(): #muiltiplayer function
    global menu, wn
    menu = 0 #stops the menu screen
    wn.fill(BGCOLOR)
    pygame.display.flip()
    global first
    first = True #first turn is true

    def set_enemy(): #set up enemy player
        global ehealth, eamour, eweapons, ename, edeck, ehand, eamourm, eweaponsm, edurability
        ehealth = 20 #there health
        eamour = 5 #there amour
        eamourm = 0 #there amour mod
        eweapons = 1 #there weapons
        eweaponsm = 0 #there weapons mod
        edurability = 0 #there durability
        ename = keyboard(1,2, "enter the name of palyer 2") #there name
        edeck = []
        for i in range(20): #20 card deck
            card = random.choice(card_list) #get random card from cardlist
            edeck.append(cards[card]) #add that card to there deck
        ehand = []
        for i in range(5): #5 card hand
            card = random.choice(edeck) #get random card from deck
            edeck.remove(card) #remove this card from deck
            ehand.append(card) #add this card to hand


    def set_player():
        global health, amour, weapons, name, deck, hand, weaponsm, amourm, durability
        health = 20 #there health
        amour = 5 #there amour
        amourm = 0 #there amour mod
        weapons = 1 #there weapons
        weaponsm = 0 #there weaponsm
        durability = 0 #there durability

        name=keyboard(0, 2, "name of palyer 1")

        #txt_button('A',50,200,40,40,GREY,GREEN,BLACK,ignore)
        #pygame.display.flip()


        ##name = str(input("What is the name of your champion player1: ")) #there name

        text = 'Health: ' + str(health)
        message_display(text,50,25,15,BLACK)
        text = 'Armour: ' + str(amour+amourm)
        message_display(text,50,40,15,BLACK)
        text = 'Weapons: ' + str(weapons+weaponsm)
        message_display(text,50,55,15,BLACK)
        pygame.display.flip()

        deck = []
        for i in range(20): #20 card deck
            card = random.choice(card_list) #get random card from cardlist
            deck.append(cards[card]) #add that card to there deck
        hand = []
        for i in range(5): #5 card hand
            card = random.choice(deck) #get random card from deck
            deck.remove(card) #remove this card from deck
            hand.append(card) #add this card to hand

    def end():
        global turn, contvar
        contvar=0
        turn=False
        return turn, contvar

    def attack():
        global weaponsm, ehealth, durability, contvar
        damage = (weapons + weaponsm)/(eamour + eamourm) #damage is weapons total agaisnt eamout total
        if damage <= 0: #stops them doing negative damge
            print("You do no damage.")
        else:
            ehealth -= damage #takes of damge dealt
            print("You do " + str(damage) + " damage.")
        durability -= 1 #lowers weapons durability
        if durability == 0:
            print("You weapon broke") #says if weapon broke
            weaponsm = 0 #reset weapon mod
        turn = False #end turn
        contvar=2

    def turn():
        global health, amour, weapons, name, deck, hand, ehealth, eamour, eweapons, ename, edeck, ehand, first, amourm, weaponsm, eamourm, ewaponsm, durability, edurability, deck, hand, contvar, turn
        if first == True: #if first time run say who fighting who.
            print("Champion " + name + " you are fighting champion " + ename + ".")
            first == False #make it so its no longer first time run
    #   players turn
        print("Player1's turn") #say whos turn it is
        print("Your hand is:")
        for card in hand:
            print(card[0]) #say what cards are in hand
        print("\nYour stats are:")
        print("Health: " + str(health)) #say what there health is
        print("Amour: " + str(amour)) #say what there amour is
        print("weapons " + str(weapons)) #say what there weapons are
        turn = True
        contvar=1
        while contvar!=0:
            for event in pygame.event.get():
                text = 'Health: ' + str(health)
                message_display(text,50,25,15,BLACK)
                text = 'Armour: ' + str(amour+amourm)
                message_display(text,50,40,15,BLACK)
                text = 'Weapons: ' + str(weapons+weaponsm)
                message_display(text,50,55,15,BLACK)
                if contvar!=2:
                    txt_button("Attack",100,100,100,20,GREEN,DARKGREEN,BLACK,attack,"")
                else:
                    txt_button("Attack",100,100,100,20,DARKGREEN,DARKGREEN,BLACK,attack,"")
                txt_button("End",200,100,100,20,GREEN,DARKGREEN,BLACK,end,"")
                pygame.display.flip()
            time.sleep(0.2)
##            else: #dont realy inderstant what this did/is far. Was as an else on when the user enterd a word not understood on the old keyboard.
##                for card in hand: #get all cards from hand
##                    if action == card[0]: #see if action is one
##                        hand.remove(card) #remove the card from hand
##                        action = None #change action to stop it removeing reacorsense
##                        health += card[1] #apply health
##                        amourm = card[2] #apply amourm
##                        weaponsm = card[3] #apply weaponsm
##                        durability = card[4] #apply durability
        if len(deck) == 0: #see if any deck is left
            print("You have no deck left")
        else:
            hand.append(deck[0]) #add the first in deck to hand
            deck.remove(deck[0]) #remove the first item in deck
    #   computers turn

    set_cards() #run set up cards
    set_player() #run set up player1
    set_enemy() #run set up player2
    turn() #run the turn loop

def turn_1():
    global wn, turn
    wn.fill(BGCOLOR)
    pygame.display.flip()
    ctypes.windll.user32.MessageBoxW(0, "Player 1, take turn?", "Continue", 0)
    hand1=[1,2,3,4]
    turn=1
    while turn==1:
        for event in pygame.event.get():
            for i in range (len(hand1)):
                txt_button("Close",300,100,200,50,GREEN,DARKGREEN,BLACK,terminate,"")
                img_button((i*150)+100,600,150,200,terminate,str(i+1)+".jpg")
        pygame.display.flip()
        time.sleep(0.2)

def whenClicked():
    return "clicked"

#Deck Builder Check Run Code:
set_cards()

def deckBuilderScreen():
    choice = False
    deckBuilder = True
    wn.fill(DARKPINK)
    message_display("Pick your cards from classes below: 20 Cards in Total", 450, 150, 20, GREEN)
    #Set up template so that position, description etc. can be easily modified no matter the card
    #[X, Y, WIDTH, HEIGHT]
    cardAttributes = ["Name:", "Health Modifier:", "Armour Modifer:", "Weapon Modifer:", "Durability:", "Card Type:"]
    cardOneTemplate = [300, 400, 150, 200]
    while deckBuilder == True:
        for event in pygame.event.get():
            txt_button("Return", 200, 200, 75, 75, GREEN, DARKGREEN, BLACK, menuFunction, "")
            txt_button("Exit", 600, 200, 75, 75, GREEN, DARKGREEN, BLACK, terminate, "")
            img_button(cardOneTemplate[0], cardOneTemplate[1], cardOneTemplate[2], cardOneTemplate[3], cardSelect, "1.jpg")
            #Description Layout
            cardAttributeY = cardOneTemplate[1] + 250
            attributeY = cardOneTemplate[1] + 250
            for i in (cardAttributes):
                message_display(i, cardOneTemplate[0]+50, attributeY, 20, BLACK)
                attributeY += 20
            for i in range(0,(len(cardAttributes))):
                message_display(str(cards["0001"][i]), cardOneTemplate[0]+ 150, cardAttributeY,20, GREEN)
                cardAttributeY += 20
            pygame.display.flip()

def cardSelect(cardFile):
    if checkDeck() == True:
        mainDeck.append(cardFile)
    else:
        message_display("WARNING DECK ALREADY AT MAX CAPACITY", 450, 450, 50, RED)
        time.sleep(2)

    print(mainDeck)
    return mainDeck

def checkDeck():
    cardCount=0
    for i in mainDeck:
        cardCount+=1
    if cardCount>= 20:
        return False
    else:
        return True

menuFunction()
terminate()
