var settings = {
    position: 'top',
    animationTime: 500,
    easing: "ease-in-out",
    offset: 4,
    hidePlaceholderOnFocus: false
};

function clear_all() {
    let el = $('.label_better');
    el.each(function(index, value){
        let btn = $(this);
        btn.val('');
        btn.parent().find(".lb_label")
                    .bind("transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd"
                            ,function(){ $(this).remove(); })
                    .removeAnimate(settings, btn);
        btn.parent().find(".lb_label").removeClass("active");
    });
}

function save() {
    
}

$(document).ready(function(){
    $(".innerbox").attr("disabled","disabled");
    $(".innerbox").removeClass("label-better");
    $(".innerbox").addClass("demon");
});

$("#info").change(function() { //为checkbox添加状态改变事件
    if($(this).is(':checked')){//判断checkbox是否选中
    //选中状态
        $(".innerbox").removeAttr("disabled");
        $('.switch-box-label').text('Save');
    }else{
    //未选中状态
        $(".innerbox").attr("disabled","disabled");
        $('.switch-box-label').text('Edit');
        save();
        clear_all();
    }
});
