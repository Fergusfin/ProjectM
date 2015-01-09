#ProjectM 0.3.1415962

#Imports
import pygame, sys
from pygame.locals import *
import socket

#Pygame Initilization
pygame.init()
fpsClock = pygame.time.Clock()
Font = pygame.font.Font(None, 21)
Font2 = pygame.font.Font(None, 40)

#Start Display
screen = pygame.display.set_mode((500, 700))
screen.fill((236, 236, 236))
pygame.display.update()

#Declare all the variables!
Messages = []
Send = ""
timer = 0
timer2 = 0
yp = 0
xp = 0
TryCon = False
Shutdown = False
NameLen = False
Connected = False
Received = ''
data = ''
accepted = False
User = ''
HOST = ''
PORT = 1338
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
Requests = {}



def textcut(text,line):
	cut = 0
	#print text
	#lenxT, lenxZ = Font.size(text)
	TextSplit = text.split(" ")
	Runs = len(TextSplit)
	Ln1 = []
	Ln2 = []
	print "Start"
	while True:
		print "run"
		lenx, leny = Font.size(" ".join(TextSplit[:cut]))
		print " ".join(TextSplit[:cut])
		print str(lenx)		
		if lenx > 485:
			cut -= 1
			Ln1 = " ".join(TextSplit[:cut])
			Ln2 = " ".join(TextSplit[cut:])
			print Ln2
			if line == 1:
				return Ln1
			else:
				return Ln2
			break
		else:
			print "1"
			cut += 1
			
		"""else:
			Ln1 = " ".join(Ln1)
			Ln2 = " ".join(TextSplit)
			print Ln1
			print Ln2		
			return Ln1, Ln2
			break"""
		
		"""lenx, leny = Font.size("".join(New))
		if lenx < 485:
			print "Yes"
			cut += 1
			print str(cut)
			New = []
		else:
			del New[-1]
			for z in range(cut, len(textSplit)):
				Ln2.append(TextSplit[z])
			New = "".join(New)
			Ln2 = "".join(Ln2)
			print "You got here"
			print New
			print Ln2		
			return New, Ln2
			break"""
				
	"""for x in range(len(TextSplit)):
		lenxT, lenxZ = Font.size(" ".join(TextSplit))
		if lenxT > 482:
			cut += 1
			if TextSplit[len(TextSplit) - cut] == " ":
				TNL += " " + TNL
			else:
				TNL = TextSplit[len(TextSplit) - cut] + " " + TNL	
			del TextSplit[-1]
	else:
		TOR = " ".join(TextSplit)
		return TOR, TNL"""

	"""if len(TextSplit) <= 4: # "-" cut
		pass
		#"dash cuting"
		#look for word just before a good length
		#cut that word by the letter until it fits with a "-"
		#for
			#if
		#else:
			#TOR =
			#TNL =
	else: # " " cut
		while lenxT > 140:
			for x in range(len(TextSplit)):
				if TextSplit[x] == " ":
					TOR += " "
				else:
					TOR += TextSplit[x] + " "
			else:
				TOR = TOR[:-1] # cut "space" off end
				lenxT, lenxZ = Font.size(TOR)
		else: # while loop End
			print str(len(TextSplit) - cut)
			print str(len(TextSplit))
			if len(TextSplit) > 4:
				for x in range(len(TextSplit) - cut, len(TextSplit)): # the other line of text
					#print x
					break			
					#TNL += TextSplit[x] # will have to make a chack for the whole dash cut thing
			print "TOR " + TOR
			print "TNL " + TNL
			return TOR, TNL"""



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
			if event.key == K_BACKSPACE or event.key == K_DELETE:
				User = User[:-1]
			elif event.key == K_RETURN or event.key == K_KP_ENTER:
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
	EntUser = Font.render("Enter Username", 1, (0,0,0))
	screen.blit(EntUser, (191,582))

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
			data = "QuitDe" + str(User[6:])
			broadcast_socket.sendto(data, broadcast)
			Shutdown = True
			s.close()
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_UP:
                                if TryCon == True or accepted == True:
                                        pass
                                else:
                                        if yp == 0:
                                                pass
                                        else:
                                                yp -= 1
			elif event.key == K_DOWN:
				if TryCon == True or accepted == True:
                                        pass
                                else:
                                        if yp == (len(Users.keys()) -1):
                                                pass
                                        else:
                                                yp += 1
			elif event.key == K_a:
                                if Users.values()[yp] in Requests.values():
                                        accepted = True
                        elif event.key == K_d:
                                data = "ConDec" + Users.values()[yp]
                                for x in Requests.values():
                                        if addr[0] in x:
                                                del Requests[Requests.keys()[Requests.values().index(str(x))]]
			elif event.key == K_RETURN or event.key == K_KP_ENTER:
				if cp == 0:
					pass
				else:
					data = "ConReq" + Users.values()[yp] + str(User)
                                        TryCon = True
                        elif event.key == K_ESCAPE:
                                data = "Cancel" + Users.values()[yp]
                                TryCon = False
        
        broadcast_socket.sendto(data, broadcast)
	
	recv_data, addr = recieve_socket.recvfrom(2048)
	# Conneting Requst
        if TryCon == True:
                if recv_data == "ConDec" + str(MYIP):
                	data = User
                        TryCon = False
                else:
                        try:
				CLIENT = Users.values()[yp]
                                s.connect((CLIENT, PORT))
				break
                        except:
                                pass
	# Others
	if recv_data[:6] == "UserNm":
		#if addr[0] != MYIP and addr[0] not in Users.values(): #Connect to others
		if addr[0] not in Users.values(): #Connect to yourself
			Users[recv_data[6:]] = addr[0]
	elif recv_data[:6] == "QuitDe":
		del Users[recv_data[6:]]
	elif recv_data[:6 + len(MYIP)] == "ConReq" + str(MYIP):
                if recv_data not in Requests.keys():
                        Requests[recv_data] = addr[0]
        elif recv_data == "Cancel" + str(MYIP):
                for x in Requests.values():
                        if addr[0] in x:
                                del Requests[Requests.keys()[Requests.values().index(str(x))]]
        
        if accepted == True:
                        try:
				CLIENT = Users.values()[yp]
                                s.connect((CLIENT, PORT))
                                break
                        except:
                                pass
		
	if data != User:
		timer2 += fpsClock.get_time()
		if timer2 >= 1000:
			data = User

	y = 10
        for z in range(len(Users.keys())):
                if yp == z:
                        pygame.draw.rect(screen, (20, 20, 20), Rect((10, y), (404, 28)), 0) # OUT SHAPE
                        pygame.draw.rect(screen, (100, 100, 240), Rect((12, y+2), (400, 24)), 0) # SELECT C # 240
                        pygame.draw.rect(screen, (1, 1, 1), Rect((14, y+4), (396, 20)), 0) # IN BOX
                        pygame.draw.rect(screen, (255, 255, 255), Rect((16, y+6), (392, 16)), 0) # Base Box
                else:
                        pygame.draw.rect(screen, (20, 20, 20), Rect((10, y), (404, 28)), 0) # OUT SHAPE
                        pygame.draw.rect(screen, (240, 240, 240), Rect((12, y+2), (400, 24)), 0) # SELECT C # 240
                        pygame.draw.rect(screen, (1, 1, 1), Rect((14, y+4), (396, 20)), 0) # IN BOX
                        pygame.draw.rect(screen, (255, 255, 255), Rect((16, y+6), (392, 16)), 0) # Base Box
                UsersRen = Font.render(Users.keys()[z], 1, (0,0,0))
                screen.blit(UsersRen, (18 , y+6))
                
                for c in Requests.keys():
                        if Users.keys()[z] == c[12+len(str(MYIP)):]:
                                pygame.draw.rect(screen, (20, 20, 20), Rect((416, y), (12, 28)), 0)
                                pygame.draw.rect(screen, (255, 102, 0), Rect((418, y+2), (8, 24)), 0)
                                if yp == z:
                                        UserReqA = Font.render("A", 1, (44, 202, 60))
                                        UserReqS = Font.render("/", 1, (0,0,0))
                                        UserReqD = Font.render("D", 1, (233, 2, 22))
                                        screen.blit(UserReqA, (380, y+6))
                                        screen.blit(UserReqS, (392, y+6))
                                        screen.blit(UserReqD, (397, y+6))
                        
                y += 30
		

	pygame.draw.rect(screen, (1, 1, 1), Rect((0, 660), (500, 2)), 0)
	pygame.draw.rect(screen, (255, 255, 255), Rect((0, 662), (500, 38)), 0) # w
	
	if TryCon == True or accepted == True: # for a planned connetting animation
                trans = pygame.Surface((500, 700), pygame.SRCALPHA, 32)
                trans.fill((120, 120, 120, 180))
                screen.blit(trans, (0,0))
		timer += fpsClock.get_time()
		if timer <= 1000:
			ContDot = Font2.render("Connecting", 1, (0,0,0))
		elif timer <= 2000:
			ContDot = Font2.render("Connecting.", 1, (0,0,0))
		elif timer <= 3000:
			ContDot = Font2.render("Connecting..", 1, (0,0,0))
		elif timer <= 4000:
			ContDot = Font2.render("Connecting...", 1, (0,0,0))
		elif timer <= 5000:
			timer = 0
		screen.blit(ContDot, (165, 335))
	
	pygame.display.update()
	fpsClock.tick(60)

s.settimeout(0)
while True: #Talking Loop
	for event in pygame.event.get():
		if event.type == QUIT:
			s.sendall("#4r5>Ty" + User[6:] + " HAS LEFT.")
			Shutdown = True
			s.close()
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_BACKSPACE or event.key == K_DELETE:
				Send = Send[:-1]
			elif event.key == K_RETURN or event.key == K_KP_ENTER:
				if Send == "":
					pass
				else:
					try:
						s.sendall(User[6:] + ": " + Send)
					except IOError, e:
						pass
					Messages.append([Send, 0])
					Send = ""
			else:
				Send += event.unicode

	SendRendered = Font.render(Send, 1, (0,0,0))
	screen.fill((236, 236, 236))
	pygame.draw.rect(screen, (1, 1, 1), Rect((0, 650), (500, 4)), 0)
		

	try:        
		Received = s.recv(1024)
	except:
		pass
	if Received != '':
		Messages.append([Received, 1])
		Received = ''

	#render Messages
	y = 624
	for z in range(len(Messages)-1,-1,-1):
		if y >= -10: # stops rendering above the view max
			lenx, leny = Font.size(str(Messages[z][0]))
			lenx2, leny2 = Font.size(str(Messages[z][0]))
			#print textcut(Messages[z][0])
			if Messages[z][1] == 0:
				if lenx2 > 482:#double box render.........
					y -= 19
					SplitWord = textcut(Messages[z][0])
					onex, oney = Font.size(str(SplitWord[0]))
					twox, twoy = Font.size(str(SplitWord[1]))
					pygame.draw.rect(screen, (1, 1, 1), Rect((482 - onex, y-1), (onex+16, 20 + twoy)), 0) #black
					pygame.draw.rect(screen, (255, 255, 255), Rect((484 - onex, y+1), (onex + 2, 16 + twoy)), 0) #white
					pygame.draw.rect(screen, (26, 169, 174), Rect((488, y+1), (8, 16 + twoy)), 0) # Blue
					MessagesRendered = Font.render(SplitWord[0], 1, (0,0,0))
					MessagesRendered2 = Font.render(SplitWord[1], 1, (0,0,0))
					screen.blit(MessagesRendered, (485 - onex ,y+1))
					screen.blit(MessagesRendered2, (485 - onex ,y+19))
					
				else:
					pygame.draw.rect(screen, (1, 1, 1), Rect((482 - lenx2, y-1), (lenx2+16, 20)), 0) #black
					pygame.draw.rect(screen, (255, 255, 255), Rect((484 - lenx2, y+1), (lenx2 + 2, 16)), 0) #white
					pygame.draw.rect(screen, (26, 169, 174), Rect((488, y+1), (8, 16)), 0) #change for diffent colour
					MessagesRendered = Font.render(Messages[z][0], 1, (0,0,0))
					screen.blit(MessagesRendered, (485 - lenx2 ,y+1))
			else: # recived
				if Messages[z][0][:7] == "#4r5>Ty":
					lenx, leny = Font.size(str(Messages[z][0][7:]))
					pygame.draw.rect(screen, (1, 1, 1), Rect((6, y-1), (lenx + 8, 20)), 0)
					pygame.draw.rect(screen, (255, 255, 255), Rect((8, y+1), (lenx + 4, 16)), 0)
					MessagesRendered = Font.render(Messages[z][0][7:], 1, (204,42,39))
					screen.blit(MessagesRendered, (10,y+1))
					if event.type == KEYDOWN:
						if event.key == K_RETURN:
							Shutdown = True
							s.close()
							pygame.quit()
							sys.exit()
					
				else: # normal
					if lenx > 482:
						y -= 19
						onex, oney = Font.size(str(textcut(Send, 1)))
						twox, twoy = Font.size(str(textcut(Send, 2)))
						pygame.draw.rect(screen, (1, 1, 1), Rect((6, y-1), (onex + 8, 20 + twoy)), 0)
						pygame.draw.rect(screen, (255, 255, 255), Rect((8, y+1), (onex + 4, 16 + twoy)), 0)
						MessagesRendered = Font.render(textcut(Send, 1), 1, (0,0,0))
						MessagesRendered2 = Font.render(textcut(Send, 2), 1, (0,0,0))
						screen.blit(MessagesRendered, (10,y+1))
						screen.blit(MessagesRendered2, (10,y+19))
					else:
						pygame.draw.rect(screen, (1, 1, 1), Rect((6, y-1), (lenx + 8, 20)), 0)
						pygame.draw.rect(screen, (255, 255, 255), Rect((8, y+1), (lenx + 4, 16)), 0)
						MessagesRendered = Font.render(Messages[z][0], 1, (0,0,0))
						screen.blit(MessagesRendered, (10,y+1))
		y -= 24
	
	onex, oney = Font.size(Send)
	if onex > 485:		
		twox, twoy = Font.size(textcut(Send, 2))
		LineOne = Font.render(textcut(Send, 1), 1, (0,0,0))
		LineTwo = Font.render(textcut(Send, 2), 1, (0,0,0))
		screen.blit(LineOne, (10,660))
		screen.blit(LineTwo, (10,678))
	else:
		screen.blit(SendRendered, (10,660))

	lenx2, leny2 = Font.size(str(Send))
	timer += fpsClock.get_time()
	if timer >= 1000: # blink box
		if onex < 485:
			pygame.draw.rect(screen, (50, 50, 50), Rect((lenx2 + 10, 661), (9, 15)), 0)
		else:
			twox, twoy = Font.size(textcut(Send, 2))
			pygame.draw.rect(screen, (50, 50, 50), Rect((twox + 9, 679), (9, 15)), 0)
		if timer >= 2000:
			timer = 0

	pygame.display.update()
	fpsClock.tick(60)
