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
${a3_server}                a3_server1

*** Settings ***
Library     Collections
Library     common/Utils.py
Library     extauto/common/Cli.py
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

Force Tags   testbed_none

Suite Setup      Suite Setup

*** Keywords ***
Suite Setup
    [Documentation]   Suite Setup

    ${LOGIN_STATUS}=                Login User          ${tenant_username}      ${tenant_password}     check_warning_msg=True
    should be equal as integers     ${LOGIN_STATUS}         1

    ${ENABLE_SSH_ON_A3NODE}=      Enable SSH Access On A3 Node     ${${a3_server}.node1_ip}  ${${a3_server}.ui_username}   ${${a3_server}.ui_password}    ${${a3_server}.password}    7
    should be equal as strings    '${ENABLE_SSH_ON_A3NODE}'   '1'

    ${A3_NODE_SPAWN}=          Open Paramiko SSH Spawn    ${${a3_server}.node1_ip}   ${${a3_server}.username}    ${${a3_server}.password}  ${${a3_server}.port}
    should not be equal as strings             '${A3_NODE_SPAWN}'              '-1'

    Set Suite Variable      ${A3_NODE_SPAWN}

*** Test Cases ***
TCCS-11572: Link/Unlink A3 to XIQ - Sanity
    [Documentation]    Link/Unlink A3 to XIQ - Sanity

    [Tags]             production       tccs_11572

    #Link A3 Cluster To XIQ
    ${LINK_A3}=                     Link A3 Nodes To XIQ    ${A3_NODE_SPAWN}   ${tenant_username}   ${tenant_password}  url=${CLOUD_GDC_URL}
    should be equal as strings      '${LINK_A3}'   '${CURL_CODE_SUCCESS}'

    #Verify A3 Cluster Node and Virtual IP Status
    ${A3_SERVER_STATUS}=            Get A3 Server Status   ${${a3_server}.ip}
    should be equal as strings      '${A3_SERVER_STATUS}'   'green'

    ${A3_NODE1_STATUS}=             Get A3 Node Status   ${${a3_server}.ip}  ${${a3_server}.node1_hostname}
    should be equal as strings    '${A3_NODE1_STATUS}'   'green'
    ${A3_NODE2_STATUS}=             Get A3 Node Status   ${${a3_server}.ip}  ${${a3_server}.node2_hostname}
    should be equal as strings    '${A3_NODE2_STATUS}'   'green'
    ${A3_NODE3_STATUS}=             Get A3 Node Status   ${${a3_server}.ip}  ${${a3_server}.node3_hostname}
    should be equal as strings    '${A3_NODE3_STATUS}'   'green'

    #Verify A3 Virtual IP Access From XIQ
    ${A3_SERVER_STATUS}=            Verify A3 Server Login On XIQ   ${${a3_server}.ip}   ${${a3_server}.ui_username}  ${${a3_server}.ui_password}
    should be equal as strings      '${A3_SERVER_STATUS}'   '${A3_PAGE_TITLE}'

    #UnLink A3 Cluster To XIQ
    ${UNLINK_A3}=                   UnLink A3 Nodes From XIQ    ${A3_NODE_SPAWN}
    should be equal as strings      '${UNLINK_A3}'   '${CURL_CODE_SUCCESS}'

    ${LOGOUT_RESULT}=               Logout User
    Should Be Equal As Integers     ${LOGOUT_RESULT}                1

    ${LOGIN_STATUS}=                Login User          ${tenant_username}      ${tenant_password}     check_warning_msg=True
    should be equal as integers     ${LOGIN_STATUS}         1

    #Verify A3 Page after UnLink A3 Cluster To XIQ
    ${A3_SERVER_STATUS}=            Validate A3 Page After Unlink    ${${a3_server}.ip}
    should contain any              '${A3_SERVER_STATUS}'    '${UNLINK_A3_PAGE_TEXT}'  '1'

    [Teardown]   run keywords       Logout User
    ...                             Quit Browser