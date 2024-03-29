# SGS: the Smart Grid Simulator

## Blockchain-based Smart Grid Simulator

#### Prerequisits
Before installing SGS, be sure to have installed the Chrome browser and to satisfy the following prerequisits.

###### Virtual environment
The use of a Python virtual environment is strongly suggested. [Anaconda][] is recomended but not mandatory.

###### Matlab
It is suggested to have a recent [Matlab][] version, but it is also possible to use SGS with old versions, such as Matlab R2018a. The [Matlab engine][] for Python and [Matpower][] are also required.

###### Ganache
A [Ganache][] workspace with at least 81 accounts is needed.


## Installation

To install SGS, please download the content of the repository and follow these easy 4 steps.

#### Step 1:
After opening the workspace on Ganache, go to [Remix][], copy-and-paste the content of *transaction.sol* (in the *Agent* folder).
<center><img src="https://github.com/lau175/SmartGridSimulator/blob/main/images4readme/rmx1.PNG"></center>


Select Web3 Provider (endpoint: http://127.0.0.1:7545) as environment and click "Compile".
<center><img src="https://github.com/lau175/SmartGridSimulator/blob/main/images4readme/rmx2.PNG"></center>
<center><img src="https://github.com/lau175/SmartGridSimulator/blob/main/images4readme/rmx3.PNG"></center>
<center><img src="https://github.com/lau175/SmartGridSimulator/blob/main/images4readme/rmx4.PNG"></center>


From the "Deploy and run contract" menu, copy the bytecode at the bottom right and paste it in *transaction.py* (still in the *Agent* folder) at line 19 (in place of the default one).
<center><img src="https://github.com/lau175/SmartGridSimulator/blob/main/images4readme/rmx5.PNG"></center>



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


## Run
To run SGS, only two actions are required:

###### a) Open Ganache and select the preferred workspace (with at least 81 accounts).
###### b) Open the terminal of the virtual enviroment and navigate to the *Agent* folder, then run the command
```typescript
mesa runserver
```
The SGS page will be automatically opened on Chrome. You will be able there to set the parameters before starting the simulation.


## Use

#### Set the parameters
Once the web page is automatically opend, it is possible to set different paramenters for the simulations:
- **Percentage of commercial activities**: probaility for prosumers following a business energy profile;
- **Probability of awareness**: probability for prosumers to care about their energy profile (they may try to reduce their energy waste or demanding more energy than the average consumption profile to increase their comfort level).

Once the parameters are set, click on "Reset" (on the top right in the navigation bar) to initialize the simulation. When the graphic for the grid is loaded, click on "Start".


#### Plots

Step by step, it is possible to visualize the grid with the prosumers and their state, how many of them are self-balanced, balanced through direct negotiations or by the local market.
It is also present the plot with the amount of exchanged energy among prosumers and with the local market.
Also the trend for the average price in the direct negotiations for each neighbourhood are shown.

<center><img src="https://github.com/lau175/SmartGridSimulator/blob/main/images4readme/grid.PNG"></center>
<center><img src="https://github.com/lau175/SmartGridSimulator/blob/main/images4readme/graph.PNG"></center>



[Anaconda]: https://www.anaconda.com/products/individual
[Matlab]: https://it.mathworks.com/help/install/
[Matlab engine]: https://it.mathworks.com/help/matlab/matlab_external/get-started-with-matlab-engine-for-python.html
[Matpower]: https://matpower.org/
[Ganache]: https://stackoverflow.com
[Remix]: https://remix.ethereum.org/#optimize=false&runs=200&evmVersion=null&version=soljson-v0.8.4+commit.c7e474f2.js
