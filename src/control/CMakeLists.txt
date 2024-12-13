cmake_minimum_required(VERSION 3.0.2)
project(control)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  geometry_msgs
  utils
  message_generation
)

add_message_files(
  FILES
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
)

set(SOURCES
    src/movement_executor_node.cpp
    src/controllers/Velocity_controller.cpp
    src/controllers/Steering_controller.cpp
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)


add_executable(movement_executor ${SOURCES})
target_link_libraries(movement_executor ${catkin_LIBRARIES} yaml-cpp)

add_executable(overseer src/overseer_node.cpp)
target_link_libraries(overseer ${catkin_LIBRARIES} yaml-cpp)
