import cv2
import numpy as np

# look into mixing python code with the c++ module
# https://stackoverflow.com/questions/54317280/how-to-mix-python-code-into-a-python-extension-module


class SingleCalibration:

    def __init__(self, file_path):
        # load calibration file
        # FILE_STORAGE_READ
        self.file_path = file_path

        cv_file = cv2.FileStorage(file_path, cv2.FILE_STORAGE_READ)


        self.cameraMatrix = cv_file.getNode("cameraMatrix").mat()
        self.distCoeffs = cv_file.getNode("distCoeffs").mat()
        # firestorage doesnt support integer, so load it as real and convert it to int
        self.imageSize = (int(cv_file.getNode("imageSize").at(0).real()), int(cv_file.getNode("imageSize").at(1).real()))
        self.boardSize = (int(cv_file.getNode("boardSize_width").real()), int(cv_file.getNode("boardSize_height").real()))
        self.squareSize = int(cv_file.getNode("squareSize").real())
        self.nofCalibrationImages = cv_file.getNode("reprojectionPointsMAE").size()
        self.intrinsicRMSE = cv_file.getNode("intrinsicRMSE").real()
        self.avgMAE = cv_file.getNode("avgMAE").real()
        self.individualMAEs = np.array([cv_file.getNode("reprojectionPointsMAE").at(i).real() for i in range(cv_file.getNode("reprojectionPointsMAE").size())])

        cv_file.release()

        # additional calculations for undistortion maps
        self.newCameraMatrix = cv2.getOptimalNewCameraMatrix(self.cameraMatrix, self.distCoeffs, self.imageSize, 1)[0]

        self.map1, self.map2 = cv2.initUndistortRectifyMap(self.cameraMatrix, self.distCoeffs, None, self.newCameraMatrix, self.imageSize, 5)

        # get node retrieves a entity, we also have to specify the type to retrieve other wise we only get a FileNode object back instead of a matrix
        self.printMeta()


    def printMeta(self):
        # intrinsicRMSE avgMAE reprojectionPointsMAE
        print('\n############# Single Calbration #############')
        print('File:', self.file_path)
        print('Boardsize:', self.boardSize)
        print('Squaresize:', self.squareSize)
        print('Imagesize:', self.imageSize)
        print('Number of calibration images:', self.nofCalibrationImages)
        print('Intrinsic RMSE:', self.intrinsicRMSE)
        print('Avg. MAE [px]:', self.avgMAE)
        print('Indiv. MAE [px]:', self.individualMAEs)
        print('##############################################\n')


    def undistortImage(self, img):

        if self.map1 is None or self.map2 is None:
            return img
        else:
            return cv2.remap(img, self.map1, self.map2, cv2.INTER_LINEAR)



    def undistortPupilSize(self, pupil):

        if self.cameraMatrix is None or not pupil.valid(-2):
            return pupil.diameter()


        rotPupil = pupil
        rotPupil.angle += 360-rotPupil.angle

        # Select the top left and top right corner of the bounding rects of the pupils as the points we undistort
        # rotatedRect points in order: bottomLeft, topLeft, topRight, bottomRight
        mainPointsArr = rotPupil.rectPoints()

        secondPoint = 2 if rotPupil.width() > rotPupil.height() else 0 # if the pupil major axis is horizontal use topLeft and topRight, else topLeft and bottomLeft

        mainPoints = [mainPointsArr[1], mainPointsArr[secondPoint]]

        undistCornerPointsBuf = cv2.undistortPoints(np.array(mainPoints), self.cameraMatrix, self.distCoeffs, R=None, P=self.newCameraMatrix)

        return cv2.norm(undistCornerPointsBuf[0] - undistCornerPointsBuf[1])

