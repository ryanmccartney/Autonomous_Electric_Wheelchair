def whiteBalance(image,threshold):
    
    thresholdMax = 180
    thresholdMin = 40
    whiteMax = 30
    whiteMin = 3
    iterations = 10
    direction = 0

    for i in range(0, iterations):
        rc, gray = cv.threshold(image, threshold, 0, 255)
        nwh = cv.countNonZero(gray)
        perc = int(100 * nwh / cv.countNonZero(gray))
        if perc > whiteMax:
            if threshold > thresholdMax:
                break
            if direction == -1:
                image = gray
                break
            threshold += 10
            direction = 1
        elif perc < whiteMin:
            if threshold < thresholdMin:
                break
            if  direction == 1:
                image = gray
                break
            threshold -= 10
            direction = -1
        else:
            image = gray
            break 

    return image