from robot.libraries.BuiltIn import BuiltIn

MAIL_ID1 = BuiltIn().get_variable_value("${PPSK_MAIL_ID}")
MAIL_ID1_PASS = BuiltIn().get_variable_value("${PPSK_MAIL_PASSWORD}")

if MAIL_ID1 is None:
    PPSK_MAIL_ID = 'blrtb2tenant1@gmail.com'
    PPSK_MAIL_PASSWORD = 'ozrnzboilbidupin'
else:
    PPSK_MAIL_ID = MAIL_ID1
    PPSK_MAIL_PASSWORD = MAIL_ID1_PASS

MAIL_ID2 = 'blrtb2tenant2@gmail.com'
MAIL_ID2_PASS = 'Extreme@123'
