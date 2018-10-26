        $(function(){
            $.get('ktqry', function(dic){
                dProcess = dic.result;
                var aNetAll = new Array()
                hHost = $('#host');
                hProcess = $('#process');
                hNet = $('#ne');
                hRes = $('#result');
                var addHead = 0
                $.each(dProcess, function(hId,aProcess){
                    {#alert(hId)#}
                    lenPro = aProcess[0].length;
                    numSts = lenPro - 5;
                    hHost.append('<option value='+hId+'>'+hId+'</option>');
                    $.each(aProcess, function(i,proc){
                        {#alert(proc)#}
                        procName = proc[2];
                        hProcess.append('<option value='+procName+'>'+procName+'</option>');
                        sNets = proc[3];
                        if (sNets != null)
                        {
                            aNets = sNets.split(',');
                            $.each(aNets, function(i, net){
                                if($.inArray(net,aNetAll)==-1)
                                {
                                    aNetAll.push(net);
                                    hNet.append('<option value='+net+'>'+net+'</option>');
                                }
                            })
                        };
                    });
                });
                fillRes(dProcess, hRes);
            });

            $('#btn1').click(function(){
                //("#select1  option:selected").text();
                host = $('#host  option:selected').val();
                process = $('#process  option:selected').val();
                ne = $('#ne  option:selected').val();
                cmd = $('#cmd  option:selected').val();
                var dProcData = new Object();
                //alert(host + ' '+process +' '+ ne+' ' +cmd)
                dProcData.host = host;
                dProcData.process=process;
                dProcData.ne=ne;
                dProcData.cmd=cmd;

                hRes = $('#result');
                hRes.empty();

                $.get('ktproc', dProcData, function(dic){
                    dProc = dic.result
                    fillRes(dProc, hRes);
                    //res.text(dic.result);
                    //res.resize()
                })
            });
        });

        //fill result table
        function fillRes(dProcess,hRes){
                var addHead = 0;
                hRes.empty();
                $.each(dProcess, function(hId,aProcess){
                    //fill head
                    procLen = aProcess[0].length - 5;
                    if(addHead == 0) {
                        addHead = 1;
                        var $trh = $('<tr></tr>');
                        trh = hRes.append('<tr></tr>');
                        $trh.append('<th>主机</th>');
                        $trh.append('<th>序号</th>');
                        //for(var i=0; i<procLen; i++) {
                        $trh.append('<th>状态</th>');
                        //}
                        $trh.append('<th>进程名</th>');
                        $trh.append('<th>进程</th>');
                        $trh.append('<th>网元</th>');
                        //$trh.appendTo(hRes)
                        hRes.append($trh);
                    };

                    var j = 0 ;
                    $.each(aProcess, function(i,proc){
                        var $trp = $('<tr></tr>');
                        {#trh = hRes.append('<tr></tr>');#}
                        $trp.append('<td>'+proc[0]+'</td>');
                        $trp.append('<td>'+proc[4]+'</td>');
                        var sts = proc[5]
                        for(var i=1; i<procLen; i++) {
                            j = i + 5;
                            sts = sts  +','+proc[j]

                        };
                        $trp.append('<td>' + sts + '</td>');
                        $trp.append('<td>'+proc[1]+'</td>');
                        $trp.append('<td>'+proc[2]+'</td>');
                        $trp.append('<td>'+proc[3]+'</td>');
                        //$trp.appendTo(hRes)
                        hRes.append($trp);
                    });
                });
        };

