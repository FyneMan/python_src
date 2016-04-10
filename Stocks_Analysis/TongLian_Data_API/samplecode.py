# -*- coding: utf-8 -*-
from dataapiclient import Client
if __name__ == "__main__":
    try:
        client = Client()
        client.init('6f6843360756e16d8eaeff37dcadace31a698ab30c69030196945f0511b2afeb')
        url1='/api/macro/getChinaDataGDP.csv?field=&indicID=M010000002&indicName=&beginDate=&endDate='
        code, result = client.getData(url1)
        if code==200:
            print result
        else:
            print code
            print result
        url2='/api/subject/getThemesContent.csv?field=&themeID=&themeName=&isMain=1&themeSource='
        code, result = client.getData(url2)
        if(code==200):
            file_object = open('thefile.csv', 'w')
            file_object.write(result)
            file_object.close( )
        else:
            print code
            print result 
    except Exception, e:
        #traceback.print_exc()
        raise e
