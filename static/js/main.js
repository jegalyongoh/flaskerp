$(document).ready(function () {
    var table = $('#boardtab').DataTable({
             "lengthMenu" : [ [ 3, 5, 10, -1 ], [ 3, 5, 10, "All" ]],
             "ajax" : {
                 url : '/showboard',
                 type : 'POST',
             },
             columnDefs : [ {
                 targets : 1,
                 render : function(url,type,row){
                     return '<a href="./board/'+row[0]+'">'+url+'</a>';
                 }
             }]
     });
 });