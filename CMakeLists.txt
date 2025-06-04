cmake_minimum_required(VERSION 3.10)
project(MapiCLI)
set(CMAKE_CXX_STANDARD 17)

add_executable(MapiCLI src/main.cpp)

find_package(CURL REQUIRED)
target_include_directories(MapiCLI PRIVATE ${CURL_INCLUDE_DIRS})
target_link_libraries(MapiCLI PRIVATE ${CURL_LIBRARIES})
