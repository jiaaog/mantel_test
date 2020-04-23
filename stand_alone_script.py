'''
-------------------------------------------------------------------------------
Name:  Mantel Test Stand Alone Script
Author:  Jiaao Guo
Created: December 05th, 2018

Purpose of script:
This is a stand-alone Mantel test script that comparing correlation between
two distance or dissimiliary matrices. It will work for any shapefile or feature
class and contains valid,comparable attributes.

It does not require the use of ArcGIS.

Outputs: A short test message stating the significance of correlation and the
pearson's correlation between the two matrices.
-------------------------------------------------------------------------------
'''


import numpy as np
import scipy
from scipy.spatial import distance
import pandas as pd

#1 Set the route for the feature or shapefile
df = pd.read_csv("C:/data/January_precipitation.csv")
density = df.P
pointx = df.Lat
pointy = df.Long

#2 - case 1: has coordinate system information.
coord = [[i,j] for i,j in list(zip(pointx, pointy))]

#create a distance matrix
location = np.array(coord) #list array of paired coordiantes
A1 = distance.pdist(location) #calculates the pairwise distances between obervations
matrix_A = distance.squareform(A1) # name of the first matrix
#then do the same for another attribute: pm concentration
A2 = np.array(density)
matrix_B = abs(A2[..., np.newaxis] - A2[np.newaxis, ...]) # second matrix. It gets the square matrix of attribute as positive numbers


#3 Calcualte M value and define permutation times
#M value is also called the observation value in Mantel test.
M_value = np.sum(np.multiply(matrix_A,matrix_B)) #it is in arbitrary unit
#in some book, it is also referred as "Manetal Statistic Z" (Z value).
#define permutation times
n_permutation = int(1000) #a user-defined permutation number
#create a while loop to run the pernumation for n times
mvalue_list = [] # a list of m value
# Notice that M value is different from m value. See explanation in the following loop
mvalue_greater_than_M = [] #this list is used to calcualted the p value in the end

#4 Set a loop to run the permutation
i = 1 #counter i
while i<=n_permutation:
    i = i+1 #set a counter for permutation times
    permutated_array = np.random.permutation(A2) #permuate the array
    #the random permuation function in numpy can work both for 1D or 2D array.
    #However, the permutation for 2D array (matrix) only permutes the rows, not the column
    #therefore, I setup the permutation for the list first, then converted it into matrix again
    #i.e. Permute both row and column
    permutated_matrix = abs(permutated_array[..., np.newaxis] - permutated_array[np.newaxis, ...])
    #in Mantel test, we only permute one matrix, then compared with another unchanged matrix
    #in this case, I permute the attribute matrix, and compared new matrix with the distance matrix
    #But user could also permute the distance matrix. The statistical significance will not change.
    #We will calculate new M value from the permuted matrix, let's call it "m" value.
    #Thus, a distribution of m values (for n times) will appear in the end, and they used to calcualte p value
    m_value = np.sum(np.multiply(permutated_matrix,matrix_A))#it's same as the M_value calculation except it uses one permuted matrix
    mvalue_list.append(m_value) #append m value to the list
    #P value = (1+n)/(1+N)
    #where n is the number of randomized m-value equal to or above (or equal to or below) the observed value,  N is the number of times of permutations.
    #So I wanna count the m values that are greater or equal than M value first:
    if m_value >= M_value:
        mvalue_greater_than_M.append(m_value)

#5 Calculate some statistics for final message
n = len(mvalue_greater_than_M) #number of m value that are greater or equal to M value
p_value = float((1+n))/float((1+n_permutation))#p statistics
mean_mvalue = np.mean(mvalue_list) #mean of mvalue distribution
std_m = np.std(mvalue_list) #standard deviation of mvalue

#6 create a function to calculate the pearson's r of the two matrices:
import math
def pearson_r(matrix1,matrix2):
    new_array = matrix1.ravel() #it is calculated based on the un-fold array of the matrix
    new_permuted_array = matrix2.ravel() #so we the matrix
    mean_newarray = np.mean(new_array)
    mean_permutadarray = np.mean(new_permuted_array)
    x1 =[item_x-mean_newarray for item_x in new_array]
    y1 = [item_y-mean_permutadarray for item_y in new_permuted_array]
    xy = [x*y for x,y in list(zip(x1,y1))]
    xy_sum = sum(xy)
    x1_square = [x**2 for x in x1]
    y1_square = [y**2 for y in y1]
    xsquare_sum = sum(x1_square)
    ysquare_sum = sum(y1_square)
    denominator = math.sqrt(xsquare_sum*ysquare_sum)
    r = xy_sum/denominator
    return r #ranges from -1 to 1
    #positive r indicating proportional relationship between two matrices, or vice versa
    #if r is close to 0, indicating no correlation between the two matrices
#calculate the pearson's r for the two matrices
pearsonvalue = pearson_r(matrix_A,matrix_B)

#8 Adding final message for the tool

print "Pearson's r is:",pearsonvalue,
print "M statistics:", M_value
print "P value, mean mvalue, and std are:",p_value,mean_mvalue,std_m,", respectively"

#end of the script
