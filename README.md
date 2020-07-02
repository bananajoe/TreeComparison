# TreeComparison
Python Code for comparing trees
This code is the source of all results in the Master Thesis:
"Comparing Trees" by Clemens Andritsch

## Setup and system requirements
This code runs in Python 3

The following packages are necessary to execute the script:

Standard packages:<br/>
os.path, time, datetime, copy, random, json, sys, getopt

Non-standard packages:<br/>
matplotlib, zss, six, numpy, pulp

If a package is missing on your Python3 instance, execute the following command:<br/>
pip3 install <packagename>

More information can be found in Pyhton's documentation:<br/>
https://docs.python.org/3/installing/index.html<br/>
or on Stackoverflow:<br/>
https://stackoverflow.com/questions/6587507/how-to-install-pip-with-python-3

## Executing the comparison tool
Before executing the command, take a look at the helper:


```bash
> python3 main.py -h
> main.py -t <tree_size> -n <number_of_trees>
```

tree_size: refers to the number of leaves each tree should have<br/>
number_of_trees: refers to the number of instances that will be created and compared

Executing "python3 main-py -t 10 -n 50" will create instances of pairs of trees with 10 leaves each, until 50 instances exist.
If 20 instances have already existed, it will only create 30 new instances.  
After creating them, the trees within each instance will be compared (w.r.t. the different distance measures) and the results stored in "examples/example_trees_size_<tree_size>.json"

Example result for an instance:
```json
{
  "one": [...], //The first tree 
  "two": [...], //The second tree
  "one_adapted": [...], //The first tree adapted (see Master Thesis)
  "#GRFRestr": 17836, //Number of restrictions for the gRF
  "GRF1": {"cost": 13.06453823953824, "time": 14.408450365066528, "time_creation": 0.30161476135253906}, //The gRF of order 1
  "GRF4": {"cost": 13.06453823953824, "time": 15.309490442276001, "time_creation": 0.27625417709350586}, //The gRF of order 4
  "GRF16": {"cost": 13.207395382395383, "time": 16.79816746711731, "time_creation": 0.29645490646362305}, //The gRF of order 16
  "GRF64": {"cost": 13.350252525252525, "time": 23.279428482055664, "time_creation": 0.29589271545410156}, //The gRF of order 64
  "ATED": {"cost": 22.0, "time": 0.05101919174194336}, //0.5-ATED
  "CTED": {"cost": 14.0, "time": 0.04715991020202637}, 
  "STED": {"cost": 28.0, "time": 0.043374061584472656}, 
  "ATED_a": {"cost": 20.0, "time": 0.06212902069091797}, //0.5-ATED with tree one_adapted
  "CTED_a": {"cost": 12.0, "time": 0.05405998229980469}, //CTED with tree one_adapted
  "STED_a": {"cost": 24.0, "time": 0.05463433265686035} //STED with tree one_adapted
}
```

Afterwards a couple of different plots are generated that compare TEDs with each other as well as the gRF.
Those plots are saved in "plots/<plot_type>_<tree_size>.png"

## Comparing your customized instance
1. Create instances of two trees according to the structured described in the Master Thesis:
```
  .
 / \
1   .
   / \
  2   3
=> [[1],[[2],[3]] 
```
Both instances need to be of the same size and on the same set of taxa ({1,...,tree_size})

2. Create example file "example_tree_size_<tree_size>.json" with the following content:<br/>
"[{"one":[...], "two":[...]}]"

3. Execute the script with the correct parameters

