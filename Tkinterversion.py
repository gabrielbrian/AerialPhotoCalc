import tkinter as tk
import csv
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

class Camera:
	def __init__(self, x_res, y_res):
		self.x_res = x_res
		self.y_res = y_res
	
	def get_res(self):
		return self.x_res * self.y_res	

"""class Geo:
	def __init__(self, distance, altitude):
		self.distance = distance
		self.altitude = altitude

	def get_ops(self):
		return math.sqrt(float(self.distance**2 + self.altitude**2))"""

lens200 = Lens(200,10.3,6.9)
lens300 = Lens(300,6.9,4.6)
lens600 = Lens(600,3.4,2.3)
lens800 = Lens(800,2.6,1.7)
lens1700 = Lens(1700,1.23,0.8)

CamD850 = Camera(8256,5504)
CamD5 = Camera(5588,3712)
Sony_Ar7= Camera(9504,6336)

root = tk.Tk()

def Get():
	text_box.delete(1.0, "end-1c")
	Currentcam = cam_var.get()
	if Currentcam == "D5":
		Currentcam = CamD5.x_res
	elif Currentcam == "D850":
		Currentcam = CamD850.x_res
	elif Currentcam == "Sony_Ar7":
		Currentcam = Sony_Ar7.x_res
	else:
		raise SystemExit
	
	Currnetlens = lens_var.get()
	
	if Currnetlens == "1700MM":
		Currnetlens_y = lens1700.get_degy()
		Currnetlens_x = lens1700.get_degx()
		Currnetlens_mm = lens1700.mm
	elif Currnetlens == "800MM":
		Currnetlens_y = lens800.get_degy()
		Currnetlens_x = lens800.get_degx()
		Currnetlens_mm = lens800.mm
	elif Currnetlens == "600MM":
		Currnetlens_y = lens600.get_degy()
		Currnetlens_x = lens600.get_degx()
		Currnetlens_mm = lens600.mm
	elif Currnetlens == "300MM":
		Currnetlens_y = lens300.get_degy()
		Currnetlens_x = lens300.get_degx()
		Currnetlens_mm = lens300.mm
	elif Currnetlens == "200MM":
		Currnetlens_y = lens200.get_degy()
		Currnetlens_x = lens200.get_degx()
		Currnetlens_mm = lens200.mm
	else:
		raise SystemExit

	Currentdis = int(distance_entry.get())
	Currentalt = int(altitude_entry.get())
	camTriagle = math.sqrt(float(Currentdis**2 + Currentalt**2))

	angleFromPlane = math.asin(Currentdis/camTriagle) * 180/math.pi
	angleOnGround = math.asin(Currentalt/camTriagle) * 180/math.pi
	C = 180 - angleFromPlane - angleOnGround

	closeBorderAng = angleFromPlane - Currnetlens_y
	farBorderAng = angleFromPlane + Currnetlens_y
	C2 = 90 - closeBorderAng
   
	closeBorder = math.tan(math.radians(closeBorderAng))
	closeBorder_Dis = closeBorder * Currentalt
	closeBorder_Half = closeBorder_Dis * math.tan(math.radians(Currnetlens_x))
	closeBorder_res = (closeBorder_Half * 2 / Currentcam)

	farBorder = math.tan(math.radians(farBorderAng))
	farBorder_Dis = farBorder * Currentalt
	farBorder_Half = farBorder_Dis * math.tan(math.radians(Currnetlens_x))
	farBorder_res = (farBorder_Half * 2 / Currentcam)

	height = farBorder_Dis - closeBorder_Dis
	squaremeter = ((farBorder_Half + closeBorder_Half) * height)
	avg_ppm = (farBorder_res + 	closeBorder_res) / 2

	Distancetotarget = " distance to target : " + str("{:.2f}".format(camTriagle))
	Groundangle = " ground target angle : " + str("{:.2f}".format(angleOnGround))
	Planeangle = " Camera angle from plane : " + str("{:.2f}".format(angleFromPlane))
	Farres =  " pixel per meter top : " + str("{:.2f}".format(farBorder_res*100))
	Closeres = " pixel per meter bottom : " + str("{:.2f}".format(closeBorder_res*100))
	Ppmavg = " avg pixel per meter : " + str("{:.2f}".format(avg_ppm*100))
	Height = " height : " + str("{:.2f}".format(height))
	Farlength = " top length : " + str("{:.2f}".format(farBorder_Half* 2))
	Closelength = " bottom length : "+ str("{:.2f}".format(closeBorder_Half * 2))
	Sqm = " squaremeter : " + str("{:.2f}".format(squaremeter))
	Avghl = " avg height and length : " + str("{:.2f}".format(math.sqrt(squaremeter)))

	text_box.insert('1.0',Distancetotarget + '\n')
	text_box.insert('2.0',Groundangle + '\n')
	text_box.insert('3.0',Planeangle + '\n')
	text_box.insert('4.0',Farres + '\n')
	text_box.insert('5.0',Closeres + '\n')
	text_box.insert('6.0',Ppmavg + '\n')
	text_box.insert('7.0',Height + '\n')
	text_box.insert('8.0',Farlength + '\n')
	text_box.insert('9.0',Closelength + '\n')
	text_box.insert('10.0',Sqm + '\n' )
	text_box.insert('11.0',Avghl+  '\n')

root.title('PhotoCalculator')
root.geometry("400x400") 
root.resizable(0, 0)

background_image = tk.PhotoImage(file='plane.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

distance = tk.Label(root,font=("Courier", 8),text="Distance Mtr",bd = 2)
distance.place(x=200,y=20)
distance_entry = tk.Entry(root,bd = 2)
distance_entry.place(x=300,y=20,width=50)

altitude = tk.Label(root,font=("Courier", 8),text="Altitude Mtr",bd = 2)
altitude.place(x=200,y=50)
altitude_entry = tk.Entry(root,bd = 2)
altitude_entry.place(x=300,y=50,width=50)

CamList = ["D5","D850","Sony_Ar7",] 
cam_var = tk.StringVar(root)
cam_var.set(CamList[0])

CamMenu = tk.OptionMenu(root,cam_var,*CamList)
CamMenu.config(width=8,height=1,font=("Courier", 10))
CamMenu.place(x=40,y=10)

LensList = ["200MM","300MM","600MM","800MM","1700MM"] 
lens_var = tk.StringVar(root)
lens_var.set(LensList[0])

LensMenu = tk.OptionMenu(root,lens_var,*LensList)
LensMenu.config(width=8,height=1,font=("Courier", 10))
LensMenu.place(x=40,y= 50)

Calculate = tk.Button(root, text = "Calculate",font=("Courier", 14,"bold"), command = Get)
Calculate.place(width="100px",x = 130 , y = 100)

text_box = tk.Text(root, width = 40, height = 14)
text_box.place(x=40,y=150)

root.mainloop()








