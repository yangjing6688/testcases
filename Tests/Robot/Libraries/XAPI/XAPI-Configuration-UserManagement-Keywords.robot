*** Settings ***
Library     common/TestFlow.py
Library     common/Xapi.py
Library     common/Utils.py

*** Variables ***
${PPSK_USERGROUP_URI}=  /usergroups
${PPSK_USER_URI}=  /endusers
${PPSK_UPDATE_USER_URI}=  /endusers/:id


*** Keywords ***

#####  PPSK USER Group Keywords   #####

xapi create ppsk user group
    [Documentation]  create ppsk user group
    [Arguments]  ${NAME}
    ${RESP}=  rest api post v3  ${PPSK_USERGROUP_URI}  '{"name":"${NAME}","description":"AShortDescription","password_db_location":"CLOUD","password_type":"PPSK","enable_max_clients_per_ppsk":"false","max_clients_per_ppsk":"0","pcg_use_only":"false","pcg_type":"AP_BASED","ppsk_use_only":"false","enable_cwp_reg":"false","password_settings":{"enable_letters":"true","enable_numbers":"true","enable_special_characters":"true","password_character_types":"INCLUDE_ALL_CHARACTER_TYPE_ENABLED","psk_generation_method":"USER_STRING_PASSWORD","password_concat_string":"","password_length":"10"},"expiration_settings":{"expiration_type":"NEVER_EXPIRE","valid_during_dates":{"time_zone":"America/Los_Angeles","start_date_time":{"day_of_month":"20","month":"4","year":"2021","hour_of_day":"15","minute_of_hour":"30"},"end_date_time":{"day_of_month":"25","month":"4","year":"2021","hour_of_day":"5","minute_of_hour":"30"}},"valid_for_time_period":{"valid_time_period_after":"ID_CREATION","after_id_creation_settings":{"valid_time_period":"2","valid_time_period_unit":"HOUR"},"after_first_login_settings":{"valid_time_period":"12","valid_time_period_unit":"WEEK","first_login_within":"5","first_login_within_unit":"DAY"}},"valid_daily":{"daily_start_hour":"20","daily_start_minute":"59","daily_end_hour":"22","daily_end_minute":"59"},"expiration_action":"SHOW_MESSAGE","post_expiration_action":{"enable_credentials_renewal":"true","enable_delete_immediately":"false","delete_after_value":"30","delete_after_unit":"DAY"}},"delivery_settings":{"email_template_id":"52001","sms_template_id":"53001"}}'
    log  ${RESP}
    ${id}=  get json values  ${RESP}  key=id
    [Return]    ${id}

xapi get ppsk usergroups
    [Documentation]  get all ppsk usergroups
    ${RESP}=  rest api get  ${PPSK_USERGROUP_URI}
    log  ${RESP}
    ${count}=  get json values  ${RESP}  key=total_count
    [Return]  ${count}

xapi delete ppsk usergroup
    [Documentation]  delete ppsk usergroup
    [Arguments]  ${PPSK_USERGROUP_ID}
    log  ${PPSK_USERGROUP_ID}
    ${RESP}=  rest api delete  ${PPSK_USERGROUP_URI}  ${PPSK_USERGROUP_ID}
    log  ${RESP}
    [Return]  ${RESP}


#####  PPSK USER Keywords   #####
xapi create ppsk user
    [Documentation]  create ppsk user
    [Arguments]  ${PPSK_USER_GROUP_ID}  ${PPSK_USER_NAME}
    ${RESP}=  rest api post v3  ${PPSK_USER_URI}  '{"user_group_id": ${PPSK_USER_GROUP_ID}, "user_name": "${PPSK_USER_NAME}"}'
    log  ${RESP}
    ${user_id}=  get json values  ${RESP}  key=id
    [Return]  ${user_id}

xapi get ppsk users
    [Documentation]  get all ppsk users
    [Arguments]  ${PPSK_USERNAME}
    ${RESP}=  rest api get  ${PPSK_USER_URI}?usernames=${PPSK_USERNAME}
    log  ${RESP}
    ${count}=  get json values  ${RESP}  key=total_count
    [Return]  ${count}

xapi delete ppsk user
    [Documentation]  delete ppsk user
    [Arguments]  ${PPSK_USERID}
    ${RESP}=  rest api delete  ${PPSK_USER_URI}  ${PPSK_USERID}
    log  ${RESP}
    [Return]  ${RESP}
