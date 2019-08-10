#include <stdlib.h>

/**
 * Defines for raspberry pi 3b+ GPIO address
 */
#define PERI_BASE                   0x3F000000
#define GPIO_BASE                   (PERI_BASE + 0x200000)
#define BLOCK_SIZE 		            (4*1024)

/**
 * Defines for GPIO Function select register values
 * This 32 bit register uses bit 0 to bit 29 to determine the function of 
 * 10 GPIO pins, each GPIO pin has 3 bits for function setting
 */
#define GPIOFSEL_INPUT              0b000
#define GPIOFSEL_OUTPUT             0b001


using gpioreg_t = uint32_t;         // each gpio address is 32 bit wide

enum gpio_status
{
    LOW = 0,
    HIGH
};
using gpio_t = gpio_status;

class RpiGPIOMapping
{
public:
    virtual ~RpiGPIOMapping();

    static RpiGPIOMapping* GetInstance();

    inline volatile gpioreg_t* GetMapping()
    {
        return m_pGPIOBase;
    }

    inline uint32_t GPIOPinToFunctionSelectorIndex(uint32_t GPIOPin)
    {
        return GPIOPin / 10;
    };

    inline uint32_t GPIOPinBitLocation(uint32_t GPIOPin)
    {
        return (GPIOPin % 10) * 3;
    };

    inline volatile gpioreg_t* GetGPIOFunctionSelector(uint32_t functionSelectorIndex)
    {
        return m_pGPIOBase + functionSelectorIndex;
    };

    void SetInput(uint32_t GPIOPin);
    void SetOutput(uint32_t GPIOPin);

    gpio_t ReadGPIO(uint32_t GPIOPin);

private:
    static RpiGPIOMapping*          m_pInstance;
    volatile gpioreg_t*             m_pGPIOBase;    /** GPIO Base in user space */
    int                             m_memFd;

    // private singleton constructor
    RpiGPIOMapping();
};
