#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : John Borges
# Description   : Test Suite for testing the device utilities menu
# Topology      :
# 1 AP(Any AP), 1 Switch(Any non EXOS/VOSS Switch) and 1 Router(Any Router)
# No connections to each other necessary


*** Settings ***
Library          common/TestFlow.py
Library          common/Cli.py
Library          xiq/flows/common/DeviceCommon.py
Library          xiq/flows/manage/DevicesUtilities.py

Resource         ../../ManageDevices/Resources/AllResources.robot

Force Tags       testbed_3_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}            ${xiq.test_url}
${XIQ_USER}           ${xiq.tenant_username}
${XIQ_PASSWORD}       ${xiq.tenant_password}
${XIQ_CAPWAP_URL}     ${xiq.capwap_url}
${IQAGENT}            ${xiq.sw_connection_host}

${AP_SERIAL}          ${ap1.serial}
${AP_MAKE}            ${ap1.make}
${AP_LOCATION}        ${ap1.location}
${AP_CONSOLE_IP}      ${ap1.console_ip}
${AP_CONSOLE_PORT}    ${ap1.console_port}
${AP_USERNAME}        ${ap1.username}
${AP_PASSWORD}        ${ap1.password}
${AP_PLATFORM}        ${ap1.platform}

${SW_SERIAL}          ${aerohive_sw1.serial}
${SW_MAKE}            ${aerohive_sw1.make}
${SW_LOCATION}        ${aerohive_sw1.location}
${SW_CONSOLE_IP}      ${aerohive_sw1.console_ip}
${SW_CONSOLE_PORT}    ${aerohive_sw1.console_port}
${SW_USERNAME}        ${aerohive_sw1.username}
${SW_PASSWORD}        ${aerohive_sw1.password}
${SW_PLATFORM}        ${aerohive_sw1.platform}

${RT_SERIAL}          ${router1.serial}
${RT_MAKE}            ${router1.make}
${RT_LOCATION}        ${router1.location}
${RT_CONSOLE_IP}      ${router1.console_ip}
${RT_CONSOLE_PORT}    ${router1.console_port}
${RT_USERNAME}        ${router1.username}
${RT_PASSWORD}        ${router1.password}
${RT_PLATFORM}        ${router1.platform}


*** Test Cases ***
TCXM-16933: Confirm Client Information Tool Is Available Only For A Single AP or Router
    [Documentation]     Confirms the Client Information menu item is available for only a single selected AP or Router and opens/closes the correct dialog
    [Tags]              tcxm_16933   development

    # Client Information Tool is available for a single AP
    Select Device       ${AP_SERIAL}
    ${nav_result}=      Navigate To Device Client Information
    Should Be Equal As Integers  ${nav_result}  1
    ${load_result}=     Verify Device Tool Loading Is Open
    Should Be Equal As Integers  ${nav_result}  1
    ${verify_result}=   Wait Until Device Tool Client Information Is Open
    Should Be Equal As Integers  ${verify_result}  1
    ${close_result}=    Close Device Tool Client Information
    Should Be Equal As Integers  ${close_result}  1

    # Client Information Tool is NOT available for multiple devices
    Select Devices      ${AP_SERIAL}   ${RT_SERIAL}
    ${nav_result}=      Navigate To Device Client Information
    Should Be Equal As Integers  ${nav_result}  -1

    Refresh Devices Page

    # Client Information Tool is NOT available for a single switch
    Select Device       ${SW_SERIAL}
    ${nav_result}=      Navigate To Device Client Information
    Should Be Equal As Integers  ${nav_result}  -1

    Refresh Devices Page

    # Client Information Tool is available for a single router
    Select Device       ${RT_SERIAL}
    ${nav_result}=      Navigate To Device Client Information
    Should Be Equal As Integers  ${nav_result}  1
    ${close_result}=    Close Device Tool Client Information
    Should Be Equal As Integers  ${close_result}  1

TCXM-16934: Confirm Get Tech Data Tool Is Available For Any Number Of Devices
    [Documentation]     Confirms the Get Tech Data menu item is available for any number of selected devices and opens/closes the correct dialog
    [Tags]              tcxm_16934   development

    Refresh Devices Page

    # Get Tech Data Tool is available for a single AP
    Select Device       ${AP_SERIAL}
    ${nav_result}=      Navigate To Device Get Tech Data
    Should Be Equal As Integers  ${nav_result}  1
    ${verify_result}=   Verify Confirm Message Dialog Is Open
    Should Be Equal As Integers  ${verify_result}  1
    ${reject_result}=   Reject Device Tool Get Tech Data
    Should Be Equal As Integers  ${reject_result}  1

    # Get Tech Data Tool is ALSO available for multiple devices
    Select Devices      ${AP_SERIAL}   ${SW_SERIAL}
    ${nav2_result}=     Navigate To Device Get Tech Data
    Should Be Equal As Integers  ${nav2_result}  1
    ${ver2_result}=     Verify Confirm Message Dialog Is Open
    Should Be Equal As Integers  ${ver2_result}  1
    ${accept_result}=   Accept Device Tool Get Tech Data
    Should Be Equal As Integers  ${accept_result}  1
    ${load_result}=     Verify Device Tool Loading Is Open
    Should Be Equal As Integers  ${load_result}  1
    ${ver3_result}=     Wait Until Device Tool Get Tech Data Is Open
    Should Be Equal As Integers  ${ver3_result}  1
    ${close_result}=    Close Device Tool Get Tech Data
    Should Be Equal As Integers  ${close_result}  1

    # Including routers
    Select Device       ${RT_SERIAL}
    ${nav2_result}=     Navigate To Device Get Tech Data
    Should Be Equal As Integers  ${nav2_result}  1
    ${reject_result}=   Reject Device Tool Get Tech Data
    Should Be Equal As Integers  ${reject_result}  1

TCXM-16935: Confirm Locate Device Tool Is Available Only For A Single AP or Router
    [Documentation]     Confirms the Locate Device menu item is available for only a single selected AP or Router and opens/closes the correct dialog
    [Tags]              tcxm_16935   development

    Refresh Devices Page

    # Locate Device Tool is available for a single AP
    Select Device       ${AP_SERIAL}
    ${nav_result}=      Navigate To Device Locate Device
    Should Be Equal As Integers  ${nav_result}  1
    ${load_result}=     Verify Device Tool Loading Is Open
    Should Be Equal As Integers  ${load_result}  1
    ${verify_result}=   Wait Until Device Tool Locate Device Is Open
    Should Be Equal As Integers  ${verify_result}  1
    ${close_result}=    Close Device Tool Locate Device
    Should Be Equal As Integers  ${close_result}  1

    # Locate Device Tool is NOT available for multiple devices
    Select Devices      ${AP_SERIAL}   ${RT_SERIAL}
    ${nav_result}=      Navigate To Device Locate Device
    Should Be Equal As Integers  ${nav_result}  -1

    Refresh Devices Page

    # Locate Device Tool is NOT available for a single switch
    Select Device       ${SW_SERIAL}
    ${nav_result}=      Navigate To Device Locate Device
    Should Be Equal As Integers  ${nav_result}  -1

    Refresh Devices Page

    # Locate Device Tool is available for a single router
    Select Device       ${RT_SERIAL}
    ${nav_result}=      Navigate To Device Locate Device
    Should Be Equal As Integers  ${nav_result}  1
    ${load_result}=     Verify Device Tool Loading Is Open
    Should Be Equal As Integers  ${load_result}  1
    ${verify_result}=   Wait Until Device Tool Locate Device Is Open
    Should Be Equal As Integers  ${verify_result}  1
    ${close_result}=    Close Device Tool Locate Device
    Should Be Equal As Integers  ${close_result}  1

TCXM-16936: Confirm L2 Neighbor Info Tool Is Available Only For A Single AP or Router
    [Documentation]     Confirms the L2 Neighbor Info menu item is available for only a single selected AP or Router and opens/closes the correct dialog
    [Tags]              tcxm_16936   development

    Refresh Devices Page

    # L2 Neighbor Info Tool is available for a single AP
    Select Device       ${AP_SERIAL}
    ${nav_result}=      Navigate To Device Layer Neighbor Info
    Should Be Equal As Integers  ${nav_result}  1
    ${load_result}=     Verify Device Tool Loading Is Open
    Should Be Equal As Integers  ${nav_result}  1
    ${verify_result}=   Wait Until Device Tool Neighbor Info Is Open
    Should Be Equal As Integers  ${verify_result}  1
    ${close_result}=    Close Device Tool Neighbor Info
    Should Be Equal As Integers  ${close_result}  1

    # L2 Neighbor Info Tool is NOT available for multiple devices
    Select Devices      ${AP_SERIAL}   ${RT_SERIAL}
    ${nav_result}=      Navigate To Device Layer Neighbor Info
    Should Be Equal As Integers  ${nav_result}  -1

    Refresh Devices Page

    # L2 Neighbor Info Tool is NOT available for a single switch
    Select Device       ${SW_SERIAL}
    ${nav_result}=      Navigate To Device Layer Neighbor Info
    Should Be Equal As Integers  ${nav_result}  -1

    Refresh Devices Page

    # L2 Neighbor Info Tool is available for a single router
    Select Device       ${RT_SERIAL}
    ${nav_result}=      Navigate To Device Layer Neighbor Info
    Should Be Equal As Integers  ${nav_result}  1
    ${close_result}=    Close Device Tool Neighbor Info
    Should Be Equal As Integers  ${close_result}  1

TCXM-16938: Confirm VLAN Probe Tool Is Available For Any Number Of Devices
    [Documentation]     Confirms the VLAN Probe menu item is available for any number of selected devices and opens/closes the correct dialog
    [Tags]              tcxm_16938   development

    Refresh Devices Page

    # VLAN Probe Tool is available for a single AP
    Select Device       ${AP_SERIAL}
    ${nav_result}=      Navigate To Device Vlan Probe
    Should Be Equal As Integers  ${nav_result}  1
    ${load_result}=     Verify Device Tool Loading Is Open
    Should Be Equal As Integers  ${load_result}  1
    ${verify_result}=   Wait Until Device Tool Vlan Probe Is Open
    Should Be Equal As Integers  ${verify_result}  1
    ${close_result}=    Close Device Tool Vlan Probe
    Should Be Equal As Integers  ${close_result}  1

    # VLAN Probe Tool is ALSO available for multiple devices
    Select Devices      ${AP_SERIAL}   ${SW_SERIAL}
    ${nav_result}=      Navigate To Device Vlan Probe
    Should Be Equal As Integers  ${nav_result}  1
    ${close_result}=    Close Device Tool Vlan Probe
    Should Be Equal As Integers  ${close_result}  1

    # Including routers
    Select Device       ${RT_SERIAL}
    ${nav2_result}=     Navigate To Device Vlan Probe
    Should Be Equal As Integers  ${nav2_result}  1
    ${reject_result}=   Close Device Tool Vlan Probe
    Should Be Equal As Integers  ${reject_result}  1

TCXM-16937: Confirm Packet Capture Tool Is Available Only For A Single AP
    [Documentation]     Confirms the Packet Capture menu item is available for only a single selected AP and opens/closes the correct dialog
    [Tags]              tcxm_16937   development

    Refresh Devices Page

     # Packet Capture Tool is available for a single AP
    Select Device       ${AP_SERIAL}
    ${nav_result}=      Navigate To Device Packet Capture
    Should Be Equal As Integers  ${nav_result}  1
    ${load_result}=     Verify Device Tool Loading Is Open
    Should Be Equal As Integers  ${load_result}  1
    ${verify_result}=   Wait Until Device Tool Packet Capture Is Open
    Should Be Equal As Integers  ${verify_result}  1
    ${close_result}=    Close Device Tool Packet Capture
    Should Be Equal As Integers  ${close_result}  1

    # Packet Capture Tool is NOT available for multiple devices
    Select Devices      ${AP_SERIAL}   ${SW_SERIAL}
    ${nav_result}=      Navigate To Device Packet Capture
    Should Be Equal As Integers  ${nav_result}  -1

    Refresh Devices Page

    # Packet Capture Tool is NOT available for single switch
    Select Device       ${SW_SERIAL}
    ${nav_result}=      Navigate To Device Packet Capture
    Should Be Equal As Integers  ${nav_result}  -1

    Refresh Devices Page

    # Packet Capture Tool is NOT available for single router
    Select Device       ${RT_SERIAL}
    ${nav_result}=      Navigate To Device Packet Capture
    Should Be Equal As Integers  ${nav_result}  -1

TCXM-16931: Confirm Ping Tool Is Available Only For A Single Device
    [Documentation]     Confirms the Diagnostics Ping menu item is available for only one device and opens/closes the correct dialog
    [Tags]              tcxm_16931   development

    Refresh Devices Page

    # Ping is available for a single AP
    Select Device       ${AP_SERIAL}
    ${nav_result}=      Navigate To Device Ping
    Should Be Equal As Integers  ${nav_result}  1
    ${load_result}=     Verify Device Tool Loading Is Open
    Should Be Equal As Integers  ${load_result}  1
    ${verify_result}=   Wait Until Device Tool Ping Is Open
    Should Be Equal As Integers  ${verify_result}  1
    ${close_result}=    Close Device Tool Ping
    Should Be Equal As Integers  ${close_result}  1

    Refresh Devices Page

    # Ping is available for a single Switch
    Select Device       ${SW_SERIAL}
    ${nav_result}=      Navigate To Device Ping
    Should Be Equal As Integers  ${nav_result}  1
    ${close_result}=    Close Device Tool Ping
    Should Be Equal As Integers  ${close_result}  1

    Refresh Devices Page

    # Ping is NOT available for multiple devices
    Select Devices      ${AP_SERIAL}   ${RT_SERIAL}
    ${nav_result}=      Navigate To Device Ping
    Should Be Equal As Integers  ${nav_result}  -1

    Refresh Devices Page

    # Ping is available for a single Router
    Select Device       ${RT_SERIAL}
    ${nav_result}=      Navigate To Device Ping
    Should Be Equal As Integers  ${nav_result}  1
    ${close_result}=    Close Device Tool Ping
    Should Be Equal As Integers  ${close_result}  1

TCXM-16932: Confirm Show Roaming Cache Tool Is Available For A Single AP
    [Documentation]     Confirms the Diagnostic Show Roaming Cache menu item is available for only a single selected AP and opens/closes the correct dialog
    [Tags]              tcxm_16932   development

    Refresh Devices Page

    # Show Roaming Cache tool is available for a single AP
    Select Device       ${AP_SERIAL}
    ${nav_result}=      Navigate To Device Show Roaming Cache
    Should Be Equal As Integers  ${nav_result}  1
    ${load_result}=     Verify Device Tool Loading Is Open
    Should Be Equal As Integers  ${load_result}  1
    ${verify_result}=   Wait Until Device Tool Show Roaming Cache Is Open
    Should Be Equal As Integers  ${verify_result}  1
    ${close_result}=    Close Device Tool Show Roaming Cache
    Should Be Equal As Integers  ${close_result}  1

    # Show Roaming Cache tool is NOT available for multiple devices
    Select Devices      ${AP_SERIAL}   ${SW_SERIAL}
    ${nav_result}=      Navigate To Device Show Roaming Cache
    Should Be Equal As Integers  ${nav_result}  -1

    Refresh Devices Page

    # Show Roaming Cache tool is NOT available for single switch
    Select Device       ${SW_SERIAL}
    ${nav_result}=      Navigate To Device Show Roaming Cache
    Should Be Equal As Integers  ${nav_result}  -1

    Refresh Devices Page

    # Show Roaming Cache is NOT available for single router
    Select Device       ${RT_SERIAL}
    ${nav_result}=      Navigate To Device Show Roaming Cache
    Should Be Equal As Integers  ${nav_result}  -1


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success  ${XIQ_USER}  ${XIQ_PASSWORD}  ${XIQ_URL}
    Onboard Test Devices

Onboard Test Devices
    [Documentation]     Onboards the test devices

    # Configure the IQAgent or Hive Agent on the devices
    Configure CAPWAP               ${AP_CONSOLE_IP}  ${AP_CONSOLE_PORT}  ${AP_USERNAME}
    ...                            ${AP_PASSWORD}  ${AP_PLATFORM}  ${XIQ_CAPWAP_URL}

    Configure CAPWAP               ${RT_CONSOLE_IP}  ${RT_CONSOLE_PORT}  ${RT_USERNAME}
    ...                            ${RT_PASSWORD}  ${RT_PLATFORM}  ${XIQ_CAPWAP_URL}

    Configure iqagent for Aerohive Switch  ${SW_CONSOLE_IP}  ${SW_CONSOLE_PORT}  ${SW_USERNAME}
    ...                                    ${SW_PASSWORD}  ${IQAGENT}

    Navigate to Devices and Confirm Success

    # Onboard the devices for the test
    ${dut1_result}=     Search Device Serial   ${AP_SERIAL}
    Run Keyword If      '${dut1_result}' != '1'  Onboard Device   ${AP_SERIAL}  ${AP_MAKE}  location=${AP_LOCATION}
    ${dut2_result}=     Search Device Serial   ${SW_SERIAL}
    Run Keyword If      '${dut2_result}' != '1'  Onboard Device   ${SW_SERIAL}  ${SW_MAKE}  location=${SW_LOCATION}
    ${dut3_result}=     Search Device Serial   ${RT_SERIAL}
    Run Keyword If      '${dut3_result}' != '1'  Onboard Device   ${RT_SERIAL}  ${RT_MAKE}  location=${RT_LOCATION}

    # Confirm the devices were onboarded
    Confirm Device Serial Present  ${AP_SERIAL}
    Confirm Device Serial Present  ${SW_SERIAL}
    Confirm Device Serial Present  ${RT_SERIAL}

    Wait Until Device Online  ${AP_SERIAL}
    Wait Until Device Online  ${RT_SERIAL}
    Wait Until Device Online  ${SW_SERIAL}

Select Device
    [Documentation]     Selects the specified device and confirms the action was successful
    [Arguments]         ${serial}

    ${result}=          Select Device Row   ${serial}
    Should Be Equal As Integers    ${result}  1

Select Devices
    [Documentation]     Selects the specified devices and confirms the action was successful
    [Arguments]         ${serial1}   ${serial2}

    ${result}=          Select Device Rows   device_serials=${serial1},${serial2}
    Should Be Equal As Integers    ${result}  1

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, and closes the browser

    Clean Up Test Device and Confirm Success  ${AP_SERIAL}
    Clean Up Test Device and Confirm Success  ${SW_SERIAL}
    Clean Up Test Device and Confirm Success  ${RT_SERIAL}
    Log Out of XIQ and Quit Browser

Clean Up Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Navigate to Devices and Confirm Success
    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}

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
