import random

class Tetrimino:
	NoneTet = 0
	ITet = 1
	LTet = 2
	JTet = 3
	TTet = 4
	OTet = 5
	STet = 6
	ZTet = 7


	TetriColor = [0, 0x01EDFA, 0xFFC82E, 0x2E2E84, 0xDD0AB2, 0xFEFB34, 0x53DA3F, 0xEA141C]
	TetriData = (
		((0,0),(0,0),(0,0),(0,0)),
		((0,-1),(0,0),(0,1),(0,2)),
		((0,-1),(0,0),(0,1),(1,1)),
		((0,-1),(0,0),(0,1),(-1,1)),
		((0,-1),(0,0),(0,1),(1,0)),
		((0,0),(0,-1),(1,0),(1,-1)),
		((0,0),(0,-1),(-1,0),(1,-1)),
		((0,0),(0,-1),(1,0),(-1,-1))
	)



	def __init__(self, tet = 0):
		self.Tet = tet

	def GetRotateOff(self, direction):
		CurrentTet = Tetrimino.TetriData[self.Tet]
		#print(str(self.Tet)+'/'+str(CurrentTet))
		if direction == 0 or self.Tet == Tetrimino.OTet:
			return ((x,y) for x, y in CurrentTet)
		if direction == 1:
			return ((-y, x) for x, y in CurrentTet)
		if direction == 2:
			if self.Tet in (Tetrimino.ITet, Tetrimino.ZTet, Tetrimino.STet):
				return ((x, y) for x, y in CurrentTet)
			else:
				return ((-x, -y) for x, y in CurrentTet)
		if direction == 3:
			if self.Tet in (Tetrimino.ITet, Tetrimino.ZTet, Tetrimino.STet):
				return ((-y, x) for x, y in CurrentTet)
			else:
				return ((y, -x) for x, y in CurrentTet)
		
	def GetCoord(self, direction, x, y):
		return ((x + xx, y + yy) for xx, yy in self.GetRotateOff(direction))

	def GetBoundingOff(self, direction):
		CurOff = self.GetRotateOff(direction)
		minX, maxX, minY, maxY = 0,0,0,0
		for x, y in CurOff:
			#print(str(x)+'/'+str(y)+'\n')
			if minX > x:
				minX = x
			if maxX < x:
				maxX = x
			if minY > y:
				minY = y
			if maxY < y:
				maxY = y
		return (minX, maxX, minY, maxY)


class GameData:
	Width = 10
	Height = 22 + 4

	def __init__(self):
		self.Back = [0] * GameData.Width * GameData.Height
		self.CurrentX = -1
		self.CurrentY = -1
		self.CurrentDirection = 0
		self.CurrentTet = Tetrimino()
		self.NextTet = [Tetrimino(random.randint(1,7)),Tetrimino(random.randint(1,7)),Tetrimino(random.randint(1,7)),Tetrimino(random.randint(1,7)),Tetrimino(random.randint(1,7))]
		self.HoldTet = Tetrimino()
		
		#self.TetStat = [0] * 8

	def GetBackData(self):
		return self.Back[:]
	def GetValue(self, x, y):
		return self.Back[x + y * GameData.Width]
	def GetCurrentTetCoord(self):
		return self.CurrentTet.GetCoord(self.CurrentDirection, self.CurrentX, self.CurrentY)
	def CreateTet(self):
		minX, maxX, minY, maxY = self.NextTet[0].GetBoundingOff(0)
		print('['+str(minY)+'/'+str(maxY)+']')
		Result = False
		CurY = 0
		self.CurrentTet = self.NextTet[0]
		for OkY in range(-minY, -minY + 1 + 4):
			if self.TryMove(0,5,OkY):
				CurY = OkY
				Result = True
			else:
				break
		if Result == True:
			self.CurrentX = 5
			self.CurrentY = CurY
			self.CurrentDirection = 0
			self.NextTet[4] = Tetrimino(random.randint(1,7))
		else:
			self.CurrentShape = Tetrimino()
			self.CurrentX = -1
			self.CurrentY = -1
			self.CurrentDirection = 0
			Result = False
		#self.TetStat[self.CurrentTet.tet] += 1
		return Result
	def ChangeHold(self):
		HoldTet = self.HoldTet
		self.HoldTet = self.CurrentTet
		if HoldTet.Tet == 0:
			HoldTet = self.NextTet[0]
		self.NextTet[0] = HoldTet
		self.CreateTet()
	def TryMove(self, direction, x, y):
		return self.TryMoveTet(self.CurrentTet, direction, x, y)
	def TryMoveTet(self, tet, direction, x, y):
		for x, y in tet.GetCoord(direction, x, y):
			if x >= GameData.Width or x < 0 or y >= GameData.Height or y < 0:
				return False
			if self.Back[x + y * GameData.Width] > 0:
				return False
		return True
	def MoveDown(self):
		Line = 0
		if self.TryMove(self.CurrentDirection, self.CurrentX, self.CurrentY + 1):
			self.CurrentY += 1
		else:
			self.Merge()
			line = self.RemoveFullLine()
			self.CreateTet()
		return Line
	def DropDown(self):
		while self.TryMove(self.CurrentDirection, self.CurrentX, self.CurrentY + 1):
			self.CurrentY += 1
		self.Merge()
		Line = self.RemoveFullLine()
		self.CreateTet()
		return Line
	def MoveLeft(self):
		if self.TryMove(self.CurrentDirection, self.CurrentX - 1, self.CurrentY):
			self.CurrentX -= 1
	def MoveRight(self):
		if self.TryMove(self.CurrentDirection, self.CurrentX + 1, self.CurrentY):
			self.CurrentX += 1
	def RotateLeft(self):
		A,B,MinY,MaxY = self.CurrentTet.GetBoundingOff((self.CurrentDirection - 1) % 4)
		for CurY in range(0,-MinY+MaxY+2):
			if self.TryMove((self.CurrentDirection - 1) % 4, self.CurrentX, self.CurrentY-CurY):
				self.CurrentDirection = (self.CurrentDirection - 1) % 4
				self.CurrentY -= CurY
				break
	def RotateRight(self):
		A,B,MinY,MaxY = self.CurrentTet.GetBoundingOff((self.CurrentDirection + 1) % 4)
		for CurY in range(0,-MinY+MaxY+2):
			#print(str(MinY)+'/'+str(MaxY)+'/'+str(CurY))
			if self.TryMove((self.CurrentDirection + 1) % 4, self.CurrentX, self.CurrentY-CurY):
				self.CurrentDirection = (self.CurrentDirection + 1) % 4
				self.CurrentY -= CurY
				break
	def RemoveFullLine(self):
		NewBack = [0] * GameData.Width * GameData.Height
		NewY = GameData.Height - 1
		Line = 0
		for y in range(GameData.Height - 1, -1, -1):
			BlockCount = sum([1 if self.Back[x + y * GameData.Width] > 0 else 0 for x in range(GameData.Width)])
			if BlockCount < GameData.Width:
				for x in range(GameData.Width):
					NewBack[x + NewY * GameData.Width] = self.Back[x + y * GameData.Width]
				NewY -= 1
			else:
				Line += 1
		if Line > 0:
			self.Back = NewBack
		return Line
	def Merge(self):
		for x, y in self.CurrentTet.GetCoord(self.CurrentDirection, self.CurrentX, self.CurrentY):
			self.Back[x + y * GameData.Width] = self.CurrentTet.Tet
		self.CurrentX = -1
		self.CurrentY = -1
		self.CurrentDirection = 0
		self.CurrentTet = Tetrimino()
	def Clear(self):
		self.CurrentX = -1
		self.CurrentY = -1
		self.CurrentDirection = 0
		self.CurrentShape = Tetrimino()
		self.Back = [0] * GameData.Width * GameData.Height

Game = GameData()

		