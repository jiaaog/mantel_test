# mantel_test
## Mentel permutation test
<a href="https://mb3is.megx.net/gustame/hypothesis-tests/the-mantel-test">Mantel Test</a> is a commonly used non-parametric test for testing the existence of spatial correlation between corresponding positions of two (dis)similarity or distance matrices (Mantel, 1967).<br>
<br>
There are different kinds of Mantel test (for exmaple, simple and partial Mantel test). The aim of this repository is to share the *Simple Mantel Test - Python script tool* that I created. It is used in ArcGIS Desktops (e.g. ArcMap, ArcCatalog, etc.) to find out the Mantel statistics and significance between two distance or dissimilarity matrices. Currently it will work (I hope) for any feature or shapefile that contain valid and comparable fields, constructing matrices from the fields’ value, and return a neat report for correlation significance.<br>
<br>
## Null Hypothesis
The Null hypothesis of simple Mantel test (H0) can be viewed as: <br>
> ‘H0: The distances among objects in matrix DY are not (linearly or monotonically) related to the corresponding distances in DX’ (Legendre & Legendre 2012, p. 600)<br>
<br>
Similar Null hypothesis can be found in Legendre (2000, p. 41) and in Legendre & Fortin (2010, p. 835):<br> 
> ‘The simple Mantel test is a procedure to test the hypothesis that the distances among objects in a *distance* matrix A are linearly independent of the distances among the same objects in another *distance* matrix B’.<br>
<br>
## So what the heck is a Mantel Test?
In simple words, the idea underlying Mantel's Test is that <em>if there is a relationship between two matrices, the sum of products (**M value**) of these two matrices will be relatively very high (positive relation) or very low (negative relation)</em>. And a random Monte Carlo simulation of rows and columns for one of the matrix will change the sum of products (**M value**) of these two matrices. Thus if such random simulation (permutation of row and column of one matrix) was applied for 10000 times (or any user-defined times>1000), a distribution of M values will be shown. Then we could see if the p-value from the number of m-values that are equal or greater (or equal or less) than the original M value, and conclude that if there is a significant correlation between two matrices.<br>
<br>
The equation for calculating M value is detailed demonstrated in Giraldo et al. (2016). Firstly, say we have a dissimilarity matrix C and geographic distances matrix D:<br>
<div align="center">![Matrices](https://user-images.githubusercontent.com/41793727/80041256-328ae100-84b9-11ea-8574-7ddcf8db0b73.png)</div><br>
where c*ij* is the *i*th element of column *j* in the dissimilarity matrix C, and d*ij* is the ith element in column *j* in the geographic distance matrix D. After the *N* times of permutation, we could compare the new **M value** with the original M value, and see how many of the new M values are equal or greater (or equal or smaller) than the original M value. The p value is, therefore, calculated in the way that:
<div align="center"> *p* value = (1+*n*)/(1+N)</div><br>
where *n* is the number of randomized new **M values** equal to or above (or equal to or below) the original, observed **M value**, *N* is the number of times of permutations<br>
<br>
Pearson’s *r* in Mantel test is conducted as the normal regression *r* correlation test. However, it’s the unfolded version of matrices (and it’s different from the original array of attributes). It can be calculated in the way that:<br>
<div align="center">![pearson r](https://user-images.githubusercontent.com/41793727/80042246-c067cb80-84bb-11ea-8d1e-b76e824a2833.gif)</div><br>
The *r* value ranges from -1 to 1. The positive *r* value indicate the positive correlation between the two matrices, and negative *r* indicates reversed correlation between two matrices. If *r* is quite close to 0 (i.e. -0.1 < r < 0.1), it indicates poor or no correlation between two matrices.<br>
<br>

## Mentel permutation test (Python script tool) in ArcGIS Desktop
In Mantel Test Script Tool (MTST), firstly, there are 3 statistics to be calculated to make the Mantel test complete: the M statistics (the sum of products of matrices), the Pearson’s r value and the p-value. It requires importing “numpy” and “scipy” to extend native Python functions for arrays and matrices calculation. It will also use the SearchCursor from “arcpy” functionalities. This project will be a lot easier if ArcGIS Desktop was run on Python 3. This is because there is a third party function from “[skbio.math.stats.distance](http://scikit-bio.org/docs/0.1.3/generated/skbio.math.stats.distance.mantel.html)” to do Mantel test. All the user need are two array of list, and it will return all the 3 statistics of Mantel Test. However, the “skbio” only works on Windows at Python version 3.4. Thus, it would be possible to create a Mantel test in ArcGIS Pro (Python 3) by importing this package.<br> 

The result of this script tool is validated with <em>R</em> packages such as [ade4](https://cran.r-project.org/web/packages/ade4/index.html) and [vegan](https://cran.r-project.org/web/packages/vegan/index.html).<br>

## Examples
### Case A - Distance Matrices
We have the data for [12 air quality monitoring facilities in Greater Toronto and Hamilton Area](https://open.canada.ca/data/en/dataset/881a606b-69e0-473f-841d-aec9e2815e58) (Figure 1). Data can be downloaded [here](https://github.com/jiaaog/mantel_test/blob/master/dataset.gdb.zip). We want to find out if the average PM 2.5 concentration in 2013 is spatially correlated with their geographic locations, we could run the the Mantel Test script tool [Toolbax](https://github.com/jiaaog/mantel_test/blob/master/ArcGIS_Toolbox.zip).<br>
<div align="center">![ AQI facilities](https://user-images.githubusercontent.com/41793727/80042736-efcb0800-84bc-11ea-878a-593e2d2c864d.png)</div><br>
<div align="center">Figure 1: AQI monitoring facilities</div><br>
Firstly, the user may need to check the attribute table of the feature to see the corresponding names of fields (Figure 2). <br>
<div align="center">![ attribute table 1](https://user-images.githubusercontent.com/41793727/80042735-ef327180-84bc-11ea-9cc7-dd222b3b1320.png)</div><br>Attribute table in ArcGISGUI of the script too</div><br>
In this case, three attributes are useful to us: “Longitude”, “Latitude”, and “Average_Fine_PM_2013”. Then it can be done as Figure 3:<br>
<div align="center">![ gui of mantel test](https://user-images.githubusercontent.com/41793727/80042738-f0639e80-84bc-11ea-894e-47d91bb80828.png)</div><br>
<div align="center">Figure 3: Input GUI of Case A</div><br>
After all the parameter is set, click “OK” to run MTST. The result will be like a message window similar to Figure 4. If the p-value is very small (e.g. 0.016), we would be confident that there is correlation between two matrices (at significance level of 0.05, or 95% confident). Whether such correlation is positive or native, depends on the sign of Pearson’s r value.
<div align="center">![gui of mantel test](https://user-images.githubusercontent.com/41793727/80042828-4a646400-84bd-11ea-8ace-475e2fa64bf8.png)</div><br>
<div align="center">Figure 4: Result messages</div><br>

### Case B - Dissimilarity Matrices###
We have the data for the soil properties in Calgary and surrounding areas (Figure 5). Say if we want to compare correlation between soil pH value and the soil organic carbon percentage as two fields in the data (Figure 6). In this case, we don’t have the x-y coordinate information. However, Mantel test can still test the absolute distance between two datasets by constructing dissimilarity matrices. The matrices will calculate the absolute different between pairwise points.
<div align="center">![soil calgary area](https://user-images.githubusercontent.com/41793727/80042733-ef327180-84bc-11ea-94b8-5042bd7b0a40.png)</div><br>
<div align="center">Figure 5: Soil properties in Calgary and surrounding areas. “PH2” is the field name of pH value,
“ORGCARB” is the field name of soil organic carbon percentage (%) in relative to weight.</div><br>
<div align="center">![attribute table 2](https://user-images.githubusercontent.com/41793727/80042732-ee99db00-84bc-11ea-8a83-a63ce7db3344.png)</div><br>
<div align="center">Figure 6. Calgary and surrounding soil properties attribute table.</div><br>
To do so, it’s quite similar as the process in Case A, but with the *xy* coordinate information box unchecked (Figure 7). The final message section will be in the same format as Case 1.<br>
<div align="center">![GUI Case B](https://user-images.githubusercontent.com/41793727/80042737-efcb0800-84bc-11ea-8152-6dba257bf918.png)</div><br>
<div align="center">Figure 7. Input GUI of Case B</div><br>

## Limitations##
There are also some limitation of Mantel test that user should be aware.
1. The interdependence between distance matrices may result lousy permutation result. For example, Calgary is 3000 km away from Montreal, Montreal is 500 km way from Toronto. These two distance relationships limit the location of Toronto in relative to Calgary (3000km ±500km).
2. If matrices size are too small (e.g. two 5 by 5 matrices), the accuracy is also limited. This is because the permutation will be simply repetitions for the same matrix.
3. Mantel test only assumes linear relationships between matrices. Sometimes the reality is non-linear.
4. This script tool cannot be applied to raster images directly. However, the user can always using "Extract Values to Points" tool to convert raster into vector data.
5. This project for now only works for ArcGIS Desktop (Python 2.7). There is a third party function from “[skbio.math.stats.distance](http://scikit-bio.org/docs/0.1.3/generated/skbio.math.stats.distance.mantel.html)” to do Mantel test but it runs only on Python version 3.4 (Windows). Thus, it would be a lot easier to create a Mantel test in ArcGIS Pro (Python 3) by importing this package. I will try to update the script tool for ArcGIS Pro soon.

<br>
For more detailed significance and whether should Mantel Test should be used, you can find it in Legendre <em>et al</em> (2015).

## Stand-alone script for Mantel Test##
The codes for ArcGIS Desktop script tool can be found [here](https://github.com/jiaaog/mantel_test/blob/master/script_tool.py). However, if you want to try, there is also a [stand-alone script](https://github.com/jiaaog/mantel_test/blob/master/stand_alone_script.py).<br>

## References##
Mantel, N. (1967). The detection of disease clustering and a generalized regression approach. *Cancer research*, 27(2 Part 1), 209-220.<br>
Giraldo, R., Caballero, W., & Camacho-Tamayo, J. (2018). Mantel test for spatial functional data. *AStA Advances in Statistical Analysis*, 102(1), 21-39.<br>
Legendre, P., & Legendre, L. (2012). Numerical ecology, 3rd English edn Amsterdam. <em>The Netherlands: Elsevier Science BV</em>.<br>
Legendre, P. (2000). Comparison of permutation methods for the partial correlation and partial Mantel tests. <em>Journal of statistical computation and simulation</em>1), 37-73.<br>
Legendre, P., Fortin, M. J., & Borcard, D. (2015). Should the Mantel test be used in spatial analysis?. <em>Methods in Ecology and Evolution</em>, 6(11), 1239-1247.<br>
