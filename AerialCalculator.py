import tkinter as tk
import csv
from math import acos, degrees
import math
import os
from exif import Image

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

	Distancetotarget = " Distance to target : " + str("{:.2f}".format(camTriagle))
	Groundangle = " Ground target angle : " + str("{:.2f}".format(angleOnGround))
	Planeangle = " Camera angle from plane : " + str("{:.2f}".format(angleFromPlane))
	Farres =  " Pixel per CM top : " + str("{:.2f}".format(farBorder_res*100))
	Closeres = " Pixel per CM bottom : " + str("{:.2f}".format(closeBorder_res*100))
	Ppmavg = " Avg pixel per meter : " + str("{:.2f}".format(avg_ppm*100))
	Height = " Height : " + str("{:.2f}".format(height))
	Farlength = " Top length : " + str("{:.2f}".format(farBorder_Half* 2))
	Closelength = " Bottom length : "+ str("{:.2f}".format(closeBorder_Half * 2))
	Sqm = " Squaremeter : " + str("{:.2f}".format(squaremeter))
	Avghl = " Avg height and length : " + str("{:.2f}".format(math.sqrt(squaremeter)))

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
	
	with open('Report.csv', 'a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow([Distancetotarget])
		writer.writerow([Groundangle])
		writer.writerow([Planeangle])
		writer.writerow([Farres])
		writer.writerow([Closeres])
		writer.writerow([Ppmavg])
		writer.writerow([Height])
		writer.writerow([Farlength])
		writer.writerow([Closelength])
		writer.writerow([Sqm])
		writer.writerow([Avghl])
		writer.writerow(["------------------------------------------------------- "])


def getLoc():
	text_box2.delete(1.0, "end-1c")
	Dir = Picfolder_entry.get()
	text_box2.insert('1.0',"       -------coordinates-------")
	def dms_to_dd(gps_coords, gps_coords_ref):
	    d, m, s =  gps_coords
	    dd = d + m / 60 + s / 3600
	    if gps_coords_ref.upper() in ('S', 'W'):
	        return -dd
	    elif gps_coords_ref.upper() in ('N', 'E'):
	        return dd
	    else:
	        raise RuntimeError('Incorrect gps_coords_ref {}'.format(gps_coords_ref))
	
	Coordinate_List = []

	for pic in os.listdir(Dir):
	    fullpath = os.path.join(Dir,pic)       
	    with open(fullpath, 'rb') as image_file:
	        my_image = Image(image_file)
	                
	        latitude_final = dms_to_dd(my_image.gps_latitude, my_image.gps_latitude_ref)
	        longitude_final = dms_to_dd(my_image.gps_longitude, my_image.gps_longitude_ref)
	                
	        complete = latitude_final,longitude_final
	
	        text_box2.insert('end','\n')
	        text_box2.insert('end',complete)
	        Coordinate_List.append(complete)
			
	with open('coordinates.csv', 'a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["------------------------------------------------------- "])
		for i in range(len(Coordinate_List)):
			writer.writerow([Coordinate_List[i]])


def getalt():
	text_box2.delete(1.0, "end-1c")
	Dir = Picfolder_entry.get()
	text_box2.insert('1.0',"       -------altitude-------")
	for pic in os.listdir(Dir):
	    fullpath = os.path.join(Dir,pic)       
	    with open(fullpath, 'rb') as image_file:
	        my_image = Image(image_file)
	               
	        altitude_final = my_image.gps_altitude 
	        text_box2.insert('end','\n')
	        text_box2.insert('end',altitude_final)

root.title('PhotoCalculator')
root.geometry("800x450") 
root.resizable(0, 0)

#background_image = tk.PhotoImage(file='Plane.png') //uncomment to add background
#background_label = tk.Label(root, image=background_image)
#background_label.place(relwidth=1, relheight=1)

distance = tk.Label(root,font=("Courier", 8),bg="#C5F0CE",text="Distance Mtr",bd = 2)
distance.place(x=200,y=20)
distance_entry = tk.Entry(root,bd = 2)
distance_entry.place(x=300,y=20,width=50)

altitude = tk.Label(root,font=("Courier", 8),bg="#C5F0CE",text="Altitude Mtr",bd = 2)
altitude.place(x=200,y=50)
altitude_entry = tk.Entry(root,bd = 2)
altitude_entry.place(x=300,y=50,width=50)

CamList = ["D5","D850","Sony_Ar7",] 
cam_var = tk.StringVar(root)
cam_var.set(CamList[0])

CamMenu = tk.OptionMenu(root,cam_var,*CamList)
CamMenu.config(width=8,height=1,font=("Courier", 10),bg="#C5F0CE")
CamMenu.place(x=40,y=10)

LensList = ["200MM","300MM","600MM","800MM","1700MM"] 
lens_var = tk.StringVar(root)
lens_var.set(LensList[0])

LensMenu = tk.OptionMenu(root,lens_var,*LensList)
LensMenu.config(width=8,height=1,font=("Courier", 10),bg="#C5F0CE")
LensMenu.place(x=40,y= 50)

Calculate = tk.Button(root, text = "Calculate",font=("Courier", 14,"bold"),bg="#F2DDEC",activebackground = "grey", command = Get)
Calculate.place(width="100px",x = 130 , y = 100)

text_box = tk.Text(root, width = 40, height = 16,borderwidth=3,font=("Courier", 10))
text_box.place(x=40,y=150)

Picfolder = tk.Label(root,font=("Courier", 8),bg="#C5F0CE",text="Folder path :",bd = 2)
Picfolder.place(x=450,y=50)
Picfolder_entry = tk.Entry(root,bd = 2)
Picfolder_entry.place(x=550,y=50,width=200)

Get_location = tk.Button(root, text = "Get coordinates",font=("Courier", 10,"bold"),bg="#F2DDEC",activebackground = "grey",command = getLoc)
Get_location.place(width="120px",x = 620 , y = 100)

Get_alt = tk.Button(root, text = "Get altitude",font=("Courier", 10,"bold"),bg="#F2DDEC",activebackground = "grey",command = getalt)
Get_alt.place(width="120px",x = 445 , y = 100)

text_box2 = tk.Text(root, width = 40, height = 16,borderwidth=3,font=("Courier", 10))
text_box2.place(x=450,y=150)

root.mainloop()








