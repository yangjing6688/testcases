# This file contains keywords specific to Product URL.

*** Variables ***
${XIQ_Instance}     Unknown
${ENV_TYPE}         Unknown

*** Settings ***
Library          String
Library         Collections

*** Keywords ***
Get XIQ Instance from URL
    [Documentation]     Extracts XIQ environment from GDC URL
    [Arguments]         ${url}

    ${contains}=    get regexp matches  ${url}    https://(.*).qa.xcloudiq.com    1

    ${length}=  Get Length  ${contains}

    IF  ${length} > 0
        ${XIQ_Instance}=    Get from list  ${contains}     0
    ELSE
        ${contains}=    get regexp matches  ${url}    https://(.*).extremecloudiq.com    1

        ${length}=  Get Length  ${contains}

        IF  ${length} > 0
            ${XIQ_Instance}=    Get from list  ${contains}     0
        ELSE
            ${XIQ_Instance}=    Set variable    Production
        END
    END

    [return]    ${XIQ_Instance}     ${length}

Generate Product URL
    [Documentation]     Generate Product Url
    [Arguments]         ${result}   ${length}

    IF  ${length} == 0
        ${product_url}      Set Variable    https://productinfo.extremecloudiq.com/productinfo
        ${ENV_TYPE}=        Set Variable    Production
    ELSE IF  "${length}" > "0" and "${result}" == "a-cloud"
        ${product_url}      Set Variable    https://${result}-productinfo.extremecloudiq.com/productinfo
        ${ENV_TYPE}=        Set Variable    Staging
    ELSE
        ${product_url}      Set Variable    https://${result}-productinfo.qa.xcloudiq.com/productinfo
        ${ENV_TYPE}=        Set Variable    Test
    END

    [return]    ${product_url}      ${ENV_TYPE}

Generate Developer Portal URL
    [Documentation]     Generate Developer Portal URL
    [Arguments]         ${XIQ_Instance}   ${length}

    IF  ${length} == 0
        ${ENV_TYPE}=        Set Variable    Production

        ${developer_portal}                 Set Variable    https://developer.extremecloudiq.com/
        ${developer_portal_documentation}   Set Variable    https://developer.extremecloudiq.com/documentation/
        ${developer_portal_api_docs}        Set Variable    https://extremecloudiq.com/api-docs/api-docs.html
        ${developer_portal_swagger_ui}      Set Variable    https://api.extremecloudiq.com/swagger-ui/index.html

    ELSE IF  "${length}" > "0" and "${XIQ_Instance}" == "a-cloud"
        ${ENV_TYPE}=        Set Variable    Staging

        ${developer_portal}                 Set Variable    https://${XIQ_Instance}-developer.extremecloudiq.com/
        ${developer_portal_documentation}   Set Variable    https://${XIQ_Instance}-developer.extremecloudiq.com/documentation/
        ${developer_portal_api_docs}        Set Variable    https://${XIQ_Instance}.extremecloudiq.com/api-docs/api-docs.html
        ${developer_portal_swagger_ui}      Set Variable    https://${XIQ_Instance}-api.extremecloudiq.com/swagger-ui/index.html
    ELSE
        ${ENV_TYPE}=        Set Variable    Test

        ${developer_portal}                 Set Variable    https://${XIQ_Instance}-developer.qa.xcloudiq.com/
        ${developer_portal_documentation}   Set Variable    https://${XIQ_Instance}-developer.qa.xcloudiq.com/documentation/
        ${developer_portal_api_docs}        Set Variable    https://${XIQ_Instance}.qa.xcloudiq.com/api-docs/api-reference.html
        ${developer_portal_swagger_ui}      Set Variable    https://${XIQ_Instance}-api.qa.xcloudiq.com/swagger-ui/index.html
    END

    [return]    ${developer_portal}     ${developer_portal_documentation}   ${developer_portal_api_docs}     ${developer_portal_swagger_ui}     ${ENV_TYPE}