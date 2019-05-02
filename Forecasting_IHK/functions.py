import pandas as pd
import numpy as np
from pandas import DataFrame
from io import StringIO
import time, json
from datetime import date
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.arima_model import ARIMA,ARMA
from statsmodels.tsa.arima_model import ARIMAResults,ARMAResults
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
import statsmodels.api as sm
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.svm import SVR
import math
from scipy import stats
import datetime
from sklearn.cross_validation import train_test_split
import datetime
import calendar

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
    new_ts = ts_class.ts
    if (test_stationarity(new_ts) <= 0.05):
        ts_class.d = 0
        ts_class.ts = new_ts
    else:
        d = 0
        while(test_stationarity(new_ts) > 0.05):
            new_ts = diffrencing_ts(new_ts)
            d = d + 1
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
    n_lag = 11
    lag = [i for i in range(n_lag+1)]
    lag_acf = acf(ts, nlags=n_lag)
    lag_pacf = pacf(ts, nlags=n_lag, method='ols')
    lag_acf = lag_acf.tolist()
    lag_pacf = lag_pacf.tolist()
    y0 = [0]*len(lag_acf)
    ymin = [(-1.96/np.sqrt(len(ts)))]*len(lag_acf)
    yplus = [(1.96/np.sqrt(len(ts)))]*len(lag_acf)
    return lag_acf,lag_pacf,y0,ymin,yplus,lag

# get ACF and PACF value
def diff_ts(ts):
    mean = ts.mean()
    step = 1

    sum_diff_arr = []
    for i in range(len(ts)):
        j = 0
        sum_diff = 0.0
        while (j + step < len(ts)):
            sum_diff += ((ts[j] - mean) * (ts[j + step] - mean))
            j += 1
        step += 1
        sum_diff_arr.append(sum_diff)
    sum_diff_square_arr = [(x - mean) * (x - mean) for x in sum_diff_arr]
    ACF = []
    for x in sum_diff_arr:
        ACF.append(x / sum(sum_diff_square_arr))
    PACF_dict = {}
    for k in range(len(ts)):
        j = 1
        sum_PACF_ACF_A = 0.0
        sum_PACF_ACF_B = 0.0
        while (j <= k):
            sum_PACF_ACF_A += (PACF_dict[str(k) + str(j)] * ACF[k + 1 - j])
            sum_PACF_ACF_B += (PACF_dict[str(k) + str(j)] * ACF[j])
            j += 1
        PACF_dict[str(k + 1) + str(k + 1)] = (ACF[k] - sum_PACF_ACF_A) / (1 - sum_PACF_ACF_B)

        j = 1
        while (j <= k):
            PACF_dict[str(k + 1) + str(j)] = PACF_dict[str(k) + str(j)] - (
                        PACF_dict[str(k + 1) + str(k + 1)] * PACF_dict[str(k) + str(k + 1 - j)])
            j += 1
    PACF = []
    for i in range(len(ts)):
        PACF.append(PACF_dict[str(i + 1) + str(i + 1)])
    ACF_limit_A = []
    for i in range(len(ACF)):
        sum_of_acf = 0.0
        for j in range(i + 1):
            sum_of_acf += (ACF[i] * 2)
        ACF_limit_A.append(math.sqrt(1 / (len(ACF) * (1.0 + sum_of_acf))))
    ACF_limit_B = [x * -1 for x in ACF_limit_A]
    PACF_limit_A = [(2.0 / math.sqrt(len(PACF))) for _ in PACF]
    PACF_limit_B = [x * -1 for x in PACF_limit_A]
    ACF.insert(0, 1.0)
    PACF.insert(0, 1.0)
    return ACF[:25], PACF[:25], ACF_limit_A[:25], ACF_limit_B[:25], PACF_limit_A[:25], PACF_limit_B[:25], [i for i in
                                                                                                           range(25)],[0]*25

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

def parameter_significance_test(ts, region_name):
    resid_ts = residual_ts(ts)
    b0,b1 = regression(ts)
    time_X = ['1/1/1999','1/1/2000','12/1/2001','12/1/2002','11/1/2003','11/1/2004','11/1/2005','10/1/2006','10/1/2007','10/1/2008',
        '9/1/2009','9/1/2010','8/1/2011','8/1/2012','8/1/2013','7/1/2014','7/1/2015','7/1/2016','6/1/2017']
    time_X = pd.to_datetime(time_X)
    ordes = [(1,1,0),(0,1,0),(0,1,1)]
    orde_rmse = {}
    for o in ordes:
        model = ARIMA(resid_ts, order=o)
        results_ARIMA = model.fit(disp=-1)
        residual_ARIMAX = []
        result_predict_arima = [resid_ts[0]]
        for i in range (len(results_ARIMA.fittedvalues)):
            if(i > 0):
                result_predict_arima.append(result_predict_arima[i-1]+results_ARIMA.fittedvalues[i])
            else:
                result_predict_arima.append(result_predict_arima[0]+results_ARIMA.fittedvalues[i])
        for i in range(len(ts)):
            if (ts.index[i] in time_X):
                residual_ARIMAX.append(ts[i] - (b0+(b1*1)+result_predict_arima[i]))
            else:
                residual_ARIMAX.append(ts[i] - (b0+(b1*0)+result_predict_arima[i]))
        residual_ARIMAX = [x**2 for x in residual_ARIMAX]
        rmse = np.sqrt(sum(residual_ARIMAX)/len(ts))
        orde_rmse[o] = rmse
    deskripsi = ('<b>RMSE<i>(Root Mean Squared Error)</i></b> dari uji signifikansi <b>Model ARIMAX(0,1,0)</b> terhadap parameter AR dan MA adalah:<br>'
                '<b>ARIMAX(0, 1, 0) = '+str(orde_rmse[(0,1,0)])[:5]+'</b><br>'
                '<b>ARIMAX(1, 1, 0) = '+str(orde_rmse[(1,1,0)])[:5]+'</b><br>'
                '<b>ARIMAX(0, 1, 1) = '+str(orde_rmse[(0,1,1)])[:5]+'</b><br>')
    orde_rmse = sorted(orde_rmse.items(), key=lambda kv: kv[1])
    deskripsi = (deskripsi + '<br>Dari hasil uji signifikansi didapatkan model dengan RMSE terendah adalah <b>Model ARIMAX'+
                str(orde_rmse[0][0])+'</b> dengan nilai <b>RMSE = '+str(orde_rmse[0][1])[:5]+'</b><br>Maka Pemodelan ARIMAX yang digunakan untuk <b>Daerah '+region_name+'</b> adalah <b>Model ARIMAX'+str(orde_rmse[0][0])+'</b>')
    return orde_rmse[0][0],deskripsi

def get_desc_arimax_2(ts, region_name, orde):
    N_test30 = int(len(ts) * 30 / 100)
    N_test20 = int(len(ts) * 20 / 100)
    N_test10 = int(len(ts) * 10 / 100)
    total_data = len(ts)
    train70, test30 = total_data - N_test30, N_test30
    train80, test20 = total_data - N_test20, N_test20
    train90, test10 = total_data - N_test10, N_test10
    desc = ('Total data yang terdapat pada <b>Daerah '+region_name+'</b> adalah sebanyak <b>'+str(total_data)+' Data</b>. Data tersebut '
           'dibagi menjadi 3 pembagian data:<br><b><ol><li>70% data training('+str(train70)+' data) & 30% data testing('+str(test30)+' data)</li>'
           '<li>80% data training('+str(train80)+' data) & 20% data testing('+str(test20)+' data)</li>'
           '<li>90% data training('+str(train90)+' data) & 10% data testing('+str(test10)+' data)</li></ol></b>')
    return desc

# modeling ARIMAX
def ARIMAX(ts, orde, n_test):
    resid_ts = residual_ts(ts)
    b0, b1 = regression(ts)
    time_X = ['1/1/1999', '1/1/2000', '12/1/2001', '12/1/2002', '11/1/2003', '11/1/2004', '11/1/2005', '10/1/2006',
              '10/1/2007', '10/1/2008',
              '9/1/2009', '9/1/2010', '8/1/2011', '8/1/2012', '8/1/2013', '7/1/2014', '7/1/2015', '7/1/2016',
              '6/1/2017']
    time_X = pd.to_datetime(time_X)
    N_test = int(len(ts) * n_test / 100)
    size = int(len(ts) - N_test)
    train, test = resid_ts[0:size], ts[size:len(ts)]
    history = [float(h) for h in train]
    data_test = []
    data_predict = []

    label = []
    for i in test.index:
        B = datetime.datetime.strftime(i, '%B')
        Y = datetime.datetime.strftime(i, '%Y')
        label.append(B + ' ' + Y)

    model = ARIMA(history, order=orde)
    model_fit = model.fit(disp=False, transparams=False)
    output = model_fit.forecast(steps=size)
    for i in range(len(test)):
        yhat = output[0][i]
        data_test.append(test[i])
        if test.index[i] in time_X:
            data_predict.append(b0 + (b1 * 1) + yhat)
        else:
            data_predict.append(b0 + (b1 * 0) + yhat)

    mape = accuracy(data_test, data_predict)
    rmse = mean_squared_error(data_test, data_predict)
    rmse = np.sqrt(rmse)
    return label, '%.2f' % (100 - float(mape)), '%.2f' % rmse, data_test, data_predict

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
def save_residuals(ts, orde, region_name):
    resid_ts = residual_ts(ts)
    b0, b1 = regression(ts)
    time_X = ['1/1/1999', '1/1/2000', '12/1/2001', '12/1/2002', '11/1/2003', '11/1/2004', '11/1/2005', '10/1/2006',
              '10/1/2007', '10/1/2008',
              '9/1/2009', '9/1/2010', '8/1/2011', '8/1/2012', '8/1/2013', '7/1/2014', '7/1/2015', '7/1/2016',
              '6/1/2017']
    time_X = pd.to_datetime(time_X)
    model = ARIMA(resid_ts, order=orde)
    results_ARIMA = model.fit(disp=-1)
    result_predict_arima = [resid_ts[0]]
    for i in range(len(results_ARIMA.fittedvalues)):
        if (i > 0):
            result_predict_arima.append(result_predict_arima[i - 1] + results_ARIMA.fittedvalues[i])
        else:
            result_predict_arima.append(result_predict_arima[0] + results_ARIMA.fittedvalues[i])
    residuals = []
    for i in range(len(ts)):
        if ts.index[i] in time_X:
            residuals.append(ts[i] - (b0 + (b1 * 1) + result_predict_arima[i]))
        else:
            residuals.append(ts[i] - (b0 + (b1 * 0) + result_predict_arima[i]))
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
    residulas_df.to_csv(
        'D:/Kuliah/Jupyter Notebook/TA/Forecasting IHK/Forecasting/Residual/' + region_name + ' Residual.csv',
        encoding='utf-8', index=False)

def get_residual_data(region_name):
    return pd.read_csv('D:/Kuliah/Jupyter Notebook/TA/Forecasting IHK/Forecasting/Residual/'+region_name+' Residual.csv')

# modeling ARIMAX - SVR
def ARIMAX_SVR(ts, orde, n_test, residual_data):
    resid_ts = residual_ts(ts)
    b0, b1 = regression(ts)
    time_X = ['1/1/1999', '1/1/2000', '12/1/2001', '12/1/2002', '11/1/2003', '11/1/2004', '11/1/2005', '10/1/2006',
              '10/1/2007', '10/1/2008',
              '9/1/2009', '9/1/2010', '8/1/2011', '8/1/2012', '8/1/2013', '7/1/2014', '7/1/2015', '7/1/2016',
              '6/1/2017']
    time_X = pd.to_datetime(time_X)
    N_test = int(len(ts) * n_test / 100)
    #SVR
    parameter_SVR = {10: [24000.0, 0.01, 0.25],
                     23: [1000.0, 0.01, 0.02],
                     30: [1000.0, 0.27, 0.8]}

    train_residual = residual_data[:len(residual_data) - N_test]
    test_residual = residual_data[len(residual_data) - N_test:]

    X_train_residual = train_residual.values[:, :1]
    Y_train_residual = train_residual.values[:, 3]

    X_test_residual = test_residual.values[:, :1]
    Y_test_residual = test_residual.values[:, 3]
    X_train_residual, X_validation, Y_train_residual, Y_validation = train_test_split(X_train_residual,
                                                                                      Y_train_residual, test_size=0.2,
                                                                                      random_state=0)
    svr_rbf = SVR(kernel='rbf', C=parameter_SVR[n_test][0], gamma=parameter_SVR[n_test][1],
                  epsilon=parameter_SVR[n_test][2])

    svr_rbf.fit(X_train_residual, Y_train_residual)
    Y_predictSVR = svr_rbf.predict(X_test_residual)

    #ARIMAX
    size = int(len(ts) - N_test)

    train, test = resid_ts[0:size], ts[size:len(ts)]
    history = [float(h) for h in train]
    data_test = []
    data_predict = []

    label = []
    for i in test.index:
        B = datetime.datetime.strftime(i, '%B')
        Y = datetime.datetime.strftime(i, '%Y')
        label.append(B + ' ' + Y)

    model = ARIMA(history, order=orde)
    model_fit = model.fit(disp=False, transparams=False)
    output = model_fit.forecast(steps=size)
    for i in range(len(test)):
        yhat = output[0][i]
        data_test.append(test[i])
        if test.index[i] in time_X:
            data_predict.append(b0 + (b1 * 1) + yhat + Y_predictSVR[i])
        else:
            data_predict.append(b0 + (b1 * 0) + yhat + Y_predictSVR[i])

    mape = accuracy(data_test, data_predict)
    rmse = mean_squared_error(data_test, data_predict)
    rmse = np.sqrt(rmse)
    return label, '%.2f' % (100 - float(mape)), '%.2f' % rmse, data_test, data_predict

def get_desc_hybrid_1(orde):
    desc = ('Hasil dari pemodelan <b>Single ARIMAX'+str(orde)+'</b> akan menghasilkan <b>Nilai Error</b> atau <b>Residual.</b><br>'
            '<b>Residual</b> tersebut akan dimodelkan dengan menggunakan <b>SVR</b> untuk mendapatkan <b>Model Hybrid ARIMAX - SVR.</b> '
            'Pada simulator ini menggunakan <b>Lag ke 1</b> dari <b>Residual</b> sebagai <b>Input SVR</b><br><br>')
    return desc

def get_desc_hybrid_2(orde):
    desc = ('Berikut merupakan 3 evaluasi dari <b>Hybrid Model ARIMAX'+str(orde)+' - SVR</b>.')
    return desc


def accuracy(data_test, data_predict):
    sum_abs = []
    sum_abs_per_test = 0.0
    for i in range(len(data_test)):
        sum_abs.append(np.abs(data_test[i] - data_predict[i]))

    for i in range(len(sum_abs)):
        sum_abs_per_test += (float(sum_abs[i]) / float(data_test[i]))
    return ((sum_abs_per_test / len(data_test)) * 100)


def regression(ts):
    n = len(ts)
    time_X = ['1/1/1999','1/1/2000','12/1/2001','12/1/2002','11/1/2003','11/1/2004','11/1/2005','10/1/2006','10/1/2007','10/1/2008',
        '9/1/2009','9/1/2010','8/1/2011','8/1/2012','8/1/2013','7/1/2014','7/1/2015','7/1/2016','6/1/2017']
    time_X = pd.to_datetime(time_X)
    Y = []
    X = []
    for k,v in ts.iteritems():
        Y.append(v)
        if(k in time_X):
            X.append(1)
        else:
            X.append(0)
    X_sum = sum(X)
    Y_sum = sum(Y)
    XY = []
    for i in range(n):
        XY.append(X[i]*Y[i])
    XY_sum = sum(XY)
    X_sum_square = X_sum*X_sum
    b0 = ((Y_sum*X_sum)-(X_sum*XY_sum))/((n*X_sum)-X_sum_square)
    b1 = ((n*XY_sum)-(X_sum*Y_sum))/((n*X_sum)-X_sum_square)
    return b0,b1

def predicted_regression(ts):
    b0,b1 = regression(ts)
    predicted = []
    n = len(ts)
    time_X = ['1/1/1999','1/1/2000','12/1/2001','12/1/2002','11/1/2003','11/1/2004','11/1/2005','10/1/2006','10/1/2007','10/1/2008',
        '9/1/2009','9/1/2010','8/1/2011','8/1/2012','8/1/2013','7/1/2014','7/1/2015','7/1/2016','6/1/2017']
    time_X = pd.to_datetime(time_X)
    X = []
    for k,_ in ts.iteritems():
        if(k in time_X):
            X.append(1)
        else:
            X.append(0)
    for i in range(n):
        predicted.append(b0+(b1*X[i]))
    return predicted

def residual_regression(ts):
    n = len(ts)
    predicted = predicted_regression(ts)
    residual = []
    Y = []
    for _,v in ts.iteritems():
        Y.append(v)
    for i in range(n):
        residual.append(Y[i]-predicted[i])
    return residual

def residual_ts(ts):
    k = [k for k,_ in ts.iteritems()]
    resid = residual_regression(ts)
    resid_ts = pd.Series(data=resid,index=k)
    return resid_ts


def add_one_month(orig_date):
    new_year = orig_date.year
    new_month = orig_date.month + 1
    if new_month > 12:
        new_year += 1
        new_month -= 12

    last_day_of_month = calendar.monthrange(new_year, new_month)[1]
    new_day = min(orig_date.day, last_day_of_month)

    return orig_date.replace(year=new_year, month=new_month, day=new_day)


def PREDICT_12_DATA(ts, orde):
    resid_ts = residual_ts(ts)
    b0, b1 = regression(ts)
    time_X = ['1/1/1999', '1/1/2000', '12/1/2001', '12/1/2002', '11/1/2003', '11/1/2004', '11/1/2005', '10/1/2006',
              '10/1/2007', '10/1/2008',
              '9/1/2009', '9/1/2010', '8/1/2011', '8/1/2012', '8/1/2013', '7/1/2014', '7/1/2015', '7/1/2016',
              '6/1/2017', '6/1/2018']
    time_X = pd.to_datetime(time_X)

    history = [float(h) for h in resid_ts]
    data_predict = []

    last_date = ts.index[len(ts) - 1]
    label_date = [add_one_month(last_date)]
    for i in range(1, 12):
        label_date.append(add_one_month(label_date[i - 1]))
    label = []

    for i in label_date:
        B = datetime.datetime.strftime(i, '%B')
        Y = datetime.datetime.strftime(i, '%Y')
        label.append(B + ' ' + Y)

    model = ARIMA(history, order=orde)
    model_fit = model.fit(disp=False, transparams=False)
    output = model_fit.forecast(steps=12)

    for i in range(12):
        yhat = output[0][i]
        if label_date[i] in time_X:
            data_predict.append(b0 + (b1 * 1) + yhat)
        else:
            data_predict.append(b0 + (b1 * 0) + yhat)

    return label, ['%.2f' % x for x in data_predict]














































def get_a():
    print('DEBUG fungsi get_a')
    return 'from get_a'

