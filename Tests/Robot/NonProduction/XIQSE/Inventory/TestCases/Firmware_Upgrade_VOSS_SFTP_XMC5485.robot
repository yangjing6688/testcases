#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David Truesdell
# Description   : Test Suite for testing an VOSS SFTP firmware upgrade within XIQSE.
#                 This is qTest TC-911 in the XIQSE project.

*** Settings ***
Library         xiqse/flows/network/devices/site/actions/XIQSE_NetworkDevicesSiteActions.py
Library         xiqse/flows/network/devices/tree_panel/XIQSE_NetworkDevicesTreePanel.py
Library         xiqse/flows/network/XIQSE_Network.py
Library         xiqse/flows/network/devices/devices/XIQSE_NetworkDevicesDevicesRestartDevice.py
Library         xiqse/flows/network/devices/tree_panel/XIQSE_NetworkDevicesTreePanelDeviceType.py

Resource        ../../Inventory/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session

*** Variables ***
${XIQSE_URL}                        ${xiqse.url}
${XIQSE_USERNAME}                   ${xiqse.user}
${XIQSE_PASSWORD}                   ${xiqse.password}
${XIQSE_IP_ADDRESS}                 ${xiqse.ip}
${XIQSE_MAC}                        ${xiqse.mac}
${INSTALL_MODE}                     ${upgrades.install_mode}

${XIQ_URL}                          ${xiq.test_url}
${XIQ_EMAIL}                        ${xiq.tenant_username}
${XIQ_PASSWORD}                     ${xiq.tenant_password}

${DUT_IP}                           ${netelem2.ip}
${DUT_PROFILE}                      ${netelem2.profile}

${FIRMWARE_SFTP_DIRECTORY}          /root/firmware/images
${VOSS_RELEASE_BASE}                http://nhweb.labs.extremenetworks.com/voss
${VOSS_SFTP_DEFINITION_FILENAME}    VOSS - SFTP
${VOSS_SFTP_TRANSFER_MODE}          SFTP (default)
${VOSS_UPGRADE_RELEASE_DIRECTORY}   v8.5.0.0
${VOSS_INT_DIRECTORY}               int029
${VOSS_DEV_TYPE}                    VOSS4400
${VOSS_UPGRADE_RELEASE_VERSION}     ${VOSS_DEV_TYPE}.8.5.0.0int029
${VOSS_FIRMWARE_VERSION}            8.5.0.0_B029
${VOSS_IMAGE_EXTENSION}             tgz
${VOSS_UI_DISPLAY_VERSION}          v${VOSS_UPGRADE_RELEASE_VERSION}
${VOSS_UPGRADE_RELEASE}             ${VOSS_UPGRADE_RELEASE_VERSION}.${VOSS_IMAGE_EXTENSION}

${SSH_PORT}                         22
${DOWNLOAD_TIMEOUT_SEC}             300
${INSTALL_DOWNLOAD_TIMEOUT_SEC}     7200

${WORLD_SITE}                       World
${OPS_PANEL_RESTART}                Device Restart - Operation Complete
${OPS_PANEL_FIRMWARE_DOWNLOAD}      Firmware Download - Operation Complete
${EVENT_DEVICE_RESTART}             Device Restart Manual Reset: (${DUT_IP}) - Operation Complete
${EVENT_FIRMWARE_DOWNLOAD}          (${DUT_IP}) - Operation Complete.  Downloaded ${VOSS_UPGRADE_RELEASE}


*** Test Cases ***
Test 1: Perform Upgrade Firmware
    [Documentation]     Perform firmware upgrade of switch in XIQSE
    [Tags]              tcxe_911    xmc_5485    development    xiqse    inventory    firmware_upgrade    voss    tftp    test1

    Perform Firmware Upgrade and Confirm Success        ${DUT_IP}    ${VOSS_SFTP_TRANSFER_MODE}    ${VOSS_SFTP_DEFINITION_FILENAME}
    ...                                                 ${VOSS_UPGRADE_RELEASE}    ${VOSS_FIRMWARE_VERSION}

Test 2: Confirm Operations Panel Message
    [Documentation]     Confirms the operations panel contains the expected messages
    [Tags]              tcxe_911    xmc_5485    development    xiqse    inventory    firmware_upgrade    voss    tftp    test2

    XIQSE Operations Wait Until Operation Complete      Inventory Audit
    Confirm Operations Panel Message For Type           Inventory Audit  ${OPS_PANEL_RESTART}
    Log To Console  >> THIS IS FUTURE TEST SECTION TO CONFIRM FIRMWARE DOWNLOAD EVENT
#    Confirm Operations Panel Message For Type      Inventory Audit  ${OPS_PANEL_FIRMWARE_DOWNLOAD}

Test 3: Confirm Events
    [Documentation]     Confirms the events view contains the expected events
    [Tags]              tcxe_911    xmc_5485    development    xiqse    inventory    firmware_upgrade    voss    tftp    test3

    Navigate to Events and Confirm Success
    Set Event Time Range and Confirm Success        Last 30 Minutes
    Set Event Type and Confirm Success              Inventory
    Set Event Search String and Confirm Success     Firmware Download
    Confirm Event Row Contains Text                 ${EVENT_FIRMWARE_DOWNLOAD}
    Clear Event Search String and Confirm Success
    Set Event Search String and Confirm Success     Device Restart
    Confirm Event Row Contains Text                 ${EVENT_DEVICE_RESTART}
    Clear Event Search String and Confirm Success


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs in and configures everything that is required for the test to run

    Log Into XIQSE and Confirm Success                 ${XIQSE_USERNAME}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}
    Handle License Agreement If Displayed              ${XIQ_EMAIL}  ${XIQ_PASSWORD}
    Close Panels on Login If Displayed
    Set Option Web Server Session Timeout and Confirm Success  7  day(s)
    Set Alarm Event Search Scope    true
    Set Option Device Tree Name Format and Confirm Success     IP Address
    Navigate and Set Option Status Polling Group 2 Interval and Confirm Success      2
    Navigate and Set Option SFTP Login Information Anonymous and Confirm Success     false
    Set Option SFTP Username and Password Login Information and Confirm Success      ${XIQSE_USERNAME}    ${XIQSE_PASSWORD}
    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver   ${WORLD_SITE}
    Download Firmware to XIQ-SE and Confirm Success    ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${FIRMWARE_SFTP_DIRECTORY}
    ...    ${VOSS_RELEASE_BASE}/${VOSS_UPGRADE_RELEASE_DIRECTORY}/${VOSS_INT_DIRECTORY}/${VOSS_UPGRADE_RELEASE}
    ...    ${FIRMWARE_SFTP_DIRECTORY}/${VOSS_UPGRADE_RELEASE}
    ...    ${DOWNLOAD_TIMEOUT_SEC}
    Onboard XIQSE To XIQ If In Connected Mode     ${INSTALL_MODE}  ${XIQSE_IP_ADDRESS}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}
    Navigate and Create Device                    ${DUT_IP}  ${DUT_PROFILE}
    Clear Operations Panel and Confirm Success

Tear Down Test and Close Session
    [Documentation]     Logs in and cleans up all items that were set up for the test

    Navigate to Devices and Confirm Success
    Delete Device and Confirm Success             ${DUT_IP}
    Restore Web Server Options to Default and Confirm Success
    Restore Site Engine General Options to Default and Confirm Success
    Set Alarm Event Search Scope    false
    Restore Status Polling Options to Default and Confirm Success
    XIQSE Restore Default Inventory Manager Options and Save
    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    Delete Firmware from XIQ-SE and Confirm Success    ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${FIRMWARE_SFTP_DIRECTORY}
    Log Out of XIQSE and Quit Browser
    Remove XIQSE From XIQ If In Connected Mode     ${INSTALL_MODE}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}  ${XIQ_URL}  ${XIQSE_MAC}
