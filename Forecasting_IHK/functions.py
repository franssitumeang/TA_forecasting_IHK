import pandas as pd
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 8, 4
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np
from statsmodels.tsa.stattools import adfuller, acf, pacf
import statsmodels.api as sm
import datetime
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_absolute_error

class tsStationerClass():
    d = 0
    ts = None


def get_ts(csv):
    data = pd.read_csv(csv)
    data['Waktu'] = pd.to_datetime(data['Waktu'])
    index = data.set_index('Waktu')
    ts = index['IHK']
    return ts

def replace_file_name(path):
    csv_file_name = path[12:len(path)]
    return csv_file_name

def get_name_region(file_name):
    file_name = file_name[::-1]
    file_name = file_name[4:len(file_name)]
    return file_name[::-1]

def plot_ts(ts, region_name):
    plt.plot(ts)
    plt.title('Original IHK Data in ' + region_name + ' Region')
    plt.savefig(
        'D:/Kuliah/Jupyter Notebook/TA/Django Project/Website/Forecasting_IHK/static/images/' + region_name + '.png')
    plt.close()

def plot_decomposition_ts(ts, region_name):
    decomposition = seasonal_decompose(ts)

    trend = decomposition.trend
    seasonal = decomposition.seasonal

    plt.subplot(211)
    plt.title('Trend & Seasonality Time Series')
    plt.plot(trend, label='Trend')
    plt.legend(loc='best')
    plt.subplot(212)
    plt.plot(seasonal, label='Seasonality')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('D:/Kuliah/Jupyter Notebook/TA/Django Project/Website/Forecasting_IHK/static/images/' + region_name + ' Decomposition.png')
    plt.close()

def transform_log(ts):
    ts_log = np.log(ts)
    return ts_log

def diffrencing_ts(ts):
    ts_diff = ts - ts.shift()
    ts_diff.dropna(inplace=True)
    return ts_diff

def test_stationarity(ts):
    dftest = adfuller(ts, autolag='AIC')
    return np.float16(dftest[1])

def ts_to_stationer(ts_class: tsStationerClass) -> tsStationerClass:
    new_ts = transform_log(ts_class.ts)
    if (test_stationarity(new_ts) < 0.05):
        ts_class.d = 0
        ts_class.ts = new_ts
    else:
        d = 0
        while(test_stationarity(new_ts) > 0.05):
            new_ts = diffrencing_ts(new_ts)
            d += 1
        ts_class.d = d
        ts_class.ts = new_ts

def plot_stationarity_ts(ts):
    rolmean = ts.rolling(window=52, center=False).mean()
    rolstd = ts.rolling(window=52, center=False).std()
    return rolmean, rolstd

def plot_acf_pacf_ts(ts, region_name):
    fig = plt.figure()
    ax1 = fig.add_subplot(221)
    fig = sm.graphics.tsa.plot_acf(ts, lags=20, ax=ax1)
    ax2 = fig.add_subplot(222)
    fig = sm.graphics.tsa.plot_pacf(ts, lags=20, ax=ax2)
    plt.savefig(
        'D:/Kuliah/Jupyter Notebook/TA/Django Project/Website/Forecasting_IHK/static/images/' + region_name + ' ACF_PACF.png')
    plt.close()

def ts_to_dict(ts):
    ts_dict = {}
    for i, v in ts.iteritems():
        B = datetime.datetime.strftime(i, '%B')
        Y = datetime.datetime.strftime(i, '%Y')
        key = B+' '+Y
        ts_dict[key] = '%.3f'%v
    return ts_dict

def get_index_dict(dictionary):
    return [i for i,v in dictionary.items()]

def get_value_dict(dictionary):
    return [v for i,v in dictionary.items()]

def get_seasonal(ts):
    decomposition = seasonal_decompose(ts)
    seasonal =  decomposition.seasonal
    return seasonal

def get_trend(ts):
    decomposition = seasonal_decompose(ts)
    trend =  decomposition.trend
    # seasonal.dropna(inplace=True)
    return trend

def get_acf_pacf_y0_ymin_yplus_lag(ts):
    n_lag = 24
    lag = [i for i in range(n_lag+1)]
    lag_acf = acf(ts, nlags=n_lag)
    lag_pacf = pacf(ts, nlags=n_lag, method='ols')
    lag_acf = lag_acf.tolist()
    lag_pacf = lag_pacf.tolist()
    y0 = [0]*len(lag_acf)
    ymin = [(-1.96/np.sqrt(len(ts)))]*len(lag_acf)
    yplus = [(1.96/np.sqrt(len(ts)))]*len(lag_acf)
    return lag_acf,lag_pacf,y0,ymin,yplus,lag

def get_exog(path):
    ts = get_ts(path)
    time_X = ['1/1/1999','1/1/2000','12/1/2001','12/1/2002','11/1/2003','11/1/2004','11/1/2005','10/1/2006','10/1/2007','10/1/2008',
        '9/1/2009','9/1/2010','8/1/2011','8/1/2012','8/1/2013','7/1/2014','7/1/2015','7/1/2016','6/1/2017']
    time_X = pd.to_datetime(time_X)
    for i, v in ts.iteritems():
        if(i in time_X):
            ts[i] = int(1)
        else:
            ts[i] = int(0)
    return ts

def parameter_significance_test(ts_log, ts, exogx,region_name):
    ordes = [(1,1,0),(0,1,0),(0,1,1),(1,1,1)]
    orde_rmse = {}
    for o in ordes:
        model = ARIMA(ts_log, order=o, exog=exogx)
        results_ARIMA = model.fit(disp=-1)
        predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
        predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
        predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
        predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
        predictions_ARIMA = np.exp(predictions_ARIMA_log)
        rmse = np.sqrt(sum((predictions_ARIMA-ts)**2)/len(ts))
        orde_rmse[o] = rmse
    deskripsi = ('RMSE dari uji signifikansi <b>Model ARIMAX(0,1,0)</b> terhadap parameter AR dan MA adalah<br>'
                '<b>ARIMAX(0, 1, 0) = '+str(orde_rmse[(0,1,0)])[:5]+'</b><br>'
                '<b>ARIMAX(1, 1, 0) = '+str(orde_rmse[(1,1,0)])[:5]+'</b><br>'
                '<b>ARIMAX(0, 1, 1) = '+str(orde_rmse[(0,1,1)])[:5]+'</b><br>'
                '<b>ARIMAX(1, 1, 1) = '+str(orde_rmse[(1,1,1)])[:5] +'</b><br>')
    orde_rmse = {k: orde_rmse[k] for k in sorted(orde_rmse)}
    deskripsi = (deskripsi + '<br>Dari hasil uji signifikansi didapatkan model dengan RMSE terendah adalah <b>Model ARIMAX'+
                str(list(orde_rmse.keys())[0])+'</b> dengan nilai <b>RMSE = '+str(list(orde_rmse.values())[0])[:5]+'</b><br>Maka Pemodelan ARIMAX yang digunakan untuk <b>Daerah '+region_name+'</b> adalah <b>Model ARIMAX'+str(list(orde_rmse.keys())[0])+'</b>')
    return list(orde_rmse.keys())[0],deskripsi

def get_desc_arimax_2(ts, region_name, orde):
    total_data = len(ts)
    train,test = len(ts)-12,12
    desc = ('Total data yang terdapat pada <b>Daerah '+region_name+'</b> adalah sebanyak <b>'+str(total_data)+' Data</b>. Data tersebut '
           'dibagi menjadi 2 bagian yaitu <b>'+str(train)+' Data Training</b> dan <b>'+str(test)+' Data Testing</b>.<br>'
           '<br>Berikut merupakan evaluasi dari <b>Single Model ARIMAX'+str(orde)+'</b> dengan menggunakan <b>'+str(test)+' Data Testing</b>.')
    return desc


def model_arimax(ts_log, exogx, orde):
    size = int(len(ts_log) - 12)
    train, h_exogx, test = ts_log[0:size], exogx[0:size], ts_log[size:len(ts_log)]
    history = [h for h in train]
    predictions = list()
    data_test = []
    data_predict = []
    ts = ts_log[size:]
    ts = np.exp(ts)

    label = []
    for i, v in ts.iteritems():
        B = datetime.datetime.strftime(i, '%B')
        Y = datetime.datetime.strftime(i, '%Y')
        label.append(B + ' ' + Y)

    for t in range(len(test)):
        model = ARIMA(history, order=orde, exog=h_exogx)
        model_fit = model.fit(disp=False, transparams=False)
        output = model_fit.forecast(steps=size + t, exog=h_exogx)

        yhat = output[0][0]
        predictions.append(float(yhat))
        obs = test[t]
        history.append(obs)
        h_exogx = exogx[:size + t + 1]
        data_test.append(np.exp(obs))
        data_predict.append(np.exp(yhat))

    data_test = ['%.2f' % i for i in data_test]
    data_predict = ['%.2f' % i for i in data_predict]
    mape = mean_absolute_error(test, predictions)
    return label, '%.6f' % mape, data_test, data_predict


