#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Dan McCarthy
# Description   : Test Suite for sanity testing of the XIQ-SE Configure Device view when "onboarding" a ZTP+ device.
#                 This is qTest TC-901 in the XIQ-SE project.

*** Settings ***
Library         xiqse/flows/common/XIQSE_CommonTable.py
Library         xiqse/flows/network/common/XIQSE_NetworkCommonConfigureDevice.py
Library         xiqse/flows/network/common/configure_device/XIQSE_NetworkCommonConfigureDeviceDevice.py
Library         xiqse/flows/network/common/configure_device/XIQSE_NetworkCommonConfigureDeviceImportSiteConfig.py
Library         xiqse/flows/network/common/configure_device/XIQSE_NetworkCommonConfigureDeviceZtpPlus.py
Library         xiqse/flows/network/discovered/XIQSE_NetworkDiscovered.py

Resource        ../../ZtpPlus/Resources/AllResources.robot

Force Tags      testbed_1_node

Suite Setup     Log Into XIQSE and Close Panels    ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
Suite Teardown  Log Out of XIQSE and Quit Browser


*** Variables ***
${ENV}                          environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                         topo.test.xiqse1.connected.yaml
${TESTBED}                      SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}                    ${xiqse.url}
${XIQSE_USER}                   ${xiqse.user}
${XIQSE_PASSWORD}               ${xiqse.password}

# Configure Device > ZTP+ Device Settings > Basic Management Example Values
${ZTP1_SERIAL}                  ${netelem1.serial}
${ZTP1_IP_SUBNET}               ${netelem1.ip}
${ZTP1_GATEWAY_ADDRESS}         10.10.9.1
${ZTP1_MANAGEMENT_INTERFACE}    Out-Of-Band
${ZTP1_CLI_RECOVERY_MODE_ONLY}  Disable
${ZTP1_DOMAIN_NAME}             ztp.org
${ZTP1_DNS_SERVER_1}            1.2.3.1
${ZTP1_DNS_SERVER_2}            1.2.3.2
${ZTP1_DNS_SERVER_3}            1.2.3.3
${ZTP1_DNS_SEARCH_SUFFIX}       extremenetworks.com
${ZTP1_NTP_SERVER_1}            2.2.2.1
${ZTP1_NTP_SERVER_2}            2.2.2.2

# Configure Device > ZTP+ Device Settings > Device Protocols Default Example Values
${ZTP1_TELNET}                  Enable
${ZTP1_SSH}                     Enable
${ZTP1_HTTP}                    Enable
${ZTP1_HTTPS}                   Enable
${ZTP1_FTP}                     Enable
${ZTP1_SNMP}                    Enable
${ZTP1_LACP}                    Disable
${ZTP1_LLDP}                    Enable
${ZTP1_MVRP}                    Enable
${ZTP1_MSTP}                    Enable
${ZTP1_POE}                     Enable
${ZTP1_VXLAN}                   Disable

# Configure Device > Device
${ZTP1_SYSTEM_NAME}             ${netelem1.name}
${ZTP1_SYSTEM_CONTACT}          AUTO LAB ADMIN
${ZTP1_SYSTEM_LOCATION}         AUTO HARDWARE LAB
${ZTP1_ADMIN_PROFILE}           ${netelem1.profile}
${ZTP1_DEFAULT_SITE}            /World
${ZTP1_IMPORT_SITE_CFG}         No
${ZTP1_SITE_PRECEDENCE}         None
${ZTP1_POLL_GROUP}              More Frequent
${ZTP1_POLL_TYPE}               ZTP+
${ZTP1_TOPO_LAYER}              L2 Access


*** Test Cases ***
Test 1: Configure Devices Dialog For Ztp Plus Device Use Discovered Disabled
    [Documentation]     Confirms that the Configure Device Dialog can be open and configured for a ZTP+ Device
    [Tags]              tcxe_901    xmc_4478    development     xiqse     ztp+    discovered_configure      test1

    Navigate To Network Discovered and Update Table

    Configure The ZTP+ Device

    ${action_result}=  XIQSE Configure Device Dialog Select Tab  ZTP+ Device Settings
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Configure Device Dialog Ztp Verify Serial Number  ${ZTP1_SERIAL}
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Configure Device Dialog Ztp Set Use Discovered  Disabled
    Should Be Equal As Integers         ${action_result}     1

    ZTP+ Configure Device Set ZTP+ Device Settings Basic Management Values

    ZTP+ Configure Device Set ZTP+ Device Settings Device Protocols Values

    ${action_result}=  XIQSE Configure Device Dialog Select Tab  Device
    Should Be Equal As Integers         ${action_result}     1

    ZTP+ Configure Device Set Device Values

    ${action_result}=  XIQSE Configure Device Dialog Click Cancel
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Refresh Table
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Discovered Get Device Column Value  ${ZTP1_SERIAL}  Status
    should be equal as strings          ${action_result}     ZTP+ Pending Edit

    [Teardown]    XIQSE Configure Device Dialog Click Cancel

Test 2: Configure Devices Dialog For Ztp Plus Device Use Discovered IP
    [Documentation]     Confirms that the Configure Device Dialog can be open and configured for a ZTP+ Device
    [Tags]              tcxe_901    xmc_4478    development     xiqse     ztp+    discovered_configure      test2

    Navigate To Network Discovered and Update Table

    ${action_result}=  XIQSE Discovered Open Configure Devices By Serial Number  ${ZTP1_SERIAL}
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Configure Device Dialog Select Tab  ZTP+ Device Settings
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Configure Device Dialog Ztp Verify Serial Number  ${ZTP1_SERIAL}
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Configure Device Dialog Ztp Set Use Discovered  IP
    Should Be Equal As Integers         ${action_result}     1

    ZTP+ Configure Device Set ZTP+ Device Settings Basic Management Values

    ZTP+ Configure Device Set ZTP+ Device Settings Device Protocols Values

    ${action_result}=  XIQSE Configure Device Dialog Select Tab  Device
    Should Be Equal As Integers         ${action_result}     1

    ZTP+ Configure Device Set Device Values

    ${action_result}=  XIQSE Configure Device Dialog Click Cancel
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Refresh Table
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Discovered Get Device Column Value  ${ZTP1_SERIAL}  Status
    Should Be Equal As Strings          ${action_result}     ZTP+ Pending Edit

    [Teardown]    XIQSE Configure Device Dialog Click Cancel

Test 3: Configure Devices Dialog For Ztp Plus Device Use Discovered IP And Management Interface
    [Documentation]     Confirms that the Configure Device Dialog can be open and configured for a ZTP+ Device
    [Tags]              tcxe_901    xmc_4478    development     xiqse     ztp+    discovered_configure      test3

    Navigate To Network Discovered and Update Table

    Configure The ZTP+ Device

    ${action_result}=  XIQSE Configure Device Dialog Select Tab  ZTP+ Device Settings
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Configure Device Dialog Ztp Verify Serial Number  ${ZTP1_SERIAL}
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Configure Device Dialog Ztp Set Use Discovered  IP and Management Interface
    Should Be Equal As Integers         ${action_result}     1

    ZTP+ Configure Device Set ZTP+ Device Settings Basic Management Values

    ZTP+ Configure Device Set ZTP+ Device Settings Device Protocols Values

    ${action_result}=  XIQSE Configure Device Dialog Select Tab  Device
    Should Be Equal As Integers         ${action_result}     1

    ZTP+ Configure Device Set Device Values

    ${action_result}=  XIQSE Configure Device Dialog Click Cancel
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Refresh Table
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Discovered Get Device Column Value  ${ZTP1_SERIAL}  Status
    Should Be Equal As Strings          ${action_result}     ZTP+ Pending Edit

    [Teardown]    XIQSE Configure Device Dialog Click Cancel

Test 4: Configure Devices Dialog For Ztp Plus Device Use Discovered Management Interface
    [Documentation]     Confirms that the Configure Device Dialog can be open and configured for a ZTP+ Device
    [Tags]              tcxe_901    xmc_4478    development     xiqse     ztp+    discovered_configure      test4

    Navigate To Network Discovered and Update Table

    ${action_result}=  XIQSE Discovered Open Configure Devices Menu By Serial Number   ${ZTP1_SERIAL}
    Should Be Equal As Integers         ${action_result}    1

    ${action_result}=  XIQSE Configure Device Dialog Select Tab  ZTP+ Device Settings
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Configure Device Dialog Ztp Verify Serial Number  ${ZTP1_SERIAL}
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Configure Device Dialog Ztp Set Use Discovered  Management Interface
    Should Be Equal As Integers         ${action_result}     1

    ZTP+ Configure Device Set ZTP+ Device Settings Basic Management Values

    ZTP+ Configure Device Set ZTP+ Device Settings Device Protocols Values

    ${action_result}=  XIQSE Configure Device Dialog Select Tab  Device
    Should Be Equal As Integers         ${action_result}     1

    ZTP+ Configure Device Set Device Values

    ${action_result}=  XIQSE Configure Device Dialog Click Cancel
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Refresh Table
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Discovered Get Device Column Value  ${ZTP1_SERIAL}  Status
    Should Be Equal As Strings          ${action_result}     ZTP+ Pending Edit

    [Teardown]    XIQSE Configure Device Dialog Click Cancel

*** Keywords ***
Navigate To Network Discovered And Update Table
    [Documentation]     Open the Network Discovered tab and update the table settings

    ${nav_result}=  XIQSE Navigate To Network Discovered Tab
    Should Be Equal As Integers         ${nav_result}     1

    ${action_result}=  XIQSE Discovered Do Not Show In Groups
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Refresh Table
    Should Be Equal As Integers         ${action_result}     1

Configure The ZTP+ Device
    [Documentation]     Open the Configure Device view for the selected ZTP+ Device.

    ${action_result}=  XIQSE Discovered Select Row By Serial Number        ${ZTP1_SERIAL}
    Should Be Equal As Integers         ${action_result}    1

    ${action_result}=  XIQSE Discovered Configure Devices Toolbar
    Should Be Equal As Integers         ${action_result}    1

ZTP+ Configure Device Set Device Values
    [Documentation]     OneView > Network > Discovered table > Configure Device > Device panel

    ${action_result}=  XIQSE Configure Device Dialog Set System Name       ${ZTP1_SYSTEM_NAME}
    Should Be Equal As Integers         ${action_result}      1

    ${action_result}=  XIQSE Configure Device Dialog Set Contact           ${ZTP1_SYSTEM_CONTACT}
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Configure Device Dialog Set Location          ${ZTP1_SYSTEM_LOCATION}
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Configure Device Dialog Set Admin Profile     ${ZTP1_ADMIN_PROFILE}
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Configure Device Dialog Set Poll Group        ${ZTP1_POLL_GROUP}
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Configure Device Dialog Set Poll Type         ${ZTP1_POLL_TYPE}
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Configure Device Dialog Set Default Site      ${ZTP1_DEFAULT_SITE}    import_site=${ZTP1_IMPORT_SITE_CFG}
    Should Be Equal As Integers         ${action_result}     1

    ${action_result}=  XIQSE Configure Device Dialog Set Topology Layer    ${ZTP1_TOPO_LAYER}
    Should Be Equal As Integers         ${action_result}     1

ZTP+ Configure Device Set ZTP+ Device Settings Basic Management Values
    [Documentation]     OneView > Network > Discovered table > Configure Device > ZTP+ Device Settings > Basic Management section

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set IP Address And Subnet             ${ZTP1_IP_SUBNET}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Gateway Address                   ${ZTP1_GATEWAY_ADDRESS}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Management Interface              ${ZTP1_MANAGEMENT_INTERFACE}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Cli Recovery Mode Only Checkbox   ${ZTP1_CLI_RECOVERY_MODE_ONLY}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Domain Name                       ${ZTP1_DOMAIN_NAME}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Dns Server                        ${ZTP1_DNS_SERVER_1}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Dns Server Two                    ${ZTP1_DNS_SERVER_2}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Dns Server Three                  ${ZTP1_DNS_SERVER_3}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Dns Search Suffix                 ${ZTP1_DNS_SEARCH_SUFFIX}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set ntp server                        ${ZTP1_NTP_SERVER_1}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Ntp Server Two                    ${ZTP1_NTP_SERVER_2}
    Should Be Equal As Integers         ${actions_result}     1

ZTP+ Configure Device Set ZTP+ Device Settings Device Protocols Values
    [Documentation]     OneView > Network > Discovered table > Configure Device > ZTP+ Device Settings > Device Protocols section

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Device Protocols Telnet Checkbox     ${ZTP1_TELNET}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Device Protocols Ssh Checkbox        ${ZTP1_SSH}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Device Protocols Http Checkbox       ${ZTP1_HTTP}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Device Protocols Https Checkbox      ${ZTP1_HTTPS}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Device Protocols Ftp Checkbox        ${ZTP1_FTP}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Device Protocols Snmp Checkbox       ${ZTP1_SNMP}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Device Protocols Lacp Checkbox       ${ZTP1_LACP}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Device Protocols Lldp Checkbox       ${ZTP1_LLDP}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Device Protocols Mvrp Checkbox       ${ZTP1_MVRP}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Device Protocols Mstp Checkbox       ${ZTP1_MSTP}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Device Protocols Poe Checkbox        ${ZTP1_POE}
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Configure Device Dialog Ztp Set Device Protocols Vxlan Checkbox      ${ZTP1_VXLAN}
    Should Be Equal As Integers         ${actions_result}     1
