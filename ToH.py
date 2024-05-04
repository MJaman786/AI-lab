def toh(numbers, start, aux, end):
	if(numbers == 1):
		print("Move disc 1 from rod {} to rod {}".format(start,end))
		return
	toh(numbers-1, start, end, aux)
	print("Move disc {} from rod {} to rod {}".format(numbers,start,end))
	toh(numbers-1,aux, start, end)
	
toh(3, "A", "B", "C")
