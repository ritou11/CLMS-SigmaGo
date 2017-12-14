$(document).ready(function(){
    $('.sb-icon-search').click(function(){
        sbdiv = $('.sb-search');
        if(sbdiv.hasClass('sb-search-open')){
            keys = $('.sb-search-input').val();
            if(keys.length > 0){
                sbdiv[0].getElementsByTagName('form')[0].submit();
            }else{
                sbdiv.removeClass('sb-search-open');
            }
        }else{
            $('.sb-search').toggleClass('sb-search-open');
            $('.sb-search-input').focus();
        }
    });
    $('.sb-search').focusout(function(){
        window.setTimeout(function() { $('.sb-search').removeClass('sb-search-open'); }, 100);
    });
});