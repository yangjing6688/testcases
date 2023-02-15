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
    [Documentation]     deletes existing file, downloads the upgrade binary to site engine and perform upgrade

    Delete SE Existing Files  ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}
    Download File   ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${XIQSE_FOLDER}  ${NSRELEASE_XIQSE_FILE}
    Install SE Software  ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${NSRELEASE_XIQSE_FILE}
    Check Server Exit Code  ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${NSRELEASE_XIQSE_FILE}
    Sleep  120s
    NBI Check Server Is Up    ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${NBI_FILE}
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
    NBI Check Server Is Up    ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${NBI_FILE}

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
    [Documentation]   Installs the downloaded binary on the PurviewSSH_PORT appliance
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
    NBI Check Server Is Up                ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${NBI_FILE}

Inject XIQ CLOUD properties into NSJBoss Properties File and Restart
    [Documentation]     Injects Base and Redirector XIQ Urls into NSJBoss.properties file and restarts XIQSE service
    [Arguments]         ${ip}  ${user}  ${password}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  echo extreme.xiq.baseUrl=${XIQ_BASE_URL} >> /usr/local/Extreme_Networks/NetSight/appdata/NSJBoss.properties
    ${output} =  Send Paramiko CMD        ${sshSession}  echo extreme.xiq.redirectorurl=${XIQ_REDIRECT_URL} >> /usr/local/Extreme_Networks/NetSight/appdata/NSJBoss.properties
    # DO NOT DELETE - Specifically setting the Serial Number here so the VM will retain the expected serial number
    ${output} =  Send Paramiko CMD        ${sshSession}  echo DeveloperOptions.airGapSerialNumber=${XIQSE_SERIAL} >> ~/NetSight/DeveloperOptions.properties
    ${output} =  Send Paramiko CMD        ${sshSession}  ${XIQSE_RESTART_SERVER}
    NBI Check Server Is Up                ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${NBI_FILE}


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
    ${output} =  Send Paramiko CMD        ${sshSession}  cat ${NSRELEASE_NAC_LOG_FILE} | grep "upgrade to ${NSRELEASE_BUILD} was completed"
    Should Contain  ${output}  upgrade to ${NSRELEASE_BUILD} was completed

Check Purview Exit Code
    [Documentation]     Parses installer log for exit code. If "upgrade was completed" line is present, it was successful.
    [Arguments]    ${ip}  ${user}  ${password}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  cat ${NSRELEASE_Purview_LOG_FILE} | grep "upgrade to ${NSRELEASE_BUILD} was completed"
    Should Contain  ${output}  upgrade to ${NSRELEASE_BUILD} was completed

Check NGAnalytics Exit Code
    [Documentation]     Parses installer log for exit code. If "upgrade was completed" line is present, it was successful.
    [Arguments]    ${ip}  ${user}  ${password}

    ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
    ${output} =  Send Paramiko CMD        ${sshSession}  cat ${NSRELEASE_NGANALYTICS_LOG_FILE} | grep "upgrade to ${NSRELEASE_BUILD} was completed"
    Should Contain  ${output}  upgrade to ${NSRELEASE_BUILD} was completed

NBI Check Server Is Up
    [Documentation]    Checks the server is up and running via an NBI call
    [Arguments]        ${ip}  ${user}  ${password}  ${nbi_file}

    FOR    ${index}    IN RANGE    45
        ${sshSession} =    open_paramiko_ssh_spawn  ${ip}  ${user}  ${password}  ${SSH_PORT}
        IF  "${sshSession}"=="-1"
            Log To Console  Failed to open ssh session for ${ip}: ${user},${password}
        ELSE
            ${output} =  Send Paramiko CMD        ${sshSession}  rm ${nbi_file}
            ${output} =  Send Paramiko CMD        ${sshSession}  curl -k -u ${user}:${password} https://${ip}:8443/Clients/nbi/graphql/index.html?query=query%7Bnetwork%20%7Bsites%20%7BsiteName%7D%7D%7D > ${nbi_file}
            ${result} =  Send Paramiko CMD        ${sshSession}  cat ${nbi_file} | grep "World"

            Exit For Loop If  'World' in '''${result}'''
        END
        Sleep  60s
        IF  "${index}"=="44"
            Log To Console          Server is not yet up. Please check the server for any errors
            Should Be True          'World' in '''${result}'''
        ELSE
            Log To Console  Waiting for Server
        END
    END

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
    Log   Upgrading XIQ-SE from version ${version} to ${NSRELEASE_BUILD}
    Reset VM   ${esxIp}  ${esxUser}  ${esxPw}  ${vmid}  ${snapshot}
    NBI Check Server Is Up    ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${NBI_FILE}
    Upgrade Site Engine
    NBI Check Server Is Up    ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${NBI_FILE}

Nac Engine Upgrade
    [Documentation]  Handles the upgrade of NAC appliances
    [Arguments]      ${upgradeParams}
    ${version} =   Get From Dictionary   ${upgradeParams}  version
    ${vmid} =   Get From Dictionary   ${upgradeParams}  nacVmId
    ${snapshot} =   Get From Dictionary   ${upgradeParams}  nacSnapShotId
    ${esxIp} =  Get From Dictionary  ${upgradeParams}  esxIp
    ${esxUser} =  Get From Dictionary  ${upgradeParams}  esxUser
    ${esxPw} =  Get From Dictionary  ${upgradeParams}  esxPw
    Log   Upgrading NAC from version ${version} to ${NSRELEASE_BUILD}
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
    Log   Upgrading Purview from version ${version} to ${NSRELEASE_BUILD}
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
    Log   Upgrading NGAnalytics from version ${version} to ${NSRELEASE_BUILD}
    Reset VM   ${esxIp}  ${esxUser}  ${esxPw}  ${vmid}  ${snapshot}
    Check NGAnalytics Is Up
    Upgrade NGAnalytics Engine

UPDATE_SUITE_VERSION_VARIABLES
    [Documentation]    Gets the latest version and sets the install variables
    [Arguments]        ${release}

    ${result} =     Run Process   curl    http://nsrelease.extremenetworks.com/release/?release\=${release}
    @{output} =     Split String   ${result.stdout}    Release Version\=
    ${res} =        Split String   ${output}[1]    <
    ${version}=     Set Variable    ${res}[0]
    ${base_path}=   Set Variable  http://nsrelease.extremenetworks.com/release/netsightweb/ns_console/Console/NETSIGHT_Suite_


    # Set Suite variables

    Set Suite Variable    ${LOG_DIRECTORY}                    /var/log/
    Set Suite Variable    ${XIQSE_FILE_PREFIX}                ExtremeCloudIQSiteEngine_
    Set Suite Variable    ${NAC_BINARY_PREFIX}                nac_appliance_64bit_sw_upgrade_to_
    Set Suite Variable    ${PURVIEW_BINARY_PREFIX}            purview_appliance_upgrade_to_
    Set Suite Variable    ${NGANALYTICS_BINARY_PREFIX}        analytics_appliance_upgrade_to_

    Set Suite Variable    ${XIQSE_FOLDER}                     NetSight
    Set Suite Variable    ${NAC_FOLDER}                       NAC
    Set Suite Variable    ${PURVIEW_FOLDER}                   Purview
    Set Suite Variable    ${NGANALYTICS_FOLDER}               Analytics

    Set Suite Variable    ${XIQSE_LOG_PREFIX}                 ExtremeCloudIQSiteEngine_
    Set Suite Variable    ${NAC_LOG_PREFIX}                   nacSoftwareUpgradeTo
    Set Suite Variable    ${PURVIEW_LOG_PREFIX}               purviewSoftwareUpgradeTo
    Set Suite Variable    ${NGANALYTICS_LOG_PREFIX}           analyticsSoftwareUpgradeTo

    Set Suite Variable    ${NSRELEASE_BUILD}                  ${version}
    Set Suite Variable    ${NSRELEASE_XIQSE_FILE}             ${XIQSE_FILE_PREFIX}${version}_64bit_install.bin
    Set Suite Variable    ${NSRELEASE_XIQSE_LOG_FILE}         ${XIQSE_LOG_PREFIX}${version}_64bit_install.log
    Set Suite Variable    ${NSRELEASE_VERSION_BASE}           ${base_path}${version}
    Set Suite Variable    ${NSRELEASE_NAC_FILE}               ${NAC_BINARY_PREFIX}${version}.bin
    Set Suite Variable    ${NSRELEASE_NAC_LOG_FILE}           ${LOG_DIRECTORY}${NAC_LOG_PREFIX}${version}.log
    Set Suite Variable    ${NSRELEASE_PURVIEW_FILE}           ${PURVIEW_BINARY_PREFIX}${version}.bin
    Set Suite Variable    ${NSRELEASE_PURVIEW_LOG_FILE}       ${LOG_DIRECTORY}${PURVIEW_LOG_PREFIX}${version}.log
    Set Suite Variable    ${NSRELEASE_NGANALYTICS_FILE}       ${NGANALYTICS_BINARY_PREFIX}${version}.bin
    Set Suite Variable    ${NSRELEASE_NGANALYTICS_LOG_FILE}   ${LOG_DIRECTORY}${NGANALYTICS_LOG_PREFIX}${version}.log

    [return]    ${version}