from open3d import *
import numpy as np
import time

def main():

    start = time.time()

    #Read the point cloud
    pcd = read_point_cloud("testing/open3D/bunny.ply")
    #Visualize the point cloud
    draw_geometries([pcd])

    end = time.time()

    processingTime = end - start
    print("INFO: Point Cloud processing took "+str(round(processingTime,2))+" seconds.")

if __name__ == "__main__":
    main()