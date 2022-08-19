#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE tab and sub tab navigation.
#                 This is qTest TC-105 in the XIQ-SE project.

*** Settings ***
Library         xiqse/flows/admin/XIQSE_Administration.py
Library         xiqse/flows/admin/device_types/XIQSE_AdminDeviceTypes.py
Library         xiqse/flows/admin/diagnostics/XIQSE_AdminDiagnostics.py
Library         xiqse/flows/admin/options/XIQSE_AdminOptions.py
Library         xiqse/flows/admin/profiles/XIQSE_AdminProfiles.py
Library         xiqse/flows/alarms_events/XIQSE_AlarmsEvents.py
Library         xiqse/flows/alarms_events/event_config/XIQSE_AlarmsEventsEventConfig.py
Library         xiqse/flows/analytics/XIQSE_Analytics.py
Library         xiqse/flows/common/XIQSE_CommonNavigator.py
Library         xiqse/flows/connect/XIQSE_Connect.py
Library         xiqse/flows/connect/configuration/XIQSE_ConnectConfiguration.py
Library         xiqse/flows/connect/diagnostics/XIQSE_ConnectDiagnostics.py
Library         xiqse/flows/control/XIQSE_Control.py
Library         xiqse/flows/network/XIQSE_Network.py
Library         xiqse/flows/network/devices/XIQSE_NetworkDevices.py
Library         xiqse/flows/network/devices/site/XIQSE_NetworkDevicesSite.py
Library         xiqse/flows/reports/XIQSE_Reports.py
Library         xiqse/flows/tasks/XIQSE_Tasks.py
Library         xiqse/flows/wireless/XIQSE_Wireless.py
Library         xiqse/flows/wireless/clients/XIQSE_WirelessClients.py
Library         xiqse/flows/wireless/threats/XIQSE_WirelessThreats.py

Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_0_node

Suite Setup     Log Into XIQSE and Close Panels  ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
Suite Teardown  Log Out of XIQSE and Quit Browser


*** Variables ***
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}


*** Test Cases ***
Test 1: Confirm Main Navigation Works
    [Documentation]     Confirms the main navigation works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test1

    ${connect_result}=  XIQSE Navigate to Connect Tab
    Should Be Equal As Integers    ${connect_result}    1

    ${admin_result}=  XIQSE Navigate to Administration Tab
    Should Be Equal As Integers    ${admin_result}    1

    ${tasks_result}=  XIQSE Navigate to Tasks Tab
    Should Be Equal As Integers    ${tasks_result}    1

    ${reports_result}=  XIQSE Navigate to Reports Tab
    Should Be Equal As Integers    ${reports_result}    1

    ${wireless_result}=  XIQSE Navigate to Wireless Tab
    Should Be Equal As Integers    ${wireless_result}    1

    ${analytics_result}=  XIQSE Navigate to Analytics Tab
    Should Be Equal As Integers    ${analytics_result}    1

    ${control_result}=  XIQSE Navigate to Control Tab
    Should Be Equal As Integers    ${control_result}    1

    ${ae_result}=  XIQSE Navigate to Alarms and Events Tab
    Should Be Equal As Integers    ${ae_result}    1

    ${network_result}=  XIQSE Navigate to Network Tab
    Should Be Equal As Integers    ${network_result}    1

Test 2: Confirm Network Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Network tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test2

    ${nav_result}=  XIQSE Navigate to Network Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${reports_result}=  XIQSE Network Select Reports Tab
    Should Be Equal As Integers    ${reports_result}    1

    ${config_result}=  XIQSE Network Select Configuration Templates Tab
    Should Be Equal As Integers    ${config_result}    1

    ${archives_result}=  XIQSE Network Select Archives Tab
    Should Be Equal As Integers    ${archives_result}    1

    ${fw_result}=  XIQSE Network Select Firmware Tab
    Should Be Equal As Integers    ${fw_result}    1

    ${disc_result}=  XIQSE Network Select Discovered Tab
    Should Be Equal As Integers    ${disc_result}    1

    ${devices_result}=  XIQSE Network Select Devices Tab
    Should Be Equal As Integers    ${devices_result}    1

    ${dashboard_result}=  XIQSE Network Select Dashboard Tab
    Should Be Equal As Integers    ${dashboard_result}    1

Test 3: Confirm Network Devices Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Network> Devices tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test3

    ${nav_result}=  XIQSE Navigate to Network Devices Tab
    Should Be Equal As Integers         ${nav_result}     1

    ${flex_result}=  XIQSE Devices Select FlexReports Tab
    Should Be Equal As Integers         ${flex_result}     1

    ${ep_result}=  XIQSE Devices Select Endpoint Locations Tab
    Should Be Equal As Integers         ${ep_result}     1

    ${summary_result}=  XIQSE Devices Select Site Summary Tab
    Should Be Equal As Integers         ${summary_result}     1

    ${site_result}=  XIQSE Devices Select Site Tab
    Should Be Equal As Integers         ${site_result}     1

    ${devices_result}=  XIQSE Devices Select Devices Tab
    Should Be Equal As Integers         ${devices_result}     1

Test 4: Confirm Network Devices Site Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Network> Devices> Site tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test4

    ${nav_result}=  XIQSE Navigate to Network Devices Tab
    Should Be Equal As Integers         ${nav_result}     1

    ${site_result}=  XIQSE Devices Select Site Tab
    Should Be Equal As Integers         ${site_result}     1

    ${actions_result}=  XIQSE Site Select Custom Variables Tab
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Site Select Analytics Tab
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Site Select Endpoint Locations Tab
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Site Select ZTP Device Defaults Tab
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Site Select Port Templates Tab
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Site Select Services Tab
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Site Select Topologies Tab
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Site Select VRF VLAN Tab
    Should Be Equal As Integers         ${actions_result}     1

    ${actions_result}=  XIQSE Site Select Actions Tab
    Should Be Equal As Integers         ${actions_result}     1

    ${disc_result}=  XIQSE Site Select Discover Tab
    Should Be Equal As Integers         ${disc_result}     1

Test 5: Confirm Alarm and Events Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Alarms & Events tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test5

    ${nav_result}=  XIQSE Navigate to Alarms and Events Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${ec_result}=  XIQSE AlarmsEvents Select Event Configuration Tab
    Should Be Equal As Integers    ${ec_result}    1

    ${events_result}=  XIQSE AlarmsEvents Select Events Tab
    Should Be Equal As Integers    ${events_result}    1

    ${ac_result}=  XIQSE AlarmsEvents Select Alarm Configuration Tab
    Should Be Equal As Integers    ${ac_result}    1

    ${alarms_result}=  XIQSE AlarmsEvents Select Alarms Tab
    Should Be Equal As Integers    ${alarms_result}    1

Test 6: Confirm Event Configuration Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Alarms & Events> Event Configuration tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test6

    ${nav_result}=  XIQSE Navigate to Event Configuration Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${patterns_result}=  XIQSE Event Configuration Select Event Patterns Tab
    Should Be Equal As Integers         ${patterns_result}     1

    ${logs_result}=  XIQSE Event Configuration Select Event Logs Tab
    Should Be Equal As Integers         ${logs_result}     1

Test 7: Confirm Control Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Control tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test7

    ${nav_result}=  XIQSE Navigate to Control Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${reports_result}=  XIQSE Control Select Reports Tab
    Should Be Equal As Integers    ${reports_result}    1

    ${es_result}=  XIQSE Control Select End Systems Tab
    Should Be Equal As Integers    ${es_result}    1

    ${ac_result}=  XIQSE Control Select Access Control Tab
    Should Be Equal As Integers    ${ac_result}    1

    ${policy_result}=  XIQSE Control Select Policy Tab
    Should Be Equal As Integers    ${policy_result}    1

    ${dashboard_result}=  XIQSE Control Select Dashboard Tab
    Should Be Equal As Integers    ${dashboard_result}    1

Test 8: Confirm Analytics Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Analytics tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test8

    ${nav_result}=  XIQSE Navigate to Analytics Tab
    Should Be Equal As Integers    ${nav_result}    1
    XIQSE Close Location Data Unavailable Message

    ${reports_result}=  XIQSE Analytics Select Reports Tab
    Should Be Equal As Integers    ${reports_result}    1

    ${config_result}=  XIQSE Analytics Select Configuration Tab
    Should Be Equal As Integers    ${config_result}    1

    ${pc_result}=  XIQSE Analytics Select Packet Captures Tab
    Should Be Equal As Integers    ${pc_result}    1

    ${fp_result}=  XIQSE Analytics Select Fingerprints Tab
    Should Be Equal As Integers    ${fp_result}    1

    ${flows_result}=  XIQSE Analytics Select Application Flows Tab
    Should Be Equal As Integers    ${flows_result}    1

    ${browser_result}=  XIQSE Analytics Select Browser Tab
    Should Be Equal As Integers    ${browser_result}    1
    XIQSE Close Location Data Unavailable Message

    ${dashboard_result}=  XIQSE Analytics Select Dashboard Tab
    Should Be Equal As Integers    ${dashboard_result}    1

Test 9: Confirm Wireless Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Wireless tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test9

    ${nav_result}=  XIQSE Navigate to Wireless Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${reports_result}=  XIQSE Wireless Select Reports Tab
    Should Be Equal As Integers    ${reports_result}    1

    ${threats_result}=  XIQSE Wireless Select Threats Tab
    Should Be Equal As Integers    ${threats_result}    1

    ${clients_result}=  XIQSE Wireless Select Clients Tab
    Should Be Equal As Integers    ${clients_result}    1

    ${ap_result}=  XIQSE Wireless Select Access Points Tab
    Should Be Equal As Integers    ${ap_result}    1

    ${controllers_result}=  XIQSE Wireless Select Controllers Tab
    Should Be Equal As Integers    ${controllers_result}    1

    ${network_result}=  XIQSE Wireless Select Network Tab
    Should Be Equal As Integers    ${network_result}    1

    ${dashboard_result}=  XIQSE Wireless Select Dashboard Tab
    Should Be Equal As Integers    ${dashboard_result}    1

Test 10: Confirm Wireless Client Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Wireless> Clients tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test10

    ${nav_result}=  XIQSE Navigate to Wireless Clients Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${analyzer_result}=  XIQSE Wireless Clients Select Event Analyzer Tab
    Should Be Equal As Integers         ${analyzer_result}     1
    XIQSE Wireless Clients Close Event Collection Disabled Dialog

    ${events_result}=  XIQSE Wireless Clients Select Client Events Tab
    Should Be Equal As Integers         ${events_result}     1
    XIQSE Wireless Clients Close Event Collection Disabled Dialog

    ${clients_result}=  XIQSE Wireless Clients Select Clients Tab
    Should Be Equal As Integers         ${clients_result}     1

Test 11: Confirm Wireless Threats Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Wireless> Threats tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test11

    ${nav_result}=  XIQSE Navigate to Wireless Threats Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${ie_result}=  XIQSE Wireless Threats Select Interference Events Tab
    Should Be Equal As Integers         ${ie_result}     1

    ${i_result}=  XIQSE Wireless Threats Select Interference Tab
    Should Be Equal As Integers         ${i_result}     1

    ${te_result}=  XIQSE Wireless Threats Select Threat Events Tab
    Should Be Equal As Integers         ${te_result}     1

    ${t_result}=  XIQSE Wireless Threats Select Threats Tab
    Should Be Equal As Integers         ${t_result}     1

Test 12: Confirm Reports Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Reports tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test12

    ${nav_result}=  XIQSE Navigate to Reports Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${designer_result}=  XIQSE Reports Select Report Designer Tab
    Should Be Equal As Integers    ${designer_result}    1
    XIQSE Close No Data Available Message

    ${custom_result}=  XIQSE Reports Select Custom Report Tab
    Should Be Equal As Integers    ${custom_result}    1
    XIQSE Close No Data Available Message

    ${reports_result}=  XIQSE Reports Select Reports Tab
    Should Be Equal As Integers    ${reports_result}    1

Test 13: Confirm Tasks Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Tasks tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test13

    ${nav_result}=  XIQSE Navigate to Tasks Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${wf_result}=  XIQSE Tasks Select Workflows Tab
    Should Be Equal As Integers    ${wf_result}    1

    ${scripts_result}=  XIQSE Tasks Select Scripts Tab
    Should Be Equal As Integers    ${scripts_result}    1

    ${saved_result}=  XIQSE Tasks Select Saved Tasks Tab
    Should Be Equal As Integers    ${saved_result}    1

    ${sched_result}=  XIQSE Tasks Select Scheduled Tasks Tab
    Should Be Equal As Integers    ${sched_result}    1

    ${dashboard_result}=  XIQSE Tasks Select Workflow Dashboard Tab
    Should Be Equal As Integers    ${dashboard_result}    1

Test 14: Confirm Administration Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Administration tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test14

    ${nav_result}=  XIQSE Navigate to Administration Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${api_result}=  XIQSE Admin Select Client API Access Tab
    Should Be Equal As Integers    ${api_result}    1

    ${diag_result}=  XIQSE Admin Select Diagnostics Tab
    Should Be Equal As Integers    ${diag_result}    1

    ${backup_result}=  XIQSE Admin Select Backup Restore Tab
    Should Be Equal As Integers    ${backup_result}    1

    ${dt_result}=  XIQSE Admin Select Device Types Tab
    Should Be Equal As Integers    ${dt_result}    1

    ${options_result}=  XIQSE Admin Select Options Tab
    Should Be Equal As Integers    ${options_result}    1

    ${cert_result}=  XIQSE Admin Select Certificates Tab
    Should Be Equal As Integers    ${cert_result}    1

    ${lic_result}=  XIQSE Admin Select Licenses Tab
    Should Be Equal As Integers    ${lic_result}    1

    ${server_result}=  XIQSE Admin Select Server Information Tab
    Should Be Equal As Integers    ${server_result}    1

    ${users_result}=  XIQSE Admin Select Users Tab
    Should Be Equal As Integers    ${users_result}    1

    ${profiles_result}=  XIQSE Admin Select Profiles Tab
    Should Be Equal As Integers    ${profiles_result}    1

Test 15: Confirm Profiles Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Administration> Profiles tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test15

    ${nav_result}=  XIQSE Navigate to Admin Profiles Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${mapping_result}=  XIQSE Profiles Select Device Mapping Tab
    Should Be Equal As Integers         ${mapping_result}     1

    ${cli_result}=  XIQSE Profiles Select CLI Credentials Tab
    Should Be Equal As Integers         ${cli_result}     1

    ${snmp_result}=  XIQSE Profiles Select SNMP Credentials Tab
    Should Be Equal As Integers         ${snmp_result}     1

Test 16: Confirm Device Types Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Administration> Device Types tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test16

    ${nav_result}=  XIQSE Navigate to Admin Device Types Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${mac_result}=  XIQSE Device Types Select MAC OUI Vendors Tab
    Should Be Equal As Integers         ${mac_result}     1

    ${dp_result}=  XIQSE Device Types Select Detection and Profiling Tab
    Should Be Equal As Integers         ${dp_result}     1

Test 17: Confirm Connect Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Connect tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test17

    ${nav_result}=  XIQSE Navigate to Connect Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${services_result}=  XIQSE Connect Select Services API Tab
    Should Be Equal As Integers    ${services_result}    1

    ${diag_result}=  XIQSE Connect Select Diagnostics Tab
    Should Be Equal As Integers    ${diag_result}    1

    ${config_result}=  XIQSE Connect Select Configuration Tab
    Should Be Equal As Integers    ${config_result}    1

Test 18: Confirm Connect Configuration Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Connect> Configuration tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test18

    ${nav_result}=  XIQSE Navigate to Connect Configuration Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${opt_result}=  XIQSE Connect Configuration Select Options Tab
    Should Be Equal As Integers         ${opt_result}     1

    ${serv_result}=  XIQSE Connect Configuration Select Services Tab
    Should Be Equal As Integers         ${serv_result}     1

Test 19: Confirm Connect Diagnostics Tab Navigation Works
    [Documentation]     Confirms navigation to the sub tabs of the Connect> Diagnostics tab works
    [Tags]              tcxe_105    aiq_1332    development    sample    xiqse    tab_nav    test19

    ${nav_result}=  XIQSE Navigate to Connect Diagnostics Tab
    Should Be Equal As Integers    ${nav_result}    1

    ${stat_result}=  XIQSE Connect Diagnostics Select Statistics Tab
    Should Be Equal As Integers         ${stat_result}     1

    ${esg_result}=  XIQSE Connect Diagnostics Select End System Groups Tab
    Should Be Equal As Integers         ${esg_result}     1

    ${es_result}=  XIQSE Connect Diagnostics Select End Systems Tab
    Should Be Equal As Integers         ${es_result}     1
