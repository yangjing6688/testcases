# Author        : Kun Li
# Date          : Feb 22th 2023
# Description   : ESP Alert Audit Log
# Note          : First supported release is 23r1.1, use the refactor audit log api

# Topology:
# ---------
#    ScriptHost/AutoIQ
#      |________
#      |        |
#     Cloud     AP
# Pre-config:
# -----------
#
#
#
# Execution Command:
# ------------------
# robot -v ENV:environment.local.chrome.yaml -v TOPO:topo.test.aio.hz.148.yaml -v TESTBED:HANGZHOU/Dev/xiq_hz_tb2_ap550.yaml ESPAlert_AuditLog_XIQ6051.robot

*** Variables ***
${LOG_KEYWORD_CREATE_DEV_UP}    Created alert policy [when device up
${LOG_KEYWORD_CREATE_DEV_DN}    Created alert policy [when device down
${LOG_KEYWORD_DELETE_DEV_UP}    Deleted alert policy [when device up
${LOG_KEYWORD_DELETE_DEV_DN}    Deleted alert policy [when device down
${LOG_KEYWORD_DISABLE_POLICY}   Disabled alert policy
${LOG_KEYWORD_ENABLE_POLICY}    Enabled alert policy

*** Settings ***
Documentation  robot -v ENV:environment.local.chrome.yaml -v TOPO:topo.test.aio.hz.148.yaml -v TESTBED:HANGZHOU/Dev/xiq_hz_tb2_ap550.yaml ESPAlert_AuditLog_XIQ6051.robot

Library     extauto/common/Utils.py
Library     extauto/common/Screen.py
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
Library     extauto/xiq/flows/common/Login.py
Library     extauto/xiq/flows/common/Navigator.py
Library     extauto/xiq/flows/manage/Location.py
Library     extauto/xiq/flows/manage/Devices.py
Library     extauto/xiq/flows/globalsettings/GlobalSetting.py
Library     String
Library     Collections
Library     extauto/xiq/flows/manage/EspAlert.py
Library     extauto/xiq/flows/globalsettings/Webhook.py
Library     Tests/Robot/Functional/XAPI/Log/Resources/xapi_log_keyword.py

Resource    Tests/Robot/Libraries/XAPI/XAPI-Logs-Keywords.robot

Variables   ../Resources/Webhook.yaml
Variables   ../Resources/AlertPolicy.yaml

Variables   Environments/Config/waits.yaml
#Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}
Variables   Environments/${ENV}

Force Tags      testbed_none

Suite Setup     Test Suite Setup
Suite Teardown  Test Suite Clean Up

*** Keywords ***

Test Suite Setup
    [Documentation]  Suite setup.

    # login the user
    Login User   ${tenant_username}   ${tenant_password}

    Navigate Manage Alerts
    Go To Alert Policy
    Clean Alert Policy

    # Generate xapi access token
    ${ACCESS_TOKEN}=   Generate Access Token   ${tenant_username}   ${tenant_password}   login
    set suite variable     ${ACCESS_TOKEN}
    Log    Checking the Access Token not equal to -1
    skip if     '${ACCESS_TOKEN}' == '-1'

Test Suite Clean Up
    [Documentation]  Suite clean.

    Go Out Alerts
    Logout User
    Quit Browser

Log Count by Keyword
    [Documentation]  Get log count based on log keyword
    [Arguments]  ${LOG_KEYWORD}

    ${LOG_KEYWORD_URI}=  encode uri  ${LOG_KEYWORD}
    ${LOG_CONTENT_KEYWORD}=  xapi list first page audit logs by keyword   ${LOG_KEYWORD_URI}
    ${LOG_COUNT_KEYWORD}=  xapi get audit log count   ${LOG_CONTENT_KEYWORD}

    [Return]  ${LOG_COUNT_KEYWORD}

Clean Alert Policy
    [Documentation]  Delete exist device up down alert policy

    ${EXIST_DEV_UP}=  find when in configured grid  ${alert_device_up.when}
    run keyword if  ${EXIST_DEV_UP}==1  Delete Alert Policy  ${alert_device_up.when}
    ${EXIST_DEV_DN}=  find when in configured grid  ${alert_device_down.when}
    run keyword if  ${EXIST_DEV_DN}==1  Delete Alert Policy  ${alert_device_down.when}

*** Test Cases ***
TCXM-22414: Audit Log when Create Event Type Alert Policy
    [Documentation]     The audit log should be generated when create a new alert policy of event type
    [Tags]              tcxm_22414  development

    # Check audit log before create alert policy
    ${LOG_COUNT_CREATE_DEV_DN_BEFORE}=  Log Count by Keyword  ${LOG_KEYWORD_CREATE_DEV_DN}
    ${LOG_COUNT_CREATE_DEV_UP_BEFORE}=  Log Count by Keyword  ${LOG_KEYWORD_CREATE_DEV_UP}

    # Create an alert policy of event type
    ${POLICY_DEV_DOWN}=  Create Alert Policy  ${alert_device_down.policy_type}  ${alert_device_down.source_parent}  ${alert_device_down.source}  ${alert_device_down.trigger_type}  ${alert_device_down.when}
    Should Be Equal As Integers  ${POLICY_DEV_DOWN}  1
    ${POLICY_DEV_UP}=  Create Alert Policy  ${alert_device_up.policy_type}  ${alert_device_up.source_parent}  ${alert_device_up.source}  ${alert_device_up.trigger_type}  ${alert_device_up.when}
    Should Be Equal As Integers  ${POLICY_DEV_UP}  1

    # Wait for audit log generated and check audit Log after create alert polcy
    ${EXPECT_LOG_COUNT_CREATE_DEV_DN_AFTER}=  evaluate   ${LOG_COUNT_CREATE_DEV_DN_BEFORE} + 1
    ${EXPECT_LOG_COUNT_CREATE_DEV_UP_AFTER}=  evaluate   ${LOG_COUNT_CREATE_DEV_UP_BEFORE} + 1
    Sleep  5
    FOR  ${CHECK_TIME}   IN RANGE    ${20}
         ${LOG_COUNT_CREATE_DEV_DN_AFTER}=  Log Count by Keyword  ${LOG_KEYWORD_CREATE_DEV_DN}
         run keyword if  ${LOG_COUNT_CREATE_DEV_DN_AFTER}==${EXPECT_LOG_COUNT_CREATE_DEV_DN_AFTER}  exit for loop
         sleep  1
    END
    FOR  ${CHECK_TIME}   IN RANGE    ${20}
         ${LOG_COUNT_CREATE_DEV_UP_AFTER}=  Log Count by Keyword  ${LOG_KEYWORD_CREATE_DEV_UP}
         run keyword if  ${LOG_COUNT_CREATE_DEV_UP_AFTER}==${EXPECT_LOG_COUNT_CREATE_DEV_UP_AFTER}  exit for loop
         sleep  1
    END

    Should Be Equal As Integers  ${LOG_COUNT_CREATE_DEV_DN_AFTER}  ${EXPECT_LOG_COUNT_CREATE_DEV_DN_AFTER}
    Should Be Equal As Integers  ${LOG_COUNT_CREATE_DEV_UP_AFTER}  ${EXPECT_LOG_COUNT_CREATE_DEV_UP_AFTER}

TCXM-22415: Audit Log when Disable Event Type Alert Policy
    [Documentation]     The audit log should be generated when disable an exist alert policy of event type
    [Tags]              tcxm_22415  development

    # Check audit log before create alert policy
    ${LOG_COUNT_DISABLE_BEFORE}=  Log Count by Keyword  ${LOG_KEYWORD_DISABLE_POLICY}

    # Diable an exist alert policy
    ${POLICY_DISABLE}=  toggle alert policy status  ${alert_device_up.when}
    Should Be Equal As Integers  ${POLICY_DISABLE}  1

    # Wait for audit log generated and check audit Log after disable alert polcy
    ${EXPECT_LOG_COUNT_DISABLE_AFTER}=  evaluate   ${LOG_COUNT_DISABLE_BEFORE} + 1

    Sleep  5
    FOR  ${CHECK_TIME}   IN RANGE    ${20}
         ${LOG_COUNT_DISABLE_AFTER}=  Log Count by Keyword  ${LOG_KEYWORD_DISABLE_POLICY}
         run keyword if  ${LOG_COUNT_DISABLE_AFTER}==${EXPECT_LOG_COUNT_DISABLE_AFTER}  exit for loop
         sleep  1
    END

    Should Be Equal As Integers  ${LOG_COUNT_DISABLE_AFTER}  ${EXPECT_LOG_COUNT_DISABLE_AFTER}

TCXM-22416: Audit Log when Enable Event Type Alert Policy
    [Documentation]     The audit log should be generated when enable an exist alert policy of event type
    [Tags]              tcxm_22416  development

    # Check audit log before create alert policy
    ${LOG_COUNT_ENABLE_BEFORE}=  Log Count by Keyword  ${LOG_KEYWORD_ENABLE_POLICY}

    # Enable an exist alert policy
    ${POLICY_ENABLE}=  toggle alert policy status  ${alert_device_up.when}
    Should Be Equal As Integers  ${POLICY_ENABLE}  1

    # Wait for audit log generated and check audit Log after enable alert polcy
    ${EXPECT_LOG_COUNT_ENABLE_AFTER}=  evaluate   ${LOG_COUNT_ENABLE_BEFORE} + 1

    Sleep  5
    FOR  ${CHECK_TIME}   IN RANGE    ${20}
         ${LOG_COUNT_ENABLE_AFTER}=  Log Count by Keyword  ${LOG_KEYWORD_ENABLE_POLICY}
         run keyword if  ${LOG_COUNT_ENABLE_AFTER}==${EXPECT_LOG_COUNT_ENABLE_AFTER}  exit for loop
         sleep  1
    END

    Should Be Equal As Integers  ${LOG_COUNT_ENABLE_AFTER}  ${EXPECT_LOG_COUNT_ENABLE_AFTER}

TCXM-22417: Audit Log when Delete Event Type Alert Policy
    [Documentation]     The audit log should be generated when delete an exist alert policy of event type
    [Tags]              tcxm_22417  development

    # Check audit log before delete alert policy
    ${LOG_COUNT_DELETE_DEV_UP_BEFORE}=  Log Count by Keyword  ${LOG_KEYWORD_DELETE_DEV_UP}
    ${LOG_COUNT_DELETE_DEV_DN_BEFORE}=  Log Count by Keyword  ${LOG_KEYWORD_DELETE_DEV_DN}

    # Delete an exist alert policy of event type
    ${POLICY_DEV_DOWN}=  Delete Alert Policy  ${alert_device_down.when}
    Should Be Equal As Integers   ${POLICY_DEV_DOWN}  1
    ${POLICY_DEV_UP}=  Delete Alert Policy   ${alert_device_up.when}
    Should Be Equal As Integers   ${POLICY_DEV_UP}  1

    # Wait for audit log generated and check audit Log after delete alert polcy
    ${EXPECT_LOG_COUNT_DELETE_DEV_UP_AFTER}=  evaluate   ${LOG_COUNT_DELETE_DEV_UP_BEFORE} + 1
    ${EXPECT_LOG_COUNT_DELETE_DEV_DN_AFTER}=  evaluate   ${LOG_COUNT_DELETE_DEV_DN_BEFORE} + 1
    Sleep  5
    FOR  ${CHECK_TIME}   IN RANGE    ${20}
         ${LOG_COUNT_DELETE_DEV_DN_AFTER}=  Log Count by Keyword  ${LOG_KEYWORD_DELETE_DEV_DN}
         run keyword if  ${LOG_COUNT_DELETE_DEV_DN_AFTER}==${EXPECT_LOG_COUNT_DELETE_DEV_DN_AFTER}  exit for loop
         sleep  1
    END
    FOR  ${CHECK_TIME}   IN RANGE    ${20}
         ${LOG_COUNT_DELETE_DEV_UP_AFTER}=  Log Count by Keyword  ${LOG_KEYWORD_DELETE_DEV_UP}
         run keyword if  ${LOG_COUNT_DELETE_DEV_UP_AFTER}==${EXPECT_LOG_COUNT_DELETE_DEV_UP_AFTER}  exit for loop
         sleep  1
    END

    Should Be Equal As Integers  ${LOG_COUNT_DELETE_DEV_UP_AFTER}  ${EXPECT_LOG_COUNT_DELETE_DEV_UP_AFTER}
    Should Be Equal As Integers  ${LOG_COUNT_DELETE_DEV_DN_AFTER}  ${EXPECT_LOG_COUNT_DELETE_DEV_DN_AFTER}
