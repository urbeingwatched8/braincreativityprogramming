import numpy as np
data = np.load('filename.npy')
print(len(data))
print(len(data[0]))
print(data[0])
sum1=0
for i in range(len(data)):
    sum1=sum1+sum(data[i])/len(data[i])
avg=sum1/len(data)
print(avg)

