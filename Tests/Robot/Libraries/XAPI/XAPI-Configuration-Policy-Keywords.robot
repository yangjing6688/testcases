*** Variables ***

${CCGS_URI}             /ccgs

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
xapi Update Cloud Control Group
    [Documentation]     update the cloud control group by Id
    [Arguments]         ${ID}    ${DATA}
    log                 update the cloud control group URL: ${CCGS_URI}/${ID}
    log                 update the cloud control group DATA: ${DATA}
    ${RESP} =           rest api put   ${CCGS_URI}/${ID}     ${DATA}
    log                 update the cloud control group resp: ${RESP}
    [Return]            ${RESP}

#####  Delete Cloud Control Group By ID  #####
xapi Delete Cloud Control Group
    [Documentation]     delete cloud control group by Id
    [Arguments]         ${ID}
    log                 delete cloud control group -- URI/ID: ${CCGS_URI}/${ID}
    ${RESP_CODE} =      rest api delete     ${CCGS_URI}    ${ID}
    [Return]            ${RESP_CODE}
