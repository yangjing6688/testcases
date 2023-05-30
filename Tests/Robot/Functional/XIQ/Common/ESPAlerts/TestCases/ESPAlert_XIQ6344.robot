# Author        : Zhihui Chen
# Date          : Jul 28th 2022
# Description   : ESP Alert
#
# Topology      :
# Host ----- Cloud
*** Variables ***

*** Settings ***
Documentation  robot -v ENV:environment.local.chrome.yaml -v TOPO:topo.test.cp8r1.yaml  ESPAlert_XIQ6344.robot

Library      String
Library      Collections
Library      extauto/common/TestFlow.py
Library      extauto/common/Cli.py
Library      extauto.xiq.flows.manage.EspAlert
Library      extauto.xiq.flows.globalsettings.Webhook

Resource    ../Resources/AllResources.robot

Force Tags            testbed_1_node

Suite Setup      lib_login.Log Into XIQ and Confirm Success  ${tenant_username}  ${tenant_password}  ${test_url}
Suite Teardown   Clean Up Alert Policies And Webhooks

*** Test Cases ***
TCXM-18016: Check device down(up)/Immediate can be saved
    [Documentation]         Create alert policies
    [Tags]                  tcxm_18016  development
    Navigate Manage Alerts
    Go To Alert Policy
    ${result}=  Create Alert Policy  ${alert_device_down.policy_type}  ${alert_device_down.source_parent}  ${alert_device_down.source}  ${alert_device_down.trigger_type}  ${alert_device_down.when}
    Should Be Equal As Integers  ${result}  1
    ${result}=  Create Alert Policy  ${alert_device_up.policy_type}  ${alert_device_up.source_parent}  ${alert_device_up.source}  ${alert_device_up.trigger_type}  ${alert_device_up.when}
    Should Be Equal As Integers  ${result}  1

TCXM-22007: Verify user is able to add a new webhook
    [Documentation]         Create webhook
    [Tags]                  tcxm_22007  development
    Depends On  TCXM-18016
    Go Out Alerts
    Navigate To Webhooks Page
    ${result}=  Create Webhook  ${webhook1}
    Should Be Equal As Integers  ${result}  1

TCXM-22009: Verify user is able to edit the existing webhook
    [Documentation]         Edit webhook
    [Tags]                  tcxm_22009  development
    Depends On  TCXM-22007
    ${result}=  Edit Webhook  ${webhook1}  ${webhook2}
    Should Be Equal As Integers  ${result}  1

*** Keywords ***
Clean Up Alert Policies And Webhooks
    [Documentation]  delete alert policies and webhooks that create by above due to it cannot be duplicated
    Navigate Manage Alerts
    Go To Alert Policy
    Delete Alert Policy  ${alert_device_down.when}
    Delete Alert Policy  ${alert_device_up.when}
    Go Out Alerts
    Navigate To Webhooks Page
    Delete Webhook  ${webhook2}
    Logout User
    Quit Browser
