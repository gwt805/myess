// 屏蔽空格向下翻页
document.onkeydown = function (ev) {
    var e = ev || event;
    if (e.keyCode == 32) return false;
}

//禁用F12
window.onkeydown = window.onkeyup = window.onkeypress = function (event) {
    // 判断是否按下F12，F12键码为123
    if (event.keyCode == 123) {
        event.preventDefault(); // 阻止默认事件行为
        window.event.returnValue = false;
    }
}

// 禁用右击
document.oncontextmenu = function () {
    return false;
}

// 禁止选取内容
document.onselectstart = function () {
    return false;
}

// 禁止复制
document.oncopy = function () {
    return false;
}

// 禁止打开开发者工具
var threshold = 160; // 打开控制台的宽或高阈值
// 每秒检查一次
setInterval(function () {
    if (window.outerWidth - window.innerWidth > threshold ||
        window.outerHeight - window.innerHeight > threshold) {
        // 如果打开控制台，关闭页面
        if (navigator.userAgent.indexOf('MSIE') > 0) { // close IE
            if (navigator.userAgent.indexOf('MSIE 6.0') > 0) {
                window.location.href = "https://www.baidu.com/";
            } else {
                window.location.href = "https://www.baidu.com/";
            }
        } else { // close chrome;It is effective when it is only one.
            window.location.href = "https://www.baidu.com/";
        }
    }
}, 1000);