*** Variables ***

${NETWORK_POLICY_URI}=          /network-policies

*** Settings ***


Library     common/Xapi.py
Library     common/Cli.py
Library     common/Utils.py

Variables   Environments/Config/waits.yaml




*** Keywords ***
#####  LIST Network Policies  #####
xapi List Network Policies
    [Documentation]  list network policies
    ${RESP}=  rest api get  ${NETWORK_POLICY_URI}
    log  ${RESP}
    [Return]  ${RESP}

#####  Get Network Policy By ID  #####
xapi Get Network Policy
    [Documentation]  get network policy by id
    [Arguments]  ${ID}
    log  ${ID}
    ${RESP}=  rest api get  ${NETWORK_POLICY_URI}/${ID}
    [Return]  ${RESP}

#####  Create Network Policy  #####
xapi Create Network Policy
    [Documentation]  create network policy
    [Arguments]     ${PAYLOAD}
    ${RESP}=  rest api post v3  ${NETWORK_POLICY_URI}      ${PAYLOAD}      result_code=201
    log  ${RESP}
    [Return]  ${RESP}
	
#####  Assign Network Policy to Multiple Devices  #####
xapi assign network policy to multiple devices
    [Documentation]  Assign Network Policy to Multiple Devices
    [Arguments]  ${DEVICE_ID_1}    ${DEVICE_ID_2}   ${NETWORK_POLICY_ID}

    ${RESP}=  rest api post     /devices/network-policy/:assign     post_data='{"devices": {"ids": [${DEVICE_ID_1},${DEVICE_ID_2}]},"network_policy_id": ${NETWORK_POLICY_ID}}'      result_code=200
    log                             ${RESP}
    [Return]                        ${RESP}

#####  Assign Network Policy to a Device  #####
xapi assign network policy to a device
    [Documentation]  Assign Network Policy to a Device
    [Arguments]  ${DEVICE_ID}   ${NETWORK_POLICY_ID}

    ${RESP}=  rest api post    /devices/network-policy/:assign      post_data='{"devices": {"ids": [${DEVICE_ID}]},"network_policy_id": ${NETWORK_POLICY_ID}}'     result_code=200
    log                             ${RESP}
    [Return]                        ${RESP}
	

#####  Update Network Policy By ID  #####
xapi Update Network Policy
    [Documentation]  update network policy by id
    [Arguments]  ${ID}      ${REQ_BODY}
    log  ${ID}
    log  ${REQ_BODY}
    ${RESP}=  rest api put  ${NETWORK_POLICY_URI}/:${ID}    ${REQ_BODY}
    [Return]  ${RESP}

#####  Delete Network Policy By ID  #####
xapi Delete Network Policy
    [Documentation]  delete network policy by id
    [Arguments]  ${ID}
    log  ${ID}
    ${RESPCODE}=  rest api delete  ${NETWORK_POLICY_URI}/${ID}
    [Return]  ${RESPCODE}
