#ProjectM 1.0.2

#Imports
import pygame, sys
from pygame.locals import *
import socket
from threading import Thread
import time
from multiprocessing import Queue

#Pygame Initilization
pygame.init()
fpsClock = pygame.time.Clock()
Font = pygame.font.Font(None, 21)

#Start Display
screen = pygame.display.set_mode((500, 700))
screen.fill((236, 236, 236))
pygame.display.update()

#Declare all the variables!
Messages = []
Send = ""
timer = 0
yp = 0
xp = 0
Shutdown = False
NameLen = False
Connected = False
Received = ''
data = ''
accepted = False
User = ''
HOST = ''
PORT = 1337
MYIP = socket.gethostbyname(socket.gethostname()) 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scan = ('', 54545)
recieve_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recieve_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
recieve_socket.bind(scan)
recieve_socket.settimeout(0)
broadcast = ('<broadcast>', 54545)
broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcast_socket.settimeout(0)
Users = {}

while True:
	try:
		s.bind((HOST, PORT))
		break
	except:
		timer += fpsClock.get_time()
		if timer >= 5000:
			print "ERROR: Could not bind port."
			s.close()
			pygame.quit()
			sys.exit()
			break

while True: #Nameing Loop
	screen.fill((236, 236, 236))
	lenx2, leny2 = Font.size(str(User.upper()))
	for event in pygame.event.get():
		if event.type == QUIT:
			Shutdown = True
			s.close()
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_BACKSPACE:
				User = User[:-1]
			elif event.key == K_DELETE:
				User = User[:-1]
			elif event.key == K_RETURN:
				User = User.upper()
				NameLen = True
			elif event.key == K_KP_ENTER:
				pass
			elif lenx2 >= 126:
				pass
			else:
				User += event.unicode

				
	#500/2 - boxsize/2 = centered | 250 - 69 = 183
	pygame.draw.rect(screen, (1, 1, 1), Rect((181, 600), (138, 20)), 0) # b
	pygame.draw.rect(screen, (255, 255, 255), Rect((183, 602), (134, 16)), 0) # w
	Name = Font.render(User.upper(), 1, (0,0,0))
	screen.blit(Name, (184,603))

	if lenx2 >= 126:
		pass
	else:
		timer += fpsClock.get_time()
		if timer >= 1000: # blink box
			pygame.draw.rect(screen, (50, 50, 50), Rect((lenx2 + 185, 603), (9, 14)), 0)
			if timer >= 2000:
				timer = 0
		if NameLen == True:
			User = "UserNm" + User
			data = User
			break

	pygame.display.update()
	fpsClock.tick(60)

while True: #Connecting Loop
	screen.fill((236, 236, 236))
	cp = len(Users.keys())
	for event in pygame.event.get():
		if event.type == QUIT:
			Shutdown = True
			s.close()
			pygame.quit()
			sys.exit()
			data = "QuitDe" + str(User[6:]) 
		elif event.type == KEYDOWN:
			if event.key == K_UP:
				print "Up"
				if yp == 0:
					pass
				else:
					yp -= 1
			elif event.key == K_DOWN:
				print "Down"
				if yp == (len(Users.keys()) -1):
					pass
				else:
					yp += 1
					print str(yp)
			elif event.key == K_LEFT: # make change to 'a' and 'd' for accepting
				xp -= 1
			elif event.key == K_RIGHT:
				xp += 1
			elif event.key == K_RETURN:
				if cp == 0:
					print "0: Online"
				else:
					data = "ConReq" + Users.values()[yp]
	if data[:6] == "ConReq":
		try:
			s.connect(Users.values()[yp], PORT)
		except:
			print Users.values()[yp]

	broadcast_socket.sendto(data, broadcast)
	
	recv_data, addr = recieve_socket.recvfrom(2048)
	if recv_data[:6] == "UserNm":
		#if addr[0] != MYIP and addr[0] not in Users.values(): #Connect to others
		if addr[0] not in Users.values(): #Connect to yourself
			Users[recv_data[6:]] = addr[0]
	elif recv_data[:6] == "QuitDe":
		del Users[recv_data[6:]]
	elif recv_data == "ConReq" + str(MYIP):
		if accepted == False:
			if raw_input(str(recv_data[6:]) + " would like to connect (y/n)").upper() == "Y":
				accepted = True
		if accepted == True:
			try:
				s.connect((addr[0], PORT))
				break
			except:
				print str(addr[0])

	elif recv_data[:6] == "Cancel":
		pass
		
	
	y = 10
	for z in range(len(Users.keys())):
		UsersRen = Font.render(Users.keys()[z], 1, (0,0,0))
		screen.blit(UsersRen, (34 , y))
		y += 20
	
	if True:
		pygame.draw.rect(screen, (1, 1, 1), Rect((24, (yp * 20) + 16), (10, 4)), 0)
		
		

	pygame.draw.rect(screen, (1, 1, 1), Rect((0, 660), (500, 2)), 0)
	pygame.draw.rect(screen, (255, 255, 255), Rect((0, 662), (500, 38)), 0) # w
	
	pygame.display.update()
	fpsClock.tick(60)

s.settimeout(0)
while True: #Talking Loop
	for event in pygame.event.get():
		if event.type == QUIT:
			s.sendall(User + " HAS LEFT.#4r5>Ty")
			Shutdown = True
			s.close()
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_BACKSPACE:
				Send = Send[:-1]
			elif event.key == K_DELETE:
				User = User[:-1]
			elif event.key == K_KP_ENTER:
				pass
			elif event.key == K_RETURN:
				if Send == "":
					pass
				else:
					try:
						s.sendall(User + ": " + Send)
					except IOError, e:
						pass
					Messages.append([Send, 0])
					Send = ""
			else:
				Send += event.unicode

	SendRendered = Font.render(Send, 1, (0,0,0))
	screen.fill((236, 236, 236))
	pygame.draw.rect(screen, (1, 1, 1), Rect((0, 660), (500, 4)), 0)
		

	try:        
		Received = s.recv(1024)
	except:
		pass
	if Received != '':
		Messages.append([Received[6:], 1])
		Received = ''

	x = 634
	#render Messages
	for y in range(len(Messages)-1,-1,-1):
		if x >= -10: # stops rendering above the view max
			lenx, leny = Font.size(str(Messages[y][0]))
			lenx2, leny2 = Font.size(str(Messages[y][0]))
			if Messages[y][1] == 0:
				pygame.draw.rect(screen, (1, 1, 1), Rect((482 - lenx2, x-1), (lenx2+16, 20)), 0) #black
				pygame.draw.rect(screen, (255, 255, 255), Rect((484 - lenx2, x+1), (lenx2 + 2, 16)), 0) #white
				pygame.draw.rect(screen, (26, 169, 174), Rect((488, x+1), (8, 16)), 0) #change for diffent colour
				MessagesRendered = Font.render(Messages[y][0], 1, (0,0,0))
				screen.blit(MessagesRendered, (485 - lenx2 ,x+1))
			else: # recived
				if Messages[y][0][-7:] == "#4r5>Ty": # We know of this bug, but... (it's kinda funny)
					lenx, leny = Font.size(str(Messages[y][0][:-7]))
					pygame.draw.rect(screen, (1, 1, 1), Rect((6, x-1), (lenx + 8, 20)), 0)
					pygame.draw.rect(screen, (255, 255, 255), Rect((8, x+1), (lenx + 4, 16)), 0)
					MessagesRendered = Font.render(Messages[y][0][:-7], 1, (204,42,39))
					screen.blit(MessagesRendered, (10,x+1))
					if event.type == KEYDOWN:
						if event.key == K_RETURN:
							Shutdown = True
							s.close()
							pygame.quit()
							sys.exit()
					
				else: # normal
					pygame.draw.rect(screen, (1, 1, 1), Rect((6, x-1), (lenx + 8, 20)), 0)
					pygame.draw.rect(screen, (255, 255, 255), Rect((8, x+1), (lenx + 4, 16)), 0)
					MessagesRendered = Font.render(Messages[y][0], 1, (0,0,0))
					screen.blit(MessagesRendered, (10,x+1))
		x -= 24

	screen.blit(SendRendered, (10,675))

	lenx2, leny2 = Font.size(str(Send))
	timer += fpsClock.get_time()
	if timer >= 1000: # blink box
		pygame.draw.rect(screen, (50, 50, 50), Rect((lenx2 + 10, 676), (9, 15)), 0)
		if timer >= 2000:
			timer = 0

	pygame.display.update()
	fpsClock.tick(60)

