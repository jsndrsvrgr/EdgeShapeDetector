import common
import math #note, for this lab only, your are allowed to import math

def detect_slope_intercept(image):
	# PUT YOUR CODE HERE
	# access the image using "image[y][x]"
	# where 0 <= y < common.constants.WIDTH and 0 <= x < common.constants.HEIGHT
	# set line.m and line.b
	# to create an auxiliar bidimentional structure
	# you can use "space=common.init_space(heigh, width)"
	W = common.constants.WIDTH
	H = common.constants.HEIGHT

	#Create Sobel Output matrices
	Dx = common.init_space(H - 2, W - 2)
	Dy = common.init_space(H - 2, W - 2)

	sobel_x = [[ 1, 0,-1],
	           [ 2, 0,-2],
	           [ 1, 0,-1]]

	sobel_y = [[ 1, 2, 1],
	           [ 0, 0, 0],
	           [-1,-2,-1]]

	# h[m, n] = Sum(f[k, l] * I[m + k, n + l])
	for m in range(1, H - 1):
		for n in range(1, W - 1):
			sum_x = 0
			sum_y = 0
			for k in range(-1, 2):
				for l in range(-1, 2):
					sum_x += sobel_x[k+1][l+1] * image[m + k][n + l]
					sum_y += sobel_y[k+1][l+1] * image[m + k][n + l]
			Dx[m - 1][n - 1] = sum_x
			Dy[m - 1][n - 1] = sum_y

	Edge_m = common.init_space(H - 2, W - 2)
	edge_threshold = 100

	for m in range(H - 2):
		for n in range(W - 2):
			strength = math.sqrt(Dx[m][n]**2 + Dy[m][n]**2)
			Edge_m[m][n] = 1 if strength > edge_threshold else 0

	#Transform to Hough space with parametrization
	diagonal = math.ceil(math.sqrt((W-2)**2 + (H-2)**2))
	num_w = 2 * diagonal + 1
	num_theta = 180
	H_acc = common.init_space(num_theta, num_w)

	#Fill the accumulator array
	for m in range(H - 2):
		for n in range(W - 2):
			if Edge_m[m][n] == 1:
				for theta in range(num_theta):
					theta_rad = theta * math.pi / 180
					w = n * math.cos(theta_rad) + m * math.sin(theta_rad)
					w_idx = int(round(w)) + diagonal
					if 0 <= w_idx < num_w:
						H_acc[theta][w_idx] += 1

	best_theta = 0
	best_w = 0
	max = 0

	for theta in range(num_theta):
		for w_id in range(num_w):
			if H_acc[theta][w_id] > max:
				max = H_acc[theta][w_id]
				best_theta = theta
				best_w = w_id

	theta = best_theta * math.pi / 180
	best_w = best_w - diagonal

	#Go through accumulator array with threshold to see if peak a real line

	line=common.Line()
	line.m = -math.cos(theta) / math.sin(theta)
	line.b = best_w / math.sin(theta)
	return line

def detect_circles(image):
	# PUT YOUR CODE HERE
	# access the image using "image[y][x]"
	# where 0 <= y < common.constants.WIDTH and 0 <= x < common.constants.HEIGHT
	# to create an auxiliar bidimentional structure
	# you can use "space=common.init_space(heigh, width)"
	W = common.constants.WIDTH
	H = common.constants.HEIGHT

	#Create Sobel Output matrices
	Dx = common.init_space(H - 2, W - 2)
	Dy = common.init_space(H - 2, W - 2)

	sobel_x = [[ 1, 0,-1],
	           [ 2, 0,-2],
	           [ 1, 0,-1]]

	sobel_y = [[ 1, 2, 1],
	           [ 0, 0, 0],
	           [-1,-2,-1]]

	# h[m, n] = Sum(f[k, l] * I[m + k, n + l])
	for m in range(1, H - 1):
		for n in range(1, W - 1):
			sum_x = 0
			sum_y = 0
			for k in range(-1, 2):
				for l in range(-1, 2):
					sum_x += sobel_x[k+1][l+1] * image[m + k][n + l]
					sum_y += sobel_y[k+1][l+1] * image[m + k][n + l]
			Dx[m - 1][n - 1] = sum_x
			Dy[m - 1][n - 1] = sum_y

	Edge_m = common.init_space(H - 2, W - 2)
	edge_threshold = 100

	for m in range(H - 2):
		for n in range(W - 2):
			strength = math.sqrt(Dx[m][n]**2 + Dy[m][n]**2)
			Edge_m[m][n] = 1 if strength > edge_threshold else 0

	#Transform to Hough space for circles
	R = 30
	H_acc = common.init_space(H, W)

	#Fill the accumulator array
	for m in range(H - 2):
		for n in range(W - 2):
			if Edge_m[m][n] == 1:
				for theta in range(360):
					theta_rad = theta * math.pi / 180
					a = int(round((m + 1) - R * math.sin(theta_rad)))
					b = int(round((n + 1) - R * math.cos(theta_rad)))
					if 0 <= a < H and 0 <= b < W:
						H_acc[a][b] += 1

	#Find peaks in accumulator to count circles
	max_votes = 0
	for m in range(H):
		for n in range(W):
			if H_acc[m][n] > max_votes:
				max_votes = H_acc[m][n]

	threshold = max_votes // 2
	count = 0

	while True:
		best_m = 0
		best_n = 0
		best_val = 0
		for m in range(H):
			for n in range(W):
				if H_acc[m][n] > best_val:
					best_val = H_acc[m][n]
					best_m = m
					best_n = n
		if best_val < threshold:
			break
		count += 1
		#Zero out neighborhood around found peak
		for m in range(H):
			for n in range(W):
				if math.sqrt((m - best_m)**2 + (n - best_n)**2) <= R:
					H_acc[m][n] = 0

	return count
