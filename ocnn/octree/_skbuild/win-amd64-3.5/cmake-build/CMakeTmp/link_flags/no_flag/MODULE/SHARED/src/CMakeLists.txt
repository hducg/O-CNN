
      cmake_minimum_required(VERSION 3.9.3)
      project(link_flags C)

      include_directories(F:/wjcao/github/hducg/O-CNN/ocnn/octree/_skbuild/win-amd64-3.5/cmake-build/CMakeTmp/link_flags/no_flag/MODULE/SHARED/src)

      add_library(number SHARED number.c)
      add_library(counter MODULE counter.c)
    
        set_target_properties(counter PROPERTIES PREFIX "")
      
      add_executable(main main.c)
    
        target_link_libraries(main number)
      
        target_link_libraries(main "")
      