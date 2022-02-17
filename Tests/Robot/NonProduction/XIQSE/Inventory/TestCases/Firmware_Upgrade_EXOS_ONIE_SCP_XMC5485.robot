#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David Truesdell
# Description   : Test Suite for testing an EXOS ONIE SCP firmware upgrade within XIQSE.
#                 This is qTest TC-904 in the XIQSE project.

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

${DUT_IP}                           ${netelem9.ip}
${DUT_PROFILE}                      ${netelem9.profile}

${FIRMWARE_SCP_DIRECTORY}           /root/firmware/images
${EXOS_RELEASE_BASE}                http://biltmore.extremenetworks.com/image_pool/public
${EXOS_SCP_DEFINITION_FILENAME}     ExtremeXOS - SCP (VR-Default)
${EXOS_SCP_TRANSFER_MODE}           SCP
${EXOS_UPGRADE_RELEASE_PARENT}      31_5
${EXOS_INT_DIRECTORY}               31.5.1.5
${EXOS_UPGRADE_RELEASE_VERSION}     31.5.1.5
${EXOS_FILENAME_PREFIX}             onie-
${EXOS_FILENAME_EXTENSION}          x86_64.xos
${EXOS_UPGRADE_RELEASE}             31.5.1.5
${EXOS_FIRMWARE_VERSION}            31.5.1.5

${SSH_PORT}                         22
${DOWNLOAD_TIMEOUT_SEC}             300
${INSTALL_DOWNLOAD_TIMEOUT_SEC}     7200

${WORLD_SITE}                       World
${OPS_PANEL_RESTART}                Device Restart - Operation Complete
${OPS_PANEL_FIRMWARE_DOWNLOAD}      Firmware Download - Operation Complete
${EVENT_DEVICE_RESTART}             Device Restart Manual Reset: (${DUT_IP}) - Operation Complete
${EVENT_FIRMWARE_DOWNLOAD}          (${DUT_IP}) - Operation Complete.  Downloaded ${EXOS_FILENAME_PREFIX}${EXOS_UPGRADE_RELEASE_VERSION}.${EXOS_FILENAME_EXTENSION}


*** Test Cases ***
Test 1: Perform Upgrade Firmware
    [Documentation]     Perform firmware upgrade of switch in XIQSE
    [Tags]              xiqse_tc_904    xmc_5485    development    xiqse    inventory    firmware_upgrade    exos    onie    scp    test1

    Perform Firmware Upgrade and Confirm Success        ${DUT_IP}    ${EXOS_SCP_TRANSFER_MODE}    ${EXOS_SCP_DEFINITION_FILENAME}
    ...                                                 ${EXOS_UPGRADE_RELEASE_VERSION}    ${EXOS_FIRMWARE_VERSION}

Test 2: Confirm Operations Panel Message
    [Documentation]     Confirms the operations panel contains the expected messages
    [Tags]              xiqse_tc_904    xmc_5485    development    xiqse    inventory    firmware_upgrade    exos    onie    scp    test2

    XIQSE Operations Wait Until Operation Complete      Inventory Audit
    Confirm Operations Panel Message For Type           Inventory Audit  ${OPS_PANEL_RESTART}
    Log To Console  >> THIS IS FUTURE TEST SECTION TO CONFIRM FIRMWARE DOWNLOAD EVENT
#    Confirm Operations Panel Message For Type      Inventory Audit  ${OPS_PANEL_FIRMWARE_DOWNLOAD}

Test 3: Confirm Events
    [Documentation]     Confirms the events view contains the expected events
    [Tags]              xiqse_tc_904    xmc_5485    development    xiqse    inventory    firmware_upgrade    exos    onie    scp    test3

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

    Log Into XIQSE and Close Panels               ${XIQSE_USERNAME}    ${XIQSE_PASSWORD}    url=${XIQSE_URL}
    Set Option Web Server Session Timeout and Confirm Success  7  day(s)
    Set Option Device Tree Name Format and Confirm Success     IP Address
    Navigate and Set Option Status Polling Group 2 Interval and Confirm Success      2
    Navigate and Set Option SCP Login Information Anonymous and Confirm Success      false
    Set Option SCP Username and Password Login Information and Confirm Success       ${XIQSE_USERNAME}    ${XIQSE_PASSWORD}
    Disable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver   ${WORLD_SITE}
    Download Firmware to XIQ-SE and Confirm Success    ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${FIRMWARE_SCP_DIRECTORY}
    ...    ${EXOS_RELEASE_BASE}/${EXOS_UPGRADE_RELEASE_PARENT}/${EXOS_INT_DIRECTORY}/${EXOS_FILENAME_PREFIX}${EXOS_UPGRADE_RELEASE_VERSION}.${EXOS_FILENAME_EXTENSION}
    ...    ${FIRMWARE_SCP_DIRECTORY}/${EXOS_FILENAME_PREFIX}${EXOS_UPGRADE_RELEASE_VERSION}.${EXOS_FILENAME_EXTENSION}
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
    Restore Status Polling Options to Default and Confirm Success
    Restore Default Inventory Manager Options and Confirm Success
    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    Delete Firmware from XIQ-SE and Confirm Success    ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}  ${FIRMWARE_SCP_DIRECTORY}
    Log Out of XIQSE and Quit Browser
    Remove XIQSE From XIQ If In Connected Mode    ${INSTALL_MODE}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}  ${XIQ_URL}  ${XIQSE_MAC}
