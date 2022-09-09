#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Dan McCarthy
# Description   : Sanity tests to verify basic Digital Twin functionality for the XIQ 22R6 release.
#               : These test cases require that the CoPilot feature can be enabled.
#               : The 'user' account will need to have either an active CoPilot license
#               :  or use the 30-Day Trial license.
#               : qTest test cases in the CSIT project.
#                 - TCCS-13497: Test 1: Enable the Digital Twin feature
#                 - TCCS-13498: Test 2: Onboard Digital Twin Device
#                 - TCCS-13499: Test 3: Digital Twin Device D360 Overview panel
#                 - TCCS-13500: Test 4: Disable the Digital Twin Feature

*** Settings ***
Resource         ../../DigitalTwin/Resources/AllResources.robot

Force Tags       testbed_none

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${test_url}
${XIQ_USER}                 ${tenant_username}
${XIQ_PASSWORD}             ${tenant_password}

${DT_PERSONA}               SwitchEngine
${DT_MAKE}                  Switch Engine
${DT_MODEL}                 5320-24T-8XE
${DT_VERSION}               32.1.1.6
${DT_POLICY}
${DT_SERIAL}
${DT_MAC}
${DT_IP_ADDRESS}            10.0.2.15
${DT_IQAGENT}               0.5.61

${LOCATION}                 San Jose, building_01, floor_02
${DEFAULT_DEVICE_PWD}       Aerohive123
${POLICY_NAME}              Automation_Policy


*** Test Cases ***
Test 1: Enable Digital Twin Feature
    [Documentation]     Enables the "Digital Twin" feature by enabling CoPilot. (Required for 22R6)
    [Tags]      tccs-13497      development    xiq    digital_twin    sanity    test1

    Navigate to Devices and Confirm Success
    Confirm Digital Twin Feature Is Disabled
    Enable CoPilot Feature and Confirm Success
    Navigate to Devices and Confirm Success
    Confirm Digital Twin Feature Is Enabled

    [Teardown]    Refresh Page

Test 2: Onboard Digital Twin Device
    [Documentation]     Onboard "Digital Twin" device.
    [Tags]      tccs-13498      development    xiq    digital_twin    sanity    test2

    Depends On      Test 1

    Navigate to Devices and Confirm Success

    ${dt_serial}=  Onboard Device DT                        device_type=Digital_Twin        os_persona=${DT_PERSONA}
    ...                                                     device_model=${DT_MODEL}     os_version=${DT_VERSION}
    ...                                                     policy=${DT_POLICY}
    Set Suite Variable                                      ${DT_SERIAL}    ${dt_serial}

    Confirm Digital Twin Serial Number                      ${DT_SERIAL}
    Confirm Device Status Icon                              ${DT_SERIAL}    expected_icon=digital_twin
    Select Device                                           ${DT_SERIAL}
    Confirm Actions Relaunch Digital Twin Option Visible
    Confirm Actions Shutdown Digital Twin Option Hidden
    Confirm Device Serial Online                            ${DT_SERIAL}    retry_duration=5    retry_count=60
    Confirm Device Serial Managed                           ${DT_SERIAL}    retry_duration=5    retry_count=60
    Confirm Device Serial Has Expected Status               ${DT_SERIAL}    green

    ${dt_mac}=   Get Device Details                         ${DT_SERIAL}    MAC
    Set Suite Variable                                      ${DT_MAC}       ${dt_mac}

    Confirm Digital Twin MAC Address                        ${DT_MAC}

    ${dt_iqagent}=   Get Device Details                     ${DT_SERIAL}    IQAGENT
    Set Suite Variable                                      ${DT_IQAGENT}   ${dt_iqagent}

    [Teardown]    Refresh Page

Test 3: Digital Twin Device D360 Overview panel
    [Documentation]     Open D360 view.  Verify the device specific information is displayed.
    [Tags]      tccs-13499      development    xiq    digital_twin    sanity    test3

    Depends On      Test 2

    Navigate to Devices and Confirm Success
    Open Device360 Using MAC And Confirm Success            ${DT_MAC}
    Confirm D360 Digital Twin Status                        connected
    Confirm Device360 Top Bar Information for Digital Twin Device

    [Teardown]    Close Device360 And Refresh Devices Page

Test 4: Disable Digital Twin Feature
    [Documentation]     Disables the "Digital Twin" feature by disabling CoPilot. (Required for 22R6)
    [Tags]      tccs-13500      development    xiq    digital_twin    sanity    test4

    Navigate to Devices and Confirm Success
    Confirm Digital Twin Feature Is Enabled
    Disable CoPilot Feature and Confirm Success

    Navigate to Devices and Confirm Success
    Confirm Digital Twin Feature Is Disabled

    Depends On      Test 2
    Confirm Device Serial Has Expected Status               ${DT_SERIAL}     disconnected
    Select Device                                           ${DT_SERIAL}
    Confirm Actions Button Is Disabled

    [Teardown]    Refresh Page

*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs into XIQ and configures pre-requisites for the test

    Log Into XIQ and Confirm Success  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}
    Disable CoPilot Feature and Confirm Success
    Refresh Page

Tear Down Test and Close Session
    [Documentation]     Cleans up the components created during the test and ends the test

    Delete Device and Confirm Success                       ${DT_SERIAL}
    Log Out of XIQ and Quit Browser

Confirm Device360 Top Bar Information for Digital Twin Device
    [Documentation]     Confirms the topbar of the Device360 view contains correct values for the Digital Twin device.

    # Obtain the data displayed along the top bar in the Device360 > Overview panel.
    &{topbar_info}=  Get Switch Information

    ${topbar_ip}=       Get From Dictionary  ${topbar_info}  ip_address
    ${topbar_mac}=      Get From Dictionary  ${topbar_info}  mac_address
    ${topbar_version}=  Get From Dictionary  ${topbar_info}  software_version
    ${topbar_model}=    Get From Dictionary  ${topbar_info}  device_model
    ${topbar_serial}=   Get From Dictionary  ${topbar_info}  serial_number
    ${topbar_make}=     Get From Dictionary  ${topbar_info}  device_make
    ${topbar_iqagent}=  get from dictionary  ${topbar_info}  IQAgent_version

    Should Be Equal                 ${topbar_ip}        ${DT_IP_ADDRESS}
    Should Be Equal                 ${topbar_mac}       ${DT_MAC}
    Should Be Equal                 ${topbar_version}   ${DT_VERSION}
    Should Contain                  ${topbar_model}     ${DT_MODEL}
    Should Be Equal                 ${topbar_serial}    ${DT_SERIAL}
    Should Be Equal                 ${topbar_make}      ${DT_MAKE}
    Should Be Equal                 ${topbar_iqagent}   ${DT_IQAGENT}
