import time

def step():
    # Takes step after fixed time
    t_end = time.time() + 0.05
    k = -1
    while time.time() < t_end:
        if k == -1:
            k = cv2.waitKey(1)
        else:
            continue