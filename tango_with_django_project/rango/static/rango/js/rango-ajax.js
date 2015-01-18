$(document).ready(function() {
    $("#likes").click(function(event) {
        var category_id;
        category_id = $(this).attr("data-catid");
        $.get('/rango/like_category/', {category_id: category_id}, function(data) {
            $("#like_count").html(data);
            $("#likes").hide();
        });
    });

    $("#suggestion").keyup(function() {
        var query;
        query = $(this).val();
        $.get("/rango/suggest_category/", {suggestion: query}, function(data) {
            $("#cats").html(data);
        });
    });

    $(".search_add_page").click(function(event) {
        var category_id = $(this).attr("data-catid");
        var page_link = $(this).attr("data-url");
        var page_title = $(this).attr("data-title");
        $(this).hide();
        $.get('/rango/search_add_page/', {category_id:category_id, page_link:page_link, page_title:page_title}, function(data) {
            $("#pages").html(data);
        });

    });
});