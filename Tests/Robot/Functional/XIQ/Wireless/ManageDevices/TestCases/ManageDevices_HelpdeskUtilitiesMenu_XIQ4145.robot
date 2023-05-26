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
Library          xiq/flows/globalsettings/AccountManagement.py
Library          common/GmailHandler.py

Resource         ../../ManageDevices/Resources/AllResources.robot

Force Tags       testbed_3_node

Suite Setup      Log Into XIQ and Set Up Test
Suite Teardown   Run Keyword And Warn On Failure    Tear Down Test and Close Session


*** Variables ***
${XIQ_URL}            ${test_url}
${XIQ_USER}           ${tenant_username}
${XIQ_PASSWORD}       ${tenant_password}
${XIQ_CAPWAP_URL}     ${capwap_url}
${IQAGENT}            ${sw_connection_host}

${AP_LOCATION}        auto_location_01, Santa Clara, building_02, floor_04
${SW_LOCATION}        auto_location_01, Santa Clara, building_02, floor_04
${RT_LOCATION}        auto_location_01, Santa Clara, building_02, floor_04


*** Test Cases ***
TCXM-19799: Confirm Access To APs Diagnostics
    [Documentation]     Confirms the expected list of utilities diagnostics are available for APs
    [Tags]              tcxm_19799   development

    Navigate to Devices and Confirm Success
    Select Device       ${device1.serial}
    ${nav_result}=      Navigate To Device Utilities Diagnostics
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Verify Device Tool Ping Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Log Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Version Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Running Config Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Startup Config Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Ip Routes Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Mac Routes Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Arp Cache Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Roaming Cache Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Dnxp Neighbors Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Dnxp Cache Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Amrp Tunnel Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Gre Tunnel Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Ike Event Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Ike Sa Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Ipsec Sa Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Ipsec Tunnel Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Cpu Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Memory Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19757: Confirm No Access To APs Reset Device To Default
    [Documentation]     Confirms the Reset Device To Default is not available for APs
    [Tags]              tcxm_19757   development

    ${nav_visible}=     Verify Reset Device To Default Available    expect_failure=True
    Should Be Equal As Integers   ${nav_visible}   -1

TCXM-19801: Confirm Access To APs Spectrum Intelligence
    [Documentation]     Confirms the Spectrum Intelligence is available for APs
    [Tags]              tcxm_19801   development

    ${nav_visible}=     Verify Device Spectrum Intelligence Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19805: Confirm Access To APs Status
    [Documentation]     Confirms the expected list of Status actions are available for APs
    [Tags]              tcxm_19805   development

    ${nav_result}=      Navigate To Device Utilities Status
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Verify Device Status Advanced Channel Selection Protocol Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Status Interface Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Status Wifi Status Summary Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19808: Confirm Access To APs Tools
    [Documentation]     Confirms the expected list of Tools are available for APs
    [Tags]              tcxm_19808   development

    ${nav_result}=      Navigate To Device Utilities Tools
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Verify Device Tool Client Information Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Get Tech Data Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Locate Device Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Layer Neighbor Info Available
    Should Be Equal As Integers   ${nav_visible}   1
#    ${nav_visible}=     Is Device Tool Packet Capture Available
#    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Vlan Probe Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19800: Confirm Access To Routers Diagnostics
    [Documentation]     Confirms the expected list of utilities diagnostics are available for routers
    [Tags]              tcxm_19800   development

    Refresh Devices Page
    Select Device       ${device3.serial}
    ${nav_result}=      Navigate To Device Utilities Diagnostics
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Verify Device Tool Ping Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Log Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Version Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Running Config Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Startup Config Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Ip Routes Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Mac Routes Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Arp Cache Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Ike Event Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Ike Sa Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Ipsec Sa Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Ipsec Tunnel Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Cpu Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Memory Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19757: Confirm No Access To Routers Reset Device To Default
    [Documentation]     Confirms the Reset Device To Default is not available for routers
    [Tags]              tcxm_19757   development

    ${nav_visible}=     Verify Reset Device To Default Available    expect_failure=True
    Should Be Equal As Integers   ${nav_visible}   -1

TCXM-19807: Confirm Access To Routers Status
    [Documentation]     Confirms the expected list of Status actions are available for routers
    [Tags]              tcxm_19807   development

    ${nav_result}=      Navigate To Device Utilities Status
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Verify Device Status Interface Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19809: Confirm Access To Routers Tools
    [Documentation]     Confirms the expected list of Tools are available for routers
    [Tags]              tcxm_19809   development

    ${nav_result}=      Navigate To Device Utilities Tools
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Verify Device Tool Client Information Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Get Tech Data Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Locate Device Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Layer Neighbor Info Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Vlan Probe Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19810: Confirm Access To Switches Diagnostics
    [Documentation]     Confirms the expected list of utilities diagnostics are available for switches
    [Tags]              tcxm_19810   development

    Refresh Devices Page
    Select Device       ${device2.serial}
    ${nav_result}=      Navigate To Device Utilities Diagnostics
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Verify Device Tool Ping Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Log Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Mac Table Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Version Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Running Config Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Startup Config Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Ip Routes Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Cpu Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Memory Available
    Should Be Equal As Integers   ${nav_visible}   1
    ${nav_visible}=     Verify Device Tool Show Pse Available
    Should Be Equal As Integers   ${nav_visible}   1

TCXM-19757: Confirm No Access To Switches Reset Device To Default
    [Documentation]     Confirms the Reset Device To Default is not available for switches
    [Tags]              tcxm_19757   development

    ${nav_visible}=     Verify Reset Device To Default Available    expect_failure=True
    Should Be Equal As Integers   ${nav_visible}   -1

TCXM-19993: Confirm Access To Switches Tools
    [Documentation]     Confirms the expected list of Tools are available for switches
    [Tags]              tcxm_19993   development

    ${nav_result}=      Navigate To Device Utilities Tools
    Should Be Equal As Integers  ${nav_result}  1

    ${nav_visible}=     Verify Device Tool Get Tech Data Available
    Should Be Equal As Integers   ${nav_visible}   1


*** Keywords ***
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    ${device1}=      Create Dictionary
    ...     name=simulated_dut05
    ...     model=AP460C
    ...     simulated_count=1
    ...     onboard_device_type=Simulated
    ...     location=auto_location_01, Santa Clara, building_02, floor_04

    set suite variable    ${device1}

    ${device2}=      Create Dictionary
    ...     name=simulated_dut06
    ...     model=SR2348P
    ...     simulated_count=1
    ...     onboard_device_type=Simulated
    ...     location=auto_location_01, Santa Clara, building_02, floor_04

    set suite variable    ${device2}

    ${device3}=      Create Dictionary
    ...     name=simulated_dut07
    ...     model=XR600P
    ...     simulated_count=1
    ...     onboard_device_type=Simulated
    ...     location=auto_location_01, Santa Clara, building_02, floor_04

    set suite variable    ${device3}

    Log Into XIQ and Confirm Success   ${XIQ_USER}   ${XIQ_PASSWORD}   ${XIQ_URL}
    Delete Management Account   ${XIQ_HD_USER}
    Onboard Test Devices
    Log Out of XIQ and Quit Browser
    Create HelpDesk Role Account        ${HELPDESK_ROLE}
     Log Into XIQ and Confirm Success   ${XIQ_HD_USER}   ${XIQ_HD_PASSWORD}   ${XIQ_URL}

Create HelpDesk Role Account
    [Documentation]     Create HelpDesk Role Account
    [Arguments]         ${HELPDESK_ROLE}
    Login User  ${TENANT_USERNAME}    ${TENANT_PASSWORD}
    Create Role Based Account        ${HELPDESK_ROLE}
    logout user
    sleep   4s
    ${URL}=                 get_url_to_set_password_for_new_user     ${HELPDESK_EMAIL}     ${HELPDESK_APP_PASSWORD}
    ${DRIVER}=              load web page       url=${URL}
    ${result2}=             set_password      ${help_password}
    Quit Browser

Onboard Test Devices
    [Documentation]     Onboards the test devices

    ${ONBOARD_RESULT1}=      onboard device quick    ${device1}
    Should Be Equal As Strings          ${ONBOARD_RESULT1}       1

    ${ONBOARD_RESULT2}=       onboard device quick    ${device2}
    Should Be Equal As Strings          ${ONBOARD_RESULT2}       1

    ${ONBOARD_RESULT3}=       onboard device quick    ${device3}
    Should Be Equal As Strings          ${ONBOARD_RESULT3}       1

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
    Clean Up Test Device and Confirm Success  ${device1.serial}
    Clean Up Test Device and Confirm Success  ${device2.serial}
    Clean Up Test Device and Confirm Success  ${device3.serial}
    Log Out of XIQ and Quit Browser

Clean Up Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Delete Device and Confirm Success  ${serial}
    Confirm Device Serial Not Present  ${serial}
