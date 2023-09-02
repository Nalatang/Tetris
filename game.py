from game_m import Game, Tetrimino, GameData
import win32api
import win32con
import win32gui

import os

class Tetris:
	MoveLeft = 1
	MoveRight = 2
	MoveDown = 3
	HardDrop = 4
	RotateLeft = 5
	RotateRight = 6
	Hold = 7

	def __init__(self):
		self.IsStarted = False
		self.PreviousHold = False
		self.Score = 0

	def Start(self):
		self.IsStarted = True
		self.PreviousHold = False
		self.Score = 0
		Game.Clear()
		Game.CreateTet()
		#self.UpdateWindow()
		#while True:
		#	inputed = input()
		#	KeyEvt = {'a': Tetris.MoveLeft, 'd': Tetris.MoveRight, 's': Tetris.MoveDown, ' ': Tetris.HardDrop, 'z': Tetris.RotateLeft, 'c' : Tetris.RotateRight, 'h': Tetris.Hold, 'q': 1000}
		#	key = 0
		#	try:
		#		key = KeyEvt[inputed]
		#		if key == 1000:
		#			break
		#	except KeyError:
		#		pass
		#	else:
		#		self.DispatchKeyEvt(key)
		#		self.UpdateWindow()

	def KeyEvent(vk):
		KeyEvt = {0x41: Tetris.MoveLeft,0x44: Tetris.MoveRight, 0x53: Tetris.MoveDown, win32con.VK_SPACE: Tetris.HardDrop, 0x5A: Tetris.RotateLeft, 0x58 : Tetris.RotateRight, 0x43: Tetris.Hold, 0x51: 1000}
		key = 0
		try:
			key = KeyEvt[vk]
		except KeyError:
			pass
		else:
			TetrisGame.DispatchKeyEvt(key)
			
	def DispatchKeyEvt(self,key):
		if not self.IsStarted or Game.CurrentTet == Tetrimino.NoneTet:
			return
		Line = 0
		if key == Tetris.MoveLeft:
			Game.MoveLeft()
		elif key == Tetris.MoveRight:
			Game.MoveRight()
		elif key == Tetris.MoveDown:
			Line = Game.MoveDown()
		elif key == Tetris.HardDrop:
			Line = Game.DropDown()
		elif key == Tetris.RotateLeft:
			Game.RotateLeft()
		elif key == Tetris.RotateRight:
			Game.RotateRight()
		elif key == Tetris.Hold and self.PreviousHold == False:
			Game.ChangeHold()
		
		if Line != 0:
			self.PreviousHold = False
			self.Score += Line
	def UpdateWindow(HDC):
		NewBack = [0] * GameData.Width * GameData.Height
		AlertBack = [0] * GameData.Width * 4
		IsAlert = False
		MinHeight = 4
		if Game.CurrentX != -1:
			for x, y in Game.CurrentTet.GetCoord(Game.CurrentDirection, Game.CurrentX, Game.CurrentY):
				NewBack[x + y * GameData.Width] = Game.CurrentTet.Tet
				if y < 4:
					IsAlert = True
					MinHeight = 0
		else:
			IsAlert = True
			MinHeight = 0
			print('GameOver')
		for i in range(GameData.Width * MinHeight, GameData.Width * GameData.Height):
			if NewBack[i] == 0 or (Game.CurrentX == -1):
				NewBack[i] = Game.Back[i]
		
		
		if IsAlert == True:
			NextMinY = Game.NextTet.GetBoundingOff(0)[2]
			for x, y in Game.NextTet.GetCoord(0, 5, -NextMinY):
				AlertBack[x + y * GameData.Width] = 1



		BoxSize = 26
		Left = 200
		Top = 200 - ((BoxSize + 2) * (4 -MinHeight))
		Width = (BoxSize+2) * GameData.Width
		Height = (BoxSize+2) * (GameData.Height - MinHeight)
		Color = 0
		if IsAlert:
			Brush = RawWin32.CreateColor(0x501000)
			RawWin32.DrawFillRect(Left,Top,Left+Width,Top+(BoxSize+2)*4,HDC,Brush)
			RawWin32.ReleaseWin32(Brush)
			Color = 0xFF3705
		else:
			Color = 0xFFFFFF
		Brush = RawWin32.CreateColor(Color)
		RawWin32.DrawBorderRect(Left,Top,Width + Left,Height + Top,HDC,Brush)
		RawWin32.DrawFillRect(Left-152,Top,Left,Top+30,HDC,Brush)
		Pen = RawWin32.CreatePen(Color,2)
		RawWin32.DrawLine(Left-151,Top,Left-151,Top+100,HDC,Pen)
		RawWin32.DrawLine(Left-151,Top+100,Left-131,Top+120,HDC,Pen)
		RawWin32.DrawLine(Left-131,Top+120,Left,Top+120,HDC,Pen)
		RawWin32.ReleaseWin32(Pen)
		Pen = RawWin32.CreatePen(0x000000,3)
		RawWin32.DrawLine(Left-144,Top+5,Left-144,Top+25,HDC,Pen)
		RawWin32.DrawLine(Left-144,Top+15,Left-132,Top+15,HDC,Pen)
		RawWin32.DrawLine(Left-132,Top+5,Left-132,Top+25,HDC,Pen)
		RawWin32.ReleaseWin32(Brush)	
		Brush = RawWin32.CreateColor(0x1b1b1b)
		for x in range(1,GameData.Width):
			RawWin32.DrawBorderRect(Left + (BoxSize + 2) * x, Top + 1, 1 + Left + (BoxSize + 2) * x, Height + Top - 2, HDC, Brush)
		for y in range(1,GameData.Height - MinHeight):
			RawWin32.DrawBorderRect(Left + 1, Top + (BoxSize + 2 ) * y, Left + Width - 2, 1 + Top + (BoxSize + 2) * y, HDC,Brush)
		RawWin32.ReleaseWin32(Brush)
		
		Brushes = []
		for BrushColor in Tetrimino.TetriColor:
			Brushes.append(RawWin32.CreateColor(BrushColor))
		for i in range(GameData.Width * MinHeight,GameData.Width * GameData.Height):
			y = int(i / GameData.Width)
			x = int(i % GameData.Width)

			#print(str(Left+1+(BoxSize+2)*x)+'/'+str(Top+1+(BoxSize+2)*y)+'/'+str(Left+BoxSize+1+(BoxSize+2)*x)+'/'+str(Top+BoxSize+1+(BoxSize+2)*y))
			if NewBack[i] == 0:
				continue
			RawWin32.DrawFillRect(Left+1+(BoxSize+2)*x,Top+1+(BoxSize+2)*(y-MinHeight),Left+BoxSize+1+(BoxSize+2)*x,Top+BoxSize+1+(BoxSize+2)*(y-MinHeight),HDC,Brushes[NewBack[i]])
			
		for Brushes_ in Brushes:
			RawWin32.ReleaseWin32(Brushes_)

		if IsAlert:
			for i in range(0,GameData.Width*4):
				y = int(i / GameData.Width)
				x = int(i % GameData.Width)

				if AlertBack[i] == 1:
					RawWin32.DrawX(Left+1+(BoxSize+2)*x,Top+1+(BoxSize+2)*y,Left+BoxSize+1+(BoxSize+2)*x,Top+BoxSize+1+(BoxSize+2)*y,HDC,0xfda48e)
		
			

class RawWin32:
	def __init__(self):
		self.WindowHandle = 0

	def CreateColor(color):
		ColorRef = (color & 0xFF0000) >> 16 | (color & 0xFF00) | (color & 0xFF) << 16
		return win32gui.CreateSolidBrush(ColorRef)
	def CreatePen(color,width):
		ColorRef = (color & 0xFF0000) >> 16 | (color & 0xFF00) | (color & 0xFF) << 16
		return win32gui.CreatePen(win32con.PS_SOLID,width,ColorRef)

	def ReleaseWin32(obj):
		win32gui.DeleteObject(obj)
	
	def DrawBorderRect(left,top,right,bottom,HDC,Brush):
		win32gui.FrameRect(HDC,(left,top,right,bottom),Brush)
	def DrawFillRect(left,top,right,bottom,HDC,Brush):
		win32gui.FillRect(HDC,(left,top,right,bottom),Brush)
	def DrawX(left,top,right,bottom,HDC,color):
		ColorRef = (color & 0xFF0000) >> 16 | (color & 0xFF00) | (color & 0xFF) << 16
		Pen = win32gui.CreatePen(win32con.PS_SOLID,2,ColorRef)
		OldPen = win32gui.SelectObject(HDC,Pen)
		win32gui.MoveToEx(HDC,left,top)
		win32gui.LineTo(HDC,right,bottom)
		win32gui.MoveToEx(HDC,right,top)
		win32gui.LineTo(HDC,left,bottom)
		win32gui.SelectObject(HDC,OldPen)
		win32gui.DeleteObject(Pen)
	def DrawLine(X1,Y1,X2,Y2,HDC,Pen):
		OldPen = win32gui.SelectObject(HDC,Pen)
		win32gui.MoveToEx(HDC,X1,Y1)
		win32gui.LineTo(HDC,X2,Y2)
		win32gui.SelectObject(HDC,OldPen)

	def WindowProcedure(hWnd, uMsg, wParam, lParam):
		if uMsg == win32con.WM_DESTROY:
			win32gui.PostQuitMessage(1)
		elif uMsg == win32con.WM_PAINT:
			HDC, ps = win32gui.BeginPaint(Win32.WindowHandle)
			
			Tetris.UpdateWindow(HDC)

			win32gui.EndPaint(Win32.WindowHandle,ps)
		elif uMsg == win32con.WM_KEYDOWN:
			Tetris.KeyEvent(wParam)
			win32gui.InvalidateRect(Win32.WindowHandle,None,True)
			win32gui.UpdateWindow(Win32.WindowHandle)
		return win32gui.DefWindowProc(hWnd,uMsg,wParam,lParam)

	def CreateWindow(self):
		hInstance = win32api.GetModuleHandle(None)
		WCW = win32gui.WNDCLASS()
		WCW.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
		WCW.lpfnWndProc = RawWin32.WindowProcedure
		WCW.hInstance = hInstance
		WCW.lpszClassName = "TetrisGame"
		WCW.hbrBackground = win32gui.GetStockObject(win32con.BLACK_BRUSH)

		win32gui.RegisterClass(WCW)
		
		self.WindowHandle = win32gui.CreateWindowEx(0,"TetrisGame","Tetris",win32con.WS_OVERLAPPED | win32con.WS_CAPTION | win32con.WS_MINIMIZEBOX | win32con.WS_SYSMENU | win32con.WS_BORDER,0,0,900,1000,0,0,hInstance,None)		
		win32gui.ShowWindow(self.WindowHandle,win32con.SW_NORMAL)
		win32gui.UpdateWindow(self.WindowHandle)
	
	def ClearMsg(self):
		#WM_QUIT 불가
		#while True:
			#Msg = win32gui.PeekMessage(self.WindowHandle,0,0,win32con.PM_REMOVE)
			#if Msg[1][1] == win32con.WM_QUIT:
			#	print(Msg[1])
			#	return False
			#if Msg[0] == 0:
			#	break
			#print(Msg[1][1])
			#win32gui.TranslateMessage(Msg[1])
			#win32gui.DispatchMessage(Msg[1])
		Quit = win32gui.PumpWaitingMessages()
		if Quit == 1:
			return False
		return True
TetrisGame = Tetris()
TetrisGame.Start()
Win32 = RawWin32()
Win32.CreateWindow()


while True:
	Res = Win32.ClearMsg()
	if Res == False:
		break