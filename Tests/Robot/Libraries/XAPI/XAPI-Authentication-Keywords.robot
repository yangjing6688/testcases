*** Settings ***

Library     common/Xapi.py
Library     common/Cli.py
Library     common/Utils.py


Variables   Environments/Config/waits.yaml

*** Keywords ***

#### Generate new Access Token #####
xapi login
    [Documentation]             Generate the Access Token
    [Arguments]                 ${login_name}      ${password}
    ${ACCESS_TOKEN} =           generate_access_token    ${login_name}      ${password}      login
    log                         generated access token -- ${ACCESS_TOKEN}
    [Return]                    ${ACCESS_TOKEN}


#####  Revoke Access Token  #####
xapi logout
    [Documentation]  Revoke current Access Token
    [Arguments]     ${access_token}

    ${RESP}=  rest api post     /logout    access_token=${access_token}    result_code=200
    log                             ${RESP}
    [Return]                        ${RESP}
