    # Author        : Subramani R
# Date          : 15 February 2022
# Description   : XAPI - PPSK Usergroups and PPSK Users

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
# robot  -v TOPO:topo.xapi.yaml New_API_5_XIQ-3193.robot
#
#


*** Variables ***
${PPSK_USERGROUP_URI}=  /usergroups
${PPSK_USER_URI}=  /endusers
${PPSK_USER_GROUP_ID}=  0
${PPSK_UPDATE_USER_URI}=  /endusers/:id
${PPSK_USER_ID}=  0
${PPSK_USERGROUP_GLOBAL}=    group3
${PPSK_USERNAME_GLOBAL}=    ppskuser1
${PPSK_USERGROUP}=    group1
${PPSK_USERNAME}=    ppskuser
${NEW_PASSWORD}=    Test@123456789
${ERROR_CODE}=  error_code
${ERROR_CODE_KNOWN_VALUE}=  UNKNOWN
${ERROR_CODE_ERROR_VALUE}=  ServerError

*** Settings ***
Force Tags  testbed_3_node

Library     common/TestFlow.py
Library     common/Xapi.py
Library     common/Utils.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/configure/CommonObjects.py


Resource    ../../XAPI_PHASE_5A/Resources/AllResources.robot

Variables   Environments/Config/waits.yaml


*** Keywords ***

#####  PPSK USER Group Keywords   #####

create ppsk user group
    [Documentation]  create ppsk user group
    [Arguments]  ${NAME}
    ${RESP}=  rest api post  ${PPSK_USERGROUP_URI}  '{"name":"${NAME}","description":"AShortDescription","password_db_location":"CLOUD","password_type":"PPSK","enable_max_clients_per_ppsk":"false","max_clients_per_ppsk":"0","pcg_use_only":"false","pcg_type":"AP_BASED","ppsk_use_only":"false","enable_cwp_reg":"false","password_settings":{"enable_letters":"true","enable_numbers":"true","enable_special_characters":"true","password_character_types":"INCLUDE_ALL_CHARACTER_TYPE_ENABLED","psk_generation_method":"USER_STRING_PASSWORD","password_concat_string":"","password_length":"10"},"expiration_settings":{"expiration_type":"NEVER_EXPIRE","valid_during_dates":{"time_zone":"America/Los_Angeles","start_date_time":{"day_of_month":"20","month":"4","year":"2021","hour_of_day":"15","minute_of_hour":"30"},"end_date_time":{"day_of_month":"25","month":"4","year":"2021","hour_of_day":"5","minute_of_hour":"30"}},"valid_for_time_period":{"valid_time_period_after":"ID_CREATION","after_id_creation_settings":{"valid_time_period":"2","valid_time_period_unit":"HOUR"},"after_first_login_settings":{"valid_time_period":"12","valid_time_period_unit":"WEEK","first_login_within":"5","first_login_within_unit":"DAY"}},"valid_daily":{"daily_start_hour":"20","daily_start_minute":"59","daily_end_hour":"22","daily_end_minute":"59"},"expiration_action":"SHOW_MESSAGE","post_expiration_action":{"enable_credentials_renewal":"true","enable_delete_immediately":"false","delete_after_value":"30","delete_after_unit":"DAY"}},"delivery_settings":{"email_template_id":"52001","sms_template_id":"53001"}}'
    log  ${RESP}
    [Return]  ${RESP}

create and get ppsk group id
    [Documentation]  create ppsk user group
    [Arguments]  ${NAME}
    ${RESP}=  create ppsk user group  ${NAME}
    ${ID}=  get json values  ${RESP}  key=id
    [Return]  ${ID}

get ppsk usergroups
    [Documentation]  get all ppsk usergroups
    ${RESP}=  rest api get  ${PPSK_USERGROUP_URI}
    log  ${RESP}
    [Return]  ${RESP}

delete ppsk usergroup
    [Documentation]  delete ppsk usergroup
    [Arguments]  ${PPSK_USERGROUP_ID}
    log  ${PPSK_USERGROUP_ID}
    ${RESP}=  rest api delete  ${PPSK_USERGROUP_URI}  ${PPSK_USERGROUP_ID}
    log  ${RESP}
    [Return]  ${RESP}



#####  PPSK USER Keywords   #####
create ppsk user
    [Documentation]  create ppsk user
    [Arguments]  ${PPSK_USER_GROUP_ID}  ${PPSK_USER_NAME}
    ${RESP}=  rest api post  ${PPSK_USER_URI}  '{"user_group_id": ${PPSK_USER_GROUP_ID}, "user_name": "${PPSK_USER_NAME}"}'

    log  ${RESP}
    [Return]  ${RESP}

create and get ppsk user id
    [Documentation]  create ppsk user
    [Arguments]  ${NAME}
    ${RESP}=  create ppsk user  ${PPSK_USER_GROUP_ID}  ${NAME}
    ${ID}=  get json values  ${RESP}  key=id
    [Return]  ${ID}

get ppsk users
    [Documentation]  get all ppsk users
    [Arguments]  ${PPSK_USERNAME}
    ${RESP}=  rest api get  ${PPSK_USER_URI}?usernames=${PPSK_USERNAME}
    log  ${RESP}
    [Return]  ${RESP}

delete ppsk user
    [Documentation]  delete ppsk user
    [Arguments]  ${PPSK_USERID}
    ${RESP}=  rest api delete  ${PPSK_USER_URI}  ${PPSK_USERID}
    log  ${RESP}
    [Return]  ${RESP}




*** Test Cases ***

# generate the key once per suite
Pre Condition-Login
    [Documentation]   Login and generate access_token
    [Tags]                  xim_tc_16480     development
    
    ${ACCESS_TOKEN}=        generate_access_token    ${tenant_username}      ${tenant_password}      login
    set global variable     ${ACCESS_TOKEN}
    
Pre Condition-UserGroup
    [Documentation]         create ppsk usergroup
    [Tags]                  xim_tc_6678     development
    
    ${PPSK_USER_GROUP_ID}=   create and get ppsk group id   ${PPSK_USERGROUP_GLOBAL}
    set global variable  ${PPSK_USER_GROUP_ID}

TC-6677: create ppsk usergroup
    [Documentation]         create ppsk usergroup
    [Tags]                  xim_tc_6677     development
    
    ${RESP}=  create ppsk user group  ${PPSK_USERGROUP}
    ${id}=  get json values  ${RESP}  key=id

    should be true  ${id}>0

    [Teardown]
    delete ppsk usergroup  ${id}


TC-6676: PPSK-Get list of PPSK user groups
    [Documentation]         fetch ppsk usergroups
    [Tags]                  xim_tc_6676     development
    
    ${CREATE_RESP}=  create ppsk user group  ${PPSK_USERGROUP}
    ${id}=  get json values  ${CREATE_RESP}  key=id
    ${RESP}=  get ppsk usergroups
    ${count}=  get json values  ${RESP}  key=count
    should be true  ${count}>0

    [Teardown]
    delete ppsk usergroup  ${id}


TC-16308: Create PPSK User for a particular user group with EMAIL and SMS
    [Documentation]         Create PPSK User for a particular user group with EMAIL and SMS
    [Tags]                  xim_tc_16308     development
    
    ${RESP}=  create ppsk user     ${PPSK_USER_GROUP_ID}  ${PPSK_USERNAME}
    ${user_id}=  get json values  ${RESP}  key=id

    should be true  ${user_id}>0

    [Teardown]
    delete ppsk user  ${user_id}

TC-16319: PPSK-Get list of PPSK users
    [Documentation]         PPSK-Get list of PPSK users
    [Tags]                  xim_tc_16319       development
    
    ${RESP}=  create ppsk user     ${PPSK_USER_GROUP_ID}  ${PPSK_USERNAME}
    ${user_id}=  get json values  ${RESP}  key=id
    ${READ_RESP}=  get ppsk users   ${PPSK_USERNAME}
    ${count}=  get json values  ${READ_RESP}  key=count
    should be true  ${count}>0

    [Teardown]
    delete ppsk user  ${user_id}
    delete ppsk usergroup  ${PPSK_USER_GROUP_ID}
