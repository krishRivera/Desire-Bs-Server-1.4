import bs
#import threading
import bsInternal
import hack #Desire was here 
#import time
counter = {}
spammers = {}


def warn(ID):
	if ID in spammers:
		spammers[ID] += 1
	else:
		spammers[ID] = 1	
	return spammers[ID]

def getID(clID):
	#aid = None
	for i in bsInternal._getGameRoster():
	    if i['clientID'] == clID:
		displayString = i['displayString']
		return displayString


def checkSpam(clientID):
	#name = getID(clientID)
	#find id from clientID
	for i in bsInternal._getGameRoster():
	    if i['clientID'] == clientID:
		ID = i['displayString']
		name = ID
		try:
			name = i['players'][0]['nameFull']
		except:
			pass
	
	global counter
	if ID in counter: 
		counter[ID] += 1
		if counter[ID] == 3:
			bs.screenMessage("Don't Spam Here!",color = (1,0,0))
			warnCount = warn(ID)
			with bs.Context(bsInternal._getForegroundHostActivity()):bs.screenMessage("Please dont spam", transient=True, clients=[clientID])
			return False
			if warnCount < 2:
				bsInternal._chatMessage("{}, don't spam here!".format(name))
				with bs.Context(bsInternal._getForegroundHostActivity()):bs.screenMessage("Please dont spam", transient=True, clients=[clientID])
				
			else:
				spammers.pop(ID)		
				bsInternal._chatMessage("Warn limit exceeded. Kicking {} for spamming.".format(name))
				#bsInternal._chatMessage("ChatFilter Made By Ankit")
				bsInternal._disconnectClient(clientID)
	else: counter[ID] = 1

def reset():
    global counter
    counter = {}
if hack.spamProtection: timer = bs.Timer(2000,reset,timeType='real',repeat=True)
print 'Spam protection loaded...' 