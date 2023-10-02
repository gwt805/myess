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


// 必须登录
$(window).load(function () {
    const isLogin = window.localStorage.getItem("isLogin");
    let zhuname = window.localStorage.getItem("zhuname");
    if (isLogin != 'true') {
        window.location.href = "/login";
    } else {
        $("#name").html(zhuname);
    }
});

// 禁用缩放
document.addEventListener('keydown', (event) => {
    if ((event.ctrlKey === true || event.metaKey === true) && (event.which === 61 || event.which === 107 || event.which === 173 || event.which === 109 || event.which === 187 || event.which === 189)) {
      event.preventDefault();
    }
  }, false);
  
  document.addEventListener('mousewheel', (e) => {
    if ((e.wheelDelta && e.ctrlKey) || e.detail) {
      e.preventDefault();
    }
  }, {
    capture: false,
    passive: false
  });