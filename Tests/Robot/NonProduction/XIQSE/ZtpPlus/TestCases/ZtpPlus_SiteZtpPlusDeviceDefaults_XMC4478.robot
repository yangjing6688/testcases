# ----------------------------------------------------------------------
# Copyright (C) 2021... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
# ----------------------------------------------------------------------
#
# Author        : Dan McCarthy
# Description   : Test Suite for sanity testing of the XIQ-SE Site > ZTP+ Device Defaults panel UI functionality.

*** Settings ***
Library         xiqse/flows/network/devices/site/ztp_device_defaults/XIQSE_NetworkDevicesSiteZtpDeviceDefaults.py

Resource        ../../ZtpPlus/Resources/AllResources.robot

Force Tags      testbed_0_node

Suite Setup     Log Into XIQSE and Close Panels    ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
Suite Teardown  Log Out of XIQSE and Quit Browser


*** Variables ***
${ENV}                           environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                          topo.test.xiqse1.connected.yaml
${TESTBED}                       SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}                     ${xiqse.url}
${XIQSE_USER}                    ${xiqse.user}
${XIQSE_PASSWORD}                ${xiqse.password}

# Basic Management Values
${SITE}                          World
${SITE_SUBNET_ADDRESS}           10.54.39.0/24
${SITE_STARTING_IP_ADDRESS}      10.54.39.90
${SITE_ENDING_IP_ADDRESS}        10.54.39.100
${SITE_GATEWAY_ADDRESS}          10.54.39.1
${SITE_MANAGEMENT_INTERFACE}     Default
${SITE_CLI_RECOVERY_MODE_ONLY}   Disable
${SITE_DOMAIN_NAME}              ztp.test.org
${SITE_DNS_SERVER_1}             10.1.5.11
${SITE_DNS_SERVER_2}             10.1.7.63
${SITE_DNS_SERVER_3}             10.1.7.82
${SITE_DNS_SEARCH_SUFFIX}        extremenetworks.com
${SITE_NTP_SERVER_1}             134.141.79.191
${SITE_NTP_SERVER_2}             134.141.79.190
${SITE_SYSTEM_CONTACT}           Lab Admin
${SITE_SYSTEM_LOCATION}          Hardware Lab
${SITE_ADMIN_PROFILE}            EXTR_v2_Profile
${SITE_POLL_GROUP}               More Frequent
${SITE_POLL_TYPE}                ZTP+
${SITE_PRECEDENCE}               None
# Device Protocols Default Values
${SITE_TELNET}                   Enable
${SITE_SSH}                      Enable
${SITE_HTTP}                     Enable
${SITE_HTTPS}                    Enable
${SITE_FTP}                      Enable
${SITE_SNMP}                     Enable
${SITE_LACP}                     Disable
${SITE_LLDP}                     Enable
${SITE_MVRP}                     Enable
${SITE_MSTP}                     Enable
${SITE_POE}                      Enable
${SITE_VXLAN}                    Disable


*** Test Cases ***
Test 1: Site ZTP Plus Configuration Use Discovered Disabled
    [Documentation]     Confirms the Site > ZTP+ Device Defaults panel can be successfully configured.
    [Tags]              xiqse_tc_902    xmc_4478    development     xiqse     ztp+    use_discovered    site_defaults   test1

    Navigate to Site and Select ZTP+ Device Defaults            ${SITE}

    ${actions_result}=  XIQSE Site Ztp Set Use Discovered       Disabled
    Should Be Equal As Integers         ${actions_result}       1

    Configure Site ZTP+ Device Defaults Basic Management Section

    ${actions_result}=  XIQSE Site ZTP Set Cli Recovery Mode Only Checkbox  Enable
    Should Be Equal As Integers         ${actions_result}       1

    Configure Site ZTP+ Device Defaults Disable All Device Protocols

    ${save_result}=  XIQSE Site Click Save
    Should Be Equal As Integers         ${save_result}          1

    XIQSE Devices Select Devices Tab

    [Teardown]    XIQSE Site Unsaved Changes Dialog             No

Test 2: Site ZTP Plus Configuration Use Discovered IP
    [Documentation]     Confirms the Site > ZTP+ Device Defaults panel can be successfully configured.
    [Tags]              xiqse_tc_902    xmc_4478    development     xiqse     ztp+    use_discovered    site_defaults   test2

    Navigate to Site and Select ZTP+ Device Defaults            ${SITE}

    ${actions_result}=  XIQSE Site Ztp Set Use Discovered       IP
    Should Be Equal As Integers         ${actions_result}       1

    Configure Site ZTP+ Device Defaults Basic Management Section

    ${actions_result}=  XIQSE Site ZTP Set Cli Recovery Mode Only Checkbox  Disable
    Should Be Equal As Integers         ${actions_result}       1

    Configure Site ZTP+ Device Defaults Enable All Device Protocols

    ${save_result}=  XIQSE Site Click Save
    Should Be Equal As Integers         ${save_result}          1

    XIQSE Devices Select Devices Tab

    [Teardown]    XIQSE Site Unsaved Changes Dialog             No

Test 3: Site ZTP Plus Configuration Use Discovered IP And Management Interface
    [Documentation]     Confirms the Site > ZTP+ Device Defaults panel can be successfully configured.
    [Tags]              xiqse_tc_902    xmc_4478    development     xiqse     ztp+    use_discovered    site_defaults   test3

    Navigate to Site and Select ZTP+ Device Defaults            ${SITE}

    ${actions_result}=  XIQSE Site Ztp Set Use Discovered       IP and Management Interface
    Should Be Equal As Integers         ${actions_result}       1

    Configure Site ZTP+ Device Defaults Basic Management Section

    ${actions_result}=  XIQSE Site ZTP Set Cli Recovery Mode Only Checkbox  Enable
    Should Be Equal As Integers         ${actions_result}       1

    Configure Site ZTP+ Device Defaults Disable All Device Protocols

    ${save_result}=  XIQSE Site Click Save
    Should Be Equal As Integers         ${save_result}          1

    XIQSE Devices Select Devices Tab

    [Teardown]    XIQSE Site Unsaved Changes Dialog             No

Test 4: Site ZTP Plus Configuration Use Discovered Management Interface
    [Documentation]     Confirms the Site > ZTP+ Device Defaults panel can be successfully configured.
    [Tags]              xiqse_tc_902    xmc_4478    development     xiqse     ztp+    use_discovered    site_defaults   test4

    Navigate to Site and Select ZTP+ Device Defaults            ${SITE}

    ${actions_result}=  XIQSE Site Ztp Set Use Discovered       Management Interface
    Should Be Equal As Integers         ${actions_result}       1

    Configure Site ZTP+ Device Defaults Basic Management Section

    ${actions_result}=  XIQSE Site ZTP Set Cli Recovery Mode Only Checkbox  Disable
    Should Be Equal As Integers         ${actions_result}       1

    Configure Site ZTP+ Device Defaults Enable ALl Device Protocols

    ${save_result}=  XIQSE Site Click Save
    Should Be Equal As Integers         ${save_result}          1

    XIQSE Devices Select Devices Tab

    [Teardown]    XIQSE Site Unsaved Changes Dialog             No

Test 5: Site ZTP Plus Configuration CLI Recovery Mode Only
    [Documentation]     Confirms the Site > ZTP+ Device Defaults > CLI Recovery Mode Only field is read-only when the Poll Type is set to SNMP.
    [Tags]              xiqse_tc_902    xmc_4478    development     xiqse     ztp+    cli_recoverey_mode    site_defaults   test5

    Navigate to Site and Select ZTP+ Device Defaults            ${SITE}

    ${actions_result}=  XIQSE Site Ztp Set Poll Type            SNMP
    Should Be Equal As Integers         ${actions_result}       1

    ${actions_result}=  XIQSE Site ZTP Set Cli Recovery Mode Only Checkbox  Disable
    Should Be Equal As Integers         ${actions_result}       2

    ${actions_result}=  XIQSE Site Ztp Set Poll Type            ZTP+
    Should Be Equal As Integers         ${actions_result}       1

    ${actions_result}=  XIQSE Site ZTP Set Cli Recovery Mode Only Checkbox  Disable
    Should Be Equal As Integers         ${actions_result}       1

    ${save_result}=  XIQSE Site Click Save
    Should Be Equal As Integers         ${save_result}          1

    XIQSE Devices Select Devices Tab

    [Teardown]    XIQSE Site Unsaved Changes Dialog             No

Test 6: Site ZTP Plus Configuration SNMP Device Protocol
    [Documentation]     Confirms the Site > ZTP+ Device Defaults > SNMP Device Protocol field is read-only when the Poll Type is set to SNMP.
    [Tags]              xiqse_tc_902    xmc_4478    development     xiqse     ztp+    snmp_device_protocol  site_defaults   test6

    Navigate to Site and Select ZTP+ Device Defaults            ${SITE}

    ${actions_result}=  XIQSE Site Ztp Set Poll Type            SNMP
    Should Be Equal As Integers         ${actions_result}       1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Snmp Checkbox  Disable
    Should Be Equal As Integers         ${actions_result}       2

    ${actions_result}=  XIQSE Site Ztp Set Poll Type            ZTP+
    Should Be Equal As Integers         ${actions_result}       1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Snmp Checkbox  Disable
    Should Be Equal As Integers         ${actions_result}       1

    ${save_result}=  XIQSE Site Click Save
    Should Be Equal As Integers         ${save_result}          1

    XIQSE Devices Select Devices Tab

    [Teardown]    XIQSE Site Unsaved Changes Dialog             No

Test 7: Site ZTP Plus Configuration Site Assignment Precedence
    [Documentation]     Confirms the Site > ZTP+ Device Defaults > Site Assignment Prcedence field is read-write for the World site.
    [Tags]              xiqse_tc_902    xmc_4478    development     xiqse     ztp+    site_assignment_precedence  site_defaults   test7

    Navigate to Site and Select ZTP+ Device Defaults            ${SITE}

    ${actions_result}=  XIQSE Site Ztp Set Site Precedence      IP Range, LLDP
    Should Be Equal As Integers                                 ${actions_result}   1

    ${save_result}=  XIQSE Site Click Save
    Should Be Equal As Integers                                 ${save_result}      1

    XIQSE Devices Select Devices Tab

    Navigate and Create Site                                    ZTP Plus Site

    Navigate to Site and Select ZTP+ Device Defaults            ZTP Plus Site

    ${actions_result}=  XIQSE Site Ztp Set Site Precedence      LLDP Only
    Should Be Equal As Integers                                 ${actions_result}   2

    XIQSE Site Ztp Toggle Section                               Configuration/Upgrade

    ${save_result}=  XIQSE Site Click Save
    Should Be Equal As Integers                                 ${save_result}      1

    Delete Site and Confirm Success                             ZTP Plus Site

    [Teardown]    XIQSE Site Unsaved Changes Dialog             No

Test 8: Site ZTP Plus Configuration Global IP to Site Mapping
    [Documentation]     Confirms the Site > ZTP+ Device Defaults > Global IP to Site Mapping field is read-write for the World site.
    [Tags]              xiqse_tc_902    xmc_4478    development     xiqse     ztp+    global_ip_to_site  site_defaults   test8

    Navigate to Site and Select ZTP+ Device Defaults            ${SITE}

    ${actions_result}=  XIQSE Site Ztp Global IP To Site Mapping State
    Should Be Equal As Integers                                 ${actions_result}   1

    ${save_result}=  XIQSE Site Click Save
    Should Be Equal As Integers                                 ${save_result}      1

    XIQSE Devices Select Devices Tab

    Navigate and Create Site                                    ZTP Plus Site

    Navigate to Site and Select ZTP+ Device Defaults            ZTP Plus Site

    XIQSE Site Ztp Toggle Section                               Basic Management

    XIQSE Site Ztp Toggle Section                               Device Protocols

    ${actions_result}=  XIQSE Site Ztp Global IP To Site Mapping State
    Should Be Equal As Integers                                 ${actions_result}   2

    XIQSE Site Ztp Toggle Section                               Basic Management

    ${save_result}=  XIQSE Site Click Save
    Should Be Equal As Integers                                 ${save_result}      1

    Delete Site and Confirm Success                             ZTP Plus Site

    [Teardown]    XIQSE Site Unsaved Changes Dialog             No


*** Keywords ***
Navigate to Site and Select ZTP+ Device Defaults
    [Documentation]     Navigate to the Site and select the ZTP+ Device Defaults tab
    [Arguments]         ${site}

    ${nav_result}=  XIQSE Navigate to Network Devices Tab
    Should Be Equal As Integers         ${nav_result}           1

    ${sel_tree}=  XIQSE Devices Select Site Tree Node           ${site}
    Should Be Equal As Integers         ${sel_tree}             1

    XIQSE Devices Select Devices Tab

    ${site_result}=  XIQSE Devices Select Site Tab              ${site}
    Should Be Equal As Integers         ${site_result}          1

    ${actions_result}=  XIQSE Site Select ZTP Device Defaults Tab
    Should Be Equal As Integers         ${actions_result}       1

Configure Site ZTP+ Device Defaults Basic Management Section
    [Documentation]     Configure the Site > ZTP+ Device Defaults > Basic Management section

    ${actions_result}=  XIQSE Site Ztp Set Subnet Address           ${SITE_SUBNET_ADDRESS}
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Starting IP Address      ${SITE_STARTING_IP_ADDRESS}
    Should Not Be Equal As Integers         ${actions_result}     -1

    ${actions_result}=  XIQSE Site Ztp Set Ending IP Address        ${SITE_ENDING_IP_ADDRESS}
    Should Not Be Equal As Integers         ${actions_result}     -1

    ${actions_result}=  XIQSE Site Ztp Set Gateway Address          ${SITE_GATEWAY_ADDRESS}
    Should Not Be Equal As Integers         ${actions_result}     -1

    ${actions_result}=  XIQSE Site Ztp Set Management Interface     ${SITE_MANAGEMENT_INTERFACE}
    Should Not Be Equal As Integers         ${actions_result}     -1

    ${actions_result}=  XIQSE Site Ztp Set Cli Recovery Mode Only Checkbox  ${SITE_CLI_RECOVERY_MODE_ONLY}
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Domain Name              ${SITE_DOMAIN_NAME}
    Should Not Be Equal As Integers         ${actions_result}     -1

    ${actions_result}=  XIQSE Site Ztp Set Dns Server               ${SITE_DNS_SERVER_1}
    Should Not Be Equal As Integers         ${actions_result}     -1

    ${actions_result}=  XIQSE Site Ztp Set Dns Server Two           ${SITE_DNS_SERVER_2}
    Should Not Be Equal As Integers         ${actions_result}     -1

    ${actions_result}=  XIQSE Site Ztp Set Dns Server Three         ${SITE_DNS_SERVER_3}
    Should Not Be Equal As Integers         ${actions_result}     -1

    ${actions_result}=  XIQSE Site Ztp Set Dns Search Suffix        ${SITE_DNS_SEARCH_SUFFIX}
    Should Not Be Equal As Integers         ${actions_result}     -1

    ${actions_result}=  xiqse site ztp set ntp server               ${SITE_NTP_SERVER_1}
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Ntp Server Two           ${SITE_NTP_SERVER_2}
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set System Contact           ${SITE_SYSTEM_CONTACT}
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set System Location          ${SITE_SYSTEM_LOCATION}
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Admin Profile            ${SITE_ADMIN_PROFILE}
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Poll Group               ${SITE_POLL_GROUP}
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Poll Type                ${SITE_POLL_TYPE}
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Site Precedence          ${SITE_PRECEDENCE}
    Should Not Be Equal As Integers         ${actions_result}     -1

Configure Site ZTP+ Device Defaults Enable All Device Protocols
    [Documentation]  Configure the Site > ZTP+ Device Defaults > Device Protocols section. Enable all options.

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Telnet Checkbox     Enable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Ssh Checkbox        Enable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Http Checkbox       Enable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Https Checkbox      Enable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Ftp Checkbox        Enable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Snmp Checkbox       Enable
    Should Not Be Equal As Integers         ${actions_result}     -1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Lacp Checkbox       Enable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Lldp Checkbox       Enable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Mvrp Checkbox       Enable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Mstp Checkbox       Enable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Poe Checkbox        Enable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Vxlan Checkbox      Enable
    Should Be Equal As Integers             ${actions_result}     1

Configure Site ZTP+ Device Defaults Disable All Device Protocols
    [Documentation]  Configure the Site > ZTP+ Device Defaults > Device Protocols section.  Disable all options.

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Telnet Checkbox     Disable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Ssh Checkbox        Disable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Http Checkbox       Disable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Https Checkbox      Disable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Ftp Checkbox        Disable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Snmp Checkbox       Disable
    Should Not Be Equal As Integers         ${actions_result}     -1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Lacp Checkbox       Disable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Lldp Checkbox       Disable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Mvrp Checkbox       Disable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Mstp Checkbox       Disable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Poe Checkbox        Disable
    Should Be Equal As Integers             ${actions_result}     1

    ${actions_result}=  XIQSE Site Ztp Set Device Protocols Vxlan Checkbox      Disable
    Should Be Equal As Integers             ${actions_result}     1
