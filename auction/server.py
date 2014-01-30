#!/usr/bin/env python
# Echo server program
import select
import socket
import sys
import random

HOST = ''        # Symbolic name meaning all available interfaces
PORT = 50018              # Arbitrary non-privileged port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
input = [server,sys.stdin]
numbidders = 2
bidderids = []
neededtowin = 3 # how many items each player needs to win
itemtypes = ['t1', 't2', 't3', 't4'] # four different types
maxbudget = 100 # budget per player
won = {}
won['t1'] = [0 for x in range(numbidders)]
won['t2'] = [0 for x in range(numbidders)]
won['t3'] = [0 for x in range(numbidders)]
won['t4'] = [0 for x in range(numbidders)]
moneyspent= [0 for x in range(numbidders)]
listtosend = ''
typearray = []
i = 0
while(i < 200):
  	x = itemtypes[int((len(itemtypes))*random.random())]
  	typearray.append(x)
  	listtosend = listtosend + x + ' '
	i+= 1
print listtosend

# distribute list to send to everyone
bidderids = []
while(numbidders > len(bidderids)):
   inputready,outputready,exceptready = select.select(input,[],[])
   for s in inputready:
    if s == server:
	 # print "In server case"
	client, address = server.accept()
	input.append(client)
    if((s != server) & (s!=sys.stdin)):
      data = s.recv(1024)
      if not data: 
	  print "Have not received data from", str(s)
      indata = data.split(" ")
      # print ' '.join(indata)
      if(indata[0] in bidderids):
      	s.send("Not ready " + indata[0] )
      else:
         s.send(listtosend)
         bidderids.append(indata[0])

doneflag = 0 # will be done only if someone wins or goes over budget with money spent
j = 0
while(0 == doneflag):
  # print "Auction round is: ", j
  bidderids = []
  bids = []
  mytype = typearray[j]
  while(numbidders > len(bidderids)):
   inputready,outputready,exceptready = select.select(input,[],[])
   for s in inputready:
    if s == server:
	 # print "In server case"
	client, address = server.accept()
	input.append(client)
    if((s != server) & (s!=sys.stdin)):
      data = s.recv(1024)
      if not data: 
	 print "Have not received data from", str(s)
      indata = data.split(" ")
      # print ' '.join(indata)
      if(indata[0] in bidderids):
      	s.send("Not ready " + indata[0] + " to tell you about move " + str(j) )
      else:
         s.send("Thank you, " + indata[0] +  " I have received your bid of " + indata[1])
	 x = int(indata[1])
	 if (x > (maxbudget - moneyspent[int(indata[0])])):
		x = 0 # indata[0] is not allowed to bid over budget
         bids.append(x)
         bidderids.append(indata[0])
         # print "number of bids received is: ", len(bidderids)
  # Now have all the bids
  bestbid = max(bids)
  # print "Best bid for step ", j, " is ", bestbid
  # print "Here are the identifiers of the bidders " 
  # print bidderids
  # print "Here are the bids "
  # print bids
  winnerid=bidderids[random.choice([x for x in range(len(bids)) if bids[x]==bestbid])]
  #winnerid = bidderids[bids.index(bestbid)]

  # Now receive requests for results
  deletedindexes = [] # record which indexes are gone
  while(numbidders > len(deletedindexes)):
   inputready,outputready,exceptready = select.select(input,[],[])
   for s in inputready:
    if((s != server) & (s!=sys.stdin)):
      data = s.recv(1024)
      if not data: 
	 print "Have not received data from", str(s)
      indata = data.split(" ")
      # print ' '.join(indata)
      myindex = bidderids.index(indata[0])
      if(myindex not in deletedindexes):
	   deletedindexes.append(myindex)
           if(myindex == bids.index(bestbid)) :
    		# s.send(bidderids[myindex] + ' you have bought this item of type ' + mytype)
    		s.send(bidderids[myindex] + ' Player ' + winnerid +  ' has bought this item of type ' + mytype + ' for ' + str(bestbid))
		print "Player ", winnerid, " bought type ", mytype, " in round ", j
		won[mytype][int(bidderids[myindex])]+= 1
		moneyspent[int(bidderids[myindex])]+= bestbid
		if(won[mytype][int(bidderids[myindex])] >= neededtowin):
			print "Player ", bidderids[myindex], " has won."
			doneflag = 1
           else:
    		s.send(bidderids[myindex] + ' Player ' + winnerid +  ' has bought this item of type ' + mytype + ' for ' + str(bestbid))
      else:
         s.send("Not ready for next round yet " + indata[0])
  j+=1
