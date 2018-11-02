
var aWords=[];
$(function(){
    $.get('/dictation/qryTestWords/', function(dic){
		aWords = dic.words;
        // alert('get words')
		hWords = $('#words');
		fillWords(aWords,hWords);
    });

    $('.word').click(function(){
        // $(this).attr({'code':1});
        // alert($(this).attr('code'));
        $(this).toggleClass("se");
    });

    $('#saveTest').click(function(){
        // alert('save test');
        wdResult = {};
        $('.word').each(function(i,w){
            // alert(w.id);
            // alert(w.className);
            if(w.className.indexOf('se') >= 0) {
                wdResult[w.id] = 'True'
            } else {
                wdResult[w.id] = 'False'
            }
        });
        // alert(wdResult);
        $.post('/dictation/saveTest/',wdResult);

    })
});

function fillWords(aWords,hWords){
    hWords.empty();
    $.each(aWords, function(i,aWd){
        var code = aWd[0];
        // alert(aWd);
        var dispName = aWd[1];
        hWords.append('<label class="word un" id='+code+'>'+dispName+'</label>');

    });
    $('.word').click(function(){
        $(this).toggleClass("se");
    })
}


