# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

# If CMAKE_DISABLE_SOURCE_CHANGES is set to true and the source directory is an
# existing directory in our source tree, calling file(MAKE_DIRECTORY) on it
# would cause a fatal error, even though it would be a no-op.
if(NOT EXISTS "/home/m1tsos/BB/BrakingBad_BFMC2025/src/Embedded_Platform/cmake_build/NUCLEO_F401RE/develop/GCC_ARM/_deps/greentea-client-src")
  file(MAKE_DIRECTORY "/home/m1tsos/BB/BrakingBad_BFMC2025/src/Embedded_Platform/cmake_build/NUCLEO_F401RE/develop/GCC_ARM/_deps/greentea-client-src")
endif()
file(MAKE_DIRECTORY
  "/home/m1tsos/BB/BrakingBad_BFMC2025/src/Embedded_Platform/cmake_build/NUCLEO_F401RE/develop/GCC_ARM/_deps/greentea-client-build"
  "/home/m1tsos/BB/BrakingBad_BFMC2025/src/Embedded_Platform/cmake_build/NUCLEO_F401RE/develop/GCC_ARM/_deps/greentea-client-subbuild/greentea-client-populate-prefix"
  "/home/m1tsos/BB/BrakingBad_BFMC2025/src/Embedded_Platform/cmake_build/NUCLEO_F401RE/develop/GCC_ARM/_deps/greentea-client-subbuild/greentea-client-populate-prefix/tmp"
  "/home/m1tsos/BB/BrakingBad_BFMC2025/src/Embedded_Platform/cmake_build/NUCLEO_F401RE/develop/GCC_ARM/_deps/greentea-client-subbuild/greentea-client-populate-prefix/src/greentea-client-populate-stamp"
  "/home/m1tsos/BB/BrakingBad_BFMC2025/src/Embedded_Platform/cmake_build/NUCLEO_F401RE/develop/GCC_ARM/_deps/greentea-client-subbuild/greentea-client-populate-prefix/src"
  "/home/m1tsos/BB/BrakingBad_BFMC2025/src/Embedded_Platform/cmake_build/NUCLEO_F401RE/develop/GCC_ARM/_deps/greentea-client-subbuild/greentea-client-populate-prefix/src/greentea-client-populate-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/home/m1tsos/BB/BrakingBad_BFMC2025/src/Embedded_Platform/cmake_build/NUCLEO_F401RE/develop/GCC_ARM/_deps/greentea-client-subbuild/greentea-client-populate-prefix/src/greentea-client-populate-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/home/m1tsos/BB/BrakingBad_BFMC2025/src/Embedded_Platform/cmake_build/NUCLEO_F401RE/develop/GCC_ARM/_deps/greentea-client-subbuild/greentea-client-populate-prefix/src/greentea-client-populate-stamp${cfgdir}") # cfgdir has leading slash
endif()
