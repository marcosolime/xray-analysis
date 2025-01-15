"""
Given a set of projections and angles, the script reconstructs the 3D volume using SART algorithm.

The script requires a dictionary containing the following values:
"projs": a numpy array of dimension (#projections, height, width) e.g. (180, 256, 256)
"angles": a numpy array of dimension (180,)

"""

from __future__ import division
from __future__ import print_function

import numpy as np
import tigre
import tigre.algorithms as algs
from tigre.utilities import sample_loader
from tigre.utilities.Measure_Quality import Measure_Quality
import tigre.utilities.gpu as gpu
import matplotlib.pyplot as plt
import os
from PIL import Image

# 1) Showing available GPUs
listGpuNames = gpu.getGpuNames()
if len(listGpuNames) == 0:
    print("Error: No gpu found")
else:
    for id in range(len(listGpuNames)):
        print("{}: {}".format(id, listGpuNames[id]))

gpuids = gpu.getGpuIds(listGpuNames[0])
#print(gpuids)

# 2) Geometry
geo = tigre.geometry()

geo.DSD = float(1500)  # distance source <-> detector in mm
geo.DSO = float(1000)  # distance source <-> object in mm

# detector properties
geo.nDetector = np.array([256, 256])  # number of pixels
geo.dDetector = np.array([1.0, 1.0])  # size of pixel
geo.sDetector = geo.nDetector * geo.dDetector  # total detector size

# voxel properties
geo.nVoxel = np.array([256, 256, 256]) # number of voxels
geo.dVoxel = np.array([1.0, 1.0, 1.0]) # size of each voxel
geo.sVoxel = geo.nVoxel * geo.dVoxel  # total volume

# additional geometry
geo.offOrigin = np.array([0, 0, 0])  # offset reconstructed volume
geo.offDetector = np.array([0, 0])  # offset of the detector (if any)

geo.accuracy = 0.5  # projection accuracy

# 3) Load projections
projs_angles = np.load("../data/battery/3_clear/npz/projs_angles.npz")
projections = projs_angles["projs"].astype(np.float32)  # shape: (180, 256, 256)
angles = projs_angles["angles"].astype(np.float32)      # shape: (180,)

# half number of projections and angles
#projections = projections[::2]
#angles = angles[::2]
print(f"projections: {projections.shape}")
print(f'angle length: {len(angles)}')
print(f'min: {np.min(projections)}, max: {np.max(projections)}')

# 4) Reconstruction

# SART reconstruction
'''
niter = 20  # Number of iterations for the algorithm
reconstructed_volume = algs.sart(projections, geo, angles, niter=niter)
np.save('sart_volume.npy', fdkout)
'''

# OSSART reconstruction
'''
niter = 50
ossart = algs.ossart(projections, geo, angles, niter, blocksize=20, gpuids=gpuids)
np.save('ossart_volume.npy', ossart)
'''

# FDK reconstruction
fdkout = algs.fdk(projections, geo, angles, gpuids=gpuids)
np.save('fdk_volume.npy', fdkout)

print('DONE.')