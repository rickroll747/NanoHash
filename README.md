# NanoHash
A Duinocoin Cryptominer for Overpowered Computers.

# Recommended Specs:
A 3070 For NVIDIA.
A 7600 xt For AMD

# Disclaimer
This Cryptominer Is For "Educational Purposes" Only. Using This Tool To Mine On The Official Duino-Coin Network Will Probably Get You **Banned!**. Use This Application At Your Own risk. Its Recommended To Use A Backup Wallet In-Case Of Getting Black-Listed. I Am Not Responsible For Any Damage Caused By This Miner To Your Account.

# Required Libraries/Dependencies & Instructions
First Get a Wallet from https://wallet.duinocoin.com/register.html, Get Verified and Follow the Instructions:
## Windows
1. Get Python 3.8+ And pip from https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe
2. Install numpy, siphash (also hashlib if you have Python 2.6) requests, PyCuda If You have An NVIDIA GPU And PyOpenCL If You have An AMD GPU.
3. Download and Extract The Latest Release and Open "NH_Miner.exe".

## Linux
Install Python 3.8+
```bash
sudo apt install python3.8
```

Now Install pip:
```bash
sudo apt install python3-pip
```
And Verify the Instalation.
```bash
python3 --version
pip3 --version
```
and Install numpy, requests, PyOpenCL (for CPUs and AMD GPUs), And PyCuda If You have An NVIDIA GPU
Then Download and Extract the Latest Release, And Open the Terminal:
python3 NH_Miner.py.

# Fixing Error on Windows/Linux
## Windows
If you open the exe file and it closes and the output says: "pytools\persistent_dict.py:52: RecommendedHashNotFoundWarning: Unable to import recommended hash 'siphash24.siphash13', falling back to 'hashlib.sha256'. Run 'python3 -m pip install siphash24' to install the recommended hash.
[ERROR] PyOpenCL is not installed. Please install it with: pip install pyopencl" its because you havent installed the libraris for your gpu and cpu.
## Linux
If the output says something like "Traceback (most recent call last): File import pycuda.driver as cuda ModuleNotFoundError" then you havent installed all the dependencies and required libraries.
