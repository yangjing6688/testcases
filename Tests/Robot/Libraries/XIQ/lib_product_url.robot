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
    END

    IF  ${length} == 0
        ${contains}=    get regexp matches  ${url}    https://(.*).extremecloudiq.com    1

        ${length}=  Get Length  ${contains}

        IF  ${length} > 0
        ${XIQ_Instance}=    Get from list  ${contains}     0
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
