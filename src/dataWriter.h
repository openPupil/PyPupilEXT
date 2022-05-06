#ifndef PUPILALGOSIMPLE_DATAWRITER_H
#define PUPILALGOSIMPLE_DATAWRITER_H

#include "pupil-detection-methods/Pupil.h"
#include <fstream>

class DataWriter {

public:

    explicit DataWriter(const std::string& fileName);
    ~DataWriter();

    void writePupilData(const std::vector<Pupil>& pupilData);
    void appendPupilData(uint64 timestamp, const Pupil &pupil, const std::string &filename);
    void close();

private:

    std::string method;
    std::string header;

    std::ofstream dataFile;

    static std::string pupilToQString(uint64 timestamp, const Pupil &pupil, const std::string &filepath);

};


#endif //PUPILALGOSIMPLE_DATAWRITER_H
