#include <iostream>
#include <thread>
#include <chrono>
#include "rpigpio.h"

int main(int argc, char** argv)
{
    uint32_t buttonGPIO = 18;
    while (true)
    {
        std::cout << RpiGPIOMapping::GetInstance()->ReadGPIO(buttonGPIO) << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }

    return 0;
}