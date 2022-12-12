

// <!-- <script>
//     // 开始结束时间 组件
//     // $(function () {
//     //     var locale = {
//     //         "format": 'YYYY-MM-DD',
//     //         "separator": " - ",
//     //         "applyLabel": "确定",
//     //         "cancelLabel": "取消",
//     //         "fromLabel": "起始时间",
//     //         "toLabel": "结束时间'",
//     //         "customRangeLabel": "自定义",
//     //         "weekLabel": "W",
//     //         "daysOfWeek": ["日", "一", "二", "三", "四", "五", "六"],
//     //         "monthNames": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
//     //         "firstDay": 1
//     //     };
//     //     $('#demo').daterangepicker({
//     //         'locale': locale,
//     //         // ranges: {
//     //         //     '今日': [moment(), moment()],
//     //         //     '昨日': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
//     //         //     '最近7日': [moment().subtract(6, 'days'), moment()],
//     //         //     '最近30日': [moment().subtract(29, 'days'), moment()],
//     //         //     '本月': [moment().startOf('month'), moment().endOf('month')],
//     //         //     '上月': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month')
//     //         //         .endOf('month')
//     //         //     ]
//     //         // },
//     //         "alwaysShowCalendars": true,
//     //         // "startDate": new Date(),
//     //         // "endDate": new Date(),
//     //         "opens": "right",
//     //     }, function (start, end, label) {
//     //         // startDate =  start.format('YYYY-MM-DD');
//     //         // endDate = end.format('YYYY-MM-DD');
//     //         console.log('New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')');

//     //         // $.ajax('/index/', {
//     //         //     method: "GET",
//     //         //     contentType: "application/json; charset=utf-8",
//     //         //     dataType: "json",
//     //         //     data: {
//     //         //         startDate: start.format('YYYY-MM-DD'),
//     //         //         endDate: end.format('YYYY-MM-DD')
//     //         //     }
//     //         // }).done(function (res) {
//     //         //     if (res && res.states == 'successful') {
//     //         //         // console.log(res.dat)
//     //         //         // $('#table').bootstrapTable('destroy');

//     //         //         // tableshow(res.data);
//     //         //         // $("#table").bootstrapTable('selectPage', 1);
//     //         //         console.log("加载成功!");
//     //         //     } else {
//     //         //         console.log(res);
//     //         //     }
//     //         // });
//     //     });
//     // })


//     var operateFormatter = function (value, row, index) {//赋予的参数
//         return [
//             '<button class="btn btn-info btn-sm rightSize detailBtn" type="button"><span class="glyphicon glyphicon-plus" aria-hidden="true">修改</button>',
//             '<button class="btn btn-danger btn-sm rightSize packageBtn" type="button"><span class="glyphicon glyphicon-remove" aria-hidden="true">删除</button>'
//         ].join('');
//     }

//     $('#table').bootstrapTable({
//         data: all_task_job,             //请求后台的URL（*）
//         toolbar: '#toolbar',                //工具按钮用哪个容器
//         height: 850,                          // 固定表头
//         uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
//         pagination: true,                   //是否显示分页（*）
//         sortOrder: "asc",                   //排序方式
//         filterControl: true,                 // 过滤
//         showColumnsToggleAll:true,//设置true 为在列选项/下拉列表中显示“全部切换”复选框。
//         showColumnsSearch:true, //设置true 为显示对列过滤器的搜索。
//         search: true,   //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
//         showButtonText:true,  //所有按钮都将在其上显示文本
//         showSearchClearButton:true, //清除搜索输入
//         // clickToSelect: true,  //是否启用点击选中行
//         sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
//         pageNumber: 1,                       //初始化加载第一页，默认第一页
//         pageSize: 15,                       //每页的记录行数（*）
//         pageList: [15, 50, 100, 200],        //可供选择的每页的行数（*）
//         filterControl: true,
//         strictSearch: true,
//         columns: [
//             {
//                 field: 'id',
//                 title: 'ID',
//                 align: 'center',
//                 sortable: true,
//             }, {
//                 field: 'uname',
//                 title: '用户名',
//                 align: 'center',
//                 filterControl: 'select',
//             }, {
//                 field: 'pname',
//                 title: '项目名字',
//                 align: 'center',
//                 filterControl: 'select'
//             }, {
//                 field: 'waibao',
//                 title: '标注方',
//                 align: 'center',
//                 filterControl: 'select'
//             }, {
//                 field: 'task_id',
//                 title: '任务ID',
//                 align: 'center',
//                 filterControl: 'input'
//             }, {
//                 field: 'dtime',
//                 title: '日期',
//                 align: 'center',
//                 sortable: true,
//                 filterControl: 'select'
//             }, {
//                 field: 'kinds',
//                 title: '任务类型',
//                 align: 'center',
//                 filterControl: 'select'
//             }, {
//                 field: 'pnums',
//                 title: '图片/视频数量',
//                 align: 'center'
//             }, {
//                 field: 'knums',
//                 title: '框数/属性/时长',
//                 align: 'center'
//             }, {
//                 field: 'ptimes',
//                 title: '工时',
//                 align: 'center'
//             }, {
//                 field: 'operate',
//                 title: '操作',
//                 align: 'center',
//                 valign: 'middle',
//                 formatter: operateFormatter //自定义方法，添加操作按钮
//             }]
//     });



// </script> -->