*** Variables ***

${index_value}=    0

*** Settings ***

Library     Collections
Library     common/Xapi.py
Library     common/Cli.py
Library     common/Utils.py


Variables   Environments/Config/waits.yaml


*** Keywords ***

xapi get first page audit logs
    [Documentation]  Get first page audit logs, max 100 counts.

    ${AUDIT_LOG_URL}=    set variable    /logs/audit?page=1&limit=100&categories=
    Log    AUDIT_LOG_URL = ${AUDIT_LOG_URL}
    ${AUDIT_LOG_CONTENT}=  rest api get      ${AUDIT_LOG_URL}
    [Return]    ${AUDIT_LOG_CONTENT}


xapi list first page audit logs by keyword
    [Documentation]  Get first page audit logs by keyword.
    [Arguments]      ${KEYWORD}

    ${AUDIT_LOG_URL}=    set variable    /logs/audit?page=1&limit=100&categories=&keyword=${KEYWORD}
    Log    AUDIT_LOG_URL = ${AUDIT_LOG_URL}
    ${AUDIT_LOG_CONTENT}=  rest api get      ${AUDIT_LOG_URL}
    [Return]    ${AUDIT_LOG_CONTENT}


xapi list first page audit logs by category and keyword
    [Documentation]  Get first page audit logs by category and keyword.
    [Arguments]      ${CATEGORY}    ${KEYWORD}

    #The available CATEGORY is: ADMIN, CONFIG, DEPLOYMENT, MONITOR, ALARM, SYSTEM
    ${AUDIT_LOG_URL}=    set variable    /logs/audit?page=1&limit=100&categories=${CATEGORY}&keyword=${KEYWORD}
    Log    AUDIT_LOG_URL = ${AUDIT_LOG_URL}
    ${AUDIT_LOG_CONTENT}=  rest api get      ${AUDIT_LOG_URL}
    [Return]    ${AUDIT_LOG_CONTENT}


xapi list first page audit logs by user and keyword
    [Documentation]  Get first page audit logs by admin user and keyword.
    [Arguments]      ${ADMIN_USER}    ${KEYWORD}

    ${AUDIT_LOG_URL}=    set variable    /logs/audit?page=1&limit=100&categories=&username=${ADMIN_USER}&keyword=${KEYWORD}
    Log    AUDIT_LOG_URL = ${AUDIT_LOG_URL}
    ${AUDIT_LOG_CONTENT}=  rest api get      ${AUDIT_LOG_URL}
    [Return]    ${AUDIT_LOG_CONTENT}


xapi list first page audit logs by category user and keyword
    [Documentation]  Get first page audit logs by category user and keyword.
    [Arguments]      ${CATEGORY}    ${ADMIN_USER}    ${KEYWORD}

    #The available CATEGORY is: ADMIN, CONFIG, DEPLOYMENT, MONITOR, ALARM, SYSTEM
    ${AUDIT_LOG_URL}=    set variable    /logs/audit?page=1&limit=100&categories=${CATEGORY}&username=${ADMIN_USER}&keyword=${KEYWORD}
    Log    AUDIT_LOG_URL = ${AUDIT_LOG_URL}
    ${AUDIT_LOG_CONTENT}=  rest api get      ${AUDIT_LOG_URL}
    [Return]    ${AUDIT_LOG_CONTENT}


xapi get audit log count
    [Documentation]  Get audit logs count from log contents.
    [Arguments]      ${AUDIT_LOG_CONTENT}

    Log     AUDIT_LOG_CONTENT = ${AUDIT_LOG_CONTENT}
    ${LOG_COUNT}=  get json values      ${AUDIT_LOG_CONTENT}     key=total_count
    ${LOG_COUNT_INT}=    convert to integer    ${LOG_COUNT}
    Log     LOG_COUNT=${LOG_COUNT}; LOG_COUNT_INT=${LOG_COUNT_INT}
    [Return]    ${LOG_COUNT_INT}


xapi get audit log data
    [Documentation]  Get audit logs data from log contents.
    [Arguments]      ${AUDIT_LOG_CONTENT}

    Log     AUDIT_LOG_CONTENT = ${AUDIT_LOG_CONTENT}
    ${LOG_DATA}=  get json values      ${AUDIT_LOG_CONTENT}     key=data
    Log     LOG_DATA = ${LOG_DATA}
    [Return]    ${LOG_DATA}


xapi get admin user list from audit log data
    [Documentation]  Get admin user list from audit logs data.
    [Arguments]      ${AUDIT_LOG_DATA}

    Log     AUDIT_LOG_DATA = ${AUDIT_LOG_DATA}
    @{ADMIN_USER_LIST}    create list
    FOR     ${LOG_DATA}    IN    @{AUDIT_LOG_DATA}
            ${ADMIN_USER}=  get json values      ${LOG_DATA}     key=username
            append to list    ${ADMIN_USER_LIST}    ${ADMIN_USER}
    END
    [Return]    ${ADMIN_USER_LIST}


xapi get category list from audit log data
    [Documentation]  Get category list from audit logs data.
    [Arguments]      ${AUDIT_LOG_DATA}

    Log     AUDIT_LOG_DATA = ${AUDIT_LOG_DATA}
    @{CATEGORY_LIST}    create list
    FOR     ${LOG_DATA}    IN    @{AUDIT_LOG_DATA}
            ${CATEGORY}=  get json values      ${LOG_DATA}     key=category
            append to list    ${CATEGORY_LIST}    ${CATEGORY}
    END
    [Return]    ${CATEGORY_LIST}


xapi get description list from audit log data
    [Documentation]  Get description list from audit logs data.
    [Arguments]      ${AUDIT_LOG_DATA}

    Log     AUDIT_LOG_DATA = ${AUDIT_LOG_DATA}
    @{DESCRIPT_LIST}    create list
    FOR     ${LOG_DATA}    IN    @{AUDIT_LOG_DATA}
            ${DESCRIPT}=  get json values      ${LOG_DATA}     key=description
            append to list    ${DESCRIPT_LIST}    ${DESCRIPT}
    END
    [Return]    ${DESCRIPT_LIST}


xapi get timestamp list from audit log data
    [Documentation]  Get timestamp list from audit logs data.
    [Arguments]      ${AUDIT_LOG_DATA}

    Log     AUDIT_LOG_DATA = ${AUDIT_LOG_DATA}
    @{TIMESTAMPT_LIST}    create list
    FOR     ${LOG_DATA}    IN    @{AUDIT_LOG_DATA}
            ${TIMESTAMPT}=  get json values      ${LOG_DATA}     key=timestamp
            append to list    ${TIMESTAMPT_LIST}    ${TIMESTAMPT}
    END
    [Return]    ${TIMESTAMPT_LIST}