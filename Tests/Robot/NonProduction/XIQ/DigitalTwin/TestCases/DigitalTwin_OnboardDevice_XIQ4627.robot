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
${DT_SE_SERIAL}
${DT_SE_MAC}
${DT_FE_PERSONA}            FabricEngine
${DT_FE_MODEL}              5420F-24S-4XE
${DT_FE_VERSION}            8.7.0.0
${DT_FE_POLICY}
${DT_FE_SERIAL}
${DT_FE_MAC}

${LOCATION}                 San Jose, building_01, floor_02
${DEFAULT_DEVICE_PWD}       Aerohive123
${POLICY_NAME}              Automation_Policy


*** Test Cases ***
Test 1: Enable Digital Twin Soft Launch Feature
    [Documentation]     Enables the "Digital Twin" soft-launch feature. (Required for 22R4 & 22R5)
    [Tags]      tcxm_21616   xiq_4627    xiq_6669   development    xiq    digital_twin    test1

    Navigate to Devices and Confirm Success
    Confirm Digital Twin Feature Is Disabled
    Enable Digital Twin Feature                             ${XIQ_URL}
    Confirm Digital Twin Feature Is Enabled

    [Teardown]    Refresh Page

Test 2: Onboard Digital Twin Switch Engine Device
    [Documentation]     Onboard "Digital Twin" Switch Engine device.
    [Tags]      tcxm_21215    tcxm_21229    xiq_4627     xiq_6669    development    xiq    digital_twin    test2

    Navigate to Devices and Confirm Success

    ${dt_se_serial}=  Onboard Device DT                     device_type=Digital_Twin        os_persona=${DT_SE_PERSONA}
    ...                                                     device_model=${DT_SE_MODEL}     os_version=${DT_SE_VERSION}
    ...                                                     policy=${DT_SE_POLICY}
    Set Suite Variable                                      ${DT_SE_SERIAL}     ${dt_se_serial}

    Confirm Digital Twin Serial Number                      ${DT_SE_SERIAL}
    Confirm Device Status Icon                              ${DT_SE_SERIAL}     expected_icon=digital_twin
    Select Device                                           ${DT_SE_SERIAL}
    Confirm Actions Relaunch Digital Twin Option Visible
    Confirm Actions Shutdown Digital Twin Option Hidden
    Confirm Device Serial Online                            ${DT_SE_SERIAL}     retry_duration=10    retry_count=60
    Confirm Device Serial Managed                           ${DT_SE_SERIAL}     retry_duration=10    retry_count=60
    Confirm Device Serial Has Expected Status               ${DT_SE_SERIAL}     green

    ${dt_se_mac}=   Get Device Details                      ${DT_SE_SERIAL}     MAC
    Set Suite Variable                                      ${DT_SE_MAC}        ${dt_se_mac}

    Confirm Digital Twin MAC Address                        ${DT_SE_MAC}

    [Teardown]    Refresh Page

Test 3: Onboard Digital Twin Fabric Engine Device
    [Documentation]     Onboard "Digital Twin" Fabric Engine device.
    [Tags]      tcxm_21216   tcxm_21229    xiq_4627   xiq_6669    development    xiq    digital_twin    test3

    Navigate to Devices and Confirm Success

    ${dt_fe_serial}=  Onboard Device DT                     device_type=digital_twin        os_persona=${DT_FE_PERSONA}
    ...                                                     device_model=${DT_FE_MODEL}     os_version=${DT_FE_VERSION}
    ...                                                     policy=${DT_FE_POLICY}
    Set Suite Variable                                      ${DT_FE_SERIAL}     ${dt_fe_serial}

    Confirm Digital Twin Serial Number                      ${DT_FE_SERIAL}
    Confirm Device Status Icon                              ${DT_FE_SERIAL}     expected_icon=digital_twin
    Select Device Row                                       ${DT_FE_SERIAL}
    Confirm Actions Relaunch Digital Twin Option Visible
    Confirm Actions Shutdown Digital Twin Option Hidden
    Confirm Device Serial Online                            ${DT_FE_SERIAL}     retry_duration=10    retry_count=60
    Confirm Device Serial Managed                           ${DT_FE_SERIAL}     retry_duration=10    retry_count=60
    Confirm Device Serial Has Expected Status               ${DT_FE_SERIAL}     green

    ${dt_fe_mac}=   Get Device Details                      ${DT_FE_SERIAL}     MAC
    Set Suite Variable                                      ${DT_FE_MAC}        ${dt_fe_mac}

    Confirm Digital Twin MAC Address                        ${DT_FE_MAC}

    [Teardown]    Refresh Page

Test 4: Shutdown Digital Twin Device
    [Documentation]     Shutdown "Digital Twin" devices and verify Actions menu options.
    [Tags]      tcxm_21230   tcxm_21229    xiq_4627   xiq_6669    development    xiq    digital_twin    test4

    Navigate to Devices and Confirm Success
    Select Device Rows                                      device_serials=${DT_SE_SERIAL},${DT_FE_SERIAL}
    Confirm Actions Relaunch Digital Twin Option Hidden
    Confirm Actions Shutdown Digital Twin Option Visible
    Shutdown Digital Twin Device
    Confirm Device Serial Offline                           ${DT_SE_SERIAL}     retry_duration=10    retry_count=60
    Confirm Device Serial Offline                           ${DT_FE_SERIAL}     retry_duration=10    retry_count=60
    Confirm Device Serial Has Expected Status               ${DT_SE_SERIAL}     disconnected
    Confirm Device Serial Has Expected Status               ${DT_FE_SERIAL}     disconnected
    Select Device Rows                                      device_serials=${DT_SE_SERIAL},${DT_FE_SERIAL}
    Confirm Actions Relaunch Digital Twin Option Visible
    Confirm Actions Shutdown Digital Twin Option Hidden

    [Teardown]    Refresh Page

Test 5: Relaunch Digital Twin Device
    [Documentation]     Relaunch "Digital Twin" devices and verify Actions menu options.
    [Tags]      tcxm_21275   tcxm_21229    xiq_4627     xiq_6669    development    xiq    digital_twin    test5

    Navigate to Devices and Confirm Success
    Select Device Rows                                      device_serials=${DT_SE_SERIAL},${DT_FE_SERIAL}
    Confirm Actions Relaunch Digital Twin Option Visible
    Confirm Actions Shutdown Digital Twin Option Hidden
    Relaunch Digital Twin Device
    Select Device Rows                                      device_serials=${DT_SE_SERIAL},${DT_FE_SERIAL}
    Confirm Actions Relaunch Digital Twin Option Visible
    Confirm Device Serial Online                            ${DT_SE_SERIAL}     retry_duration=10    retry_count=60
    Confirm Device Serial Online                            ${DT_FE_SERIAL}     retry_duration=10    retry_count=60
    Confirm Device Serial Has Expected Status               ${DT_SE_SERIAL}     green
    Confirm Device Serial Has Expected Status               ${DT_FE_SERIAL}     green
    Select Device Rows                                      device_serials=${DT_SE_SERIAL},${DT_FE_SERIAL}
    Confirm Actions Relaunch Digital Twin Option Hidden
    Confirm Actions Shutdown Digital Twin Option Visible

    [Teardown]    Refresh Page

Test 6: Disable Digital Twin Soft Launch Feature
    [Documentation]     Disables the "Digital Twin" soft-launch feature. (Required for 22R4 & 22R5)
    [Tags]      tcxm_21617   xiq_4627     xiq_6669    development    xiq    digital_twin    test6

    Navigate to Devices and Confirm Success
    Confirm Digital Twin Feature Is Enabled
    Disable Digital Twin Feature                            ${XIQ_URL}
    Confirm Digital Twin Feature Is Disabled

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

    Delete Device and Confirm Success                       ${DT_SE_SERIAL}
    Delete Device and Confirm Success                       ${DT_FE_SERIAL}
    Log Out of XIQ and Quit Browser
