import wx
import wx.lib.newevent
from defines import *
from testCase import *

HORIZONTAL_OFFSET = 5
VERTICAL_OFFSET = 5

LISTBOX_X = 10
LISTBOX_Y = 10
LISTBOX_WIDTH = 300
LISTBOX_HEIGHT = 100

BUTTON_CLEAR_X = (LISTBOX_X)
BUTTON_CLEAR_Y = (LISTBOX_Y + LISTBOX_HEIGHT + VERTICAL_OFFSET)

BUTTON_TEST_X = (LISTBOX_X + LISTBOX_WIDTH + HORIZONTAL_OFFSET)
BUTTON_TEST_Y = (LISTBOX_Y)

logUpdateEvent, EVT_UPDATE_LOG = wx.lib.newevent.NewEvent()

class Application(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, -1, 'uZiP HA Controller Test Tool', size=(600, 400))

		mainPanel = wx.Panel(self)
		sizer = wx.BoxSizer(wx.VERTICAL)
		mainPanel.SetSizer(sizer)

		# Setup the menu
		menu = wx.Menu()
		# Add menu item
		menuAbout = menu.Append(wx.ID_ABOUT, "&About uZiP HA Controller Test Tool", "")
		menuExit = menu.Append(wx.ID_EXIT, "&Exit", "")

		# Create the menu bar
		menuBar = wx.MenuBar()
		menuBar.Append(menu, "&File")
		self.SetMenuBar(menuBar)
		
		# Add Listbox to mainPanel
		choices = []
		self.logListBox = wx.ListBox(mainPanel, -1, (LISTBOX_X, LISTBOX_Y), (LISTBOX_WIDTH, LISTBOX_HEIGHT), choices, wx.LB_SINGLE)

		# Add 'Test' Button to mainPanel
		testButton = wx.Button(mainPanel, label="Test", pos=(BUTTON_TEST_X, BUTTON_TEST_Y))

		# Add 'Clear' button to mainPanel
		clearButton = wx.Button(mainPanel, label="Clear", pos=(BUTTON_CLEAR_X, BUTTON_CLEAR_Y))

		# Event
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_BUTTON, self.OnClickTest, testButton)
		self.Bind(wx.EVT_BUTTON, self.OnClickClear, clearButton)
		self.Bind(EVT_UPDATE_LOG, self.OnLogUpdate)

		self.Centre()
		self.Show(True)
	
	def OnAbout(self, event):
		aboutDlg = wx.MessageDialog(self, "uZiP HA Controller Test Tool v" + TOOL_VERSION, "About uZiP HA Controller Test Tool", wx.OK)
		aboutDlg.ShowModal()
		aboutDlg.Destroy()
	
	def OnExit(self, event):
		self.Close()
	
	def OnClickTest(self, event):
		e = logUpdateEvent()
		wx.PostEvent(self, e)
		#runTest(self, event)
	
	def OnClickClear(self, event):
		self.logListBox.Clear()
	
	def OnLogUpdate(self, event):
		#print 'OnLogUpdate'
		self.logListBox.Append("OnLogUpdate")

app = wx.App(False)
Application(None)
app.MainLoop()
