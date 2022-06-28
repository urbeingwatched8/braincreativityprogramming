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

#for comparing first 10 epochs per file to last 10 epochs
#import numpy as np
#data = np.load('D:\\experiments\\artemBnpy\\artempaint1alpha.npy')
#print(len(data))
#print(len(data[0]))
#print(data[0])
#sum1=0
#for i in range(10):
#    sum1=sum1+sum(data[i])/len(data[i])
#avg=sum1/10
#print(avg)

#sum2=0
#for j in range(len(data)-10,len(data)):
#    sum2=sum2+sum(data[j])/len(data[j])
#avg2=sum2/10
#print(avg2)

