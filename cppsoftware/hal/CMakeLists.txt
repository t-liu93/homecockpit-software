include_directories(inc)

set(SOURCEDIR ${CMAKE_CURRENT_SOURCE_DIR}/src)

set(SOURCES ${SOURCEDIR}/rpigpio.cpp)


add_library(rpihal ${SOURCES})