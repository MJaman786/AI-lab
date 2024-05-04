def bubble_sort(arr):
	n = len(arr)
	print("\nBubble-sort")
	for i in range(n):
		for j in range(n-i-1):
			if(arr[j]>arr[j+1]):
				temp   = arr[j]
				arr[j] = arr[j+1]
				arr[j+1] = temp
	print("Final result : ",arr) 
	
def insertion_sort(arr):
	print("\nInsertion-sort")
	n = len(arr)
	for i in range(1, n):
		
		key = arr[i]
		j   = i - 1
		
		while(j>=0 and arr[j]>key):
			arr[j+1] = arr[j]
			j -= 1
		arr[j+1] = key
	print("Final result : ",arr)

def selection_sort(arr):
	print("\nSelection-sort")
	n = len(arr)
	for i in range(n):
		minposition = i
		for j in range(i, n):
			if(arr[j]<arr[minposition]):
				minposition = j
		
		temp = arr[i]
		arr[i] = arr[minposition]
		arr[minposition] = temp
	print("Final result : ",arr)

def main():
	
	arr1 = [4, 2, 3, 1, 0, 5]
	bubble_sort(arr1)
	
	arr2 = [4, 2, 3, 1, 0, 5]
	insertion_sort(arr2)
	
	arr3 = [4, 2, 3, 1, 0, 5]
	selection_sort(arr3)
	
main()
