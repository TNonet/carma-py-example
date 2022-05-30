CMAKE_MINIMUM_REQUIRED(VERSION 3.16)

SET(MODNAME "carma_py_example")

PROJECT(${MODNAME})

set(BUILD_SHARED_LIBS OFF CACHE BOOL "build shared library" FORCE)

SET(ARMADILLO_SUBDIR external/armadillo-code)
ADD_SUBDIRECTORY(external/pybind11)
ADD_SUBDIRECTORY(${ARMADILLO_SUBDIR})
ADD_SUBDIRECTORY(external/carma)

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

# Add -fPIC for Armadillo (and OpenBLAS if compiled)
if(NOT MSVC)
    # clang on Windows does not support -fPIC
    if(NOT WIN32)
        target_compile_options(armadillo PRIVATE -fPIC)
    endif()
endif()

if(MSVC)
    target_include_directories(${PROJECT_NAME} PUBLIC
            "${CMAKE_CURRENT_SOURCE_DIR}/../include"
            )
    target_compile_definitions(${PROJECT_NAME} PRIVATE
            "ARMA_USE_LAPACK;"
            "ARMA_USE_BLAS"
            )

    target_compile_options(${PROJECT_NAME} PRIVATE
            ${DEFAULT_CXX_DEBUG_INFORMATION_FORMAT};
            ${DEFAULT_CXX_EXCEPTION_HANDLING}
            )
    target_link_options(${PROJECT_NAME} PRIVATE
            $<$<CONFIG:Debug>:
            /DEBUG
            >
            )

    add_custom_command(
            TARGET ${PROJECT_NAME}
            POST_BUILD
            COMMANDS
            COMMAND $<CONFIG:Debug> copy ${CMAKE_CURRENT_SOURCE_DIR}/${ARMADILLO_SUBDIR}/examples/lib_win64/*.dll $<SHELL_PATH:${OUTPUT_DIRECTORY}>
            COMMAND $<CONFIG:Release> copy ${CMAKE_CURRENT_SOURCE_DIR}/${ARMADILLO_SUBDIR}/examples/lib_win64/*.dll $<SHELL_PATH:${OUTPUT_DIRECTORY}>
            COMMENT "Copy .DLL to output directory"
    )

    set(ADDITIONAL_LIBRARY_DEPENDENCIES
            "libopenblas"
            )
    target_link_libraries(${PROJECT_NAME} PUBLIC "${ADDITIONAL_LIBRARY_DEPENDENCIES}")

    target_link_directories(${PROJECT_NAME} PUBLIC
            "${CMAKE_CURRENT_SOURCE_DIR}/${ARMADILLO_SUBDIR}/examples/lib_win64"
            )
endif()


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
