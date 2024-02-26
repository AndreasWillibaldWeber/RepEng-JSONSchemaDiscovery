#!/bin/bash

echo "# ------------------------ START SMOKE TEST ---------------------------------"

command_list=("python3" "pip3" "mongorestore" "pdflatex" "make")

for command_name in ${command_list[@]}; do

    err_msg="Error: Command ${command_name} not found"
    ok_msg="Ok: Command ${command_name} is installed"

    ${command_name} --version > /dev/null

    if [ $? -ne 0 ]; then
        echo $err_msg
    else
        echo $ok_msg
    fi

done

python_package_list=("rich" "requests")

for package_name in ${pyhton_package_list[@]}; do

    err_msg="Error: Python3 package ${package_name} not found"
    ok_msg="Ok: Python package ${package_name} is installed"

    pip3 show ${package_name} > /dev/null

    if [ $? -ne 0 ]; then
        echo $err_msg
    else
        echo $ok_msg
    fi

done

apt_package_list=("wget" "git" "jq" "python3" "python3-pip" "make" "texlive-base" "texlive-bibtex-extra" "texlive-fonts-recommended" "texlive-fonts-extra" "texlive-latex-extra" "texlive-publishers")

for package_name in ${apt_package_list[@]}; do

    err_msg="Error: Apt package ${package_name} not found"
    ok_msg="Ok: Apt package ${package_name} is installed"

    found_packages=$( apt list --installed 2> /dev/null | grep -w "$package_name" | wc -l )

    if [ $found_packages -eq 0 ]; then
        echo $err_msg
    else
        echo $ok_msg
    fi

done

web_api_url="http://webapi:4200"
web_api_status_response="$(wget --spider --server-response ${web_api_url} 2>&1 | awk '/^  HTTP/{print $2}')"
if [ $web_api_status_response -ne 200 ]; then 
    echo "Error: WebAPI is not reachable"
else
    echo "OK: WebAPI is reachable"
fi

mongo_host="mongo"
mongo_port="27017"
mongo_response=$( mongorestore --host=${mongo_host} --port=${mongo_port} 2>&1 | grep "error connecting to host:" | wc -l )
if [ $mongo_response -ne 0 ]; then 
    echo "Error: MongoDB is not reachable"
else
    echo "OK: MongoDB is reachable"
fi

echo "# ------------------------- END SMOKE TEST ----------------------------------"