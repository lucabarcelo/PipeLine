import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import colorama
from colorama import Fore
import numpy as np
import seaborn as sns
import random

plt.style.use('ggplot')
colorama.init(autoreset=True)

print(Fore.WHITE+ ' -------------- ')

User_Call = input('Please Provide a ticker or list of tickers to begin: (ex: tsla / tsla appl nvda) \n> ')

print(Fore.WHITE +' -------------- ')
print(' Please Select an Option: ')
print(Fore.BLUE+ ' 1. General Info & Moving Averages')
print(Fore.BLUE+ ' 2. Stock Risk & Comparisons')
print(Fore.BLUE+ ' 3. Simulate Portfolio')
print(Fore.WHITE+ ' -------------- ')

Selection = input('> ')

print(Fore.WHITE + ' -------------- ')
user_start = input(Fore.BLUE + 'Please select a starting date \n> ')
user_end = input(Fore.BLUE + 'Please select an ending date \n> ')


def __main__():
	if int(Selection) == 1:
		print(stock_hist(User_Call, user_start, user_end))
		print(Fore.WHITE + ' -------------- ')
		print(Fore.RED + 'Graphs Loading...')
		Rolling()
		print(Fore.RED + 'Graphs Loaded.')

	elif int(Selection) == 2:
		RiskNRelevance()
		print(Fore.WHITE + ' -------------- ')
		Correlations()

	elif int(Selection) == 3:
		print(Fore.WHITE + ' -------------- ')
		Simulation()


cached_data = {}
def stock_hist(symbol, start=None, end=None):
	""" GET SHWIFTY W UR DOWNLOADS """
	# to do:
	if not symbol in cached_data:
		cached_data[symbol] = yf.download(symbol, start=user_start, end=user_end)
		print(Fore.RED + 'Loaded {} num values = {}'.format(symbol, len(cached_data[symbol])))
	return cached_data[symbol] # dataframe


def Rolling():
	""" GIMME SOME BASIC MAs BOI """
	PreRoll = stock_hist(User_Call, user_start, user_end)['Adj Close']
	FiftyRoll = PreRoll.rolling(window=50).mean().iloc[49:]
	TwoRoll = PreRoll.rolling(window=200).mean().iloc[199:]

	Fifty = pd.DataFrame(FiftyRoll)
	TwoHund = pd.DataFrame(TwoRoll)
	# Foosh = TwoHund.query('index < @start_remove or index > @end_remove')
	# Foo = Fifty.query('index < @start_remove or index > @end_remove')

	df = pd.concat([Fifty, TwoHund], axis=1)
	columns = df.columns.values
	columns[0] = 'Fifty-Day'
	columns[1] = 'TwoHundred-Day'
	
	df.plot(title='FIFTY VS. TWOHUNDRED DAY MAs')
	plt.plot(PreRoll)

	plt.show()


def RiskNRelevance():
	""" FOR WHEN USER WANTS PORTFOLIO ANALYSIS """
	ticks = User_Call.split(' ')
	N = len(ticks)
	historical = pd.concat((stock_hist(symbol, user_start, user_end)['Adj Close'] for symbol in ticks), axis=1, keys=ticks)
	returns = (historical/historical.iloc[0]).fillna(method='backfill')
	returns['PORTFOLIO'] = returns.iloc[:,0:N].sum(axis=1) / N

	daily_pct_delta = np.log(returns.pct_change() +1)
	risk = daily_pct_delta.std() * np.sqrt(252)

	print(Fore.WHITE + ' -------------- ')
	print('Relative Volatility Breakdown')
	print(risk)
	returns.plot(title='Comparative Returns', legend=True)
	plt.show()


def Correlations():
	""" FOR WHEN U WANT TO UNDERSTAND RELATIVITY """
	Falloon = User_Call.split(' ')
	stock_prices = pd.concat((stock_hist(symbol)['Adj Close'] for symbol in Falloon), axis=1, keys=Falloon)
	stock_returns = (stock_prices.pct_change() + 1)[1:]
	log_returns = np.log(stock_returns)
	corelate = log_returns.corr()
	sns.heatmap(corelate, annot=True)
	plt.title('Correlations Between Input Stocks')
	plt.show()


def Simulation():
	""" FOR WHEN YOU WANT TO DIVINE THE FUTURE """
	BISH = User_Call.split(' ')
	stock_prices = pd.concat((stock_hist(symbol)['Adj Close'] for symbol in BISH), axis=1, keys=BISH)
	stock_returns = (stock_prices.pct_change() + 1)[1:]
	simulated = pd.DataFrame([((stock_returns.iloc[random.choices(range(len(stock_returns)), k=60)]).mean(axis=1)).cumprod().values for x in range(1000)]).T
	simulated.plot(legend=False, linewidth=1, alpha=0.1, color='blue', title='60,000 Random Simulated Trials for Spread of Likely Returns')
	simulated.quantile([0.05, 0.50, 0.95], axis=1).T.plot(title='Likelihood of Loss/Gain post-60k Trials (Quantiles)')
	plt.show()


__main__()


