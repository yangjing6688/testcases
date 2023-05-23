# Author        : LitianWu
# Date          : 03 Apr 2023
# Description   : XAPI Automation for NG-XAPI-CFD-Cases

# Topology:
# ---------
#    ScriptHost
#      |________
#      |        |
#     Cloud     AP
# Pre-config:
# -----------
#
#

# Execution Command:
# ------------------
# robot -v ENV:environment.seleniumhub.docker.chrome.yaml -v TOPO:topo.test.g2r1.yaml New_API_7_XIQ-10365.robot
#


*** Variables ***
${VLAN_PROFILE_ID}=                -1

*** Settings ***
Force Tags  testbed_none

Library     Collections
Library     extauto/common/Cli.py
Library     extauto/common/TestFlow.py
Library     extauto/common/Utils.py
Library     keywords/xapi_base/XapiBaseConfigurationBasicApi.py
Library     keywords/xapi_base/XapiBaseConfigurationPolicyApi.py
Library     keywords/xapi_base/XapiBaseLocationApi.py
Library     extauto/xiq/xapi/common/XapiLogin.py
Library     extauto/xiq/xapi/configure/XapiVlan.py
Library     extauto/xiq/flows/manage/Location.py
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     extauto/xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py

Resource    Tests/Robot/Libraries/XAPI/XAPI-Authentication-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-VLAN-Keywords.robot


Variables    Environments/Config/waits.yaml
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Force Tags      testbed_none

Suite Setup      Pre Condition
Suite Teardown   Suite Clean Up

*** Keywords ***
Pre Condition

    ${XAPI_LOGIN}=         XapiLogin.login        ${tenant_username}       ${tenant_password}
    skip if       '${XAPI_LOGIN}' == '-1'

Teardown
    ${RESP_RAW_OBJECT}=        xapi base delete location        id=${LOCATION_ID}         _preload_content=${False}

Suite Clean Up
    [Documentation]    logout and quit web browser
    [Tags]             development          tcxm_26873
    log        ${VLAN_PROFILE_ID}
    ${RESP_RAW_OBJECT}=  xapi_base_delete_vlan_profile  id=${VLAN_PROFILE_ID}        _preload_content=${False}

*** Test Cases ***

TCCS-13482: Create a VLAN PROFILE via ADMIN USER
    [Documentation]         Create a VLAN
    [Tags]                  tccs-13482      development
    ${vlan_profile}=        create dictionary    name=vlan1        default_vlan_id=100         enable_classification=false
    ${RESP_RAW_OBJECT}=        xapi_base_create_vlan_profile  xiq_create_vlan_profile_request=${vlan_profile}   _preload_content=${False}
    # Convert the raw object to json
    ${RESP}=                  XapiBaseConfigurationBasicApi.convert_preload_content_data_to_object   ${RESP_RAW_OBJECT}
    ${VLAN_PROFILE_ID}=         get json values         ${RESP}         key=id
    log to console      ID: ${VLAN_PROFILE_ID}
    should be true        ${VLAN_PROFILE_ID}>0
    set global variable     ${VLAN_PROFILE_ID}

TCCS-13481: List a VLAN PROFILE via ADMIN USER
    [Documentation]         Run the GET API request to list the VLAN PROFILES
    [Tags]                  tccs-13481    development
    ${RESP_RAW_OBJECT}=        xapi_base_list_vlan_profiles    _preload_content=${False}
    # Convert the raw object to json
    ${RESP}=                  XapiBaseConfigurationBasicApi.convert_preload_content_data_to_object   ${RESP_RAW_OBJECT}
    ${total_count}=         get json values         ${RESP}         key=total_count
    log to console      ID: ${total_count}
    should be true        ${total_count}>0

TCCS-13484: Create a CLASSFICATION RULE of type LOCATION via ADMIN USER
    [Documentation]         Run the POST API request to Create a CLASSFICATION RULE of type LOCATION
    [Tags]                  tccs-13484    development
    ${org_profile}=        create dictionary    organization=test_organization_1       country=CHINA_156
    ${RESP_RAW_OBJECT}=        xapi_base_initialize_location        xiq_initialize_location_request=${org_profile}        _preload_content=${False}
    ${RESP}=                  XapiBaseConfigurationBasicApi.convert_preload_content_data_to_object   ${RESP_RAW_OBJECT}
    ${LOCATION_ID}=        get json values         ${RESP}        key=id
    ${classification_1}=        create dictionary      classification_type=CLASSIFICATION_TYPE_LOCATION         match=${true}        classification_type_id=${LOCATION_ID}
    ${classification_list}=       create list        ${classification_1}
    ${classrule_profile}=        create dictionary      name=rule_1        description=testing       classifications=${classification_list}
    ${RESP_RAW_OBJECT}=        xapi_base_create_classification_rule        xiq_create_classification_rule_request=${classrule_profile}        _preload_content=${False}
    ${RESP}=                  XapiBaseConfigurationBasicApi.convert_preload_content_data_to_object   ${RESP_RAW_OBJECT}
    ${RULE_ID}=        get json values         ${RESP}        key=id

    [teardown]
    ${RESP_RAW_OBJECT}=        xapi base delete location        id=${LOCATION_ID}         _preload_content=${False}
    ${RESP_RAW_OBJECT}=        xapi_base_delete_classification_rule        id=${RULE_ID}         _preload_content=${False}










