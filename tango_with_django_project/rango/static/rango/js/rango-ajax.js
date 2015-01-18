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

    // If the elements are added dynamically, selecting for the ID or class will not work
    $(document).on("click", ".page_links", function(){
        var category_id = $(this).attr("data-catid");
        var page_id = $(this).attr("data-page_id");
        $.get('/rango/goto/', {category_id:category_id, page_id:page_id}, function(data){
            $("#pages").html(data);
        });
    });
});
