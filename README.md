# mantel_test
Mentel permutation test (Python script tool) in ArcGIS Desktop
<a href="https://mb3is.megx.net/gustame/hypothesis-tests/the-mantel-test">Mantel Test</a> is a commonly used non-parametric test for testing the existence of spatial correlation between corresponding positions of two (dis)similarity or distance matrices.
There are also different kinds of Mantel test (simple, partial). Here I was trying to add the simple Mantel Test function into ArcGIS Desktop by writing a Python-based script tool.

The Null hypothesis of simple Mantel test, according to A correct formulation ofH0 for the Mantel test is the following: ‘H0:
The distances among objects in matrix DY are not (linearly or monotonically) related to the corresponding distances in DX’ (Legendre & Legendre 2012, p. 600)
Similar Null hypothesis can be found in Legendre (2000, p. 41): ‘The simple Mantel test is a procedure to test the hypothesis that the distances among objects in a [distance] matrix A are linearly independent of the distances among the same objects in another [distance] matrix B’ and in Legendre & Fortin (2010, p. 835).



References:
Legendre, P. & Legendre, L. (2012) Numerical Ecology, 3rd English edn. Elsevier Science BV, Amsterdam.
Legendre, P. (2000) Comparison of permutation methods for the partial correlation and partial Mantel tests. Journal of Statistical Computation and Simulation, 67, 37–73.
