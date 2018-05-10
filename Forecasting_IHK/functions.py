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
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR

class tsStationerClass():
    d = 0
    ts = None

# get file csv from directory
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

# transform data
def transform_log(ts):
    ts_log = np.log(ts)
    return ts_log

# diffrencing data
def diffrencing_ts(ts):
    ts_diff = ts - ts.shift()
    ts_diff.dropna(inplace=True)
    return ts_diff

# test stationarity data using dickey-fuller
def test_stationarity(ts):
    dftest = adfuller(ts, autolag='AIC')
    return np.float16(dftest[1])

# make data to stationer
def ts_to_stationer(ts_class: tsStationerClass) -> tsStationerClass:
    new_ts = transform_log(ts_class.ts)
    if (test_stationarity(new_ts) <= 0.05):
        ts_class.d = 0
        ts_class.ts = new_ts
    else:
        d = 0
        while(test_stationarity(new_ts) > 0.05):
            new_ts = diffrencing_ts(new_ts)
            d += 1
        ts_class.d = d
        ts_class.ts = new_ts

# get stationarity data
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

# get seasonal data
def get_seasonal(ts):
    decomposition = seasonal_decompose(ts)
    seasonal =  decomposition.seasonal
    return seasonal

# get trend data
def get_trend(ts):
    decomposition = seasonal_decompose(ts)
    trend =  decomposition.trend
    return trend

# get ACF and PACF value
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
    ordes = [(1,1,0),(0,1,0),(0,1,1)]
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
    deskripsi = ('<b>RMSE<i>(Root Mean Squared Error)</i></b> dari uji signifikansi <b>Model ARIMAX(0,1,0)</b> terhadap parameter AR dan MA adalah:<br>'
                '<b>ARIMAX(0, 1, 0) = '+str(orde_rmse[(0,1,0)])[:5]+'</b><br>'
                '<b>ARIMAX(1, 1, 0) = '+str(orde_rmse[(1,1,0)])[:5]+'</b><br>'
                '<b>ARIMAX(0, 1, 1) = '+str(orde_rmse[(0,1,1)])[:5]+'</b><br>')
    orde_rmse = {k: orde_rmse[k] for k in sorted(orde_rmse)}
    deskripsi = (deskripsi + '<br>Dari hasil uji signifikansi didapatkan model dengan RMSE terendah adalah <b>Model ARIMAX'+
                str(list(orde_rmse.keys())[0])+'</b> dengan nilai <b>RMSE = '+str(list(orde_rmse.values())[0])[:5]+'</b><br>Maka Pemodelan ARIMAX yang digunakan untuk <b>Daerah '+region_name+'</b> adalah <b>Model ARIMAX'+str(list(orde_rmse.keys())[0])+'</b>')
    return list(orde_rmse.keys())[0],deskripsi

def get_desc_arimax_2(ts, region_name, orde):
    N_test = int(len(ts) * 20 / 100)
    total_data = len(ts)
    train,test = len(ts)-N_test,N_test
    desc = ('Total data yang terdapat pada <b>Daerah '+region_name+'</b> adalah sebanyak <b>'+str(total_data)+' Data</b>. Data tersebut '
           'dibagi menjadi 2 bagian yaitu <b>'+str(train)+' Data Training</b> dan <b>'+str(test)+' Data Testing</b>.<br>'
           '<br>Berikut merupakan evaluasi dari <b>Single Model ARIMAX'+str(orde)+'</b> dengan menggunakan <b>'+str(test)+' Data Testing</b>.')
    return desc

# modeling ARIMAX
def model_arimax(ts_log, exogx, orde):
    N_test = int(len(ts_log) * 20 / 100)
    size = int(len(ts_log) - N_test)
    train, h_exogx, test = ts_log[0:size], exogx[0:size], ts_log[size:len(ts_log)]
    history = [float(h) for h in train]
    data_test = []
    data_predict = []
    ts = ts_log[size:]
    ts = np.exp(ts)

    label = []
    for i, v in ts.iteritems():
        B = datetime.datetime.strftime(i, '%B')
        Y = datetime.datetime.strftime(i, '%Y')
        label.append(B + ' ' + Y)

    model = ARIMA(history, order=orde, exog=h_exogx)
    model_fit = model.fit(disp=False, transparams=False)
    output = model_fit.forecast(steps=size, exog=h_exogx)
    for t in range(len(test)):
        yhat = output[0][t]
        obs = test[t]
        data_test.append(np.exp(obs))
        data_predict.append(np.exp(yhat))

    data_test = ['%.2f' % i for i in data_test]
    data_predict = ['%.2f' % i for i in data_predict]
    predictions = [np.log(float(i)) for i in data_predict]
    mape = mean_absolute_error(test, predictions)
    rmse = mean_squared_error(test, predictions)
    rmse = np.sqrt(rmse)
    return label, '%.6f' % mape, '%.6f' % rmse, data_test, data_predict

# get time variance from data
def get_str_time_variance(x):
    time_variance = [k for k,v in x.iteritems() if v == 1.0]
    time_variance = [datetime.datetime.strftime(t, '%B')+' '+ datetime.datetime.strftime(t, '%Y') for t in time_variance]
    str_time_variance = ''
    for i in range(len(time_variance)):
        if(i != len(time_variance)-1):
            str_time_variance += time_variance[i]+', '
        else:
            str_time_variance += time_variance[i]
    return str_time_variance

# Save Residual Data
def save_residuals(ts,orde,exogx,region_name):
    model = ARIMA(ts, order=orde, exog=exogx)
    results_ARIMA = model.fit(disp=-1)
    predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
    predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
    predictions_ARIMA_log = pd.Series(ts.ix[0], index=ts.index)
    predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
    predictions_ARIMA = np.exp(predictions_ARIMA_log)
    residuals = []
    for i in range(len(ts)):
        residuals.append(np.exp(ts[i]) - predictions_ARIMA[i])
    at1 = residuals[2:len(residuals) - 1]
    at2 = residuals[1:len(residuals) - 2]
    at3 = residuals[:len(residuals) - 3]
    residuals = residuals[3:]
    residulas_df = pd.DataFrame(
    {'residual': residuals,
     'at1': at1,
     'at2': at2,
     'at3': at3
    })
    residulas_df.to_csv('D:/Kuliah/Jupyter Notebook/TA/Forecasting IHK/Forecasting/Residual/'+region_name+' Residual.csv', encoding='utf-8', index=False)

def get_residual_data(region_name):
    return pd.read_csv('D:/Kuliah/Jupyter Notebook/TA/Forecasting IHK/Forecasting/Residual/'+region_name+' Residual.csv')

# modeling ARIMAX - SVR
def model_arimax_svr(ts_log, exogx, orde, residual_data):
    N_test = int(len(ts_log) * 20 / 100)
    #     SVR
    train_residual = residual_data[:len(residual_data) - N_test]
    test_residual = residual_data[len(residual_data) - N_test:]
    data_test = []
    data_predict = []
    rmses = []
    mapes = []
    label = []
    atmin = [1, 2, 3]
    for at in atmin:
        X_train_residual = train_residual.values[:, :at]
        Y_train_residual = train_residual.values[:, 3]

        X_test_residual = test_residual.values[:, :at]
        X_train_residual, X_validation, Y_train_residual, Y_validation = train_test_split(X_train_residual,
                                                                                          Y_train_residual, test_size=0.2,
                                                                                          random_state=0)
        svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
        svr_rbf.fit(X_train_residual, Y_train_residual)
        Y_predictSVR = svr_rbf.predict(X_test_residual)
        # ARIMAX
        size = int(len(ts_log) - N_test)
        train, h_exogx, test = ts_log[0:size], exogx[0:size], ts_log[size:len(ts_log)]
        history = [h for h in train]
        ts = ts_log[size:]
        ts = np.exp(ts)

        for i, v in ts.iteritems():
            B = datetime.datetime.strftime(i, '%B')
            Y = datetime.datetime.strftime(i, '%Y')
            label.append(B + ' ' + Y)

        model = ARIMA(history, order=orde, exog=h_exogx)
        model_fit = model.fit(disp=False, transparams=False)
        output = model_fit.forecast(steps=size, exog=h_exogx)
        for t in range(len(test)):
            yhat = output[0][t]
            obs = test[t]
            data_test.append(np.exp(obs))
            data_predict.append(np.exp(yhat) + Y_predictSVR[t])
        data_predict = ['%.2f' % float(i) for i in data_predict]
        predictions = [np.log(float(i)) for i in data_predict]
        test = [np.log(float(i)) for i in data_test]
        mape = mean_absolute_error(test, predictions)
        mapes.append(mape)
        rmse = mean_squared_error(test, predictions)
        rmse = np.sqrt(rmse)
        rmses.append(rmse)
    index = rmses.index(min(rmses))
    return label, '%.6f' % mapes[index], '%.6f' % rmses[index], data_test, data_predict, index

def get_desc_hybrid_1(orde, index):
    desc = ('Hasil dari pemodelan <b>Single ARIMAX'+str(orde)+'</b> akan menghasilkan <b>Nilai Error</b> atau <b>Residual.</b><br>'
            '<b>Residual</b> tersebut akan dimodelkan dengan menggunakan <b>SVR</b> untuk mendapatkan <b>Model Hybrid ARIMAX - SVR.</b> '
            'Pada simulator ini menggunakan <b>Lag 1, 2, dan 3</b> dari <b>Residual</b> sebagai <b>Input SVR</b><br><br>'
            '<b>Hasil Uji Input SVR,</b> didapat <b>Model Hybrid</b> terbaik adalah dengan <b>Input SVR</b> menggunakan ')
    if(index == 1):
        desc += ('<b>Lag 1.</b>')
    elif(index == 2):
        desc += ('<b>Lag 1 dan 2.</b>')
    elif (index == 3):
        desc += ('<b>Lag 1, 2 dan 3.</b>')
    return desc

def get_desc_hybrid_2(ts, orde):
    test = int(len(ts) * 20 / 100)
    desc = ('Berikut merupakan evaluasi dari <b>Hybrid Model ARIMAX'+str(orde)+' - SVR</b> dengan menggunakan <b>'+str(test)+' Data Testing</b>.')
    return desc














































def get_a():
    print('DEBUG fungsi get_a')
    return 'from get_a'

