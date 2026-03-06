import struct, array
import common
import student_code

class bcolors:
	RED    = "\x1b[31m"
	GREEN  = "\x1b[32m"
	NORMAL = "\x1b[0m"

def readBmp(filename):
	pixels=0
	
	image=[[0 for x in range(200)] for y in range(200)]

	with open(filename, 'rb') as fd:
		header = fd.read(15)
		for y in range(200):
			row = list(bytearray(fd.read(3*200)))
			
			#print row
			for x in range(200):
				pixels+=1
				index=x*3
				image[y][x]= row[index]
	return image
	
def between(v, l, u):
	return v>=l and v <= u

def similar(v, c, m):
	return between(v,c-m,c+m)

def check_slopeintercept ( title, filename, m_gold, b_gold):
	success=True
	image=readBmp(filename)
	line = student_code.detect_slope_intercept(image)
	print(title + " slope intercept results:")
	if (similar (line.m,m_gold,.1)):
		print("m: " + str(line.m) + " (" + bcolors.GREEN + "SUCCESS" + bcolors.NORMAL + ")")
	else:
		print("m: " + str(line.m) + " (" + bcolors.RED + "FAIL" + bcolors.NORMAL + ") expected "+ str(m_gold))
		success = False

	if (similar(line.b,b_gold,3)):
		print("b: " + str(line.b) + " (" + bcolors.GREEN + "SUCCESS" + bcolors.NORMAL + ")")
	else:
		print("b: " + str(line.b) + " (" + bcolors.RED + "FAIL" + bcolors.NORMAL + ") expected "+ str(b_gold))
		success = False
	print 
	return success

def check_circles ( title, filename, c_gold):
	success=True
	image=readBmp(filename)
	circles = student_code.detect_circles(image)
	print(title + " normal intercept results:")
	if (circles==c_gold):
		print("detected: " + str(circles) + " (" + bcolors.GREEN + "SUCCESS" + bcolors.NORMAL + ")")
	else:
		print("detected: " + str(circles) + " (" + bcolors.RED + "FAIL" + bcolors.NORMAL + ") expected "+ str(c_gold))
		success = False
	print 
	return success


	
all_passed = True


all_passed = check_slopeintercept("Line 1","../test1.ppm",-1.0,300) and all_passed
all_passed = check_slopeintercept("Line 2","../test2.ppm",.85,26) and all_passed
all_passed = check_slopeintercept("Line 3","../test3.ppm",.215,97) and all_passed
all_passed = check_slopeintercept("Line 4","../test4.ppm",2.0,-100) and all_passed
all_passed = check_slopeintercept("Line 5","../test5.ppm",5.0,0) and all_passed

all_passed = check_circles("Circles 1","../circ1.ppm",1) & all_passed
all_passed = check_circles("Circles 2","../circ2.ppm",3) & all_passed
all_passed = check_circles("Circles 3","../circ3.ppm",5) & all_passed
all_passed = check_circles("Circles 4","../test1.ppm",0) & all_passed



if all_passed:
	exit(0)
else:
	exit(1)
