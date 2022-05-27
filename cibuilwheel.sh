python -m pip install cibuildwheel==2.5.0

export CIBW_SKIP="pp* *-win32"
export CIBW_BEFORE_ALL_LINUX="yum install -y lapack-devel && bash scripts/install_linux_libs.sh"
export CIBW_BEFORE_BUILD_WINDOWS="pip install scipy && bash scripts/install_linux_libs.sh"
export CIBW_BEFORE_TEST="pip install pytest numpy"
export CIBW_TEST_COMMAND="pytest {package}/tests"
export CIBW_BUILD_VERBOSITY=3
python -m cibuildwheel --output-dir wheelhouse --platform windows --archs AMD64
