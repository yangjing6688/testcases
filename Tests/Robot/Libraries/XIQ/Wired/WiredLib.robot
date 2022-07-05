# Author        : Senthilkumar Karuppasamy
# Description   : Common library for all the robot functions

*** Settings ***
Resource     WiredCommon.robot


*** Variables ***
${LOCATION}                 ${netelem1.mac},Chennai,F1


*** Keywords ***

Configure IQagent EXOS
    [Documentation]     Configures the EXOS Iqagent

    log to console          "Executed the exos IQAgent configuration"
    connect to network element  dut1_telnet  ${netelem1.console_ip}  ${netelem1.username}  ${netelem1.password}  telnet  ${netelem1.cli_type}  ${netelem1.console_port}
    send cmd  dut1_telnet   disable iqagent
    send cmd  dut1_telnet   disable cli prompting
    send cmd  dut1_telnet   configure iqagent server vr VR-Mgmt
    send cmd  dut1_telnet   configure iqagent server ipaddress ${sw_connection_host}
    ${check_results}=  send cmd  dut1_telnet   show iqagent
    log   ${check_results[0].cmd_obj._return_text}
    log to console      ${check_results[0].cmd_obj._return_text}
    Should Contain   ${check_results[0].cmd_obj._return_text}   ${sw_connection_host}
    send cmd  dut1_telnet   enable iqagent
    send cmd  dut1_telnet   restart process iqagent
    Sleep   45s
    close connection to network element  dut1_telnet

Configure IQagent VOSS
    [Documentation]     Configures the VOSS IQAgent

    log to console          "Executed the voss Iqagent configuration"
    connect to network element  dut1_telnet  ${netelem1.ip}  ${netelem1.username}  ${netelem1.password}  telnet  ${netelem1.cli_type} 
    send cmd  dut1_telnet   enable
    send cmd  dut1_telnet   configure terminal
    send cmd  dut1_telnet   application
    send cmd  dut1_telnet   no iqagent ena
    send cmd  dut1_telnet   no iqagent server
    send cmd  dut1_telnet   iqagent server ${sw_connection_host}
    send cmd  dut1_telnet   iqagent ena
    ${check_results}=  send cmd  dut1_telnet   show application iqagent
    log   ${check_results[0].cmd_obj._return_text}
    log to console      ${check_results[0].cmd_obj._return_text}
    Should Contain   ${check_results[0].cmd_obj._return_text}   ${sw_connection_host}
    close connection to network element  dut1_telnet

Log Into XIQ and Set Up Test
    [Documentation]     Logs into XIQ and sets up the elements necessary to complete this test suite

    Log Into XIQ and Confirm Success
    
    Create Org

Create Org
    [Documentation]      Creates the required org for the device serial

    ${randomstring}     Generate Random String

    ${location}=        Set variable             ${netelem1.mac}_${randomstring}
    ${building}=        Set variable             building_${randomstring}
    ${floor}=           Set variable               floor_${randomstring}

    set global variable     ${location}
    set global variable     ${building}
    set global variable     ${floor}

    create_first_organization       Extreme       broadway        new york     Romania

    delete_location_building_floor              ${location}      ${building}    ${floor}
    create_location_building_floor              ${location}      ${building}    ${floor}
 


Log Into XIQ and Confirm Success
    [Documentation]     Logs into XIQ and confirms the login was successful

    ${result}=      Login User      ${tenant_username}     ${tenant_password}
    Should Be Equal As Integers     ${result}     1


Clean Up Test Device and Confirm Success
    [Documentation]     Deletes the specified device and confirms the action was successful
    [Arguments]         ${serial}

    Navigate to Devices and Confirm Success

    RUN KEYWORD IF  '${netelem1.platform}' == 'Stack'  Delete Device   device_mac=${netelem1.mac}

    @{result} =    Split String    ${netelem1.serial}    ,
    FOR         ${serialnumber}     IN    @{result}
                Delete Device       device_serial=${serialnumber}
    END

    ${del_result}=  Delete Device   ${serial}

Navigate to Devices and Confirm Success
    [Documentation]     Navigates to the Manage> Devices view and confirms the action was successful

    ${nav_result}=  Navigate to Devices
    Should Be Equal As Integers  ${nav_result}  1


Log Out of XIQ and Confirm Success
    [Documentation]     Logs out of XIQ and confirms the logout was successful

    ${result}=      Logout User
    Should Be Equal As Integers     ${result}     1

Tear Down Test and Close Session
    [Documentation]     Cleans up test data, logs out of XIQ, closes the browser, and resets the NOS version


    Clean Up Test Device and Confirm Success    ${netelem1.serial}

    delete_location_building_floor              ${location}         ${building}     ${floor}

    RUN KEYWORD IF  '${netelem1.cli_type}' == 'exos'  Cleanup IQagent EXOS
    RUN KEYWORD IF  '${netelem1.cli_type}' == 'voss'  Cleanup IQagent VOSS


    Log Out of XIQ and Confirm Success
    Quit Browser


Cleanup IQagent EXOS
    [Documentation]     Unconfigures the EXOS Iqagent

    log to console          "Executing the exos IQAgent Cleanup"
    connect to network element  dut1_telnet  ${netelem1.console_ip}  ${netelem1.username}  ${netelem1.password}  telnet  ${netelem1.cli_type}  ${netelem1.console_port}
    send cmd  dut1_telnet   disable cli prompting
    send cmd  dut1_telnet   configure iqagent server ipaddress none
    ${check_results}=  send cmd  dut1_telnet   show iqagent
    log   ${check_results[0].cmd_obj._return_text}
    log to console      ${check_results[0].cmd_obj._return_text}
    close connection to network element  dut1_telnet

Cleanup IQagent VOSS
    [Documentation]     Unconfigures the VOSS IQAgent

    log to console          "Executing  the voss Iqagent Cleanup"
    connect to network element  dut1_telnet  ${netelem1.ip}  ${netelem1.username}  ${netelem1.password}  telnet  ${netelem1.cli_type}
    send cmd  dut1_telnet   enable
    send cmd  dut1_telnet   configure terminal
    send cmd  dut1_telnet   application
    send cmd  dut1_telnet   no iqagent ena
    send cmd  dut1_telnet   no iqagent server
    ${check_results}=  send cmd  dut1_telnet   show application iqagent
    log   ${check_results[0].cmd_obj._return_text}
    log to console      ${check_results[0].cmd_obj._return_text}
    close connection to network element  dut1_telnet


