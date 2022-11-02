# Author        : Jerome Ly
# Date          : 31 May 2022
# Description   : XAPI - Radio Profile Common Objects

# Topology:
# ---------
#    ScriptHost
#      |________
#      |        |
#     Cloud     AP
# Pre-config:
# -----------
#
#

# Execution Command:
# ------------------
# robot  -v TOPO:topo.test.cp1r1.yaml New_API_5C_XIQ-3375.robot
#


*** Variables ***

${RADIO_PROFILE_URI}            /radio-profiles

${NEIGHBOR_ANALYSIS_URI}        ${RADIO_PROFILE_URI}/neighborhood-analysis

${CHANNEL_SELECTION_URI}        ${RADIO_PROFILE_URI}/channel-selection

${RADIO_USAGE_OPT_URI}          ${RADIO_PROFILE_URI}/radio-usage-opt

${MISCELLANEOUS_URI}            ${RADIO_PROFILE_URI}/miscellaneous

${WMM_QOS_URI}                  ${RADIO_PROFILE_URI}/wmm-qos

${MAC_OUIS_URI}                 ${RADIO_PROFILE_URI}/mac-ouis

${SENSOR_SCAN_URI}              ${RADIO_PROFILE_URI}/sensor-scan

*** Settings ***
Force Tags  testbed_1_node

Library     common/Xapi.py
Library     common/Cli.py
Library     common/TestFlow.py
Library     common/Utils.py
Library     Collections

Resource    Tests/Robot/Libraries/XAPI/XAPI-Authentication-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Configuration-Policy-Keywords.robot

Variables   Environments/Config/waits.yaml
Variables   Environments/${TOPO}

*** Test Cases ***

Pre Condition
    [Tags]                      tcxm_16480    development
#Login and Generate Access Token
    ${ACCESS_TOKEN} =           xapi login    ${tenant_username}      ${tenant_password}
    should not be empty         ${ACCESS_TOKEN}
    set suite variable          ${ACCESS_TOKEN}


# Radio Profile Test Cases
# ------------------------
TC-21315: create radio profile for APs
    [Documentation]         create radio profile for APs
    [Tags]                  tcxm_21315   development
    ${RESP} =               xapi create radio settings   ${RADIO_PROFILE_URI}    '{"name": "simple_radio_profile", "description": "Creating radio profile made easy."}'
    ${RADIO_PROFILE_ID} =   get json values     ${RESP}     key=id
    should be true          ${RADIO_PROFILE_ID} > 0
    set suite variable     ${RADIO_PROFILE_ID}

    ${NEIGHBOR_ANALYSIS_ID} =   get json values     ${RESP}     key=neighborhood_analysis_id
    should be true          ${NEIGHBOR_ANALYSIS_ID} > 0
    set suite variable     ${NEIGHBOR_ANALYSIS_ID}

    ${CHANNEL_SELECTION_ID} =   get json values     ${RESP}     key=channel_selection_id
    should be true          ${CHANNEL_SELECTION_ID} > 0
    set suite variable     ${CHANNEL_SELECTION_ID}

    ${RADIO_USAGE_OPT_ID} =   get json values     ${RESP}     key=radio_usage_optimization_id
    should be true          ${RADIO_USAGE_OPT_ID} > 0
    set suite variable     ${RADIO_USAGE_OPT_ID}

    ${MISCELLANEOUS_ID} =   get json values     ${RESP}     key=miscellaneous_settings_id
    should be true          ${MISCELLANEOUS_ID} > 0
    set suite variable     ${MISCELLANEOUS_ID}

    ${SENSOR_SCAN_ID} =     get json values     ${RESP}     key=sensor_scan_settings_id
    should be true          ${SENSOR_SCAN_ID} > 0
    set suite variable     ${SENSOR_SCAN_ID}

TC-21316: list all radio profiles
    [Documentation]         list radio profiles
    [Tags]                  tcxm_21316   development
    ${RESP} =               xapi list radio settings     ${RADIO_PROFILE_URI}
    ${count} =              get json values     ${RESP}     key=total_count
    should be true          ${count} > 0

TC-21331: get radio profile by ID
    [Documentation]         get radio profile by ID
    [Tags]                  tcxm_21331   development
    Depends On              TC-21315
    ${RESP} =               xapi get radio settings      ${RADIO_PROFILE_URI}    ${RADIO_PROFILE_ID}
    ${id} =                 get json values     ${RESP}     key=id
    should be true          ${id}==${RADIO_PROFILE_ID}

TC-21317: update radio profile by id
    [Documentation]         update radio profile by id
    [Tags]                  tcxm_21317   development
    Depends On              TC-21315
    ${RESP} =               xapi update radio settings   ${RADIO_PROFILE_URI}     ${RADIO_PROFILE_ID}     {"name": "simple_radio_profile_for_APs"}
    ${name} =               get json values     ${RESP}     key=name
    should be equal as strings      '${name}'   'simple_radio_profile_for_APs'


# Radio Neighborhood Analysis Test Cases
# --------------------------------------

TC-21372: get radio neighborhood analysis
    [Documentation]         get radio neighborhood analysis by id
    [Tags]                  tcxm_21372   development
    Depends On              TC-21315
    ${RESP} =               xapi get radio settings      ${NEIGHBOR_ANALYSIS_URI}    ${NEIGHBOR_ANALYSIS_ID}
    ${id} =                 get json values     ${RESP}     key=id
    should be true          ${id}==${NEIGHBOR_ANALYSIS_ID}

TC-21373: update radio neighborhood analysis
    [Documentation]         update radio neighborhood analysis by id
    [Tags]                  tcxm_21373   development
    Depends On              TC-21315
    ${RESP} =               xapi update radio settings   ${NEIGHBOR_ANALYSIS_URI}     ${NEIGHBOR_ANALYSIS_ID}     {"enable_background_scan": false}
    ${enable_background_scan} =     get json values     ${RESP}     key=enable_background_scan
    should be true    ${enable_background_scan}==False


# Radio Channel Selection Test Cases
# ----------------------------------

TC-21346: get radio channel selection
    [Documentation]         get radio channel selection by id
    [Tags]                  tcxm_21346   development
    Depends On              TC-21315
    ${RESP} =               xapi get radio settings      ${CHANNEL_SELECTION_URI}    ${CHANNEL_SELECTION_ID}
    ${id} =                 get json values     ${RESP}     key=id
    should be true          ${id}==${CHANNEL_SELECTION_ID}

TC-21347: update radio channel selection
    [Documentation]         update radio channel selection by id
    [Tags]                  tcxm_21347   development
    Depends On              TC-21315
    ${RESP} =               xapi update radio settings   ${CHANNEL_SELECTION_URI}     ${CHANNEL_SELECTION_ID}     {"rf_interference_threshold": 50}
    ${rf_interference_threshold} =     get json values     ${RESP}     key=rf_interference_threshold
    should be true    ${rf_interference_threshold}==50


# Radio MAC OUI Test Cases
# -----------------------------------

TC-21357: create product MAC OUI
    [Documentation]         create product MAC OUI for APs
    [Tags]                  tcxm_21357   development
    ${RESP} =               xapi create radio settings   ${MAC_OUIS_URI}    '{"name": "New-005C00", "description": "Create New MAC Device 005C00.", "value": "005C00"}'
    ${MAC_OUIS_ID} =        get json values     ${RESP}     key=id
    should be true          ${MAC_OUIS_ID} > 0
    set suite variable     ${MAC_OUIS_ID}

TC-21356: list all product MAC OUIs
    [Documentation]         list product MAC OUIs
    [Tags]                  tcxm_21356   development
    ${RESP} =               xapi list radio settings     ${MAC_OUIS_URI}
    ${count} =              get json values     ${RESP}     key=total_count
    should be true          ${count} > 0

TC-21358: get product MAC OUI info
    [Documentation]         get product MAC OUI info by id
    [Tags]                  tcxm_21358   development
    Depends On              TC-21315    TC-21357
    ${RESP} =               xapi get radio settings      ${MAC_OUIS_URI}    ${MAC_OUIS_ID}
    ${id} =                 get json values     ${RESP}     key=id
    should be true          ${id}==${MAC_OUIS_ID}

TC-21359: update product MAC OUI info
    [Documentation]         update product MAC OUI info by id
    [Tags]                  tcxm_21359   development
    Depends On              TC-21315    TC-21357
    ${RESP} =               xapi update radio settings   ${MAC_OUIS_URI}     ${MAC_OUIS_ID}     {"name": "Generic Brand", "value": "00FF00"}
    ${mac_oui} =            get json values     ${RESP}     key=value
    should be equal as strings    '${mac_oui}'    '00FF00'

TC-21360: delete product MAC OUI info
    [Documentation]         delete product MAC OUI info by id
    [Tags]                  tcxm_21360   development
    Depends On              TC-21315    TC-21357
    ${RESP_CODE} =          xapi delete radio settings   ${MAC_OUIS_URI}     ${MAC_OUIS_ID}
    should be true          ${RESP_CODE} == 1

    ${RESP} =               xapi get radio settings     ${MAC_OUIS_URI}    ${MAC_OUIS_ID}
    ${error_message} =      get json values     ${RESP}     key=error_message
    should be equal as strings      '${error_message}'   'INVALID_ARGUMENT: core.service.data.object.with.id.not.found'


# Radio Miscellaneous Settings Test Cases
# ---------------------------------------

TC-21361: get radio miscellaneous settings
    [Documentation]         get radio miscellaneous settings by id
    [Tags]                  tcxm_21361   development
    Depends On              TC-21315
    ${RESP} =               xapi get radio settings      ${MISCELLANEOUS_URI}    ${MISCELLANEOUS_ID}
    ${id} =                 get json values     ${RESP}     key=id
    should be true          ${id}==${MISCELLANEOUS_ID}

    ${wmm_qos_settings} =   get json values     ${RESP}     key=wmm_qos_settings
    ${count} =              Get Length	${wmm_qos_settings}
    should be true          ${count} > 0

    ${wmm_qos} =            Get From List   ${wmm_qos_settings}     0
    ${WMM_QOS_ID} =         get json values     ${wmm_qos}     key=id
    should be true          ${WMM_QOS_ID} > 0
    set suite variable     ${WMM_QOS_ID}

TC-21362: update radio miscellaneous settings
    [Documentation]         update radio miscellaneous settings by id
    [Tags]                  tcxm_21362   development
    Depends On              TC-21315
    ${RESP} =               xapi update radio settings   ${MISCELLANEOUS_URI}     ${MISCELLANEOUS_ID}     {"sla_throughput_level": "HIGH_DENSITY", "radio_range": 5000}
    ${sla_throughput_level} =     get json values     ${RESP}     key=sla_throughput_level
    should be equal as strings    '${sla_throughput_level}'    'HIGH_DENSITY'


# Radio Profile Clean-Up Test Cases
# ---------------------------------

TC-21318: delete radio profile by id
    [Documentation]         delete radio profile by id
    [Tags]                  tcxm_21318   development
    Depends On              TC-21315

    [Teardown]
    ${RESP_CODE} =          xapi delete radio settings   ${RADIO_PROFILE_URI}     ${RADIO_PROFILE_ID}
    should be true          ${RESP_CODE} == 1

    ${RESP} =               xapi get radio settings     ${RADIO_PROFILE_URI}    ${RADIO_PROFILE_ID}
    ${error_message} =      get json values     ${RESP}     key=error_message
    should be equal as strings      '${error_message}'   'INVALID_ARGUMENT: core.service.data.object.with.id.not.found'
