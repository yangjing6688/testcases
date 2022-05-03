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
Resource        ../../Install_Upgrade/Resources/AllResources.robot

Force Tags      testbed_no_node

Suite Setup     Ubuntu Clear SSH Keys


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
${XIQ_CAPWAP_URL}                   g2r1-cwpm-01.qa.xcloudiq.com

${APPLIANCE_USERNAME}               ${appliance.user}
${APPLIANCE_PASSWORD}               ${appliance.password}

${NSRELEASE_BASE}                   http://nsrelease.extremenetworks.com/release/netsightweb/ns_console/Console/NETSIGHT_Suite_
${XIQSE_FOLDER}                     NetSight
${NAC_FOLDER}                       NAC
${NGANALYTICS_FOLDER}               Analytics
${PURVIEW_FOLDER}                   Purview
${XIQSE_FILE_PREFIX}                ExtremeCloudIQSiteEngine_
${NAC_BINARY_PREFIX}                nac_appliance_64bit_sw_upgrade_to_
${NAC_LOG_PREFIX}                   nacSoftwareUpgradeTo
${PURVIEW_BINARY_PREFIX}            purview_appliance_upgrade_to_
${PURVIEW_LOG_PREFIX}               purviewSoftwareUpgradeTo
${NGANALYTICS_BINARY_PREFIX}        analytics_appliance_upgrade_to_
${NGANALYTICS_LOG_PREFIX}           analyticsSoftwareUpgradeTo
${LOG_DIRECTORY}                    /var/log/
${NSRELEASE_XIQSE_FILE}             ${XIQSE_FILE_PREFIX}${NSRELEASE_VERSION}_64bit_install.bin
${NSRELEASE_XIQSE_LOG_FILE}         ${XIQSE_FILE_PREFIX}${NSRELEASE_VERSION}_64bit_install.log
${NSRELEASE_NAC_FILE}               ${NAC_BINARY_PREFIX}${NSRELEASE_VERSION}.bin
${NSRELEASE_NAC_LOG_FILE}           ${LOG_DIRECTORY}${NAC_LOG_PREFIX}${NSRELEASE_VERSION}.log
${NSRELEASE_PURVIEW_FILE}           ${PURVIEW_BINARY_PREFIX}${NSRELEASE_VERSION}.bin
${NSRELEASE_PURVIEW_LOG_FILE}       ${LOG_DIRECTORY}${PURVIEW_LOG_PREFIX}${NSRELEASE_VERSION}.log
${NSRELEASE_NGANALYTICS_FILE}       ${NGANALYTICS_BINARY_PREFIX}${NSRELEASE_VERSION}.bin
${NSRELEASE_NGANALYTICS_LOG_FILE}   ${LOG_DIRECTORY}${NGANALYTICS_LOG_PREFIX}${NSRELEASE_VERSION}.log
${NSRELEASE_VERSION_BASE}           ${NSRELEASE_BASE}${NSRELEASE_VERSION}
${SSH_PORT}                         22
${DOWNLOAD_TIMEOUT_SEC}             300
${INSTALL_DOWNLOAD_TIMEOUT_SEC}     7200
${ESX_VM_CMD_TIMEOUT_SEC}           300

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
    [Tags]           xiqse_tcxe_958    xmc_5685    development    xiqse    acceptance    upgrade_xiqse_from_xiqse    upgrade_from_xiqse    test1

    ${version} =   Get From Dictionary   ${UPGRADE_TEST_XIQSE}    version
    Run Keyword If  'xiqseSnapShotId' in ${UPGRADE_TEST_XIQSE}      Site Engine Upgrade  ${UPGRADE_TEST_XIQSE}
    ...    ELSE  Log   Skipping XIQ-SE Upgrade from XMC ${version}

Test 2: CLI NAC Appliance From XIQSE
    [Documentation]  Tests NAC Upgrades from XIQSE defined in topology file
    [Tags]           xiqse_tcxe_958    xmc_5685    development    xiqse    acceptance    upgrade_nac_from_xiqse    upgrade_from_xiqse    test2

    ${version} =   Get From Dictionary   ${UPGRADE_TEST_XIQSE}  version
    Run Keyword If  'nacSnapShotId' in ${UPGRADE_TEST_XIQSE}     Nac Engine Upgrade  ${UPGRADE_TEST_XIQSE}
    ...    ELSE  Log   Skipping NAC Upgrade from XMC ${version}

Test 3: CLI Purview Appliance From XIQSE
    [Documentation]  Tests Purview Upgrades from XIQSE as defined in topology file
    [Tags]           xiqse_tcxe_958    xmc_5685    development    xiqse    acceptance    upgrade_purview_from_xiqse    upgrade_from_xiqse    test3

    ${version} =   Get From Dictionary   ${UPGRADE_TEST_XIQSE}  version
    Run Keyword If   'purviewSnapShotId' in ${UPGRADE_TEST_XIQSE}    Purview Engine Upgrade  ${UPGRADE_TEST_XIQSE}
    ...    ELSE  Log   Skipping Purview Upgrade From XMC ${version}

Test 4: CLI NGAnalytics Appliance From XIQSE
    [Documentation]  Tests NGAnalytics Upgrades from XIQSE as defined in topology file
    [Tags]           xiqse_tcxe_958    xmc_5685    development    xiqse    acceptance    upgrade_nganalytics_from_xiqse    upgrade_from_xiqse    test4

    ${version} =   Get From Dictionary   ${UPGRADE_TEST_XIQSE}  version
    Run Keyword If    'ngAnalyticsSnapShotId' in ${UPGRADE_TEST_XIQSE}   NGAnalytics Engine Upgrade  ${UPGRADE_TEST_XIQSE}
    ...    ELSE  Log   Skipping NG Analytics Upgrade From XMC ${version}

Test 5: Check Server Log
    [Documentation]   Check server.log for exceptions.
    [Tags]            known_issue    xiqse_tcxe_958    xmc_5685    development    xiqse    acceptance    exception_check    test5
    Check Server Log For Exceptions  ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}
