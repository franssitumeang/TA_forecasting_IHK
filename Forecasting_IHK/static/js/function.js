

$(document).ready(function(){
    // LOADING 
    $('#loading_pre_processing').hide();
    $('#loading_modeling').hide();



    $('#btn_plot_original').click(function(){ 
        
        view_original();
        view_trend_seasonal();
        view_stationarity();
        view_acf_pacf();
        
    })    



    $('#upload_btn').change(function(){
        $('#text_csv').text($(this).val());
        $('#title_page').text("Forecasting IHK "+$(this).val().split("\\")[2]);
        
    });


    $('#btn_modeling').click(function(){
        $('#loading_modeling').show();  
        $.ajax({
            type: 'POST',
            url: '/simulatorforecasting/modeling',
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}',
                path : $('#text_csv').text(),
                AR : $('#input_AR').val(),
                I : $('#input_I').val(),
                MA : $('#input_MA').val(),
            },
            success:function(data){     
                $('#loading_modeling').hide();
                $('#desc_arima_1').html(data.desc_arima_1);
                $('#desc_arima_2').html(data.desc_arima_2);
                $('#desc_hybrid_1').html(data.desc_hybrid_1);
                $('#desc_hybrid_2').html(data.desc_hybrid_2);
                var config_model_arimax_70_30 = {
                    type: 'line',
                    data: {
                        labels: data.label_30,
                        datasets: [{
                            label: 'Actual',
                            backgroundColor: window.chartColors.blue,
                            borderColor: window.chartColors.blue,
                            data: data.test_arimax_30,
                            fill: false,
                        },{
                            label: 'Predict',
                            backgroundColor: window.chartColors.red,
                            borderColor: window.chartColors.red,
                            data: data.predict_arimax_30,
                            fill: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Evaluate Single Model ARIMAX (70% Training - 30% Testing)'
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                        },
                        hover: {
                            mode: 'nearest',
                            intersect: true
                        },
                        scales: {
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Time'
                                }
                            }],
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'IHK Value'
                                }
                            }]
                        }
                    }
                };
                var config_model_arimax_80_20 = {
                    type: 'line',
                    data: {
                        labels: data.label_20,
                        datasets: [{
                            label: 'Actual',
                            backgroundColor: window.chartColors.blue,
                            borderColor: window.chartColors.blue,
                            data: data.test_arimax_20,
                            fill: false,
                        },{
                            label: 'Predict',
                            backgroundColor: window.chartColors.red,
                            borderColor: window.chartColors.red,
                            data: data.predict_arimax_20,
                            fill: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Evaluate Single Model ARIMAX (80% Training - 20% Testing)'
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                        },
                        hover: {
                            mode: 'nearest',
                            intersect: true
                        },
                        scales: {
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Time'
                                }
                            }],
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'IHK Value'
                                }
                            }]
                        }
                    }
                };
                var config_model_arimax_90_10 = {
                    type: 'line',
                    data: {
                        labels: data.label_10,
                        datasets: [{
                            label: 'Actual',
                            backgroundColor: window.chartColors.blue,
                            borderColor: window.chartColors.blue,
                            data: data.test_arimax_10,
                            fill: false,
                        },{
                            label: 'Predict',
                            backgroundColor: window.chartColors.red,
                            borderColor: window.chartColors.red,
                            data: data.predict_arimax_10,
                            fill: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Evaluate Single Model ARIMAX (90% Training - 10% Testing)'
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                        },
                        hover: {
                            mode: 'nearest',
                            intersect: true
                        },
                        scales: {
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Time'
                                }
                            }],
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'IHK Value'
                                }
                            }]
                        }
                    }
                };    
                var config_model_hybrid_70_30 = {
                    type: 'line',
                    data: {
                        labels: data.label_30,
                        datasets: [{
                            label: 'Actual',
                            backgroundColor: window.chartColors.blue,
                            borderColor: window.chartColors.blue,
                            data: data.test_hybrid_30,
                            fill: false,
                        },{
                            label: 'Predict',
                            backgroundColor: window.chartColors.red,
                            borderColor: window.chartColors.red,
                            data: data.predict_hybrid_30,
                            fill: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Evaluate Hybrid Model ARIMAX - SVR (70% Training - 30% Testing)'
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                        },
                        hover: {
                            mode: 'nearest',
                            intersect: true
                        },
                        scales: {
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Time'
                                }
                            }],
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'IHK Value'
                                }
                            }]
                        }
                    }
                };
                var config_model_hybrid_80_20 = {
                    type: 'line',
                    data: {
                        labels: data.label_20,
                        datasets: [{
                            label: 'Actual',
                            backgroundColor: window.chartColors.blue,
                            borderColor: window.chartColors.blue,
                            data: data.test_hybrid_20,
                            fill: false,
                        },{
                            label: 'Predict',
                            backgroundColor: window.chartColors.red,
                            borderColor: window.chartColors.red,
                            data: data.predict_hybrid_20,
                            fill: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Evaluate Hybrid Model ARIMAX - SVR (80% Training - 20% Testing)'
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                        },
                        hover: {
                            mode: 'nearest',
                            intersect: true
                        },
                        scales: {
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Time'
                                }
                            }],
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'IHK Value'
                                }
                            }]
                        }
                    }
                };     
                var config_model_hybrid_90_10 = {
                    type: 'line',
                    data: {
                        labels: data.label_10,
                        datasets: [{
                            label: 'Actual',
                            backgroundColor: window.chartColors.blue,
                            borderColor: window.chartColors.blue,
                            data: data.test_hybrid_10,
                            fill: false,
                        },{
                            label: 'Predict',
                            backgroundColor: window.chartColors.red,
                            borderColor: window.chartColors.red,
                            data: data.predict_hybrid_10,
                            fill: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Evaluate Hybrid Model ARIMAX - SVR (90% Training - 10% Testing)'
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                        },
                        hover: {
                            mode: 'nearest',
                            intersect: true
                        },
                        scales: {
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Time'
                                }
                            }],
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'IHK Value'
                                }
                            }]
                        }
                    }
                };            
                var ctx_model_arimax_70_30 = document.getElementById('canvas_predict_arimax_70_30').getContext('2d');
                var ctx_model_arimax_80_20 = document.getElementById('canvas_predict_arimax_80_20').getContext('2d');
                var ctx_model_arimax_90_10 = document.getElementById('canvas_predict_arimax_90_10').getContext('2d');
                
                window.myLine = new Chart(ctx_model_arimax_70_30, config_model_arimax_70_30);
                window.myLine = new Chart(ctx_model_arimax_80_20, config_model_arimax_80_20);
                window.myLine = new Chart(ctx_model_arimax_90_10, config_model_arimax_90_10);

                var ctx_model_hybrid_70_30 = document.getElementById('canvas_predict_hybrid_70_30').getContext('2d');
                var ctx_model_hybrid_80_20 = document.getElementById('canvas_predict_hybrid_80_20').getContext('2d');
                var ctx_model_hybrid_90_10 = document.getElementById('canvas_predict_hybrid_90_10').getContext('2d');

                window.myLine = new Chart(ctx_model_hybrid_70_30, config_model_hybrid_70_30);
                window.myLine = new Chart(ctx_model_hybrid_80_20, config_model_hybrid_80_20);
                window.myLine = new Chart(ctx_model_hybrid_90_10, config_model_hybrid_90_10);
                
                

                $('#rmse_arimax_30').text(data.rmse_arimax_30);
                $('#rmse_arimax_20').text(data.rmse_arimax_20);
                $('#rmse_arimax_10').text(data.rmse_arimax_10);

                $('#accuracy_arimax_30').text(data.accuracy_arimax_30+' %');
                $('#accuracy_arimax_20').text(data.accuracy_arimax_20+' %');
                $('#accuracy_arimax_10').text(data.accuracy_arimax_10+' %');

                $('#rmse_hybrid_30').text(data.rmse_hybrid_30);
                $('#rmse_hybrid_20').text(data.rmse_hybrid_20);
                $('#rmse_hybrid_10').text(data.rmse_hybrid_10);

                $('#accuracy_hybrid_30').text(data.accuracy_hybrid_30+' %');
                $('#accuracy_hybrid_20').text(data.accuracy_hybrid_20+' %');
                $('#accuracy_hybrid_10').text(data.accuracy_hybrid_10+' %');


                $('#date_1').text(data.label_pred[0]);
                $('#ihk_1').text(data.predict_12[0]);
                $('#date_2').text(data.label_pred[1]);
                $('#ihk_2').text(data.predict_12[1]);
                $('#date_3').text(data.label_pred[2]);
                $('#ihk_3').text(data.predict_12[2]);
                $('#date_4').text(data.label_pred[3]);
                $('#ihk_4').text(data.predict_12[3]);
                $('#date_5').text(data.label_pred[4]);
                $('#ihk_5').text(data.predict_12[4]);
                $('#date_6').text(data.label_pred[5]);
                $('#ihk_6').text(data.predict_12[5]);
                $('#date_7').text(data.label_pred[6]);
                $('#ihk_7').text(data.predict_12[6]);
                $('#date_8').text(data.label_pred[7]);
                $('#ihk_8').text(data.predict_12[7]);
                $('#date_9').text(data.label_pred[8]);
                $('#ihk_9').text(data.predict_12[8]);
                $('#date_10').text(data.label_pred[9]);
                $('#ihk_10').text(data.predict_12[9]);
                $('#date_11').text(data.label_pred[10]);
                $('#ihk_11').text(data.predict_12[10]);
                $('#date_12').text(data.label_pred[11]);
                $('#ihk_12').text(data.predict_12[11]);




            },
            error:function(m){
                $('#loading_modeling').hide();
                console.log('error fungsi BosKu');
            }
            
        });
        
    })
    function view_original(){
        $('#loading_pre_processing').show();
        $.ajax({
            type: 'POST',
            url: '/simulatorforecasting/plot_original_data',
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}',
                path : $('#text_csv').text()
            },
            success:function(data){     
                $('#loading_plot_original').hide();  
                var config = {
                    type: 'line',
                    data: {
                        labels: data.label,
                        datasets: [{
                            label: data.region_name+' Region',
                            backgroundColor: window.chartColors.blue,
                            borderColor: window.chartColors.blue,
                            data: data.data,
                            fill: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Original IHK Data'
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                        },
                        hover: {
                            mode: 'nearest',
                            intersect: true
                        },
                        scales: {
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Time'
                                }
                            }],
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'IHK Value'
                                }
                            }]
                        }
                    }
                };               
                var ctx = document.getElementById('canvas_original').getContext('2d');
                window.myLine = new Chart(ctx, config);
                $('#desc_original').html(data.desc);
            },
            error:function(m){              
                console.log('error fungsi BosKu');
            }
            
        });
    }

    function view_trend_seasonal(){
         
        $.ajax({
            type: 'POST',
            url: '/simulatorforecasting/plot_decomposition_data',
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}',
                path : $('#text_csv').text()
            },
            success:function(data){
                
                $('#loading_plot_decomposition').hide();
                var config_trend = {
                    type: 'line',
                    data: {
                        labels: data.label_trend,
                        datasets: [{
                            label: 'Trend',
                            backgroundColor: window.chartColors.blue,
                            borderColor: window.chartColors.blue,
                            data: data.data_trend,
                            fill: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Trend Data'
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                        },
                        hover: {
                            mode: 'nearest',
                            intersect: true
                        },
                        scales: {
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: ''
                                }
                            }],
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: ''
                                }
                            }]
                        }
                    }
                };    
                var config_seasonal = {
                    type: 'line',
                    data: {
                        labels: data.label_seasonal,
                        datasets: [{
                            label: 'Seasonal',
                            backgroundColor: window.chartColors.blue,
                            borderColor: window.chartColors.blue,
                            data: data.data_seasonal,
                            fill: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Seasonal Data'
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                        },
                        hover: {
                            mode: 'nearest',
                            intersect: true
                        },
                        scales: {
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: ''
                                }
                            }],
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: ''
                                }
                            }]
                        }
                    }
                };               
                var ctx_trend = document.getElementById('canvas_trend').getContext('2d');
                var ctx_seasonal = document.getElementById('canvas_seasonal').getContext('2d');
                window.myLine = new Chart(ctx_trend, config_trend);
                window.myLine = new Chart(ctx_seasonal, config_seasonal);
                $('#desc_trend').html(data.desc_trend);
                $('#desc_seasonal').html(data.desc_seasonal);
            },
            error:function(m){
                
                console.log('error fungsi BosKu')
            }
            
        });
    }
    function view_stationarity(){
         
        $.ajax({
            type: 'POST',
            url: '/simulatorforecasting/plot_stationary_data',
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}',
                path : $('#text_csv').text()
            },
            success:function(data){
                $('#loading_plot_stationarity').hide();
                var config = {
                    type: 'line',
                    data: {
                        labels: data.label,
                        datasets: [{
                            label: 'Rolling Mean',
                            backgroundColor: window.chartColors.red,
                            borderColor: window.chartColors.red,
                            data: data.data_rolmean,
                            fill: false,
                        },{                            
                            label: 'Original Time Series',
                            backgroundColor: window.chartColors.blue,
                            borderColor: window.chartColors.blue,
                            data: data.data_original,
                            fill: false,

                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Time Series Stationary to Rolling Mean'
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                        },
                        hover: {
                            mode: 'nearest',
                            intersect: true
                        },
                        scales: {
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: ''
                                }
                            }],
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: ''
                                }
                            }]
                        }
                    }
                };               
                var ctx = document.getElementById('canvas_stationary').getContext('2d');
                window.myLine = new Chart(ctx, config);
                $('#input_I').val(data.d);
                $('#desc_stasioner').html(data.desc);                      
            },
            error:function(m){
                
                console.log('error fungsi BosKu')
            }
            
        });
    }
    function view_acf_pacf(){
         
        $.ajax({
            type: 'POST',
            url: '/simulatorforecasting/plot_acf_pacf_data',
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}',
                path : $('#text_csv').text()
            },
            success:function(data){     
                $('#loading_plot_acf_pacf').hide();
                var config_acf = {
                    type: 'line',
                    data: {
                        labels: data.label,
                        datasets: [{
                            label: 'ACF',
                            backgroundColor: window.chartColors.blue,
                            borderColor: window.chartColors.blue,
                            data: data.data_acf,
                            fill: false,
                        },{                            
                            label: 'Batas Atas ACF',
                            backgroundColor: window.chartColors.grey,
                            borderColor: window.chartColors.grey,
                            data: data.yplusACF,
                            fill: false,

                        },{                            
                            label: 'Batas Bawah ACF',
                            backgroundColor: window.chartColors.grey,
                            borderColor: window.chartColors.grey,
                            data: data.yminACF,
                            fill: false,

                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Autocorrelation'
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                        },
                        hover: {
                            mode: 'nearest',
                            intersect: true
                        },
                        scales: {
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Lag'
                                }
                            }],
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: ''
                                }
                            }]
                        }
                    }
                };
                var config_pacf = {
                    type: 'line',
                    data: {
                        labels: data.label,
                        datasets: [{
                            label: 'PACF',
                            backgroundColor: window.chartColors.blue,
                            borderColor: window.chartColors.blue,
                            data: data.data_pacf,
                            fill: false,
                        },{                            
                            label: 'Batas Atas PACF',
                            backgroundColor: window.chartColors.grey,
                            borderColor: window.chartColors.grey,
                            data: data.yplusPACF,
                            fill: false,

                        },{                            
                            label: 'Batas Bawah PACF',
                            backgroundColor: window.chartColors.grey,
                            borderColor: window.chartColors.grey,
                            data: data.yminPACF,
                            fill: false,

                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Partial Autocorrelation'
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                        },
                        hover: {
                            mode: 'nearest',
                            intersect: true
                        },
                        scales: {
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: 'Lag'
                                }
                            }],
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: ''
                                }
                            }]
                        }
                    }
                };               
                var ctx_acf = document.getElementById('canvas_acf').getContext('2d');
                var ctx_pacf = document.getElementById('canvas_pacf').getContext('2d');
                window.myLine = new Chart(ctx_acf, config_acf);
                window.myLine = new Chart(ctx_pacf, config_pacf);
                 $('#desc_acf_pacf').html(data.desc);
                 $('#loading_pre_processing').hide();    
                // $('#img_acf_pacf_data').attr("src", "/static/images/"+m+" ACF_PACF.png"); 
                // $('#img_acf_pacf_data').show();           
            },
            error:function(m){
                $('#loading_pre_processing').hide();
                console.log('error fungsi BosKu')
            }
            
        });
    }
});