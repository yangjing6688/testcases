# Author        : Shreen Banu
# Date          : Aug 2022
# Description   : Product URL Validation
#
# Topology      :   None

*** Variables ***
${mapping}      dellsnstmapping
${serial_num}   24301900000000
${Tag}          72XGLN2

*** Settings ***
Library     extauto/common/Rest.py

Resource    Tests/Robot/Libraries/XIQ/lib_product_url.robot

Variables    Environments/${TOPO}

Force Tags  testbed_none

*** Keywords ***

*** Test Cases ***
TCCS-13221: ProductInfo URL validation
    [Documentation]         ProductInfo URL validation

    [Tags]                  production      tccs_13221

    ${result}   ${length} =          Get XIQ Instance from URL   ${CLOUD_GDC_URL}
    Should not be equal as strings  "${result}"   "Unknown" 

    ${product_url}  ${ENV_TYPE} =     Generate Product URL    ${result}   ${length}
    Should not be equal as strings  "${ENV_TYPE}"   "Unknown"

    skip if  "${ENV_TYPE}" != "Production"  and "${ENV_TYPE}" != "Unknown"
        ${complete_product_url}=    Set variable    ${product_url}/${mapping}/${serial_num}

        ${ProductURL_Status} =   Get Http Response Code     ${complete_product_url}
        Should be equal as Integers     ${ProductURL_Status}     200

        ${Service_Tag} =   Get Http Data     ${complete_product_url}
        Should contain  ${Service_Tag}  ${Tag}
