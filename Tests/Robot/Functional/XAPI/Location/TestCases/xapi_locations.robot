# Author        : Subanesh Amarasekaran
# Date          : 22 Oct 2022
# Description   : XAPI

# Topology:
# ---------
#    ScriptHost/AutoIQ
#      |________
#      |        |
#     Cloud     AP
# Pre-config:
# -----------
#
#
#
# Execution Command:
# ------------------
# robot -v TESTBED:dev_blr_tb_1 -v TOPO:g2r1-xapi-1 -e user_inputs_required xapi_topology.robot
#
# Please make sure your setup robot file contains bleow variables to run this test suite
#   ${XAPI_BASE_URL}                    https://g2-api.qa.xcloudiq.com
#   ${TENANT_USERNAME}                  surendranandyala1990@gmail.com
#   ${TENANT_PASSWORD}                  Aerohive123
#

# Script transformed from https://github.extremenetworks.com/Engineering/cw_automation/blob/master/testsuites/xiq/xapi/xapi_topology.robot


*** Variables ***
${LOCATION_1}                         XAPI-Topology-Location-1
${LOCATION_2}                         XAPI-Topology-Location-2

${BUILDING_1}                         XAPI-Topology-Building-1
${BUILDING_2}                         XAPI-Topology-Building-2
${BUILDING_1_ADDR}                    Address-01
${BUILDING_2_ADDR}                    Address-02

${FLOOR_1}                            XAPI-Topology-Floor-1
${FLOOR_2}                            XAPI-Topology-Floor-2

${WRONG_ID}                           999999999
${ERROR_CODE_STR}                     error_code

${FLOOR_PLAN_1_PNG}                   Resources/floorplan-1.png
${FLOOR_PLAN_2_PNG}                   Resources/floorplan-2.png
${FLOOR_PLAN_3_JPG}                   Resources/floorplan-3.jpg
${FLOOR_PLAN_4_JPEG}                  Resources/floorplan-4.jpeg
${FLOOR_PLAN_5_GIF}                   Resources/floorplan-5.gif
${FLOOR_PLAN_3000KB_JPG}              Resources/floorplan-3000KB.jpg
${FLOOR_PLAN_ERROR_MSG}               Failed to parse multipart servlet request
${FLOOR_PLAN_MAX_SIZE_ERROR_MSG}      Maximum upload size exceeded


*** Settings ***

Resource    Tests/Robot/Libraries/XAPI/XAPI-Authentication-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Configuration-Deployment-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Network-Policy-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Device-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Location-Keywords.robot

Variables   Environments/Config/waits.yaml
Variables   Environments/${TOPO}

Force Tags  testbed_none

Suite Setup     Pre Condition



*** Keywords ***
# generate the key once per suite
Pre Condition
    ${ACCESS_TOKEN}=        generate_access_token    ${tenant_username}      ${tenant_password}      login
    set suite variable     ${ACCESS_TOKEN}
    Log    Checking the Access Token not equal to -1
    skip if     '${ACCESS_TOKEN}' == '-1'
    
    #Get Root Location ID

    ${ROOT_LOCATION_ID}=    xapi get root location id
    set suite variable     ${ROOT_LOCATION_ID}

    
*** Test Cases ***
TCXM-6759: Topology-Create LOCATION
    [Documentation]         TCXM-6759: Topology-Create LOCATION
    [Tags]                  development      tcxm_6759
    
    ${LOCATION_6759_1}=  Set Variable  XAPI-Topology-Location-6759-1
    ${LOCATION_6759_2}=  Set Variable  XAPI-Topology-Location-6759-2
    ${BUILDING_6759_1}=  Set Variable  XAPI-Topology-Building-6759-1
    ${BUILDING_6759_2}=  Set Variable  XAPI-Topology-Building-6759-2
    ${BUILDING_6759_1_ADDR} =  Set Variable  Address-01-6759
    ${BUILDING_6759_2_ADDR} =  Set Variable  Address-02-6759
    ${FLOOR_6759} =  Set Variable  XAPI-Topology-Floor-6759
    
    ${LOCATION_6759_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6759_1}
    #Check whether location created or not
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}        ${LOCATION_6759_1}

    set suite variable      ${LOCATION_6759_ID}

    [Teardown]
    xapi delete location  ${LOCATION_6759_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6759_1}


TCXM-6760: Topology-Create multiple LOCATION's
    [Documentation]         TCXM-6760: Topology-Create multiple LOCATION's
    [Tags]                  development      tcxm_6760
    
    ${LOCATION_6760_1}=  Set Variable  XAPI-Topology-Location-6760-1
    ${LOCATION_6760_2}=  Set Variable  XAPI-Topology-Location-6760-2
    ${BUILDING_6760_1}=  Set Variable  XAPI-Topology-Building-6760-1
    ${BUILDING_6760_2}=  Set Variable  XAPI-Topology-Building-6760-2
    ${BUILDING_6760_1_ADDR} =  Set Variable  Address-01-6760
    ${BUILDING_6760_2_ADDR} =  Set Variable  Address-02-6760
    ${FLOOR_6760} =  Set Variable  XAPI-Topology-Floor-6760
    
   
    ${LOCATION_6760_1_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6760_1}
    ${LOCATION_6760_2_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6760_2}
    #Check whether location created or not
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}        ${LOCATION_6760_1}
    should contain          ${RESPONSE}        ${LOCATION_6760_2}

    [Teardown]
    xapi delete location  ${LOCATION_6760_1_ID}
    xapi delete location  ${LOCATION_6760_2_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6760_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6760_2}


TCXM-6761: Topology-Update LOCATION by ID
    [Documentation]         TCXM-6761: Topology-Update LOCATION by ID
    [Tags]                  development      tcxm_6761
    
    ${LOCATION_6761_1}=  Set Variable  XAPI-Topology-Location-6761-1
    ${LOCATION_6761_2}=  Set Variable  XAPI-Topology-Location-6761-2
    ${BUILDING_6761_1}=  Set Variable  XAPI-Topology-Building-6761-1
    ${BUILDING_6761_2}=  Set Variable  XAPI-Topology-Building-6761-2
    ${BUILDING_6761_1_ADDR} =  Set Variable  Address-01-6761
    ${BUILDING_6761_2_ADDR} =  Set Variable  Address-02-6761
    ${FLOOR_6761} =  Set Variable  XAPI-Topology-Floor-6761
    
    ${LOCATION_6761_1_ID} =       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6761_1}
    #Check whether location created or not
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}        ${LOCATION_6761_1}

    ${LOCATION_1_ID} =  xapi update location         ${ROOT_LOCATION_ID}     ${LOCATION_6761_1_ID}    ${LOCATION_6761_2}
    #${LOCATION_1_ID}=       xapi update location         ${ROOT_LOCATION_ID}     ${LOCATION_6761_1_ID}    ${LOCATION_6761_2}
    sleep  5
    #Check whether location name is updated or not
    ${RESPONSE}=            xapi get locations tree string
    should not contain          ${RESPONSE}        ${LOCATION_6761_1}
    should contain              ${RESPONSE}        ${LOCATION_6761_2}

    [Teardown]
    xapi delete Location  ${LOCATION_6761_1_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6761_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6761_2}


TCXM-6762: Topology-Delete LOCATION by ID
    [Documentation]  TCXM-6762: Topology-Delete LOCATION by ID
    [Tags]           development      tcxm_6762
    Log     "This flow will be covered as part of xapi delete location keyword usage in other test cases"


TCXM-6763: Topology-Create BUILDING
    [Documentation]         TCXM-6763: Topology-Create BUILDING
    [Tags]                  development      tcxm_6763
    
    ${LOCATION_6763_1}=  Set Variable  XAPI-Topology-Location-6763-1
    ${LOCATION_6763_2}=  Set Variable  XAPI-Topology-Location-6763-2
    ${BUILDING_6763_1}=  Set Variable  XAPI-Topology-Building-6763-1
    ${BUILDING_6763_2}=  Set Variable  XAPI-Topology-Building-6763-2
    ${BUILDING_6763_1_ADDR}=  Set Variable  Address-01-6763
    ${BUILDING_6763_2_ADDR}=  Set Variable  Address-02-6763
    ${FLOOR_6763}=  Set Variable  XAPI-Topology-Floor-6763
    
    ${LOCATION_6763_1_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6763_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${LOCATION_6763_1}

    ${BUILDING_6763_1_ID}=       xapi create building         ${LOCATION_6763_1_ID}     ${BUILDING_6763_1}     ${BUILDING_6763_1_ADDR}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${BUILDING_6763_1}

    [Teardown]
    xapi delete building  ${BUILDING_6763_1_ID}
    xapi delete location  ${LOCATION_6763_1_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${BUILDING_6763_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6763_1}


TCXM-6764: Topology-Create multiple BUILDINGs
    [Documentation]         TCXM-6764: Topology-Create multiple BUILDINGs
    [Tags]                  development      tcxm_6764
    
    ${LOCATION_6764_1}=  Set Variable  XAPI-Topology-Location-6764-1
    ${LOCATION_6764_2}=  Set Variable  XAPI-Topology-Location-6764-2
    ${BUILDING_6764_1}=  Set Variable  XAPI-Topology-Building-6764-1
    ${BUILDING_6764_2}=  Set Variable  XAPI-Topology-Building-6764-2
    ${BUILDING_6764_1_ADDR}=  Set Variable  Address-01-6764
    ${BUILDING_6764_2_ADDR}=  Set Variable  Address-02-6764
    ${FLOOR_6764}=  Set Variable  XAPI-Topology-Floor-6764
    
    ${LOCATION_6764_1_ID}=       xapi create Location         ${ROOT_LOCATION_ID}     ${LOCATION_6764_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${LOCATION_6764_1}

    ${BUILDING_6764_1_ID}=       xapi create building         ${LOCATION_6764_1_ID}     ${BUILDING_6764_1}     ${BUILDING_6764_1_ADDR}
    ${BUILDING_6764_2_ID}=       xapi create building         ${LOCATION_6764_1_ID}     ${BUILDING_6764_2}     ${BUILDING_6764_2_ADDR}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${BUILDING_6764_1}
    should contain          ${RESPONSE}             ${BUILDING_6764_2}

    [Teardown]
    xapi delete building  ${BUILDING_6764_1_ID}
    xapi delete building  ${BUILDING_6764_2_ID}
    xapi delete location  ${LOCATION_6764_1_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${BUILDING_6764_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${BUILDING_6764_2}
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6764_1}


TCXM-6765: Topology-Update BUILDING by ID
    [Documentation]         TCXM-6765: Topology-Update BUILDING by ID
    [Tags]                  development      tcxm_6765
    
    ${LOCATION_6765_1}=  Set Variable  XAPI-Topology-Location-6765-1
    ${BUILDING_6765_1}=  Set Variable  XAPI-Topology-Building-6765-1
    ${BUILDING_6765_2}=  Set Variable  XAPI-Topology-Building-6765-2
    ${BUILDING_6765_1_ADDR}=  Set Variable  Address-01-6765-1
    ${FLOOR_6765}=  Set Variable  XAPI-Topology-Floor-6765
    
    ${LOCATION_6765_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6765_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${LOCATION_6765_1}

    ${BUILDING_6765_ID}=       xapi create building         ${LOCATION_6765_ID}     ${BUILDING_6765_1}     ${BUILDING_6765_1_ADDR}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${BUILDING_6765_1}

    ${BUILDING_6765_ID}=       xapi update building         ${LOCATION_6765_ID}     ${BUILDING_6765_ID}    ${BUILDING_6765_2}
    sleep  5
    #Check whether location name is updated or not
    ${RESPONSE}=            xapi get locations tree string
    should not contain          ${RESPONSE}        ${BUILDING_6765_1}
    should contain              ${RESPONSE}        ${BUILDING_6765_2}

    [Teardown]
    xapi delete building  ${BUILDING_6765_ID}
    xapi delete location  ${LOCATION_6765_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${BUILDING_6765_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${BUILDING_6765_2}
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6765_1}


TCXM-6766: Topology-Delete BUILDING by ID
    [Documentation]  TCXM-6766: Topology-Delete BUILDING by ID
    [Tags]           development      tcxm_6766
    Log     "This flow will be coverd as part of xapi delete building keyword usage in other test cases"


TCXM-6767: Topology-Create FLOOR
    [Documentation]         TCXM-6767: Topology-Create FLOOR
    [Tags]                  development      tcxm_6767
    
    ${LOCATION_6767}=  Set Variable  XAPI-Topology-Location-6767
    ${BUILDING_6767}=  Set Variable  XAPI-Topology-Building-6767
    ${BUILDING_6767_ADDR} =  Set Variable  Address-01-6767
    ${FLOOR_6767} =  Set Variable  XAPI-Topology-Floor-6767

     
    ${LOCATION_6767_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6767}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${LOCATION_6767}

    ${BUILDING_6767_ID}=       xapi create building         ${LOCATION_6767_ID}     ${BUILDING_6767}     ${BUILDING_6767_ADDR}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${BUILDING_6767}

    ${FLOOR_6767_ID}=          xapi create floor            ${BUILDING_6767_ID}     ${FLOOR_6767}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${FLOOR_6767}

    [Teardown]
    xapi delete floor     ${FLOOR_6767_ID}
    xapi delete building  ${BUILDING_6767_ID}
    xapi delete location  ${LOCATION_6767_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${FLOOR_6767}
    should not contain                ${LOCATIONS_TREE_STRING}            ${BUILDING_6767}
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6767}


TCXM-6768: Topology-Create multiple FLOORs
    [Documentation]         TC-6768: Topology-Create multiple FLOORs
    [Tags]                  development      tcxm_6768
    
    ${LOCATION_6768_1}=  Set Variable  XAPI-Topology-Location-6768-1
    ${LOCATION_6768_2}=  Set Variable  XAPI-Topology-Location-6768-2
    ${BUILDING_6768_1}=  Set Variable  XAPI-Topology-Building-6768-1
    ${BUILDING_6768_2}=  Set Variable  XAPI-Topology-Building-6768-2
    ${BUILDING_6768_1_ADDR} =  Set Variable  Address-01-6768
    ${BUILDING_6768_2_ADDR} =  Set Variable  Address-02-6768
    ${FLOOR_6768_1} =  Set Variable  XAPI-Topology-Floor-6768-1
    ${FLOOR_6768_2} =  Set Variable  XAPI-Topology-Floor-6768-2
    
    ${LOCATION_6768_1_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6768_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${LOCATION_6768_1}

    ${BUILDING_6768_1_ID}=       xapi create building         ${LOCATION_6768_1_ID}     ${BUILDING_6768_1}  ${BUILDING_6768_1_ADDR}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${BUILDING_6768_1}

    ${FLOOR_6768_1_ID}=          xapi create floor            ${BUILDING_6768_1_ID}     ${FLOOR_6768_1}
    ${FLOOR_6768_2_ID}=          xapi create floor            ${BUILDING_6768_1_ID}     ${FLOOR_6768_2}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${FLOOR_6768_1}
    should contain          ${RESPONSE}             ${FLOOR_6768_2}

    [Teardown]
    xapi delete floor     ${FLOOR_6768_1_ID}
    xapi delete floor     ${FLOOR_6768_2_ID}
    xapi delete building  ${BUILDING_6768_1_ID}
    xapi delete location  ${LOCATION_6768_1_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${FLOOR_6768_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${FLOOR_6768_2}
    should not contain                ${LOCATIONS_TREE_STRING}            ${BUILDING_6768_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6768_1}


TCXM-6769: Topology-Update FLOOR by ID
    [Documentation]         TCXM-6769: Topology-Update FLOOR by ID
    [Tags]                  development      tcxm_6769
    
    ${LOCATION_6769_1}=  Set Variable  XAPI-Topology-Location-6769-1
    ${LOCATION_6769_2}=  Set Variable  XAPI-Topology-Location-6769-2
    ${BUILDING_6769_1}=  Set Variable  XAPI-Topology-Building-6769-1
    ${BUILDING_6769_2}=  Set Variable  XAPI-Topology-Building-6769-2
    ${BUILDING_6769_1_ADDR} =  Set Variable  Address-01-6769
    ${BUILDING_6769_2_ADDR} =  Set Variable  Address-02-6769
    ${FLOOR_6769_1} =  Set Variable  XAPI-Topology-Floor-6769-1
    ${FLOOR_6769_2} =  Set Variable  XAPI-Topology-Floor-6769-2
    
    ${LOCATION_6769_1_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6769_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${LOCATION_6769_1}

    ${BUILDING_6769_1_ID}=       xapi create building         ${LOCATION_6769_1_ID}     ${BUILDING_6769_1}     ${BUILDING_6769_1_ADDR}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${BUILDING_6769_1}

    ${FLOOR_6769_1_ID}=          xapi create floor            ${BUILDING_6769_1_ID}     ${FLOOR_6769_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${FLOOR_6769_1}

    ${FLOOR_6769_1_ID}=          xapi update floor            ${BUILDING_6769_1_ID}     ${FLOOR_6769_1_ID}    ${FLOOR_6769_2}
    sleep  5
    #Check whether location name is updated or not
    ${RESPONSE}=            xapi get locations tree string
    should not contain          ${RESPONSE}        ${FLOOR_6769_1}
    should contain              ${RESPONSE}        ${FLOOR_6769_2}

    [Teardown]
    xapi delete floor     ${FLOOR_6769_1_ID}
    xapi delete building  ${BUILDING_6769_1_ID}
    xapi delete location  ${LOCATION_6769_1_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${FLOOR_6769_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${FLOOR_6769_2}
    should not contain                ${LOCATIONS_TREE_STRING}            ${BUILDING_6769_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6769_1}


TCXM-6770: Topology-Delete FLOOR by ID
    [Documentation]  TCXM-6770: Topology-Delete FLOOR by ID
    [Tags]           development      tcxm_6770
    Log     "This flow will be coverd as part of xapi delete floor keyword usage in other test cases"


#TCXM-6771: Topology-Upload floor plan
#    [Documentation]     TCXM-6771: Topology-Upload floor plan
#    [Tags]              development  tcxm_6771
#    #Uploading floor plan image of type PNG
#    Log                     Uploading ${FLOOR_PLAN_1_PNG} image
#    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${FLOOR_PLAN_1_PNG}
#    should not contain      ${RESPONSE_STRING}                              ${ERROR_CODE_STR}


#TCXM-6772: Topology-Upload floor plan with various file types - JPG, PNG
#    [Documentation]     TCXM-6771: Topology-Upload floor plan
#    [Tags]              development  tcxm_6772
#    #Uploading floor plan image of type JPG
#    Log                     Uploading ${FLOOR_PLAN_3_JPG} image
#    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${FLOOR_PLAN_3_JPG}
#    should not contain      ${RESPONSE_STRING}                              ${ERROR_CODE_STR}

#   #Uploading floor plan image of type PNG
#    Log                     Uploading ${FLOOR_PLAN_1_PNG} image
#    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${FLOOR_PLAN_1_PNG}
#    should not contain      ${RESPONSE_STRING}                              ${ERROR_CODE_STR}


#TCXM-6773: Topology-Upload multiple floor plan
#    [Documentation]     TCXM-6771: Topology-Upload floor plan
#    [Tags]              development  tcxm_6773
#    #Uploading floor plan image of type PNG
#    Log                     Uploading ${FLOOR_PLAN_1_PNG} image
#    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${FLOOR_PLAN_1_PNG}
#    should not contain      ${RESPONSE_STRING}          ${ERROR_CODE_STR}

#    #Uploading floor plan image of type PNG
#    Log                     Uploading ${FLOOR_PLAN_2_PNG} image
#    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${FLOOR_PLAN_2_PNG}
#    should not contain      ${RESPONSE_STRING}                              ${ERROR_CODE_STR}


TCXM-6774: NEG-Topology-xapi create location with no PARENT ID and/or Location Name
    [Documentation]         TC-6774: NEG-Topology-xapi create location with no PARENT ID and/or Location Name
    [Tags]                  development      tcxm_6774
    
    ${LOCATION_6774_1}=  Set Variable  XAPI-Topology-Location-6774-1
    ${LOCATION_6774_2}=  Set Variable  XAPI-Topology-Location-6774-2
    ${BUILDING_6774_1}=  Set Variable  XAPI-Topology-Building-6774-1
    ${BUILDING_6774_2}=  Set Variable  XAPI-Topology-Building-6774-2
    ${BUILDING_6774_1_ADDR} =  Set Variable  Address-01-6774
    ${BUILDING_6774_2_ADDR} =  Set Variable  Address-02-6774
    ${FLOOR_6774_1} =  Set Variable  XAPI-Topology-Floor-6774-1
    ${FLOOR_6774_2} =  Set Variable  XAPI-Topology-Floor-6774-2
    
    ${RESPONSE}=              xapi create location with no parent id       ${LOCATION_6774_1}
    ${RESPONSE_STRING}=       get json value as string                ${RESPONSE}
    should contain     ${RESPONSE_STRING}      ${ERROR_CODE_STR}

    ${RESPONSE}=              xapi create location with no name            ${ROOT_LOCATION_ID}
    ${RESPONSE_STRING}=       get json value as string                ${RESPONSE}
    should contain     ${RESPONSE_STRING}      ${ERROR_CODE_STR}


TCXM-6775: NEG-Topology-xapi create location with incorrect PARENT ID of GLOBAL VIEW
    [Documentation]         TCXM-6775: NEG-Topology-xapi create location with incorrect PARENT ID of GLOBAL VIEW
    [Tags]                  development      tcxm_6775
    
    ${LOCATION_6775_1}=  Set Variable  XAPI-Topology-Location-6775-1
    
    ${LOCATION_6775_1_ID}=       xapi create location         ${WRONG_ID}     ${LOCATION_6775_1}
    should be equal as integers     ${LOCATION_6775_1_ID}      -1


TCXM-6777: NEG-Topology-Update LOCATION with incorrect PARENT ID of GLOBAL VIEW and/or Location ID
    [Documentation]         TCXM-6777: NEG-Topology-Update LOCATION with incorrect PARENT ID of GLOBAL VIEW and/or Location ID
    [Tags]                  development      tcxm_6777
    
    ${LOCATION_6777_1}=  Set Variable  XAPI-Topology-Location-6777-1
    ${LOCATION_6777_2}=  Set Variable  XAPI-Topology-Location-6777-2
    
    ${LOCATION_6777_1_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6777_1}
    #Check whether location created or not
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}        ${LOCATION_6777_1}

    #Update LOCATION with incorrect PARENT ID of GLOBAL VIEW
    ${RESPONSE}=            xapi update location and get api response        ${WRONG_ID}     ${LOCATION_6777_1_ID}    ${LOCATION_6777_2}
    ${RESPONSE_STRING}=     get json value as string                    ${RESPONSE}
    should contain          ${RESPONSE_STRING}        ${ERROR_CODE_STR}

    #Update LOCATION with incorrect Location ID
    ${RESPONSE}=            xapi update location and get api response        ${ROOT_LOCATION_ID}     ${WRONG_ID}    ${LOCATION_6777_2}
    ${RESPONSE_STRING}=     get json value as string                    ${RESPONSE}
    should contain          ${RESPONSE_STRING}        ${ERROR_CODE_STR}

    [Teardown]
    xapi delete location  ${LOCATION_6777_1_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6777_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6777_2}


TCXM-6779: NEG-Topology-Delete LOCATION by providing incorrect location ID
    [Documentation]         TCXM-6779: NEG-Topology-Delete LOCATION by providing incorrect location ID
    [Tags]                  development      tcxm_6779
    ${RESPONSE}=              xapi delete location                   ${WRONG_ID}
    ${RESPONSE_STRING}=       get json value as string          ${RESPONSE}
    should contain     ${RESPONSE_STRING}      ${ERROR_CODE_STR}


TCXM-6780: NEG-Topology-Delete LOCATION which has building and floor under it
    [Documentation]         TCXM-6780: NEG-Topology-Delete LOCATION which has building and floor under it
    [Tags]                  development      tcxm_6780
    
    ${LOCATION_6780_1}=  Set Variable  XAPI-Topology-Location-6780-1
    ${LOCATION_6780_2}=  Set Variable  XAPI-Topology-Location-6780-2
    ${BUILDING_6780_1}=  Set Variable  XAPI-Topology-Building-6780-1
    ${BUILDING_6780_2}=  Set Variable  XAPI-Topology-Building-6780-2
    ${BUILDING_6780_1_ADDR} =  Set Variable  Address-01-6780
    ${BUILDING_6780_2_ADDR} =  Set Variable  Address-02-6780
    ${FLOOR_6780_1} =  Set Variable  XAPI-Topology-Floor-6780-1
    ${FLOOR_6780_2} =  Set Variable  XAPI-Topology-Floor-6780-2
    
    
    ${LOCATION_6780_1_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6780_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${LOCATION_6780_1}

    ${BUILDING_6780_1_ID}=       xapi create building         ${LOCATION_6780_1_ID}     ${BUILDING_6780_1}     ${BUILDING_6780_1_ADDR}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${BUILDING_6780_1}

    ${FLOOR_6780_1_ID}=          xapi create floor            ${BUILDING_6780_1_ID}     ${FLOOR_6780_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}                     ${FLOOR_6780_1}

    ${RESPONSE}=            xapi delete location                 ${LOCATION_6780_1_ID}
    ${RESPONSE_STRING}=     get json value as string        ${RESPONSE}
    should contain     ${RESPONSE_STRING}      ${ERROR_CODE_STR}

    [Teardown]
    xapi delete floor     ${FLOOR_6780_1_ID}
    xapi delete building  ${BUILDING_6780_1_ID}
    xapi delete location  ${LOCATION_6780_1_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${FLOOR_6780_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${BUILDING_6780_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6780_1}


TCXM-6781: NEG-Topology-xapi create building with no PARENT ID and/or NAME and/or ADDRESS
    [Documentation]         TCXM-6781: NEG-Topology-xapi create building with no PARENT ID and/or NAME and/or ADDRESS
    [Tags]                  development      tcxm_6781
    
    ${LOCATION_6781_1}=  Set Variable  XAPI-Topology-Location-6781-1
    ${LOCATION_6781_2}=  Set Variable  XAPI-Topology-Location-6781-2
    ${BUILDING_6781_1}=  Set Variable  XAPI-Topology-Building-6781-1
    ${BUILDING_6781_2}=  Set Variable  XAPI-Topology-Building-6781-2
    ${BUILDING_6781_1_ADDR} =  Set Variable  Address-01-6781
    ${BUILDING_6781_2_ADDR} =  Set Variable  Address-02-6781
    ${FLOOR_6781_1} =  Set Variable  XAPI-Topology-Floor-6781-1
    ${FLOOR_6781_2} =  Set Variable  XAPI-Topology-Floor-6781-2
    
    
    ${RESPONSE}=              xapi create building with no parent id       ${BUILDING_6781_1}
    ${RESPONSE_STRING}=       get json value as string                ${RESPONSE}
    should contain     ${RESPONSE_STRING}      ${ERROR_CODE_STR}

    ${LOCATION_6781_1_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6781_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${LOCATION_6781_1}

    ${RESPONSE}=            xapi create building with no name and address      ${LOCATION_6781_1_ID}
    ${RESPONSE_STRING}=     get json value as string                      ${RESPONSE}
    should contain          ${RESPONSE_STRING}                            ${ERROR_CODE_STR}

    [Teardown]
    xapi delete location  ${LOCATION_6781_1_ID}
    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6781_1}


TCXM-6782: NEG-Topology-Create BUILDING with incorrect PARENT ID of Location
    [Documentation]         TCXM-6782: NEG-Topology-Create BUILDING with incorrect PARENT ID of Location
    [Tags]                  development      tcxm_6782
    
    ${LOCATION_6782_1}=  Set Variable  XAPI-Topology-Location-6782-1
    ${LOCATION_6782_2}=  Set Variable  XAPI-Topology-Location-6782-2
    ${BUILDING_6782_1}=  Set Variable  XAPI-Topology-Building-6782-1
    ${BUILDING_6782_2}=  Set Variable  XAPI-Topology-Building-6782-2
    ${BUILDING_6782_1_ADDR} =  Set Variable  Address-01-6782
    ${BUILDING_6782_2_ADDR} =  Set Variable  Address-02-6782
    ${FLOOR_6782_1} =  Set Variable  XAPI-Topology-Floor-6782-1
    ${FLOOR_6782_2} =  Set Variable  XAPI-Topology-Floor-6782-2
    
    ${BUILDING_6782_1_ID}=       xapi create building         ${WRONG_ID}     ${BUILDING_6782_1}     ${BUILDING_6782_1_ADDR}
    should be equal as integers                     ${BUILDING_6782_1_ID}      -1


TCXM-6784: NEG-Topology-Update BUILDING with incorrect PARENT ID of Location and/or BUILDING ID
    [Documentation]         TC-6784: NEG-Topology-Update BUILDING with incorrect PARENT ID of Location and/or BUILDING ID
    [Tags]                  development      tcxm_6784
    
    ${LOCATION_6784_1}=  Set Variable  XAPI-Topology-Location-6784-1
    ${LOCATION_6784_2}=  Set Variable  XAPI-Topology-Location-6784-2
    ${BUILDING_6784_1}=  Set Variable  XAPI-Topology-Building-6784-1
    ${BUILDING_6784_2}=  Set Variable  XAPI-Topology-Building-6784-2
    ${BUILDING_6784_1_ADDR} =  Set Variable  Address-01-6784
    ${BUILDING_6784_2_ADDR} =  Set Variable  Address-02-6784
    ${FLOOR_6784_1} =  Set Variable  XAPI-Topology-Floor-6784-1
    ${FLOOR_6784_2} =  Set Variable  XAPI-Topology-Floor-6784-2
    
    ${LOCATION_6784_1_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6784_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${LOCATION_6784_1}

    ${BUILDING_6784_1_ID}=       xapi create building         ${LOCATION_6784_1_ID}        ${BUILDING_6784_1}     ${BUILDING_6784_1_ADDR}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${BUILDING_6784_1}

    #Update BUILDING with incorrect PARENT ID of Building
    ${RESPONSE}=            xapi update building and get api response            ${WRONG_ID}         ${BUILDING_6784_1_ID}    ${BUILDING_6784_2}
    ${RESPONSE_STRING}=     get json value as string                        ${RESPONSE}
    should contain          ${RESPONSE_STRING}        ${ERROR_CODE_STR}

    #Update BUILDING with incorrect BUILDING ID
    ${RESPONSE}=            xapi update building and get api response            ${LOCATION_6784_1_ID}     ${WRONG_ID}        ${BUILDING_6784_2}
    ${RESPONSE_STRING}=     get json value as string                        ${RESPONSE}
    should contain          ${RESPONSE_STRING}        ${ERROR_CODE_STR}

    [Teardown]
    xapi delete building  ${BUILDING_6784_1_ID}
    xapi delete location  ${LOCATION_6784_1_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${BUILDING_6784_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${BUILDING_6784_2}
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6784_1}


TCXM-6786: NEG-Topology-Delete BUILDING by providing incorrect BUILDING ID
    [Documentation]         TCXM-6786: NEG-Topology-Delete BUILDING by providing incorrect BUILDING ID
    [Tags]                  development      tcxm_6786
    ${RESPONSE}=              xapi delete building                   ${WRONG_ID}
    ${RESPONSE_STRING}=       get json value as string          ${RESPONSE}
    should contain     ${RESPONSE_STRING}      ${ERROR_CODE_STR}


TCXM-6787: NEG-Topology-Delete BUILDING which has floor(s)under it
    [Documentation]         TCXM-6787: NEG-Topology-Delete BUILDING which has floor(s)under it
    [Tags]                  development      tcxm_6787

    ${LOCATION_6787_1}=  Set Variable  XAPI-Topology-Location-6787-1
    ${LOCATION_6787_2}=  Set Variable  XAPI-Topology-Location-6787-2
    ${BUILDING_6787_1}=  Set Variable  XAPI-Topology-Building-6787-1
    ${BUILDING_6787_2}=  Set Variable  XAPI-Topology-Building-6787-2
    ${BUILDING_6787_1_ADDR} =  Set Variable  Address-01-6787
    ${BUILDING_6787_2_ADDR} =  Set Variable  Address-02-6787
    ${FLOOR_6787_1} =  Set Variable  XAPI-Topology-Floor-6787-1
    ${FLOOR_6787_2} =  Set Variable  XAPI-Topology-Floor-6787-2


    ${LOCATION_6787_1_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6787_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${LOCATION_6787_1}

    ${BUILDING_6787_1_ID}=       xapi create building         ${LOCATION_6787_1_ID}     ${BUILDING_6787_1}     ${BUILDING_6787_1_ADDR}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${BUILDING_6787_1}

    ${FLOOR_6787_1_ID}=         xapi create floor            ${BUILDING_6787_1_ID}     ${FLOOR_6787_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}                     ${FLOOR_6787_1}

    ${RESPONSE}=            xapi delete building                 ${BUILDING_6787_1_ID}
    ${RESPONSE_STRING}=     get json value as string        ${RESPONSE}
    should contain     ${RESPONSE_STRING}      ${ERROR_CODE_STR}

    [Teardown]
    xapi delete floor     ${FLOOR_6787_1_ID}
    xapi delete building  ${BUILDING_6787_1_ID}
    xapi delete location  ${LOCATION_6787_1_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${FLOOR_6787_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${BUILDING_6787_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6787_1}


TCXM-6788: NEG-Topology-Create FLOOR with no PARAMETERS
    [Documentation]         TCXM-6788: NEG-Topology-Create FLOOR with no PARAMETERS
    [Tags]                  development      tcxm_6788
    
    ${LOCATION_6788_1}=  Set Variable  XAPI-Topology-Location-6788-1
    ${LOCATION_6788_2}=  Set Variable  XAPI-Topology-Location-6788-2
    ${BUILDING_6788_1}=  Set Variable  XAPI-Topology-Building-6788-1
    ${BUILDING_6788_2}=  Set Variable  XAPI-Topology-Building-6788-2
    ${BUILDING_6788_1_ADDR} =  Set Variable  Address-01-6788
    ${BUILDING_6788_2_ADDR} =  Set Variable  Address-02-6788
    ${FLOOR_6788_1} =  Set Variable  XAPI-Topology-Floor-6788-1
    ${FLOOR_6788_2} =  Set Variable  XAPI-Topology-Floor-6788-2
    
    
    #Create xapi create floor with no parent id
    ${RESPONSE}=              xapi create floor with no parent id          ${FLOOR_6788_1}
    ${RESPONSE_STRING}=       get json value as string                ${RESPONSE}
    should contain     ${RESPONSE_STRING}      ${ERROR_CODE_STR}

    #Create xapi create floor with no name
    ${LOCATION_1_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6788_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${LOCATION_6788_1}

    ${BUILDING_1_ID}=       xapi create building         ${LOCATION_1_ID}     ${BUILDING_6788_1}     ${BUILDING_6788_1_ADDR}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${BUILDING_6788_1}

    ${RESPONSE}=            xapi create floor with no name               ${BUILDING_1_ID}
    ${RESPONSE_STRING}=     get json value as string                ${RESPONSE}
    should contain          ${RESPONSE_STRING}                      ${ERROR_CODE_STR}

    [Teardown]
    xapi delete building  ${BUILDING_1_ID}
    xapi delete location  ${LOCATION_1_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${BUILDING_6788_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6788_1}


TCXM-6789: NEG-Topology-Create FLOOR with incorrect PARAMETERS
    [Documentation]         TCXM-6789: NEG-Topology-Create FLOOR with incorrect PARAMETERS
    [Tags]                  development      tcxm_6789
    
    ${LOCATION_6789_1}=  Set Variable  XAPI-Topology-Location-6789-1
    ${LOCATION_6789_2}=  Set Variable  XAPI-Topology-Location-6789-2
    ${BUILDING_6789_1}=  Set Variable  XAPI-Topology-Building-6789-1
    ${BUILDING_6789_2}=  Set Variable  XAPI-Topology-Building-6789-2
    ${BUILDING_6789_1_ADDR} =  Set Variable  Address-01-6789
    ${BUILDING_6789_2_ADDR} =  Set Variable  Address-02-6789
    ${FLOOR_6789_1} =  Set Variable  XAPI-Topology-Floor-6789-1
    ${FLOOR_6789_2} =  Set Variable  XAPI-Topology-Floor-6789-2
    
    ${LOCATION_6789_1_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6789_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${LOCATION_6789_1}

    ${BUILDING_6789_1_ID}=       xapi create building         ${LOCATION_6789_1_ID}     ${BUILDING_6789_1}     ${BUILDING_6789_1_ADDR}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${BUILDING_6789_1}

    ${FLOOR_6789_1_ID}=          xapi create floor with incorrect db attenuation    ${BUILDING_6789_1_ID}     ${FLOOR_6789_1}
    should be equal as integers     ${FLOOR_6789_1_ID}      -1

    [Teardown]
    xapi delete building  ${BUILDING_6789_1_ID}
    xapi delete location  ${LOCATION_6789_1_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${FLOOR_6789_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${BUILDING_6789_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6789_1}


TCXM-6791: NEG-Topology-Update FLOOR with incorrect PARAMETERS
    [Documentation]         TCXM-6791: NEG-Topology-Update FLOOR with incorrect PARAMETERS
    [Tags]                  development      tcxm_6791
    
    ${LOCATION_6791_1}=  Set Variable  XAPI-Topology-Location-6791-1
    ${LOCATION_6791_2}=  Set Variable  XAPI-Topology-Location-6791-2
    ${BUILDING_6791_1}=  Set Variable  XAPI-Topology-Building-6791-1
    ${BUILDING_6791_2}=  Set Variable  XAPI-Topology-Building-6791-2
    ${BUILDING_6791_1_ADDR} =  Set Variable  Address-01-6791
    ${BUILDING_6791_2_ADDR} =  Set Variable  Address-02-6791
    ${FLOOR_6791_1} =  Set Variable  XAPI-Topology-Floor-6791-1
    ${FLOOR_6791_2} =  Set Variable  XAPI-Topology-Floor-6791-2
    
    ${LOCATION_6791_1_ID}=       xapi create location         ${ROOT_LOCATION_ID}     ${LOCATION_6791_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${LOCATION_6791_1}

    ${BUILDING_6791_1_ID}=       xapi create building         ${LOCATION_6791_1_ID}     ${BUILDING_6791_1}     ${BUILDING_6791_1_ADDR}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${BUILDING_6791_1}

    ${FLOOR_6791_1_ID}=          xapi create floor            ${BUILDING_6791_1_ID}     ${FLOOR_6791_1}
    ${RESPONSE}=            xapi get locations tree string
    should contain          ${RESPONSE}             ${FLOOR_6791_1}

    #Update FLOOR with incorrect PARENT ID of Floor
    ${RESPONSE}=            xapi update floor and get api response            ${WRONG_ID}          ${FLOOR_6791_1_ID}    ${FLOOR_6791_2}
    ${RESPONSE_STRING}=     get json value as string                     ${RESPONSE}
    should contain          ${RESPONSE_STRING}                           ${ERROR_CODE_STR}

    #Update FLOOR with incorrect FLOOR ID
    ${RESPONSE}=            xapi update floor and get api response            ${BUILDING_6791_1_ID}     ${WRONG_ID}      ${FLOOR_6791_2}
    ${RESPONSE_STRING}=     get json value as string                     ${RESPONSE}
    should contain          ${RESPONSE_STRING}                           ${ERROR_CODE_STR}

    [Teardown]
    xapi delete floor     ${FLOOR_6791_1_ID}
    xapi delete building  ${BUILDING_6791_1_ID}
    xapi delete location  ${LOCATION_6791_1_ID}

    ${LOCATIONS_TREE_STRING}=         xapi get locations tree string
    should not contain                ${LOCATIONS_TREE_STRING}            ${FLOOR_6791_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${FLOOR_6791_2}
    should not contain                ${LOCATIONS_TREE_STRING}            ${BUILDING_6791_1}
    should not contain                ${LOCATIONS_TREE_STRING}            ${LOCATION_6791_1}


TCXM-6793: NEG-Topology-Delete FLOOR by providing incorrect FLOOR ID
    [Documentation]         TCXM-6793: NEG-Topology-Delete FLOOR by providing incorrect FLOOR ID
    [Tags]                  development      tcxm_6793
    ${RESPONSE}=              xapi delete floor                      ${WRONG_ID}
    ${RESPONSE_STRING}=       get json value as string          ${RESPONSE}
    should contain     ${RESPONSE_STRING}      ${ERROR_CODE_STR}


TCXM-6794: NEG-Topology-Upload floor plan with no image file
    [Documentation]     TCXM-6794: NEG-Topology-Upload floor plan with no image file
    [Tags]              development      tcxm_6794
    Log                     uploading floor plan with no image file
    ${RESPONSE_STRING}=     xapi upload floor plan with no image
    should contain          ${RESPONSE_STRING}                  ${ERROR_CODE_STR}
    should contain          ${RESPONSE_STRING}                  ${FLOOR_PLAN_ERROR_MSG}


#TCXM-6795: NEG-Topology-Upload floor plan with invalid file
#    [Documentation]     TCXM-6795: NEG-Topology-Upload floor plan with invalid file
#    [Tags]              development      tcxm_6795
#    #Uploading floor plan with invalid file of type JPEG
#    Log                     Uploading floor plan with invalid file ${FLOOR_PLAN_4_JPEG}
#    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${FLOOR_PLAN_4_JPEG}
#    should contain          ${RESPONSE_STRING}                              ${ERROR_CODE_STR}

#    #Uploading floor plan with invalid file of type GIF
#    Log                     Uploading floor plan with invalid file ${FLOOR_PLAN_5_GIF}
#    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${FLOOR_PLAN_5_GIF}
#    should contain          ${RESPONSE_STRING}                              ${ERROR_CODE_STR}


#TCXM-6796: NEG-Topology-Upload floor plan with file of large size
#    [Documentation]     TCXM-6796: NEG-Topology-Upload floor plan with file of large size
#    [Tags]              development  tcxm_6796
#    Log                     Uploading floor plan with file of large size ${FLOOR_PLAN_3000KB_JPG}
#    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${FLOOR_PLAN_3000KB_JPG}
#    should contain          ${RESPONSE_STRING}                              ${ERROR_CODE_STR}
#    should contain          ${RESPONSE_STRING}                              ${FLOOR_PLAN_MAX_SIZE_ERROR_MSG}
