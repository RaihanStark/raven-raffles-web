$(document).ready(function () {
  $(".btn-shoes").on("click", function () {
    $(".shoes").each(function (index) {
      $(this).removeClass("selected");
    });
    $(this).parent().parent().toggleClass("selected");
  });
});
