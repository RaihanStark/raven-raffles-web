$(document).ready(function () {
  $(".btn-shoes").on("click", function () {
    $(".shoes").each(function (index) {
      $(this).removeClass("selected");
    });
    $(this).parent().parent().toggleClass("selected");
  });

  //Add task
  $("#add-task").on("click", function () {
    // Close Modal
    $("#taskModal").modal("toggle");

    // Append Body
    let task_html = `<tr> <th scope="row"> <i class="far fa-square glow-checkbox" aria-hidden="true"></i> </th> <td>Bandana Box Logo Tee Black</td><td>Small</td><td>Profile 1</td><td>US Residental</td><td class="app-success-color">Successful Checkout</td><td> <a name="" id="" class="btn btn-sm btn-light mr-0 mt-2 mr-md-1 mt-lg-0" href="#" role="button"><i class="fas fa-play fa-md btn-tasks-icon" aria-hidden="true"></i></a> <a name="" id="" class="btn btn-sm btn-light mr-0 mt-2 mr-md-1 mt-lg-0" href="#" role="button"><i class="fas fa-edit fa-md btn-tasks-icon" aria-hidden="true"></i></a> <a name="" id="" class="btn btn-sm btn-light mr-0 mt-2 mr-md-1 mt-lg-0" href="#" role="button"><i class="fas fa-copy fa-md btn-tasks-icon" aria-hidden="true"></i></a> <a name="" id="" class="btn btn-sm btn-light mr-0 mt-2 mr-md-1 mt-lg-0" href="#" role="button"><i class="fas fa-trash fa-md btn-tasks-icon" aria-hidden="true"></i></a> </td></tr>`;
    $("#task-body").append(task_html);
  });

  $('a[name="delete-task"]').on("click", function () {
    $(this).parent().parent().remove();
  });
});
