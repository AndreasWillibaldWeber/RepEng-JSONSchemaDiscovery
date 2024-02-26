#!/bin/bash

# folder paths and file names
experiemnt_folder=/experiment
system_information_folder=/system_information
report_folder=/report
smoke_file=smoke.sh
restore_file=restore.sh
collect_system_information_file=collect_system_information.sh

# --------------------------------------------------------------------------------------------------------------------------------------
# process options from the commandline arguments
# --------------------------------------------------------------------------------------------------------------------------------------
# - -r and --omit-restore: Omit to restore the MongoDB database
# - -s and --smoke: Execution of smoke test
# - -h and --help: Shows Information about available flags
# --------------------------------------------------------------------------------------------------------------------------------------
omit_restore=false
smoke_test=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        -r|--omit-restore)
            echo "Info: Omit to restore the MongoDB database."
            omit_restore=true
            ;;
        -s|--smoke)
            echo "Info: Execute smoke test."
            smoke_test=true
            ;;
        -h|--help)
            echo "Help:"
            echo " Option -r or --omit-restore omits restoring the MongoDB database."
            echo " Option -s or --omit-smoke omits executing smoke test."
            echo " Option -h or --help shows information about available flags."
            exit;;
    esac
    shift
done

# --------------------------------------------------------------------------------------------------------------------------------------
# omit to execute smoke test
# --------------------------------------------------------------------------------------------------------------------------------------
# - -s or --smoke flag executes smoke.sh
# --------------------------------------------------------------------------------------------------------------------------------------
if [ $smoke_test == true ]; then
    bash ${experiemnt_folder}/${smoke_file}
fi

# --------------------------------------------------------------------------------------------------------------------------------------
# read out the cpu and memory for the report
# --------------------------------------------------------------------------------------------------------------------------------------
# - read collect_system_information.sh and readme.md for more information
# --------------------------------------------------------------------------------------------------------------------------------------
bash ${system_information_folder}/${collect_system_information_file} ${report_folder}

# --------------------------------------------------------------------------------------------------------------------------------------
# omit to restore MongoDB database
# --------------------------------------------------------------------------------------------------------------------------------------
# - to restore the MongoDB database is only necessary the first time, after that it can be omitted
# - if the data within MongoDB or the database has been deleted from the hard drive, the restore command must be executed again
# - -r or --omit-restore flag avoids the execution of restore.sh
# --------------------------------------------------------------------------------------------------------------------------------------
if [ $omit_restore != true ]; then
    bash ${experiemnt_folder}/${restore_file}
fi