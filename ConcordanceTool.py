import wx
import wx.dataview
import threading
import os
import glob
import re
import sys

class Concordance(wx.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.InitUI()

	def InitUI(self):
		self.mainframe=wx.Frame(self)

		font1 = wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
		font2 = wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Sans Serrif')
        
		self.panel=wx.Panel(self.mainframe)
		self.panel.SetBackgroundColour("dark grey")
		self.panel1=wx.Panel(self.panel)
		vbox=wx.BoxSizer(wx.VERTICAL)

		self.text=wx.TextCtrl(self.panel1, pos=(450,15), size=(530,360),
			style=wx.TE_MULTILINE
			|wx.TE_RICH2
			|wx.HSCROLL
			|wx.TE_LEFT)
		self.text.SetFont(font1)
		self.text.SetBackgroundColour("grey")

		self.box=wx.StaticBox(self.panel1, pos=(440,0), size=(550,510))
		
		self.entry=wx.SearchCtrl(self.panel1, pos=(450,400), size=(320,-1),
			style=wx.TE_PROCESS_ENTER)
		self.entry.SetFocus()

		self.tree=wx.dataview.TreeListCtrl(self.panel1, 
			pos=(10,12), 
			size=(410,500),
			style=wx.dataview.TL_SINGLE)
		self.tree.AppendColumn("F I L E S")
		self.tree.SetBackgroundColour("grey")

		self.stopButton=wx.Button(self.panel1, label="Stop", pos=(800,400))

		self.label=wx.StaticText(self.panel1, pos=(10, 520))
		self.label.SetForegroundColour("yellow")

		self.label1=wx.StaticText(self.panel1, pos=(200, 520))
		self.label1.SetForegroundColour("khaki")

		self.label.SetFont(font2)
		self.label1.SetFont(font2)

		# self.readonlytext=wx.TextCtrl(self.panel1, pos=(900,310), size=(160,240),
		# 	style=wx.TE_READONLY|wx.TE_MULTILINE)
		# self.readonlytext.SetBackgroundColour((200,200,200))


		vbox.Add(self.panel1, 1, wx.EXPAND|wx.ALL, 15)
		self.panel.SetSizer(vbox)

		self.entry.Bind(wx.EVT_TEXT_ENTER, self.concord_thread)
		self.tree.Bind(wx.dataview.EVT_TREELIST_ITEM_ACTIVATED, self.openfile_thread)
		self.stopButton.Bind(wx.EVT_BUTTON, self.stop1isfalse_thread)
		self.stopButton.Bind(wx.EVT_BUTTON, self.stopisfalse_thread)

		self.SetTitle("ConcFile")
		self.SetSize(600,600)
		self.Centre()
		self.mainframe.Show(True)

	def concord(self):
		n=0
		self.stop=True
		thelist=[]
		pattern=" "+self.entry.GetValue()+" "
		pattern1=re.compile(r'.{30} '+self.entry.GetValue()+r' .{30}', re.DOTALL)
		self.tree.DeleteAllItems()
		self.text.Clear()
		self.path=(os.getcwd())
		for filename in glob.glob(os.path.join(self.path, '*.txt')):
			try:
				file=open(filename, 'r')
				read_file=file.read()
				file.close()
				re_pattern=re.findall(pattern1, read_file)
				if pattern in read_file:
					if self.stop!=False:
						titleonly=re.findall(r'.+\\(.+txt)', filename)
						thefilename=open(filename, 'r')
						read_filename=thefilename.read()
						thefilename.close()
						find_number=re.findall(pattern, read_filename)
						for number in set(find_number):
							thenumber=len(find_number)
							for i in titleonly:
								n+=1
								self.text.AppendText(str(thenumber)+" | "+i+"\n")
								self.label.SetLabel(i)
								thelist.append(thenumber)
								self.root = self.tree.InsertItem(self.tree.GetRootItem(), wx.dataview.TLI_FIRST, i)
				# self.readonlytext.AppendText(pattern+":   "+str(sum(thelist))+"\n")
			except:
				continue
			self.label.SetLabel("Total: "+str(sum(thelist)))

	def concord_thread(self, e):
		a=threading.Thread(target=self.concord)
		a.start()

	def stopisfalse(self):
		self.stop=False

	def stopisfalse_thread(self, e):
		st=threading.Thread(target=self.stopisfalse)
		st.start()

	def openfile(self):
		n=0
		self.stop1=True
		data=self.tree.GetItemText(self.tree.GetSelection())
		file=open(os.getcwd()+data, 'r')
		read_file=file.read()
		file.close()
		find_pattern=re.findall(r'.{30} '+self.entry.GetValue()+r' .{30}', read_file, re.DOTALL)
		self.text.Clear()
		for i in find_pattern:
			if self.stop1!=False:
				n+=1
				editi=re.sub(r'\n+', ' ', i)
				editi1=re.sub(r'\s{4}', '****', editi)
				self.text.AppendText(editi1+"\n")
		self.get_text=self.text.GetValue()
		find_index=re.finditer(self.entry.GetValue(), self.get_text)
		for i in find_index:
			start=i.start()
			end=i.end()
			self.text.SetStyle(start, end, wx.TextAttr("white", "grey"))
		self.label1.SetLabel("Total: "+str(n))

	def openfile_thread(self,e):
		threading.Thread(target=self.openfile).start()

	def stop1isfalse(self):
		self.stop1=False

	def stop1isfalse_thread(self, e):
		st1=threading.Thread(self.stop1isfalse)
		st1.start()

def main():
	app=wx.App()
	Concordance(None)
	app.MainLoop()

if __name__ == '__main__':
	main()
