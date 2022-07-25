*** Settings ***

Library     common/Xapi.py
Library     common/Cli.py
Library     common/Utils.py


Variables   Environments/Config/waits.yaml



*** Keywords ***
#####  Revoke Access Token  #####
xapi logout
    [Documentation]  Revoke current Access Token
    [Arguments]     ${access_token}

    ${RESP}=  rest api post     /logout    access_token=${access_token}    result_code=200
    log                             ${RESP}
    [Return]                        ${RESP}
