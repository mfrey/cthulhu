cthulhu
-------

### Installation from git

1. Clone the repository:

		git clone git://github.com/mfrey/cthulhu.git

2. Please install the required (python) dependencies

		matplotlib
		numpy

3. Run the program

		./cthulhu

### Examples
If you want to run simulations
```
./cthulu -r -c BaselineGTS -i /full/path/to/omnetpp.ini 
```
and if you want to evaluate simulation results
```
./cthulu -p -c /full/path/to/resultfile.txt
```
If there is more than one network active in a simulation result, you have to specify the ``-n`` parameter for evaluation, e.g.:
```
./cthulu -p -c /full/path/to/resultfile.txt -n
```
You can also run several parts of the tool independtly, e.g. the castalia trace parser
```
./castaliatraceparser.py --file /path/to/tracefile -t 1.017,10.017
```
