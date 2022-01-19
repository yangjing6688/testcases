# Author        : Ramkumar
# Date          : September 23th 2020
# Description   : Link/Unlink A3 instances to Cloud
#
# Topology      :
# A3 -->A3 Instances

# Pre-Condtion
#===============
# 1. Should have A3 Instances Ready to Link/Unlink to Cloud

# Execution Command:
# ------------------
# robot -L INFO -v TEST_URL:https://extremecloudiq.com/ -v TOPO:production -v OS_PLATFORM:windows10 -v BROWSER:chrome  a3_linking_on_cloud.robot

*** Variables ***
${EXIT_LEVEL}               test_suite
${CURL_CODE_SUCCESS}        {"code": "ok"}
${A3_PAGE_TITLE}            Administrator - A3
${UNLINK_A3_PAGE_TEXT}      You do not have any A3 instances connected to your account.
${CLOUD_GDC_URL}            https://cloud.aerohive.com

*** Settings ***
Library     Collections
Library     common/Utils.py
Library     common/Cli.py
Library     common/TestFlow.py

Library     xiq/flows/common/Login.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/common/MuCaptivePortal.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/WirelessNetworks.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/flows/configure/UserGroups.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/manage/Client.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/a3/A3Inventory.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/device_commands.yaml

Suite Setup      Pre Condition

*** Keywords ***
Pre Condition
    [Documentation]   Enable the SSH Access on A3 Node
    ${ENABLE_SSH_ON_A3NODE}=      Run Keyword If   '${${a3_version}.version}'=='3.2'  Enable SSH Access On A3 Node     ${${a3_version}.node1_ip}  ${${a3_version}.ui_username}   ${${a3_version}.ui_password}    ${${a3_version}.console_password}    7
    Run Keyword If  '${${a3_version}.version}'=='3.2'      should be equal as strings    '${ENABLE_SSH_ON_A3NODE}'   '1'

*** Test Cases ***
Test1 : Link A3 Cluster To XIQ
    [Documentation]    Link A3 Cluster To XIQ Using A3 Virtual IP
    [Tags]      sanity   A3  Link  unlink  P1  regression  production   Test1
    log to console              ${a3_version}
    log to console              ${${a3_version}.ip}
    ${A3_NODE_SPAWN}=          Open Paramiko SSH Spawn    ${${a3_version}.node1_ip}   ${${a3_version}.console_username}    ${${a3_version}.console_password}  ${${a3_version}.console_port}
    Log to Console      ${tenant_username}
    Log to Console      ${tenant_password}
    ${LINK_A3}=                 Link A3 Nodes To XIQ    ${A3_NODE_SPAWN}   ${tenant_username}   ${tenant_password}  url=${CLOUD_GDC_URL}
    should be equal as strings    '${LINK_A3}'   '${CURL_CODE_SUCCESS}'

Test2 : Verify A3 Cluster Node and Virtual IP Status
    [Documentation]    Verify A3 Cluster Node and Virtual IP Status
    [Tags]      sanity   A3  Link  unlink  P1  regression   production

    Depends On          Test1
    ${LOGIN_XIQ}=                  Login User          ${tenant_username}      ${tenant_password}
    ${A3_SERVER_STATUS}=           Get A3 Server Status   ${${a3_version}.ip}
    should be equal as strings    '${A3_SERVER_STATUS}'   'green'

    ${A3_NODE1_STATUS}=             Get A3 Node Status   ${${a3_version}.ip}  ${${a3_version}.node1_hostname}
    should be equal as strings    '${A3_NODE1_STATUS}'   'green'
    ${A3_NODE2_STATUS}=             Get A3 Node Status   ${${a3_version}.ip}  ${${a3_version}.node2_hostname}
    should be equal as strings    '${A3_NODE2_STATUS}'   'green'
    ${A3_NODE3_STATUS}=             Get A3 Node Status   ${${a3_version}.ip}  ${${a3_version}.node3_hostname}
    should be equal as strings    '${A3_NODE3_STATUS}'   'green'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test3 : Verify A3 Virtual IP Access From XIQ
    [Documentation]    Verify A3 Virtual IP Access From XIQ
    [Tags]      sanity   A3  Link  unlink  P1  regression  production

    Depends On          Test1
    ${LOGIN_XIQ}=                  Login User          ${tenant_username}      ${tenant_password}
    ${A3_SERVER_STATUS}=           Verify A3 Server Login On XIQ   ${${a3_version}.ip}   ${${a3_version}.ui_username}  ${${a3_version}.ui_password}
    should be equal as strings    '${A3_SERVER_STATUS}'   '${A3_PAGE_TITLE}'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser

Test4 : UnLink A3 Cluster To XIQ
    [Documentation]    UnLink A3 Cluster To XIQ
    [Tags]      sanity   A3  Link  unlink  P1  regression  production

    ${ENABLE_SSH_ON_A3NODE}=      Run Keyword If   '${${a3_version}.version}'=='3.2'  Enable SSH Access On A3 Node     ${${a3_version}.node1_ip}  ${${a3_version}.ui_username}   ${${a3_version}.ui_password}    ${${a3_version}.console_password}    7
    Run Keyword If  '${${a3_version}.version}'=='3.2'      should be equal as strings    '${ENABLE_SSH_ON_A3NODE}'   '1'

    ${A3_NODE_SPAWN}=          Open Paramiko SSH Spawn    ${${a3_version}.node1_ip}   ${${a3_version}.console_username}    ${${a3_version}.console_password}  ${${a3_version}.console_port}
    ${UNLINK_A3}=              UnLink A3 Nodes From XIQ    ${A3_NODE_SPAWN}
    should be equal as strings    '${UNLINK_A3}'   '${CURL_CODE_SUCCESS}'

Test5 : Verify A3 Page after UnLink A3 Cluster To XIQ
    [Documentation]    Verify A3 Page after UnLink A3 Cluster To XIQ
    [Tags]      sanity   A3  Link  unlink  P1  regression  production

    Depends On          Test1
    ${LOGIN_XIQ}=                  Login User          ${tenant_username}      ${tenant_password}
    ${A3_SERVER_STATUS}=           Validate A3 Page After Unlink    ${${a3_version}.ip}
    should contain any   '${A3_SERVER_STATUS}'    '${UNLINK_A3_PAGE_TEXT}'  '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser