# Author        : Siva prasath
# Description   : This script run the below tests for WEB CLI feature according with APC-45706 story
# TestCases	: TCXM-13373,TCXM-13369,TCXM-13368,TCXM-13371,TCXM-13370,TCXM-13372,TCXM-13377,TCXM-13376,TCXM-13374,TCXM-13367
# Comments	: This testcase runs on Standalone - EXOS, Doesn't work on VOSS and EXOS-Stack- Hence it will skip on VOSS and EXOS-Stack
# Pre-Requests  : First organization should be created in the XIQ prior to start this test script in case of AIO.
#                 In cloud it is not necessary.

*** Variables ***

${IQAGENT}                  ${CAPWAP_URL}
${delete_vlan_flag}         False

*** Settings ***

Resource    Tests/Robot/Libraries/XIQ/Wired/WiredCommon.robot

Suite Setup      Pre Condition
Suite Teardown   Tear Down Test and Close Session
Force Tags      testbed_1_node

*** Test Cases ***
TCXM-13367: CLI Access is available for an EXOS device
    [Documentation]     Verify that CLI Access is available for an EXOS device
    [Tags]              tcxm_13367   production   p2

    sleep  2s
    refresh devices page
    ${output}=              test device cli     show iqagent		device_serial=${netelem1.serial}
    should be string        ${output}
    should contain          ${output}           ${netelem1.serial}
    sleep  2s

TCXM-13373: Show commands can be executed from WEB CLI on an EXOS switch
    [Documentation]     Verify that show commands can be executed from WEB CLI on an EXOS switch
    [Tags]              tcxm_13373                 p2

    refresh devices page
    ${output}=              test device cli     show switch     	device_serial=${netelem1.serial}      delay=60
    log to console          ${output}
    should be string        ${output}
    should contain          ${output}           OPERATIONAL
    sleep  2s

TCXM-13369: Traceroute command can be executed to a specific destination
    [Documentation]     Verify that Traceroute command can be executed to a specific destination from an onboarded EXOS switch
    [Tags]              tcxm_13369   production   p2

    refresh devices page
    ${output}=              test device cli     traceroute www.google.com	device_serial=${netelem1.serial}      delay=60
    log to console          ${output}
    should be string        ${output}
    should contain          ${output}           traceroute
    sleep  2s

TCXM-13368 Ping command can be executed to a specific destination
    [Documentation]     Verify that Ping command can be executed to a specific destination from an onboarded EXOS switch
    [Tags]              tcxm_13368                 p2

    refresh devices page
    ${output}=              test device cli     ping 127.0.0.1	    device_serial=${netelem1.serial}
    should be string        ${output}
    should contain   ${output}   packets received
    sleep  2s

TCXM-13371 Interface status commands can be executed from WEB CLI on an EXOS switch
    [Documentation]     Verify that interface status commands can be executed from WEB CLI on an EXOS switch
    [Tags]              tcxm_13371                 p2

    refresh devices page
    ${output}=              test device cli     show ports no-refresh	     device_serial=${netelem1.serial}
    should be string        ${output}
    should contain   ${output}       Port Summary
    sleep  2s


TCXM-13370 Protocol status commands can be executed from WEB CLI on an EXOS switch
    [Documentation]     Verify that protocol status commands can be executed from WEB CLI on an EXOS switch
    [Tags]              tcxm_13370                 p2

    refresh devices page
    ${output}=              test device cli    show protocol 		device_serial=${netelem1.serial}
    should be string        ${output}
    should contain   ${output}   Value
    sleep  2s

TCXM-13372 User can send configuration commands from WEB CLI
    [Documentation]     Verify that user can send configuration commands from WEB CLI
    [Tags]              tcxm_13372   production   p2

    refresh devices page
    ${output}=              test device cli
    ...  create vlan 3,configure vlan 3 ipaddress 2.2.2.2/24,configure vlan 3 ipaddress 2.2.2.2/24
    ...	    device_serial=${netelem1.serial}		delay=10
    should be string        ${output}
    should contain   ${output}   Can't change primary IP Address. Please unconfig the Primary IP address on VLAN first
    sleep  2s
    #Set TRUE ${delete_vlan_flag} true . The vlan 3 will be deleted in teardown
    SET GLOBAL VARIABLE     ${delete_vlan_flag}       ${TRUE}

TCXM-13377 Execute multiple commands from WEB CLI on an EXOS switch
    [Documentation]     Execute multiple commands separated by a semicolon cannot be executed from WEB CLI on an EXOS switch
    [Tags]              tcxm_13377                 p2

    refresh devices page
    ${output}=              test device cli    ping 127.0.0.1,show iq,show vlan  	device_serial=${netelem1.serial}
    log to console          Result: ${output}
    should be string        ${output}
    should contain   ${output}   loss
    should contain   ${output}   ${netelem1.serial}
    should contain   ${output}   Default
    sleep  2s

TCXM-13376 Invalid commands cannot be executed from WEB CLI on an EXOS switch
    [Documentation]     Verify that invalid commands cannot be executed from WEB CLI on an EXOS switch
    [Tags]              tcxm_13376   production   p2

    refresh devices page
    ${output}=              test device cli    randomtext		device_serial=${netelem1.serial}
    log to console          Result: ${output}
    should be string        ${output}
    should contain   ${output}   Invalid input detected
    sleep  2s

TCXM-13374 Commands are prefixed with disabled cli paging and cli refresh
    [Documentation]    Verify  CLI commands are prefixed with disabled cli paging and cli refresh, to avoid EXOS paging the output.
    [Tags]              tcxm_13374                 p2

    refresh devices page
    ${output}=              test device cli    show configuration	 device_serial=${netelem1.serial}
    should be string        ${output}
    should contain   ${output}   Module vpex configuration
    sleep  2s

*** Keywords ***
Pre Condition
    [Documentation]     Pre condition to check if the OS is voss the test should skip
    run keyword if  """${netelem1.cli_type}""" == "exos" and """${netelem1.platform}""" != "Stack"    Log Into XIQ and Set Up Test
    ...  ELSE   run keywords  log to console  The testbed runs on OS ${netelem1.cli_type} and platform ${netelem1.platform}, where the Story not supported on VOSS and Stack. Hence skipping all testcases
    ...  AND    skip
    ${randomstring}     Generate Random String

    ${location}=        Set variable             ${netelem1.mac}_${randomstring}
    ${building}=        Set variable             building_${randomstring}
    ${floor}=           Set variable               floor_${randomstring}
    set global variable     ${location}
    set global variable     ${building}
    set global variable     ${floor}

    create_first_organization       Extreme       broadway        new york     Romania

    delete_location_building_floor           ${location}         ${building}     ${floor}

    create_location_building_floor           ${location}         ${building}     ${floor}

    Delete Device       device_serial=${netelem1.serial}

    ${DUT_LOCATION}      Set Variable       ${location},${building},${floor}

    quick_onboarding_cloud_manual     ${netelem1.serial}    exos      ${DUT_LOCATION}

    Configure IQAgent for EXOS Switch

    #Check Status:
    Check Device Online

    #Check Managed status:
    column picker select    Managed

    ${mngt_sw2}=    WAIT UNTIL DEVICE MANAGED       ${netelem1.serial} 

    Should Be Equal As Integers                 ${mngt_sw2}       1

Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success

Log Into XIQ and Confirm Success
    [Documentation]     Logs into XIQ and confirms the login was successful

    ${result}=      Login User      ${tenant_username}     ${tenant_password}
    Should Be Equal As Integers     ${result}     1


Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, closes the browser, and resets the NOS version
    run keyword if  """${netelem1.cli_type}""" == "exos" and """${netelem1.platform}""" != "Stack"       Delete Device       device_serial=${netelem1.serial}
    ...  ELSE   run keywords  log to console  The testbed runs on OS ${netelem1.cli_type} and platform ${netelem1.platform}, where this story not supported on VOSS or Stack. Hence skipping all testcases
    ...  AND    skip

    delete_location_building_floor              ${location}         ${building}     ${floor}

    clear vlans
    Log Out of XIQ and Confirm Success
    Quit Browser

Log Out of XIQ and Confirm Success
    [Documentation]     Log out of XIQ and confirms the logout was successful

    ${result}=      Logout User
    Should Be Equal As Integers     ${result}     1

Configure IQAgent for EXOS Switch
    [Documentation]     Configures the iqagent for the VOSS switch

    connect to network element  dut1_telnet  ${netelem1.ip}  ${netelem1.username}  ${netelem1.password}  telnet  ${netelem1.cli_type}
    send cmd   dut1_telnet      configure iqagent server ipaddress none
    send cmd   dut1_telnet     configure iqagent server vr VR-Mgmt
    send cmd   dut1_telnet      configure iqagent server ipaddress ${sw_connection_host}
    send cmd   dut1_telnet      enable iqagent
    ${check_results}=  send cmd  dut1_telnet   show iqagent
    log  ${check_results[0].return_text}
    Should Contain   ${check_results[0].return_text}   ${sw_connection_host}
    [Teardown]  close connection to network element  dut1_telnet


Check Device Online
    [Documentation]     This keyword will check if devices are online

    ${online_sw2}=      Wait Until Device Online                    ${netelem1.serial}

    Should Be Equal As Integers                 ${online_sw2}       1

clear vlans
    [Documentation]     This keyword will delete vlan 3

    connect to network element  dut1_telnet  ${netelem1.ip}  ${netelem1.username}  ${netelem1.password}  telnet  ${netelem1.cli_type}
    send cmd   dut1_telnet      delete vlan 3

    [Teardown]  close connection to network element  dut1_telnet
