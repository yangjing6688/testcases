#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Chuck Bickford - converted to new framework by David Truesdell
# Description   : Test for testing upgrades of server/engines from previous versions of XIQ-SE to latest builds
#                 This is qTest TCXE-958 in the XIQ-SE project.

*** Settings ***
Library         Process
Library         String
Resource        ../../Install_Upgrade/Resources/AllResources.robot

Force Tags      testbed_no_node

Suite Setup     Prepare Test Variables


*** Variables ***
${XIQSE_URL}                        ${xiqse.url}
${XIQSE_USERNAME}                   ${xiqse.user}
${XIQSE_PASSWORD}                   ${xiqse.password}
${XIQSE_IP_ADDRESS}                 ${xiqse.ip}
${XIQSE_SERIAL}                     ${xiqse.serial}
${INSTALL_MODE}                     ${upgrades.install_mode}
${XIQSE_RESTART_SERVER}             systemctl restart nsserver

${NAC_IP}                           ${nac.ip}
${PURVIEW_IP}                       ${purview.ip}
${NEXTGEN_IP}                       ${nextgen.ip}

${XIQ_EMAIL}                        ${xiq.tenant_username}
${XIQ_PASSWORD}                     ${xiq.tenant_password}
${INSTALL_MODE}                     ${upgrades.install_mode}
${PILOT_ENTITLEMENT}                ${xiq.pilot_entitlements}
${NAVIGATOR_ENTITLEMENT}            ${xiq.navigator_entitlements}
${XIQ_BASE_URL}                     "https\://g2.qa.xcloudiq.com"
${XIQ_REDIRECT_URL}                 "https\://g2-hac.qa.xcloudiq.com"
${XIQ_CAPWAP_URL}                   "g2r1-cwpm-01.qa.xcloudiq.com"

${APPLIANCE_USERNAME}               ${appliance.user}
${APPLIANCE_PASSWORD}               ${appliance.password}

${SSH_PORT}                         22
${DOWNLOAD_TIMEOUT_SEC}             600
${INSTALL_DOWNLOAD_TIMEOUT_SEC}     7200
${ESX_VM_CMD_TIMEOUT_SEC}           300

${NBI_FILE}                         nbi.out

@{ALL_APPLIANCES}                   ${XIQSE_IP_ADDRESS}  ${NAC_IP}  ${PURVIEW_IP}  ${NEXTGEN_IP}

&{UPGRADE_TEST_XIQSE}               version=${upgrades.nsrelease_version}  esxIp=${upgrades.esx.esx_ip}
...                                 esxUser=${upgrades.esx.esx_user}  esxPw=${upgrades.esx.esx_password}
...                                 xiqseVmId=${upgrades.xiqse.xiqse_vm_id}   xiqseSnapShotId=${upgrades.xiqse.xiqse_snapshot_id}
...                                 nacVmId=${upgrades.xiqse.nac_vm_id}  nacSnapShotId=${upgrades.xiqse.nac_snapshot_id}
...                                 purviewVmId=${upgrades.xiqse.purview_vm_id}  purviewSnapShotId=${upgrades.xiqse.purview_snapshot_id}
...                                 ngAnalyticsVmId=${upgrades.xiqse.ng_analytics_vm_id}  ngAnalyticsSnapShotId=${upgrades.xiqse.ng_analytics_snapshot_id}
${NSRELEASE_VERSION}                ${upgrades.nsrelease_version}


*** Test Cases ***
Test 1: Cli XIQSE Upgrade From XIQSE
    [Documentation]  Tests XIQ-SE Upgrades from XIQSE as defined in topology file
    [Tags]           tcxe_958    xmc_5685    development    xiqse    acceptance    upgrade_xiqse_from_xiqse    upgrade_from_xiqse    test1

    ${version} =   Get From Dictionary   ${UPGRADE_TEST_XIQSE}    version
    Run Keyword If  'xiqseSnapShotId' in ${UPGRADE_TEST_XIQSE}      Site Engine Upgrade  ${UPGRADE_TEST_XIQSE}
    ...    ELSE  Log   Skipping XIQ-SE Upgrade from XMC ${version}

Test 2: CLI NAC Appliance From XIQSE
    [Documentation]  Tests NAC Upgrades from XIQSE defined in topology file
    [Tags]           tcxe_958    xmc_5685    development    xiqse    acceptance    upgrade_nac_from_xiqse    upgrade_from_xiqse    test2

    ${version} =   Get From Dictionary   ${UPGRADE_TEST_XIQSE}  version
    Run Keyword If  'nacSnapShotId' in ${UPGRADE_TEST_XIQSE}     Nac Engine Upgrade  ${UPGRADE_TEST_XIQSE}
    ...    ELSE  Log   Skipping NAC Upgrade from XMC ${version}

Test 3: CLI Purview Appliance From XIQSE
    [Documentation]  Tests Purview Upgrades from XIQSE as defined in topology file
    [Tags]           tcxe_958    xmc_5685    development    xiqse    acceptance    upgrade_purview_from_xiqse    upgrade_from_xiqse    test3

    ${version} =   Get From Dictionary   ${UPGRADE_TEST_XIQSE}  version
    Run Keyword If   'purviewSnapShotId' in ${UPGRADE_TEST_XIQSE}    Purview Engine Upgrade  ${UPGRADE_TEST_XIQSE}
    ...    ELSE  Log   Skipping Purview Upgrade From XMC ${version}

Test 4: CLI NGAnalytics Appliance From XIQSE
    [Documentation]  Tests NGAnalytics Upgrades from XIQSE as defined in topology file
    [Tags]           tcxe_958    xmc_5685    development    xiqse    acceptance    upgrade_nganalytics_from_xiqse    upgrade_from_xiqse    test4

    ${version} =   Get From Dictionary   ${UPGRADE_TEST_XIQSE}  version
    Run Keyword If    'ngAnalyticsSnapShotId' in ${UPGRADE_TEST_XIQSE}   NGAnalytics Engine Upgrade  ${UPGRADE_TEST_XIQSE}
    ...    ELSE  Log   Skipping NG Analytics Upgrade From XMC ${version}

*** Keywords ***
Prepare Test Variables
    [Documentation]    Sets the version to install and all variables used by keywords

    Log To Console     SETTING TEST UP
    Ubuntu Clear SSH Keys
    ${version}=    UPDATE_SUITE_VERSION_VARIABLES    ${NSRELEASE_VERSION}
    Log To Console    version=${version}
