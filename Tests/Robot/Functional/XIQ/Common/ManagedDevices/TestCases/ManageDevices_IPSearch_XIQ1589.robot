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

Force Tags       testbed_not_required

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session

*** Variables ***
${XIQ_URL}            ${test_url}
${XIQ_USER}           ${tenant_username}
${XIQ_PASSWORD}       ${tenant_password}

${LOCATION}             auto_location_milpitas, San_Jose, building_1, floor_1


*** Test Cases ***
TCXM-18675: Basic IP Address Search
    [Documentation]     Confirms the device IP Search
    [Tags]              xim_tc_18675   development

    ${ip_list_result}=      Get Device Data Field Value     AP460C      ipAddress
    ${search-result}=       Perform Search on Devices Table    ${ip_list_result[0]}
    Should Be Equal As Integers             ${search-result}               1
    Clear Search On Devices Table

*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Login User      ${XIQ_USER}  ${XIQ_PASSWORD}  url=${XIQ_URL}
    Onboard Test Devices

Tear Down Test and Close Session
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Clean Up Test Device and Confirm Success    ${SIM_SERIAL}
    Logout User
    Quit Browser

Onboard Test Devices
    [Documentation]     Onboards the test devices

    ${SIM_SERIAL}=    Onboard Simulated Device        AP460C      location=${LOCATION}
    Set Suite Variable          ${SIM_SERIAL}

Clean Up Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Delete Device and Confirm Success  ${serial}