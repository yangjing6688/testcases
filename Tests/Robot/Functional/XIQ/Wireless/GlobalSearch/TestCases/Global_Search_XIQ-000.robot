# Author        : Ramkumar
# Date          : May 7th 2020
# Description   : Global Search
# Host ----- Cloud

# Topology
# Client -----> AP --->XIQ Instance

# Execution Command:
# ------------------
# robot -L INFO -v DEVICE:AP630 -v TOPO:aio_137.120 global_seach.robot
# Select the Topology file based on Test bed
# Complte test will take "45 Minutes"

*** Variables ***
${AP_CATEGORY}              Device
${APPLICATION_CATEGORY}     Application
${APPLICATION_NAME1}        FACEBOOK APPS ${EMPTY}
${APPLICATION_RESULT}       FACEBOOK APPS
${APPLICATION_NAME2}        FTP ${EMPTY}
${APPLICATION_RESULT2}      FTP
${CLIENT_CATEGORY}          Client
${NETWORK_CATEGORY}         NetworkPolicy
${SEARCH_MAC}               mac
${SEARCH_HOST}              hostname
${SEARCH_IP}                IP
${SEARCH_SERIAL}            serial_number
${SSID}                     testssid

*** Settings ***
Resource      ../../GlobalSearch/Resources/AllResources.robot

Library	      Remote  http://${mu1.ip}:${mu1.port}    WITH NAME   Remote_Server

Force Tags    testbed_1_node

Suite Setup     Suite Setup
Suite Teardown  Run Keyword And Warn On Failure  Suite Teardown

*** Keywords ***
Suite Setup
    [Documentation]     Cleanup before running the suite
    [Tags]              development  cleanup

    Log To Console      CONFIGURING PRECONDITIONS AND CLEANUP BEFORE RUNNING THE SUITE!

    ${random_string}=         Get Random String   length=5

    ${device1_np_01}=         Catenate       ${random_string}_network_Policy
    ${device1_ssid_01}=       Catenate       ${random_string}_ssid

    Set Global Variable        ${device1_np_01}
    Set Global Variable        ${device1_ssid_01}


#    # Use this method to convert the ap, wing, netelem to a generic device object
#    # device1      => device1
#    # wing1    => device1
#    # netelem1 => device1 (EXOS/VOSS)
    Convert To Generic Device Object    device      index=1     look_for_device_type=ap     set_to_index=1
#
    # Create the connection to the device
    Base Test Suite Setup
    Set Global Variable     ${MAIN_DEVICE_SPAWN}            ${device1.name}

    ${simulated_device}=      Create Dictionary
    ...     name=simulated_dut08
    ...     model=AP460C
    ...     simulated_count=7
    ...     onboard_device_type=Simulated
    ...     location=auto_location_01, Santa Clara, building_02, floor_04

    ${LOGIN_RESULT}=            Login User                  ${tenant_username}      ${tenant_password}      check_warning_msg=True
    Should Be Equal As Integers     ${LOGIN_RESULT}         1

    ${ONBOARD_SIM_AP}=                  onboard device quick    ${simulated_device}
    Should Be Equal As Strings          ${ONBOARD_SIM_AP}       1

    ${SEARCH_RESULT}=           Search Device               device_serial=${device1.serial}     ignore_cli_feedback=true
    IF  ${SEARCH_RESULT} == 1
        ${DISCONNECT_DEVICE_RESULT}=    Disconnect Device From Cloud        ${device1.cli_type}      ${MAIN_DEVICE_SPAWN}
        Should Be Equal As Integers     ${DISCONNECT_DEVICE_RESULT}         1

        ${DELETE_DEVICE_RESULT}=        Delete Device                       device_serial=${device1.serial}
        Should Be Equal As Integers     ${DELETE_DEVICE_RESULT}             1
    END

    ${ONBOARD_RESULT}=      Onboard Device Quick        ${device1}
    Should Be Equal As Strings      ${ONBOARD_RESULT}       1

    ${CONF_RESULT}=         Configure Device To Connect To Cloud            ${device1.cli_type}     ${generic_capwap_url}   ${MAIN_DEVICE_SPAWN}
    Should Be Equal As Integers     ${CONF_RESULT}          1

    ${WAIT_CONF_RESULT}=    Wait For Configure Device To Connect To Cloud   ${device1.cli_type}     ${generic_capwap_url}   ${MAIN_DEVICE_SPAWN}
    Should Be Equal As Integers     ${WAIT_CONF_RESULT}     1

    ${ONLINE_STATUS}=       Wait Until Device Online    ${device1.serial}
    Should Be Equal As Integers     ${ONLINE_STATUS}        1

    ${MANAGED_STATUS}=      Wait Until Device Managed   ${device1.serial}
    Should Be Equal As Integers     ${MANAGED_STATUS}       1

    ${DEVICE_STATUS}=       Get Device Status           device_mac=${device1.mac}
    Should Contain Any              ${DEVICE_STATUS}    green   config audit mismatch

    ${POLICY_STATUS}=         Create Open Auth Express Network Policy         ${device1_np_01}            ${device1_ssid_01}
    Should Be Equal As Integers     ${LOGIN_RESULT}         1

    ${UPDATE_POLICY_TO_AP}=   Deploy Network Policy                   ${device1_np_01}                ${device1.serial}
    Should Be Equal As Integers     ${UPDATE_POLICY_TO_AP}         1

    Remote_Server.Disconnect WiFi

Suite Teardown
    [Documentation]     Cleanup after running the suite
    [Tags]              development  cleanup

    Log To Console      DOING CLEANUP AFTER RUNNING THE SUITE!

    ${SEARCH_RESULT}=   Search Device               device_serial=${device1.serial}     ignore_cli_feedback=true
    IF  ${SEARCH_RESULT} == 1
        ${DISCONNECT_DEVICE_RESULT}=    Disconnect Device From Cloud        ${device1.cli_type}     ${MAIN_DEVICE_SPAWN}
        Should Be Equal As Integers     ${DISCONNECT_DEVICE_RESULT}         1

        ${DELETE_DEVICE_RESULT}=        Delete Device                       device_serial=${device1.serial}
        Should Be Equal As Integers     ${DELETE_DEVICE_RESULT}             1
    END

    ${DELETE_DEVICES}=               Delete All Devices
    Should Be Equal As Integers     ${DELETE_DEVICES}                    1

    ${DELETE_NP}=               Delete Network Policy  ${device1_np_01}
    Should Be Equal As Integers     ${DELETE_NP}                    1

    ${DELETE_SSID}=               Delete SSIDs   ${device1_ssid_01}
    Should Be Equal As Integers     ${DELETE_SSID}                    1

    ${LOGOUT_RESULT}=               Logout User
    Should Be Equal As Integers     ${LOGOUT_RESULT}                    1

    ${QUIT_BROWSER_RESULT}=         Quit Browser
    Should Be Equal As Integers     ${QUIT_BROWSER_RESULT}              1

*** Test Cases ***
TCCS-7377:Verfiy Device MAC Can Be Searched From Global Search
    [Documentation]                         Verfiy Device MAC Can Be Searched From Global Search
    [Tags]                                  development  tccs-7377

    Navigate To Devices

    ${search_result1}=                      Global Search               ${device1.mac}              ${AP_CATEGORY}      ${device1.name}
    Should not Be Equal as strings          ${search_result1}           -1

    ${host_name_1}    ${serial_number_1}    ${device1_MAC_1}   ${IP_1}      Get AP Details          ${search_result1}
    Should Be Equal as strings              ${device1_MAC_1}                ${device1.mac}

    ${mac_lower}=                           Convert To Lower Case        ${device1.mac}
    ${search_result2}=                      Global Search               ${MAC_lower}            ${AP_CATEGORY}     ${device1.name}
    Should not Be Equal as strings          ${search_result2}           -1
    ${host_name_2}    ${serial_number_2}    ${device1_MAC_2}   ${IP_2}      Get AP Details          ${search_result2}
    Should Be Equal as strings              ${device1_MAC_2}                ${device1.mac}

    ${MAC_upper}=                           Convert To Upper Case        ${device1.mac}
    ${search_result3}=                      Global Search               ${MAC_upper}            ${AP_CATEGORY}     ${device1.name}
    Should not Be Equal as strings          ${search_result3}           -1
    ${host_name_3}    ${serial_number_3}    ${device1_MAC_3}   ${IP_3}      Get AP Details          ${search_result3}
    Should Be Equal as strings              ${device1_MAC_3}                ${device1.mac}

    ${MAC_randomcase}=                      Convert MAC To Random Case  ${device1.mac}
    ${search_result4}=                      Global Search               ${MAC_randomcase}       ${AP_CATEGORY}     ${device1.name}
    Should not Be Equal as strings          ${search_result4}           -1
    ${host_name_4}    ${serial_number_4}    ${device1_MAC_4}   ${IP_4}      Get AP Details          ${search_result4}
    Should Be Equal as strings              ${device1_MAC_4}                ${device1.mac}

    ${first_half}=                          Get First Half Of MAC       ${device1.mac}
    ${search_result5}=                      Global Search               ${first_half}           ${AP_CATEGORY}     ${device1.name}
    Should not Be Equal as strings          ${search_result5}           -1
    ${host_name_5}    ${serial_number_5}    ${device1_MAC_5}   ${IP_5}      Get AP Details          ${search_result5}
    Should Be Equal as strings              ${device1_MAC_5}                ${device1.mac}

    ${second_half}=                         Get Second Half Of MAC      ${device1.mac}
    ${search_result6}=                      Global Search               ${second_half}          ${AP_CATEGORY}     ${device1.name}
    Should not Be Equal as strings          ${search_result6}           -1
    ${host_name_6}    ${serial_number_6}    ${device1_MAC_6}   ${IP_6}      Get AP Details          ${search_result6}
    Should Be Equal as strings              ${device1_MAC_6}                ${device1.mac}

    ${last_6_digits}=                       Get Last 6 Digts Of MAC     ${device1.mac}
    ${search_result7}=                      Global Search               ${last_6_digits}        ${AP_CATEGORY}     ${device1.name}
    Should not Be Equal as strings          ${search_result7}           -1
    ${host_name_7}    ${serial_number_7}    ${device1_MAC_7}   ${IP_7}      Get AP Details          ${search_result7}
    Should Be Equal as strings              ${device1_MAC_7}                ${device1.mac}

TCCS-7223 :Verfiy Device Hostname Can Be Searched From Global Search
    [Documentation]                         Verfiy Device Hostname Can Be Searched From Global Search
    [Tags]                                  development      tccs-7223

    Navigate To Devices

    ${search_result1}=                      Global Search               ${device1.name}             ${AP_CATEGORY}
    Should not Be Equal as strings          ${search_result1}           -1
    ${host_name_1}    ${serial_number_1}    ${device1_MAC_1}   ${IP_1}      Get AP Details          ${search_result1}
    Should Be Equal as strings              ${host_name_1}              ${device1.name}

    ${name_part1}    ${name_part2}          ${name_part3}    Split String Into 3 Parts          ${device1.name}
    ${search_result2}=                      Global Search               ${name_part1}           ${AP_CATEGORY}      ${device1.name}
    Should not Be Equal as strings          ${search_result2}           -1
    ${host_name_2}    ${serial_number_2}    ${device1_MAC_2}   ${IP_2}      Get AP Details          ${search_result2}
    Should Be Equal as strings              ${host_name_2}              ${device1.name}

    ${search_result3}=                      Global Search               ${name_part2}           ${AP_CATEGORY}      ${device1.name}
    Should not Be Equal as strings          ${search_result3}           -1
    ${host_name_3}    ${serial_number_3}    ${device1_MAC_3}   ${IP_3}      Get AP Details          ${search_result3}
    Should Be Equal as strings              ${host_name_3}              ${device1.name}

    ${search_result4}=                      Global Search               ${name_part3}           ${AP_CATEGORY}      ${device1.name}
    Should not Be Equal as strings          ${search_result4}           -1
    ${host_name_4}    ${serial_number_4}    ${device1_MAC_4}   ${IP_4}      Get AP Details          ${search_result4}
    Should Be Equal as strings              ${host_name_4}              ${device1.name}

TCCS-7322: Verfiy device serial number can be searched from global search
    [Documentation]                         Verfiy device serial number can be searched from global search
    [Tags]                                  development   tccs-7322

    Navigate To Devices

    ${search_result1}=                      Global Search               ${device1.serial}           ${AP_CATEGORY}      ${device1.name}
    Should not Be Equal as strings          ${search_result1}           -1
    ${host_name_1}    ${serial_number_1}    ${device1_MAC_1}   ${IP_1}      Get AP Details          ${search_result1}
    Should Be Equal as strings              ${serial_number_1}          ${device1.serial}

    ${serial_part1}    ${serial_part2}      ${serial_part3}             split_string_into_3_parts     ${device1.serial}
    ${search_result2}=                      Global Search               ${serial_part1}         ${AP_CATEGORY}      ${device1.name}
    Should not Be Equal as strings          ${search_result2}           -1
    ${host_name_2}    ${serial_number_2}    ${device1_MAC_2}   ${IP_2}      Get AP Details          ${search_result2}
    Should Be Equal as strings              ${serial_number_2}          ${device1.serial}

    ${search_result3}=                      Global Search               ${serial_part2}         ${AP_CATEGORY}      ${device1.name}
    Should not Be Equal as strings          ${search_result3}           -1
    ${host_name_3}    ${serial_number_3}    ${device1_MAC_3}   ${IP_3}      Get AP Details          ${search_result3}
    Should Be Equal as strings              ${serial_number_3}          ${device1.serial}

    ${search_result4}=                      Global Search               ${serial_part3}         ${AP_CATEGORY}      ${device1.name}
    Should not Be Equal as strings          ${search_result4}           -1
    ${host_name_4}    ${serial_number_4}    ${device1_MAC_4}   ${IP_4}      Get AP Details          ${search_result4}
    Should Be Equal as strings              ${serial_number_4}          ${device1.serial}

TCCS-7275 :Verfiy ip address can be searched from global search
    [Documentation]                         Verfiy ip address can be searched from global search
    [Tags]                                  development   tccs-7275

    ${partial_IP}                           get_partial_ip                  ${device1.ip}
    ${search_result1}=                      Global Search               ${partial_IP}               ${AP_CATEGORY}      ${device1.name}
    Should not Be Equal as strings          ${search_result1}           -1
    ${host_name_1}    ${serial_number_1}    ${device1_MAC_1}   ${IP_1}      Get AP Details              ${search_result1}
    Should Be Equal as strings              ${IP_1}                     ${device1.ip}

    ${search_result2}=                      Global Search               ${device1.ip}                   ${AP_CATEGORY}      ${device1.name}
    Should not Be Equal as strings          ${search_result2}           -1
    ${host_name_2}    ${serial_number_2}    ${device1_MAC_2}   ${IP_2}      Get AP Details              ${search_result2}
    Should Be Equal as strings              ${IP_2}                     ${device1.ip}

TCCS-7262:Verfiy Network Policy Searched From Global Search
    [Documentation]                         Verfiy Network Policy Searched From Global Search
    [Tags]                                  development  tccs-7262

    ${net_policy_result1}=                  Global Search               ${device1_np_01}           ${NETWORK_CATEGORY}
    Should not Be Equal as strings          ${net_policy_result1}       -1

    ${NET_POLICY_NAME1}      ${NET_SSID1}   Net Policy Details          ${net_policy_result1}
    Should Be Equal as strings              ${NET_POLICY_NAME1}         ${device1_np_01}
    Should Be Equal as strings              ${NET_SSID1}                ${device1_ssid_01}

    ${net_policy_part1}                     get_first_half_of_name       ${device1_np_01}
    ${net_policy_result2}=                  Global Search               ${net_policy_part1}     ${NETWORK_CATEGORY}     ${device1_NP_01}
    Should not Be Equal as strings          ${net_policy_result2}       -1

    ${NET_POLICY_NAME2}      ${NET_SSID2}   Net Policy Details          ${net_policy_result2}
    Should Be Equal as strings              ${NET_POLICY_NAME2}         ${device1_np_01}
    Should Be Equal as strings              ${NET_SSID2}                ${device1_ssid_01}

    ${net_policy_part2}                     get_second_half_of_name     ${device1_np_01}
    ${net_policy_result3}=                  Global Search               ${net_policy_part2}     ${NETWORK_CATEGORY}     ${device1_NP_01}
    Should not Be Equal as strings          ${net_policy_result3}       -1

    ${NET_POLICY_NAME3}      ${NET_SSID3}   Net Policy Details          ${net_policy_result3}
    Should Be Equal as strings              ${NET_POLICY_NAME3}         ${device1_np_01}
    Should Be Equal as strings              ${NET_SSID3}                ${device1_ssid_01}


TCCS-7302:Verfiy client hostname can be searched from global search
    [Documentation]          Verfiy client hostname can be searched from global search
    [Tags]                   development  tccs-7302

    ${CONNECT_WIFI}=           Remote_Server.Connect Open Network      ${device1_ssid_01}
    Should Be Equal As Integers     ${CONNECT_WIFI}         1

    Log to Console      Sleep for ${CLIENT_CONNECT_WAIT}
    Sleep                         ${CLIENT_CONNECT_WAIT}
    ${search_mu_name_input}=                Catenate       ${mu1.hostname} ${EMPTY}

    ${search_result1}=                      Global Search               ${search_mu_name_input}     ${CLIENT_CATEGORY}   ${mu1.hostname}
    Should not Be Equal as strings          ${search_result1}           -1
    ${client_name1}    ${client_MAC1}       ${client_IP1}               Get Client Details      ${search_result1}
    Should Be Equal as strings              ${client_name1}             ${mu1.hostname}

    ${cli_part1}    ${cli_part2}            ${cli_part3}                split_string_into_3_parts   ${mu1.hostname}
    ${search_result2}=                      Global Search               ${cli_part1}            ${CLIENT_CATEGORY}      ${mu1.hostname}
    Should not Be Equal as strings          ${search_result2}           -1
    ${client_name2}    ${client_MAC2}       ${client_IP2}               Get Client Details      ${search_result2}
    Should Be Equal as strings              ${client_name2}             ${mu1.hostname}

    ${search_result3}=                      Global Search               ${cli_part2}            ${CLIENT_CATEGORY}      ${mu1.hostname}
    Should not Be Equal as strings          ${search_result3}           -1
    ${client_name3}    ${client_MAC3}       ${client_IP3}               Get Client Details      ${search_result3}
    Should Be Equal as strings              ${client_name3}             ${mu1.hostname}

    ${cli_part3}=                           Catenate       ${cli_part3} ${EMPTY}
    ${search_result4}=                      Global Search               ${cli_part3}            ${CLIENT_CATEGORY}      ${mu1.hostname}
    Should not Be Equal as strings          ${search_result4}           -1
    ${client_name4}    ${client_MAC4}       ${client_IP4}               Get Client Details      ${search_result4}
    Should Be Equal as strings              ${client_name4}             ${mu1.hostname}

TCCS-7329:Verfiy Client MAC Can Be Searched From Global Search
    [Documentation]                         Verfiy Client MAC Can Be Searched From Global Search
    [Tags]                                  development   tccs-7329

    ${search_result1}=                      Global Search               ${mu1.wifi_mac}          ${CLIENT_CATEGORY}      ${mu1.hostname}
    Should not Be Equal as strings          ${search_result1}           -1
    ${client_name1}    ${client_MAC1}       ${client_IP1}               Get Client Details      ${search_result1}
    Should Be Equal as strings              ${client_name1}              ${mu1.hostname}

    ${client_MAC_lower}=                    Convert To Lower Case        ${mu1.wifi_mac}
    ${search_result2}=                      Global Search               ${client_MAC_lower}     ${CLIENT_CATEGORY}      ${mu1.hostname}
    Should not Be Equal as strings          ${search_result2}           -1
    ${client_name2}    ${client_MAC2}       ${client_IP2}               Get Client Details      ${search_result2}
    Should Be Equal as strings              ${client_name2}              ${mu1.hostname}

    ${client_MAC_upper}=                    Convert To Upper Case        ${mu1.wifi_mac}
    ${search_result3}=                      Global Search               ${client_MAC_upper}     ${CLIENT_CATEGORY}      ${mu1.hostname}
    Should not Be Equal as strings          ${search_result3}           -1
    ${client_name3}    ${client_MAC3}       ${client_IP3}               Get Client Details      ${search_result3}
    Should Be Equal as strings              ${client_name3}              ${mu1.hostname}

    ${client_MAC_randomcase}=               Convert MAC To Random Case  ${mu1.wifi_mac}
    ${search_result4}=                      Global Search               ${client_MAC_randomcase}    ${CLIENT_CATEGORY}  ${mu1.hostname}
    Should not Be Equal as strings          ${search_result4}           -1
    ${client_name4}    ${client_MAC4}       ${client_IP4}               Get Client Details          ${search_result4}
    Should Be Equal as strings              ${client_name4}              ${mu1.hostname}

    ${client_first_half}=                   Get First Half Of MAC       ${mu1.wifi_mac}
    ${client_first_half}=                   Catenate       ${client_first_half} ${EMPTY}
    ${search_result5}=                      Global Search               ${client_first_half}        ${CLIENT_CATEGORY}   ${mu1.hostname}
    Should not Be Equal as strings          ${search_result5}           -1
    ${client_name5}    ${client_MAC5}       ${client_IP5}               Get Client Details          ${search_result5}
    Should Be Equal as strings              ${client_name5}              ${mu1.hostname}

    ${client_second_half}=                  Get Second Half Of MAC      ${mu1.wifi_mac}
    ${client_second_half}=                  Catenate       ${client_second_half} ${EMPTY}
    ${search_result6}=                      Global Search               ${client_second_half}      ${CLIENT_CATEGORY}    ${mu1.hostname}
    Should not Be Equal as strings          ${search_result6}           -1
    ${client_name6}    ${client_MAC6}       ${client_IP6}               Get Client Details          ${search_result6}
    Should Be Equal as strings              ${client_name6}              ${mu1.hostname}

    ${client_last_6_digits}=                Get Last 6 Digts Of MAC     ${mu1.wifi_mac}
    ${client_last_6_digits}=                Catenate       ${client_last_6_digits} ${EMPTY}
    ${search_result7}=                      Global Search               ${client_last_6_digits}     ${CLIENT_CATEGORY}  ${mu1.hostname}
    Should not Be Equal as strings          ${search_result7}           -1
    ${client_name7}    ${client_MAC7}       ${client_IP7}               Get Client Details          ${search_result7}
    Should Be Equal as strings              ${client_name7}              ${mu1.hostname}

TCCS-7288 :Verfiy Historical Clients Can Be Searched From Global Search
    [Documentation]                         Verfiy Historical Clients Can Be Searched From Global Search
    [Tags]                                  development     tccs-7288
    ${result_mu_removed}=                   Remote_Server.Disconnect WiFi
    ${search_mu_mac_input}=                 Catenate       ${mu1.hostname} ${EMPTY}
    Log to Console      Sleep for ${CLIENT_CONNECT_WAIT}
    Sleep                         ${CLIENT_CONNECT_WAIT}

    ${search_result1}=                      Global Search               ${search_mu_mac_input}        ${CLIENT_CATEGORY}   ${mu1.hostname}
    Should not Be Equal as strings          ${search_result1}           -1
    ${client_name1}    ${client_MAC1}       ${client_IP1}               Get Client Details      ${search_result1}
    Should Be Equal as strings              ${client_name1}             ${mu1.hostname}

    ${old_cli_part1}    ${old_cli_part2}    ${old_cli_part3}            split_string_into_3_parts      ${mu1.hostname}

    ${search_result2}=                      Global Search               ${old_cli_part1}        ${CLIENT_CATEGORY}      ${mu1.hostname}
    Should not Be Equal as strings          ${search_result2}           -1
    ${client_name2}    ${client_MAC2}       ${client_IP2}               Get Client Details      ${search_result2}
    Should Be Equal as strings              ${client_name2}             ${mu1.hostname}

    ${search_result3}=                      Global Search               ${old_cli_part2}        ${CLIENT_CATEGORY}      ${mu1.hostname}
    Should not Be Equal as strings          ${search_result3}           -1
    ${client_name3}    ${client_MAC3}       ${client_IP3}               Get Client Details      ${search_result3}
    Should Be Equal as strings              ${client_name3}             ${mu1.hostname}

    ${old_cli_part3}=                       Catenate       ${old_cli_part3} ${EMPTY}
    ${search_result4}=                      Global Search               ${old_cli_part3}        ${CLIENT_CATEGORY}      ${mu1.hostname}
    Should not Be Equal as strings          ${search_result4}           -1
    ${client_name4}    ${client_MAC4}       ${client_IP4}               Get Client Details      ${search_result4}
    Should Be Equal as strings              ${client_name4}             ${mu1.hostname}

    ${search_result5}=                      Global Search               ${search_mu_mac_input}         ${CLIENT_CATEGORY}      ${mu1.hostname}
    Should not Be Equal as strings          ${search_result5}           -1
    ${client_name5}    ${client_MAC5}       ${client_IP5}               Get Client Details      ${search_result5}
    Should Be Equal as strings              ${client_name5}             ${mu1.hostname}

TCCS-14475:Verfiy L7 Applications Searched From Global Search.
    [Documentation]                         Verfiy L7 Applications Searched From Global Search
    [Tags]                                  development   tccs-14475

    ${search_result1}=                      Global Search               ${APPLICATION_NAME1}    ${APPLICATION_CATEGORY}   ${APPLICATION_RESULT}
    Should not Be Equal as strings          ${search_result1}           -1
    ${app_name1}     ${app_category1}       Application Details         ${search_result1}
    Should Be Equal as strings              ${app_name1}                ${APPLICATION_RESULT}

    ${search_result2}=                      Global Search               ${APPLICATION_NAME2}    ${APPLICATION_CATEGORY}  ${APPLICATION_RESULT2}
    Should not Be Equal as strings          ${search_result2}           -1
    ${app_name2}     ${app_category2}       Application Details         ${search_result2}
    Should Be Equal as strings              ${app_name2}                ${APPLICATION_RESULT2}
