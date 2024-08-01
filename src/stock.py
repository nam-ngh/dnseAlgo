import pandas as pd
import vnstock as stc

class Stock:
    def __init__(self , symbol: str, type: str='stock'):
        '''
        ARGS:
        - symbol: stock's 3-character symbol OR index name (VNINDEX, ...)
        - type: 'stock' or 'index'
        '''
        self.symbol = symbol
        self.type = type

    def get_history(self, start_date: str, end_date: str, res: str = '1D', source: str='DNSE'):
        '''
        Sets the value of the 'history' attribute: df of historical price data for the symbol 
        obtained using the vnstock.stock_historical_data function
        
        Args:
        - start_date: In 'YYYY-MM-DD' format
        - end_date: In 'YYYY-MM-DD' format
        - res: '1', '3', '5', '15', '30' (minute), '1H', '1D' resolution
        - source: 'DNSE', 'TCBS' -- Default: 'DNSE'
        '''

        self.history = stc.stock_historical_data(
            symbol=self.symbol,
            start_date=start_date, 
            end_date=end_date,
            resolution=res,
            type=self.type,
            beautify=True,
            source=source
        )
    
    def set_sma(self, windows: int|list):
        '''
        Sets the value of the 'sma' attribute: df containing sma columns of the desired window length(s) for the entire history period

        ARGS: 
        - windows: Int or list of Int = window length(s) in days
        '''

        self.sma = pd.DataFrame()
        if isinstance(windows, int):
            windows = [windows,]
        for win in windows:
            col = f'SMA{win}'
            self.sma[col] = self.history['close'].rolling(window=win).mean()

    def set_ema(self, windows: int|list):
        '''
        Sets the value of the 'ema' attribute: df containing ema columns of the desired window length(s) for the entire history period

        ARGS: 
        - windows: Int or list of Int = window length(s) in days
        '''
        self.ema = pd.DataFrame()
        if isinstance(windows, int):
            windows = [windows,]
        for win in windows:
            col = f'EMA{win}'
            self.ema[col] = self.history['close'].ewm(span=win, adjust=False).mean()
    
    def set_macd(self, short: int = 12, long: int = 26, signal: int = 9,):
        # compute long and short emas:
        short = self.history['close'].ewm(span=short, adjust=False).mean()
        long = self.history['close'].ewm(span=long, adjust=False).mean()

        # compute macd:
        self.macd = pd.DataFrame()
        self.macd['MACD'] = short - long
        self.macd['signal'] = self.macd['MACD'].ewm(span=signal, adjust=False).mean()
        self.macd['diff'] = self.macd['MACD'] - self.macd['signal']