cmake_minimum_required(VERSION 3.8)
project(sas_ur_control_template)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(sas_robot_driver_ur REQUIRED)

# According to https://github.com/SmartArmStack/sas_robot_driver/blob/ros2/CMakeLists.txt
##### LAUNCH FILES #####

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/
)

##END## LAUNCH FILES #####

# According to https://github.com/SmartArmStack/sas_datalogger/blob/78ac681f9cb049c5b9715d215f163565f16b5cdc/CMakeLists.txt
##### PYTHON EXECUTABLES #####
install(PROGRAMS
  scripts/joint_interface_example.py
  DESTINATION lib/${PROJECT_NAME}
)
##END## PYTHON EXECUTABLES #####

if(BUILD_TESTING)
    find_package(ament_lint_auto REQUIRED)
    # the following line skips the linter which checks for copyrights
    # comment the line when a copyright and license is added to all source files
    set(ament_cmake_copyright_FOUND TRUE)
    # the following line skips cpplint (only works in a git repo)
    # comment the line when this package is in a git repo and when
    # a copyright and license is added to all source files
    set(ament_cmake_cpplint_FOUND TRUE)
    ament_lint_auto_find_test_dependencies()
endif()

ament_package()    
