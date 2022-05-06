# ifndef __NDARRAY_CONVERTER_H__
# define __NDARRAY_CONVERTER_H__

#include <Python.h>
#include <opencv2/core/core.hpp>


class NDArrayConverter {
public:
    // must call this first, or the other routines don't work!
    static bool init_numpy();

    static bool toMat(PyObject* o, cv::Mat &m);
    static PyObject* toNDArray(const cv::Mat& mat);
};

//
// Define the type converter
//

#include <pybind11/pybind11.h>
#include <pybind11/cast.h>
#include <pybind11/pytypes.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
// Used sources while implementing this header file
// Reference 1:
//...

namespace pybind11 { namespace detail {

        template <typename Sequence>
        inline array_t<typename Sequence::value_type> to_pyarray(const Sequence& seq) {
            return pybind11::array(seq.size(), seq.data());
        }

        template <> struct type_caster<cv::Mat> {
        public:

            PYBIND11_TYPE_CASTER(cv::Mat, _("numpy.ndarray"));

            bool load(handle src, bool) {
                return NDArrayConverter::toMat(src.ptr(), value);
            }

            static handle cast(const cv::Mat &m, return_value_policy, handle defval) {
                return handle(NDArrayConverter::toNDArray(m));
            }
        };

        template<class T>
        struct type_caster<cv::Point_<T>>{

        PYBIND11_TYPE_CASTER(cv::Point_<T>, _("tuple_xy"));

            bool load(handle obj, bool){
                if(!isinstance<tuple>(obj)){
                    std::logic_error("Point(x,y) should be a tuple!");
                    return false;
                }

                tuple pt = reinterpret_borrow<tuple>(obj);
                if(pt.size()!=2){
                    std::logic_error("Point(x,y) tuple should be size of 2");
                    return false;
                }

                value = cv::Point_<T>(pt[0].cast<T>(), pt[1].cast<T>());
                return true;
            }

            static handle cast(const cv::Point_<T>& pt, return_value_policy, handle){
                return make_tuple(pt.x, pt.y).release();
            }
        };

        template<class T>
        struct type_caster<cv::Rect_<T>>{
        PYBIND11_TYPE_CASTER(cv::Rect_<T>, _("tuple_xywh"));

            bool load(handle obj, bool){
                if(!isinstance<tuple>(obj)){
                    std::logic_error("Rect should be a tuple!");
                    return false;
                }
                tuple rect = reinterpret_borrow<tuple>(obj);
                if(rect.size()!=4){
                    std::logic_error("Rect (x,y,w,h) tuple should be size of 4");
                    return false;
                }

                value = cv::Rect_<T>(rect[0].cast<T>(), rect[1].cast<T>(), rect[2].cast<T>(), rect[3].cast<T>());
                return true;
            }

            static handle cast(const cv::Rect_<T>& rect, return_value_policy, handle){
                return make_tuple(rect.x, rect.y, rect.width, rect.height).release();
            }
        };

        template<class T>
        struct type_caster<cv::Size_<T>>{

        PYBIND11_TYPE_CASTER(cv::Size_<T>, _("tuple_xy"));

            bool load(handle obj, bool){
                if(!isinstance<tuple>(obj)){
                    std::logic_error("Size(w,h) should be a tuple!");
                    return false;
                }

                tuple pt = reinterpret_borrow<tuple>(obj);
                if(pt.size()!=2){
                    std::logic_error("Size(w,h) tuple should be size of 2");
                    return false;
                }

                value = cv::Size_<T>(pt[0].cast<T>(), pt[1].cast<T>());
                return true;
            }

            static handle cast(const cv::Size_<T>& pt, return_value_policy, handle){
                return make_tuple(pt.width, pt.height).release();
            }
        };

    }} // namespace pybind11::detail

# endif