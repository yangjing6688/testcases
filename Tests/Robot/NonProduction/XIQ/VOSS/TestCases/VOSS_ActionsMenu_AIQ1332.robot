#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for testing device actions of the VOSS switch from the Actions menu:
#                   - Assign Network Policy
#                   - Assign Location
#                   - Reboot
#                 This is qTest test case TC-8387 in the CSIT project.

*** Settings ***
Library          xiq/flows/manage/Location.py

Resource         ../../VOSS/Resources/AllResources.robot

Force Tags       testbed_voss_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${xiq.test_url}
${XIQ_USER}                 ${xiq.tenant_username}
${XIQ_PASSWORD}             ${xiq.tenant_password}
${IQAGENT}                  ${xiq.sw_connection_host}

${DUT_SERIAL}               ${netelem3.serial}
${DUT_NAME}                 ${netelem3.name}
${DUT_TEMPLATE}             ${netelem3.template}
${DUT_CONSOLE_IP}           ${netelem3.ip}
${DUT_CONSOLE_PORT}         ${netelem3.port}
${DUT_USERNAME}             ${netelem3.username}
${DUT_PASSWORD}             ${netelem3.password}
${DUT_PLATFORM}             ${netelem3.platform}

${DEFAULT_DEVICE_PWD}       Aerohive123
${LOCATION}                 auto_location_01, Santa Clara, building_02, floor_04
${LOCATION_DISPLAY}         auto_location_01 >> Santa Clara >> building_02 >> floor_04
${POLICY_NAME}              VOSS_POLICY_AUTO
${SSID_NAME}                VOSS_SSID_AUTO


*** Test Cases ***
Test 1: Confirm Action Assign Network Policy
    [Documentation]     Confirms the Assign Network Policy action works successfully
    [Tags]              csit_tc_8387    aiq_1332    development    xiq    voss    actions_menu    policy    test1

    # Assign the network policy
    ${action_result}=  Update Network Policy to Switch      ${POLICY_NAME}  ${DUT_SERIAL}
    Should Be Equal As Integers                             ${action_result}     1

    # Confirm the device row shows the network policy
    ${pol_result}=  Get Device Details                      ${DUT_SERIAL}   POLICY
    Should Contain                                          ${pol_result}   ${POLICY_NAME}

Test 2: Confirm Action Assign Location
    [Documentation]     Confirms the Assign Location action works successfully
    [Tags]              csit_tc_8387    aiq_1332    development    xiq    voss    actions_menu    location    test2

    # Assign the location
    ${action_result}=  Assign Location With Device Actions      ${DUT_SERIAL}  ${LOCATION}
    Should Be Equal As Integers                                 ${action_result}     1

    # Confirm the device row shows the location
    ${loc_result}=  Get Device Details                          ${DUT_SERIAL}   LOCATION
    Should Contain                                              ${loc_result}   ${LOCATION_DISPLAY}

Test 3: Confirm Action Reboot
    [Documentation]     Confirms the Reboot action works successfully
    [Tags]              csit_tc_8387    aiq_1332    development    xiq    voss    actions_menu    reboot    test3

    # Reboot the device
    ${action_result}=  Device Reboot                ${DUT_SERIAL}
    Should Be Equal As Integers                     ${action_result}     1

    # Confirm the device reboots
    ${reboot_result}=  Wait Until Device Reboots    ${DUT_SERIAL}
    Should Be Equal As Integers                     ${reboot_result}     1


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}
    Change Device Password and Confirm Success  ${DEFAULT_DEVICE_PWD}
    Create Open Express Policy With Switch Template and Confirm Success  ${POLICY_NAME}  ${SSID_NAME}  ${DUT_TEMPLATE}
    Configure Test Device  ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${IQAGENT}
    Onboard New Test Device  ${DUT_SERIAL}  ${LOCATION}

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    Clean Up Test Device and Confirm Success    ${DUT_SERIAL}
    Delete Policy and Confirm Success           ${POLICY_NAME}
    Delete SSID and Confirm Success             ${SSID_NAME}
    Log Out of XIQ and Quit Browser

Configure Test Device
    [Documentation]     Configures the specified test device by resetting to factory defaults and configuring the iqagent
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${agent}

    Reset VOSS Switch to Factory Defaults  ${ip}  ${port}  ${user}  ${pwd}
    Configure iqagent for VOSS Switch      ${ip}  ${port}  ${user}  ${pwd}  ${agent}

Onboard New Test Device
    [Documentation]     Onboards the specified test device, deleting it first if it already exists
    [Arguments]         ${serial}  ${location}

    Navigate to Devices and Confirm Success

    # If the device has already been onboarded, delete it first
    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}

    # Onboard the device
    Onboard VOSS Device  ${serial}  loc_name=${location}
    sleep   ${DEVICE_ONBOARDING_WAIT}
    Confirm Device Serial Present  ${serial}

Clean Up Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Navigate to Devices and Confirm Success

    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}
