#include <iostream>
#include "rpigpio.h"

int main(int argc, char** argv)
{
    RpiHAL* pRpiHal = new RpiHAL();

    std::cout << pRpiHal->GetPeriphal().pMap << std::endl;
}