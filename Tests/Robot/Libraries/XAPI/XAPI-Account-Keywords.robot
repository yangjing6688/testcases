*** Variables ***
${DEVICE_PASSWORD_URI}=  /account/viq/default-device-password

*** Settings ***

Library     common/Xapi.py
Library     common/Cli.py
Library     common/Utils.py


Variables   Environments/Config/waits.yaml


*** Keywords ***


#####  Get default device password Keywords   #####
Get Default Device Password
    [Documentation]  get the default device password
    ${RESP}=  rest api get  ${DEVICE_PASSWORD_URI}
    ${PASSWORD}=  get json values  ${RESP}  key=password
    log  ${PASSWORD}
    [Return]  ${PASSWORD}

#####  Change default device password Keywords   #####
Change Default Device Password
    [Documentation]  change device password
    [Arguments]  ${PASSWORD}
    ${RESPCODE}=  rest api put v1  ${DEVICE_PASSWORD_URI}    ${PASSWORD}
    [Return]  ${RESPCODE}
