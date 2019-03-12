cmake_minimum_required (VERSION 3.1)
set (CMAKE_CXX_STANDARD 11)
project (test-tesseract)
add_executable(Basic basic.cpp)
target_link_libraries (Basic lept tesseract)

add_executable(GetComponent getcomp.cpp)
target_link_libraries (GetComponent lept tesseract)

add_executable(WordIter worditer.cpp)
target_link_libraries (WordIter lept tesseract)

add_executable(BasicCn basiccn.cpp)
target_link_libraries (BasicCn lept tesseract)

add_executable(Osd osd.cpp)
target_link_libraries (Osd lept tesseract)

add_executable(ClassIter clsiter.cpp)
target_link_libraries (ClassIter lept tesseract)