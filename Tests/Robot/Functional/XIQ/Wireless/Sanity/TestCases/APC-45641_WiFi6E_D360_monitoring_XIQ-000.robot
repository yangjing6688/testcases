# Author        : Pranav Chauhan & Binh Nguyen
# Date          : March 14 2023
# Description   : Device 360 monitoring testcases for Ap4000 - APC-45641 [XIQ Mainline > Releases > 2021-Q3r2 > APC-44209 WiFi 6E Support > APC-45641_WiFi6E_D360_monitoring
# https://aerohive.qtestnet.com/p/101323/portal/project#tab=testdesign&object=0&id=11145012
# https://aerohive.qtestnet.com/p/101323/portal/project#tab=testdesign&object=0&id=11145012

# Pre-Condtion
# 1. AP4000 should be onboarded and online. Connected with one wifi 6e client.
# 2. There should be only Wifi6E client connected to XIQ account, there should not be client connected to 2.4G/5G radio.

*** Settings ***
Library     String
Library     Collections
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py
Library     extauto/xiq/flows/manage/Device360.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/device_commands.yaml

Force Tags       testbed_none
Suite Setup      Pre_condition
Suite Teardown   Post_condition

*** Variables ***
${Expected_Clients}     2
${Clients}              1

${retry}                3

*** Keywords ***
Pre Condition
    [Documentation]   AP Should be onboarded  and it is online. One wifi 6e client should be connetced on this AP.
    log to console                      Wait for 10 minutes for Device 360 connection update . . .
    sleep                               10m
    ${STATUS}                           Login User    ${tenant_username}   ${tenant_password}
    should be equal as strings          '${STATUS}'   '1'

Post_condition
    Logout User
    Quit Browser

*** Test Cases ***
TCXM-11490:APC-45641_func_Overview_ConnectedClientsBar
    [Documentation]  Find connetced clients count from D360 overview page
    [Tags]      tcxm-11490     p1    px    regression

    &{OVERVIEW_GET}    create dictionary     connected_clients=get
    &{MONITOR_GET}     create dictionary     overview=&{OVERVIEW_GET}
    &{D360_INFO_GET}   create dictionary     monitor=&{MONITOR_GET}

    FOR    ${i}    IN RANGE    ${retry}
        ${OUTP}      D360 Get Info   ${ap1.mac}    ${D360_INFO_GET}
        exit for loop if         '${OUTP}[monitor][overview][connected_clients]' == '${Expected_Clients}'
        log to console           Wait for 3 minutes
        sleep                    3m
    END
    Should Be Equal As Strings   '${OUTP}[monitor][overview][connected_clients]'    '${Expected_Clients}'

TCXM-8816:APC-45641_func_SystemInformation
    [Documentation]  Verify the system information in d360 page
    [Tags]      tcxm-8816     p2     px     regression
    &{SYSTEM_INFORMATION_GET}    create dictionary     host_name=get           network_policy=get      ssid=get                    device_model=get
    ...                                                function=get            device_template=get     configuration_type=get      serial_number=get
    ...                                                iq_engine=get           device_status=get       mgt0_ipv4_address=get       mgt0_ipv6_address=get
    ...                                                ipv6_subnet_mask=get    ipv4_subnet_mask=get    ipv4_default_gateway=get    ipv6_default_gateway=get
    ...                                                mgt0_mac_address=get    dns=get                 ntp=get
    &{MONITOR_GET}               create dictionary     system_information=&{SYSTEM_INFORMATION_GET}
    &{D360_INFO_GET}             create dictionary     monitor=&{MONITOR_GET}

    ${OUTP}      D360 Get Info    ${ap1.mac}                                                 ${D360_INFO_GET}
    Should Be Equal As Strings    ${OUTP}[monitor][system_information][host_name]            ${ap1.name}
    Should Be Equal As Strings    ${OUTP}[monitor][system_information][device_model]         ${ap1.model}
    Should Be Equal As Strings    ${OUTP}[monitor][system_information][mgt0_ipv4_address]    ${ap1.ip}

TCXM-8812:APC-45641_func_WirelessInterface_TotalClients
    [Documentation]  Find total clinet information from wireless d360
    [Tags]      tcxm-8812     p3     px     regression
    &{WIRELESS_INTERFACES_GET}    create dictionary     total_clients=get
    &{MONITOR_GET}                create dictionary     wireless_interfaces=&{WIRELESS_INTERFACES_GET}
    &{D360_INFO_GET}              create dictionary     monitor=&{MONITOR_GET}

    ${OUTP}      D360 Get Info    ${ap1.mac}            ${D360_INFO_GET}
    Should Be Equal As Strings    '${OUTP}[monitor][wireless_interfaces][total_clients]'   '${Expected_Clients}'

TCXM-11486:APC-45641_func_WirelessInterface_6GScores_CombinedScores
    [Documentation]  Verify the combined score and wifi 6g score from wireless interface page.
    ...              This test requies only wifi 6e connected on environment, client should not connect to 2.4G/5G radio.
    [Tags]      tcxm-11486     p4     px     regression
    &{WIFI_HEALTH_COMBINED}       create dictionary     overall_score=get
    &{WIFI_HEALTH_6GHZ}           create dictionary     overall_score=get
    &{WIRELESS_INTERFACES_GET}    create dictionary     wifi_health_combined=&{WIFI_HEALTH_COMBINED}        wifi_health_6ghz=&{WIFI_HEALTH_6GHZ}
    &{MONITOR_GET}                create dictionary     wireless_interfaces=&{WIRELESS_INTERFACES_GET}
    &{D360_INFO_GET}              create dictionary     monitor=&{MONITOR_GET}

    ${OUTP}     D360 Get Info     ${ap1.mac}             ${D360_INFO_GET}
    Should Be Equal               ${OUTP}[monitor][wireless_interfaces][wifi_health_combined][overall_score]   ${OUTP}[monitor][wireless_interfaces][wifi_health_6ghz][overall_score]

TCXM-11488:APC-45641_func_WirelessInterface_Wifi2widget
    [Documentation]  Verify the connetced client information in wifi2 widget from d360
    [Tags]      tcxm-11488     p5    px     regression
    &{WIFI2_GET}                  create dictionary     my_clients=get
    &{WIRELESS_INTERFACES_GET}    create dictionary     wifi2=&{WIFI2_GET}
    &{MONITOR_GET}                create dictionary     wireless_interfaces=&{WIRELESS_INTERFACES_GET}
    &{D360_INFO_GET}              create dictionary     monitor=&{MONITOR_GET}

    FOR    ${i}    IN RANGE    ${retry}
        ${OUTP}      D360 Get Info   ${ap1.mac}    ${D360_INFO_GET}
        exit for loop if         '${OUTP}[monitor][wireless_interfaces][wifi2][my_clients]' == '${Clients}'
        log to console           Wait for 3 minutes
        sleep                    3m
    END
    Should Be Equal As Strings   '${OUTP}[monitor][wireless_interfaces][wifi2][my_clients]'    '${Clients}'

TCXM-8832:APC-45641_func_VerifyD360_Clients_GridDisplay
    [Documentation]  Verify the wifi 6e client details displayed as grid in clients page from d360
    [Tags]      tcxm-8832    p6     px     regression
    &{CLIENT_GET}                 create dictionary     client_mac=${mu1.wifi_mac}     current_connect_status=get
    &{MONITOR_GET}                create dictionary     clients=&{CLIENT_GET}
    &{D360_INFO_GET}              create dictionary     monitor=&{MONITOR_GET}

    ${OUTP}     D360 Get Info     ${ap1.mac}            ${D360_INFO_GET}
    Should Be Equal As Strings    '${OUTP}[monitor][clients][current_connect_status]'   'CONNECTED'

TCXM-8834:APC-45641_func_VerifyD360_Clients_TotalClientsInfo
    [Documentation]  Verify the total clients information on overview d360
    [Tags]      tcxm-8834     p7     px     regression
    &{CLIENT_GET}                 create dictionary     total_clients=get
    &{MONITOR_GET}                create dictionary     clients=&{CLIENT_GET}
    &{D360_INFO_GET}              create dictionary     monitor=&{MONITOR_GET}

    ${OUTP}     D360 Get Info     ${ap1.mac}            ${D360_INFO_GET}
    Should Be Equal As Strings    '${OUTP}[monitor][clients][total_clients]'   '${Clients}'

TCXM-8833:APC-45641_func_VerifyD360_UniqueClientsLeftpane
    [Documentation]  Verify the unique client information on left pane d360 page
    [Tags]      tcxm-8833     p8    px     regression
    &{D360_INFO_GET}              create dictionary     unique_clients=get

    ${OUTP}     D360 Get Info     ${ap1.mac}            ${D360_INFO_GET}
    Should Be Equal As Strings    '${OUTP}[unique_clients]'   '${Clients}'
