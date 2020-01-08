import os
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import threading


class deviceDownloadFrame(ttk.Frame):
	def __init__(self, master, deviceName):
		ttk.Frame.__init__(self, master)
		self.deviceName = deviceName
		self.grid(sticky=tk.NSEW, padx=5, pady=5)
		self.createWidgets()
		
	
	def createWidgets(self):
		self.Info = ttk.Label(self, text=self.deviceName + "  COM Num:", justify=tk.LEFT)
		self.Info.grid(row=0, sticky=tk.W, padx=5)
		
		self.COMEntry = ttk.Entry(self, width = 5)
		self.COMEntry.grid(row=0, column=1, padx=5)
		
		self.btnStart = ttk.Button(self, text="Start", command=self.startDownload)
		self.btnStart.grid(row=0, column=2, padx=5)

#		self.btnStop = ttk.Button(self, text="Stop", command=self.stopDownload)
#		self.btnStop.grid(row=0, column=2, padx=5)
#		self.btnStop["state"] = "disable"
	
	def startDownload(self):
		self.thread = threading.Thread(target=self.devDownFunc, name="Thread-"+self.deviceName, args=(self.COMEntry.get().strip(),))
		self.thread.start()
		self.btnStart["state"] = "disable"
		#self.btnStop["state"] = "normal"
			
	def devDownFunc(self, com):
		filename = self.master.master.imageFilePathEntry.get().strip()
		need_erase = self.master.master.optionErase
		need_verify = self.master.master.optionVerify
		print(com)
		cmdStr = "BIN\STMFlashLoader.exe -c --pn " + com + " --br 115200 -i STM32F0_3x_16K -d --fn " + filename
		if (need_verify):
			cmdStr += " --v"
		if (need_erase):
			cmdStr += " -e --all"
		print(cmdStr)
		p = os.popen(cmdStr, "r")
		for line in p.readlines():
			print(line)
			if line.find("Press any key to continue ...") != -1:
				p.close()
		print(com + "done")
		self.btnStart["state"] = "normal"
		#self.btnStop["state"] = "disable"

#	def stopDownload(self):
#		self.thread = threading.Thread(target=self.devDownFunc, name="Thread-"+self.deviceName, args=(self.COMEntry.get().strip(),))
#		self.thread.start()
#		self.btnStart["state"] = "disable"
#		self.btnStop["state"] = "normal"
		

class Application(ttk.Frame):
	def __init__(self, master=None):
		ttk.Frame.__init__(self, master)
		self.grid(sticky=tk.NSEW, padx=10, pady=10)
		self.createWidgets()

	def createWidgets(self):
		self.fileFrame = ttk.Frame(self)
		self.fileFrame.grid(sticky=tk.NSEW, pady=5)

		self.Info = ttk.Label(self.fileFrame, text="MCU Image File:", justify=tk.LEFT)
		self.Info.grid(row=0, sticky=tk.W, padx=5)
		
		self.imageFilePathEntry = ttk.Entry(self.fileFrame, width = 40)
		self.imageFilePathEntry.grid(row=0, column=1, padx=5)
		
		self.getFileBtn = ttk.Button(self.fileFrame, text="Choose", command=self.chooseImageFile, width=10)
		self.getFileBtn.grid(row=0, column=2, padx=5)
		
		self.optionFrame = ttk.Frame(self)
		self.optionFrame.grid(sticky=tk.NSEW, pady=5)
		
		self.optionErase = tk.IntVar()
		self.chkBtnErase = ttk.Checkbutton(self.optionFrame, text="Erase All", variable = self.optionErase)
		self.chkBtnErase.grid(sticky=tk.W, padx=5)
		
		self.optionVerify = tk.IntVar()
		self.chkBtnVerify = ttk.Checkbutton(self.optionFrame, text="Verify", variable = self.optionVerify)
		self.chkBtnVerify.grid(sticky=tk.W, padx=5)
		
		self.devicesFrame = ttk.Frame(self)
		self.devicesFrame.grid(sticky=tk.NSEW, pady=5)
		
		self.device1 = deviceDownloadFrame(self.devicesFrame, "Device1")
		self.device2 = deviceDownloadFrame(self.devicesFrame, "Device2")
		self.device3 = deviceDownloadFrame(self.devicesFrame, "Device3")
		self.device4 = deviceDownloadFrame(self.devicesFrame, "Device4")
		
	def chooseImageFile(self):
		filename = filedialog.askopenfilename()
		if (filename != None) and (filename != ""):
			self.imageFilePathEntry.delete(0, tk.END)
			self.imageFilePathEntry.insert(0, os.path.realpath(filename))
		
	

app = Application() 
app.master.title('STM Multi Download') 
app.master.rowconfigure(0, weight=1)
app.master.columnconfigure(0, weight=1)
app.mainloop() 