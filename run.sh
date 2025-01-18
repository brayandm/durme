python3 main.py ./src/code.dm ./src/build/code.cpp --debug="./src/debug" > /dev/null

g++ -o ./src/build/code ./src/build/code.cpp

./src/build/code