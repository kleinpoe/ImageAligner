import csv
import os
import numpy as np
from PIL import Image
import glob


# Change Here:
directory = r'C:\Users\klein\Desktop\22041012\stacklongsmolshroom'
alignmentPointsFilename = 'AlignmentPoints.csv'


class Point:
    def __init__(self,x,y):
        self.X = x
        self.Y = y
        
    def Round(self) -> "Point":
        self.X = round(self.X)
        self.Y = round(self.Y)
        return self
    
    def Ceiling(self)-> "Point":
        self.X = np.ceil(self.X)
        self.Y = np.ceil(self.Y)
        return self
    
    def __add__(self, o:"Point")->"Point":
        return Point(self.X + o.X, self.Y + o.Y)
    
    def __sub__(self, o:"Point")->"Point":
        return Point(self.X - o.X, self.Y - o.Y)
        
    def __repr__(self):
        return f"Point(X={self.X}, Y={self.Y})"
    
class Rectangle:
    def __init__(self,top,left,bottom,right):
        self.Top = np.min([top,bottom])
        self.Left = np.min([ left,right])
        self.Bottom = np.max([bottom,top])
        self.Right = np.max([right,left])
        self.Width = self.Right - self.Left
        self.Height = self.Bottom - self.Top
        
    def __repr__(self):
        return f"Rectangle(T={self.Top}, L={self.Left}, B={self.Bottom}, R={self.Right}, Width={self.Width}, Height={self.Height})"
        
class AlignmentPoint:
    def __init__(self, point: Point, sliceNumber: int):
        self.Point = point 
        self.SliceNumber = sliceNumber

    def __repr__(self):
        return f"AlignmentPoint({self.Point}, Slice={self.SliceNumber})"

def import_csv(file_path) -> list[AlignmentPoint]:
    with open(file_path, mode='r', newline='') as csvfile:
        def parseLine(line: str) -> AlignmentPoint:
            return AlignmentPoint(Point(float(line['X']), float(line['Y'])), int(line['Slice']))
        points = [parseLine(line) for line in csv.DictReader(csvfile)]
        points.sort(key=lambda x: x.SliceNumber)
        return points
    
def calculateCenter(points: list[AlignmentPoint]) -> Point:
    meanX = np.mean([x.Point.X for x in points])
    meanY = np.mean([x.Point.Y for x in points])
    return Point(meanX,meanY)

def calculateShiftRectangle(points: list[AlignmentPoint]) -> Rectangle:
    minX = np.min([x.Point.X for x in points])
    maxX = np.max([x.Point.X for x in points])
    minY = np.min([x.Point.Y for x in points])
    maxY = np.max([x.Point.Y for x in points])
    return Rectangle(top=minY, left=minX, bottom=maxY, right=maxX)

def calculatePadding(shiftRectangle:Rectangle) -> Point:
    return Point(shiftRectangle.Width/2, shiftRectangle.Height/2).Ceiling()

def calculateShifts(points: list[AlignmentPoint], centerPoint: Point) -> list[AlignmentPoint]:
    shifts = [AlignmentPoint( centerPoint -x.Point  ,x.SliceNumber) for x in points]
    return shifts

def importImages(directory:str)->list[Image.Image]:
    files = glob.glob(os.path.join(directory,"*.jpg"))
    return [Image.open(file) for file in files]
    

def createShiftedImage(originalImage: Image, padding:Point, offset:Point, outputPath: str):
    new_width = int(originalImage.width + padding.X * 2)
    new_height = int(originalImage.height + padding.Y * 2)

    black_image = Image.new('RGB', (new_width, new_height), (0, 0, 0))
    effectiveOffset = padding + offset
    black_image.paste(originalImage, (int(effectiveOffset.X), int(effectiveOffset.Y)))
    black_image.save(outputPath)


alignmentPointsFilepath = os.path.join(directory,alignmentPointsFilename)
alignmentPoints = import_csv(alignmentPointsFilepath)
center = calculateCenter(alignmentPoints)
shiftRectangle = calculateShiftRectangle(alignmentPoints)
padding = calculatePadding(shiftRectangle)
shifts = calculateShifts(alignmentPoints,center)
images = importImages(directory)

print(f"Loaded {len(images)} Images. Found shifts with magnitude ({shiftRectangle.Width},{shiftRectangle.Height}). Enlarging image by ({padding.X*2,padding.Y*2}).")

for i in range(0,len(images)):
    shift = shifts[i]
    image = images[i]
    outputDirectory = os.path.join(directory,"Aligned")
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)
    outputFilename = f'Aligned_{i}.jpg'
    outputFilepath = os.path.join(outputDirectory,outputFilename)
    print(f'{i}: Saving Image {outputFilepath} Shift={shift}')
    createShiftedImage(image,padding,shift.Point,outputFilepath)

