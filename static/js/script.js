$(function(){
    $('.decimal').on('input', function(){
         this.value = this.value.replace(/^\.|[^\d\.]|\.(?=.*\.)|^0+(?=\d)/g, '');
     });
});