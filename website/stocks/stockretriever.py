"""A wrapper for the Yahoo! Finance YQL api."""

import sys, httplib, urllib, datetime
from models import Historical,SymbolInfo
try: import simplejson as json
except ImportError: import json


PUBLIC_API_URL = 'http://query.yahooapis.com/v1/public/yql'
DATATABLES_URL = 'store://datatables.org/alltableswithkeys'
HISTORICAL_URL = 'http://ichart.finance.yahoo.com/table.csv?s='
RSS_URL = 'http://finance.yahoo.com/rss/headline?s='
FINANCE_TABLES = {'quotes': 'yahoo.finance.quotes',
                 'options': 'yahoo.finance.options',
                 'quoteslist': 'yahoo.finance.quoteslist',
                 'sectors': 'yahoo.finance.sectors',
                 'industry': 'yahoo.finance.industry'}


def executeYQLQuery(yql):
    conn = httplib.HTTPConnection('query.yahooapis.com')
    queryString = urllib.urlencode({'q': yql, 'format': 'json', 'env': DATATABLES_URL})
    conn.request('GET', PUBLIC_API_URL + '?' + queryString)
    return json.loads(conn.getresponse().read())


class QueryError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def __format_symbol_list(symbolList):
    return ",".join(["\""+stock+"\"" for stock in symbolList])


def __is_valid_response(response, field):
    return 'query' in response and 'results' in response['query'] \
        and field in response['query']['results']


def __validate_response(response, tagToCheck):
    if __is_valid_response(response, tagToCheck):
        quoteInfo = response['query']['results'][tagToCheck]
    else:
        if 'error' in response:
            raise QueryError('YQL query failed with error: "%s".' 
                % response['error']['description'])
        else:
            raise QueryError('YQL response malformed.')
    return quoteInfo


def get_current_info(symbolList, columnsToRetrieve='*'):
    """Retrieves the latest data (15 minute delay) for the 
    provided symbols."""
    columns = ','.join(columnsToRetrieve)
    symbols = __format_symbol_list(symbolList)

    yql = 'select %s from %s where symbol in (%s)' \
          %(columns, FINANCE_TABLES['quotes'], symbols)
    response = executeYQLQuery(yql)
    return __validate_response(response, 'quote')


def get_historical_info(symbol):
    """Retrieves historical stock data for the provided symbol.
    Historical data includes date, open, close, high, low, volume,
    and adjusted close."""
    # yql = 'select * from csv where url=\'%s\'' \
    #       ' and columns=\"Date,Open,High,Low,Close,Volume,AdjClose\"' \
    #        % (HISTORICAL_URL + symbol)
    # results = executeYQLQuery(yql)
    # delete first row which contains column names

    # if results['query']['results'] is None:
    #     # raise QueryError('Symbol %s does not exist in yahoo!finance database.'%symbol)
    #     return None
    # else:
    #     del results['query']['results']['row'][0]
    #     return results['query']['results']['row']

    temp = Historical.objects.filter(Handle = symbol)
    if temp:
        return temp

def get_last_updated(Handle):
    """Return the date when the Handle was last cached locally."""
    in_database = Historical.objects.filter(Handle = Handle).count()
    if in_database:
        temp = Historical.objects.filter(Handle = Handle).latest('Date')
        return temp.Date
    else:
        # if the symbol isn't in the historical table then take the date
        # from the symbolInfo table which has the 1960s date.
        temp = SymbolInfo.objects.filter(Handle=Handle)
        if len(temp):
            return temp[0].DateStamp
        else:
            # raise QueryError("Symbol does not exist.")
            return None

def get_historical_info_dates(symbol,date):
    """Retrieves historical stock data for the provided symbol.
    Historical data includes date, open, close, high, low, volume,
    and adjusted close."""
    current_date = datetime.datetime.now()
    a=str(date.month)
    b=str(date.day)
    c=str(date.year)
    d=str(current_date.month)
    e=str(current_date.day)
    f=str(current_date.year)
    dates = "&a=" + a+"&b="+b + "&c="+c+"&d="+d+"&e="+e+"&f="+f
    # dates="&a=3&b=12&c=1960&d=3&e=12&f=2017"
    yql = 'select * from csv where url=\'%s\'' \
          ' and columns=\"Date,Open,High,Low,Close,Volume,AdjClose\"' \
           % (HISTORICAL_URL + symbol + dates)
    results = executeYQLQuery(yql)
    # delete first row which contains column names
    if results['query']['results']:
        del results['query']['results']['row'][0]
        return results['query']['results']['row']
    else:
        return None

def Update_database(Handle):
    # get_last_updated returns the date of last update if symbol 
    # exists else returns None
    messages=[]

    date = get_last_updated(Handle)
    if date:
        datas = get_historical_info_dates(Handle,date)
        messages.append("Database has been updated for %s : No new updates found."%Handle)
        if datas:
            messages[0] ="Database has been updated for %s : %s Updates found."%(Handle,len(datas))
            for data in datas:
                #prints updates on terminal
                print data
                Date =datetime.datetime.strptime(data['Date'],"%Y-%m-%d")

                #Does not enter update for last_updated_day
                if Date!=date:
                    SymbolInfo_Handle = SymbolInfo.objects.filter(Handle=Handle)[0]
                    Historical(Handle=SymbolInfo_Handle,Date=Date,Open=float(data['Open']),High=float(data['High']),Low=float(data['Low']),Close=float(data['Close']),Volume=float(data['Volume']),Adj_Close=float(data['AdjClose'])).save()
    else:
        messages.append("Symbol %s does not exist. Please enter another."%Handle)
    return messages

def get_month_info(symbol):
    """Retrieves historical stock data for last month for the provided symbol.
    Historical data includes date, open, close, high, low, volume,
    and adjusted close."""
    delta = datetime.timedelta(days=-33)
    today = datetime.date.today()
    month_ago = today + delta
    yql = 'select * from csv where url=\'%s\'' \
          ' and columns=\"Date,Open,High,Low,Close,Volume,AdjClose\"' \
          ' and Date >= \'%s-%s-%s\'' \
           % (HISTORICAL_URL + symbol,
              month_ago.year,
              str(month_ago.month).zfill(2),
              str(month_ago.day).zfill(2),)
    results = executeYQLQuery(yql)
    # delete first row which contains column names
    del results['query']['results']['row'][0]
    return results['query']['results']['row']

def get_news_feed(symbol):
    """Retrieves the rss feed for the provided symbol."""
    feedUrl = RSS_URL + symbol
    yql = 'select title, link, description, pubDate from rss where url=\'%s\'' % feedUrl
    print"query is: " + yql
    response = executeYQLQuery(yql)
    if response['query']['results'] is None:
        raise QueryError('Symbol %s does not exist in yahoo!finance database.'%symbol)
    if response['query']['results']['item'][0]['title'].find('not found') > 0:
        raise QueryError('Feed for %s does not exist.' % symbol)
    else:
        return response['query']['results']['item']


def get_options_info(symbol, expiration='', columnsToRetrieve ='*'):
    """Retrieves options data for the provided symbol."""
    columns = ','.join(columnsToRetrieve)
    yql = 'select %s from %s where symbol = \'%s\'' \
          % (columns, FINANCE_TABLES['options'], symbol)
    if expiration != '':
        yql += " and expiration='%s'" %(expiration)
    response = executeYQLQuery(yql)
    return __validate_response(response, 'optionsChain')


def get_index_summary(index, columnsToRetrieve='*'):
    columns = ','.join(columnsToRetrieve)
    yql = 'select %s from %s where symbol = \'@%s\'' \
          % (columns, FINANCE_TABLES['quoteslist'], index)
    response = executeYQLQuery(yql)
    return __validate_response(response, 'quote')


def get_industry_ids():
    """retrieves all industry names and ids."""
    yql = 'select * from %s' % FINANCE_TABLES['sectors']
    response = executeYQLQuery(yql)
    return __validate_response(response, 'sector')


def get_industry_index(id):
    """retrieves all symbols that belong to an industry."""
    yql = 'select * from %s where id =\'%s\'' \
          % (FINANCE_TABLES['industry'], id)
    response = executeYQLQuery(yql)
    return __validate_response(response, 'industry')


if __name__ == "__main__":
    try:
        print get_current_info(sys.argv[1:])
        #print get_industry_ids()
        #get_news_feed('yhoo')
    except QueryError, e:
        print e
        sys.exit(2)
