import os
import wx
import wx.lib.newevent
from defines import *

HORIZONTAL_OFFSET = 5
VERTICAL_OFFSET = 5

STATIC_TEXT_HEIGHT = 15

BUTTON_WIDTH = 85
BUTTON_HEIGHT = 22

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

TEXT_FILE_X = (0 + HORIZONTAL_OFFSET)
TEXT_FILE_Y = (0 + VERTICAL_OFFSET)

LISTBOX_FILE_X = (TEXT_FILE_X)
LISTBOX_FILE_Y = (TEXT_FILE_Y + STATIC_TEXT_HEIGHT + VERTICAL_OFFSET)
LISTBOX_FILE_WIDTH = (WINDOW_WIDTH - BUTTON_WIDTH - 30)
LISTBOX_FILE_HEIGHT = 20

BUTTON_OPEN_X = (LISTBOX_FILE_X + LISTBOX_FILE_WIDTH + HORIZONTAL_OFFSET)
BUTTON_OPEN_Y = (LISTBOX_FILE_Y - 1)

BUTTON_CLEAR_X = (TEXT_FILE_X)
BUTTON_CLEAR_Y = (BUTTON_OPEN_Y + BUTTON_HEIGHT + VERTICAL_OFFSET)

BUTTON_SAVE_X = (TEXT_FILE_X + BUTTON_WIDTH + HORIZONTAL_OFFSET)
BUTTON_SAVE_Y = (BUTTON_CLEAR_Y)

LISTBOX_X = (TEXT_FILE_X)
LISTBOX_Y = (BUTTON_CLEAR_Y + BUTTON_HEIGHT + VERTICAL_OFFSET)
LISTBOX_WIDTH = (WINDOW_WIDTH - 30)
LISTBOX_HEIGHT = 250

logUpdateEvent, EVT_UPDATE_LOG = wx.lib.newevent.NewEvent()

class Application(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, -1, 'EEPROM Parser', size=(600, 400))

		mainPanel = wx.Panel(self)
		sizer = wx.BoxSizer(wx.VERTICAL)
		mainPanel.SetSizer(sizer)

		# Setup the menu
		menu = wx.Menu()
		# Add menu item
		menuAbout = menu.Append(wx.ID_ABOUT, "&About EEPROM Parser", "")
		menuExit = menu.Append(wx.ID_EXIT, "&Exit", "")

		# Create the menu bar
		menuBar = wx.MenuBar()
		menuBar.Append(menu, "&File")
		self.SetMenuBar(menuBar)
		
		choices = []
		# Static Text
		textFile = wx.StaticText(mainPanel, -1, "EEPROM Hex file", (TEXT_FILE_X, TEXT_FILE_Y))
		# Add 'Path' list box
		self.filePath = wx.ListBox(mainPanel, -1, (LISTBOX_FILE_X, LISTBOX_FILE_Y), (LISTBOX_FILE_WIDTH, LISTBOX_FILE_HEIGHT), choices, wx.LB_SINGLE)
		# Add 'Open' button to mainPanel
		openButton = wx.Button(mainPanel, label="Open", pos=(BUTTON_OPEN_X, BUTTON_OPEN_Y), size=(BUTTON_WIDTH, BUTTON_HEIGHT))
		# Add 'Clear' button to mainPanel
		clearButton = wx.Button(mainPanel, label="Clear", pos=(BUTTON_CLEAR_X, BUTTON_CLEAR_Y), size=(BUTTON_WIDTH, BUTTON_HEIGHT))
		# Add 'Save' Button to mainPanel
		saveButton = wx.Button(mainPanel, label="Save", pos=(BUTTON_SAVE_X, BUTTON_SAVE_Y), size=(BUTTON_WIDTH, BUTTON_HEIGHT))
		# Add Listbox to mainPanel
		self.logListBox = wx.ListBox(mainPanel, -1, (LISTBOX_X, LISTBOX_Y), (LISTBOX_WIDTH, LISTBOX_HEIGHT), choices, wx.LB_SINGLE)

		# Event
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnDoubleClick, self.logListBox)
		self.Bind(wx.EVT_BUTTON, self.OnClickSave, saveButton)
		self.Bind(wx.EVT_BUTTON, self.OnClickClear, clearButton)
		self.Bind(wx.EVT_BUTTON, self.OnOpen, openButton)
		self.Bind(EVT_UPDATE_LOG, self.OnLogUpdate)

		# Show the window
		self.Centre()
		self.Show(True)
	
	def OnAbout(self, event):
		aboutDlg = wx.MessageDialog(self, "EEPROM Parser v" + TOOL_VERSION, "About EEPROM Parser", wx.OK)
		aboutDlg.ShowModal()
		aboutDlg.Destroy()
	
	def OnExit(self, event):
		self.Close()
	
	def OnClickSave(self, event):
		e = logUpdateEvent()
		wx.PostEvent(self, e)

	def OnClickClear(self, event):
		self.logListBox.Clear()
	
	def OnLogUpdate(self, event):
		self.logListBox.Append("OnLogUpdate")
		
	def OnOpen(self, event):
		wildcard = "HEX file (*.hex)|*.hex"
		dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
		if dialog.ShowModal() == wx.ID_OK:
			self.filePath.Append(dialog.GetPath())
			# Get the filename of the file
			self.filename = dialog.GetFilename()
			# Get the directory of where file is located
			self.dirname = dialog.GetDirectory()
			# Traverse the file directory and find filename in the OS
			f = open(os.path.join(self.dirname, self.filename), 'r')
			lines = f.readlines()
			for line in lines:
				self.logListBox.Append(line)
			f.close
	
	def OnDoubleClick(self, event):
		print 'OnDoubleClick'
	
app = wx.App(False)
Application(None)
app.MainLoop()
