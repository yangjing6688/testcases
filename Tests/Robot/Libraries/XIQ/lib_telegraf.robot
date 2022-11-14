#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains keywords specific to telegraf functionality.
#

*** Variables ***
${ALERT_URI}            /alerts

*** Settings ***
Library         String
Library         extauto.common.Utils
Library         extauto.common.Xapi

Resource   ./lib_voss.robot

*** Keywords ***
Trigger Interface Up Event for VOSS and Confirm Success
    [Documentation]    Trigger interface up event on specific port for VOSS and Confirm Success
    [Tags]             voss
    [Arguments]        ${ip}  ${port}  ${user}  ${pwd}  ${test_port}    ${keyword}
    #Enable specific port on device
    Enable Port for Test Device     ${ip}  ${port}  ${user}  ${pwd}  ${test_port}

    #Check the interface up event by XAPI
    XAPI Verify Interface Name By Alert Type     INTERFACE_ADMIN_UP    ${test_port}    ${keyword}

Trigger Interface Down Event for VOSS and Confirm Success
    [Documentation]    Trigger interface down event on specific port for VOSS and Confirm Success
    [Tags]             voss
    [Arguments]        ${ip}  ${port}  ${user}  ${pwd}  ${test_port}    ${keyword}
    #Disable specific port on device
    Disable Port for Test Device     ${ip}  ${port}  ${user}  ${pwd}  ${test_port}

    #Check the interface down event by XAPI
    XAPI Verify Interface Name By Alert Type     INTERFACE_ADMIN_DOWN    ${test_port}    ${keyword}

XAPI Verify Interface Name By Alert Type
    [Documentation]    Verify interface name by alert type on specific port
    [Tags]             alerts
    [Arguments]        ${alert_type}    ${test_port}    ${keyword}
    #Check the interface name by XAPI
    #Event should be raised at least in 5 minutes
    ${end_time}=      get_time_in_milliseconds  diff=-120000    #2 minutes later
    ${start_time}=      get_time_in_milliseconds    diff=60000     #1 minutes ago
    sleep  120    seconds
    #Fetch the specific port in Alerts
    ${result_json}=  rest api get  ${ALERT_URI}?page=1&limit=10&startTime=${start_time}&endTime=${end_time}&alertType=${alert_type}&keyword=${keyword}
    ${result_json_data}=  get json values  ${result_json}  key=data
    ${result_json_data_tags0}=    get_json_value_from_list    ${result_json_data}    tags  list_index=0
    ${result_json_data_tags0_interface_name}=  get json values  ${result_json_data_tags0}  key=interface_name
    ${result_json_data_tags0_interface_name}=   Replace String    ${result_json_data_tags0_interface_name}  :   /
    Should Contain  ${result_json_data_tags0_interface_name}  ${test_port}
