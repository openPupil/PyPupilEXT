#include <pybind11/pybind11.h>

#include <Pupil.h>
#include <PupilDetectionMethod.h>
#include <APPD.h>
#include <ElSe.h>
#include <ExCuSe.h>
#include <PuRe.h>
#include <PuReST.h>
#include <Starburst.h>
#include <Swirski2D.h>

#include "type_converter.h"
#include "dataWriter.h"

namespace py = pybind11;

using namespace APPD_DEFS;

PYBIND11_MODULE(_pypupil, m) {

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif

    NDArrayConverter::init_numpy();

    py::class_<Pupil>(m, "Pupil")
            .def(py::init<>())
            .def_readwrite("confidence", &Pupil::confidence)
            .def_readwrite("outline_confidence", &Pupil::outline_confidence)
            .def_readwrite("eyelid", &Pupil::eyelid)
            .def_readwrite("physicalDiameter", &Pupil::physicalDiameter)
            .def_readwrite("undistortedDiameter", &Pupil::undistortedDiameter)
            .def_readwrite("angle", &Pupil::angle)
            .def_readwrite("center", &Pupil::center)
            .def_readwrite("size", &Pupil::size)
            .def("rectPoints", &Pupil::rectPoints)
            .def("shift", &Pupil::shift)
            .def("valid", &Pupil::valid)
            .def("set", (void (Pupil::*)(const float &, const float &)) &Pupil::resize)
            .def("set", (void (Pupil::*)(const float &)) &Pupil::resize)
            .def("hasOutline", &Pupil::hasOutline)
            .def("width", &Pupil::width)
            .def("height", &Pupil::height)
            .def("majorAxis", &Pupil::majorAxis)
            .def("minorAxis", &Pupil::minorAxis)
            .def("diameter", &Pupil::diameter)
            .def("circumference", &Pupil::circumference)
            .def("clear", &Pupil::clear);

    py::class_<DataWriter>(m, "DataWriter")
            .def(py::init<const std::string&>())
            .def("writePupilData", &DataWriter::writePupilData)
            .def("appendPupilData", &DataWriter::appendPupilData)
            .def("close", &DataWriter::close);

    py::class_<PupilDetectionMethod>(m, "PupilDetectionMethod")
            //.def(py::init<>())
            .def("title", &PupilDetectionMethod::title)
            .def("description", &PupilDetectionMethod::description)
            .def("hasConfidence", &PupilDetectionMethod::hasConfidence)
            .def("hasCoarseLocation", &PupilDetectionMethod::hasCoarseLocation)
            .def("hasInliers", &PupilDetectionMethod::hasInliers)
            .def("runWithConfidence", (void (PupilDetectionMethod::*)(const cv::Mat &, Pupil &)) &PupilDetectionMethod::runWithConfidence)
            .def("runWithConfidence", (Pupil (PupilDetectionMethod::*)(const cv::Mat &)) &PupilDetectionMethod::runWithConfidence)
            .def("runWithConfidence", (void (PupilDetectionMethod::*)(const cv::Mat &, const cv::Rect &, Pupil &, const float &, const float &)) &PupilDetectionMethod::runWithConfidence)

            .def("run", (Pupil (PupilDetectionMethod::*)(const cv::Mat &)) &PupilDetectionMethod::run)
            .def("run", (void (PupilDetectionMethod::*)(const cv::Mat &, Pupil &)) &PupilDetectionMethod::run)
            .def("run", (void (PupilDetectionMethod::*)(const cv::Mat &, const cv::Rect &, Pupil &, const float &, const float &)) &PupilDetectionMethod::run)

            .def_static("outlineContrastConfidence", &PupilDetectionMethod::outlineContrastConfidence)
            .def_static("coarsePupilDetection", &PupilDetectionMethod::coarsePupilDetection)
            .def_static("edgeRatioConfidence", &PupilDetectionMethod::edgeRatioConfidence)
            .def_static("angularSpreadConfidence", &PupilDetectionMethod::angularSpreadConfidence)
            .def_static("aspectRatioConfidence", &PupilDetectionMethod::aspectRatioConfidence)
            .def_static("ellipse2Points", &PupilDetectionMethod::ellipse2Points);


    py::class_<APPD, PupilDetectionMethod>(m, "APPD")
            .def(py::init<>())
            .def("hasConfidence", &APPD::hasConfidence)
            .def("hasCoarseLocation", &APPD::hasCoarseLocation)
            .def("hasInliers", &APPD::hasInliers)

            .def("getEDParameter", &APPD::getEDParameter)
            .def("getSegmentParameter", &APPD::getSegmentParameter)
            .def("getCornerParameter", &APPD::getCornerParameter)
            .def("setEDParameter", &APPD::setEDParameter)
            .def("setSegmentParameter", &APPD::setSegmentParameter)
            .def("setCornerParameter", &APPD::setCornerParameter)
            .def("sortedAnchorsEnabled", &APPD::sortedAnchorsEnabled)
            .def("enableSortedAnchors", &APPD::enableSortedAnchors)
            .def("validateSegmentsEnabled", &APPD::validateSegmentsEnabled)
            .def("enableValidateSegments", &APPD::enableValidateSegments)
            .def("downscalingEnabled", &APPD::downscalingEnabled)
            .def("enableDownscaling", &APPD::enableDownscaling)

            .def("run", (Pupil (APPD::*)(const cv::Mat &)) &APPD::run)
            .def("run", (void (PupilDetectionMethod::*)(const cv::Mat &, Pupil &)) &PupilDetectionMethod::run)
            .def("run", (void (APPD::*)(const cv::Mat &, const cv::Rect &, Pupil &, const float &, const float &)) &APPD::run);


    py::class_<ElSe, PupilDetectionMethod>(m, "ElSe")
            .def(py::init<>())
            .def_readwrite("minAreaRatio", &ElSe::minAreaRatio)
            .def_readwrite("maxAreaRatio", &ElSe::maxAreaRatio)

            .def("hasConfidence", &ElSe::hasConfidence)
            .def("hasCoarseLocation", &ElSe::hasCoarseLocation)
            .def("hasInliers", &ElSe::hasInliers)

            .def("run", (Pupil (ElSe::*)(const cv::Mat &)) &ElSe::run)
            .def("run", (void (PupilDetectionMethod::*)(const cv::Mat &, Pupil &)) &PupilDetectionMethod::run)
            .def("run", (void (ElSe::*)(const cv::Mat &, const cv::Rect &, Pupil &, const float &, const float &)) &ElSe::run);


    py::class_<ExCuSe, PupilDetectionMethod>(m, "ExCuSe")
            .def(py::init<>())
            .def_readwrite("max_ellipse_radi", &ExCuSe::max_ellipse_radi)
            .def_readwrite("good_ellipse_threshold", &ExCuSe::good_ellipse_threshold)

            .def("hasConfidence", &ExCuSe::hasConfidence)
            .def("hasCoarseLocation", &ExCuSe::hasCoarseLocation)
            .def("hasInliers", &ExCuSe::hasInliers)

            .def("run", (Pupil (ExCuSe::*)(const cv::Mat &)) &ExCuSe::run)
            .def("run", (void (PupilDetectionMethod::*)(const cv::Mat &, Pupil &)) &PupilDetectionMethod::run)
            .def("run", (void (ExCuSe::*)(const cv::Mat &, const cv::Rect &, Pupil &, const float &, const float &)) &ExCuSe::run);


    py::class_<PuRe, PupilDetectionMethod>(m, "PuRe")
            .def(py::init<>())
            .def_readwrite("meanCanthiDistanceMM", &PuRe::meanCanthiDistanceMM)
            .def_readwrite("maxPupilDiameterMM", &PuRe::maxPupilDiameterMM)
            .def_readwrite("minPupilDiameterMM", &PuRe::minPupilDiameterMM)
            .def_readwrite("baseSize", &PuRe::baseSize)

            .def("hasPupilOutline", &PuRe::hasPupilOutline)
            .def("hasConfidence", &PuRe::hasConfidence)
            .def("hasCoarseLocation", &PuRe::hasCoarseLocation)
            .def("hasInliers", &PuRe::hasInliers)

            .def("run", (Pupil (PuRe::*)(const cv::Mat &)) &PuRe::run)
            .def("run", (void (PuRe::*)(const cv::Mat &, Pupil &)) &PuRe::run)
            .def("run", (void (PuRe::*)(const cv::Mat &, const cv::Rect &, Pupil &, const float &, const float &)) &PuRe::run);


    py::class_<PuReST, PupilDetectionMethod>(m, "PuReST")
            .def(py::init<>())
            .def_readwrite("meanCanthiDistanceMM", &PuReST::meanCanthiDistanceMM)
            .def_readwrite("maxPupilDiameterMM", &PuReST::maxPupilDiameterMM)
            .def_readwrite("minPupilDiameterMM", &PuReST::minPupilDiameterMM)
            .def_readwrite("baseSize", &PuReST::baseSize)

            .def("hasPupilOutline", &PuReST::hasPupilOutline)
            .def("hasConfidence", &PuReST::hasConfidence)
            .def("hasCoarseLocation", &PuReST::hasCoarseLocation)
            .def("hasInliers", &PuReST::hasInliers)

            .def("reset", &PuReST::reset)

            .def("run", (Pupil (PuReST::*)(const cv::Mat &)) &PuReST::run)
            .def("run", (void (PuReST::*)(const cv::Mat &, Pupil &)) &PuReST::run)
            .def("run", (void (PuReST::*)(const cv::Mat &, const cv::Rect &, Pupil &, const float &, const float &)) &PuReST::run)
            .def("runTracking", &PuReST::runTracking);


    py::class_<Starburst, PupilDetectionMethod>(m, "Starburst")
            .def(py::init<>())
            .def_readwrite("edge_threshold", &Starburst::edge_threshold)
            .def_readwrite("rays", &Starburst::rays)
            .def_readwrite("min_feature_candidates", &Starburst::min_feature_candidates)
            .def_readwrite("corneal_reflection_ratio_to_image_size", &Starburst::corneal_reflection_ratio_to_image_size)
            .def_readwrite("crWindowSize", &Starburst::crWindowSize)

            .def("hasConfidence", &Starburst::hasConfidence)
            .def("hasCoarseLocation", &Starburst::hasCoarseLocation)
            .def("hasInliers", &Starburst::hasInliers)

            .def("run", (Pupil (Starburst::*)(const cv::Mat &)) &Starburst::run)
            .def("run", (void (Starburst::*)(const cv::Mat &, Pupil &)) &Starburst::run);


    py::class_<TrackerParams>(m, "TrackerParams")
            .def_readwrite("Radius_Min", &TrackerParams::Radius_Min)
            .def_readwrite("Radius_Max", &TrackerParams::Radius_Max)
            .def_readwrite("CannyBlur", &TrackerParams::CannyBlur)
            .def_readwrite("CannyThreshold1", &TrackerParams::CannyThreshold1)
            .def_readwrite("CannyThreshold2", &TrackerParams::CannyThreshold2)
            .def_readwrite("StarburstPoints", &TrackerParams::StarburstPoints)
            .def_readwrite("PercentageInliers", &TrackerParams::PercentageInliers)
            .def_readwrite("InlierIterations", &TrackerParams::InlierIterations)
            .def_readwrite("ImageAwareSupport", &TrackerParams::ImageAwareSupport)
            .def_readwrite("EarlyTerminationPercentage", &TrackerParams::EarlyTerminationPercentage)
            .def_readwrite("EarlyRejection", &TrackerParams::EarlyRejection)
            .def_readwrite("Seed", &TrackerParams::Seed);

    py::class_<Swirski2D, PupilDetectionMethod>(m, "Swirski2D")
            .def(py::init<>())
            .def_readwrite("params", &Swirski2D::params)

            .def("hasConfidence", &Swirski2D::hasConfidence)
            .def("hasCoarseLocation", &Swirski2D::hasCoarseLocation)
            .def("hasInliers", &Swirski2D::hasInliers)

            .def("run", (Pupil (Swirski2D::*)(const cv::Mat &)) &Swirski2D::run)
            .def("run", (void (Swirski2D::*)(const cv::Mat &, Pupil &)) &Swirski2D::run)
            .def("run", (void (Swirski2D::*)(const cv::Mat &, const cv::Rect &, Pupil &, const float &, const float &)) &Swirski2D::run);

}