#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Dan McCarthy
# Description   : Verifies that a Digital Twin device can be onboarded Manage> Devices page
#                 For 22R4 & 22R5 - the "Digital Twin" feature is controlled by a "soft launch" url
#                 qTest Test Cases in the XIQ Mainline project.
#                   TCXM-21215 - "Onboard" Switch Engine Digital Twin device
#                   TCXM-21216 - "Onboard" Fabric Engine Digital Twin device
#                   TCXM-21229 - Manage > Devices: "Actions" menu for Digital Twin device
#                   TCXM-21230 - "Shutdown" Digital Twin device
#                   TCXM-21275 - "Relaunch" Digital Twin device
#                   TCXM-20308 - Digital Twin - Delete device
#                   TCXM-21616 - Digital Twin - Enable the feature using the "Soft Launch" URL
#                   TCXM-21617 - Digital Twin - Disable the feature using the "Soft Launch" URL

*** Settings ***
Library          common/Cli.py
Library          xiq/flows/manage/Location.py
Library          xiq/flows/manage/DevicesActions.py

Resource         ../../DigitalTwin/Resources/AllResources.robot

Force Tags       testbed_not_required

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${test_url}
${XIQ_USER}                 ${tenant_username}
${XIQ_PASSWORD}             ${tenant_password}

${ENABLE_DT_FEATURE}        ${XIQ_URL}/hm-webapp/?digitalTwin=true#/devices
${DISABLE_DT_FEATURE}       ${XIQ_URL}/hm-webapp/?digitalTwin=false#/devices

${DT_SE_PERSONA}            SwitchEngine
${DT_SE_MODEL}              5320-24T-8XE
${DT_SE_VERSION}            32.1.1.6
${DT_SE_POLICY}
${DT_FE_PERSONA}            FabricEngine
${DT_FE_MODEL}              5420F-24S-4XE
${DT_FE_VERSION}            8.7.0.0
${DT_FE_POLICY}

${LOCATION}                 San Jose, building_01, floor_02
${DEFAULT_DEVICE_PWD}       Aerohive123
${POLICY_NAME}              Automation_Policy


*** Test Cases ***
Test 1: Enable Digital Twin Soft Launch Feature
    [Documentation]     Enables the "Digital Twin" soft-launch feature. (Required for 22R4 & 22R5)
    [Tags]      xim_tcxm_21616   xiq_4627    xiq_6669   development    xiq    digital_twin    test1

    Navigate to Devices and Confirm Success

    ${result}=   Is Digital Twin Option Visible
    Should Be Equal As Integers                             ${result}   -1

    ${result}=   XIQ Soft Launch Feature Url                ${ENABLE_DT_FEATURE}
    Should Be Equal As Integers                             ${result}   1

    ${result}=   Is Digital Twin Option Visible
    Should Be Equal As Integers                             ${result}   1

    [Teardown]    Refresh Page

Test 2: Onboard Digital Twin Switch Engine Device
    [Documentation]     Onboard "Digital Twin" Switch Engine device.
    [Tags]      xim_tcxm_21215    xim_tcxm_21229    xiq_4627     xiq_6669    development    xiq    digital_twin    test2

    Navigate to Devices and Confirm Success

    ${dt_se_serial}=  Onboard Device DT                     device_type=Digital_Twin        os_persona=${DT_SE_PERSONA}
    ...                                                     device_model=${DT_SE_MODEL}     os_version=${DT_SE_VERSION}
    ...                                                     policy=${DT_SE_POLICY}
    Set Suite Variable                                      ${DT_SE_SERIAL}     ${dt_se_serial}
    Should Not Be Equal As Strings                          ${DT_SE_SERIAL}     -1

    ${dt_se_icon}=    Get Device Status Icon                ${DT_SE_SERIAL}
    Should Be Equal As Strings                              ${dt_se_icon}       digital_twin

    Select Device                                           ${DT_SE_SERIAL}
    ${dt_action_menu}=  Actions Relaunch Digital Twin Visible
    Should Be Equal As Integers                             ${dt_action_menu}   1
    ${dt_action_menu}=  Actions Shutdown Digital Twin Visible
    Should Be Equal As Integers                             ${dt_action_menu}   -1

    ${dt_se_status}=    Wait Until Device Online            device_serial=${DT_SE_SERIAL}   retry_duration=5    retry_count=60
    Should Be Equal As Integers                             ${dt_se_status}     1

    ${dt_se_state}=    Get Device Status                    ${DT_SE_SERIAL}
    Should Be Equal As Strings                              ${dt_se_state}      green

    ${dt_se_mac}=   Get Device Details                      ${dt_se_serial}     MAC
    Set Suite Variable                                      ${DT_SE_MAC}        ${dt_se_mac}

    [Teardown]    Refresh Page

Test 3: Onboard Digital Twin Fabric Engine Device
    [Documentation]     Onboard "Digital Twin" Fabric Engine device.
    [Tags]      xim_tcxm_21216   xim_tcxm_21229    xiq_4627   xiq_6669    development    xiq    digital_twin    test3

    Navigate to Devices and Confirm Success

    ${dt_fe_serial}=  Onboard Device DT                     device_type=digital_twin        os_persona=${DT_FE_PERSONA}
    ...                                                     device_model=${DT_FE_MODEL}     os_version=${DT_FE_VERSION}
    ...                                                     policy=${DT_FE_POLICY}
    Set Suite Variable                                      ${DT_FE_SERIAL}     ${dt_fe_serial}
    Should Not Be Equal As Strings                          ${DT_FE_SERIAL}     -1

    ${dt_fe_icon}=    Get Device Status Icon                ${DT_FE_SERIAL}
    Should Be Equal As Strings                              ${dt_fe_icon}       digital_twin

    Select Device                                           ${DT_FE_SERIAL}
    ${dt_action_menu}=  Actions Relaunch Digital Twin Visible
    Should Be Equal As Integers                             ${dt_action_menu}   1
    ${dt_action_menu}=  Actions Shutdown Digital Twin Visible
    Should Be Equal As Integers                             ${dt_action_menu}   -1

    ${dt_fe_status}=    Wait Until Device Online            device_serial=${DT_FE_SERIAL}   retry_duration=5    retry_count=60
    Should Be Equal As Integers                             ${dt_fe_status}     1

    ${dt_fe_state}=    Get Device Status                    ${DT_FE_SERIAL}
    Should Be Equal As Strings                              ${dt_fe_state}      green

    ${dt_fe_mac}=   Get Device Details                      ${DT_FE_SERIAL}     MAC
    Set Suite Variable                                      ${DT_FE_MAC}        ${dt_fe_mac}

    [Teardown]    Refresh Page

Test 4: Shutdown Digital Twin Device
    [Documentation]     Shutdown "Digital Twin" devices and verify Actions menu options.
    [Tags]      xim_tcxm_21230   xim_tcxm_21229    xiq_4627   xiq_6669    development    xiq    digital_twin    test4

    Navigate to Devices and Confirm Success

    Should Not Be Equal As Strings                          ${DT_SE_SERIAL}     -1
    Shutdown Digital Twin Device                            ${DT_SE_MAC}

    Should Not Be Equal As Strings                          ${DT_FE_SERIAL}     -1
    Shutdown Digital Twin Device                            ${DT_FE_MAC}

    ${dt_se_status}=    Wait Until Device Offline           device_mac=${DT_SE_MAC}     retry_duration=5    retry_count=60
    Should Be Equal As Integers                             ${dt_se_status}     1
    ${dt_fe_status}=    Wait Until Device Offline           device_mac=${DT_FE_MAC}     retry_duration=5    retry_count=60
    Should Be Equal As Integers                             ${dt_fe_status}     1

    ${dt_se_state}=    Get Device Status                    ${DT_SE_SERIAL}
    Log To Console    Digital Twin Device Status '${dt_se_state}'
    Should Be Equal As Strings                              ${dt_se_state}      disconnected
    ${dt_fe_state}=    Get Device Status                    ${DT_FE_SERIAL}
    Log To Console    Digital Twin Device Status ${dt_fe_state}
    Should Be Equal As Strings                              ${dt_fe_state}      disconnected

    Select Device                                           ${DT_SE_SERIAL}
    Select Device                                           ${DT_FE_SERIAL}
    ${dt_action_menu}=  Actions Relaunch Digital Twin Visible
    Should Be Equal As Integers                             ${dt_action_menu}   1
    ${dt_action_menu}=  Actions Shutdown Digital Twin Visible
    Should Be Equal As Integers                             ${dt_action_menu}   -1

    [Teardown]    Refresh Page

Test 5: Relaunch Digital Twin Device
    [Documentation]     Relaunch "Digital Twin" devices and verify Actions menu options.
    [Tags]      xim_tcxm_21275   xim_tcxm_21229    xiq_4627     xiq_6669    development    xiq    digital_twin    test5

    Navigate to Devices and Confirm Success

    Should Not Be Equal As Strings                          ${DT_SE_SERIAL}     -1
    Relaunch Digital Twin Device                            ${DT_SE_MAC}

    Should Not Be Equal As Strings                          ${DT_FE_SERIAL}     -1
    Relaunch Digital Twin Device                            ${DT_FE_MAC}

    Select Device                                           ${DT_SE_SERIAL}
    Select Device                                           ${DT_FE_SERIAL}
    ${dt_action_menu}=  Actions Relaunch Digital Twin Visible
    Should Be Equal As Integers                             ${dt_action_menu}   1

    ${dt_se_status}=    Wait Until Device Online            device_serial=${DT_SE_SERIAL}   retry_duration=5    retry_count=60
    Should Be Equal As Integers                             ${dt_se_status}     1
    ${dt_fe_status}=    Wait Until Device Online            device_serial=${DT_FE_SERIAL}   retry_duration=5    retry_count=60
    Should Be Equal As Integers                             ${dt_fe_status}     1

    ${dt_se_state}=    Get Device Status                    ${DT_SE_SERIAL}
    Should Be Equal As Strings                              ${dt_se_state}      green
    ${dt_fe_state}=    Get Device Status                    ${DT_FE_SERIAL}
    Should Be Equal As Strings                              ${dt_fe_state}      green

    Select Device                                           ${DT_SE_SERIAL}
    Select Device                                           ${DT_FE_SERIAL}
    ${dt_action_menu}=  Actions Relaunch Digital Twin Visible
    Should Be Equal As Integers                             ${dt_action_menu}   -1
    ${dt_action_menu}=  Actions Shutdown Digital Twin Visible
    Should Be Equal As Integers                             ${dt_action_menu}   1

    [Teardown]    Refresh Page

Test 6: Disable Digital Twin Soft Launch Feature
    [Documentation]     Disables the "Digital Twin" soft-launch feature. (Required for 22R4 & 22R5)
    [Tags]      xim_tcxm_21617   xiq_4627     xiq_6669    development    xiq    digital_twin    test6

    Navigate to Devices and Confirm Success

    ${result}=   Is Digital Twin Option Visible
    Should Be Equal As Integers                             ${result}   1

    ${result}=   XIQ Soft Launch Feature Url                ${DISABLE_DT_FEATURE}
    Should Be Equal As Integers                             ${result}   1

    ${result}=   Is Digital Twin Option Visible
    Should Be Equal As Integers                             ${result}   -1

    [Teardown]    Refresh Page

*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs into XIQ and configures pre-requisites for the test

    Log Into XIQ and Confirm Success  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

    Log To Console  >> THIS IS FUTURE TEST SECTION TO SET DEFAULT DEVICE PASSWORD AND EXPRESS POLICY
    # Change Device Password and Confirm Success      ${DEFAULT_DEVICE_PWD}
    # Create Open Express Policy and Confirm Success  ${POLICY_NAME}  ${SSID_NAME}

    Navigate to Devices and Confirm Success

Tear Down Test and Close Session
    [Documentation]     Cleans up the components created during the test and ends the test

    ${del_result}=   Delete Device                           device_mac=${DT_SE_MAC}
    Should Be Equal As Integers                              ${del_result}      1
    ${del_result}=   Delete Device                           device_mac=${DT_FE_MAC}
    Should Be Equal As Integers                              ${del_result}      1

    Log Out of XIQ and Quit Browser

Shutdown Digital Twin Device
    [Documentation]    Selects the specified device and runs the "Shutdown Digital Twin" action
    [Arguments]    ${device_mac}

    Select Device                                           device_mac=${device_mac}
    Actions Shutdown Digital Twin
    Refresh Devices Page

Relaunch Digital Twin Device
    [Documentation]    Selects the specified device and runs the "Relaunch Digital Twin" action
    [Arguments]    ${device_mac}

    Select Device                                           device_mac=${device_mac}
    Actions Relaunch Digital Twin
    Refresh Devices Page
