$(function() {
    var tabs = $('.tab-head h2');
    var contents = $('.tab-content div');
    alert(tabs.length);

    for (var i = 0, len = tabs.length; i < len; i++) {
        alert(i);
        tabs[i].onmouseover = showTab;
    }

    function showTab() {
        for (var i = 0, len = tabs.length; i < len; i++) {
            if (tabs[i] === this) {
                tabs[i].className = 'selected';
                contents[i].className = 'show';
            } else {
                tabs[i].className = '';
                contents[i].className = '';
            }
        }
    }
});



