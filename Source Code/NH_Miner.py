import socket
import time
import hashlib
import random
import threading
import pyopencl as cl
import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

print("Welcome to NanoHash Miner")
print("an 3070/6800XT is Recommended for Mining with this Miner")
print("This program is a Cryptominer made for Powerful PCs to emulate an RPI5 Cluster to make more Duino-Coins")
print("And make a Living by cheating the System.")
print("*IF* You get into Trouble for using this Program then We arent responsible")

# DUCO Pool Server Details
DUCO_HOST = "server.duinocoin.com"
DUCO_PORT = 443  # Change if necessary

# User Authentication
USERNAME = input("Enter your DUCO username: ")
KEY = input("Enter your verification key: ")

if not USERNAME or not KEY:
    print("You must verify your DUCO account to use this miner.")
    exit()

def check_credentials():
    try:
        sock = socket.socket()
        sock.connect((DUCO_HOST, DUCO_PORT))
        sock.sendall(f"JOB,{USERNAME},{KEY},RPI5x6\n".encode())  # Emulating 6x RPi 5
        response = sock.recv(1024).decode().split(",")
        if len(response) >= 3 and response[0] == "JOB":
            print(f"Connected. Mining for: {USERNAME}")
            return True
        else:
            print("Invalid credentials.")
            return False
    except Exception as e:
        print(f"Connection error: {e}")
        return False

if not check_credentials():
    print("Exiting due to invalid verification.")
    exit()

# OpenCL GPU Setup (for AMD GPUs)
def setup_opencl():
    platforms = cl.get_platforms()
    gpu_devices = [d for p in platforms for d in p.get_devices(device_type=cl.device_type.GPU)]
    if not gpu_devices:
        return None, None
    ctx = cl.Context(devices=gpu_devices)
    queue = cl.CommandQueue(ctx)
    return ctx, queue

# CUDA GPU Setup (for NVIDIA GPUs)
def setup_cuda():
    try:
        device = cuda.Device(0)
        context = device.make_context()
        return context, device
    except Exception as e:
        print("No NVIDIA GPU detected.")
        return None, None

# OpenCL Kernel (AMD GPU Mining)
def get_opencl_kernel(ctx):
    program_source = """
    __kernel void mine(__global char* job, __global int* difficulty, __global int* result) {
        int id = get_global_id(0);
        int nonce = id;
        char buffer[128];
        sprintf(buffer, "%s%d", job, nonce);
        unsigned char hash[32];
        sha256(buffer, strlen(buffer), hash);
        if (hash[0] == 0 && hash[1] < *difficulty) {
            *result = nonce;
        }
    }
    """
    return cl.Program(ctx, program_source).build()

# CUDA Kernel (NVIDIA GPU Mining)
cuda_kernel = SourceModule("""
__global__ void mine(char *job, int difficulty, int *result) {
    int id = threadIdx.x + blockIdx.x * blockDim.x;
    int nonce = id;
    char buffer[128];
    sprintf(buffer, "%s%d", job, nonce);
    unsigned char hash[32];
    sha256(buffer, strlen(buffer), hash);
    if (hash[0] == 0 && hash[1] < difficulty) {
        *result = nonce;
    }
}
""")

def cpu_mine(job, difficulty):
    nonce = random.randint(0, 1000000)
    while True:
        text = f"{job}{nonce}".encode()
        duco_hash = hashlib.sha1(text).hexdigest()
        if duco_hash[:4] == "0000":
            return nonce
        nonce += 1

def gpu_mine(job, difficulty, ctx, queue):
    kernel = get_opencl_kernel(ctx)
    mf = cl.mem_flags
    job_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.frombuffer(job.encode(), dtype=np.uint8))
    difficulty_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.array([difficulty], dtype=np.int32))
    result_buf = cl.Buffer(ctx, mf.WRITE_ONLY, size=4)
    kernel.mine(queue, (256,), None, job_buf, difficulty_buf, result_buf)
    result = np.empty(1, dtype=np.int32)
    cl.enqueue_copy(queue, result, result_buf).wait()
    return result[0]

def cuda_mine(job, difficulty, device):
    block_size = 256
    grid_size = 64
    mine_func = cuda_kernel.get_function("mine")
    result = np.zeros(1, dtype=np.int32)
    job_gpu = cuda.mem_alloc(len(job))
    difficulty_gpu = cuda.mem_alloc(4)
    result_gpu = cuda.mem_alloc(4)
    cuda.memcpy_htod(job_gpu, job.encode())
    cuda.memcpy_htod(difficulty_gpu, np.int32(difficulty))
    mine_func(job_gpu, difficulty_gpu, result_gpu, block=(block_size, 1, 1), grid=(grid_size, 1, 1))
    cuda.memcpy_dtoh(result, result_gpu)
    return result[0]

def mine():
    ctx, queue = setup_opencl()
    cuda_ctx, cuda_device = setup_cuda()
    
    while True:
        sock = socket.socket()
        sock.connect((DUCO_HOST, DUCO_PORT))
        sock.sendall(f"JOB,{USERNAME},{KEY},RPI5x6\n".encode())
        response = sock.recv(1024).decode().split(",")
        job, difficulty = response[0], int(response[2])
        
        if cuda_device:
            nonce = cuda_mine(job, difficulty, cuda_device)
        elif ctx:
            nonce = gpu_mine(job, difficulty, ctx, queue)
        else:
            nonce = cpu_mine(job, difficulty)
        
        sock.sendall(f"{nonce}\n".encode())
        print(f"Mined nonce: {nonce}")
        time.sleep(0.1)

if __name__ == "__main__":
    mine()
