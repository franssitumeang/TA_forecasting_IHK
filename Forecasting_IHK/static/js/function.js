

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
    })


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
                var config_model_arimax = {
                    type: 'line',
                    data: {
                        labels: data.label,
                        datasets: [{
                            label: 'Actual',
                            backgroundColor: window.chartColors.blue,
                            borderColor: window.chartColors.blue,
                            data: data.data_test,
                            fill: false,
                        },{
                            label: 'Predict',
                            backgroundColor: window.chartColors.red,
                            borderColor: window.chartColors.red,
                            data: data.data_predict_arima,
                            fill: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Evaluate Single Model ARIMAX'
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
                var config_model_hybrid = {
                    type: 'line',
                    data: {
                        labels: data.label,
                        datasets: [{
                            label: 'Actual',
                            backgroundColor: window.chartColors.blue,
                            borderColor: window.chartColors.blue,
                            data: data.data_test,
                            fill: false,
                        },{
                            label: 'Predict',
                            backgroundColor: window.chartColors.red,
                            borderColor: window.chartColors.red,
                            data: data.data_predict_hybrid,
                            fill: false,
                        }]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Evaluate Hybrid Model ARIMAX - SVR'
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
                var ctx_model_arimax = document.getElementById('canvas_predict_arimax').getContext('2d');
                var ctx_model_hybrid = document.getElementById('canvas_predict_hybrid').getContext('2d');
                window.myLine = new Chart(ctx_model_arimax, config_model_arimax);
                window.myLine = new Chart(ctx_model_hybrid, config_model_hybrid);
                $('#desc_mape_arima').html(data.desc_mape_arima);
                $('#desc_mape_hybrid').html(data.desc_mape_hybrid);
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
                dmin = data.ymin
                dplus = data.yplus
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
                            label: 'y('+String(dmin[0]).substring(0,5)+')',
                            backgroundColor: window.chartColors.grey,
                            borderColor: window.chartColors.grey,
                            data: data.ymin,
                            fill: false,

                        },{                            
                            label: 'y('+String(dplus[0]).substring(0,4)+')',
                            backgroundColor: window.chartColors.grey,
                            borderColor: window.chartColors.grey,
                            data: data.yplus,
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
                            label: 'y('+String(dmin[0]).substring(0,5)+')',
                            backgroundColor: window.chartColors.grey,
                            borderColor: window.chartColors.grey,
                            data: data.ymin,
                            fill: false,

                        },{                            
                            label: 'y('+String(dplus[0]).substring(0,4)+')',
                            backgroundColor: window.chartColors.grey,
                            borderColor: window.chartColors.grey,
                            data: data.yplus,
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