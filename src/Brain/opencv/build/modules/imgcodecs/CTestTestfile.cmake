# CMake generated Testfile for 
# Source directory: /home/bb/Brain/opencv/opencv-4.x/modules/imgcodecs
# Build directory: /home/bb/Brain/opencv/build/modules/imgcodecs
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_imgcodecs "/home/bb/Brain/opencv/build/bin/opencv_test_imgcodecs" "--gtest_output=xml:opencv_test_imgcodecs.xml")
set_tests_properties(opencv_test_imgcodecs PROPERTIES  LABELS "Main;opencv_imgcodecs;Accuracy" WORKING_DIRECTORY "/home/bb/Brain/opencv/build/test-reports/accuracy" _BACKTRACE_TRIPLES "/home/bb/Brain/opencv/opencv-4.x/cmake/OpenCVUtils.cmake;1799;add_test;/home/bb/Brain/opencv/opencv-4.x/cmake/OpenCVModule.cmake;1365;ocv_add_test_from_target;/home/bb/Brain/opencv/opencv-4.x/modules/imgcodecs/CMakeLists.txt;201;ocv_add_accuracy_tests;/home/bb/Brain/opencv/opencv-4.x/modules/imgcodecs/CMakeLists.txt;0;")
add_test(opencv_perf_imgcodecs "/home/bb/Brain/opencv/build/bin/opencv_perf_imgcodecs" "--gtest_output=xml:opencv_perf_imgcodecs.xml")
set_tests_properties(opencv_perf_imgcodecs PROPERTIES  LABELS "Main;opencv_imgcodecs;Performance" WORKING_DIRECTORY "/home/bb/Brain/opencv/build/test-reports/performance" _BACKTRACE_TRIPLES "/home/bb/Brain/opencv/opencv-4.x/cmake/OpenCVUtils.cmake;1799;add_test;/home/bb/Brain/opencv/opencv-4.x/cmake/OpenCVModule.cmake;1264;ocv_add_test_from_target;/home/bb/Brain/opencv/opencv-4.x/modules/imgcodecs/CMakeLists.txt;212;ocv_add_perf_tests;/home/bb/Brain/opencv/opencv-4.x/modules/imgcodecs/CMakeLists.txt;0;")
add_test(opencv_sanity_imgcodecs "/home/bb/Brain/opencv/build/bin/opencv_perf_imgcodecs" "--gtest_output=xml:opencv_perf_imgcodecs.xml" "--perf_min_samples=1" "--perf_force_samples=1" "--perf_verify_sanity")
set_tests_properties(opencv_sanity_imgcodecs PROPERTIES  LABELS "Main;opencv_imgcodecs;Sanity" WORKING_DIRECTORY "/home/bb/Brain/opencv/build/test-reports/sanity" _BACKTRACE_TRIPLES "/home/bb/Brain/opencv/opencv-4.x/cmake/OpenCVUtils.cmake;1799;add_test;/home/bb/Brain/opencv/opencv-4.x/cmake/OpenCVModule.cmake;1265;ocv_add_test_from_target;/home/bb/Brain/opencv/opencv-4.x/modules/imgcodecs/CMakeLists.txt;212;ocv_add_perf_tests;/home/bb/Brain/opencv/opencv-4.x/modules/imgcodecs/CMakeLists.txt;0;")
