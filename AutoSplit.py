## Copyright 2017 Ben Massey
## Simple Python program that looks at your SUPERHOT VR save file in order to
## automatically do splits with livesplit for any% speedruns.

## IT SHOULD BE NOTED that there is a lot of hardcoded stuff in here.
## The filepath is set to my own computer's specific one. Make sure to change
## it to your own.
## My livesplit is specifically set to split with the "end" key, make sure to
## change to your own split key.

## It should also be said that while this is for speedrunning, these splits do
## not correspond directly to the way that SUPERHOT VR Any% is timed. Make sure
## to use separate splits when using this versus when trying to do leaderboard
## timing.

# Imports
from tkinter import * # Need for gui
import win32api, win32con # Need for keypresses
from time import * # Need for timing
import re # Need for parsing through SUPERHOT VR save file

VK_CODE = {'backspace':0x08,
           'tab':0x09,
           'clear':0x0C,
           'enter':0x0D,
           'shift':0x10,
           'ctrl':0x11,
           'alt':0x12,
           'pause':0x13,
           'caps_lock':0x14,
           'esc':0x1B,
           'spacebar':0x20,
           'page_up':0x21,
           'page_down':0x22,
           'end':0x23,
           'home':0x24,
           'left_arrow':0x25,
           'up_arrow':0x26,
           'right_arrow':0x27,
           'down_arrow':0x28,
           'select':0x29,
           'print':0x2A,
           'execute':0x2B,
           'print_screen':0x2C,
           'ins':0x2D,
           'del':0x2E,
           'help':0x2F,
           '0':0x30,
           '1':0x31,
           '2':0x32,
           '3':0x33,
           '4':0x34,
           '5':0x35,
           '6':0x36,
           '7':0x37,
           '8':0x38,
           '9':0x39,
           'a':0x41,
           'b':0x42,
           'c':0x43,
           'd':0x44,
           'e':0x45,
           'f':0x46,
           'g':0x47,
           'h':0x48,
           'i':0x49,
           'j':0x4A,
           'k':0x4B,
           'l':0x4C,
           'm':0x4D,
           'n':0x4E,
           'o':0x4F,
           'p':0x50,
           'q':0x51,
           'r':0x52,
           's':0x53,
           't':0x54,
           'u':0x55,
           'v':0x56,
           'w':0x57,
           'x':0x58,
           'y':0x59,
           'z':0x5A,
           'numpad_0':0x60,
           'numpad_1':0x61,
           'numpad_2':0x62,
           'numpad_3':0x63,
           'numpad_4':0x64,
           'numpad_5':0x65,
           'numpad_6':0x66,
           'numpad_7':0x67,
           'numpad_8':0x68,
           'numpad_9':0x69,
           'multiply_key':0x6A,
           'add_key':0x6B,
           'separator_key':0x6C,
           'subtract_key':0x6D,
           'decimal_key':0x6E,
           'divide_key':0x6F,
           'F1':0x70,
           'F2':0x71,
           'F3':0x72,
           'F4':0x73,
           'F5':0x74,
           'F6':0x75,
           'F7':0x76,
           'F8':0x77,
           'F9':0x78,
           'F10':0x79,
           'F11':0x7A,
           'F12':0x7B,
           'F13':0x7C,
           'F14':0x7D,
           'F15':0x7E,
           'F16':0x7F,
           'F17':0x80,
           'F18':0x81,
           'F19':0x82,
           'F20':0x83,
           'F21':0x84,
           'F22':0x85,
           'F23':0x86,
           'F24':0x87,
           'num_lock':0x90,
           'scroll_lock':0x91,
           'left_shift':0xA0,
           'right_shift ':0xA1,
           'left_control':0xA2,
           'right_control':0xA3,
           'left_menu':0xA4,
           'right_menu':0xA5,
           'browser_back':0xA6,
           'browser_forward':0xA7,
           'browser_refresh':0xA8,
           'browser_stop':0xA9,
           'browser_search':0xAA,
           'browser_favorites':0xAB,
           'browser_start_and_home':0xAC,
           'volume_mute':0xAD,
           'volume_Down':0xAE,
           'volume_up':0xAF,
           'next_track':0xB0,
           'previous_track':0xB1,
           'stop_media':0xB2,
           'play/pause_media':0xB3,
           'start_mail':0xB4,
           'select_media':0xB5,
           'start_application_1':0xB6,
           'start_application_2':0xB7,
           'attn_key':0xF6,
           'crsel_key':0xF7,
           'exsel_key':0xF8,
           'play_key':0xFA,
           'zoom_key':0xFB,
           'clear_key':0xFE,
           '+':0xBB,
           ',':0xBC,
           '-':0xBD,
           '.':0xBE,
           '/':0xBF,
           '`':0xC0,
           ';':0xBA,
           '[':0xDB,
           '\\':0xDC,
           ']':0xDD,
           "'":0xDE,
           '`':0xC0}

run = False
		   
debug = 0 # 0 = none, 1 = basic, 2 = advanced

levelSearch = re.compile(b"\"highestfinishedLevel\":\"([a-zA-Z_]+)") # Search term for finding the level
finishedSearch = re.compile(b"\"gameFinished\":([a-z]+)") # Search term for finding the finished state

lastLevel = "NOLEVEL" # This will store the last level that you have been to, starts arbitrarily at "NOLEVEL" when you haven't started

# This will store what key the user chooses, but default is end key (because that's what I use)
try:
	file = open("key.txt")
	if len(file.readline()) > 0:
		key = VK_CODE[file.readline()]
	else:
		key = VK_CODE['end']
	file.close()
except:
	key = VK_CODE['end']


# Try to get the save file dir path, but nbd if nothing yet
try:
	file = open("path.txt")
	path = file.readline()
	file.close()
	if debug >= 1:
		print("Found directory!", path)
except:
	path = "" # They need to update it

class App:

	def __init__(self):
		self.root = Tk()
		self.root.title("SHVR Any% Autosplitter")
		try:
			self.root.iconbitmap('shvr.ico')
		except:
			pass # No big deal if no icon
		self.root.minsize(width=1,height=1)
		
		Label(self.root, text='Split Key:').pack()
		self.keyselect = StringVar()
		self.keys = ['backspace','tab','clear','enter','shift','ctrl','alt','pause','caps_lock','esc','spacebar','page_up','page_down','end','home','left_arrow','up_arrow','right_arrow','down_arrow','select','print','execute','print_screen','ins','del','help','0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','numpad_0','numpad_1','numpad_2','numpad_3','numpad_4','numpad_5','numpad_6','numpad_7','numpad_8','numpad_9','multiply_key','add_key','separator_key','subtract_key','decimal_key','divide_key','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','F13','F14','F15','F16','F17','F18','F19','F20','F21','F22','F23','F24','num_lock','scroll_lock','left_shift','right_shift ','left_control','right_control','left_menu','right_menu','browser_back','browser_forward','browser_refresh','browser_stop','browser_search','browser_favorites','browser_start_and_home','volume_mute','volume_Down','volume_up','next_track','previous_track','stop_media','play/pause_media','start_mail','select_media','start_application_1','start_application_2','attn_key','crsel_key','exsel_key','play_key','zoom_key','clear_key','+',',','-','.','/','`',';','[','\\',']',"'",'`']
		file = open("key.txt")
		self.keyselect.set(file.readline())
		file.close()
		self.selector = OptionMenu(self.root, self.keyselect, *self.keys).pack()
		self.keyselect.trace('w', self.setkey)
		try:
			self.setkey()
		except:
			pass
		
		Label(self.root, text='Save Directory:').pack()
		file = open("path.txt")
		self.savedir = StringVar(value=file.readline())
		file.close()
		self.saveEntry = Entry(self.root, textvariable=self.savedir).pack()
		self.titleButton = Button(self.root, text='Set', command = self.updatepath, fg = 'white',bg='black').pack()
		
		# Little button to test the split key functionality
		#self.manualsplit = Button(self.root, text='SPLIT', command = split, fg = 'white',bg='black').pack()
		
	def setkey(self, *args):
		global key, VK_CODE
		key = VK_CODE[self.keyselect.get()]
		file = open("key.txt", 'w')
		file.write(self.keyselect.get())
		file.close()
		
	def updatepath(self, *args):
		global path 
		path = self.savedir.get()
		file = open("path.txt", 'w')
		file.write(self.savedir.get())
		file.close()


def split():
	# Presses the key set which should split on livesplit
	global key
	win32api.keybd_event(key, 0,0,0) # Push down the key
	sleep(.05) # Wait a little bit
	win32api.keybd_event(key,0 ,win32con.KEYEVENTF_KEYUP ,0) # Let up the key
	if debug == 2:
		print("PRESSED SPLIT KEY")

def levelChange():
	# Returns boolean on whether or not the level has changed
	global lastLevel, levelSearch, path
	
	# Grab the save file if it exists, and if it doesn't go ahead and break out as to not trigger a split
	try:
		saveFile = open(path + "\\VRsuper.hot", "rb") # Open the save file as a byte string
		if debug >= 2:
			print("FOUND ME LUCKY CHARMS")
	except:
		if debug >= 2:
			print("DIDN'T FIND ME LUCKY CHARMS")
		return False
	
	levelResult = levelSearch.search(saveFile.read()) # Look through the file for our level search term
	
	saveFile.close() # Close the save file
	
	currentLevel = levelResult.group(1) # Grab the resulting level name
	
	#if debug == 2:
	#	print("currentLevel:", currentLevel)
	
	# Exceptions (Switch from nothing or switch to beginning)
	if lastLevel == "NOLEVEL" or currentLevel == b'CezaryVR_ReverseFall': # 
		if debug >= 2:
			print("Changed from", lastLevel, "to", currentLevel, "KNOWN EXCEPTION (STOPPED SPLIT)")
		lastLevel = currentLevel # Update our last level
		return False
		
	if lastLevel != currentLevel: # We changed levels
		if debug >= 1:
			print("Changed from", lastLevel, "to", currentLevel)
		lastLevel = currentLevel # Update our last level
		return True
		
	else: # We didn't change levels
		lastLevel = currentLevel # Update our last level
		return False

def finishedGame():
	# Returns boolean on whether or not the game is finished
	
	global lastLevel, finishedSearch, path
	# Grab the save file if it exists, and if it doesn't go ahead and break out as to not trigger a split
	try:
		saveFile = open(path + "\\VRsuper.hot", "rb") # Open the save file as a byte string
	except:
		return False
		
	finishedResult = finishedSearch.search(saveFile.read()) # Look through the file for our finished search term
	
	saveFile.close() # Close the save file
	
	if finishedResult != None:
		finishedGame = finishedResult.group(1) # Grab the resulting finished game state
	else:
		finishedGame = b"false"
		
	if finishedGame == b"true": # We finished the game
		if debug >= 1:
			print("Finished the game!")
		return True
		
	else: # We didn't finish the game
		return False
		
prevFinished = finishedGame() # Need to have previous finished state to be checked so we don't keep pressing the end key

def splitHandle():
	global prevFinished
	finished = finishedGame()
	if(finished and not prevFinished): # Finished state changed from true to false
		if debug >= 1:
			print("split")
		split()
	if(levelChange()):
		if debug >= 1:
			print("split")
		split()
	prevFinished = finished
	app.root.after(100, splitHandle)


app = App()

#def on_closing():
#	run = False
#app.root.protocol("WM_DELETE_WINDOW", on_closing)

app.root.after(100, splitHandle)
app.root.mainloop()

