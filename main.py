import pygame
from settings import *
from app_class import *
from button_class import *

# the game #
def game():
    app=App()
    app.run()


pygame.init()
pygame.font.init()

# rules window #
def rules():
	window = pygame.display.set_mode((WIDTH,HEIGHT))
	pygame.display.set_caption('rules')
	textfont=pygame.font.SysFont('arial',20)
	bfont=pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold',30)
	run = True
	f1=open('rules.txt','r')
	rulestr=f1.readlines()
	f1.close()
	line_1=rulestr[1][0:-1]
	line_2=rulestr[2][0:-1]
	line_3=rulestr[3][0:-1]
	line_4=rulestr[4][0:-1]
	line_5=rulestr[5][0:-1]
	line_6=rulestr[6][0:-1]
	line_7=rulestr[7][0:-1]
	line_8=rulestr[8][0:-1]
	line_9=rulestr[9]
	
	while run:
		window.fill(black)
		
		body_text_1= textfont.render(line_1, True, orange)
		body_text_2= textfont.render(line_2, True, orange)
		body_text_3= textfont.render(line_3, True, orange)
		body_text_4= textfont.render(line_4, True, orange)
		body_text_5= textfont.render(line_5, True, orange)
		body_text_6= textfont.render(line_6, True, orange)
		body_text_7= textfont.render(line_7, True, orange)
		body_text_8= textfont.render(line_8, True, orange)
		body_text_9= textfont.render(line_9, True, orange)

		window.blit(body_text_1,(20,50))
		window.blit(body_text_2,(20,75))
		window.blit(body_text_3,(20,100))
		window.blit(body_text_4,(20,125))
		window.blit(body_text_5,(20,150))
		window.blit(body_text_6,(20,175))
		window.blit(body_text_7,(20,200))
		window.blit(body_text_8,(20,225))
		window.blit(body_text_9,(20,250))

		mx,my=pygame.mouse.get_pos()

		button_e= pygame.Rect(100, 600 , 100 , 50)
		button_e_text = bfont.render("BACK", True , black)
		pygame.draw.rect(window,magenta,button_e)
		window.blit(button_e_text , (105,610))

		for event in pygame.event.get():
			if(event.type==pygame.QUIT):
				run = False
			if(event.type==pygame.MOUSEBUTTONDOWN):
				if(button_e.collidepoint((mx,my))):
					if(event.button==1):
						run=False

		pygame.display.update()


# menu window + integration of entire program #

def main():


	win = pygame.display.set_mode((WIDTH,HEIGHT))
	pygame.display.set_caption("menu")
	clock = pygame.time.Clock()
	run = True
	gamefont = pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 40)
	titlefont = pygame.font.SysFont('comicsansms', 100)
	while run:
		

		win.fill(black)
		title_text= titlefont.render('SUDOKU', True, white)
		win.blit(title_text,(150,100))

		mx,my= pygame.mouse.get_pos()

		button_1= pygame.Rect(250, 300 , 200 , 50)
		button_1_text = gamefont.render("PLAY", True , black)
		
		button_2= pygame.Rect(250, 500, 200 , 50)
		button_2_text = gamefont.render("EXIT", True , black)

		button_3= pygame.Rect(250, 400 , 200 , 50)
		button_3_text = gamefont.render("RULES", True , black)
		
		pygame.draw.rect(win,green,button_1)
		win.blit(button_1_text , (295,305))

		pygame.draw.rect(win,red,button_2)
		win.blit(button_2_text , (295,505))

		pygame.draw.rect(win,blue,button_3)
		win.blit(button_3_text , (280,405))

		pygame.display.update()
		
		for event in pygame.event.get():
			if(event.type==pygame.QUIT):
				run = False
			if(event.type==pygame.MOUSEBUTTONDOWN):
				if(button_1.collidepoint((mx,my))):
					if(event.button==1):
						game()
				elif(button_2.collidepoint((mx,my))):
					if(event.button==1):
						run= False
				elif(button_3.collidepoint((mx,my))):
					if(event.button==1):
						rules()

	pygame.quit()

# calling the main function loop#

if(__name__=='__main__'):
	main()






