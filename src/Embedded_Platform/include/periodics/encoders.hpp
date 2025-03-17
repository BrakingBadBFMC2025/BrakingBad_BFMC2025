#ifndef ENCODERS_HPP
#define ENCODERS_HPP

// TODO: Add your code here

#include <chrono>
#include <utils/task.hpp>
#include "drivers/as5600.hpp"
#include <brain/globalsv.hpp>

namespace periodics
{
   /**
    * @brief Class encoders
    *
    */
    class CEncoders: public utils::CTask
    {
        public:
            /* Constructor */
            CEncoders(
                std::chrono::milliseconds f_period,
                UnbufferedSerial& f_serial,
                drivers::CAs5600& leftEncoder,
                bool& encoderActiveRef
            );

            void serialCallbackEncoderCommand(char const * a, char * b);

            /* Destructor */
            ~CEncoders();
        private:
            /* private variables & method member */


            /* Run method */
            virtual void  _run() override; 

            void _updateEncoderData();
            UnbufferedSerial& m_serial;
            drivers::CAs5600& m_leftEncoder;
            int m_delta_time;
            bool& bool_globalsV_encoder_isActive;  // Add global state reference

            uint32_t m_lastUpdate;

            /** @brief Active flag  */
            bool m_isActive;

    }; // class CEncoders
}; // namespace periodics

#endif // ENCODERS_HPP
