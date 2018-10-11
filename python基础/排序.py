list_1=[1,3,5,22,4,66,9,7,8,10]

def func(lis):
	for i in lis:
         for i in range(len(lis)-1):
             if lis[i] > lis[i+1]:
                 lis[i], lis[i + 1] = lis[i + 1], lis[i]
	print(lis)
func(list_1)

