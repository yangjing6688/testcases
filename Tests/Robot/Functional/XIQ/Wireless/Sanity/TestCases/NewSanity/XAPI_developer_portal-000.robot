                                                                                                                                                # Author        : Shreen Banu
# Date          : Dec 2022
# Description   : XAPI Developer Portal Validation
#
# Topology      :   None

*** Variables ***

*** Settings ***
Library     extauto/common/Rest.py

Resource    Tests/Robot/Libraries/XIQ/lib_url_validation.robot

Variables    Environments/${TOPO}

Force Tags  testbed_none

*** Keywords ***

*** Test Cases ***
TCCS-13220: XAPI Developer Portal Validation
    [Documentation]         XAPI Developer Portal Validation

    [Tags]                  production      tccs_13220

    ${XIQ_Instance}   ${length} =          Get XIQ Instance from URL   ${CLOUD_GDC_URL}
    Should not be equal as strings  "${XIQ_Instance}"   "Unknown"

    ${developer_portal}     ${developer_portal_documentation}   ${developer_portal_api_docs}     ${developer_portal_swagger_ui}     ${ENV_TYPE} =     Generate Developer Portal URL    ${XIQ_Instance}   ${length}
    Should not be equal as strings  "${ENV_TYPE}"   "Unknown"

    ${Status_url1} =   Get Http Response Code     ${developer_portal}
    Should be equal as Integers     ${Status_url1}     200

    ${Status_url2} =   Get Http Response Code     ${developer_portal_documentation}
    Should be equal as Integers     ${Status_url2}     200

    ${Status_url3} =   Get Http Response Code     ${developer_portal_api_docs}
    Should be equal as Integers     ${Status_url3}     200

    ${Status_url4} =   Get Http Response Code     ${developer_portal_swagger_ui}
    Should be equal as Integers     ${Status_url4}     200

    ${result} =   Validate unresolved directive   ${developer_portal_api_docs}
    Should Be Equal As Integers     ${result}       -1 
