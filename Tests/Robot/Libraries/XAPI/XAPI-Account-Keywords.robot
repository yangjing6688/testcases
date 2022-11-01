*** Variables ***
${DEVICE_PASSWORD_URI}=  /account/viq/default-device-password

*** Settings ***

Library     common/Xapi.py
Library     common/Cli.py
Library     common/Utils.py


Variables   Environments/Config/waits.yaml


*** Keywords ***


#####  Get default device password Keywords   #####
xapi get default device password
    [Documentation]  get the default device password in global settings
    ${RESP}=  rest api get  ${DEVICE_PASSWORD_URI}
    ${PASSWORD}=  get json values  ${RESP}  key=password
    log  ${PASSWORD}
    [Return]  ${PASSWORD}

#####  Change default device password Keywords   #####
xapi change default device password
    [Documentation]  change default device password in global settings
    [Arguments]  ${PASSWORD}
    ${RESPCODE}=  rest api put v1  ${DEVICE_PASSWORD_URI}    ${PASSWORD}
    [Return]  ${RESPCODE}
