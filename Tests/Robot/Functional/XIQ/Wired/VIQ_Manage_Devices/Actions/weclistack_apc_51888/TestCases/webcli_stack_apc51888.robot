@@ -1,206 +0,0 @@
# Author        : Siva prasath
# Description   : This script run the below tests for WEB CLI feature according with APC-51888 story
# Testcases      : TCXM-15265,TCXM-15266,TCXM-15267,TCXM-15268,TCXM-15269,TCXM-15270
# Date Updated  : 17-Mar-2022
# Pre-Requests  : First organization should be created in the XIQ prior to start this test script in case of AIO. In cloud it is not necessary.
# Comments      : This test is applicable for exos stack devices(5520/5420/5320/X440G2) only, while the test case will skip on other platforms



*** Variables ***

${IQAGENT}                  ${CAPWAP_URL}
${delete_vlan_flag}         False
*** Settings ***
Resource    Tests/Robot/Libraries/XIQ/Wired/WiredCommon.robot

Suite Setup      Pre Condition
Suite Teardown   Cleanup
Force Tags      testbed_1_node
*** Test Cases ***
TCXM-15265: Verify that WEB CLI is available for EXOS Stack
    #Onboarding:
    [Documentation]	This testcase Onboard and checks the Web CLI is available for stack
    [Tags]              tcxm_15265   production              p1

    Delete Device     device_mac=${netelem1.mac}
    @{result} =    Split String    ${netelem1.serial}    ,
    FOR		${serialnumber}     IN    @{result}
    		Delete Device       device_serial=${serialnumber}
    END
 
   
    create_first_organization       Extreme       broadway        new york     Romania

    delete_location_building_floor           ${location}         ${building}     ${floor}

    create_location_building_floor           ${location}         ${building}     ${floor}
    
    ${DUT_LOCATION}      Set Variable       ${location},${building},${floor}
    
    log to console          os  ${netelem1.cli_type}      platform ${netelem1.platform}
    run keyword if  """${netelem1.cli_type}"""== "exos" and """${netelem1.platform}""" != "Stack"
    ...  quick_onboarding_cloud_manual     ${netelem1.serial}    exos      ${DUT_LOCATION}
    #Configure IQAgent

    run keyword if  """${netelem1.cli_type}"""== "exos" and """${netelem1.platform}""" == "Stack"
    ...    quick_onboarding_cloud_manual     ${netelem1.serial}    exos      ${DUT_LOCATION}
    #Configure IQAgent
    Configure IQAgent for EXOS Switch

    #Check Status:
    sleep   120s
    check device online

    #Check Managed status:
    column picker select    Managed
    
    ${onboard_result} =   Wait Until Device Online   device_mac=${netelem1.mac}
    Should Be Equal As Integers                 ${onboard_result}       1

    sleep  2s
    Navigate to Devices and Confirm Success
    refresh devices page
    ${output}=              Test device cli     show iq         device_mac=${netelem1.mac}
    should be string        ${output}
    run keyword if      """${netelem1.platform}"""== "Stack"
    ...     should contain          ${output}           ${netelem1.stack.slot1.serial}
    ...     ELSE        should contain          ${output}           ${netelem1.serial}
    sleep  2s

TCXM-15266: Ping command can be executed to a specific destination
    [Documentation]	Verify that the user can iniate a ping command from EXOS Stack through WEB CLI
    [Tags]              tcxm_15266   production              p1

    Navigate to Devices and Confirm Success
    refresh devices page
    ${output}=              test device cli   ping 127.0.0.1        device_mac=${netelem1.mac}
    should be string        ${output}
    should contain   ${output}   packets received
    sleep  2s

TCXM-15267: Traceroute command can be executed to a specific destination
    [Documentation]	Verify that the user can iniate a traceroute command from EXOS Stack through WEB CLI
    [Tags]              tcxm_15267   production              p1
    Navigate to Devices and Confirm Success
    refresh devices page
    ${output}=              test device cli    traceroute www.google.com   device_mac=${netelem1.mac}      delay=60
    log to console          ${output}
    should be string        ${output}
    should contain          ${output}           traceroute
    sleep  2s


TCXM-15268: Verify that the user can iniate show commands for interface, protocols through WEB CLI
    [Documentation]	Verify that the user can iniate show commands for interface, protocols through WEB CLI
    [Tags]              tcxm_15268   production              p1
    Navigate to Devices and Confirm Success
    refresh devices page
    ${output}=              test device cli     show ports no-refresh       device_mac=${netelem1.mac}
    should be string        ${output}
    should contain   ${output}       Port Summary
    sleep  2s
    refresh devices page
    Navigate to Devices and Confirm Success
    ${output}=              test device cli   show protocol     device_mac=${netelem1.mac}
    should be string        ${output}
    should contain   ${output}   Value
    sleep  2s

TCXM-15269 Verify that the user can iniate bogus commands through WEB CLI
    [Documentation]	Verify that the user can iniate bogus commands through WEB CLI
    [Tags]              tcxm_15269   production              p1

    Navigate to Devices and Confirm Success
    refresh devices page
    ${output}=              test device cli   randomtext        device_mac=${netelem1.mac}
    log to console          Result: ${output}
    should be string        ${output}
    should contain   ${output}   Invalid input detected
    sleep  2s

TCXM-15270: Verify that the user has the ability for configuring items are supported in XIQ, through WEB CLI
    [Documentation]	Verify that the user has the ability for configuring items not supported in XIQ, through WEB CLI
    [Tags]              tcxm_15270   production              p1
    Navigate to Devices and Confirm Success
    refresh devices page
    ${output}=              test device cli
    ...  create vlan 3,configure vlan 3 ipaddress 2.2.2.2/24,configure vlan 3 ipaddress 2.2.2.2/24   delay=10
    ...  device_mac=${netelem1.mac}
    should be string        ${output}
    should contain   ${output}   Can't change primary IP Address. Please unconfig the Primary IP address on VLAN first
    sleep  2s
    #Set TRUE ${delete_vlan_flag} true . The vlan 3 will be deleted in teardown
    SET GLOBAL VARIABLE     ${delete_vlan_flag}       ${TRUE}

*** Keywords ***
Pre Condition
    [Documentation]     Pre condition to check if the OS is voss the test should skip
    run keyword if  """${netelem1.platform}""" == "Stack"        Log Into XIQ and Set Up Test
    ...  ELSE   run keywords  log to console  The testbed runs on VOSS or EXOS Standalone where the feature not supported on VOSS/EXOS. Hence skipping all testcases
    ...  AND    skip
    ${randomstring}     Generate Random String
    ${location}=        Set variable             ${netelem1.mac}_${randomstring}
    ${building}=        Set variable             building_${randomstring}
    ${floor}=           Set variable               floor_${randomstring}
    set global variable     ${location}
    set global variable     ${building}
    set global variable     ${floor}
Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success
    Navigate to Devices and Confirm Success
Log Into XIQ and Confirm Success
    [Documentation]     Logs into XIQ and confirms the login was successful

    ${result}=      Login User      ${tenant_username}     ${tenant_password}
    Should Be Equal As Integers     ${result}     1

Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view and confirms the action was successful

    ${nav_result}=  Navigate to Devices
    Should Be Equal As Integers  ${nav_result}  1

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, closes the browser, and resets the NOS version
    Delete Device       device_mac=${netelem1.mac}
    @{result} =    Split String    ${netelem1.serial}    ,
    FOR		${serialnumber}     IN    @{result}
    		Delete Device       device_serial=${serialnumber}
    END
    delete_location_building_floor              ${location}         ${building}     ${floor}
    clear vlans
    Log Out of XIQ and Confirm Success
    Quit Browser
Cleanup
    [Documentation]     Cleans up test data, logs out of XIQ, closes the browser, and resets the NOS version
    run keyword if  """${netelem1.platform}"""== "Stack"                 Tear Down Test and Close Session
    ...  ELSE   run keywords  log to console  The testbed runs on VOSS or EXOS, where the feature not supported on VOSS/EXOS. Hence skipping all testcases
    ...  AND    skip

Log Out of XIQ and Confirm Success
    [Documentation]     Log out of XIQ and confirms the logout was successful

    ${result}=      Logout User
    Should Be Equal As Integers     ${result}     1

Configure IQAgent for EXOS Switch
    [Documentation]     Configures the iqagent for the EXOS switch


    connect to network element  dut1_telnet  ${netelem1.ip}  ${netelem1.username}  ${netelem1.password}  telnet  ${netelem1.cli_type}
    send cmd  dut1_telnet   disable iqagent    max_wait=10    interval=2    confirmation_phrases="Do you want to continue?"    confirmation_args="y"

    send cmd  dut1_telnet   configure iqagent server ipaddress none
    send cmd  dut1_telnet   configure iqagent server vr VR-Mgmt
    send cmd  dut1_telnet   configure iqagent server ipaddress ${sw_connection_host}
    send cmd  dut1_telnet   enable iqagent
    ${check_results}=  send cmd  dut1_telnet   show iqagent
    log   ${check_results[0].cmd_obj._return_text}
    log to console      ${check_results[0].cmd_obj._return_text}
    Should Contain   ${check_results[0].cmd_obj._return_text}   ${sw_connection_host}
    log  ${check_results[0].return_text}
    Should Contain   ${check_results[0].return_text}   ${sw_connection_host}
    [Teardown]  close connection to network element  dut1_telnet

Check Device Online
    [Documentation]     This keyword will check if devices are online

    ${online_sw2}=      Wait Until Device Online                    device_mac=${netelem1.mac}

    Should Be Equal As Integers                 ${online_sw2}       1


clear vlans
    [Documentation]     This keyword will delete vlan 3

    connect to network element  dut1_telnet  ${netelem1.ip}  ${netelem1.username}  ${netelem1.password}  telnet  ${netelem1.cli_type}
    send cmd   dut1_telnet      delete vlan 3

    [Teardown]  close connection to network element  dut1_telnet
