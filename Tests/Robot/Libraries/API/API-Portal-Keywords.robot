*** Settings ***

Library     Collections
Library     common/Xapi.py
Library     common/Cli.py
Library     common/Utils.py



*** Keywords ***

api datacenter sdwan
    [Documentation]  api get the list of RDCs that deployed sdwan

    ${PORTAL_DA_URL}=    set variable    /acsportal/datacenters/sdwan
    Log    PORTAL_DA_URL = ${PORTAL_DA_URL}
    ${DARACENTER_SDWAN_CONTENT}=  rest api get      ${PORTAL_DA_URL}
    [Return]    ${DARACENTER_SDWAN_CONTENT}
