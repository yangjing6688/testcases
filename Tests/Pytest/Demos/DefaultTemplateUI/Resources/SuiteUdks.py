from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
#----------------------------------------------------------------------------------------------------------
#   Setup/Teardown Keywords
#----------------------------------------------------------------------------------------------------------

class SuiteUdk():
    
    def __init__(self):
        self.defaultLibrary = DefaultLibrary()

    def doExtraStuff(self):
        print("doExtraStuff")
