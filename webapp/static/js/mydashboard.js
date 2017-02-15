/**
 * Created by yueyt on 2017/2/15.
 */
$(document).ready(function () {
    function myHcharts() {
        $('#container').highcharts({                  //图表展示容器，与 div 的 id 保持一致
            chart: {
                type: 'bar'                           //指定图表的类型，默认是折线图（line）
            },
            title: {
                text: '我的第一个图表'                 //指定图表标题
            },
            xAxis: {
                categories: ['苹果', '香蕉', '橙子']   //指定x轴分组
            },
            yAxis: {
                title: {
                    text: 'something'                 //指定y轴的标题
                }
            },
            series: [{                                 //指定数据列
                name: '小明',                          //数据列名
                data: [1, 0, 4]                        //数据
            }, {
                name: '小红',
                data: [5, 7, 3]
            }]
        });
    }

    function myHcharts2() {
        var charts = Highcharts.chart('container', {
            title: {
                text: '机器占比'
            },
            xAxis: {
                categories: ['P1', 'P2', 'P3']
            },
            labels: {
                items: [{
                    html: '环境占比',
                    style: {
                        left: '100px',
                        top: '18px',
                        color: (Highcharts.theme && Highcharts.theme.textColor) || 'black'
                    }
                }]
            },
            credits: {text: 'this is test', enabled: false},
            series: [{
                type: 'column',
                name: 'P1',
                data: [
                    {name: 'DEV', y: 3, drilldown: 'DEV'},
                    {name: 'SIT', y: 5, drilldown: 'SIT'},
                    {name: 'UAT', y: 8, drilldown: 'UAT'}
                ]
            }, {
                type: 'column',
                name: 'P2',
                data: [
                    {name: 'DEV', y: 1, drilldown: 'DEV'},
                    {name: 'SIT', y: 2, drilldown: 'SIT'},
                    {name: 'UAT', y: 3, drilldown: 'UAT'}
                ]
            }, {
                type: 'column',
                name: 'P3',
                data: [
                    {name: 'DEV', y: 11, drilldown: 'DEV'},
                    {name: 'SIT', y: 2, drilldown: 'SIT'},
                    {name: 'UAT', y: 40, drilldown: 'UAT'}
                ]
            }, {
                type: 'pie',
                name: 'Total consumption',
                data: [{
                    name: 'Jane',
                    y: 13,
                    color: Highcharts.getOptions().colors[0] // Jane's color
                }, {
                    name: 'John',
                    y: 23,
                    color: Highcharts.getOptions().colors[1] // John's color
                }, {
                    name: 'Joe',
                    y: 19,
                    color: Highcharts.getOptions().colors[2] // Joe's color
                }],
                center: [100, 80],
                size: 100,
                showInLegend: false,
                dataLabels: {
                    enabled: false
                }
            }],
            drilldown: {
                series: [{
                    name: 'DEV',
                    id: 'DEV',
                    data: {y: 19}

                }, {
                    name: 'DEV',
                    id: 'DEV',
                    data: {y: 19}

                }]
            }
        });
        $.get('/api/servers', function (data) {
                console.log('this is test')
            }
        )
    }

    function myHcharts3() {
        // Create the chart
        Highcharts.chart('container', {
            chart: {
                type: 'column'
            },
            title: {
                text: 'Browser market shares. January, 2015 to May, 2015'
            },
            subtitle: {
                text: 'Click the columns to view versions. Source: <a href="http://netmarketshare.com">netmarketshare.com</a>.'
            },
            xAxis: {
                type: 'category'
            },
            yAxis: {
                title: {
                    text: 'Total percent market share'
                }
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                series: {
                    borderWidth: 0,
                    dataLabels: {
                        enabled: true,
                        format: '{point.y:.1f}%'
                    }
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
            },
            series: [{
                name: 'Brands',
                colorByPoint: true,
                data: [{
                    name: 'Microsoft Internet Explorer',
                    y: 56.33,
                    drilldown: 'Microsoft Internet Explorer'
                }, {
                    name: 'Chrome',
                    y: 24.03,
                    drilldown: 'Chrome'
                }, {
                    name: 'Firefox',
                    y: 10.38,
                    drilldown: 'Firefox'
                }, {
                    name: 'Safari',
                    y: 4.77,
                    drilldown: 'Safari'
                }, {
                    name: 'Opera',
                    y: 0.91,
                    drilldown: 'Opera'
                }, {
                    name: 'Proprietary or Undetectable',
                    y: 0.2,
                    drilldown: null
                }]
            }],
            drilldown: {
                series: [{
                    name: 'Microsoft Internet Explorer',
                    id: 'Microsoft Internet Explorer',
                    data: [
                        [
                            'v11.0',
                            24.13
                        ],
                        [
                            'v8.0',
                            17.2
                        ],
                        [
                            'v9.0',
                            8.11
                        ],
                        [
                            'v10.0',
                            5.33
                        ],
                        [
                            'v6.0',
                            1.06
                        ],
                        [
                            'v7.0',
                            0.5
                        ]
                    ]
                }, {
                    name: 'Chrome',
                    id: 'Chrome',
                    data: [
                        [
                            'v40.0',
                            5
                        ],
                        [
                            'v41.0',
                            4.32
                        ],
                        [
                            'v42.0',
                            3.68
                        ],
                        [
                            'v39.0',
                            2.96
                        ],
                        [
                            'v36.0',
                            2.53
                        ],
                        [
                            'v43.0',
                            1.45
                        ],
                        [
                            'v31.0',
                            1.24
                        ],
                        [
                            'v35.0',
                            0.85
                        ],
                        [
                            'v38.0',
                            0.6
                        ],
                        [
                            'v32.0',
                            0.55
                        ],
                        [
                            'v37.0',
                            0.38
                        ],
                        [
                            'v33.0',
                            0.19
                        ],
                        [
                            'v34.0',
                            0.14
                        ],
                        [
                            'v30.0',
                            0.14
                        ]
                    ]
                }, {
                    name: 'Firefox',
                    id: 'Firefox',
                    data: [
                        [
                            'v35',
                            2.76
                        ],
                        [
                            'v36',
                            2.32
                        ],
                        [
                            'v37',
                            2.31
                        ],
                        [
                            'v34',
                            1.27
                        ],
                        [
                            'v38',
                            1.02
                        ],
                        [
                            'v31',
                            0.33
                        ],
                        [
                            'v33',
                            0.22
                        ],
                        [
                            'v32',
                            0.15
                        ]
                    ]
                }, {
                    name: 'Safari',
                    id: 'Safari',
                    data: [
                        [
                            'v8.0',
                            2.56
                        ],
                        [
                            'v7.1',
                            0.77
                        ],
                        [
                            'v5.1',
                            0.42
                        ],
                        [
                            'v5.0',
                            0.3
                        ],
                        [
                            'v6.1',
                            0.29
                        ],
                        [
                            'v7.0',
                            0.26
                        ],
                        [
                            'v6.2',
                            0.17
                        ]
                    ]
                }, {
                    name: 'Opera',
                    id: 'Opera',
                    data: [
                        [
                            'v12.x',
                            0.34
                        ],
                        [
                            'v28',
                            0.24
                        ],
                        [
                            'v27',
                            0.17
                        ],
                        [
                            'v29',
                            0.16
                        ]
                    ]
                }]
            }
        });


    }

    myHcharts2()
});