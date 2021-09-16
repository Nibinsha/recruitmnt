

$(document).ready(function() {
    $('#filter_report').click(function(e){
        var rows = '';
        var frmDate = $('#start_date').val();
        var toDate = $('#end_date').val();
        $.ajax({
            type: 'POST',
            url: '/report_filter/',
            data: {
                'from': frmDate,
                'to': toDate,
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(response) {
                var data = JSON.parse(response)
                if(data.length == 0){
                    alert('No data!'); 
                }
                for (var i = 0; i < data.length; i++) {
                    var expired = false
                    if(data[i][5] != ''){
                        var now = moment();
                        var current_date = new Date(moment(now).format('YYYY-MM-DD HH:mm:ss'));
                        current_date = moment(current_date).format('YYYY-MM-DD HH:mm:ss');
                        var expiry_date = data[i][5]
                        if(expiry_date < current_date ){
                            expired = true
                        }else{
                            var no_of_year = moment.duration(moment(data[i][5]).diff(now)).asYears();
                            if(no_of_year < 1){
                                expired = true
                            }
                        }
                    }
                    if (expired == true){
                        rows += '<tr><td>' + data[i][0] + '</td><td>' + data[i][1] + '</td><td>' + data[i][2] + '</td><td>' + data[i][3] + '</td><td>' + data[i][4] + '</td><td style="background-color:#ffcccc">' + data[i][5] + '</td><td>' + data[i][6] + '</td><td>' + data[i][7] + '</td><td>' + data[i][8] + '</td></tr>';
                    }else{
                        rows += '<tr><td>' + data[i][0] + '</td><td>' + data[i][1] + '</td><td>' + data[i][2] + '</td><td>' + data[i][3] + '</td><td>' + data[i][4] + '</td><td>' + data[i][5] + '</td><td>' + data[i][6] + '</td><td>' + data[i][7] + '</td><td>' + data[i][8] + '</td></tr>';
                    }
                }
                document.getElementById('report').innerHTML = rows;
            }
        });
    });
});

 
