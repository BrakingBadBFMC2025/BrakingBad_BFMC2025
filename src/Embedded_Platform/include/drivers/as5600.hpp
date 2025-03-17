#ifndef AS5600_HPP
#define AS5600_HPP

#include "mbed.h"
#include <cstdint>

#define AS5600_I2C_ADDR    0x36
#define AS5600_RAW_ANGLE_H 0x0C

// TODO: Add your code here

namespace drivers
{
   /**
    * @brief Class as5600
    *
    */
    class CAs5600
    {
        public:

            // Add static I2C instance like BNO055
            static I2C* i2c_instance;
            /* Constructor */
            CAs5600(PinName sda, PinName scl);

            
            /* Destructor */
            ~CAs5600();

            /**
            * @brief Read raw angle value from sensor
            * @return uint16_t 12-bit raw angle (0-4095)
            */
            uint16_t readRawAngle();

            /**
            * @brief Read angle in radians
            * @return float Angle in radians (0-2π)
            */
            float readAngle();
            int32_t begin(); 

        private:
            /* private variables & method member */

            I2C* m_i2c;


            /**
             * @brief Read register from AS5600
             * @param reg Register address
             * @return uint8_t Register value
             */
            uint8_t readRegister(uint8_t reg);


    }; // class CAs5600
}; // namespace drivers

#endif // AS5600_HPP
