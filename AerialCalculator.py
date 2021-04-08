import tkinter as tk
import csv
import math
import os
from exif import Image as img
from PIL import Image, ExifTags

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
#lens selection (mm,x_fov,y_fov)
lens200 = Lens(200,10.3,6.9) 
lens300 = Lens(300,6.9,4.6)
lens600 = Lens(600,3.4,2.3)
lens800 = Lens(800,2.6,1.7)
lens1700 = Lens(1700,1.23,0.8)
#camera selection (x,y pixel density)
CamD850 = Camera(8256,5504)
CamD5 = Camera(5588,3712)
Sony_Ar7= Camera(9504,6336)

root = tk.Tk()


def Get():
	
	text_box.delete(1.0, "end-1c")
	Currentcam = cam_var.get()
									#easier way to select variable?
	if Currentcam == "D5":
		Currentcam = CamD5.x_res
	elif Currentcam == "D850":
		Currentcam = CamD850.x_res
	elif Currentcam == "Sony_Ar7":
		Currentcam = Sony_Ar7.x_res
	else:
		raise SystemExit
	
	Currnetlens = lens_var.get()
									#easier way to select variable?
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

	Currentdis = int(distance_entry.get())	#Distance input in meters
	Currentalt = int(altitude_entry.get())	#Alt input in feet
	Currentalt = Currentalt * 0.3048 	#conversion from feet to meters
	
	#distance and angles to and from ground
	camTriagle = math.sqrt(float(Currentdis**2 + Currentalt**2))
	angleFromPlane = math.asin(Currentdis/camTriagle) * 180/math.pi
	angleOnGround = math.asin(Currentalt/camTriagle) * 180/math.pi
	C = 180 - angleFromPlane - angleOnGround

	closeBorderAng = angleFromPlane - Currnetlens_y  #adding and subtracting lens fov to calculate far and close border distance
	farBorderAng = angleFromPlane + Currnetlens_y
	C2 = 90 - closeBorderAng
   	
   	#width of close border of photo calculation
	closeBorder = math.tan(math.radians(closeBorderAng))
	closeBorder_Dis = closeBorder * Currentalt
	closeBorder_Half = closeBorder_Dis * math.tan(math.radians(Currnetlens_x))
	closeBorder_res = (closeBorder_Half * 2 / Currentcam)
	
	#width of far border of photo calculation
	farBorder = math.tan(math.radians(farBorderAng))
	farBorder_Dis = farBorder * Currentalt
	farBorder_Half = farBorder_Dis * math.tan(math.radians(Currnetlens_x))
	farBorder_res = (farBorder_Half * 2 / Currentcam)

	#addition calculations formatting and conversions
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

	parameters = [Distancetotarget,Groundangle,Planeangle,Farres,Closeres,Ppmavg,Height,Farlength,Closelength,Sqm,Avghl]


	with open('Report.csv', 'a', newline='') as file:
		writer = csv.writer(file)
		for i in range(len(parameters)):
			writer.writerow([parameters[i]])
			text_box.insert('end',parameters[i] + '\n')
		writer.writerow(["------------------------------------------------------- "])



def getLoc():
	text_box2.delete(1.0, "end-1c")
	text_box2.insert('1.0',"coordinates in csv")
	
	Dir = Picfolder_entry.get()
	img_contents = os.listdir(Dir)
	Coordinate_List_lat = []
	Coordinate_List_long = []
	
	def convert_to_degress(value): #conversion from tupled exif coordinates to dms.

		d0 = value[0][0]
		d1 = value[0][1]
		d = float(d0) / float(d1)

		m0 = value[1][0]
		m1 = value[1][1]
		m = float(m0) / float(m1)

		s0 = value[2][0]
		s1 = value[2][1]
		s = float(s0) / float(s1)

		return d + (m / 60.0) + (s / 3600.0)

	for image in img_contents:

		full_path = os.path.join(Dir, image)
		pil_img = Image.open(full_path)
		exif = {ExifTags.TAGS[k]: v for k, v in pil_img._getexif().items() if k in ExifTags.TAGS} #compact dictionary of all exif data
		gps_all = {}
    
		for key in exif['GPSInfo'].keys(): #retrival of coordinates
			try:

				decoded_value = ExifTags.GPSTAGS.get(key)
				gps_all[decoded_value] = exif['GPSInfo'][key]

			except:
				text_box2.insert('end',full_path)
			
			long = gps_all.get('GPSLongitude')
			lat = gps_all.get('GPSLatitude')
			
	
		Coordinate_List_lat.append(lat)
		Coordinate_List_long.append(long)
	
	with open('coordinates.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["-----coordinates------"])
	
	
	with open('coordinates.csv', 'w', newline='') as file:	
		wr = csv.writer(file)
		wr.writerow(("Lat", "Long"))
		rcount = 0
		for row in Coordinate_List_lat:
			wr.writerow((Coordinate_List_lat[rcount], Coordinate_List_long[rcount]))
			rcount = rcount + 1
		file.close()
		
	
def getalt():
	text_box2.delete(1.0, "end-1c")
	Dir = Picfolder_entry.get()
	text_box2.insert('1.0',"          -------altitude-------")
	
	for pic in os.listdir(Dir):
	    fullpath = os.path.join(Dir,pic) 
	    
	    with open(fullpath, 'rb') as image_file:
	        my_image = img(image_file)
	               
	        altitude_final = my_image.gps_altitude 
	        text_box2.insert('end','\n')
	        text_box2.insert('end',altitude_final)


root.title('PhotoCalculator')
root.geometry("800x450") 
root.resizable(0, 0)

#background_image = tk.PhotoImage(file='Plane.png') //uncomment to add background
#background_label = tk.Label(root, image=background_image)
#background_label.place(relwidth=1, relheight=1)

distance = tk.Label(root,font=("Courier", 8),bg="#d6f9ff",text="Distance Mtr",bd = 2)
distance.place(x=200,y=35)
distance_entry = tk.Entry(root,bd = 2)
distance_entry.place(x=300,y=30,width=65)

altitude = tk.Label(root,font=("Courier", 8),bg="#d6f9ff",text="Altitude FT",bd = 2)
altitude.place(x=200,y=65)
altitude_entry = tk.Entry(root,bd = 2)
altitude_entry.place(x=300,y=60,width=65)

CamList = ["D5","D850","Sony_Ar7",] 
cam_var = tk.StringVar(root)
cam_var.set(CamList[0])

CamMenu = tk.OptionMenu(root,cam_var,*CamList)
CamMenu.config(width=8,height=1,font=("Courier", 10),bg="#d6f9ff")
CamMenu.place(x=50,y=20)

LensList = ["200MM","300MM","600MM","800MM","1700MM"] 
lens_var = tk.StringVar(root)
lens_var.set(LensList[0])

LensMenu = tk.OptionMenu(root,lens_var,*LensList)
LensMenu.config(width=8,height=1,font=("Courier", 10),bg="#d6f9ff")
LensMenu.place(x=50,y= 60)

Calculate = tk.Button(root, text = "Calculate",font=("Times New Roman", 14,"bold"),bg="#d6f9ff",activebackground = "grey", command = Get)
Calculate.place(width="100px",x = 135 , y = 100)

text_box = tk.Text(root, width = 42, height = 16,borderwidth=3,font=("Courier", 10))
text_box.place(x=40,y=150)

Picfolder = tk.Label(root,font=("Courier", 8),bg="#d6f9ff",text="Folder path :",bd = 2)
Picfolder.place(x=450,y=55)
Picfolder_entry = tk.Entry(root,bd = 2)
Picfolder_entry.place(x=550,y=50,width=200)

Get_location = tk.Button(root, text = "Get coordinates",font=("Times New Roman", 10,"bold"),bg="#d6f9ff",activebackground = "grey",command = getLoc)
Get_location.place(width="120px",x = 620 , y = 100)

Get_alt = tk.Button(root, text = "Get altitude",font=("Times New Roman", 10,"bold"),bg="#d6f9ff",activebackground = "grey",command = getalt)
Get_alt.place(width="120px",x = 445 , y = 100)

text_box2 = tk.Text(root, width = 42, height = 16,borderwidth=3,font=("Courier", 10))
text_box2.place(x=425,y=150)

root.mainloop()








