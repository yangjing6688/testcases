*** Variables ***
&{SW_SR20_SR21_01}      device_function=Extreme Networks SR20xx / SR21xx Switches       device_model=SR2024P     service_tags=Disable   ip_subnetworks=Disable      network_policy=${POLICY_NAME_02}
&{SW_SR20_SR21_01}      device_function=Extreme Networks SR20xx / SR21xx Switches       device_model=SR2024P     service_tags=Disable   ip_subnetworks=Disable      network_policy=${POLICY_NAME_02}

&{SW_SR22_SR23_01}      device_function=Extreme Networks SR22xx / SR23xx Switches       device_model=SR2348P     service_tags=Disable   ip_subnetworks=Disable      network_policy=${POLICY_NAME_02}
&{SW_SR22_SR23_02}      device_function=Extreme Networks SR22xx / SR23xx Switches       device_model=SR2348P     service_tags=Disable   ip_subnetworks=Disable      network_policy=${POLICY_NAME_02}

&{SW_ADVANCED_SETTINGS_01}          upload_firmware=Disable       upload_configuration=Disable      reboot=Disable
&{SW_ADVANCED_SETTINGS_02}          upload_firmware=Disable       upload_configuration=Disable      reboot=Enable
&{SW_ADVANCED_SETTINGS_03}          upload_firmware=Disable       upload_configuration=Enable       reboot=Disable
&{SW_ADVANCED_SETTINGS_04}          upload_firmware=Disable       upload_configuration=Enable        reboot=Enable

&{CAPWAP_CONFIGURATION_01}          CAPWAP_credential=disable       primary_CAPWAP=default      backup_CAPWAP=default       primary_name=default        primary_IP_addr=default     primary_hostname=default       backup_name=default      backup_IP_addr=default      backup_hostname=default     passphrase=default
&{DEVICE_CREDENTIAL_01}             device_credential=disable		root_admin_name=default		root_admin_password=default		read_only_admin_name=default		read_only_admin_password=default