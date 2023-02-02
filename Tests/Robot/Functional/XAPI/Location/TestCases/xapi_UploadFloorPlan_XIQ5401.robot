# Author        : Kun Li
# Date          : 10 Jan 2023
# Description   : XIQ-5401 XAPI Upload FloorPlan 

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
# robot -v TOPO:g2r1-xapi-1 xapi_UploadFloorPlan_XIQ5401.robot
#
# Please make sure your setup robot file contains blow variables to run this test suite
#   ${XAPI_BASE_URL}                    https://g2-api.qa.xcloudiq.com
#   ${TENANT_USERNAME}                  kuli@extremenetworks.com
#   ${TENANT_PASSWORD}                  Aerohive123
#


*** Variables ***
${LOCATION_1}                         XAPI-Auto-Topology-Location-1
${LOCATION_2}                         XAPI-Auto-Topology-Location-2

${BUILDING_1}                         XAPI-Auto-Topology-Building-1
${BUILDING_2}                         XAPI-Auto-Topology-Building-2
${BUILDING_1_ADDR}                    XAPI-Auto-Building-Address-01
${BUILDING_2_ADDR}                    XAPI-Auto-Building-Address-02

${FLOOR_1}                            XAPI-Auto-Topology-Floor-1
${FLOOR_2}                            XAPI-Auto-Topology-Floor-2

${WRONG_ID}                           999999999
${ERROR_CODE_STR}                     error_code

${FLOOR_PLAN_1_PNG}                   Resources/floorplan-1.png
${FLOOR_PLAN_2_PNG}                   Resources/floorplan-2.png
${FLOOR_PLAN_3_JPG}                   Resources/floorplan-3.jpg
${FLOOR_PLAN_4_JPEG}                  Resources/floorplan-4.jpeg
${FLOOR_PLAN_5_GIF}                   Resources/floorplan-5.gif
${FLOOR_PLAN_3000KB_JPG}              Resources/floorplan-3000KB.jpg
${FLOOR_PLAN_2M_PNG}                  Resources/floorplan_xapi_xiq5401_2M.png
${FLOOR_PLAN_2M_JPG}                  Resources/floorplan_xapi_xiq5401_2M.jpg
${FLOOR_PLAN_10M_PNG}                 Resources/floorplan_xapi_xiq5401_10M.png
${FLOOR_PLAN_10M_JPG}                 Resources/floorplan_xapi_xiq5401_10M.jpg
${FLOOR_PLAN_11M_PNG}                 Resources/floorplan_xapi_xiq5401_11M.png
${FLOOR_PLAN_11M_JPG}                 Resources/floorplan_xapi_xiq5401_11M.jpg

${ERROR_MSG_INVALID_IMG_FORMAT}       image.format.not.valid
${FLOOR_PLAN_MAX_SIZE_ERROR_MSG}      Maximum upload size exceeded


*** Settings ***

Library     common/Cli.py
Library     common/Utils.py

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

    ${CUR_FEATURE_PATH}=         Get Feature Path           ${SUITE SOURCE}
    set suite variable     ${CUR_FEATURE_PATH}
    Log                     Current feature full path is: ${CUR_FEATURE_PATH}

    
*** Test Cases ***
TCXM-24681: Topology - Upload floor plan with various file types: JPG, PNG, JPEG, GIF
    [Documentation]     TCXM-24681: Topology - Upload floor plan with different file type. JPG and PNG were supported; JPEG or GIF was unsupported.
    [Tags]              development  tcxm_24681

    #Verify upload pass when uploading a supported image file (JPG is supported)
    Log                     Uploading ${CUR_FEATURE_PATH}/${FLOOR_PLAN_3_JPG} image
    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${CUR_FEATURE_PATH}/${FLOOR_PLAN_3_JPG}
    should not contain      ${RESPONSE_STRING}                              ${ERROR_CODE_STR}

    #Verify upload pass when uploading a supported image file (PNG is supported)
    Log                     Uploading ${CUR_FEATURE_PATH}/${FLOOR_PLAN_1_PNG} image
    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${CUR_FEATURE_PATH}/${FLOOR_PLAN_1_PNG}
    should not contain      ${RESPONSE_STRING}                              ${ERROR_CODE_STR}

    #Verify upload fails when uploading an unsupported image file (JPEG is unsupported)
    Log                     Uploading ${CUR_FEATURE_PATH}/${FLOOR_PLAN_4_JPEG} image
    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${CUR_FEATURE_PATH}/${FLOOR_PLAN_4_JPEG}
    should contain      ${RESPONSE_STRING}                              ${ERROR_CODE_STR}
    should contain      ${RESPONSE_STRING}                              ${ERROR_MSG_INVALID_IMG_FORMAT}
    
    #Verify upload fails when uploading an unsupported image file (GIF is unsupported)
    Log                     Uploading ${CUR_FEATURE_PATH}/${FLOOR_PLAN_5_GIF} image
    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${CUR_FEATURE_PATH}/${FLOOR_PLAN_5_GIF}
    should contain      ${RESPONSE_STRING}                              ${ERROR_CODE_STR}
    should contain      ${RESPONSE_STRING}                              ${ERROR_MSG_INVALID_IMG_FORMAT}    

TCXM-24682: Topology - Upload floor plan with file size less than 2M
    [Documentation]     TCXM-24682: Topology - Upload floor plan with file size less than 2M which will not be compressed
    [Tags]              development  tcxm_24682

    #Uploading floor plan image of type JPG and file size less than 2M
    Log                     Uploading ${CUR_FEATURE_PATH}/${FLOOR_PLAN_2M_JPG} image
    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${CUR_FEATURE_PATH}/${FLOOR_PLAN_2M_JPG}
    should not contain      ${RESPONSE_STRING}                              ${ERROR_CODE_STR}

    #Uploading floor plan image of type PNG and file size less than 2M
    Log                     Uploading ${CUR_FEATURE_PATH}/${FLOOR_PLAN_2M_PNG} image
    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${CUR_FEATURE_PATH}/${FLOOR_PLAN_2M_PNG}
    should not contain      ${RESPONSE_STRING}                              ${ERROR_CODE_STR}

    #TBD: download the image and check the file was not compressed

TCXM-24683: Topology - Upload floor plan with file size between 2M and 10M
    [Documentation]     TCXM-24683: Topology - Upload floor plan with file size between 2M  and 10M which will be compressed
    [Tags]              development  tcxm_24683

    #Uploading floor plan image of type JPG and file size between 2M and 10M
    Log                     Uploading ${CUR_FEATURE_PATH}/${FLOOR_PLAN_10M_JPG} image
    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${CUR_FEATURE_PATH}/${FLOOR_PLAN_10M_JPG}
    should not contain      ${RESPONSE_STRING}                              ${ERROR_CODE_STR}

    #Uploading floor plan image of type PNG and file size between 2M and 10M
    Log                     Uploading ${CUR_FEATURE_PATH}/${FLOOR_PLAN_10M_PNG} image
    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${CUR_FEATURE_PATH}/${FLOOR_PLAN_10M_PNG}
    should not contain      ${RESPONSE_STRING}                              ${ERROR_CODE_STR}

    #TBD: download the image and check the file was compressed

TCXM-24684: Topology - Upload floor plan with file size more than 10M
    [Documentation]     TCXM-24684: Topology - Upload floor plan with file size more than 10M which will be fail
    [Tags]              development  tcxm_24684

    #Verify Upload fail when uploading the jpg image file size more than 10M
    Log                     Uploading ${CUR_FEATURE_PATH}/${FLOOR_PLAN_11M_JPG} image
    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${CUR_FEATURE_PATH}/${FLOOR_PLAN_11M_JPG}
    should contain      ${RESPONSE_STRING}                              ${ERROR_CODE_STR}
    should contain      ${RESPONSE_STRING}                              ${FLOOR_PLAN_MAX_SIZE_ERROR_MSG}

    #Verify Upload fail when uploading the png image file size more than 10M
    Log                     Uploading ${CUR_FEATURE_PATH}/${FLOOR_PLAN_11M_PNG} image
    ${RESPONSE_STRING}=     xapi upload floor plan get response string           ${CUR_FEATURE_PATH}/${FLOOR_PLAN_11M_PNG}
    should contain      ${RESPONSE_STRING}                              ${ERROR_CODE_STR}
    should contain      ${RESPONSE_STRING}                              ${FLOOR_PLAN_MAX_SIZE_ERROR_MSG}