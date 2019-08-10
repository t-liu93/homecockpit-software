cmake_minimum_required(VERSION 3.10)

project(homecockpit-software)

option(COMPILE_PI "choose compiler for raspberry pi" ON)

if(COMPILE_PI)
    set(CMAKE_SYSTEM_NAME Linux)
    set(CMAKE_SYSTEM_PROCESSOR arm)
    set(CMAKE_C_COMPILER arm-linux-gnueabihf-gcc)
    set(CMAKE_CXX_COMPILER arm-linux-gnueabihf-g++)
    SET(CMAKE_FIND_ROOT_PATH arm-linux-gnueabihf)
endif()

include_directories(hal/inc)

add_subdirectory(hal)

set(SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/rpihaltest.cpp)

add_executable(rpitest ${SOURCES})
target_link_libraries(rpitest rpihal)

add_custom_target(testonpi DEPENDS rpitest)
add_custom_command(TARGET testonpi
                POST_BUILD
                COMMAND scp rpitest jamespi:)