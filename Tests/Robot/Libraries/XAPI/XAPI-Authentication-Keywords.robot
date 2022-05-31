*** Settings ***


Library     common/Xapi.py
Library     common/Cli.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/extreme_location/ExtremeLocation.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/AdditionalSettings.py

Library     common/TestFlow.py
Library     common/Utils.py

Library     xiq/flows/manage/Devices.py
Library     Collections


#Resource    ../../XAPI_PHASE_5A/Resources/AllResources.robot
#Resource    Tests/Robot/Libraries/XIQ/Wireless/XAPI/XAPI-Production-Sanity-Keywords.robot

Variables   Environments/Config/waits.yaml
Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}



*** Keywords ***
#####  Revoke Access Token  #####
xapi logout
    [Documentation]  Revoke current Access Token
    [Arguments]

    ${RESP}=  rest api post      /logout        result_code=200
    log                             ${RESP}
    [Return]                        ${RESP}