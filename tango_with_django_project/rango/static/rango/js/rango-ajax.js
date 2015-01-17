$(document).ready(function() {
    $("#likes").click(function(event) {
        var category_id;
        category_id = $(this).attr("data-catid");
        $.get('/rango/like_category/', {category_id: category_id}, function(data) {
            $("#like_count").html(data);
            $("#likes").hide();
        });
    });
});