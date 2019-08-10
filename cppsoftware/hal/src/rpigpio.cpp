#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <iostream>
#include "rpigpio.h"

RpiHAL::RpiHAL()
{
    m_periphal.mem_fd = open("/dev/mem", O_RDWR | O_SYNC);
    if (m_periphal.mem_fd < 0)
    {
        std::cerr << "/dev/mem open failed.. exiting" << std::endl;
        exit(EXIT_FAILURE);
    }

    m_periphal.pAddr = GPIO_BASE;
    m_periphal.pMap = mmap(NULL, BLOCK_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, m_periphal.mem_fd, m_periphal.pAddr);

    if (m_periphal.pMap == MAP_FAILED)
    {
        std::cerr << "mapping failed" << std::endl;
        exit(EXIT_FAILURE);
    }
    close(m_periphal.mem_fd);
}

RpiHAL::~RpiHAL()
{
    // unmap
    munmap(m_periphal.pMap, BLOCK_SIZE);
}