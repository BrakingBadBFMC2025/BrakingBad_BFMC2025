#include "drivers/as5600.hpp"
#include "rtos/ThisThread.h"
#include <cstdint>

// TODO: Add your code here
namespace drivers
{

   
   /**
    * @brief Class constructor as5600
    *
    */
    CAs5600::CAs5600(PinName sda, PinName scl)

    {
        
        m_i2c = new I2C(sda, scl);
        m_i2c->frequency(400000);
        printf("I2C Pins: SDA=%d, SCL=%d\n", sda, scl);
        ThisThread::sleep_for(chrono::milliseconds(300));
    
        
        /* constructor behaviour */
    }

    uint16_t CAs5600::readRawAngle() {
        uint8_t reg = AS5600_RAW_ANGLE_H;
        uint8_t data[2];
        //printf("AS5600 RAW ANGLE: %d\n", reg);
        // Read high and low bytes
        m_i2c->write(AS5600_I2C_ADDR << 1, (char*)&reg, 1, true); // Repeated start
        m_i2c->read(AS5600_I2C_ADDR << 1, (char*)data, 2);
        
        return (data[0] << 8) | data[1];
    }
    
    float CAs5600::readAngle() {
        uint16_t raw = readRawAngle();
        //printf("AS5600 RAW ANGLE: %d\n", raw);
        return (raw / 4096.0f) * 2 * M_PI; //return in radians
    }
    
    uint8_t CAs5600::readRegister(uint8_t reg) {
        uint8_t data;
        m_i2c->write(AS5600_I2C_ADDR << 1, (char*)&reg, 1, true);
        m_i2c->read(AS5600_I2C_ADDR << 1, (char*)&data, 1);
        return data;
    }


    int32_t CAs5600::begin(){
        //check if device responds
        char cmd[1] = {0x0};
        return m_i2c->write(AS5600_I2C_ADDR<<1, cmd, 1);
    }
    

    /** @brief  CAs5600 class destructor
     */
    CAs5600::~CAs5600()
    {
        if (m_i2c) {
            delete m_i2c;
            m_i2c = nullptr;
        }
    }

}; // namespace drivers