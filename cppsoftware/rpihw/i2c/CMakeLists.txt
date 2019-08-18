include_directories(inc)

set(SOURCEDIR ${CMAKE_CURRENT_SOURCE_DIR}/src)

set(SOURCES ${SOURCEDIR}/rpii2c.cpp)

add_library(rpii2c ${SOURCES})