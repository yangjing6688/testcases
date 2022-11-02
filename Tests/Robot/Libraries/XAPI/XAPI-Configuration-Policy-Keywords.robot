*** Variables ***

${CCGS_URI}                     /ccgs

*** Settings ***

Library     common/Xapi.py
Library     common/Cli.py
Library     common/Utils.py

Variables   Environments/Config/waits.yaml

*** Keywords ***

#####  Get Cloud Control Group By ID #####
xapi Get Cloud Control Group
    [Documentation]     get the cloud config group by Id
    [Arguments]         ${ID}
    log                 get cloud control group URL: ${CCGS_URI}/${ID}
    ${RESP} =           rest api get     ${CCGS_URI}/${ID}
    [Return]            ${RESP}

#####  Create Cloud Control Group  #####
xapi Create Cloud Control Group
    [Documentation]     Post new cloud config group request with data
    [Arguments]         ${DATA}
    ${RESP} =           rest api post v3    ${CCGS_URI}    '${DATA}'
    log                 create cloud control group -- RESP: ${RESP}
    [Return]            ${RESP}

#####  Update Cloud Control Group By ID #####
xapi xapi Update Cloud Control Group
    [Documentation]     update the cloud control group by Id
    [Arguments]         ${ID}    ${DATA}
    log                 update the cloud control group URL: ${CCGS_URI}/${ID}
    log                 update the cloud control group DATA: ${DATA}
    ${RESP} =           rest api put   ${CCGS_URI}/${ID}     ${DATA}
    log                 update the cloud control group resp: ${RESP}
    [Return]            ${RESP}

#####  Delete Cloud Control Group By ID  #####
xapi xapi Delete Cloud Control Group
    [Documentation]     delete cloud control group by Id
    [Arguments]         ${ID}
    log                 delete cloud control group -- URI/ID: ${CCGS_URI}/${ID}
    ${RESP_CODE} =      rest api delete     ${CCGS_URI}    ${ID}
    [Return]            ${RESP_CODE}


#####  List Radio Settings  #####
xapi List Radio Settings
    [Documentation]     list radio settings
    [Arguments]         ${URI}
    log                 list radio settings -- URI: ${URI}
    ${RESP} =           rest api get        ${URI}
    log                 list radio settings -- RESP: ${RESP}
    [Return]            ${RESP}

#####  Get Radio Settings By ID #####
xapi Get Radio Settings
    [Documentation]     get radio settings by id
    [Arguments]         ${URI}      ${ID}
    log                 get radio settings by id -- URI/ID: ${URI}/${ID}
    ${RESP} =           rest api get      ${URI}/${ID}
    [Return]            ${RESP}

#####  Get Radio Settings After By ID #####
xapi Get Radio Settings After
    [Documentation]     get radio settings after by id
    [Arguments]         ${URI}      ${ID}
    log                 get radio settings after by id -- URI/ID: ${URI}/${ID}
    ${RESP} =           rest api get v1     ${URI}/${ID}
    [Return]            ${RESP}

#####  Create Radio Settings  #####
xapi Create Radio Settings
    [Documentation]     create radio settings
    [Arguments]         ${URI}      ${DATA}
    ${RESP} =           rest api post v3    ${URI}    ${DATA}
    log                 create radio settings -- RESP: ${RESP}
    [Return]            ${RESP}

#####  Update Radio Settings By ID  #####
xapi Update Radio Settings
    [Documentation]     update radio settings by id
    [Arguments]         ${URI}   ${ID}   ${DATA}
    log                 update radio settings by id -- URI/ID: ${URI}/${ID}
    log                 update radio settings by id -- DATA: ${DATA}
    ${RESP} =           rest api put    ${URI}/${ID}    ${DATA}     result_code="response_map"
    [Return]            ${RESP}

#####  Delete Radio Settings By ID  #####
xapi Delete Radio Settings
    [Documentation]     delete radio settings by id
    [Arguments]         ${URI}   ${ID}
    log                 delete radio settings by id -- URI/ID: ${URI}/${ID}
    ${RESP_CODE} =      rest api delete     ${URI}    ${ID}
    [Return]            ${RESP_CODE}

