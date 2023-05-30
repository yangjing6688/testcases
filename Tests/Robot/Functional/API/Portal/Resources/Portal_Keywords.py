from extauto.common.Utils import Utils
import json

class Portal_Keywords():
    def __init__(self):
        self.utils = Utils()
    def contain_check(self,res,key,except_value,containment=True):
        """
        If there is a value in the list, the details of the column are returned
        :param res: '{"content":[{"operatingSystem":'a'},{"operatingSystem":'b'}'
        :param key: "operatingSystem"
        :param except_value: 'a'
        :return: json
        Example:
        |${jdata}|list_check|'operatingSystem'|'a'|
        ${jdata}={"content":[{"operatingSystem":'a'},{"operatingSystem":'b'}']}
        """
        self.utils.print_info(f'{res}，{key},{except_value}')

        if isinstance(res,bytes):
            res = res.decode('utf-8')
        res_py = json.loads(res)

        if isinstance(res_py,dict):
             res_2 = res_py.get('data')
        elif isinstance(res_py,list):
            res_2 = res_py
        result = list()

        for i in range(len(res_2)):
            try:
                if except_value in res_2[i][key]:
                    result = res_2[i]
            ##except_value type is bool
            except TypeError as e:
                self.utils.print_info(e)
                if except_value == res_2[i][key] :
                    result.append(res_2[i])

        if containment:
            if result:
                self.utils.print_info(f"The checked value exit{result}")
                return json.dumps(result)
            else:
                raise AssertionError('The checked value doesnt exit')
        else:
            if result:
                raise AssertionError('The checked value exit')
            else:
                self.utils.print_info("The checked value doesnt exit")