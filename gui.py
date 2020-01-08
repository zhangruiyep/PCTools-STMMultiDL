import os
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import threading
import subprocess


class deviceDownloadFrame(ttk.Frame):
	def __init__(self, master, deviceName):
		ttk.Frame.__init__(self, master)
		self.deviceName = deviceName
		self.grid(sticky=tk.NSEW, padx=5, pady=5)
		self.createWidgets()
		
	
	def createWidgets(self):
		self.Info = ttk.Label(self, text=self.deviceName + "  COM Num:", justify=tk.LEFT)
		self.Info.grid(row=0, sticky=tk.E, padx=5)
		
		self.COMEntry = ttk.Entry(self, width = 5)
		self.COMEntry.grid(row=0, column=1, sticky=tk.W, padx=5)
		
		self.btnStart = ttk.Button(self, text="Start", command=self.startDownload)
		self.btnStart.grid(row=0, column=2, padx=5)
		
		self.outputText = tk.Text(self, width = 60, height = 3)
		self.outputText.grid(row=1, columnspan = 3, padx=5, pady =5)
		self.outputText["state"] = "disabled"
		
	def startDownload(self):
		self.thread = threading.Thread(target=self.devDownFunc, name="Thread-"+self.deviceName, args=(self.COMEntry.get().strip(),))
		self.thread.start()
		self.btnStart["state"] = "disable"
		#self.btnStop["state"] = "normal"
		#self.devDownFunc(self.COMEntry.get().strip())
				
			
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
		#cmdStr = "ping 1.2.3.4" #test long time exec cmd
		print(cmdStr)
		#p = os.popen(cmdStr, "r")
		self.outputText["state"] = "normal"
		p = subprocess.Popen(cmdStr, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
		for line in p.stdout:
			strLine = line.decode("gb2312")
			#print(line.decode("utf-8"))
			self.outputText.insert(tk.END, strLine)
		#for line in p.readlines():
		#	print(line)
		#	if line.find("Press any key to continue ...") != -1:
		#		p.close()
		print(p.returncode)
		self.outputText["state"] = "disabled"
		print(com + "done")
		self.btnStart["state"] = "normal"
		self.master.master.startAllBtnEnableChk()
		

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
		
		self.startAllBtn = ttk.Button(self.devicesFrame, text="Start All", command=self.startAll, width=10)
		self.startAllBtn.grid(row = 5, pady = 5)
		
	def chooseImageFile(self):
		filename = filedialog.askopenfilename()
		if (filename != None) and (filename != ""):
			self.imageFilePathEntry.delete(0, tk.END)
			self.imageFilePathEntry.insert(0, os.path.realpath(filename))
	
	def startAll(self):
		self.startAllBtn["state"] = "disabled"
		self.device1.startDownload()
		self.device2.startDownload()
		self.device3.startDownload()
		self.device4.startDownload()
		
	def startAllBtnEnableChk(self):
		if self.device1.btnStart["state"] == "disabled":
			self.startAllBtn["state"] = "disabled"
		elif self.device2.btnStart["state"] == "disabled":
			self.startAllBtn["state"] = "disabled"
		elif self.device3.btnStart["state"] == "disabled":
			self.startAllBtn["state"] = "disabled"
		elif self.device4.btnStart["state"] == "disabled":
			self.startAllBtn["state"] = "disabled"
		else:
			self.startAllBtn["state"] = "normal"

app = Application() 
app.master.title('STM Multi Download') 
app.master.rowconfigure(0, weight=1)
app.master.columnconfigure(0, weight=1)
app.mainloop() 