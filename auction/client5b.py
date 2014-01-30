# Echo client program
import socket
import random
import time

HOST = ''    # The remote host

# to act as a client
PORT = 50018              # The server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


# APPLICATION

partnerid = -1 # no partner
numberbidders = 2 # other person

# DO SOMETHING HERE
# you need to change this to do something much more clever
def determinebid(itemsinauction, partnerid, numberbidders, winnerarray, winneramount):
	i = len(winnerarray)
	print itemsinauction[:i]
	print winnerarray[:i]
	print winneramount[:i]
  	return int(50*random.random())

# DATA

mybidderid = 1  # this is the only thing that distinguishes the clients 

moneyleft = 100 # should change over time
winnerarray = [] # who won each round
winneramount = [] # how much they paid

itemsinauction = []

# EXECUTION

# get list of items and types
getlistflag = 1
while(getlistflag == 1):
  	s.send(str(mybidderid) + " " + str(int(50*random.random())))
  	# print "Have sent data from ", str(mybidderid)
  	data = s.recv(1024)
  	x = data.split(" ")
  	# print "Have received response at ", str(mybidderid), " of: ", ' '.join(x)
	if(x[0] != "Not"):
		getlistflag = 0
  		itemsinauction = x
	else:
		time.sleep(2)


# now do bids
j = 0
while(1):
   print "Auction round is: ", j
   bidflag = 1
   while(bidflag == 1):
	x = determinebid(itemsinauction, partnerid, numberbidders, winnerarray, winneramount)
  	s.send(str(mybidderid) + " " + str(x))
  	# print "Have sent data from ", str(mybidderid)
  	data = s.recv(1024)
  	x = data.split(" ")
  	# print "Have received response at ", str(mybidderid), " of: ", ' '.join(x)
	if(x[0] != "Not"):
		bidflag = 0
	else:
		time.sleep(2)

   resultflag = 1
   while(resultflag == 1):
  	s.send(str(mybidderid) + " " + str(int(50*random.random())))
  	# print "Have sent data from ", str(mybidderid)
  	data = s.recv(1024)
  	x = data.split(" ")
  	# print "Have received response at ", str(mybidderid), " of: ", ' '.join(x)
	if(x[0] != "Not"):
		resultflag = 0
  		print ' '.join(x)
		# print x
		winnerarray.append(int(x[2]))
		winneramount.append(int(x[11]))
		# update moneyleft, winnerarray
	else:
		time.sleep(2)
   j+= 1


