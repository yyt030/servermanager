/**
 * Created by yueyt on 2017/2/15.
 */
$(document).ready(function () {
    function myHcharts() {
        var charts;

        $.get('/api/projectservers', function (response) {
            console.log(response);
            charts = Highcharts.chart('container', {
                title: {
                    text: '项目组使用机器'
                },
                xAxis: {
                    // ajax 后台获取
                    categories: response['categories']
                },
                credits: {enabled: false},
                // ajax 后台获取
                series: response['series'],
                // ajax 后台获取
                drilldown: {
                    series: response['drilldown_series']
                }
            });
        })
    }


    //页面滑动加载
    function main() {
        $(window).scroll(function () {
            var scrollTop = $(this).scrollTop();
            var scrollHeight = $(document).height();
            var windowHeight = $(this).height();

            if (scrollTop + windowHeight == scrollHeight) {
                //此处是滚动条到底部时候触发的事件，在这里写要加载的数据，或者是拉动滚动条的操作
                myHcharts()
            }
        });
    }

    main()
})
;