import cv2
import numpy as np

# look into mixing python code with the c++ module
# https://stackoverflow.com/questions/54317280/how-to-mix-python-code-into-a-python-extension-module



class StereoCalibration:

    def __init__(self, file_path):

        # load calibration file
        # FILE_STORAGE_READ
        self.file_path = file_path

        cv_file = cv2.FileStorage(file_path, cv2.FILE_STORAGE_READ)

        # get node retrieves a entity, we also have to specify the type to retrieve other wise we only get a FileNode object back instead of a matrix

        self.cameraMatrix = cv_file.getNode("cameraMatrix").mat()
        self.distCoeffs = cv_file.getNode("distCoeffs").mat()
        self.imageSize = (int(cv_file.getNode("imageSize").at(0).real()), int(cv_file.getNode("imageSize").at(1).real()))
        self.boardSize = (int(cv_file.getNode("boardSize_width").real()), int(cv_file.getNode("boardSize_height").real()))
        self.squareSize = int(cv_file.getNode("squareSize").real())
        self.nofCalibrationImages = cv_file.getNode("reprojectionWorldPointsMAE").size()
        self.intrinsicRMSE = (cv_file.getNode("intrinsicRMSE").real(), cv_file.getNode("intrinsicRMSESec").real()) 
        self.avgMAE = (cv_file.getNode("avgMAE").real(), cv_file.getNode("avgMAESec").real())
        #self.individualMAEs = np.array([cv_file.getNode("reprojectionPointsMAE").at(i).real() for i in range(cv_file.getNode("reprojectionPointsMAE").size())])
        self.stereoRMSE = cv_file.getNode("stereoRMSE").real()
        self.avgWorldMAE = abs(cv_file.getNode("avgWorldMAE").real()-self.squareSize)
        self.individualWorldMAEs = np.array([abs(cv_file.getNode("reprojectionWorldPointsMAE").at(i).real()-self.squareSize) for i in range(cv_file.getNode("reprojectionWorldPointsMAE").size())])

        self.cameraMatrixSecondary = cv_file.getNode("cameraMatrixSecondary").mat()
        self.distCoeffsSecondary = cv_file.getNode("distCoeffsSecondary").mat()

        self.rotationMatrix = cv_file.getNode("rotationMatrix").mat()
        self.translationMatrix = cv_file.getNode("translationMatrix").mat()

        self.essentialMatrix = cv_file.getNode("essentialMatrix").mat()
        self.fundamentalMatrix = cv_file.getNode("fundamentalMatrix").mat()

        self.rectificationTransform = cv_file.getNode("rectificationTransform").mat()
        self.rectificationTransformSecondary = cv_file.getNode("rectificationTransformSecondary").mat()

        self.projectionMatrix = cv_file.getNode("projectionMatrix").mat()
        self.projectionMatrixSecondary = cv_file.getNode("projectionMatrixSecondary").mat()


        cv_file.release()

        self.printMeta()


        self.newCameraMatrix = cv2.getOptimalNewCameraMatrix(self.cameraMatrix, self.distCoeffs, self.imageSize, 1, self.imageSize, 0)[0]
        self.newCameraMatrixSecondary = cv2.getOptimalNewCameraMatrix(self.cameraMatrixSecondary, self.distCoeffsSecondary, self.imageSize, 1, self.imageSize, 0)[0]

        self.map1, self.map2 = cv2.initUndistortRectifyMap(self.cameraMatrix, self.distCoeffs, None, self.newCameraMatrix, self.imageSize, 5)
        self.map1Sec, self.map2Sec = cv2.initUndistortRectifyMap(self.cameraMatrixSecondary, self.distCoeffsSecondary, None, self.newCameraMatrixSecondary, self.imageSize, 5)


    def printMeta(self):
        # intrinsicRMSE avgMAE reprojectionPointsMAE
        print('\n############# Stereo Calibration #############')
        print('File:', self.file_path)
        print('Boardsize:', self.boardSize)
        print('Squaresize:', self.squareSize)
        print('Imagesize:', self.imageSize)
        print('Number of calibration images:', self.nofCalibrationImages)
        print('Intrinsic RMSE (main, secondary):', self.intrinsicRMSE)
        print('Avg. MAE [px] (main, secondary):', self.avgMAE)
        print('Stereo RMSE:', self.stereoRMSE)
        print('Stereo MAE [mm]:', self.avgWorldMAE)
        print('Indiv. Stereo MAE [mm]:', self.individualWorldMAEs)
        print('##############################################\n')


    def undistortImages(self, img, imgSecondary):

        if self.map1 is None or self.map2 is None:
            return img, imgSecondary
        else:
            return cv2.remap(img, self.map1, self.map2, cv2.INTER_LINEAR), cv2.remap(img, self.map1Sec, self.map2Sec, cv2.INTER_LINEAR)


    def undistortPupilSizes(self, pupil, pupilSecondary):

        if self.cameraMatrix is None or self.cameraMatrixSecondary is None or not pupil.valid(-2):
            return pupil.diameter(), pupilSecondary.diameter()


        rotPupil = pupil
        rotPupil.angle += 360-rotPupil.angle

        rotPupilSecondary = pupilSecondary
        rotPupilSecondary.angle += 360-rotPupilSecondary.angle

        mainPointsArr = rotPupil.rectPoints()
        secondaryPointsArr = rotPupilSecondary.rectPoints()

        secondPoint = 2 if rotPupil.width() > rotPupil.height() else 0 # if the pupil major axis is horizontal use topLeft and topRight, else topLeft and bottomLeft

        mainPoints = [mainPointsArr[1], mainPointsArr[secondPoint]]
        secondaryPoints = [secondaryPointsArr[1], secondaryPointsArr[secondPoint]]

        undistCornerPointsBuf = cv2.undistortPoints(np.array(mainPoints), self.cameraMatrix, self.distCoeffs, R=None, P=self.newCameraMatrix)
        undistCornerPointsBufSecondary = cv2.undistortPoints(np.array(secondaryPoints), self.cameraMatrixSecondary, self.distCoeffsSecondary, R=None, P=self.newCameraMatrixSecondary)

        return cv2.norm(undistCornerPointsBuf[0] - undistCornerPointsBuf[1]), cv2.norm(undistCornerPointsBufSecondary[0] - undistCornerPointsBufSecondary[1])


    def triangulatePupilSize(self, pupil, pupilSecondary):

        if self.cameraMatrix is None or self.cameraMatrixSecondary is None or not pupil.valid(-2) or not pupilSecondary.valid(-2):
            return -1.0

        rotPupil = pupil
        rotPupil.angle += 360-rotPupil.angle

        rotPupilSecondary = pupilSecondary
        rotPupilSecondary.angle += 360-rotPupilSecondary.angle

        mainPointsArr = rotPupil.rectPoints()
        secondaryPointsArr = rotPupilSecondary.rectPoints()

        secondPoint = 2 if rotPupil.width() > rotPupil.height() else 0 # if the pupil major axis is horizontal use topLeft and topRight, else topLeft and bottomLeft

        mainPoints = [mainPointsArr[1], mainPointsArr[secondPoint]]
        secondaryPoints = [secondaryPointsArr[1], secondaryPointsArr[secondPoint]]

        undistCornerPointsBuf = cv2.undistortPoints(np.array(mainPoints), self.cameraMatrix, self.distCoeffs, R=self.rectificationTransform, P=self.projectionMatrix)
        undistCornerPointsBufSecondary = cv2.undistortPoints(np.array(secondaryPoints), self.cameraMatrixSecondary, self.distCoeffsSecondary, R=self.rectificationTransformSecondary, P=self.projectionMatrixSecondary)

        homogenPoints = cv2.triangulatePoints(self.projectionMatrix, self.projectionMatrixSecondary, undistCornerPointsBuf, undistCornerPointsBufSecondary)

        worldPoints = []

        for row in homogenPoints.T:
            scale = row[3] if row[3] != 0 else 1.0
            worldPoints.append([row[0]/scale, row[1]/scale, row[2]/scale])

        worldPoints = np.array(worldPoints)
        
        return cv2.norm(worldPoints[0] - worldPoints[1])





