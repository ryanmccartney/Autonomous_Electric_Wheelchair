import pptk
import numpy as np
import time

start = time.time()

P = np.random.rand(3000,3)
v = pptk.viewer(P)

end = time.time()

processingTime = end - start
print("INFO: Point Cloud processing took "+str(round(processingTime,2))+" seconds.")

