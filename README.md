cthulhu
=======
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
