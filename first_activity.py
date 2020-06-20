from tkinter import *
import itertools as it
import random
from tkinter import messagebox

class Play:
    def __init__(self,obj):
        self.root=obj.game_board
        self.obj=obj
        self.version=obj.version
        for i in range(5):
            self.root.grid_rowconfigure(i,weight=1)
        for i in range(3):
            self.root.grid_columnconfigure(i,weight=1)

        self.turn=False
        self.flag_turn=False

        self.start()

    def start(self):

        self.player1=[]
        self.player2=[]
        
        self.turn=not self.flag_turn
        self.flag_turn= not self.flag_turn
        
            
        for i in range(3):
            for j in range(3):
                l=Label(self.root,text=' ',height=7,width=23,bg='black',fg='springgreen')
                l.grid(row=i,column=j,sticky='nswe',padx=2,pady=2)

        self.start_b=Button(self.root,text='START',command=self.Make_play_board,
                    fg='black',bg='springgreen',
                     activebackground='mediumspringgreen',activeforeground='black',font=('Arial',30,'bold'),padx=0,pady=0)
        self.start_b.grid(row=3,column=0,sticky='nswe',columnspan=3,padx=2,pady=2)

    def Make_play_board(self):
        self.board=[0,1,2,3,4,5,6,7,8]
        k=0
        self.start_b['state']=DISABLED
        self.start_b['bg']='black'
        self.start_b.grid(row=3,column=1,columnspan=1,pady=2,padx=2)
        
        for i in range(3):
            for j in range(3):
                b=Button(self.root,text=' ',height=7,width=7,bg='black',fg='springgreen',activebackground='mediumspringgreen',
                         activeforeground='black',command=lambda t=(i,j,k):self.place_X_or_O_1(t) if self.version=='Single' else self.place_X_or_O_2(t))
                b.grid(row=i,column=j,sticky='nswe',padx=2,pady=2)
                k+=1
        self.play1=Label(self.root,text=self.obj.player_1 if self.flag_turn else '        ',bg='springgreen',font=('Arial',10,'bold'),padx=0,pady=0,fg='black')
        self.play1.grid(row=3,column=0,sticky='nswe',pady=2,padx=2)
        
        self.play2=Label(self.root,text='        ' if self.flag_turn else self.obj.player_2,bg='springgreen',font=('Arial',10,'bold'),padx=0,pady=0,fg='black')
        self.play2.grid(row=3,column=2,sticky='nswe',pady=2,padx=2)

        if self.version=='Single' and not self.flag_turn:
            if self.turn:self.turn = not self.turn
            self.place_X_or_O_1((None,))
            



    def place_X_or_O_1(self,t):
        turn=self.turn
        if turn:
            l=Label(self.root,text='X',bg='black',fg='springgreen',font=('Comic Sans MS',40),padx=0,pady=0)
            l.grid(row=t[0],column=t[1],sticky='nswe',padx=2,pady=2)
            self.player1.append(t[2])   
            self.play1['text']=''
            self.play2['text']=self.obj.player_2
            self.board[t[2]]='X'

            self.iswin()
            
            self.turn=not(self.turn)

        if not self.turn:
            move=self.Ai_mode()

            
            if move is not None:
                num=0
                for i in range(3):
                    for j in range(3):
                        if num==move:
                            pos=i,j
                        num+=1           
                l=Label(self.root,text='O',bg='black',fg='springgreen',font=('Comic Sans MS',40),padx=0,pady=0)
                l.grid(row=pos[0],column=pos[1],sticky='nswe',padx=2,pady=2)
                self.player2.append(move)
                self.play2['text']=''
                self.play1['text']=self.obj.player_1
                self.board[move]='O'
            
            self.turn=not(self.turn)
        self.iswin()


    def check_for_win(self,l):
        win_combinations=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        perm=list(it.permutations(l,3))
        for i in win_combinations:
            if i in perm:
                return True


    def place_X_or_O_2(self,t):
        turn=self.turn
        l=Label(self.root,text='X' if turn else 'O',bg='black',fg='springgreen',font=('Comic Sans MS',40),padx=0,pady=0)
        l.grid(row=t[0],column=t[1],sticky='nswe',padx=2,pady=2)
        self.player1.append(t[2]) if turn else self.player2.append(t[2])
  
        if turn:
            self.play1['text']=''
            self.play2['text']=self.obj.player_2
            
            
        else:
            self.play2['text']=''
            self.play1['text']=self.obj.player_1
            
            
        self.turn=not(self.turn)
        self.iswin()

        

    def iswin(self):
        if len(self.player1)>2 and self.check_for_win(self.player1):
            messagebox.showinfo('WINNER',self.obj.player_1+' won')
            self.obj.score_update(self.obj.player_1)
            self.start()
        elif len(self.player2)>2 and self.check_for_win(self.player2):
            messagebox.showinfo('WINNER',self.obj.player_2+' won')
            self.obj.score_update(self.obj.player_2)
            self.start()
        elif (len(self.player1)==5 and len(self.player2)==4) or (len(self.player2)==5 and len(self.player1)==4):
            messagebox.showinfo('TIE','TIE')
            self.start()


    def Ai_mode(self):
        possibleMoves = [i for i,ele in enumerate(self.board) if type(ele) is int]
        move=None
        for a in ['O','X']:
            for i in possibleMoves:
                if a=='X':
                    player=self.player1[::]
                else:
                    player=self.player2[::]
                    
                player.append(i)
                
                if self.check_for_win(player):
                    move = i
                    return move
                else:
                    player.pop(-1)

        cornersOpen=[]
        for i in possibleMoves:
            if i in [0,2,6,8]:
                cornersOpen.append(i)
        if len(cornersOpen)>0:
            move=cornersOpen[random.randint(0,len(cornersOpen)-1)]
            return move
        if 4 in possibleMoves:
            move=4
            return move

        edgesOpen=[]
        for i in possibleMoves:
            if i in [0,2,6,8]:
                edgesOpen.append(i)
        if len(edgesOpen)>0:
            move=edgesOpen[random.randint(0,len(edgesOpen)-1)]
            return move


        return move


            




class Interact():
    bgcolor='black'
    fgcolor='springgreen'
    font='arail'
    def __init__(self):
        self.window=Tk()
        self.window.attributes('-fullscreen',1)
        self.window.protocol("WM_DELETE_WINDOW",lambda :self.Popup_info('Exit','We are taking you\n out from this.',1))
        self.window.config(background=bgcolor)
        self.popup=None
        self.window.bind('<Button-1>',self.close_popup)
        self.wn_width,self.wn_height=self.window.maxsize()
        self.name=Label(self.window,text='TIC TAC TOE',font=('candara',71,'bold'),anchor='n',bg=self.bgcolor,
                        fg=self.fgcolor)
        self.name.place(x=(self.wn_width//2-250),y=self.wn_height//16)
        print(self.name.size())
        self.Interact_frame=Frame(self.window,width=500,height=500,bg=self.bgcolor)
        self.Interact_frame.place(x=(self.wn_width//2-250),y=(self.wn_height//2-150))

        self.frame1=Frame(self.Interact_frame,width=500,bg=self.bgcolor,height=70)

        self.single=Button(self.frame1,text='Single-player',bg=self.bgcolor,fg=self.fgcolor,width=20,height=2,
                          font=('arial',16),command=self.single_player)
        self.single.pack(side='left')
        self.multi=Button(self.frame1,text='Multi-player',bg=self.bgcolor,fg=self.fgcolor,width=20,height=2,
                            font=('arial',16),command=self.multi_player)
        self.multi.pack(side='left')
        self.frame1.place(x=0,y=0)
        self.f1=None
        self.f2=None
        label=Label(self.window,text='Exit(Alt+F4)',font=('Arial',15,'bold'),anchor='n',bg=self.bgcolor,
                        fg=self.fgcolor)
        label.place(x=self.wn_width-120,y=0)
        self.player_1_score=0
        self.player_2_score=0
        self.window.mainloop()

    def score_update(self,player):
        if player==self.player_1:
            self.player_1_score+=1
            self.score_player_1['text']=self.player_1[0:9]+': '+str(self.player_1_score)
        else:
            self.player_2_score+=1
            self.score_player_2['text']=self.player_2[0:9]+': '+str(self.player_2_score)
            


    def fxn(self):

        import Animation
        Animation.main(self)

        
        self.game_board=Frame(self.window,width=500,height=500,bg=self.fgcolor)
        self.game_board.place(x=(self.wn_width//2-250),y=(self.wn_height//2-150))
        self.score_player_1=Label(self.window,text=self.player_1[0:9],font=(self.font,15),bg=self.bgcolor,justify='right',
                                  fg=self.fgcolor,width=10)
        self.score_player_1.place(x=(self.wn_width//2-370),y=(self.wn_height//2-150))
        
        self.score_player_2=Label(self.window,text=self.player_2[0:9],font=(self.font,15),bg=self.bgcolor,justify='left',
                                  fg=self.fgcolor,width=10)
        self.score_player_2.place(x=(self.wn_width//2+280),y=(self.wn_height//2-150))

        self.menu=Button(self.window,text="Menu",font=(self.font,15),bg=self.fgcolor,justify='right',
                                  fg=self.bgcolor,width=10,
                         command=self.show_menu)
        self.menu.place(x=(self.wn_width//2-250),y=self.wn_height//2-190)

        self.exit=Button(self.window,text="Exit",font=(self.font,15),bg=self.fgcolor,justify='right',
                                  fg=self.bgcolor,width=10,
                         command=lambda :self.Popup_info('Exit','We are taking you\n out from this.',1))
        self.exit.place(x=(self.wn_width//2+145),y=self.wn_height//2-190)
 
        self.play=Play(self)


    def show_menu(self):
        self.menu.destroy()
        self.exit.destroy()
        self.game_board.destroy()

    


    def single_player(self):
        self.single['state']=DISABLED
        self.multi['state']=NORMAL
        if self.f1:
            self.f1.destroy()
            self.f2.destroy()
        self.version='Single'

        self.f1=Frame(self.Interact_frame,height=400,width=400,bg=self.bgcolor)

        self.name_label=Label(self.f1,text='Player',font=(self.font,15),bg=self.bgcolor,justify='left',fg=self.fgcolor)
        self.name_label.pack(fill=BOTH,pady=10,side='left',padx=10)
        self.name_entry=Entry(self.f1,font=(self.font,15),bg=self.bgcolor,fg=self.fgcolor,bd=2,
                              insertbackground=self.fgcolor)
        self.name_entry.pack(fill=BOTH,pady=10,side='left',padx=10)

        self.start_button_1=Button(self.f1,text='Start',justify='center',height=1,width=7,font=(self.font,12,'bold'),
                                bg=self.bgcolor,fg=self.fgcolor,padx=0,pady=0,command=self.single_player_entry)
        self.start_button_1.pack(side='left',padx=10,pady=10)
        
        self.f1.place(x=30,y=150)

        self.f2=Frame(self.Interact_frame,height=400,width=400,bg=self.bgcolor)
        t='''Hello...
You are going to fight against my
algorithm that can beat you. You
can switch your player mode by top
menu.'''
        self.info_label=Label(self.f2,text=t,font=(self.font,15),bg=self.bgcolor,justify='left',fg='red')
        self.info_label.pack(fill=BOTH,side='left',pady=10,padx=10)


        self.f2.place(x=70,y=250)

    def single_player_entry(self):
        self.player_1=self.name_entry.get().capitalize()
        self.player_2='Opponent'
        
        if self.player_1=='':
            label=Label(self.Interact_frame,text='Plese fill the entry',font=(self.font,15),bg=self.bgcolor,justify='left',fg='red')
            label.place(x=115,y=128)
            self.name_entry.focus_set()
        else:
            self.fxn()
        
    def multi_player(self):
        self.multi['state']=DISABLED
        self.single['state']=NORMAL

        if self.f1:
            self.f1.destroy()
            self.f2.destroy()

        self.version='Multi'    
        self.f1=Frame(self.Interact_frame,height=400,width=400,bg=self.bgcolor)
        self.player_1=Label(self.f1,text='Player-1',font=(self.font,15),bg=self.bgcolor,justify='left',fg=self.fgcolor)
        self.player_1.pack(fill=BOTH,pady=10,side='left',padx=10)
        self.name_entry_1=Entry(self.f1,font=(self.font,15),bg=self.bgcolor,fg=self.fgcolor,bd=2,
                              insertbackground=self.fgcolor)
        self.name_entry_1.pack(fill=BOTH,pady=10,side='left',padx=10)
        self.f1.place(x=30,y=150)



        self.f2=Frame(self.Interact_frame,height=400,width=400,bg=self.bgcolor)

        self.player_2=Label(self.f2,text='Player-2',font=(self.font,15),bg=self.bgcolor,justify='left',fg=self.fgcolor)
        self.player_2.pack(fill=BOTH,side='left',pady=10,padx=10)

        self.name_entry_2=Entry(self.f2,bd=2,bg=self.bgcolor,font=(self.font,15),fg=self.fgcolor,
                                  insertbackground=self.fgcolor)
        self.name_entry_2.pack(fill=BOTH,pady=10,side='left',padx=10)

        self.start_button_2=Button(self.f2,text='Start',justify='center',height=1,width=7,font=(self.font,12,'bold'),
                                bg=self.bgcolor,fg=self.fgcolor,padx=0,pady=0,command=self.multi_player_entry)
        self.start_button_2.pack(side='left',padx=10,pady=10)
        self.f2.place(x=30,y=200)


    def multi_player_entry(self):
        self.player_1=self.name_entry_1.get().capitalize()
        self.player_2=self.name_entry_2.get().capitalize()
        
        if self.player_1=='' or self.player_2=='':
            label=Label(self.Interact_frame,text='Plese fill the entries',font=(self.font,15),bg=self.bgcolor,justify='left',fg='red')
            label.place(x=133,y=128)
            if self.player_1=='':
                self.name_entry_1.focus_set()
            else:
                self.name_entry_2.focus_set()
        else:
            self.fxn()


    def Popup_info(self,title='Help',t=None,flag=None):
        if self.popup:self.popup.destroy()
        self.window.bell()
        if not t: t=self.help_str
        self.popup=Toplevel(self.window)
        self.popup.protocol("WM_DELETE_WINDOW",self.fxnn)
        self.popup.title(title)
        self.popup.configure(background='black')
        self.popup.geometry('600x300+450+100')
        self.popup.transient(self.window)
        text_label=Label(self.popup,text=t,bg='black',fg='mediumspringgreen',font=('candara',15,'bold'))
        text_label.pack(side='left',fill=BOTH,expand=YES)

        for i in range(8):
            text_label.grid_rowconfigure(i,weight=1)
        for i in range(3):
            text_label.grid_columnconfigure(i,weight=1)


        Button(text_label,text='Exit',command=lambda : self.fxnn(flag),font=('candara',15,'bold'),
                  bg='mediumspringgreen',fg='black',width=10).grid(row=8,column=1,padx=5,pady=5)
            
            
        
        self.popup.mainloop()


    def fxnn(self,flag=None):
        if flag:
            self.window.destroy()
            return
        self.popup.destroy()

    def close_popup(self,event):
        if self.popup:
            self.fxnn()

        

    

if __name__=='__main__':
    i=Interact()
