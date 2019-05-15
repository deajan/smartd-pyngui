#!/usr/bin/env bash

BASE_DIR="$(pwd)"

echo using basedir [$BASE_DIR]

# Arguments: 1= Pid to wait for, 2= timeout (s)
function WaitForIt {
	local start=$SECONDS
	local pid=${1}
	local timeout=${2}

	local result

	while ps -p $pid > /dev/null 2>&1
	do
		sleep 1
		if [ $((SECONDS - start)) -ge $timeout ]; then
			kill -9 $pid
		fi
	done
	wait $pid
	result=$?
	return $result
}

cd "$BASE_DIR" || (echo "Cannot switch to directory [$BASE_DIR]." && exit 1)
echo "Basedir [$BASE_DIR] content:"
ls "$BASE_DIR"
echo "Basedir [$BASE_DIR/smartd_pyngui] content:"
ls "$BASE_DIR/smartd_pyngui"
# Make sure we don't run on any forms of cache
find "$BASE_DIR" -name "*.pyc" -or -name "__pycache__" | xargs -I {} rm -rf {}

# First let's check if program can run
python "$BASE_DIR/smartd_pyngui/smartd_pyngui.py" &
WaitForIt $! 20
result=$?

if [ $result -eq 137 ]; then
    echo "App launched from shell with success. Exit code [$result] is kill signal."
else
    echo "App failed to launch from shell. Exit code [$result]."
    exit $result
fi

# Run unit tests
py.test

# Try nuitka compilation
echo "Nuitka info"
python -m nuitka --version
echo "Nuitka compilation"
python -m nuitka --standalone "$BASE_DIR/smartd_pyngui/smartd_pyngui.py"
result=$?

if [ $result -ne 0 ]; then
    echo "Nuitka compilation failed. Exit code [$result]."
    exit $result
else
    echo "Nuitka compilation success. Trying to run built software."
    ls "$BASE_DIR"

    "$BASE_DIR/smartd_pyngui.dist/smartd_pyngui" &
    WaitForIt $! 20
    result=$?
    if [ $result -eq 127 ]; then
        echo "Nuitka compiled app is not found. Exit code [$result]."
    else
        echo "Nuitka compiled app exited with code [$result]."
    fi
fi