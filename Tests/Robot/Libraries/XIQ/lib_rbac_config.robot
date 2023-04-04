#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# This file contains variables related to role based account access
#

*** Variables ***

### Helpdesk account
${XIQ_HD_USER}                    cloudhelpdeskautomationuser@gmail.com
${XIQ_HD_PASSWORD}                Aerohive123

${HELPDESK_EMAIL}                 cloudhelpdeskautomationuser@gmail.com
${HELPDESK_APP_PASSWORD}          urfurxuppbxvdxpo
${HELPDESK_NAME}                  xiqextreme helpdesk
${help_username}                  cloudhelpdeskautomationuser@gmail.com
${help_password}                  Aerohive123
${TIMEOUT}                        120
&{HELPDESK_ROLE}                  email=${HELPDESK_EMAIL}     name=${HELPDESK_NAME}     timeout=${TIMEOUT}     role=Helpdesk