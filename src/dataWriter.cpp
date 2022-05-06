#include <iostream>
#include "dataWriter.h"


DataWriter::DataWriter(const std::string& fileName) : dataFile() {

    header = "filename,timestamp[ms],diameter[px],physicaldiameter[mm],width[px],height[px],center_x,center_y,angle[deg],circumference[px],confidence,outline_confidence";

    //QString fileName = path + '/'+ tag + '_' + method + "_data.csv";

    std::cout<<fileName<<std::endl;

    dataFile.open(fileName, std::ofstream::out | std::ofstream::trunc);

    if (!dataFile.good() || !dataFile.is_open()) {
        std::cout << "Data writer failure. Could not open: " << fileName << std::endl;
        dataFile.close();
        return;
    }

    dataFile << header << std::endl;
}

DataWriter::~DataWriter() {
    dataFile.close();
}

void DataWriter::close() {

    dataFile.close();
}

void DataWriter::appendPupilData(uint64 timestamp, const Pupil &pupil, const std::string &filename) {

    if (dataFile.good() && dataFile.is_open()) {
        dataFile<<pupilToQString(timestamp, pupil, filename)<<std::endl;
    }
}

std::string DataWriter::pupilToQString(uint64 timestamp, const Pupil &pupil, const std::string &filepath) {

    return filepath + ',' + std::to_string(timestamp) + ',' + std::to_string(pupil.diameter()) + ',' + std::to_string(pupil.physicalDiameter) + ',' + std::to_string(pupil.width()) + ',' + std::to_string(pupil.height())
        + ',' + std::to_string(pupil.center.x) + ',' + std::to_string(pupil.center.y) + ',' + std::to_string(pupil.angle)
        + ',' + std::to_string(pupil.circumference()) + ',' + std::to_string(pupil.confidence) + ',' + std::to_string(pupil.outline_confidence);
}

void DataWriter::writePupilData(const std::vector<Pupil>& pupilData) {

    int framePos = 0;
    for(const auto& pupil: pupilData) {
        if (dataFile.good() && dataFile.is_open()) {
            dataFile<<pupilToQString(framePos, pupil, "")<<std::endl;
        }
        ++framePos;
    }
}
