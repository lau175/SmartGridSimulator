# SGS: the Smart Grid Simulator

## Blockchain-based Smart Grid Simulator

#### Prerequisits
Before installing SGS, be sure have installed the Chrome browser and to satisfy the following prerequisits.

###### Virtual environment
The use Python virtual environment is strongly suggested. [Anaconda][] is recomended but not mandatory.

###### Matlab
It is suggested to have the most recent [Matlab][] version, but it is also possible to use SGS with old versions, such as Matlab R2018a. The [Matlab engine][] for Python and [Matpower][] are also required.

###### Ganache
A [Ganache][] workspace with at least 81 accounts is needed.


## Installation

To install SGS, please download the content of the repository and follow these easy 4 steps.

#### Step 1:
After opening the workspace on Ganache, go to [Remix][], copy-and-paste the content of *transaction.sol* (in the *Agent* folder). Select Web3 Provider (endpoint: http://127.0.0.1:7545) as environment and click "Compile". From the "Deploy and run contract menu", copy the bytecode and paste it in *transaction.py* (still in the *Agent* folder) at line 19 (in place of the default one).


#### Step 2:
In the virtual environment, install the MESA, Matplotlib and Jupyter Python modules:
```typescrip
pip3 install matplotlib
pip3 install jupyter
pip3 install mesa
```

#### Step 3:
Place all the downloaded .m and .mlx files, except for *t_auction_case_buyers_85.m* and *t_auction_case_sellers_85.m*, and the *Agent* folder in the Matpower folder (\path_to_folder\matpowerx.x).

Place *t_auction_case_buyers_85.m* and *t_auction_case_sellers_85.m* in the sub-folder \path_to_folder\matpowerx.x\lib\t


#### Step 4:
Place the *visualization* folder in place of the default *visualization* in Mesa (\path_to_virtual_env\path_to_libraries\mesa).
For example, with Anaconda C:\...\Anaconda3\envs\interdisc\lib\site-packages\mesa


## Use
To use SGS, only two actions are required:

###### a) Open Ganache and select the preferred workspace (with at least 81 accounts).
###### b) Open the terminal of the virtual enviroment and navigate to the *Agent* folder, then run the command
```typescript
mesa runserver
```
The SGS page will be automatically opened on Chrome. You will be able there to set the parameters before starting the simulation.



[Anaconda]: https://www.anaconda.com/products/individual
[Matlab]: https://it.mathworks.com/help/install/
[Matlab engine]: https://it.mathworks.com/help/matlab/matlab_external/get-started-with-matlab-engine-for-python.html
[Matpower]: https://matpower.org/
[Ganache]: https://stackoverflow.com
[Remix]: https://remix.ethereum.org/#optimize=false&runs=200&evmVersion=null&version=soljson-v0.8.4+commit.c7e474f2.js
