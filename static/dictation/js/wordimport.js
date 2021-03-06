var dChoiceSelected = new Object();
var aLesson=[];
$(function(){
    $.get('/dictation/initQry/', function(dic){
        dChoiceSelected = dic.choiceSelected;
        aPress = dic.press;
        aBook = dic.book;
        aUnit = dic.unit;
        aLesson = dic.lesson;

        // alert(aLesson)
        hPress = $('#press');
        hBook = $('#book');
        hUnit = $('#unit');
        hLesson = $('#lesson');
        hLsword = $('#lessonword');

        fillSelect(aPress,hPress,dChoiceSelected['press']);
        fillSelect(aBook,hBook,dChoiceSelected['book']);
        fillSelect(aUnit,hUnit,dChoiceSelected['unit']);

        // fillRadio(aLesson,hLesson,dChoiceSelected['lesson']);
        fillSelect(aLesson,hLesson,dChoiceSelected['lesson']);
        // alert(dChoiceSelected['lesson']);
        qryLessonWords(dChoiceSelected['lesson'], hLsword)
    });

    $('#press').change(function(){
        // alert('unit changed');
        hBook = $('#book');
        hBook.empty();
        pressCode = $(this).val();
        qry = '/dictation/qryBook/?press='+pressCode;
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
        qry = '/dictation/qryUnit/?book='+bookCode;
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
        aLesson.push(unitCode);
        // alert(aLesson);
        qry = '/dictation/qryLesson/?unit='+unitCode;
        // alert(qry);
        $.get(qry,function(dic){
            aLesson = dic.lesson;
            // alert(aLesson);
            // fillRadio(aLesson,hLesson,'None');
            fillSelect(aLesson,hLesson,'None');
        })
    });

    function qryLessonWords(lessonId, hlsword){
        // alert(qry);
        qry = '/dictation/qryLsWords/?lesson='+lessonId;
        // alert(qry);
        $.get(qry,function(dic){
            sWord = dic.words;
            // alert(sWord);
            // hlsword.innerHTML=sWord;
            hlsword.val(sWord);
        })
    }

    $('#lesson').change(function(){
        // alert('unit changed');
        hLsword = $('#lessonword');
        // hLsword.empty();

        lessonId = $(this).val();

        qryLessonWords(lessonId, hLsword)
    });

    $('#save').click(function(){
        // alert('unit changed');
        hLsword = $('#lessonword');
        sWord=hLsword.val();
        lessonId = $('#lesson').val();
        data = {'lesson':lessonId, 'words':sWord};
        $.post('/dictation/saveLsWords/',data);
    });

    $('#delete').click(function(){
        // alert('unit changed');
        hLsword = $('#lessonword');
        sWord=hLsword.val();
        lessonId = $('#lesson').val();
        data = {'lesson':lessonId, 'words':sWord};
        $.post('/dictation/delLsWords/',data);
        hLsword.val('');
    });

    //fill select
    function fillSelect(aOptions,hSele,selectedKey){
        hSele.empty();
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
});