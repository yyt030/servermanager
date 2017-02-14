/**
 * Created by yueyt on 2017/2/14.
 */

var del_server;
var edit_server;
$(document).ready(function () {
    var table = $('#serverlist').DataTable({
            responsive: true,
            fixedHeader: true,
            rowReorder: true,
            //服务器后台分页
            serverSide: true,
            processing: true,
            ajax: {
                url: '/api/servers',
                type: 'GET',
                error: function () {
                    alert("服务器未正常响应，请重试");
                }
            },
            "columns": [
                {"data": null, "class": "text-center"},
                {
                    "data": null,
                    "class": "text-center",
                    "defaultContent": '<input type="checkbox" name="checkList"></td>'
                },
                {"data": "subprojects", "title": "所属项目组", "defaultContent": "", "class": "text-center"},
                {"data": "envinfo", "title": "环境", "defaultContent": "", "class": "text-center"},
                {"data": "ip", "title": "ip", "defaultContent": "", "class": "text-center"},
                {"data": "oslevel", "title": "操作系统版本", "defaultContent": "", "class": "text-center"},
                {"data": "owner", "title": "机器所属人", "defaultContent": "", "class": "text-center"},
                {"data": null, "class": "text-center"},
            ],
            "columnDefs": [
                {
                    'targets': [0, 1, 2, 3, -1],//第1，2列禁止搜索排序
                    'searchable': false,
                    'orderable': false
                },
                {
                    //指定第最后一列 操作内容
                    targets: -1,
                    class: 'text-center',
                    render: function (data, type, row, meta) {
                        return '<a type="button" href="#" onclick="del_server(\'' + row.ip + '\')" >' +
                            '<span class="glyphicon glyphicon-trash"></a> ' +
                            '<a type="button" href="/servers/' + row.id + '" onclick1="edit_server(\'' + row.id + '\')" >' +
                            '<span class="glyphicon glyphicon-pencil"></a>';
                    }
                }
            ],
            "order": [[4, 'asc']],
            "language": {
                "sProcessing": "处理中...",
                "sLengthMenu": "显示 _MENU_ 项结果",
                "sZeroRecords": "没有匹配结果",
                "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
                "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
                "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
                "sInfoPostFix": "",
                "sSearch": "搜索:",
                "sUrl": "",
                "sEmptyTable": "表中数据为空",
                "sLoadingRecords": "载入中...",
                "sInfoThousands": ",",
                "oPaginate": {
                    "sFirst": "首页",
                    "sPrevious": "上页",
                    "sNext": "下页",
                    "sLast": "末页"
                }
                ,
                "oAria": {
                    "sSortAscending": ": 以升序排列此列",
                    "sSortDescending": ": 以降序排列此列"
                }
            }
            ,
            //改变每页显示的条数
            "lengthMenu": [10, 20, 30, 40, 50, 100],
        })
        ;
    //首列添加序号
    //不管是排序，还是分页，还是搜索最后都会重画，这里监听draw事件即可
    table.on('draw.dt', function () {
        table.column(0, {
            search: 'applied',
            order: 'applied'
        }).nodes().each(function (cell, i) {
            //i 从0开始，所以这里先加1
            i = i + 1;
            //服务器模式下获取分页信息，使用 DT 提供的 API 直接获取分页信息
            var page = table.page.info();
            //当前第几页，从0开始
            var pageno = page.page;
            //每页数据
            var length = page.length;
            //行号等于 页数*每页数据长度+行号
            cell.innerHTML = (i + pageno * length);
        });
    });
    //单server删除
    del_server = function (ip) {
        $.ajax({
            url: '/api/servers/' + ip,
            type: 'delete',
            success: function (data) {
                table.ajax.reload(null, false);
            }
        })
    };
    //单server编辑
    edit_server = function (ip) {
        $.ajax({
            url: '/api/servers/' + ip,
            type: 'get',
            success: function (data) {
                //table.ajax.reload(null, false);
            }
        })
    };

    //checkbox全选
    $("#checkAll").on("click", function () {
        if ($(this).prop("checked") === true) {
            $("input[name='checkList']").prop("checked", $(this).prop("checked"));
            $('#serverlist tbody tr').addClass('selected');
        } else {
            $("input[name='checkList']").prop("checked", false);
            $('#serverlist tbody tr').removeClass('selected');
        }
    });
    //标记选中行
    $('#serverlist tbody').on('click', 'tr input[name="checkList"]', function () {
        var $tr = $(this).parents('tr');
        $tr.toggleClass('selected');
        var $tmp = $('[name=checkList]:checkbox');
        $('#checkAll').prop('checked', $tmp.length == $tmp.filter(':checked').length);
    });
    //批量删除
    $('#delete_batch').click(function () {
        var $m_btn = $('#delete_batch');
        var $modal = $('#myModal');

        records = table.row('.selected');
        //批量删除
        if ($('input[name="checkList"]').length > 0) {  // at-least one checkbox checked
            var ips = [];
            $('.selected').each(function () {
                ips.push(table.row($(this)).data()['ip'])
            });
            if (ips.length > 0) {
                $.ajax({
                    type: "DELETE",
                    url: "/api/servers",
                    data: {ips: ips.toString()},
                    success: function (result) {
                        table.ajax.reload(null, false);
                    }
                });
            } else {
                //alert('至少选择一条记录。。。');
                $modal.modal({backdrop: 'static'});
                return false
            }
        }
    });


});

