#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Bienvinido Onia
# Description   : Test Suite for testing the IP Search in Device Manage page
# Topology      : One AP


*** Settings ***
Resource         ../Resources/AllResources.robot

Force Tags       testbed_none

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session

*** Variables ***
${XIQ_URL}            ${test_url}
${XIQ_USER}           ${tenant_username}
${XIQ_PASSWORD}       ${tenant_password}

*** Test Cases ***
TCXM-18675: Basic IP Address Search
    [Documentation]     Confirms the device IP Search
    [Tags]              tcxm_18675   development

    ${ip_list_result}=      Get Device Data Field Value     ${device.model}      ipAddress
    ${search-result}=       Perform Search on Devices Table    ${ip_list_result[0]}
    Should Be Equal As Integers             ${search-result}               1
    Clear Search On Devices Table

*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    ${device}=      Create Dictionary
    ...     name=simulated_dut03
    ...     model=AP460C
    ...     simulated_count=1
    ...     onboard_device_type=Simulated
    ...     location=auto_location_01, Santa Clara, building_02, floor_04

    set suite variable    ${device}
    Login User      ${XIQ_USER}  ${XIQ_PASSWORD}  url=${XIQ_URL}
    Onboard Test Devices

Tear Down Test and Close Session
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Clean Up Test Device and Confirm Success    ${device.serial}
    Logout User
    Quit Browser

Onboard Test Devices
    [Documentation]     Onboards the test devices

    ${ONBOARD_RESULT}=    onboard device quick       ${device}
    Should Be Equal As Strings          ${ONBOARD_RESULT}       1

Clean Up Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Delete Device and Confirm Success  ${serial}