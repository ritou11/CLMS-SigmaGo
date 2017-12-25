var settings = {
    position: 'top',
    animationTime: 500,
    easing: "ease-in-out",
    offset: 4,
    hidePlaceholderOnFocus: false
};

function clear_all() {
    let el = $('.label_better');
    el.each(function(index, value) {
        let btn = $(this);
        btn.val('');
        btn.parent().find(".lb_label")
            .bind("transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd", function() { $(this).remove(); })
            .removeAnimate(settings, btn);
        btn.parent().find(".lb_label").removeClass("active");
    });
}

function save() {
    let el = $('.label_better');
    let data = {};
    el.each(function(index, value) {
        let field = this.getAttribute('field');
        if(field && this.value != ''){
            data[field] = this.value;
            this.setAttribute('placeholder', this.value);
        }
    });
    $.post('/userinfo-alter', data, function(response) {
        if (response.state == null || response.state < 0) {
            alert('Error response!');
            window.location.reload();
        }
    });
}

function addTag(tagid, tagname) {
    $('#tagsbox').tagsinput('add', tagname,
        { tagid: tagid, doGet: true });
}

$(document).ready(function() {
    $(".innerbox").attr("disabled", "disabled");
    $(".innerbox").removeClass("label-better");
    $(".innerbox").addClass("demon");
});

$("#info").change(function() { //为checkbox添加状态改变事件
    if ($(this).is(':checked')) { //判断checkbox是否选中
        //选中状态
        $(".innerbox").removeAttr("disabled");
        $('.switch-box-label').text('Save');
    } else {
        //未选中状态
        $(".innerbox").attr("disabled", "disabled");
        $('.switch-box-label').text('Edit');
        save();
        clear_all();
    }
});

$('.add-tags').click(function() {
    addTag($('#select-tags').val(), $('#select-tags')[0].selectedOptions[0].text);
});

$('#tagsbox').on('itemAdded', function(event) {
    let tagname = event.item;
    if (event.options && event.options.doGet) {
        let tagid = event.options.tagid;
        $.get('/tag-api', { 'action': 'add', 'tag': tagid }, function(response) {
            if (response.state == null || response.state < 0) {
                $('#tagsbox').tagsinput('remove', tagname);
            }
        });
    }
});

$('#tagsbox').on('itemRemoved', function(event) {
    $.get('/tag-api', { 'action': 'remove', 'tag': event.item }, function(response) {
        if (response.state == null || response.state < 0) {
            $('#tagsbox').tagsinput('add', event.item);
        }
    });
});
