var text = "{{ a }}";
$.ajax({
    type : "POST",
    url : '/boardcontent',
    data : {'_id' : text},

    success : function(data){
        $('#content').html(data);
        console.log(data)
    }
})
function sub(){
    var inputname = $('#inputname').val();
    var inputbu = $('#inputbu').val();
    var inputrank = $('#inputrank').val();
    $('#name').text(inputname);
    $('#bu').text(inputbu);
    $('#rank').text(inputrank);
}