#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David Truesdell
# Description   : Test Suite for sanity testing of basic XIQSE add and delete device functionality.
#                 This is qTest TC-951 in the XIQ-SE project.

*** Settings ***
Resource        ../../Inventory/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session

*** Variables ***
${XIQSE_URL}                ${xiqse.url}
${XIQSE_USERNAME}           ${xiqse.user}
${XIQSE_PASSWORD}           ${xiqse.password}
${XIQSE_IP_ADDRESS}         ${xiqse.ip}
${XIQSE_MAC}                ${xiqse.mac}
${INSTALL_MODE}             ${upgrades.install_mode}

${XIQ_URL}                  ${xiq.test_url}
${XIQ_EMAIL}                ${xiq.tenant_username}
${XIQ_PASSWORD}             ${xiq.tenant_password}

${DUT_IP}                   ${netelem1.ip}
${DUT_PROFILE}              ${netelem1.profile}
${DUT_LICENSE}              ${netelem1.license}


${WORLD_SITE}               World
${TEST_ARCHIVE}             /World
${TRAP_REGISTERED}          Trap Receiver Registered
${TRAP_UNREGISTERED}        Trap Receiver Unregistered
${SYSLOG_REGISTERED}        Syslog Receiver Registered
${SYSLOG_UNREGISTERED}      Syslog Receiver Unregistered
${OPS_DEVICE_DISCOVERY}     Device Discovery - Operation Complete
${OPS_LICENSE_CHECK}        Device License is XIQ_${DUT_LICENSE}

*** Test Cases ***
Test 1: Add Device and Confirm Success
    [Documentation]     Confirms a device can be successfuly aded to XIQ-SE
    [Tags]              nightly1    tcxe_951    xmc_5451    development    xiqse    acceptance    inventory    add_delete    test1

    Navigate and Create Device                          ${DUT_IP}  ${DUT_PROFILE}
    Wait For Operations Panel Operation To Complete     Device Added
    Confirm IP Address Present in Devices Table         ${DUT_IP}

Test 2: Verify Operations Panel Operations Complete Successfully
    [Documentation]     Confirms all operations panel operations completed successfully
    [Tags]              nightly1    tcxe_951    xmc_5451    development    xiqse    acceptance    inventory    add_delete    test2

    Log To Console  >> Confirms Device Poller Completed
    Wait For Operations Panel Operation To Complete     Device Poller

    Log To Console  >> Confirms Device License Check Completed
    Wait For Operations Panel Operation To Complete     Device License Check

    Log To Console  >> Confirms Discover Site Actions Completed
    Wait For Operations Panel Operation To Complete     Discover Site Actions

    Log To Console  >> Confirms Inventory Audit Completed
    Wait For Operations Panel Operation To Complete     Inventory Audit

    Log To Console  >> Confirms operations panel message for device discovery
    Confirm Operations Panel Message For Type           Inventory Audit    ${OPS_DEVICE_DISCOVERY}

    Log To Console  >> Confirms operations panel message for device license check
    Confirm Operations Panel Message For Type           Device License Check    ${OPS_LICENSE_CHECK}

Test 3: Verify Device Assigned Correct License
    [Documentation]     Navigates and verifies the device license on the specified device
    [Tags]              nightly1    tcxe_951    xmc_5451    development    xiqse    acceptance    inventory    add_delete    test3

    Navigate and Confirm Device License                 ${DUT_IP}  ${DUT_LICENSE}

Test 4: Verify Device Statistics Enabled
    [Documentation]     Navigates and verifies the device historical statistics is enabled on the specified device
    [Tags]              nightly1    tcxe_951    xmc_5451    development    xiqse    acceptance    inventory    add_delete    test4

    Navigate and Confirm Device Historical Statistics       ${DUT_IP}    Collecting Historical

Test 5: Verify Events For Add Device
    [Documentation]     Navigates and confirms the events view contains the expected event for add device
    [Tags]              nightly1    tcxe_951    xmc_5451    development    xiqse    acceptance    inventory    add_delete    test5

    Navigate to Events and Confirm Success
    Set Event Time Range and Confirm Success            Last 30 Minutes
    Set Event Type and Confirm Success                  Console,Inventory
    Set Event Search String and Confirm Success         added to the database
    Confirm Event Row Contains Text                     ${DUT_IP} has been added to the database
    Clear Event Search String and Confirm Success

Test 6: Verify Event For Device License
    [Documentation]     Navigates and confirms the events view contains the expected event for device license
    [Tags]              nightly1    tcxe_951    xmc_5451    development    xiqse    acceptance    inventory    add_delete    test6

    Set Event Search String and Confirm Success         ${DUT_IP}
    Confirm Event Row Contains Text                     Device License is XIQ_${DUT_LICENSE}
    Clear Event Search String and Confirm Success

Test 7: Verify Add Actions Register Trap Receiver Successful
    [Documentation]     Navigates to the Devices tab and verifies the trap status on the specified device
    [Tags]              nightly1    tcxe_951    xmc_5451    development    xiqse    acceptance    inventory    add_delete    test7

    Wait For Operations Panel Operation To Complete     Trap Configuration
    Navigate and Confirm Trap Status                    ${DUT_IP}    ${TRAP_REGISTERED}

Test 8: Verify Add Actions Register Syslog Receiver Successful
    [Documentation]     Navigates to the Devices tab and verifies the syslog status on the specified device
    [Tags]              nightly1    tcxe_951    xmc_5451    development    xiqse    acceptance    inventory    add_delete    test8

    Wait For Operations Panel Operation To Complete     Syslog Configuration
    Navigate and Confirm Syslog Status                  ${DUT_IP}    ${SYSLOG_REGISTERED}

Test 9: Verify Add Actions Add to Archive Successful
    [Documentation]     Navigates and confirms an archive exists in the Network> Archives tree in XIQ-SE and confirms the action was successful
    [Tags]              nightly1    tcxe_951    xmc_5451    development    xiqse    acceptance    inventory    add_delete    test9

    Navigate and Confirm Archive Exists In Tree         ${TEST_ARCHIVE}

Text 10: Unregister Trap Receiver and Confirm Success
    [Documentation]     Navigates to the Devices tab and unregisters the trap receiver on the specified device, confirming the status shows unregistered
    [Tags]              nightly1    tcxe_951    xmc_5451    development    xiqse    acceptance    inventory    add_delete    test10

    Navigate and Unregister Trap Receiver                   ${DUT_IP}
    Navigate and Confirm Trap Status                        ${DUT_IP}    ${TRAP_UNREGISTERED}

Text 11: Unregister Syslog Receiver and Confirm Success
    [Documentation]     Navigates to the Devices tab and unregisters the syslog receiver on the specified device, confirming the status shows unregistered
    [Tags]              nightly1    tcxe_951    xmc_5451    development    xiqse    acceptance    inventory    add_delete    test11

    Unregister Syslog Receiver and Confirm Success          ${DUT_IP}
    Navigate and Confirm Syslog Status                      ${DUT_IP}    ${SYSLOG_UNREGISTERED}

Test 12: Delete Device and Confirm Success
    [Documentation]     Navigates and deletes the specified device from XIQ-SE and confirms it was removed successfully
    [Tags]              nightly1    tcxe_951    xmc_5451    development    xiqse    acceptance    inventory    add_delete    test12

    Navigate to Devices and Confirm Success
    Delete Device and Confirm Success                   ${DUT_IP}
    Wait For Operations Panel Operation To Complete     Device Removed
    Confirm IP Address Not Present in Devices Table     ${DUT_IP}

Test 13: Verify Event for Delete Device
    [Documentation]     Navigates and confirms the events view contains the expected event for delete device
    [Tags]              nightly1    tcxe_951    xmc_5451    development    xiqse    acceptance    inventory    add_delete    test13

    Navigate to Events and Confirm Success
    Set Event Time Range and Confirm Success            Last 30 Minutes
    Set Event Type and Confirm Success                  Inventory
    Set Event Search String and Confirm Success         deleted from the database
    Confirm Event Row Contains Text                     ${DUT_IP} and Site Engine data were deleted from the database
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
    Enable Site Actions - Add to Archive, Add Trap Receiver & Add Syslog Receiver    ${WORLD_SITE}
    Onboard XIQSE To XIQ If In Connected Mode        ${INSTALL_MODE}  ${XIQSE_IP_ADDRESS}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}
    Clear Operations Panel and Confirm Success

Tear Down Test and Close Session
    [Documentation]     Cleans up all items that were set up for the test

    Restore Web Server Options to Default and Confirm Success
    Restore Site Engine General Options to Default and Confirm Success
    Set Alarm Event Search Scope    false
    Navigate and Delete Archive                             ${TEST_ARCHIVE}
    Log Out of XIQSE and Quit Browser
    Remove XIQSE From XIQ If In Connected Mode              ${INSTALL_MODE}  ${XIQ_EMAIL}  ${XIQ_PASSWORD}  ${XIQ_URL}  ${XIQSE_MAC}
