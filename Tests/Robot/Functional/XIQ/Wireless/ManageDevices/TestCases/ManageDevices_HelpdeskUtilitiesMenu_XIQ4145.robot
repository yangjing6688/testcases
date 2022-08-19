#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : John Borges
# Description   : Test Suite for testing the device utilities menu for helpdesk user
# Topology      : 1 simulated AP, 1 simulated non EXOS/VOSS Switch and 1 simulated Router will be onboarded
#               : A helpdesk user will have to be pre-configured before running these tests


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

${AP_SERIAL}
${AP_LOCATION}        Aerohive Networks, Milpitas, Aerohive HQ, 2nd Fl - M
${SW_SERIAL}
${SW_LOCATION}        Aerohive Networks, Milpitas, Aerohive HQ, 2nd Fl - M
${RT_SERIAL}
${RT_LOCATION}        Aerohive Networks, Milpitas, Aerohive HQ, 2nd Fl - M


*** Test Cases ***
TCXM-19799: Confirm Access To APs Diagnostics
    [Documentation]     Confirms the expected list of utilities diagnostics are available for APs
    [Tags]              tcxm_19799   development

    Navigate to Devices and Confirm Success
    Select Device       ${AP_SERIAL}
    ${nav_result}=      Navigate To Device Utilities Diagnostics
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Is Device Tool Ping Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Log Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Version Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Running Config Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Startup Config Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Ip Routes Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Mac Routes Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Arp Cache Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Roaming Cache Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Dnxp Neighbors Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Dnxp Cache Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Amrp Tunnel Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Gre Tunnel Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Ike Event Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Ike Sa Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Ipsec Sa Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Ipsec Tunnel Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Cpu Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Memory Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19757: Confirm No Access To APs Reset Device To Default
    [Documentation]     Confirms the Reset Device To Default is not available for APs
    [Tags]              tcxm_19757   development

    ${nav_visible}=     Is Reset Device To Default Available
    Should Be Equal As Integers   ${nav_visible}   -1

TCXM-19801: Confirm Access To APs Spectrum Intelligence
    [Documentation]     Confirms the Spectrum Intelligence is available for APs
    [Tags]              tcxm_19801   development

    ${nav_visible}=     Is Device Spectrum Intelligence Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19805: Confirm Access To APs Status
    [Documentation]     Confirms the expected list of Status actions are available for APs
    [Tags]              tcxm_19805   development

    ${nav_result}=      Navigate To Device Utilities Status
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Is Device Status Advanced Channel Selection Protocol Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Status Interface Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Status Wifi Status Summary Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19808: Confirm Access To APs Tools
    [Documentation]     Confirms the expected list of Tools are available for APs
    [Tags]              tcxm_19808   development

    ${nav_result}=      Navigate To Device Utilities Tools
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Is Device Tool Client Information Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Get Tech Data Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Locate Device Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Layer Neighbor Info Available
    Should Be Equal As Integers   ${nav_visible}   1
#    ${nav_visible}=     Is Device Tool Packet Capture Available
#    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Vlan Probe Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19800: Confirm Access To Routers Diagnostics
    [Documentation]     Confirms the expected list of utilities diagnostics are available for routers
    [Tags]              tcxm_19800   development

    Refresh Devices Page
    Select Device       ${RT_SERIAL}
    ${nav_result}=      Navigate To Device Utilities Diagnostics
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Is Device Tool Ping Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Log Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Version Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Running Config Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Startup Config Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Ip Routes Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Mac Routes Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Arp Cache Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Ike Event Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Ike Sa Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Ipsec Sa Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Ipsec Tunnel Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Cpu Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Memory Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19757: Confirm No Access To Routers Reset Device To Default
    [Documentation]     Confirms the Reset Device To Default is not available for routers
    [Tags]              tcxm_19757   development

    ${nav_visible}=     Is Reset Device To Default Available
    Should Be Equal As Integers   ${nav_visible}   -1

TCXM-19807: Confirm Access To Routers Status
    [Documentation]     Confirms the expected list of Status actions are available for routers
    [Tags]              tcxm_19807   development

    ${nav_result}=      Navigate To Device Utilities Status
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Is Device Status Interface Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19809: Confirm Access To Routers Tools
    [Documentation]     Confirms the expected list of Tools are available for routers
    [Tags]              tcxm_19809   development

    ${nav_result}=      Navigate To Device Utilities Tools
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Is Device Tool Client Information Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Get Tech Data Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Locate Device Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Layer Neighbor Info Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Vlan Probe Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19810: Confirm Access To Switches Diagnostics
    [Documentation]     Confirms the expected list of utilities diagnostics are available for switches
    [Tags]              tcxm_19810   development

    Refresh Devices Page
    Select Device       ${SW_SERIAL}
    ${nav_result}=      Navigate To Device Utilities Diagnostics
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Is Device Tool Ping Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Log Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Mac Table Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Version Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Running Config Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Startup Config Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Ip Routes Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Cpu Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Memory Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Is Device Tool Show Pse Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19757: Confirm No Access To Switches Reset Device To Default
    [Documentation]     Confirms the Reset Device To Default is not available for switches
    [Tags]              tcxm_19757   development

    ${nav_visible}=     Is Reset Device To Default Available
    Should Be Equal As Integers   ${nav_visible}   -1

TCXM-19993: Confirm Access To Switches Tools
    [Documentation]     Confirms the expected list of Tools are available for switches
    [Tags]              tcxm_19993   development

    ${nav_result}=      Navigate To Device Utilities Tools
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Is Device Tool Get Tech Data Available
    Should Be Equal As Integers   ${nav_visible}   1


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success  ${XIQ_USER}   ${XIQ_PASSWORD}   ${XIQ_URL}
    Onboard Test Devices
    Log Out of XIQ and Quit Browser
    Log Into XIQ and Confirm Success   ${XIQ_HD_USER}   ${XIQ_HD_PASSWORD}   ${XIQ_URL}

Onboard Test Devices
    [Documentation]     Onboards the test devices

    ${AP_SERIAL}=       Onboard Simulated Device   AP460C   location=${AP_LOCATION}
    Set Suite Variable          ${AP_SERIAL}
    ${SW_SERIAL}=       Onboard Simulated Device   SR2348P   location=${SW_LOCATION}
    Set Suite Variable          ${SW_SERIAL}
    ${RT_SERIAL}=       Onboard Simulated Device   XR600P   location=${RT_LOCATION}
    Set Suite Variable          ${RT_SERIAL}

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

    Log Out of XIQ and Quit Browser
    Log Into XIQ and Confirm Success   ${XIQ_USER}   ${XIQ_PASSWORD}   ${XIQ_URL}
    Clean Up Test Device and Confirm Success  ${AP_SERIAL}
    Clean Up Test Device and Confirm Success  ${SW_SERIAL}
    Clean Up Test Device and Confirm Success  ${RT_SERIAL}
    Log Out of XIQ and Quit Browser

Clean Up Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}
