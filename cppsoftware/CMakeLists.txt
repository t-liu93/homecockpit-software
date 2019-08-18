cmake_minimum_required(VERSION 3.10)

# project name
project(homecockpit-software)

# add option to set cross compiler
option(COMPILE_PI "choose compiler for raspberry pi" ON)

# cross compiler settings
if(COMPILE_PI)
    set(CMAKE_SYSTEM_NAME Linux)
    set(CMAKE_SYSTEM_PROCESSOR arm)
    set(CMAKE_C_COMPILER arm-linux-gnueabihf-gcc)
    set(CMAKE_CXX_COMPILER arm-linux-gnueabihf-g++)
    SET(CMAKE_FIND_ROOT_PATH arm-linux-gnueabihf)
endif()

# include diretories for the top level application
include_directories(rpihw/gpio/inc)

# sub directories
add_subdirectory(rpihw)

# source dirs
set(SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/rpihaltest.cpp)

# targets
add_executable(rpitest ${SOURCES})
target_link_libraries(rpitest rpigpio rpii2c)

add_custom_target(testonpi DEPENDS rpitest)
add_custom_command(TARGET testonpi
                POST_BUILD
                COMMAND scp rpitest jamespi:)