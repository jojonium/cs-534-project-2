=========================
READ ME
=========================
This EM clusting program is written in python 3.7
To run this program make sure Python is installed
and numpy and matplotlib are installed as well. 

If numpy is not installed, you can install it from
the command line with the command
> pip install numpy

If matplotlib is not installed, you can install it from
the command line with the command
> pip install matplotlib

To run the program go to the command line and type
> python part2.py [test.csv] [#clusters]

Where test.csv is the file you want to test and #clusters
is the number of clusters to find. If you use an input of
0. The program will use Bayesian Information Criterion to
attempt to generate the number of clusters.

An error may occur if your computer is slow and BIC 
runs for over 10 seconds, if this occurs we can help fix 
that. Hopefully you have a reasonably good PC.