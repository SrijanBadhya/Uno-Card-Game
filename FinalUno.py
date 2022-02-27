from tkinter import *
from PIL import ImageTk, Image
import random
from tkinter import messagebox
root=Tk()
root.title("Uno card viewer")

deck=['r0','y0','b0','g0']     #Creating deck

for i in range(1,10):
    deck+=['r'+str(i)]*2
    deck+=['y'+str(i)]*2
    deck+=['b'+str(i)]*2
    deck+=['g'+str(i)]*2

deck+=['r+2','y+2','b+2','g+2']*2  #+2
deck+=['rr','yr','br','gr']*2    #Reverse
deck+=['rs','ys','gs','bs']*2    #Skip
deck+=['wi']*4               #Wild
deck+=['w+4']*4                 #+4

random.shuffle(deck)    
leftoverDeck = []

unique=list(set(deck))

cardimages={}
for i in unique:
    cardimages[i]=ImageTk.PhotoImage(Image.open('Unocards/%s.png'%i))

cardimages['wi']=[ImageTk.PhotoImage(Image.open('Unocards/wi.png'))]
cardimages['rw']=[ImageTk.PhotoImage(Image.open('Unocards/rw.png'))]
cardimages['bw']=[ImageTk.PhotoImage(Image.open('Unocards/bw.png'))]
cardimages['gw']=[ImageTk.PhotoImage(Image.open('Unocards/gw.png'))]
cardimages['yw']=[ImageTk.PhotoImage(Image.open('Unocards/yw.png'))]

titleimg=ImageTk.PhotoImage(Image.open("Unocards/UNO.png"))
Label(root,image=titleimg).grid(row=0,column=2)

playerCards={}
noOfPlayers=2

q=1
randlist=[]
def popup():
    global playerNames
    global namecollector
    global playerCards
    global temp
    global q
    namecollector=Toplevel()
    namecollector.title("Second window")
    

    playerNames={}

    Label(namecollector,text="Enter the names:").grid(row=2,column=0)

    ef=Entry(namecollector,width=35)
    ef.grid(row=3,column=0)

    global randlist
    def clickname():
        global playerNames
        global randlist
        randlist.append(ef.get())
        ef.delete(0,END)


    Button(namecollector,text="Submit name of player",command=clickname,pady=5).grid(row=4,column=0)

    Button(namecollector,text="Finish",command=starteverything).grid(row=5,column=0)
    rules=Label(namecollector,text="Uno rules: \n Every player views his/her cards and tries to match top card. \n You have to match either by the number, or color. \n For instance, if the top card is a red card that is an 8 you have to place either a red card or a card with an 8 on it. \n You can also play a Wild card (which can alter current color in play). \n If the player has no matches or they choose not to play any of their cards even though they might have a match, they must draw a card from the Draw pile. \n If that card can be played, play it. Otherwise, keep the card, and the game moves on to the next person in turn. \n You can also play a Wild card, or a Wild Draw Four card on your turn.")
    rules.grid(row=6,column=0)
    

    
temp=Button(root,text="Enter details here",command=popup)
temp.grid(row=1,column=2)

'''
for i in range(1,noOfPlayers+1):
    
    playerNames[i]=input("Enter name of player %d: " %(i))  # player number is key, corresponds to names.
    playerCards[i]=[]         # player number is key, corresponds to empty list for everybody
'''
def starteverything():
    global dir
    dir=1
    global topCard
    temp.destroy()
    namecollector.destroy()
    noOfPlayers=len(randlist)

    for i in range(1,noOfPlayers+1):
        playerNames[i]=randlist[i-1]
        playerCards[i]=[]
    
    print(playerNames)
    
    for player in playerCards: #player is the key, and each corresponding value is a list
        for i in range(5):
            playerCards[player].append(deck.pop())


    print(playerCards)

    topCard=deck.pop(0)
    while topCard[1] in ['r','s','i','+']:
        leftoverDeck.append(topCard)
        topCard=deck.pop(0)


    framedeck=LabelFrame(root,text="Draw a card here",padx=5)
    framedeck.grid(row=1,column=0)
    cover_img=ImageTk.PhotoImage(Image.open("Unocards/cover.png"))


    framecards=LabelFrame(root,text="These are your cards",padx=5)
    framecards.grid(row=2,column=0,columnspan=6)

    framelabel=LabelFrame(root,padx=5)
    framelabel.grid(row=1,column=4)


    '''
    def labeltext(toprint):
        screentext=Label(framelabel,text=toprint,padx=10,pady=10)
        screentext.grid(row=0,column=0)

    def okaybutton(toprint,comand):
        screentext=Button(framelabel,text=toprint,command=comand,padx=10,pady=10)
        screentext.grid(row=1,column=0)
    '''

    def skip(playerturn,additional_cards=0):
        if dir==1:
            if playerturn==noOfPlayers:
                print("Player 1 has been skipped")
                plusbackbone(additional_cards,1)
                loop(2)
            elif playerturn==noOfPlayers-1:
                print("Player %d has been skipped"%(noOfPlayers))
                plusbackbone(additional_cards,noOfPlayers)
                loop(1)
            else:
                print("Player %d has been skipped"%(playerturn+1))
                plusbackbone(additional_cards,playerturn+1)
                loop(playerturn+2)
        elif dir==-1:
            if playerturn==1:
                print("Player %d has been skipped"%(noOfPlayers))
                plusbackbone(additional_cards,noOfPlayers)
                loop(noOfPlayers-1)
            elif playerturn==2:
                print("Player 1 has been skipped")
                plusbackbone(additional_cards,1)
                loop(noOfPlayers)
            else:
                print("Player %d has been skipped"%(playerturn-1))
                plusbackbone(additional_cards,playerturn-1)
                loop(playerturn-2)

    def plustwo(playerturn):
        skip(playerturn,2)

    def plusbackbone(add_cards,victim):
        global deck
        global leftoverDeck

        if len(deck) <= 4:  #When deck is used up, leftover deck is used
            print("Leftover:",leftoverDeck)
            deck = leftoverDeck.copy()
            random.shuffle(deck)
            leftoverDeck = []
            print("Deck used up, leftover deck used")
            print("Deck:",deck)
        
        card1=deck.pop() 
        card2=deck.pop()
        
        if add_cards==2:
            playerCards[victim].extend([card1,card2])

        elif add_cards==4:

            card3=deck.pop()
            card4=deck.pop()
            playerCards[victim].extend([card1,card2,card3,card4])


    def wild(playerturn,speciality):
        global topCard
        global colour
        global TopCardImage

        top=Toplevel()
        top.title("My second window")
        Label(top,text="Choose a color").pack()
        
        def myclick(colour):
            global topCard
            global TopCardImage
            global frametop
            #colour=input("Choose the colour, type r,b,g,y")
            leftoverDeck.append(topCard)
            topCard=colour+"w"
            top.destroy()

            frametop=LabelFrame(root,text="TopCard",padx=5)

            TopCardImage.grid_forget()
            TopCardImage=Label(frametop,image=cardimages[topCard])
            TopCardImage.grid(row=0,column=0)

            frametop.grid(row=1,column=2)


            if speciality==4:
                skip(playerturn,4)

        Button(top, text="Red",command=lambda: myclick("r"), bg="red").pack()
        Button(top, text="Blue",command=lambda: myclick("b"), bg="blue").pack()
        Button(top, text="Green",command=lambda: myclick("g"), bg="green").pack()
        Button(top, text="Yellow",command=lambda: myclick("y"), bg="yellow").pack()

    


    def reverseOrder():
        global dir
        dir*=-1

    def playCard(n,card):
        global topCard
        global TopCardImage
        global framecards
        playerCards[n].remove(card)
        
        frametop=LabelFrame(root,text="TopCard",padx=5)
        frametop.grid(row=1,column=2)
        
        

        if topCard[1]!='w':
            leftoverDeck.append(topCard)

        topCard=card

        TopCardImage.grid_forget()
        TopCardImage=Label(frametop,image=cardimages[topCard])
        TopCardImage.grid(row=0,column=0)

        framecards.destroy()
        

        if len(playerCards[n]) == 0:
            print("The game of Uno has ended!")
            print("Player %s has won!"%(playerNames[n]))
            top=Toplevel()
            top.title("End of Game")
            lbl=Label(top,text="The Game of Uno has ended, Congratulations to the winner "+playerNames[n]).pack()
            btn2=Button(top,text="Close Game",command=root.quit).pack()
            
        


    def checkAndPlay(n,card):
        global framecards
        if card[0]=='w':
            playCard(n,card)
            print("You have successfully played your card ",card)
            if card[1]=='i':
                wild(n,0)
            elif card[1]=='+':
                wild(n,4)

        elif ( card[0]==topCard[0] or card[1]==topCard[1]  ) and card[1] in ["0","1","2","3","4","5","6","7","8","9"]:     #checking both letters of card
            playCard(n,card)
            print("You have successfully played your card ",card)
        
        elif ( card[0]==topCard[0] or card[1]==topCard[1] ) and card[1]=='r':   #Reverse
            playCard(n,card)
            print("You have successfully played your card ",card)
            reverseOrder()

        elif ( card[0]==topCard[0] or card[1]==topCard[1] ) and card[1]=='s':
            playCard(n,card)
            print("You have successfully played your card ",card)
            skip(n)
        
        elif ( card[0]==topCard[0] or card[1]==topCard[1] ) and card[1:]=='+2':
            playCard(n,card)
            print("You have successfully played your card ",card)
            plustwo(n)


        else: 
            print("You can't play that card.")
            messagebox.showwarning("Alert","You can't play that card, choose another")

            playRound(n)

    def draw(forplayer):
        global deck
        global leftoverDeck
        global framecards
        global drawbutton
        
        card=deck.pop()
        playerCards[forplayer].append(card)
        if len(deck) == 1:  #When deck is used up, leftover deck is used
            print("Leftover:",leftoverDeck)
            deck = leftoverDeck.copy()
            random.shuffle(deck)
            leftoverDeck = []
        
        framecards.destroy()
        framecards=LabelFrame(root,text="These are your cards",padx=5)
        framecards.grid(row=2,column=0,columnspan=6)

        def buttoncreator(i,n):
            if i<10:
                Button(framecards,image=cardimages[playerCards[n][i]],padx=5,pady=5,command=lambda: checkAndPlay(n,(playerCards[n][i]))).grid(row=0,column=i)
            elif i<20:
                Button(framecards,image=cardimages[playerCards[n][i]],padx=5,pady=5,command=lambda: checkAndPlay(n,(playerCards[n][i]))).grid(row=1,column=i-10)
            elif i<30:
                Button(framecards,image=cardimages[playerCards[n][i]],padx=5,pady=5,command=lambda: checkAndPlay(n,(playerCards[n][i]))).grid(row=2,column=i-20)
        
        
        def displaycards():
            for ii in range (len(playerCards[forplayer])):
                buttoncreator(ii,forplayer)
        displaycards()
        drawbutton.grid_forget()
        
    
            
            


    def playRound(n):    # n is player number
        global topCard
        global leftoverDeck
        global deck
        global TopCardImage
        global framecards
        global drawbutton
        
        
        screentext=Label(framelabel,text=("It's the turn of Player %s %s"%(str(n),str(playerNames[n]))),padx=10,pady=10)
        screentext.grid(row=0,column=0)

        framecards=LabelFrame(root,text="These are your cards",padx=5)
        framecards.grid(row=2,column=0,columnspan=6)


        def buttoncreator(i,n):
            if i<10:
                Button(framecards,image=cardimages[playerCards[n][i]],padx=5,pady=5,command=lambda: checkAndPlay(n,(playerCards[n][i]))).grid(row=0,column=i)
            elif i<20:
                Button(framecards,image=cardimages[playerCards[n][i]],padx=5,pady=5,command=lambda: checkAndPlay(n,(playerCards[n][i]))).grid(row=1,column=i-10)
            elif i<30:
                Button(framecards,image=cardimages[playerCards[n][i]],padx=5,pady=5,command=lambda: checkAndPlay(n,(playerCards[n][i]))).grid(row=2,column=i-20)
        
        
        def displaycards():
            for ii in range (len(playerCards[n])):
                buttoncreator(ii,n)
                

        screentext2=Button(framelabel,text="Click here to display cards",command=displaycards,padx=10,pady=10)
        screentext2.grid(row=1,column=0)

        drawbutton=Button(framedeck,image=cover_img,command=lambda: draw(n))
        drawbutton.grid(row=0,column=0)

        frametop=LabelFrame(root,text="TopCard",padx=5)
        frametop.grid(row=1,column=2)
        TopCardImage=Label(frametop,image=cardimages[topCard])
        TopCardImage.grid(row=0,column=0)


        def confirmation(r):
            global dir
            global framecards
            framecards.destroy()      
            if dir==1:
                if r==noOfPlayers:
                    loop(1) #execution when we reach the left end
                else: #regular execution
                    loop(r+1)
            elif dir==-1:
                if r==1:
                    loop(noOfPlayers)
                else:
                    loop(r-1)
        screentext3=Button(framelabel,text="Done",command= lambda: confirmation(n))
        screentext3.grid(row=2,column=0)
            
        
    def loop(playerturn):
        global dir 

        playRound(playerturn)
        #print(playerturn)
        #dir=int(input("Enter direction from the end of this turn"))
        
        print("Turn ends\n")
        '''
        if dir==1:
            if playerturn==noOfPlayers:
                loop(1) #execution when we reach the left end
            else: #regular execution
                loop(playerturn+1)
        elif dir==-1:
            if playerturn==1:
                loop(noOfPlayers)
            else:
                loop(playerturn-1)
        '''
    dir=1
    loop(1)
 
root.mainloop()
