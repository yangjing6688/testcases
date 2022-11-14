# Author        : Cairong Chen
# Date          : 10 12 2022
# Description   : ESP Alert for Telegraf Interface State Change Event
#

*** Settings ***
Documentation  robot -v ENV:environment.local.chrome.yaml -v TOPO:topo.test.cp1r3.telegraf.yaml -v TESTBED:HANGZHOU/Dev/xiq_telegraf_voss_1node1.yaml  InterfaceStateChange_AdminDownUp_XIQ8298.robot

Library      extauto.xiq.flows.manage.EspAlert
Library      ExtremeAutomation/Keywords/NetworkElementKeywords/GeneratedKeywords/NetworkElementPortGenKeywords.py

Resource    ../../Resources/AllResources.robot

Force Tags            testbed_1_node

Suite Setup    Test Suite Set Up
Suite Teardown   Test Suite Teardown

*** Test Cases ***
TCXM-22882: Verify Interface admin down Alert
    [Documentation]         Raise interface admin down Alert
    [Tags]                  tcxm_22882  development
    Trigger Interface Down Event for VOSS and Confirm Success     ${netelem1.ip}   ${netelem1.port}
    ...                                                         ${netelem1.username}    ${netelem1.password}    ${netelem1.test_port}   ${netelem1.serial}

TCXM-22883: Verify Interface admin up Alert
    [Documentation]         Raise interface admin up Alert
    [Tags]                  tcxm_22883  development
    Trigger Interface Up Event for VOSS and Confirm Success     ${netelem1.ip}   ${netelem1.port}
    ...                                                         ${netelem1.username}    ${netelem1.password}    ${netelem1.test_port}   ${netelem1.serial}

*** Keywords ***
Test Suite Set Up
     [Documentation]    Onboard device to XIQ
     # Enable specific port on device
     Enable Port for Test Device     ${netelem1.ip}   ${netelem1.port}  ${netelem1.username}    ${netelem1.password}    ${netelem1.test_port}

     # Add device serial number into XIQ
     lib_xiq.Log Into XIQ and Confirm Success   ${tenant_username}  ${tenant_password}  ${test_url}
     ${device_json_str}=       catenate                {"onboard_device_type":"${netelem1.onboard_device_type}", "serial":"${netelem1.serial}", "make":"${netelem1.make}", "location":"${netelem1.location}"}
     ${device_json}=           get_json_from_string    ${device_json_str}
     ${onboard_result}=     onboard_device_quick    ${device_json}
     should be equal as integers         ${onboard_result}  1

     # Connect device into XIQ
     Confirm iqagent for VOSS Switch is Connected to XIQ    ${netelem1.ip}   ${netelem1.port}
     ...                                                    ${netelem1.username}    ${netelem1.password}     ${sw_capwap_url}  ${netelem1.connection_method}

     # Set the access token
     Pre Condition-User-Login

Confirm iqagent for VOSS Switch is Connected to XIQ
    [Documentation]     Confirms the iqagent for the VOSS switch is connected to XIQ
    [Tags]              voss
    [Arguments]         ${ip}  ${port}  ${user}  ${pwd}  ${iqagent}  ${connection_method}

    ${spawn}=               Open Spawn  ${ip}  ${port}  ${user}  ${pwd}  VOSS  ${connection_method}
    ${conf_status_result}=    Configure Device To Connect To Cloud        VOSS    ${iqagent}   ${spawn}
    Should Be Equal As Strings       ${conf_status_result}    1

    ${iqagent_results}=     Send                ${spawn}         show application iqagent
    Log To Console          Command results are ${iqagent_results}
    Should Contain          ${iqagent_results}      connected

    [Teardown]              Close Spawn  ${spawn}

Pre Condition-User-Login
    [Documentation]  XAPI User login successful
    ${ACCESS_TOKEN}=        generate_access_token    ${tenant_username}      ${tenant_password}      login
    log to console    ${ACCESS_TOKEN}
    set global variable     ${ACCESS_TOKEN}

Test Suite Teardown
    [Documentation]  delete device on XIQ
    Navigate and Remove Device by Serial From XIQ   ${netelem1.serial}