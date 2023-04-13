#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Dan McCarthy
# Description   : Verifies that a Digital Twin device can be shutdown and relaunched from the Device360 view.
#                 For 22R5 - the "Digital Twin" feature is controlled by a "soft launch" url
#                 qTest Test Cases in the XIQ Mainline project.
#                   TCXM-21215 - "Onboard" Digital Twin device
#                   TCXM-21229 - Manage > Devices: "Actions" menu for Digital Twin device
#                   TCXM-18132 - Digital Twin - D360 view
#                   TCXM-21279 - D360 view: "Shutdown" Digital Twin device
#                   TCXM-21280 - D360 view: "Relaunch" Digital Twin device
#                   TCXM-20308 - Digital Twin - Delete device
#                   TCXM-21616 - Digital Twin - Enable the feature using the "Soft Launch" URL
#                   TCXM-21617 - Digital Twin - Disable the feature using the "Soft Launch" URL

*** Settings ***
Resource         ../../DigitalTwin/Resources/AllResources.robot

Force Tags       testbed_1_node

Variables        TestBeds/${TESTBED}
Variables        Environments/${TOPO}
Variables        Environments/${ENV}

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${test_url}
${XIQ_USER}                 ${tenant_username}
${XIQ_PASSWORD}             ${tenant_password}

${ENABLE_DT_FEATURE}        ${XIQ_URL}/hm-webapp/?digitalTwin=true#/devices
${DISABLE_DT_FEATURE}       ${XIQ_URL}/hm-webapp/?digitalTwin=false#/devices

${DT_PERSONA}               ${netelem1.digital_twin_persona}
${DT_MAKE}                  ${netelem1.make}
${DT_MODEL}                 ${netelem1.model}
${DT_VERSION}               ${netelem1.digital_twin_version}
${DT_IP_ADDRESS}            ${netelem1.ip}
${LOCATION}                 ${netelem1.location}
${DT_IQAGENT}               ${capwap_url}


*** Test Cases ***
Test 1: Enable Digital Twin Soft Launch Feature
    [Documentation]     Enables the "Digital Twin" soft-launch feature. (Required for 22R4 & 22R5)
    [Tags]      tcxm_21616      xiq_6669    development    xiq    digital_twin    test1

    Navigate to Devices and Confirm Success
    Confirm Digital Twin Feature Is Disabled
    Enable Digital Twin Feature                             ${XIQ_URL}
    Confirm Digital Twin Feature Is Disabled

    Enable CoPilot Feature and Confirm Success
    Navigate to Devices and Confirm Success
    Confirm Digital Twin Feature Is Enabled

    [Teardown]    Refresh Page

Test 2: Onboard Digital Twin Device
    [Documentation]     Onboard "Digital Twin" device.
    [Tags]      tcxm_18132    xiq_6669    development    xiq    digital_twin    test2

    Depends On    Test 1

    Navigate to Devices and Confirm Success

    ${ONBOARD_RESULT}=      onboard device quick                 ${netelem1}
    Should Be Equal As Strings                              ${ONBOARD_RESULT}     1

    ${dt_serial}=           set variable                    ${${netelem1.name}.serial}
    Set Suite Variable                                      ${DT_SERIAL}    ${dt_serial}

    Confirm Digital Twin Serial Number                      ${DT_SERIAL}
    Confirm Device Status Icon                              ${DT_SERIAL}    expected_icon=digital_twin
    Select Device                                           device_serial=${DT_SERIAL}
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
    [Tags]      tcxm-18132        xiq_6669    development    xiq    digital_twin    test3

    Depends On    Test 2

    Navigate to Devices and Confirm Success
    Open Device360 Using MAC And Confirm Success            ${DT_MAC}
    Confirm D360 Digital Twin Status                        connected
    Confirm Device360 Top Bar Information for Digital Twin Device

    [Teardown]    Refresh Page

Test 4: D360 Shutdown Digital Twin Device
    [Documentation]     Open D360 view.  Shutdown "Digital Twin" device and verify results.
    [Tags]      tcxm_21279      xiq_6669    development    xiq    digital_twin    test4

    Depends On    Test 2

    Navigate to Devices and Confirm Success
    Open Device360 Using MAC And Confirm Success            ${DT_MAC}
    Confirm D360 Digital Twin Status                        connected
    Confirm D360 Shutdown Digital Twin Option Visible
    Device360 Shutdown Digital Twin Device
    Device360 Wait Until Device Offline                     retry_duration=10       retry_count=60
    Confirm D360 Digital Twin Status                        disconnected
    Confirm D360 Relaunch Digital Twin Option Visible

    [Teardown]    Close Device360 And Refresh Devices Page

Test 5: D360 Relaunch Digital Twin Device
    [Documentation]     Open D360 view. Relaunch "Digital Twin" device and verify results.
    [Tags]      tcxm_21280      xiq_6669    development    xiq    digital_twin    test5

    Depends On    Test 2

    Navigate to Devices and Confirm Success
    Open Device360 Using MAC And Confirm Success            ${DT_MAC}
    Confirm D360 Digital Twin Status                        disconnected
    Confirm D360 Relaunch Digital Twin Option Visible
    Device360 Relaunch Digital Twin Device
    Device360 Wait Until Device Online                      retry_duration=10       retry_count=60
    Confirm D360 Digital Twin Status                        connected
    Confirm D360 Shutdown Digital Twin Option Visible

    [Teardown]    Close Device360 And Refresh Devices Page

Test 6: Disable Digital Twin Soft Launch Feature
    [Documentation]     Disables the "Digital Twin" soft-launch feature. (Required for 22R4 & 22R5)
    [Tags]      tcxm_21617     xiq_6669    development    xiq    digital_twin    test6

    Depends On    Test 1

    Navigate to Devices and Confirm Success
    Confirm Digital Twin Feature Is Enabled
    Disable Digital Twin Feature                            ${XIQ_URL}
    Confirm Digital Twin Feature Is Enabled

    Disable CoPilot Feature and Confirm Success
    Navigate to Devices and Confirm Success
    Confirm Digital Twin Feature Is Disabled

    [Teardown]    Refresh Page

*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs into XIQ and configures pre-requisites for the test

    Log Into XIQ and Confirm Success  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}
    Disable CoPilot Feature and Confirm Success
    Navigate to Devices and Confirm Success

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
    ${topbar_iqagent}=  get from dictionary  ${topbar_info}  IQAgent_version

    Should Be Equal                 ${topbar_ip}        ${DT_IP_ADDRESS}
    Should Be Equal                 ${topbar_mac}       ${DT_MAC}
    Should Be Equal                 ${topbar_version}   ${DT_VERSION}
    Should Contain                  ${topbar_model}     ${DT_MODEL}
    Should Be Equal                 ${topbar_serial}    ${DT_SERIAL}
    Should Be Equal                 ${topbar_iqagent}   ${DT_IQAGENT}
