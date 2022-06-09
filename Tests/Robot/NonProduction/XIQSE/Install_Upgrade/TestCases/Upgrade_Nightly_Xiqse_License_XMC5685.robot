#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : David Truesdell
# Description   : Test for testing upgrades of XIQSE from previous versions of XIQ-SE to latest builds
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
${XIQSE_FILE_PREFIX}                ExtremeCloudIQSiteEngine_
${LOG_DIRECTORY}                    /var/log/
${NSRELEASE_XIQSE_FILE}             ${XIQSE_FILE_PREFIX}${NSRELEASE_VERSION}_64bit_install.bin
${NSRELEASE_XIQSE_LOG_FILE}         ${XIQSE_FILE_PREFIX}${NSRELEASE_VERSION}_64bit_install.log
${NSRELEASE_VERSION_BASE}           ${NSRELEASE_BASE}${NSRELEASE_VERSION}
${SSH_PORT}                         22
${DOWNLOAD_TIMEOUT_SEC}             300
${INSTALL_DOWNLOAD_TIMEOUT_SEC}     7200
${ESX_VM_CMD_TIMEOUT_SEC}           300

${NBI_FILE}                         nbi.out

@{ALL_APPLIANCES}                   ${XIQSE_IP_ADDRESS}

&{UPGRADE_TEST_XIQSE}               version=${upgrades.nsrelease_version}  esxIp=${upgrades.esx.esx_ip}
...                                 esxUser=${upgrades.esx.esx_user}  esxPw=${upgrades.esx.esx_password}
...                                 xiqseVmId=${upgrades.xiqse.xiqse_vm_id}   xiqseSnapShotId=${upgrades.xiqse.xiqse_snapshot_id}
${NSRELEASE_VERSION}                ${upgrades.nsrelease_version}


*** Test Cases ***
Test 1: Cli XIQSE Upgrade From XIQSE
    [Documentation]  Tests XIQ-SE Upgrades from XIQSE as defined in topology file
    [Tags]           xiqse_tcxe_958    xmc_5685    development    xiqse    acceptance    upgrade_xiqse_from_xiqse    upgrade_from_xiqse    test1

    ${version} =   Get From Dictionary   ${UPGRADE_TEST_XIQSE}    version
    Run Keyword If  'xiqseSnapShotId' in ${UPGRADE_TEST_XIQSE}      Site Engine Upgrade  ${UPGRADE_TEST_XIQSE}
    ...    ELSE  Log   Skipping XIQ-SE Upgrade from XMC ${version}

Test 2: Check Server Log
    [Documentation]   Check server.log for exceptions.
    [Tags]            known_issue    xiqse_tcxe_958    xmc_5685    development    xiqse    acceptance    exception_check    test5
    Check Server Log For Exceptions  ${XIQSE_IP_ADDRESS}  ${XIQSE_USERNAME}  ${XIQSE_PASSWORD}
