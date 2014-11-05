import pygame, sys
from pygame.locals import *
import socket
from threading import Thread
import time
from multiprocessing import Queue

pygame.init()
fpsClock = pygame.time.Clock()
Font = pygame.font.Font(None, 21)

Messages = []
Send = ""
timer = 0
Shutdown = False

HOST = ''
PORT = 1337

MYIP = socket.gethostbyname(socket.gethostname())
IP = MYIP.split(".")
IP = IP[0] + "." + IP[1] + "." + IP[2] + "."
x = 0
Connected = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print "Starting..."

def Connect():
	address = ('<broadcast>', 54545)
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	data = "Request"
	client_socket.settimeout(0.5)
	while True:
		try:
			client_socket.sendto(data, address)
			recv_data, addr = client_socket.recvfrom(2048)
		except:
			pass
		if Shutdown == True:
			client_socket.close()
			break

def Receive():
	global Messages
	global Connected
	Received = ''
	while True:
		try:        
                	Received = s.recv(1024)
        	except:
                	pass
		if Received != '':
			Messages.append([Received, 1])
			Received = ''
			Connected = True
		if Shutdown == True:
			break
		
#s.bind((HOST, PORT))
while 1:
	try:
		s.bind((HOST, PORT))
		print "Port Connected"
		break
	except:
		timer += fpsClock.get_time()
		if timer >= 5000:
			print "ERROR: Could not bind port."
			s.close()
                        pygame.quit()
                        sys.exit()
			break

t1 = Thread(target = Connect)
t2 = Thread(target = Receive)
t1.start()
t2.start()

address = ('', 54545)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_socket.bind(address)

while True:
	recv_data, addr = server_socket.recvfrom(2048)
	CLIENT = addr[0]
	server_socket.sendto("", addr)
	if CLIENT != MYIP:
		break

print "Connecting to " + CLIENT

while 1:
	try:
		s.connect((CLIENT, PORT))
		break
	except:
		pass
server_socket.close()

s.settimeout(0)
User = ""
while True:
	User = raw_input("Please enter a user name less than 15 characters: ").upper()
	if User == '':
		pass
	elif len(str(User)) > 15:
		pass
	else:
		break

screen = pygame.display.set_mode((500, 700))

while True:
	for event in pygame.event.get():
                if event.type == QUIT:
                        s.sendall(User + " HAS LEFT.#4r5>Ty")
			Shutdown = True
                        s.close()
                        pygame.quit()
                        sys.exit()
		elif event.type == KEYDOWN:
			Send += event.unicode
			if event.key == K_BACKSPACE:
				Send = Send[:-2]
			elif event.key == K_RETURN:
				Send = Send[:-1]
				if Send == "":
					pass
				else:
					try:
						s.sendall(User + ": " + Send)
					except IOError, e:
						pass
					Messages.append([Send, 0])
					Send = ""

	SendRendered = Font.render(Send, 1, (0,0,0))
        screen.fill((236, 236, 236))
        pygame.draw.rect(screen, (1, 1, 1), Rect((0, 660), (500, 4)), 0)

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
