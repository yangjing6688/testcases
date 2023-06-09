*** Variables ***
${VLAN_PROFILE_URL}=               /vlan-profiles
${VLAN_PROFILE_ID}=                -1

*** Settings ***
Library     extauto/common/TestFlow.py
Library     extauto/common/Xapi.py
Library     extauto/common/Utils.py
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     extauto/xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     extauto/xiq/flows/configure/CommonObjects.py

Variables   Environments/Config/waits.yaml

*** Keywords ***

#####  Get VLAN profiles list   #####
xapi List VLAN Profiles
    [Documentation]  List VLAN profiles
    ${RESP}=  rest api get  ${VLAN_PROFILE_URL}
    log  ${RESP}
    [Return]  ${RESP}

##### Create VLAN profile  #####
xapi Create VLAN profile
    [Documentation]  create VLAN profile
    [Arguments]  ${REQ_BODY}
    ${RESP}=  rest api post v3  ${VLAN_PROFILE_URL}      ${REQ_BODY}      result_code=201
    log  ${RESP}
    [Return]  ${RESP}

#####  Get a VLAN profile By ID  #####
xapi Get VLAN profile
    [Documentation]  get a VLAN profile by id
    [Arguments]  ${ID}
    log  ${ID}
    ${RESP}=  rest api get  ${VLAN_PROFILE_URL}/${ID}
    [Return]  ${RESP}

#####  Update a VLAN profile By ID  #####
xapi Update VLAN profile
    [Documentation]  update a VLAN profile by id
    [Arguments]  ${ID}      ${REQ_BODY}
    log  ${ID}
    log  ${REQ_BODY}
    ${RESP}=  rest api patch  ${VLAN_PROFILE_URL}/${ID}    ${REQ_BODY}   result_code=201
    [Return]  ${RESP}

#####  Delete VLAN profile By ID  #####
xapi Delete VLAN profile
    [Documentation]  delete VLAN profile by id
    [Arguments]  ${ID}
    log  ${ID}
    ${RECODE}=  rest api delete  ${VLAN_PROFILE_URL}    ${ID}
    [Return]  ${RECODE}

#####  Delete VLAN profiles By IDs  #####
xapi Delete VLAN profiles
    [Documentation]  delete VLAN profiles by id
    [Arguments]  ${REQ_IDS}
    ${RESP}=  rest api post  ${VLAN_PROFILE_URL}     ${REQ_IDS}
    log  ${RESP}
    [Return]  ${RESP}

