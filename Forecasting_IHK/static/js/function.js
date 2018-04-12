

$(document).ready(function(){
    // LOADING 
    $('#loading_plot_original').hide();
    $('#loading_plot_decomposition').hide();
    $('#loading_plot_stationarity').hide();
    $('#loading_plot_acf_pacf').hide();
    $('#loading_modeling').hide();


    $('#btn_plot_original').click(function(){     
        $('#loading_plot_original').show();     
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
            },
            error:function(m){  
                $('#loading_plot_original').hide();              
                console.log('error fungsi BosKu');
            }
            
        });
    })    



    $('#upload_btn').change(function(){
        $('#text_csv').text($(this).val());
    })

    $('#btn_plot_seasonal_trend').click(function(){
    	$('#loading_plot_decomposition').show();  
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
            },
            error:function(m){
            	$('#loading_plot_decomposition').hide();
            	console.log('error fungsi BosKu')
            }
            
        });
        
    })

    $('#btn_plot_stationarity').click(function(){
    	$('#loading_plot_stationarity').show();  
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
            },
            error:function(m){
            	$('#loading_plot_stationarity').hide();
            	console.log('error fungsi BosKu')
            }
            
        });
        
    })

    $('#btn_plot_acf_pacf').click(function(){
    	$('#loading_plot_acf_pacf').show();  
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
                            label: 'y(0)',
                            backgroundColor: window.chartColors.grey,
                            borderColor: window.chartColors.grey,
                            data: data.y0,
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
                            label: 'y(0)',
                            backgroundColor: window.chartColors.grey,
                            borderColor: window.chartColors.grey,
                            data: data.y0,
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
                // $('#img_acf_pacf_data').attr("src", "/static/images/"+m+" ACF_PACF.png"); 
                // $('#img_acf_pacf_data').show();           
            },
            error:function(m){
            	$('#loading_plot_acf_pacf').hide();
            	console.log('error fungsi BosKu')
            }
            
        });
        
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
                            text: 'Evaluate Model ARIMAX'
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
                // var config_seasonal = {
                //     type: 'line',
                //     data: {
                //         labels: data.label_seasonal,
                //         datasets: [{
                //             label: 'Seasonal',
                //             backgroundColor: window.chartColors.blue,
                //             borderColor: window.chartColors.blue,
                //             data: data.data_seasonal,
                //             fill: false,
                //         }]
                //     },
                //     options: {
                //         responsive: true,
                //         title: {
                //             display: true,
                //             text: 'Seasonal Data'
                //         },
                //         tooltips: {
                //             mode: 'index',
                //             intersect: false,
                //         },
                //         hover: {
                //             mode: 'nearest',
                //             intersect: true
                //         },
                //         scales: {
                //             xAxes: [{
                //                 display: true,
                //                 scaleLabel: {
                //                     display: true,
                //                     labelString: ''
                //                 }
                //             }],
                //             yAxes: [{
                //                 display: true,
                //                 scaleLabel: {
                //                     display: true,
                //                     labelString: ''
                //                 }
                //             }]
                //         }
                //     }
                // };               
                var ctx_model_arimax = document.getElementById('canvas_predict_arimax').getContext('2d');
                // var ctx_seasonal = document.getElementById('canvas_seasonal').getContext('2d');
                window.myLine = new Chart(ctx_model_arimax, config_model_arimax);
                // window.myLine = new Chart(ctx_seasonal, config_seasonal);
                 $('#desc_mape_arima').html(data.desc_mape_arima);
            },
            error:function(m){
                $('#loading_modeling').hide();
                console.log('error fungsi BosKu');
            }
            
        });
        
    })
});