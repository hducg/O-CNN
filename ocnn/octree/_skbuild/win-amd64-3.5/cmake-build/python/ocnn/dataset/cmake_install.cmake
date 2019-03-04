# Install script for directory: F:/wjcao/github/hducg/O-CNN/ocnn/octree/python/ocnn/dataset

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "F:/wjcao/github/hducg/O-CNN/ocnn/octree/_skbuild/win-amd64-3.5/cmake-install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/python/ocnn/dataset" TYPE MODULE FILES "F:/wjcao/github/hducg/O-CNN/ocnn/octree/_skbuild/win-amd64-3.5/cmake-build/python/ocnn/dataset/Debug/_writable_data.pyd")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/python/ocnn/dataset" TYPE MODULE FILES "F:/wjcao/github/hducg/O-CNN/ocnn/octree/_skbuild/win-amd64-3.5/cmake-build/python/ocnn/dataset/Release/_writable_data.pyd")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/python/ocnn/dataset" TYPE MODULE FILES "F:/wjcao/github/hducg/O-CNN/ocnn/octree/_skbuild/win-amd64-3.5/cmake-build/python/ocnn/dataset/MinSizeRel/_writable_data.pyd")
  elseif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/python/ocnn/dataset" TYPE MODULE FILES "F:/wjcao/github/hducg/O-CNN/ocnn/octree/_skbuild/win-amd64-3.5/cmake-build/python/ocnn/dataset/RelWithDebInfo/_writable_data.pyd")
  endif()
endif()

