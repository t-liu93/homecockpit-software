#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <iostream>
#include "rpigpio.h"

RpiGPIOMapping* RpiGPIOMapping::m_pInstance = nullptr;

RpiGPIOMapping* RpiGPIOMapping::GetInstance()
{
    if (!m_pInstance)
    {
        m_pInstance = new RpiGPIOMapping();
    }

    return m_pInstance;
}

RpiGPIOMapping::RpiGPIOMapping()
{
    m_memFd = open("/dev/mem", O_RDWR | O_SYNC);
    if (m_memFd < 0)
    {
        std::cerr << "/dev/mem open failed.. exiting" << std::endl;
        exit(EXIT_FAILURE);
    }

    m_pGPIOBase = (gpioreg_t*) mmap(NULL, BLOCK_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, m_memFd, GPIO_BASE);

    if (m_pGPIOBase == MAP_FAILED)
    {
        std::cerr << "mapping failed" << std::endl;
        exit(EXIT_FAILURE);
    }
    close(m_memFd);
}

RpiGPIOMapping::~RpiGPIOMapping()
{
    std::clog << "Unmapping." << std::endl;
    munmap((void*)m_pGPIOBase, BLOCK_SIZE);
}

void RpiGPIOMapping::SetInput(uint32_t GPIOPin)
{
    *GetGPIOFunctionSelector(GPIOPinToFunctionSelectorIndex(GPIOPin)) 
        &= ~(7 << GPIOPinBitLocation(GPIOPin));
}

void RpiGPIOMapping::SetOutput(uint32_t GPIOPin)
{
    *GetGPIOFunctionSelector(GPIOPinToFunctionSelectorIndex(GPIOPin)) 
        |= (1 << GPIOPinBitLocation(GPIOPin));
}

gpio_t RpiGPIOMapping::ReadGPIO(uint32_t GPIOPin)
{

    if (GPIOPin <= 31)
    {
        return ((m_pGPIOBase[13] & (1 << GPIOPin)) > 0)? HIGH : LOW;
    }
    else
    {
        return ((m_pGPIOBase[14] & (1 << GPIOPin - 32)) > 0)? HIGH : LOW;
    }
}