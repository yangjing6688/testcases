#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Verifies the "Assign Location" functionality from the Actions button on the Manage> Devices page
#                 works as expected, as well as the hyper link in the table.
#                 This is qTest test cases TC-8192 and TC-6986 in the CSIT project.
#                     TC-8192 - Action_Assign_location (actions menu)
#                     TC-6986 - Manage device location hyperlink (hyperlink within table)

*** Settings ***
Library          common/Cli.py
Library          xiq/flows/manage/Location.py

Resource         ../../ManageDevices/Resources/AllResources.robot

Force Tags       testbed_1_node

Suite Setup      Log In and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}                  ${xiq.test_url}
${XIQ_USER}                 ${xiq.tenant_username}
${XIQ_PASSWORD}             ${xiq.tenant_password}
${XIQ_CAPWAP_URL}           ${xiq.capwap_url}
${IQAGENT}                  ${xiq.sw_connection_host}

${DUT_SERIAL}               ${ap1.serial}
${DUT_CONSOLE_IP}           ${ap1.ip}
${DUT_CONSOLE_PORT}         ${ap1.port}
${DUT_USERNAME}             ${ap1.username}
${DUT_PASSWORD}             ${ap1.password}
${DUT_PLATFORM}             ${ap1.platform}
${DUT_MAKE}                 ${ap1.make}

${LOCATION}                 San Jose, building_01, floor_02
${DEFAULT_DEVICE_PWD}       Aerohive123
${POLICY_NAME}              Automation_Policy
${SSID_NAME}                Auto_SSID
${LOCATION_1}               auto_location_01, Santa Clara, building_02, floor_04
${LOCATION_1_DISPLAY}       auto_location_01 >> Santa Clara >> building_02 >> floor_04
${LOCATION_2}               auto_location_01, San Jose, building_01, floor_01
${LOCATION_2_DISPLAY}       auto_location_01 >> San Jose >> building_01 >> floor_01


*** Test Cases ***
Test 1: Assign Location Using Actions Menu
    [Documentation]     Assigns a location to the device using the Actions menu
    [Tags]      csit_tc_8192   aiq_1332    development    xiq    manage_devices    location    test1

    ${result}=  Assign Location With Device Actions     ${DUT_SERIAL}   ${LOCATION_1}
    Should Be Equal As Integers                         ${result}   1

    ${update_result}=  Update Network Policy To AP      policy_name=${POLICY_NAME}  ap_serial=${DUT_SERIAL}
    Should Be Equal As Integers                         ${update_result}  1

    ${value}=  Get Device Details                       ${DUT_SERIAL}   LOCATION
    Should Contain                                      ${value}   ${LOCATION_1_DISPLAY}

Test 2: Assign Location Using Table Hyperlink
    [Documentation]     Assigns a location to the device using the hyperlink in the table
    [Tags]      csit_tc_6986   aiq_1332    development    xiq    manage_devices    location    test1

    ${result}=  Assign Location With Hyperlink      ${DUT_SERIAL}  ${LOCATION_2}
    Should Be Equal As Integers                     ${result}   1

    ${update_result}=  Update Network Policy To AP  policy_name=${POLICY_NAME}  ap_serial=${DUT_SERIAL}
    Should Be Equal As Integers                     ${update_result}  1

    ${value}=   Get Device Details                  ${DUT_SERIAL}   LOCATION
    Should Contain                                  ${value}   ${LOCATION_2_DISPLAY}


*** Keywords ***
Log In and Set Up Test
    [Documentation]     Logs into XIQ and configures pre-requisites for the test

    Log Into XIQ and Confirm Success  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}

    Change Device Password and Confirm Success      ${DEFAULT_DEVICE_PWD}
    Create Open Express Policy and Confirm Success  ${POLICY_NAME}  ${SSID_NAME}

    # Check if the device is already present - if not, configure and onboard it
    Navigate to Devices and Confirm Success
    ${search_result}=  Search Device Serial   ${DUT_SERIAL}
    Run Keyword If  '${search_result}' != '1' and '${DUT_PLATFORM}' == 'aerohive'         Set Up Aerohive AP Test
    Run Keyword If  '${search_result}' != '1' and '${DUT_PLATFORM}' == 'aerohive-switch'  Set Up Aerohive Switch Test
    Run Keyword If  '${search_result}' != '1' and '${DUT_PLATFORM}' == 'voss'             Set Up VOSS Test

    Run Keyword If  '${search_result}' != '1'    Set Suite Variable  ${ONBOARDED_DUT}   'True'
    ...  ELSE        Set Suite Variable  ${ONBOARDED_DUT}   'False'

    Wait Until Device Online  ${DUT_SERIAL}

Tear Down Test and Close Session
    [Documentation]     Cleans up the components created during the test and ends the test

    Navigate to Devices and Confirm Success

    Run Keyword If  ${ONBOARDED_DUT} == 'True'  Delete Device and Confirm Success  ${DUT_SERIAL}
    Run Keyword If  ${ONBOARDED_DUT} == 'True'  Delete Policy and Confirm Success  ${POLICY_NAME}
    Run Keyword If  ${ONBOARDED_DUT} == 'True'  Delete SSID and Confirm Success    ${SSID_NAME}

    Log Out of XIQ and Quit Browser

Set Up Aerohive Switch Test
    [Documentation]     Configures and onboards the Aerohive Switch test device

    Onboard Device                         ${DUT_SERIAL}  ${DUT_MAKE}  location=${LOCATION}
    Configure iqagent for Aerohive Switch  ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}
    ...                                    ${DUT_PASSWORD}  ${IQAGENT}
    Confirm Device Serial Present          ${DUT_SERIAL}

Set Up Aerohive AP Test
    [Documentation]     Configures and onboards the Aerohive AP test device

    Onboard Device                 ${DUT_SERIAL}  ${DUT_MAKE}  location=${LOCATION}
    Configure CAPWAP               ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}
    ...                            ${DUT_PASSWORD}  ${DUT_PLATFORM}  ${XIQ_CAPWAP_URL}
    Confirm Device Serial Present  ${DUT_SERIAL}

Set Up VOSS Test
    [Documentation]     Configures and onboards the VOSS test device

    Onboard VOSS Device                    ${DUT_SERIAL}  loc_name=${LOCATION}
    Reset VOSS Switch to Factory Defaults  ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}
    Configure iqagent for VOSS Switch      ${DUT_CONSOLE_IP}  ${DUT_CONSOLE_PORT}  ${DUT_USERNAME}  ${DUT_PASSWORD}  ${IQAGENT}
    Confirm Device Serial Present          ${DUT_SERIAL}

Configure CAPWAP
    [Documentation]     Configures the CAPWAP client
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${platform}  ${capwap_server}

    ${spawn}=           Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  ${platform}

    Send                ${spawn}   capwap client server name ${capwap_server}
    Send                ${spawn}   capwap client default-server-name ${capwap_server}
    Send                ${spawn}   capwap client server backup name ${capwap_server}
    Send                ${spawn}   no capwap client enable
    Send                ${spawn}   capwap client enable
    Send                ${spawn}   save config

    Close Spawn         ${spawn}

Configure iqagent for Aerohive Switch
    [Documentation]     Configures the iqagent for the Aerohive switch
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${iqagent}

    ${spawn}=               Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  aerohive-switch

    ${conf_results}=        Send Commands  ${spawn}
    ...  enable, no hivemanager address, hivemanager address ${iqagent}, application stop hiveagent, application start hiveagent, exit
    Log To Console          Command results are ${conf_results}

    [Teardown]              Close Spawn  ${spawn}
