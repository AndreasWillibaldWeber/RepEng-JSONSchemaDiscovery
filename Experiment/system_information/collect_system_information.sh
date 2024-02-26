#!/bin/bash

# folder paths and file names
sys_info_folder=/system_information
cpu_info_file=cpu_information.txt
cpu_filter_file=cpu_filter.txt
cpu_output_file=cpu_listing.txt
mem_info_file=mem_information.txt
mem_filter_file=mem_filter.txt
mem_output_file=mem_listing.txt

# ----------------------------------------------------------------------------
# read out the cpu information and prepare it for the report
# ----------------------------------------------------------------------------
# - cpu_information.txt contains all information
# - cpu_listing.txt contains filtered information for report
# - cpu_filter.txt contains strings used to filter out unwanted information
# ----------------------------------------------------------------------------
lscpu > ${sys_info_folder}/${cpu_info_file}
cat ${sys_info_folder}/${cpu_info_file} | grep -v -F -f ${sys_info_folder}/${cpu_filter_file} > ${sys_info_folder}/${cpu_output_file}

# ----------------------------------------------------------------------------
# read out the mem information and prepare it for the report
# ----------------------------------------------------------------------------
# - mem_information.txt contains all information
# - mem_listing.txt contains filtered information for report
# - mem_filter.txt contains strings used to retain wanted information
# ----------------------------------------------------------------------------
cat /proc/meminfo > ${sys_info_folder}/${mem_info_file}
cat ${sys_info_folder}/${mem_info_file} | grep -F -f ${sys_info_folder}/${mem_filter_file} > ${sys_info_folder}/${mem_output_file}