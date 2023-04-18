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
Resource        ../../DigitalTwin/Resources/AllResources.robot

Force Tags      testbed_2_node

Variables       TestBeds/${TESTBED}
Variables       Environments/${TOPO}
Variables       Environments/${ENV}

Suite Setup     Log In and Set Up Test
Suite Teardown  Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                     ${test_url}
${XIQ_USER}                    ${tenant_username}
${XIQ_PASSWORD}                ${tenant_password}
${LOCATION}                    ${netelem1.location}

${ENABLE_DT_FEATURE}           ${XIQ_URL}/hm-webapp/?digitalTwin=true#/devices
${DISABLE_DT_FEATURE}          ${XIQ_URL}/hm-webapp/?digitalTwin=false#/devices

${DT_SE_PERSONA}               ${netelem1.digital_twin_persona}
${DT_SE_MAKE}                  ${netelem1.make}
${DT_SE_MODEL}                 ${netelem1.model}
${DT_SE_VERSION}               ${netelem1.digital_twin_version}
${DT_SE_IP_ADDRESS}            ${netelem1.ip}
${DT_SE_IQAGENT}               ${capwap_url}

${DT_FE_PERSONA}               ${netelem2.digital_twin_persona}
${DT_FE_MAKE}                  ${netelem2.make}
${DT_FE_MODEL}                 ${netelem2.model}
${DT_FE_VERSION}               ${netelem2.digital_twin_version}
${DT_FE_IP_ADDRESS}            ${netelem2.ip}
${DT_FE_IQAGENT}               ${capwap_url}

*** Test Cases ***
Test 1: Enable Digital Twin Soft Launch Feature
    [Documentation]     Enables the "Digital Twin" soft-launch feature. (Required for 22R4 & 22R5)
    [Tags]      tcxm_21616   xiq_4627    xiq_6669   development    xiq    digital_twin    test1

    Navigate to Devices and Confirm Success
    Confirm Digital Twin Feature Is Disabled
    Enable Digital Twin Feature                             ${XIQ_URL}
    Confirm Digital Twin Feature Is Disabled

    Enable CoPilot Feature and Confirm Success
    Navigate to Devices and Confirm Success
    Confirm Digital Twin Feature Is Enabled

    [Teardown]    Refresh Page

Test 2: Onboard Digital Twin Switch Engine Device
    [Documentation]     Onboard "Digital Twin" Switch Engine device.
    [Tags]      tcxm_21215    tcxm_21229    xiq_4627     xiq_6669    development    xiq    digital_twin    test2

    Depends On    Test 1

    Navigate to Devices and Confirm Success

    ${ONBOARD_SE_RESULT}=      onboard device quick         ${netelem1}
    Should Be Equal As Strings                              ${ONBOARD_SE_RESULT}     1

    ${dt_se_serial}=           set variable                 ${${netelem1.name}.serial}
    Set Suite Variable                                      ${DT_SE_SERIAL}     ${dt_se_serial}

    Confirm Digital Twin Serial Number                      ${DT_SE_SERIAL}
    Confirm Device Status Icon                              ${DT_SE_SERIAL}     expected_icon=digital_twin
    Select Device                                           device_serial=${DT_SE_SERIAL}
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

    Depends On    Test 1

    Navigate to Devices and Confirm Success

    ${ONBOARD_FE_RESULT}=      onboard device quick         ${netelem2}
    Should Be Equal As Strings                              ${ONBOARD_FE_RESULT}     1

    ${dt_fe_serial}=           set variable                 ${${netelem2.name}.serial}
    Set Suite Variable                                      ${DT_FE_SERIAL}    ${dt_fe_serial}

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

    Depends On    Test 2    Test 3

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

    Depends On    Test 2    Test 3

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

    Delete Device and Confirm Success                       ${DT_SE_SERIAL}
    Delete Device and Confirm Success                       ${DT_FE_SERIAL}
    Log Out of XIQ and Quit Browser
