import os
import math
import arcpy
thumuc_in = "E:\\DTM\\" #"d:\\dtm\\"
thumuc_out = "E:\\DTM_new\\"

def make_descent_DTM(cell_size, infofile):
	fnames = os.listdir(thumuc_in)
	half_cell = cell_size/2.0
	rows = arcpy.SearchCursor(infofile,"","","Shape;FileName;Pt_Count;Pt_Spacing;Z_Min; Z_Max","")
	q = 0
	for row in rows:
		q = q + 1
		tenfile = row.FileName
		for names in fnames:
			if names.find(tenfile) >= 0:
				print "Dang xu ly file thu " + str(q) + ", co ten la: "+ tenfile
				file_in = open(thumuc_in + tenfile,"r")
				file_out = open(thumuc_out + "des" + tenfile,"w")		
				lines_in = row.Pt_count
				xmin = row.Shape.extent.XMin
				ymin = row.Shape.extent.YMin
				socot=int(math.floor((row.Shape.extent.XMax - xmin)/cell_size) + 1)
				sodong=int(math.floor((row.Shape.extent.YMax-ymin)/cell_size)+1)
				num_vector = sodong * socot
				myVector = [[0 for j in range(4)] for i in range(num_vector)]
				for i in range(int(num_vector)):
					myVector[i][0] = (i % socot)*cell_size + xmin + half_cell
					myVector[i][1] = (i // socot)*cell_size + ymin + half_cell
				title_in = file_in.readline()
				data_in = file_in.readlines()
				len_in = len(data_in)
				file_out.writelines(title_in)
				for dat in data_in:
					xyz = dat.split(" ")
					x_ = float(xyz[0])
					y_ = float(xyz[1])
					z_ = float(xyz[2])
					k_ = (x_ - xmin)/cell_size
					l_ = (y_ - ymin)/cell_size
					pos_vector = int(l_) * socot + int(k_)
					myVector[pos_vector][2] = myVector[pos_vector][2] + z_
					myVector[pos_vector][3] = myVector[pos_vector][3] + 1
				out_data = ""
				for i in range(num_vector):
					if (myVector[i][3] > 0):
						out_data = out_data + "" + str(myVector[i][0]) + " " + str(myVector[i][1]) + " " + str(myVector[i][2]/myVector[i][3]) + "\n"
				file_out.writelines(out_data)
				file_in.close()
				file_out.close()
