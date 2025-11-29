import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pypfopt import EfficientFrontier, risk_models
from pypfopt.expected_returns import mean_historical_return

tickers = ['VTI', 'SHY', 'BLV', 'GLD', 'DBC', 'IYR']
df = yf.download(tickers, start = '1980-1-1')['Close']
df = df.dropna()
df[tickers]

ret = df.pct_change()
corr = ret.corr()
sns.heatmap(corr, annot = True, cmap = 'RdYlGn', linewidths = 0.01)

df_plot = df/df.iloc[0]
label = df.columns
plt.figure(figsize = (20,10))
plt.plot(df_plot, label = label)
plt.legend()
plt.grid(True, linestyle = '--', alpha = 0.6)
plt.tight_layout()
plt.show()

mu = mean_historical_return(df)
s = risk_models.sample_cov(df)
ef = EfficientFrontier(mu, s)
weights = ef.efficient_return(target_return = 0.07)
ef.portfolio_performance(verbose = True)

for ticker, w in weights.items():
    print(f'{ticker}: {w: .2%}')

ret1 = df.pct_change().dropna()
w1 = np.array(list(weights.values()))
port_ret1 = ret.dot(w1).dropna()

level = 0.05
q = np.quantile(port_ret1, level)
port_v = 10000
VaR1 = -q * port_v
fract1 = VaR1/port_v

print(f'Il Value At Risk del portafoglio è {VaR1: 0.2f}€')
print(f'La perdita potenziale è il {fract1: 0.2%}')

ann_ret1 = port_ret1.mean()*252
ann_vol1 = port_ret1.std()*np.sqrt(252)
sharpe1 = ann_ret1/ann_vol1

print(f'Il rendimento annuo è: {ann_ret1: 0.2%}')
print(f'La volatilità annua è: {ann_vol1: 0.2%}')
print(f'Sharpe ratio è: {sharpe1: 0.2f}')

mu = mean_historical_return(df)
s = risk_models.sample_cov(df)
ef2 = EfficientFrontier(mu, s)
weights2 = ef2.efficient_return(target_return = 0.10)
ef2.portfolio_performance(verbose = True)

for ticker, w in weights2.items():
    print(f'{ticker}: {w: .2%}')

ret2 = df.pct_change().dropna()
w2 = np.array(list(weights2.values()))
port_ret2 = ret.dot(w2).dropna()

level = 0.05
q = np.quantile(port_ret2, level)
port_v = 10000
VaR2 = -q * port_v
fract2 = VaR2/port_v

print(f'Il Value At Risk del portafoglio è {VaR2: 0.2f}€')
print(f'La perdita potenziale è il {fract2: 0.2%}')

ann_ret2 = port_ret2.mean()*252
ann_vol2 = port_ret2.std()*np.sqrt(252)
sharpe2 = ann_ret2/ann_vol2

print(f'Il rendimento annuo è: {ann_ret2: 0.2%}')
print(f'La volatilità annua è: {ann_vol2: 0.2%}')
print(f'Sharpe ratio è: {sharpe2: 0.2f}')

mu = mean_historical_return(df)
s = risk_models.sample_cov(df)
ef3 = EfficientFrontier(mu, s)
weights3 = ef3.efficient_risk(target_volatility = 0.05)
ef3.portfolio_performance(verbose = True)

for ticker, w in weights3.items():
    print(f'{ticker}: {w: .2%}')

ret3 = df.pct_change().dropna()
w3 = np.array(list(weights3.values()))
port_ret3 = ret.dot(w3).dropna()

level = 0.05
q = np.quantile(port_ret3, level)
port_v = 10000
VaR3 = -q * port_v
fract3 = VaR3/port_v

print(f'Il Value At Risk del portafoglio è {VaR3: 0.2f}€')
print(f'La perdita potenziale è il {fract3: 0.2%}')

ann_ret3 = port_ret3.mean()*252
ann_vol3 = port_ret3.std()*np.sqrt(252)
sharpe3 = ann_ret3/ann_vol3

print(f'Il rendimento annuo è: {ann_ret3: 0.2%}')
print(f'La volatilità annua è: {ann_vol3: 0.2%}')
print(f'Sharpe ratio è: {sharpe3: 0.2f}')

tab = pd.DataFrame({
    'Rendimento Annuo': [ann_ret1, ann_ret2, ann_ret3],
    'Volatilità Annua': [ann_vol1, ann_vol2, ann_vol3],
    'Sharpe Ratio (versione sempl. senza rf)': [sharpe1, sharpe2, sharpe3],
    'VaR (€)': [VaR1, VaR2, VaR3]
}, index = ['Portafoglio 1', 'Portafoglio 2', 'Portafoglio 3'])

tab.style.format({
    'Rendimento Annuo': '{:.2f}%',
    'Volatilità Annua': '{:.2f}%',
    'Sharpe Ratio (versione sempl. senza rf)': '{:.2f}',
    'VaR (€)': '{:.2f}'
})
