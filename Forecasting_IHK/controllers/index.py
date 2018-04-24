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
        data = {'region_name': region_name, 'label_trend': functions.get_index_dict(dict_trend),
                'data_trend': functions.get_value_dict(dict_trend), 'label_seasonal':functions.get_index_dict(dict_seasonal),
                'data_seasonal': functions.get_value_dict(dict_seasonal)}
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
        data = {'label': functions.get_index_dict(dict_original),
                'data_rolmean': functions.get_value_dict(dict_rolmean),
                'data_original': functions.get_value_dict(dict_original),
                'd':ts_stationer.d}
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
        lag_acf, lag_pacf, y0, ymin, yplus, lag = functions.get_acf_pacf_y0_ymin_yplus_lag(ts_stationer.ts)
        data = {'label': lag, 'data_acf':lag_acf,
                'data_pacf':lag_pacf,'y0':y0,
                'ymin':ymin, 'yplus':yplus}
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
        ts_log = functions.transform_log(ts)
        exogx = functions.get_exog(path_csv)
        desc_arima_1 = ''
        orde = (AR,I, MA)
        if(orde == (0,1,0)):
            orde,desc_arima_1 = functions.parameter_significance_test(ts_log,ts,exogx,region_name)
        desc_arima_2 = functions.get_desc_arimax_2(ts,region_name,orde)
        label,mape_arima,data_test,data_predict_arima = functions.model_arimax(ts_log,exogx,orde)
        desc_mape_arima = ('Untuk melakukan evaluasi(mengukur keakuratan <b><i>Forecasting Model</i></b>) Model ARIMAX, pada simulator ini menggunakan '
                           '<b>MAPE(<i>Mean Absolute Percentage Error</i>).</b>'
                           '<br>Maka nilai <b>MAPE</b> dari <b>Single Model ARIMAX'+str(orde)+'</b> adalah <b>'+str(mape_arima)+'</b>.')


        data = {'desc_arima_1': desc_arima_1,
                'desc_arima_2': desc_arima_2,
                'label': label,
                'data_test': data_test,
                'desc_mape_arima': desc_mape_arima,
                'data_predict_arima': data_predict_arima,}
        return JsonResponse(data)