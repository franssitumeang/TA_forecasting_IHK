from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
import matplotlib.pyplot as plt
from Forecasting_IHK import functions
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles import finders
import json

a = functions.get_a()

def test_1(request):
    return HttpResponse(a)


def index(request):
    content = {

    }
    return render(request, 'index.html', content)

@csrf_exempt
def plot_original_data(request):
    if (request.method == 'POST'):
        path = request.POST['path']
        csv_file_name = functions.replace_file_name(path)
        path_csv = 'D:/Kuliah/Jupyter Notebook/TA/Forecasting IHK/Forecasting/IHK/'+csv_file_name
        region_name = functions.get_name_region(csv_file_name)
        ts = functions.get_ts(path_csv)
        dict = functions.ts_to_dict(ts)
        label = functions.get_index_dict(dict)
        time_variance = functions.get_str_time_variance(functions.get_exog('D:/Kuliah/Jupyter Notebook/TA/Forecasting IHK/Forecasting/IHK/'+csv_file_name))
        desc = ('Grafik diatas menggambarkan distribusi nilai IHK pada <b>Daerah '+region_name+'</b>. '
                'Data IHK yang terdapat pada <b>Daerah '+region_name+'</b> adalah sebanyak <b>'+str(len(ts))+' data</b> dari '
                '<b>'+label[0]+'</b> sampai <b>'+label[len(label)-1]+'</b>, data yang digunakan adalah data perbulan.<br><br>'
                'Pada Simulator ini menggunakan variabel pendukung dalam hal ini adalah <b>Variansi Kalender</b> sebagai salah '
                'satu faktor dalam melakukan peramalan. Variansi Kalender yang digunakan adalah <b>efek Hari Raya Idul Fitri. </b>'
                '<b>Data Variansi Kalender</b> yang diperoleh dari data IHK pada <b>Daerah '+region_name+'</b> adalah:<br><b>'+time_variance+'</b>')
        data = {'region_name':region_name,'label': label, 'data': functions.get_value_dict(dict),'desc':desc}
        return JsonResponse(data)

@csrf_exempt
def plot_decomposition_ts(request):
    if (request.method == 'POST'):
        path = request.POST['path']
        csv_file_name = functions.replace_file_name(path)
        path_csv = 'D:/Kuliah/Jupyter Notebook/TA/Forecasting IHK/Forecasting/IHK/'+csv_file_name
        region_name = functions.get_name_region(csv_file_name)
        ts = functions.get_ts(path_csv)
        dict_trend = functions.ts_to_dict(functions.get_trend(ts))
        dict_seasonal = functions.ts_to_dict(functions.get_seasonal(ts))
        desc_trend = ('Grafik diatas menggambarkan trend data IHK yang terdapat pada <b>Daerah '+region_name+'</b>.')
        desc_seasonal = ('Grafik diatas menggambarkan data IHK musiman yang terdapat pada <b>Daerah ' + region_name + '</b>.')
        data = {'region_name': region_name, 'label_trend': functions.get_index_dict(dict_trend),
                'data_trend': functions.get_value_dict(dict_trend), 'label_seasonal':functions.get_index_dict(dict_seasonal),
                'data_seasonal': functions.get_value_dict(dict_seasonal),
                'desc_trend': desc_trend, 'desc_seasonal':desc_seasonal}
        return JsonResponse(data)

@csrf_exempt
def plot_stationarity_ts(request):
    if (request.method == 'POST'):
        path = request.POST['path']
        csv_file_name = functions.replace_file_name(path)
        path_csv = 'D:/Kuliah/Jupyter Notebook/TA/Forecasting IHK/Forecasting/IHK/' + csv_file_name
        region_name = functions.get_name_region(csv_file_name)
        ts = functions.get_ts(path_csv)
        ts_stationer = functions.tsStationerClass()
        ts_stationer.ts = ts
        functions.ts_to_stationer(ts_stationer)
        rolmean,rolstd = functions.plot_stationarity_ts(ts_stationer.ts)
        dict_original = functions.ts_to_dict(ts_stationer.ts)
        dict_rolmean = functions.ts_to_dict(rolmean)
        p_value = functions.test_stationarity(ts)
        desc = ('Sebelum melakukan pemodelan dengan <b>ARIMAX</b>, terlebih dahulu <b>Data Time Series Harus Stasioner terhadap Rataan.'
                '</b> Dalam melakukan uji stasioner data, pada simulator ini menggunakan <b>Dicky-Fuller test.</b> Syarat dari '
                '<b>Dicky Fuller test</b> adalah:<br>'
                '<ul><li><b>Jika p-value > 0.05 : Data Time Series tidak Stasioner</b></li>'
                '<li><b>Jika p-value <= 0.05 : Data Time Series Stasioner</b></li></ul>'
                '<b>p-value</b> untuk data awal adalah : <b>'+str(p_value)+'.</b>')
        if(p_value > 0.05):
            p_value = functions.test_stationarity(ts_stationer.ts)
            desc += (' <b>Data Time Series</b> tersebut <b>belum Stasioner</b>. Maka dari itu dilakukan proses <b> Transform & Diffrencing '
                     ''+str(ts_stationer.d)+' kali</b>. Sehingga diperoleh <b>p-value : '+str(p_value)+'.</b>')
        desc += (' <b>Data Time Series</b> tersebut <b>sudah Stasioner</b>.<br>Grafik diatas menggambarkan data yang telah stasioner.')
        data = {'label': functions.get_index_dict(dict_original),
                'data_rolmean': functions.get_value_dict(dict_rolmean),
                'data_original': functions.get_value_dict(dict_original),
                'd':ts_stationer.d,
                'desc': desc}
        return JsonResponse(data)

@csrf_exempt
def plot_acf_pacf_ts(request):
    if (request.method == 'POST'):
        path = request.POST['path']
        csv_file_name = functions.replace_file_name(path)
        path_csv = 'D:/Kuliah/Jupyter Notebook/TA/Forecasting IHK/Forecasting/IHK/' + csv_file_name
        region_name = functions.get_name_region(csv_file_name)
        ts = functions.get_ts(path_csv)
        ts_stationer = functions.tsStationerClass()
        ts_stationer.ts = ts
        functions.ts_to_stationer(ts_stationer)
        ACF, PACF, ACF_limit_A, ACF_limit_B, PACF_limit_A, PACF_limit_B, lag, y0 = functions.diff_ts(ts_stationer.ts)
        desc = ('Untuk dapat melakukan pemodelan dengan ARIMAX dibutuhkan 3 paremeter yaitu <b>AR, I,</b> dan <b>MA.</b> '
                'Pada simulator ini nilai dari parameter <b>I</b> telah otomatis di generate yaitu dengan menghitung banyak '
                'diffrencing yang dilakukan sehingga data stasioner, namun untuk parameter <b>AR</b> dan <b>MA</b> '
                'harus dilakukan secara manual yaitu dengan cara:'
                '<ul><li><b>Untuk orde Q yang digunakan sebagai orde parameter MA perhatikan grafik Autocorrelation(ACF), '
                'di Lag keberapa nilai ACF(Garis Biru) keluar dari titik Y(Garis Abu-abu).</b></li>'
                '<li><b>Untuk orde P yang digunakan sebagai orde parameter AR perhatikan grafik Partial Autocorrelation(PACF), '
                'di Lag keberapa nilai PACF(Garis Biru) keluar dari antara titik Y(Garis Abu-abu) = ' +str(PACF_limit_A[0])[:4] + ' dan Y(Garis Abu-abu) = ' + str(PACF_limit_A[0])[:5] + '.</b></li></ul>')
        data = {'label': lag, 'data_acf':ACF,
                'data_pacf':PACF,'y0':y0,
                'yplusACF':ACF_limit_A, 'yminACF':ACF_limit_B,
                'yplusPACF': PACF_limit_A, 'yminPACF': PACF_limit_B,
                'desc':desc}
        return JsonResponse(data)

@csrf_exempt
def modeling(request):
    if (request.method == 'POST'):
        path = request.POST['path']
        AR = int(request.POST['AR'])
        I = int(request.POST['I'])
        MA = int(request.POST['MA'])
        csv_file_name = functions.replace_file_name(path)
        path_csv = 'D:/Kuliah/Jupyter Notebook/TA/Forecasting IHK/Forecasting/IHK/' + csv_file_name
        region_name = functions.get_name_region(csv_file_name)
        ts = functions.get_ts(path_csv)
        desc_arima_1 = ''
        orde = (AR,I, MA)
        if(orde == (0,1,0)):
            orde,desc_arima_1 = functions.parameter_significance_test(ts,region_name)
        desc_arima_2 = functions.get_desc_arimax_2(ts,region_name,orde)
        label_30, accuracy_arimax_30, rmse_arimax_30, test_arimax_30, predict_arimax_30 = functions.ARIMAX(ts,orde,30)
        label_20, accuracy_arimax_20, rmse_arimax_20, test_arimax_20, predict_arimax_20 = functions.ARIMAX(ts, orde, 23)
        # label_10, accuracy_arimax_10, rmse_arimax_10, test_arimax_10, predict_arimax_10 = functions.ARIMAX(ts, orde, 10)
        functions.save_residuals(ts, orde, region_name)


        desc_hybrid_1 = functions.get_desc_hybrid_1(orde)
        desc_hybrid_2 = functions.get_desc_hybrid_2(orde)
        residual_data = functions.get_residual_data(region_name)
        _, accuracy_hybrid_30, rmse_hybrid_30, test_hybrid_30, predict_hybrid_30 = functions.ARIMAX_SVR(ts, orde, 30, residual_data)
        _, accuracy_hybrid_20, rmse_hybrid_20, test_hybrid_20, predict_hybrid_20 = functions.ARIMAX_SVR(ts, orde, 23,
                                                                                                        residual_data)
        # _, accuracy_hybrid_10, rmse_hybrid_10, test_hybrid_10, predict_hybrid_10 = functions.ARIMAX_SVR(ts, orde, 10,
        #                                                                                                 residual_data)

        label_pred, predict_12 = functions.PREDICT_12_DATA(ts,orde)
        data = {'desc_arima_1': desc_arima_1,
                'desc_arima_2': desc_arima_2,
                'label_30': label_30,
                'test_arimax_30': test_arimax_30,
                'predict_arimax_30': predict_arimax_30,
                'label_20': label_20,
                'test_arimax_20': test_arimax_20,
                'predict_arimax_20': predict_arimax_20,
                # 'label_10': label_10,
                # 'test_arimax_10': test_arimax_10,
                # 'predict_arimax_10': predict_arimax_10,
                'rmse_arimax_30':rmse_arimax_30,
                'rmse_arimax_20': rmse_arimax_20,
                # 'rmse_arimax_10': rmse_arimax_10,
                'accuracy_arimax_30':accuracy_arimax_30,
                'accuracy_arimax_20': accuracy_arimax_20,
                # 'accuracy_arimax_10': accuracy_arimax_10,
                'desc_hybrid_1':desc_hybrid_1,
                'desc_hybrid_2': desc_hybrid_2,
                'test_hybrid_30':test_hybrid_30,
                'predict_hybrid_30':predict_hybrid_30,
                'test_hybrid_20': test_hybrid_20,
                'predict_hybrid_20': predict_hybrid_20,
                # 'test_hybrid_10': test_hybrid_10,
                # 'predict_hybrid_10': predict_hybrid_10,
                'rmse_hybrid_30':rmse_hybrid_30,
                'rmse_hybrid_20': rmse_hybrid_20,
                # 'rmse_hybrid_10': rmse_hybrid_10,
                'accuracy_hybrid_30':accuracy_hybrid_30,
                'accuracy_hybrid_20': accuracy_hybrid_20,
                # 'accuracy_hybrid_10': accuracy_hybrid_10,
                'label_pred':label_pred,
                'predict_12':predict_12,
            }
        return JsonResponse(data)