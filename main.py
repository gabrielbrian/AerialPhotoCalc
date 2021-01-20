
from math import acos, degrees
import math

class Lens:
    def __init__(self,mm , x_fov, y_fov):
        self.mm = mm
        self.x_fov = x_fov
        self.y_fov = y_fov 

    def get_degx(self):
    	return self.x_fov / 2

    def get_degy(self):
    	return self.y_fov / 2
    	

lens200 = Lens(200,10.3,6.9)
lens300 = Lens(300,6.9,4.6)
lens600 = Lens(600,3.4,2.3)
lens800 = Lens(800,2.6,1.7)
lens1700 = Lens(1700,1.23,0.8)

SelectedLens = int(input("what lens was used ? (200,300,600,800,1700) : "))
if SelectedLens == 1700:
	SelectedLens_y = lens1700.get_degy()
	SelectedLens_x = lens1700.get_degx()
	SelectedLens_mm = lens1700.mm
	print("You picked 1700mm",", x_fov = ",lens1700.x_fov,", y_fov =",lens1700.y_fov)
elif SelectedLens == 800:
	SelectedLens_y = lens800.get_degy()
	SelectedLens_x = lens800.get_degx()
	SelectedLens_mm = lens800.mm
	print("You picked 800mm",", x_fov = ",lens800.x_fov,", y_fov =",lens800.y_fov)
elif SelectedLens == 600:
	SelectedLens_y = lens600.get_degy()
	SelectedLens_x = lens600.get_degx()
	SelectedLens_mm = lens600.mm
	print("You picked 600mm",", x_fov = ",lens600.x_fov,", y_fov =",lens600.y_fov)
elif SelectedLens == 300:
	SelectedLens_y = lens300.get_degy()
	SelectedLens_x = lens300.get_degx()
	SelectedLens_mm = lens300.mm
	print("You picked 300mm",", x_fov = ",lens300.x_fov,", y_fov =",lens300.y_fov)
elif SelectedLens == 200:
	SelectedLens_y = lens200.get_degy()
	SelectedLens_x = lens200.get_degx()
	SelectedLens_mm = lens200.mm
	print("You picked 300mm",", x_fov =",lens300.x_fov,", y_fov =",lens300.y_fov)
else:
	raise SystemExit

class Camera:
	def __init__(self, x_res, y_res):
		self.x_res = x_res
		self.y_res = y_res
	
	def get_res(self):
		return self.x_res * self.y_res	

CamD850 = Camera(8256,5504)
CamD5 = Camera(5588,3712)
CamSony7= Camera(9504,6336)


SelectedCam = input("what Camera was used ? (D5,D850) : ")
if SelectedCam == "D5":
	SelectedCam = CamD5.x_res
	print("You picked D5 , RES : ", CamD5.get_res())
elif SelectedCam == "D850":
	SelectedCam = CamD850.x_res
	print("You picked D850 , RES :  ",CamD850.get_res())
elif SelectedCam == "R7":
	SelectedCam = CamSony7.x_res
	print("You picked SONY R7 , RES :  ",CamSony7.get_res())
else:
	raise SystemExit

class Geo:
	def __init__(self, distance, altitude):
		self.distance = distance
		self.altitude = altitude

	def get_ops(self):
		return math.sqrt(float(self.distance**2 + self.altitude**2))


camTriagle = Geo(int(input("What was the distance from the target ? (IN METERS) : ")),int(input("What was the flight altitude ?(IN METERS) : ")))


angleFromPlane = math.asin(camTriagle.distance/camTriagle.get_ops()) * 180/math.pi
angleOnGround = math.asin(camTriagle.altitude/camTriagle.get_ops()) * 180/math.pi
C = 180 - angleFromPlane - angleOnGround


def lenstriangle ():
	closeBorderAng = angleFromPlane - SelectedLens_y
	farBorderAng = angleFromPlane + SelectedLens_y
	C2 = 90 - closeBorderAng
   
	closeBorder = math.tan(math.radians(closeBorderAng))
	closeBorder_Dis = closeBorder * camTriagle.altitude
	closeBorder_Half = closeBorder_Dis * math.tan(math.radians(SelectedLens_x))
	closeBorder_res = (closeBorder_Half * 2 / SelectedCam)

	farBorder = math.tan(math.radians(farBorderAng))
	farBorder_Dis = farBorder * camTriagle.altitude
	farBorder_Half = farBorder_Dis * math.tan(math.radians(SelectedLens_x))
	farBorder_res = (farBorder_Half * 2 / SelectedCam)

	height = farBorder_Dis - closeBorder_Dis
	squaremeter = ((farBorder_Half + closeBorder_Half) * height)
	avg_ppm = (farBorder_res + 	closeBorder_res) / 2
	
	print("\n")
	print(" distance to target ", camTriagle.get_ops())
	print(" ground target angle : ", angleOnGround),
	print(" Camera angle from plane : ",angleFromPlane)
	print(" pixel per meter bottom : ",closeBorder_res)
	print(" pixel per meter top : ", farBorder_res)
	print(" avg pixel per meter : ",(farBorder_res + closeBorder_res) / 2 )
	print(" height : ", height)
	print(" top length : ", farBorder_Half* 2)
	print(" bottom length : ", closeBorder_Half * 2)
	print("	squaremeter : ", squaremeter)
	

lenstriangle()

