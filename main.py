# importing classes needed for the program 
from tkinter import Tk, Canvas, PhotoImage, Entry, Button, END, INSERT, Frame, messagebox, Label
from card import Card
from deck import DeckofCards

#function that will close the window when user clicks the x button in the corner or the exit button on the screen 
def close_window():
    answer = messagebox.askyesno('Baccarat', 'Are you sure you want to exit?')
    if answer == True:
        messagebox.showinfo('Baccarat', 'Thank you for playing Baccarat!')
        exit()

#function that will check the entry widget to ensure the correct information is passed: only integers
def checkentry(val, val1):
    #if a digit is entered it is accepted 
    if val.isdigit():
        entryBet.config(bg='white')
        if val1 == '' or int(val1) > 0:
            entryBet.config(bg='white')
            return True
        #if the value entered is less than a dollar an error message will appear and the widget will turn red
        else:
            messagebox.showerror('Error', 'You must bet at least $1')
            entryBet.config(bg='red')        
            entryBet.focus()
            return False
    # If a non numeric digit is entered an error will appear and the widget will turn red
    else:
        messagebox.showerror('Error', 'You must enter an integer!')
        entryBet.config(bg='red')        
        entryBet.focus()
        return False    

def place_bet():
    global playercard1, playercard2, playercard3, bankercard1, bankercard2, bankercard3
    #Seting every card to their inital back faced image
    playercard1 = Card()
    lblp1.config(image=playercard1.getImage())
    playercard2 = Card()
    lblp2.config(image=playercard2.getImage())
    playercard3 = Card()
    lblp3.config(image=playercard3.getImage())
    bankercard1 = Card()
    lblb1.config(image=bankercard1.getImage())
    bankercard2 = Card()
    lblb2.config(image=bankercard2.getImage())
    bankercard3 = Card()
    lblb3.config(image=bankercard3.getImage())
    canvas.itemconfig(outputPlayer, text='0')
    canvas.itemconfig(outputBanker, text='0')
    #If there is nothing in the entry widget an error will show up and the widget will turn red
    if entryBet.get() == '':
        entryBet.config(bg='red')
        messagebox.showerror('Error', 'Please Enter a value')
        return False
    #If the value entered is greater than their chiptotal an error will show up and the widget will turn red =
    elif int(entryBet.get()) > chiptotal:
        entryBet.config(bg='red')
        messagebox.showerror('Error', f'Your bet cannot exceed ${chiptotal}')
        return False
    #If the entry widget satisfies all requirements: the entry widget and bet widget will be disabled - the deal widget will become active - a message will appear at the bottom for the user to click the deal button
    else:
        entryBet.config(bg='white', state='disabled')
        btnBet.config(state='disabled')
        btnDeal.config(state='normal')
        canvas.itemconfig(outputMessage, text='Click DEAL!')

#function for when the user clicks the deal button
def deal(): 
    #globalizing variables that will be changed
    global playercards, bankercards, playerval, bankerval, chiptotal, playercard1, playercard2, playercard3, bankercard1, bankercard2, bankercard3
    #If the button says draw card instead of deal it will be sent to the draw_card function
    if btnDeal.cget('text') == 'DRAW CARD':
        draw_card()
    #Otherwise it will continue with this function
    else:
        #Dealing the first player card the first card from the deck - the image is retrieved and displayed as the card image
        playercard1 = playerdeck.dealCard()
        lblp1.config(image=playercard1.getImage())
        #Getting the value of the first player card and then insuring that if the card is a 10, Jack, Queen or King its value would be 0 and if it is an Ace it will be valued at a 1
        p1 = playercard1.getValue()
        if p1 == 10 or p1 == 11 or p1 == 12 or p1 == 13:
            p1 = 0
        elif p1 == 14:
            p1 = 1
        #Once the value is retrieved the number will be added to a list for playercards
        playercards.append(p1)
        #The process from above repeats except with the second player card
        playercard2 = playerdeck.dealCard()
        lblp2.config(image=playercard2.getImage())
        p2 = playercard2.getValue()
        if p2 == 10 or p2 == 11 or p2 == 12 or p2 == 13:
            p2 = 0
        elif p2 == 14:
            p2 = 1
        playercards.append(p2)
        #After both cards are added to the list - the cards will be added and checked to see if they can be divisible by 10 - that number will be the players value
        for x in playercards:
            playerval += x
        playerval = playerval % 10
        if playerval > 9:
            playerval = 0
        #The players value is getting outputted
        canvas.itemconfig(outputPlayer, text=f'{playerval}')

        #The same thing is done for the banker like the player 
        #Dealing the first banker card the first card from their deck - the image is retrieved and dispalyed as the card image
        bankercard1 = bankerdeck.dealCard()
        lblb1.config(image=bankercard1.getImage())
        #Getting the value of the first banker card and then insuring that if the card is a 10, Jack, Queen or King its value would be 0 and if it is an Ace it will be valued at a 1
        b1 = bankercard1.getValue()
        if b1 == 10 or b1 == 11 or b1 == 12 or b1 == 13:
            b1 = 0
        elif b1 == 14:
            b1 = 1
        #Once the value is retrieved the number will be added to a list for bankercards
        bankercards.append(b1)
        #The process from above repeats except with the second banker card
        bankercard2 = bankerdeck.dealCard()
        lblb2.config(image=bankercard2.getImage())
        b2 = bankercard2.getValue()
        if b2 == 10 or b2 == 11 or b2 == 12 or b2 == 13:
            b2 = 0
        elif b2 == 14:
            b2 = 1
        bankercards.append(b2)
        #After both cards are added to the list - the cards will be added and checked to see if they can be divisible by 10 - that number will be the bankers value
        for x in bankercards:
            bankerval += x
        bankerval = bankerval % 10
        if bankerval > 9:
            bankerval = 0
        #The bankers value is getting outputted
        canvas.itemconfig(outputBanker, text=f'{bankerval}')

        #Now the players value and the bankers value will be compared if either the player or banker get 8 or 9 an automatic winner is determined
        if playerval == 9 or playerval == 8 or bankerval == 8 or bankerval == 9:
            revert()
        #If the players value is less than or equal to 5 another card will have to be drawn the button label will change and a new output message will appear
        elif playerval <= 5:
            btnDeal.config(text='DRAW CARD')
            canvas.itemconfig(outputMessage, text='Draw one more card!')
        #If the players value is 6 or 7 the player doesn't get another card, however, if the banker gets a value under 5 when this happens another cad has to be drawn, therefore, the button label will change and a new output message will appear
        elif playerval == 6 or playerval == 7 and bankerval <=5:
                btnDeal.config(text='DRAW CARD')
                canvas.itemconfig(outputMessage, text='Draw one more card!')
        #If the bankrs value is not less than 5 another card cannot be drawn and an automatic winner will once again be determined
        else:
            revert()

#Function used to restart the round, output the winner and check if the user has enough money to continue
def revert():
    global playerval, bankerval, playerdeck, bankerdeck, playercards, bankercards, chiptotal
    #First a winner is determined
    #If the players total is greater than the bankers they will the money they bet will be added to the current amount of money they have and the message box will state the player wins
    if playerval > bankerval:
        chiptotal += int(entryBet.get())
        canvas.itemconfig(outputChips, text=f'${chiptotal:,d}')
        canvas.itemconfig(outputMessage, text='Player wins!')
    #If the players total is less than the bankers they will the money they bet will be subtracted to the current amount of money they have and the message box will state the banker wins
    elif playerval < bankerval:
        chiptotal -= int(entryBet.get())
        canvas.itemconfig(outputChips, text=f'${chiptotal:,d}')
        canvas.itemconfig(outputMessage, text='Banker wins!')
    #If there is a tie there will be no money change the message box will state there was a tie
    elif playerval == bankerval:
        canvas.itemconfig(outputMessage, text='Tie!')
    #Checking to see if the chiptotal is 0 if it is the user has lost and will be asked if they would like to play again - if they say yes the game will restart - no will cause the game to close
    if chiptotal == 0:
        replay = messagebox.askyesno('Baccarat', 'Game over! You have $0 remaining.\nWould you like to play again?')
        if replay == True:
            restart()
        else:
            messagebox.showinfo('Baccarat', 'Thank you for playing Baccarat!')
            exit()
    #The rest of these functions are to reset the interface to how it was before - except for the cards - players will want to see cards from the previous round to see how they won or lost once their bets are in and they have redrawn a card new images will appear and the 3rd card will flip back
    entryBet.config(state='normal')
    entryBet.focus()
    btnBet.config(state='normal')
    btnDeal.config(state='disabled', text='DEAL')
    lblp1.config(image=playercard1.getImage())
    lblp2.config(image=playercard2.getImage())
    lblp3.config(image=playercard3.getImage())
    #The player gets a new set of cards and it will be reshuffled
    playerdeck = DeckofCards(True)
    playercards = []
    playerval = 0
    lblb1.config(image=bankercard1.getImage())
    lblb2.config(image=bankercard2.getImage())
    lblb3.config(image=bankercard3.getImage())
    #The banker gets a new set of cards and it will be reshuffled
    bankerdeck = DeckofCards(True)
    bankercards = []
    bankerval = 0

#If another card has to be drawn a call will be made to this function - it will check for what cases another banker card has to be drawn
def draw_card():
    global playerval, bankerval, playercard3, bankercard3, chiptotal, playercards, bankercards
    #When the player value is less than 5 a new card has to be drawn
    if playerval <= 5:
        #The next card from the deck is given - image and value are retrieved - image is outputted values are determined based on number and restrictions - the card is then added to the player card list 
        playercard3 = playerdeck.dealCard()
        lblp3.config(image=playercard3.getImage())
        p3 = playercard3.getValue()
        if p3 == 10 or p3 == 11 or p3 == 12 or p3 == 13:
            p3 = 0
        elif p3 == 14:
            p3 = 1
        playercards.append(p3)
        #The player total will then add this value to the current total and check its divisiblity by 10 - that will be the players value - the value will then be outputted onto the canvas
        playerval += p3
        playerval = playerval % 10
        if playerval > 9:
            playerval = 0
        canvas.itemconfig(outputPlayer, text=f'{playerval}')
        #If statements have been made to determine when the banker will draw another card - when they would a function will be called
        #If the banker value is 0, 1 or 2 a call will always be made
        if bankerval == 0 or bankerval == 1 or bankerval == 2:
            draw_banker()
        #If the banker value is a 3 and the playervalue after a card is drawn is not 8
        elif bankerval == 3 and playerval != 8:
            draw_banker()
        #If the banker value is 4 and the player value after a card is drawn is between 2-7
        elif bankerval == 4 and playerval >= 2 and playerval <= 7:
            draw_banker()
        #If the banker value is 5 and the player value after a card is drawn is between 4-7
        elif bankerval == 5 and playerval >= 4 and playerval <= 7:
            draw_banker()
        # If the banker value is 6 and the player value after a card is drawn is either 6 or 7
        elif bankerval == 6 and playerval >= 6 and playerval <= 7:
            draw_banker()
        else:
            revert()
    #If the player value is 6 or 7 the player does not get a card only the banker does if their total is less than 5
    elif playerval == 6 or playerval == 7 and bankerval <= 5:
            draw_banker()
    else:
        revert()

#IF the banker needs to draw a card this function will be called
def draw_banker():
    global playerval, bankerval, playercard3, bankercard3, chiptotal, playercards, bankercards
    #A card will be dealed to the bankers third card - this will be the next card in the deck - the image will be retrieved and outputted
    bankercard3 = bankerdeck.dealCard()
    lblb3.config(image=bankercard3.getImage())
    #The card value will be recieved if it is 10 or has faces it will be 0 and if it is an ace will be made to equal 1
    b3 = bankercard3.getValue()
    if b3 == 10 or b3 == 11 or b3 == 12 or b3 == 13:
        b3 = 0
    elif b3 == 14:
        b3 = 1
    #The card is then added to the list and to the bankers total - it will be checked to see if it can be divisible by 10 - that will be the bankers value
    bankercards.append(b3)
    bankerval +=b3
    bankerval = bankerval % 10
    if bankerval > 9:
        bankerval = 0
    #The bankers value will then be outputted to the screen
    canvas.itemconfig(outputBanker, text=f'{bankerval}')
    #Revert function called to declare winner
    revert()

#IF the user decides they want to play again this function is called
def restart():
    global playercard1, playercard2, playercard3, bankercard1, bankercard2, bankercard3, playerdeck, playercards, playerval, bankerdeck, bankercards, bankerval, chiptotal
    #Everything is reset to it orginal state
    #Cards have been chnaged to their back new decks are given, player and banker totals are 0 and the lists are empty
    playercard1 = Card()
    lblp1.config(image=playercard1.getImage())
    playercard2 = Card()
    lblp2.config(image=playercard2.getImage())
    playercard3 = Card()
    lblp3.config(image=playercard3.getImage())
    playerdeck = DeckofCards(True)
    playercards = []
    playerval = 0
    bankercard1 = Card()
    lblb1.config(image=bankercard1.getImage())
    bankercard2 = Card()
    lblb2.config(image=bankercard2.getImage())
    bankercard3 = Card()
    lblb3.config(image=bankercard3.getImage())
    bankerdeck = DeckofCards(True)
    bankercards = []
    bankerval = 0

    #The chip total reloads to 500 - it is outputted as well as other text that was there when the game began
    chiptotal = 500
    canvas.itemconfig(outputChips, text=f'${chiptotal:,d}')
    canvas.itemconfig(outputPlayer, text='0')
    canvas.itemconfig(outputBanker, text='0')
    canvas.itemconfig(outputMessage, text='Place BET to begin')
    #The buttons are configed to their original state
    entryBet.config(state='normal')
    entryBet.delete(0, END)
    entryBet.focus()
    btnBet.config(state='normal')
    btnDeal.config(state='disabled', text='DEAL')

#Interface made:
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 534

root = Tk()
root.title('Baccarat')
root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{(root.winfo_screenwidth() - WINDOW_WIDTH) // 2}+{(root.winfo_screenheight() - WINDOW_HEIGHT) // 2}')
root.protocol('WM_DELETE_WINDOW', close_window)

canvas = Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

#Player cards are initialized and variables are created
playercard1 = Card()
lblp1 = Label(canvas, image=playercard1.getImage())
lblp1.place(relx=0.313, rely=0.4, anchor='c')
playercard2 = Card()
lblp2 = Label(canvas, image=playercard2.getImage())
lblp2.place(relx=0.313, rely=0.5, anchor='c')
playercard3 = Card()
lblp3 = Label(canvas, image=playercard3.getImage())
lblp3.place(relx=0.313, rely=0.6, anchor='c')
playerdeck = DeckofCards(True)
playercards = []
playerval = 0
#Banker cards are initialized and variables are created
bankercard1 = Card()
lblb1 = Label(canvas, image=bankercard1.getImage())
lblb1.place(relx=0.687, rely=0.4, anchor='c')
bankercard2 = Card()
lblb2 = Label(canvas, image=bankercard2.getImage())
lblb2.place(relx=0.687, rely=0.5, anchor='c')
bankercard3 = Card()
lblb3 = Label(canvas, image=bankercard3.getImage())
lblb3.place(relx=0.687, rely=0.6, anchor='c')
bankerdeck = DeckofCards(True)
bankercards = []
bankerval = 0

imgbackground = PhotoImage(file='images/card_table.png')
canvas.create_image(0, 0, image=imgbackground, anchor='nw')

imgtitle = PhotoImage(file='images/baccarat.png')
canvas.create_image((WINDOW_WIDTH - imgtitle.width()) // 2, 10, image=imgtitle, anchor='nw')

chiptotal = 500
outputChips = canvas.create_text(WINDOW_WIDTH // 2, 160, font=('Century Gothic', 28, 'bold'), fill='white', text=f'${chiptotal:,d}')

canvas.create_text(250, 425, text='Player has:', font=('Century Gothic', 14, 'bold'), fill='white')
canvas.create_text(550, 425, text='Banker has:', font=('Century Gothic', 14, 'bold'), fill='white')

outputMessage = canvas.create_text(WINDOW_WIDTH // 2, 385, text='Place BET to begin', font=('Century Gothic', 12, 'bold'), fill='white')
outputPlayer = canvas.create_text(250, 455, text='0', font=('Century Gothic', 14, 'bold'), fill='white')
outputBanker = canvas.create_text(550, 455, text='0', font=('Century Gothic', 14, 'bold'), fill='white')

frame = Frame(root, borderwidth=2, relief='sunken')

entryBet = Entry(frame, width=12, font=('Century Gothic', 10, 'bold'), justify='center', borderwidth=5, relief='flat', validate='key', validatecommand=(root.register(checkentry), '%S', '%P'))
entryBet.focus()
entryBet.selection_range(0, END)
entryBet.pack()

root.update()
frame.place(x=(WINDOW_WIDTH - frame.winfo_reqwidth()) // 2, y=190)

btnBet = Button(canvas, width=13, text='PLACE BET', pady=5, command=place_bet)
btnBet.place(x=(WINDOW_WIDTH - btnBet.winfo_reqwidth()) // 2, y=235)
btnDeal = Button(canvas, width=13, text='DEAL', pady=5, state='disabled', command=deal)
btnDeal.place(x=(WINDOW_WIDTH - btnDeal.winfo_reqwidth()) // 2, y= 280)
btnQuit = Button(canvas, width=13, text='QUIT', pady=5, command=close_window)
btnQuit.place(x=(WINDOW_WIDTH - btnQuit.winfo_reqwidth()) // 2, y = 325)

root.mainloop()