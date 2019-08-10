#include <stdlib.h>

// Raspberry pi 3b+
#define PERI_BASE 0x3F000000
#define GPIO_BASE (PERI_BASE + 0x200000)
#define BLOCK_SIZE 		(4*1024)

typedef struct bcm2837_peripheral
{
    size_t addr_p;
    int mem_fd;
    void* pMap;
    off_t pAddr;
} BCM2837_PERIPHERAL;

class RpiGPIOMapping
{
public:
    RpiGPIOMapping();
    virtual ~RpiGPIOMapping();

    inline BCM2837_PERIPHERAL GetPeriphal()
    {
        return m_periphal;
    };

private:
    RpiGPIOMapping*         m_pInstance;
    BCM2837_PERIPHERAL m_periphal;
};
