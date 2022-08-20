import pypupilext as pp
import cv2
import pandas as pd
import time
import matplotlib.pyplot as plt


def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    return cv2.resize(image, dim, interpolation=inter)


img = cv2.imread("1.bmp", cv2.IMREAD_GRAYSCALE)

pupilClass = pp.Pupil()
assert pupilClass.confidence == -1

pure = pp.PuRe()
pure.maxPupilDiameterMM = 7

im_reized = img
pupil = pure.runWithConfidence(im_reized)
data = pd.DataFrame([{'Outline Conf': pupil.outline_confidence, 'PupilDiameter': pupil.diameter()}])
print(data)

img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
img_plot = cv2.ellipse(img,
                       (int(pupil.center[0]), int(pupil.center[1])),
                       (int(pupil.minorAxis()/2), int(pupil.majorAxis()/2)), pupil.angle,
                       0, 360, (0, 0, 255), 1)

resize = ResizeWithAspectRatio(img_plot, width=800)

fig = plt.figure(figsize=(20, 8))
ax1 = plt.subplot(1, 1, 1)
im1 = ax1.imshow(cv2.cvtColor(resize, cv2.COLOR_BGR2RGB))
fig.tight_layout()

plt.show()
# If you want to show the image using an opencv window instead of matplotlib
#cv2.imshow("window", resize)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.waitKey(1)
