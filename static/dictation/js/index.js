
var dChoiceSelected = new Object();
var aLesson=[];
$(function(){
    $.get('/dictation/initQry/', function(dic){
        dChoiceSelected = dic.choiceSelected;
        aPress = dic.press;
        aBook = dic.book;
        aUnit = dic.unit;
        aLesson = dic.lesson;
        aTestTime = dic.testtime;
        aTest = dic.test;
        aWordScope = dic.wordscope;
        // alert(aLesson)
        hPress = $('#press');
        hBook = $('#book');
        hUnit = $('#unit');
        hLesson = $('#lesson');
        hTestTime=$('#testtime')
        hTest = $('#test');
        hWordScope=$('#wordscope')
        fillSelect(aPress,hPress,dChoiceSelected['press']);
        fillSelect(aBook,hBook,dChoiceSelected['book']);
        fillSelect(aUnit,hUnit,dChoiceSelected['unit']);

        // fillRadio(aLesson,hLesson,dChoiceSelected['lesson']);
        fillSelect(aLesson,hLesson,dChoiceSelected['lesson']);
        fillSelect(aTestTime,hTestTime,dChoiceSelected['testtime']);
        // fillSelect(aTest,hTest,dChoiceSelected['test']);
        fillSelect(aTest,hTest,0);
        fillSelect(aWordScope,hWordScope,dChoiceSelected['wordscope']);
    });

    $('#press').change(function(){
        // alert('unit changed');
        hBook = $('#book');
        hBook.empty();
        pressCode = $(this).val();
        qry = 'qryBook/?press='+pressCode;
        // alert(qry);
        $.get(qry,function(dic){
            aBook = dic.book;
            // alert(aLesson);
            // fillRadio(aLesson,hLesson,'None');
            fillSelect(aBook,hBook,'None');
        })
    });

    $('#book').change(function(){
        // alert('unit changed');
        hUnit = $('#unit');
        hUnit.empty();
        bookCode = $(this).val();
        // aLesson.push(unitCode);
        // alert(aLesson);
        qry = 'qryUnit/?book='+bookCode;
        // alert(qry);
        $.get(qry,function(dic){
            aUnit = dic.unit;
            // alert(aLesson);
            // fillRadio(aLesson,hLesson,'None');
            fillSelect(aUnit,hUnit,'None');
        })
    });

    $('#unit').change(function(){
        // alert('unit changed');
        hLesson = $('#lesson');
        hLesson.empty();
        unitCode = $(this).val();
        // alert(unitCode);
        // aLesson.push(unitCode);
        // alert(aLesson);
        qry = 'qryLesson/?unit='+unitCode;
        // alert(qry);
        $.get(qry,function(dic){
            aLesson = dic.lesson;
            // alert(aLesson);
            // fillRadio(aLesson,hLesson,'None');
            fillSelect(aLesson,hLesson,'None');
        })
    });

    $('#lesson').change(function(){
        // alert('unit changed');
        hTest = $('#test');
        hTest.empty();
        lessonId = $(this).val();
        // alert(lessonId);
        // aLesson.push(unitCode);
        // alert(aLesson);
        qry = 'qryTest/?lesson='+lessonId;
        // alert(qry);
        $.get(qry,function(dic){
            aTest = dic.test;
            // alert(aLesson);
            fillSelect(aTest,hTest,'None');
        })
    });

    $('#wrongword').click(function(){
        $(this).removeClass('btn-default');
        $(this).addClass('btn-primary');
        $('#newword').removeClass('btn-primary');
        $('#newword').addClass('btn-default');
        aWrongWd = $('.wrongword');
        aWrongWd.addClass('show');
        aWrongWd.removeClass('hide');

        $('.dictype[value=wrongword]').attr('checked','checked');
        $('.dictype[value=newword]').removeAttr('checked');
    });

    $('#newword').click(function(){
        $(this).removeClass('btn-default');
        $(this).addClass('btn-primary');
        $('#wrongword').removeClass('btn-primary');
        $('#wrongword').addClass('btn-default');
        aWrongWd = $('.wrongword');
        aWrongWd.addClass('hide');
        aWrongWd.removeClass('show');
        $('.dictype[value=wrongword]').removeAttr('checked');
        $('.dictype[value=newword]').attr('checked','checked');
    });
});

//fill select
function fillSelect(aOptions,hSele,selectedKey){
    hSele.empty();
    hSele.append('<option value="0"></option>');
    $.each(aOptions, function(i,dOpt){
        //fill head
        // alert(i);
        // alert(dOpt);
        code = dOpt[0];
        // alert(code);
        dispName = dOpt[1];
        // alert(dispName);

        if(code == selectedKey) {
            hSele.append('<option selected="selected" value='+code+'>'+dispName+'</option>');
        }
        else{
            hSele.append('<option value='+code+'>'+dispName+'</option>');
        }

    });
}

//fill ul
function fillUl(aNames,hUl){
    hUl.empty();
    // hUl.append('<label>课文</label>');
    $.each(aNames, function(i,dName){
        //fill head
        code = dName[0];
        dispName = dName[1];
        hUl.append('<li value='+code+'>'+dispName+'</li>');
    });
}

//fill radio
function fillRadio(aNames,hRadio,checkKey){
    hRadio.empty();
    // hRadio.append('<label>课文</label><br>');
    $.each(aNames, function(i,dName){
        //fill head
        code = dName[0];
        dispName = dName[1];
        if(code == checkKey) {
            hRadio.append('<label class="lsradio">'+ dispName +'<input type="radio" name="lesson" value=' + code + ' checked></label><br>');
        }
        else{
            hRadio.append('<label class="lsradio">' + dispName + '<input type="radio" name="lesson" value=' + code + '></label><br>');
        }
    });
}

