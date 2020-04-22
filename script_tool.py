'''
-------------------------------------------------------------------------------
Name:  Mantel Test Statistical Tool - ArcGIS
Author:  Jiaao Guo
Created: December 05th, 2018

Purpose of script:
To create a script tool to conduct Mantel test that comparing correlation between
two distance or dissimiliary matrices. It will work for any shapefile or feature
class and contains valid,comparable attributes.

Outputs: A short test message stating the significance of correlation and the
pearson's correlation between the two matrices.
-------------------------------------------------------------------------------
'''

import arcpy
from scipy.spatial import distance
import numpy as np

#1 Set the route for the feature or shapefile
feature = arcpy.GetParameterAsText(0)
#should be changed to user defined input later:

try:
    #2. Check if it has information about xy coordinate system
    #set if condition for geographic matrices and non-geographic matrices
    has_coordinate_info = arcpy.GetParameterAsText(1) #enter yes or other words
    #it is a boolean condition in ArcGIS. It's either "true" or "false"
    if has_coordinate_info=='true':
        #2.1 - case 1: has coordinate system information.
        coord = []  #create a list for coordinate system that contains [[x1,y1],[x2,y2],...[xn,yn]]
        attribute1 = [] #create another list for the attribute to be compared with the coordiante matrix
        fields = [arcpy.GetParameterAsText(2),arcpy.GetParameterAsText(3),arcpy.GetParameterAsText(4)]  #attributes, longitude, latitude
        cursor =  arcpy.da.SearchCursor(feature,fields)
        for row in cursor:
            coord.append([row[1],row[2]])
            attribute1.append(row[0])
        #create a distance matrix
        location = np.array(coord) #list array of paired coordiantes
        A1 = distance.pdist(location) #calculates the pairwise distances between obervations
        matrix_A = distance.squareform(A1) # name of the first matrix
        #then do the same for another attribute: pm concentration
        A2 = np.array(attribute1)
        matrix_B = abs(A2[..., np.newaxis] - A2[np.newaxis, ...]) # second matrix. It gets the square matrix of attribute as positive numbers
        attribute_Name1 = str(arcpy.GetParameterAsText(2))#name for the adding message below
        lat_log_name1 = str(arcpy.GetParameterAsText(3))
        lat_log_name2 = str(arcpy.GetParameterAsText(4))
        arcpy.AddMessage("The input for the two matrices are: {0} for dissimilarity matrix; and {1}, {2} for distance matrix".format(attribute_Name1,lat_log_name1,lat_log_name2))

    else:
        #case 2: if flieds contain 2 attributes (two non-geographic matrices)
        attribute2 = []
        attribute3 = []
        fields = [arcpy.GetParameterAsText(2),arcpy.GetParameterAsText(3)]
        cursor =  arcpy.da.SearchCursor(feature,fields)
        for row in cursor:
            attribute2.append(row[0])
            attribute3.append(row[1])
        A1= np.array(attribute2)
        A2= np.array(attribute3)
        matrix_A = abs(A1[..., np.newaxis] - A1[np.newaxis, ...]) #first matrix
        matrix_B = abs(A2[..., np.newaxis] - A2[np.newaxis, ...]) #second matrix
        attribute_Name1 = str(arcpy.GetParameterAsText(2))
        attribute_Name2 = str(arcpy.GetParameterAsText(3))
        arcpy.AddMessage("The input for the two matrices are: {0} and {1}".format(attribute_Name1,attribute_Name2))

    #3 Calcualte M value and define permutation times
    #M value is also called the observation value in Mantel test.
    #It is the sum of mulpilications of pairwise elements in two matrices
    M_value = np.sum(np.multiply(matrix_A,matrix_B))/2.0 #it is in arbitrary unit
    #in some book, it is also referred as "Manetal Statistic Z" (Z value).
    #define permutation times
    n_permutation = int(arcpy.GetParameterAsText(5)) #a user-defined permutation number
    #create a while loop to run the pernumation for n times
    mvalue_list = [] # a list of m value
    # Notice that M value is different from m value. See explanation in the following loop
    mvalue_greater_than_M = [] #this list is used to calcualted the p value in the end

    #4 Set a loop to run the permutation
    i = 1 #counter i
    arcpy.SetProgressor('step','Permutation Test',0,int(n_permutation),1)
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
        arcpy.SetProgressorLabel("{0} times of permuting the matrix".format(i))
        #We will calculate new M value from the permuted matrix, let's call it "m" value.
        #Thus, a distribution of m values (for n times) will appear in the end, and they used to calcualte p value
        m_value = np.sum(np.multiply(permutated_matrix,matrix_A))/2.0#it's same as the M_value calculation except it uses one permuted matrix
        mvalue_list.append(m_value) #append m value to the list
        #P value = (1+n)/(1+N)
        #where n is the number of randomized m-value equal to or above (or equal to or below) the observed value,  N is the number of times of permutations.
        #So I wanna count the m values that are greater or equal than M value first:
        if m_value >= M_value:
            mvalue_greater_than_M.append(m_value)
        arcpy.SetProgressorPosition()

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
    arcpy.AddMessage("Null Hypothesis: there is no correlation between two distance/dissimilarity matrices")
    arcpy.AddMessage("Alternative Hypothesis: there is some correlation between two distance/dissimilarity matrices")
    if pearsonvalue>0.5:
        arcpy.AddMessage("The Pearson's R is {0} , indicating relatively strong positive correlation between these two matrices.".format(pearsonvalue))
    elif pearsonvalue<(-0.5):
        arcpy.AddMessage("The Pearson's R is {0} , indicating relatively strong negative correlation between these two matrices.".format(pearsonvalue))
    elif 0.1<pearsonvalue<0.5:
        arcpy.AddMessage("The Pearson's R is {0} , indicating slightly positive correlation between these two matrices.".format(pearsonvalue))
    elif -0.5<pearsonvalue<-0.1:
        arcpy.AddMessage("The Pearson's R is {0} , indicating slightly negative correlation between these two matrices.".format(pearsonvalue))
    else:
        print "The Pearson's R is {0} , no clear correlation between these two matrices are found".format(pearsonvalue)

    arcpy.AddMessage("The number of m value greater or equal than M statistics ({0}) is {1}, while the number of permutation is {2}. \
    The mean of (distribution of) m values is {3} and the standard deviation of m values is {4}".format(M_value,n,len(mvalue_list),mean_mvalue,std_m))
    if p_value<0.05:
        arcpy.AddMessage("The P-value of Mantel Test is {0}, we reject the null hypothesis at significance level of 0.05".format(p_value))
    else:
        arcpy.AddMessage("The P-value of Mantel Test is {0}, we accept the null hypothesis at significance level of 0.05".format(p_value))

except: #the case when the user forget to input correct fields or mis-checked the box
    print arcpy.AddMessage("ERROR:\
    Please add information in the extra field for longitude or latitude. Or uncheck the box in the second line of input window!")

#9 Delete cursor
del cursor

#end of the script
