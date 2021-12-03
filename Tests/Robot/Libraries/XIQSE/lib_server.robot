#----------------------------------------------------------------------
# Copyright (C) 2021... 2021 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to basic XIQSE server functionality.
#

*** Settings ***
Library         common/Cli.py


*** Variables ***
${SSH_PORT}     22


*** Keywords ***
Stop XIQSE Server
    [Documentation]     Issues the command to shut down the XIQSE server
    [Arguments]         ${ip}  ${user}  ${pwd}

    ${ssh_spawn} =   Open PXSSH Spawn  ${ip}  ${user}  ${pwd}  ${SSH_PORT}  disable_strict_host_key_checking=True
    ${cmd_result} =  Send PXSSH        ${ssh_spawn}  systemctl stop nsserver
    Log To Console      PXSSH Command Result Is ${cmd_result}

    [Teardown]  Close Paramiko Spawn  ${ssh_spawn}

Start XIQSE Server
    [Documentation]     Issues the command to start the XIQSE server
    [Arguments]         ${ip}  ${user}  ${pwd}

    ${ssh_spawn} =   Open PXSSH Spawn  ${ip}  ${user}  ${pwd}  ${SSH_PORT}  disable_strict_host_key_checking=True
    ${cmd_result} =  Send PXSSH        ${ssh_spawn}  systemctl start nsserver
    Log To Console      PXSSH Command Result Is ${cmd_result}

    [Teardown]  Close Paramiko Spawn  ${ssh_spawn}

Check Server Log For Exceptions
    [Documentation]     Checks the server log for any exceptions
    [Arguments]         ${ip}  ${user}  ${pwd}
    
    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${pwd}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  cat /usr/local/Extreme_Networks/NetSight/appdata/logs/server.* | grep ERROR | wc -l
     
    Should Be Equal As Strings  0   ${output}

Remove Legacy License File and Restart XIQSE Server
    [Documentation]     Removes Legacy License File in XIQSE and Restarts
    [Arguments]         ${ip}  ${user}  ${password}  ${license_file}

    ${sshSession}=  Open Paramiko SSH Spawn     ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${lic_output}=  Send Paramiko CMD           ${sshSession}  rm /usr/local/Extreme_Networks/NetSight/appdata/license/${license_file}
    ${restart_output}=  Send Paramiko CMD       ${sshSession}  systemctl restart nsserver

    [Teardown]  Close Paramiko Spawn  ${sshSession}
