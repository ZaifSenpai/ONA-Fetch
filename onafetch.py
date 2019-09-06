import json
import requests
import pandas as pd

AUTH_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

def onafetch(form_id, state, outFile = ''):
    """
    Sends GET request to ONA Data API and returns Panda Dataframe of the data.

    :param form_id: str value showing the form id of data to be retrieved.
    :param state:   str value to filter data by given state value.
    :param outFile: str value of file where Dataframe data is to be saved. Data can be
                    read from file using pd.read_pickle(file_name) function.
    :returns:       Pandas.Dataframe of retrieved data from ONA Data Server.
    """
    session = requests.Session()

    # url as shown in docs: https://api.ona.io/static/docs/data.html#example-iv
    url = 'https://api.ona.io/api/v1/data/' + form_id + '?query={"state":{"$i":"' + state + '"}}'
    session.headers = { 'Authorization': 'Token ' + AUTH_TOKEN }

    print('Sending request...')
    response = session.request('GET', url)

    if response.status_code == 200:
        print('Data successfully retrieved')
        df = pd.DataFrame.from_dict(response.json(), orient = 'columns')
    else:
        print('Error! Response code is', response.status_code)
        df = pd.DataFrame() # To Save and Return empty dataframe

    if outFile:
        """
        Save Dataframe to a file for future use.

        To read the saved data to Pandas.Dataframe, use:
        df = pd.read_pickle(file_name)
        """
        df.to_pickle(outFile)

    return df

if __name__ == "__main__":
    # Sample use:
    onafetch(input('Enter form id: '), input('Enter state: '), "_temp.dat") # Look for 'state' in given id and save to _temp.dat
    df = pd.read_pickle("_temp.dat") # read dataframe from _temp.dat
    print(df) # print dataframe
