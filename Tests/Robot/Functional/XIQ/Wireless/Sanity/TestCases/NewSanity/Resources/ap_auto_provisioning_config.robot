*** Variables ***
&{APP_AP_01}        device_function=AP      device_model=${ap1.model}     service_tags=Disable     ip_subnetworks=Disable      network_policy=${POLICY_NAME_01}
&{APP_AP_02}        device_function=AP      device_model=${ap1.model}     service_tags=Disable     ip_subnetworks=Disable      network_policy=${POLICY_NAME_01}

&{AP_ADVANCED_SETTINGS_01}          upload_firmware=Disable       upload_configuration=Disable      reboot=Disable      Firmware_version=default
&{AP_ADVANCED_SETTINGS_02}          upload_firmware=Disable       upload_configuration=Disable      reboot=Enable       Firmware_version=default
&{AP_ADVANCED_SETTINGS_03}          upload_firmware=Disable       upload_configuration=Enable      reboot=Disable       Firmware_version=default
&{AP_ADVANCED_SETTINGS_04}          upload_firmware=Disable       upload_configuration=Enable      reboot=Enable        Firmware_version=default
&{AP_ADVANCED_SETTINGS_05}          upload_firmware=Enable       upload_configuration=Enable      reboot=Enable         Firmware_version=golden_version
&{AP_ADVANCED_SETTINGS_06}          upload_firmware=Enable       upload_configuration=Enable      reboot=Enable         Firmware_version=latest_version

&{CAPWAP_CONFIGURATION_01}          CAPWAP_credential=disable       primary_CAPWAP=default      backup_CAPWAP=default       primary_name=default        primary_IP_addr=default     primary_hostname=default       backup_name=default      backup_IP_addr=default      backup_hostname=default     passphrase=default
&{DEVICE_CREDENTIAL_01}             device_credential=disable		root_admin_name=default		root_admin_password=default		read_only_admin_name=default		read_only_admin_password=default