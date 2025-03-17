#include "periodics/encoders.hpp"
#include "mbed.h"

#define ENCODER_BUFFER_SIZE 500
// TODO: Add your code here
namespace periodics
{
   /**
    * @brief Class constructor encoders
    *
    */
    CEncoders::CEncoders(
        std::chrono::milliseconds f_period,
        UnbufferedSerial& f_serial,
        drivers::CAs5600& leftEncoder,
        bool& encoderActiveRef
    ): 
    utils::CTask(f_period),
    m_serial(f_serial),
    m_leftEncoder(leftEncoder),
    m_isActive(false),
    m_lastUpdate(0),
    bool_globalsV_encoder_isActive(encoderActiveRef)  // Initialize reference
    {
        // Add initialization like CImu
        if(m_delta_time < 150) {  // Match IMU's 150ms minimum
            setNewPeriod(150);
            m_delta_time = 150;
        }
        /* constructor behaviour */
    }

    void CEncoders::serialCallbackEncoderCommand(char const * a, char * b)
    {
        //printf("ENCODER CMD RECEIVED: a:%s and b: %s\n", a, b);  // Raw input debug
        
        uint8_t l_isActivate = 0;
        uint8_t l_res = sscanf(a,"%hhu",&l_isActivate);


        //printf("PARSED: l_res=%d, l_isActive=%d\n", l_res, l_isActivate);


        l_isActivate = atoi(a);
        //m_isActive = (l_isActivate>=1);

        l_res = 1;


        //printf("PARSED: l_res=%d, l_isActivate=%d\n", l_res, l_isActivate);

        if (l_res == 1)  {
            if(uint8_globalsV_value_of_kl == 15 || uint8_globalsV_value_of_kl == 30) {
                printf("GEIAAAAAA\n");
                m_isActive = (l_isActivate>=1);
                bool_globalsV_encoder_isActive = (l_isActivate>=1);
                sprintf(b, "1");

                /////////// Debug print
                //printf("ENCODER SERIAL COMMAND RECEIVED: %d ??? %d\n", l_isActivate, m_isActive);
                //sprintf(b, "@encoder:%hhu;;\r\n", l_isActivate);

            } else {
                m_isActive = (l_isActivate>=1);
                sprintf(b, "@error:kl15_required;;\r\n");
            }
        } else {
            sprintf(b, "@error:invalid_format;;\r\n");
        }
    }

    /** @brief  CEncoders class destructor
     */
    CEncoders::~CEncoders()
    {
    }

    /* Run method */
    void CEncoders::_run()
    {
        /* Run method behaviour */
        if(!m_isActive) return;
        // Respect the 150ms update rate like IMU
        if(HAL_GetTick() - m_lastUpdate < 150) return;
        
        char buffer[ENCODER_BUFFER_SIZE];
        float angle = 0;
        angle = m_leftEncoder.readAngle();
        printf("ENCODER TASK RUNNING\n");

        //printf("ENCODER TASK RUNNING - ANGLE IN RADIANS: %f\n", angle);
        fflush(stdout);
        
        snprintf(buffer, sizeof(buffer), "@encoder:%d.%03d;;\r\n",(int)angle, (int)((angle - (int)angle)*1000));
        m_serial.write(buffer, strlen(buffer));
        
        m_lastUpdate = HAL_GetTick();
    }

}; // namespace periodics