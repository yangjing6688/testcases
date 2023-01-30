# Author        : Venkata S Muvvala
# Date          : 2 June 2020
# Description   : This is to test XAPI - Cloud Config Groups API Tests

# Topology:
# ---------
#    ScriptHost
#      |
#      |
#     Cloud
# Pre-config:
# -----------
#  Loign With XIQ account
#  Get Access Token
#  On board a device
#
# Execution Command:
# ------------------
# cd /automation/xiq/cw_automation/testsuites/xiq/xapi
# To Run All test cases use below command
# robot -v TESTBED:blr_tb_1 -v TOPO:topo-1  -v ENV:environment  xapi_cloud_config_groups.robot
# To Run All test cases use below command to run only Test Case 2
# robot -v TESTBED:blr_tb_1 -v TOPO:topo-1  -v ENV:environment -i Test2 xapi_cloud_config_groups.robot
#
#

*** Variables ***
${INVALID_ARGUMENT}             INVALID_ARGUMENT
${RESPONSE_CCG_DEVICE_ID}

# CLOUD CONFIG GROUP POST API TEST VARIABLES
${REQUEST_CCG_DESCRIPTION_FOR_POST} =    Add New CCG Via Test Automation For POST 2023

# CLOUD CONFIG GROUP GET API BY ID TEST VARIABLES
${REQUEST_CCG_DESCRIPTION_FOR_GET} =    Add New CCG Via Test Automation For Get 2023

# CLOUD CONFIG GROUP DELETE API TEST VARIABLES
${REQUEST_CCG_DESCRIPTION_FOR_DELETE} =    Add New CCG Via Test Automation For Delete 2023

# Common HTTP Response codes
${HTTP_RESPONSE_CODE_200} =     200
${HTTP_RESPONSE_CODE_201} =     201
${HTTP_RESPONSE_CODE_202} =     202
${HTTP_RESPONSE_CODE_400} =     400
${HTTP_RESPONSE_CODE_500} =     500

*** Settings ***
Force Tags  testbed_1_node

Library     common/Xapi.py
Library     extauto/common/Cli.py
Library     common/TestFlow.py
Library     common/Utils.py
Library     xiq/flows/configure/CommonObjects.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py


Resource    Tests/Robot/Libraries/XAPI/XAPI-Authentication-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Configuration-Deployment-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Network-Policy-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Device-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Location-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Configuration-Policy-Keywords.robot


Variables   Environments/Config/waits.yaml
Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}


Suite Setup        Test Suite Setup


*** Keywords ***
# generate the key once per suite
Test Suite Setup
    # generate the key once per suite
    ${ACCESS_TOKEN}=        generate_access_token    ${tenant_username}      ${tenant_password}      login
    set suite variable     ${ACCESS_TOKEN}
    Log    Checking the Access Token not equal to -1
    skip if     '${ACCESS_TOKEN}' == '-1'

# Use this method to convert the ap, wing, netelem to a generic device object
    # device1       => device1
    # wing1     => device1
    # netelem1  => device1 (EXOS / VOSS)
    convert to generic device object   device  index=1
    log to console  ${device1.serial}

#On Board Device And Get Device Id
    # At least one device id is required to create new cloud config group
    # so creating one device to make sure ths test suite does not depened on existing test cases execution order or data
    # and its needs to be deleted at the end of test suite tear down step
    # onboard a new device using APIs
    ${DEVICE_ONBOARD}=               xapi ap device onboard      ${device1.serial}
    Log    Validating the Successful Device Onboard
    Should Be Equal As Integers          ${DEVICE_ONBOARD}       1
    sleep    ${device_onboarding_wait}

    ${SPAWN_CONNECTION}=      Open Spawn    ${device1.ip}     ${device1.port}   ${device1.username}   ${device1.password}    ${device1.cli_type}
    configure_device_to_connect_to_cloud    ${device1.cli_type}       ${capwap_url}      ${SPAWN_CONNECTION}

    #Get Device ID
    ${RESPONSE_CCG_DEVICE_ID}=            xapi list and get device id     ${device1.serial}
    skip if   ${RESPONSE_CCG_DEVICE_ID}==0
    skip if   ${RESPONSE_CCG_DEVICE_ID}==-1
    set suite variable         ${RESPONSE_CCG_DEVICE_ID}

Test Case Clean Up Steps
    [Documentation]   This is being used to call as part of each test case to delete test data that is created as part of test case.
    [Arguments]         ${device_id}            ${ccg_id}
    Test Case Clean Up Delete Device Id         ${device_id}
    Test Case Clean Up Delete Cloud Config Id   ${ccg_id}

Test Case Clean Up Delete Device Id
    [Documentation]   This is being used to delete device which is created as part of test case pre step/execution.
    [Arguments]         ${device_id}
    ${DELETE_RESP}=              xapi delete device        ${device_id}
    Log    Validating the Successful Delete of Device
    Should Be Equal As Integers      ${DELETE_RESP}       1

Test Case Clean Up Delete Cloud Config Id
     [Documentation]   This is being used to delete cloud config group id which created as part of test case pre step/execution.
     [Arguments]      ${ccg_id}
     ${DELETE_RESP}=              xapi delete ccg           ${ccg_id}
     Log    Validating the Successful Delete of CCG
     Should Be Equal As Integers      ${DELETE_RESP}       1

*** Test Cases ***
TC-7173:Test Cloud Config Groups GET API For All Records
    [Documentation]        Test Cloud Config Groups GET API For All Records
    [Tags]                 xapi    tcxm-7173	            development
    ${total_cloud_config_groups_count} =    xapi get total cloud config groups count
    Log                    ${total_cloud_config_groups_count}
    Should Be True         ${total_cloud_config_groups_count} >= 0

TC-7174:Test Cloud Config Groups POST API
    [Documentation]        Test Cloud Config Groups POST API
    [Tags]                 xapi    tcxm-7174        development
    # Pre Steps
    ${before_post_api_total_cfgs_count} =                           xapi get total cloud config groups count
    log to console  ${before_post_api_total_cfgs_count}

    # Actual Test call method
    ${REQUEST_CCG_NAME_FOR_POST} =           get random string      length=5
    Log     ${REQUEST_CCG_NAME_FOR_POST}
    ${http_post_response_body}=          xapi create new cloud config groups      ${REQUEST_CCG_NAME_FOR_POST}     ${REQUEST_CCG_DESCRIPTION_FOR_POST}      ${RESPONSE_CCG_DEVICE_ID}
    Log                     ${http_post_response_body}
    ${RESPONSE_CCG_ID_FOR_POST} =       get json values                 ${http_post_response_body}       key=id
    set global variable     ${RESPONSE_CCG_ID_FOR_POST}

    # Verification Steps
    ${http_get_response_body}=         xapi get cloud config group by id        ${RESPONSE_CCG_ID_FOR_POST}
    Log                     ${http_get_response_body}
    ${response_ccg_name} =            get json values                    ${http_get_response_body}          key=name
    Log      ${response_ccg_name}
    ${response_ccg_description} =     get json values                    ${http_get_response_body}          key=description
    Log      ${response_ccg_description}
    ${after_post_api_total_cfgs_count} =                            xapi get total cloud config groups count
    # total count should increase by 1
    ${expected_count}=          Evaluate            ${before_post_api_total_cfgs_count} + 1
    Should Be True	                                ${RESPONSE_CCG_ID_FOR_POST}
    Should be equal as integers                     ${expected_count}                       ${after_post_api_total_cfgs_count}
    should be equal as strings                      ${REQUEST_CCG_NAME_FOR_POST}            ${response_ccg_name}
    should be equal as strings                      ${REQUEST_CCG_DESCRIPTION_FOR_POST}     ${response_ccg_description}
    [Teardown]  Test Case Clean Up Delete Cloud Config Id     ${RESPONSE_CCG_ID_FOR_POST}

TC-7175:Test Cloud Config Groups GET API By Id
    [Documentation]        Test Cloud Config Groups GET API By Id
    [Tags]                 xapi    tcxm-7175               development

    # Pre Steps
    ${REQUEST_CCG_NAME_FOR_GET} =           get random string   length=5
    Log     ${REQUEST_CCG_NAME_FOR_GET}
    ${http_post_response_body}=          xapi create new cloud config groups      ${REQUEST_CCG_NAME_FOR_GET}     ${REQUEST_CCG_DESCRIPTION_FOR_GET}      ${RESPONSE_CCG_DEVICE_ID}
    Log                     ${http_post_response_body}
    ${RESPONSE_CCG_ID_FOR_GET} =       get json values                 ${http_post_response_body}       key=id
    set global variable     ${RESPONSE_CCG_ID_FOR_GET}

    # Actual Test API call
    ${http_get_response_body}        xapi get cloud config group by id                ${RESPONSE_CCG_ID_FOR_GET}
    Log                     ${http_post_response_body}

    # Verification steps
    ${response_ccg_name} =            get json values                    ${http_get_response_body}          key=name
    Log      ${response_ccg_name}
    ${response_ccg_description} =     get json values                    ${http_get_response_body}          key=description
    Log      ${response_ccg_description}

    should be equal as strings                                     ${REQUEST_CCG_NAME_FOR_GET}                 ${response_ccg_name}
    should be equal as strings                                     ${REQUEST_CCG_DESCRIPTION_FOR_GET}          ${response_ccg_description}
    [Teardown]  Test Case Clean Up Delete Cloud Config Id         ${RESPONSE_CCG_ID_FOR_GET}


TC-7177:Test Cloud Config Groups DELETE API By Id
    [Documentation]        Test Cloud Config Groups DELETE API By Id
    [Tags]                 xapi    tcxm-7177                development
     # Pre steps
    ${REQUEST_CCG_NAME_FOR_DELETE} =           get random string   length=5
    Log     ${REQUEST_CCG_NAME_FOR_DELETE}
    ${http_post_response_body}          xapi create new cloud config groups           ${REQUEST_CCG_NAME_FOR_DELETE}     ${REQUEST_CCG_DESCRIPTION_FOR_DELETE}      ${RESPONSE_CCG_DEVICE_ID}

    ${RESPONSE_CCG_ID_FOR_DELETE} =       get json values                 ${http_post_response_body}       key=id
    Set Global Variable     ${RESPONSE_CCG_ID_FOR_DELETE}
    ${before_delete_api_total_cfgs_count} =                         xapi get total cloud config groups count

    # Actual Test API Call
    ${delete_response_code}=                                        REST API Delete                       /ccgs                             ${RESPONSE_CCG_ID_FOR_DELETE}
    ${after_delete_api_total_cfgs_count} =                          xapi get total cloud config groups count

    # Verification Steps
    Log                         ${delete_response_code}
    should be equal as integers                             ${delete_response_code}                       1
    ${expected_count}=          Evaluate                    ${before_delete_api_total_cfgs_count} - 1
    Should be equal as integers                             ${expected_count}                               ${after_delete_api_total_cfgs_count}

    ${http_get_response_body}         xapi get cloud config group by id                ${RESPONSE_CCG_ID_FOR_DELETE}
    ${error_code} =                                         get json values                    ${http_get_response_body}          key=error_code
    ${error_message} =                                      get json values                    ${http_get_response_body}          key=error_message
    should be equal as strings                              NOT_FOUND                 ${error_code}
    should be equal as strings                              NOT_FOUND: core.service.data.can.not.find.object.with.id                 ${error_message}
    [Teardown]  Test Case Clean Up Delete Device Id         ${RESPONSE_CCG_DEVICE_ID}

TC-7179:NEG-Create Cloud Config User Group by providing invalid device ID as input
    [Documentation]       NEG-Create Cloud Config User Group by providing invalid device ID as input
    [Tags]                xapi    tcxm-7179          development
    # Actual Test call method
    ${REQUEST_CCG_NAME_FOR_POST} =           get random string      length=5
    Log     ${REQUEST_CCG_NAME_FOR_POST}
    ${INVALID_DEVICE_ID} =  get random integer
    Log                     ${INVALID_DEVICE_ID}
    ${http_post_response_body}          xapi create new cloud config groups  ${REQUEST_CCG_NAME_FOR_POST}     ${REQUEST_CCG_DESCRIPTION_FOR_POST}     ${INVALID_DEVICE_ID}
    ${error_code} =                                         get json values                    ${http_post_response_body}          key=error_code
    should be equal as strings                              INVALID_ARGUMENT                 ${error_code}
