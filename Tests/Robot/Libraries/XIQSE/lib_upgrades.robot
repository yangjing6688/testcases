#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to upgrading engines.
#

*** Settings ***
Library     Collections
Library     common/Cli.py
Library     OperatingSystem


*** Keywords ***
Upgrade Site Engine
    [Documentation]     deletes existing file and downloads the upgrade binary to site engine

    Delete SE Existing Files  ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}
    Download File   ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${XIQSE_FOLDER}  ${NSRELEASE_XIQSE_FILE}
    Install SE Software  ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${NSRELEASE_XIQSE_FILE}
    Check Server Exit Code  ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${NSRELEASE_XIQSE_FILE}
    Check Server Is Up
    Run Keyword If
    ...   "${INSTALL_MODE}" == "AIO"
    ...    Inject XIQ AIO property into NSJBoss Properties File and Restart  ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}
    ...    ELSE IF
    ...    "${INSTALL_MODE}" == "CONNECTED"
    ...    Inject XIQ Cloud properties into NSJBoss Properties File and Restart  ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}
    ...    ELSE IF
    ...   "${INSTALL_MODE}" == "AIRGAP"
    ...    Log To Console    >> THIS IS FUTURE TEST SECTION WHEN AIRGAP IS SUPPORTED
    ...    ELSE
    ...    Log To Console    >> Invalid value for INSTALL_MODE: ‘${INSTALL_MODE}’. Please specify AIO, CONNECTED, or AIRGAP
    Check Server Is Up

Upgrade NAC Engine
    [Documentation]     deletes existing file and downloads the upgrade binary to the access control appliance

    Delete Existing Appliance Files  ${NAC_IP}  ${APPLIANCE_USERNAME}  ${APPLIANCE_PASSWORD}  ${LOG_DIRECTORY}  ${NAC_BINARY_PREFIX}  ${NAC_LOG_PREFIX}
    Download File  ${NAC_IP}  ${APPLIANCE_USERNAME}  ${APPLIANCE_PASSWORD}  ${NAC_FOLDER}  ${NSRELEASE_NAC_FILE}
    Install NAC Software  ${NAC_IP}  ${APPLIANCE_USERNAME}  ${APPLIANCE_PASSWORD}  ${NSRELEASE_NAC_FILE}
    Check NAC Exit Code  ${NAC_IP}  ${APPLIANCE_USERNAME}  ${APPLIANCE_PASSWORD}

Upgrade Purview Engine
    [Documentation]     deletes existing file and downloads the upgrade binary to the purview appliance

    Delete Existing Appliance Files  ${PURVIEW_IP}  ${APPLIANCE_USERNAME}  ${APPLIANCE_PASSWORD}  ${LOG_DIRECTORY}  ${PURVIEW_BINARY_PREFIX}  ${PURVIEW_LOG_PREFIX}
    Download File  ${PURVIEW_IP}  ${APPLIANCE_USERNAME}  ${APPLIANCE_PASSWORD}  ${PURVIEW_FOLDER}  ${NSRELEASE_PURVIEW_FILE}
    Install Purview Software  ${PURVIEW_IP}  ${APPLIANCE_USERNAME}  ${APPLIANCE_PASSWORD}  ${NSRELEASE_PURVIEW_FILE}
    Check Purview Exit Code  ${PURVIEW_IP}  ${APPLIANCE_USERNAME}  ${APPLIANCE_PASSWORD}

Upgrade NGAnalytics Engine
    [Documentation]     deletes existing file and downloads the upgrade binary to the purview appliance

    Delete Existing Appliance Files  ${NEXTGEN_IP}  ${APPLIANCE_USERNAME}  ${APPLIANCE_PASSWORD}  ${LOG_DIRECTORY}  ${NGANALYTICS_BINARY_PREFIX}  ${NGANALYTICS_LOG_PREFIX}
    Download File  ${NEXTGEN_IP}  ${APPLIANCE_USERNAME}  ${APPLIANCE_PASSWORD}  ${NGANALYTICS_FOLDER}  ${NSRELEASE_NGANALYTICS_FILE}
    Install NGAnalytics Software  ${NEXTGEN_IP}  ${APPLIANCE_USERNAME}  ${APPLIANCE_PASSWORD}  ${NSRELEASE_NGANALYTICS_FILE}
    Check NGAnalytics Exit Code  ${NEXTGEN_IP}  ${APPLIANCE_USERNAME}  ${APPLIANCE_PASSWORD}

Ubuntu Clear SSH Keys
    FOR  ${APPLIANCE_IP}  IN  @{ALL_APPLIANCES}
        Run   ssh-keygen -f "~/.ssh/known_hosts" -R "${APPLIANCE_IP}"
    END

Delete SE Existing Files
    [Documentation]     Delete any existing binary and log files if they exist in the target directory
    [Arguments]         ${ip}  ${user}  ${password}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  rm ${XIQSE_FILE_PREFIX}*

Delete Existing Appliance Files
    [Documentation]     Delete any existing binary and log files if they exist in the target directory
    [Arguments]         ${ip}  ${user}  ${password}  ${log_directory}  ${binary_file_prefix}  ${log_file_prefix}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  rm ${binary_file_prefix}*
    ${output} =  Send Paramiko CMD        ${sshSession}  rm ${log_directory}${log_file_prefix}*

Download File
    [Documentation]  Downloads a file to the target ip
    [Arguments]  ${ip}  ${user}  ${password}   ${folder}   ${file}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  curl -f ${NSRELEASE_VERSION_BASE}/${folder}/${file} > ${file}  ${DOWNLOAD_TIMEOUT_SEC}
    ${output} =  Send Paramiko CMD        ${sshSession}  chmod 755 ${file}
    # Use the find command with empty flag, if it returns the file name, then it is empty
    ${output} =  Send Paramiko CMD        ${sshSession}  find . -empty -name ${file}
    Should Not Contain   ${output}  ${file}
    Log  ${output}

Install SE Software
    [Documentation]   Installs the downloaded binary on the XIQSE appliance
    [Arguments]    ${ip}  ${user}  ${password}  ${file}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  ./${NSRELEASE_XIQSE_FILE} --noprompts --skip-mem-check  timeout=${INSTALL_DOWNLOAD_TIMEOUT_SEC}

Install NAC Software
    [Documentation]   Installs the downloaded binary on the Access Control appliance
    [Arguments]    ${ip}  ${user}  ${password}  ${file}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  ./${NSRELEASE_NAC_FILE} -allowSameVersion -noprompts -keepalive  timeout=${INSTALL_DOWNLOAD_TIMEOUT_SEC}

Install Purview Software
    [Documentation]   Installs the downloaded binary on the Purview appliance
    [Arguments]    ${ip}  ${user}  ${password}  ${file}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  ./${NSRELEASE_PURVIEW_FILE} -allowSameVersion -noprompts -keepalive  timeout=${INSTALL_DOWNLOAD_TIMEOUT_SEC}

Install NGAnalytics Software
    [Documentation]   Installs the downloaded binary on the NextGen Analytics appliance
    [Arguments]    ${ip}  ${user}  ${password}  ${file}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  ./${NSRELEASE_NGANALYTICS_FILE} -allowSameVersion -noprompts -keepalive  timeout=${INSTALL_DOWNLOAD_TIMEOUT_SEC}

Inject XIQ AIO property into NSJBoss Properties File and Restart
    [Documentation]     Injects Base XIQ Url into NSJBoss.properties file and restarts XIQSE service
    [Arguments]         ${ip}  ${user}  ${password}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  echo extreme.xiq.baseUrl=${XIQ_BASE_URL} >> /usr/local/Extreme_Networks/NetSight/appdata/NSJBoss.properties
    ${output} =  Send Paramiko CMD        ${sshSession}  echo DeveloperOptions.airGapSerialNumber=${XIQSE_SERIAL} >> ~/NetSight/DeveloperOptions.properties
    ${output} =  Send Paramiko CMD        ${sshSession}  ${XIQSE_RESTART_SERVER}
    sleep   300s

Inject XIQ CLOUD properties into NSJBoss Properties File and Restart
    [Documentation]     Injects Base and Redirector XIQ Urls into NSJBoss.properties file and restarts XIQSE service
    [Arguments]         ${ip}  ${user}  ${password}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  echo extreme.xiq.baseUrl=${XIQ_BASE_URL} >> /usr/local/Extreme_Networks/NetSight/appdata/NSJBoss.properties
    ${output} =  Send Paramiko CMD        ${sshSession}  echo extreme.xiq.redirectorurl=${XIQ_REDIRECT_URL} >> /usr/local/Extreme_Networks/NetSight/appdata/NSJBoss.properties
    # DO NOT DELETE - Specifically setting the Serial Number here so the VM will retain the expected serial number
    ${output} =  Send Paramiko CMD        ${sshSession}  echo DeveloperOptions.airGapSerialNumber=${XIQSE_SERIAL} >> ~/NetSight/DeveloperOptions.properties
    ${output} =  Send Paramiko CMD        ${sshSession}  ${XIQSE_RESTART_SERVER}
    sleep   600s


#### Keywords for checking success of installations
Check Server Exit Code
    [Documentation]     Parses installer log for exit code. If 0, it was successful
    [Arguments]    ${ip}  ${user}  ${password}  ${file}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  cat ${NSRELEASE_XIQSE_LOG_FILE} | grep "exiting with code: 0"
    Should Contain  ${output}  exiting with code: 0

Check NAC Exit Code
    [Documentation]     Parses installer log for exit code. If "upgrade was completed" line is present, it was successful.
    [Arguments]    ${ip}  ${user}  ${password}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  cat ${NSRELEASE_NAC_LOG_FILE} | grep "upgrade to ${NSRELEASE_VERSION} was completed"
    Should Contain  ${output}  upgrade to ${NSRELEASE_VERSION} was completed

Check Purview Exit Code
    [Documentation]     Parses installer log for exit code. If "upgrade was completed" line is present, it was successful.
    [Arguments]    ${ip}  ${user}  ${password}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  cat ${NSRELEASE_Purview_LOG_FILE} | grep "upgrade to ${NSRELEASE_VERSION} was completed"
    Should Contain  ${output}  upgrade to ${NSRELEASE_VERSION} was completed

Check NGAnalytics Exit Code
    [Documentation]     Parses installer log for exit code. If "upgrade was completed" line is present, it was successful.
    [Arguments]    ${ip}  ${user}  ${password}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  cat ${NSRELEASE_NGANALYTICS_LOG_FILE} | grep "upgrade to ${NSRELEASE_VERSION} was completed"
    Should Contain  ${output}  upgrade to ${NSRELEASE_VERSION} was completed

Check Server Is Up
    [Documentation]    Checks the server is up and running.
    [Arguments]
    # XIQSE Load Page has a 60 second timeout, we want to wait max 5 minutes.
    # We expect failures here so ignore errors. 
    FOR    ${index}    IN RANGE    5
        ${passed}  ${value}   Run Keyword And Ignore Error  XIQSE Load Page    url=${XIQSE_URL}
        Log  result is ${passed}
        XIQSE Quit Browser
        Exit For Loop If  "${passed}"=="PASS"
        Log  Waiting for Server
        # No need to sleep, the XIQSE Load Page has a built in wait of 60 seconds
    END
    # Run one more login, this will be the offical results, a failure here 
    # means something is not right and should be recorded.
    ${result}=    XIQSE Load Page    url=${XIQSE_URL}
    XIQSE Quit Browser
    Log  Final result is ${passed}

Check NAC Is Up
    [Documentation]    Checks the server is up and running.
# This needs to be changed to a wait until login works.
#   ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}
    Sleep  300s

Check Purview Is Up
    [Documentation]    Checks the server is up and running.
# This needs to be changed to a wait until login works.
#   ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}
    Sleep  300s

Check NGAnalytics Is Up
    [Documentation]    Checks the server is up and running.
# This needs to be changed to a wait until login works.
#   ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}
    Sleep  300s

Reset VM 
    [Documentation]  Sets a VM back to the specified snapshot 
    [Arguments]   ${ip}   ${user}   ${password}   ${vmid}   ${snapshotid}

    Log  ip=${ip}, vmid=${vmid}, snapshot=${snapshotid}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    # power off VM
    ${output} =  Send Paramiko CMD   ${sshSession}  vim-cmd vmsvc/power.off ${vmid} ${snapshotid} 0    ${ESX_VM_CMD_TIMEOUT_SEC}
    # set snapshot
    ${output} =  Send Paramiko CMD   ${sshSession}  vim-cmd vmsvc/snapshot.revert ${vmid} ${snapshotid} 0    ${ESX_VM_CMD_TIMEOUT_SEC}
    # power on VM
    ${output} =  Send Paramiko CMD   ${sshSession}  vim-cmd vmsvc/power.on ${vmid} ${snapshotid} 0    ${ESX_VM_CMD_TIMEOUT_SEC}
    Sleep  300s

Site Engine Upgrade
    [Documentation]  Handles the upgrade of site engine
    [Arguments]      ${upgradeParams}
    ${version} =   Get From Dictionary   ${upgradeParams}  version
    ${vmid} =   Get From Dictionary   ${upgradeParams}  xiqseVmId
    ${snapshot} =   Get From Dictionary   ${upgradeParams}  xiqseSnapShotId
    ${esxIp} =  Get From Dictionary  ${upgradeParams}  esxIp
    ${esxUser} =  Get From Dictionary  ${upgradeParams}  esxUser
    ${esxPw} =  Get From Dictionary  ${upgradeParams}  esxPw
    Log   Upgrading XIQ-SE from version ${version} to ${NSRELEASE_VERSION}
    Reset VM   ${esxIp}  ${esxUser}  ${esxPw}  ${vmid}  ${snapshot}
    Check Server Is Up
    Upgrade Site Engine

Nac Engine Upgrade
    [Documentation]  Handles the upgrade of NAC appliances
    [Arguments]      ${upgradeParams}
    ${version} =   Get From Dictionary   ${upgradeParams}  version
    ${vmid} =   Get From Dictionary   ${upgradeParams}  nacVmId
    ${snapshot} =   Get From Dictionary   ${upgradeParams}  nacSnapShotId
    ${esxIp} =  Get From Dictionary  ${upgradeParams}  esxIp
    ${esxUser} =  Get From Dictionary  ${upgradeParams}  esxUser
    ${esxPw} =  Get From Dictionary  ${upgradeParams}  esxPw
    Log   Upgrading NAC from version ${version} to ${NSRELEASE_VERSION}
    Reset VM   ${esxIp}  ${esxUser}  ${esxPw}  ${vmid}  ${snapshot}
    Check NAC Is Up
    Upgrade NAC Engine

Purview Engine Upgrade
    [Documentation]  Handles the upgrade of NAC appliances
    [Arguments]      ${upgradeParams}
    ${version} =   Get From Dictionary   ${upgradeParams}  version
    ${vmid} =   Get From Dictionary   ${upgradeParams}  purviewVmId
    ${snapshot} =   Get From Dictionary   ${upgradeParams}  purviewSnapShotId
    ${esxIp} =  Get From Dictionary  ${upgradeParams}  esxIp
    ${esxUser} =  Get From Dictionary  ${upgradeParams}  esxUser
    ${esxPw} =  Get From Dictionary  ${upgradeParams}  esxPw
    Log   Upgrading Purview from version ${version} to ${NSRELEASE_VERSION}
    Reset VM   ${esxIp}  ${esxUser}  ${esxPw}  ${vmid}  ${snapshot}
    Check Purview Is Up
    Upgrade Purview Engine

NGAnalytics Engine Upgrade
    [Documentation]  Handles the upgrade of NAC appliances
    [Arguments]      ${upgradeParams}
    ${version} =   Get From Dictionary   ${upgradeParams}  version
    ${vmid} =   Get From Dictionary   ${upgradeParams}  ngAnalyticsVmId
    ${snapshot} =   Get From Dictionary   ${upgradeParams}  ngAnalyticsSnapShotId
    ${esxIp} =  Get From Dictionary  ${upgradeParams}  esxIp
    ${esxUser} =  Get From Dictionary  ${upgradeParams}  esxUser
    ${esxPw} =  Get From Dictionary  ${upgradeParams}  esxPw
    Log   Upgrading NGAnalytics from version ${version} to ${NSRELEASE_VERSION}
    Reset VM   ${esxIp}  ${esxUser}  ${esxPw}  ${vmid}  ${snapshot}
    Check NGAnalytics Is Up
    Upgrade NGAnalytics Engine