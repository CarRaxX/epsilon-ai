set-executionpolicy RemoteSigned -Scope CurrentUser
python -m venv venv
venv\Scripts\Activate.ps1
pip install scikit-build
python -m pip install -U pip wheel setuptools

git clone https://github.com/abetlen/llama-cpp-python.git
cd llama-cpp-python
cd vendor
git clone https://github.com/ggerganov/llama.cpp.git 
cd llama.cpp
# remove the line git checkout if you want the latest and new quant(=not working with old ggmls).
# git checkout b608b55a3ea8e4760c617418538465449175bdb8
cd ..\..

$Env:LLAMA_CUBLAS = "1"
$Env:FORCE_CMAKE = "1"
$Env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"
python setup.py bdist_wheel
 
Write-Host "Done! The llama_cpp folder with the cublas llama.dll is under ..\llama-cpp-python\_skbuild\win-amd64-3.10\cmake-install"
Write-Host "You can use this folder to replace your old folder. The wheel is under \llama-cpp-python\dist"

pause

# you need installed and working (PATH is the main problem):
# git, python (3.10.11) cuda toolkit (11.8)
# visual studio 2022 community AND Build Tools 2019.
# cmake (click on path during installation and restart computer)