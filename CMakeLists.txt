CMAKE_MINIMUM_REQUIRED(VERSION 3.16)

SET(MODNAME "carma_py_example")

PROJECT(${MODNAME})

set(BUILD_SHARED_LIBS OFF CACHE BOOL "build shared library" FORCE)

FIND_PACKAGE(Python3 COMPONENTS Interpreter Development.Module NumPy)
ADD_SUBDIRECTORY(external/pybind11)
ADD_SUBDIRECTORY(external/armadillo-code)

if($ENV{CIBUILDWHEEL})
    target_compile_definitions(armadillo PRIVATE -DARMA_USE_LAPACK)
    target_compile_definitions(armadillo PRIVATE -DARMA_USE_BLAS)
endif()

FIND_PACKAGE(carma CONFIG REQUIRED)

# ##############################################################################
#                                  EXECUTABLE                                  #
# ##############################################################################
pybind11_add_module(${MODNAME}
    MODULE
        src/ols.cpp
        src/arraystore.cpp
        src/example_bindings.cpp
        src/manual_conversion.cpp
        src/automatic_conversion.cpp
)
TARGET_LINK_LIBRARIES(${MODNAME} PUBLIC carma::carma)

TARGET_INCLUDE_DIRECTORIES(${MODNAME}
    PUBLIC
        $<INSTALL_INTERFACE:include>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
)

TARGET_COMPILE_OPTIONS(${MODNAME}
    PUBLIC
        "$<$<CONFIG:RELEASE>:${PROJECT_RELEASE_FLAGS}>"
)

TARGET_COMPILE_DEFINITIONS(${MODNAME}
    PUBLIC
        "$<$<CONFIG:RELEASE>:${PROJECT_RELEASE_DEFINITIONS}>"
)

# ##############################################################################
#                                   INSTALL                                    #
# ##############################################################################
INSTALL(TARGETS ${MODNAME} DESTINATION .)
#FILE(GLOB PY_EXAMPLE_FILES "${PROJECT_SOURCE_DIR}/examples/*.py")
#INSTALL(FILES ${PY_EXAMPLE_FILES} DESTINATION examples)

# ##############################################################################
#                                  EXAMPLES                                    #
# ##############################################################################
#ADD_TEST(NAME example
#        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
#        COMMAND ${PYTHON_EXECUTABLE} carma_examples.py)
#SET_PROPERTY(TEST example
#        PROPERTY ENVIRONMENT "PYTHONPATH=${CMAKE_CURRENT_BINARY_DIR}")
