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
    let task_html = `<tr> <th scope="row" class="checkboxContainer"> <input type="checkbox"/> </th> <td>Bandana Box Logo Tee Black</td><td>Small</td><td>Profile 1</td><td>US Residental</td><td class="app-success-color">Successful Checkout</td><td> <a name="" id="" class="btn btn-sm btn-light mr-0 mt-2 mr-md-1 mt-lg-0" href="#" role="button" ><i class="fas fa-play fa-md btn-tasks-icon"></i ></a> <a name="" id="" class="btn btn-sm btn-light mr-0 mt-2 mr-md-1 mt-lg-0" href="#" role="button" ><i class="fas fa-edit fa-md btn-tasks-icon"></i ></a> <a name="duplicate-task" id="" class="btn btn-sm btn-light mr-0 mt-2 mr-md-1 mt-lg-0" href="#" role="button" ><i class="fas fa-copy fa-md btn-tasks-icon"></i ></a> <a name="delete-task" id="" class="btn btn-sm btn-light mr-0 mt-2 mr-md-1 mt-lg-0" href="#" role="button" ><i class="fas fa-trash fa-md btn-tasks-icon"></i ></a> </td></tr>`;
    $("#task-body").append(task_html);

    // send notif
    Swal.fire({
      position: "center",
      icon: "success",
      title: "Tasks Added",
      showConfirmButton: false,
      timer: 1500,
    });
  });

  // Delete Task
  $("#task-body").on("click", 'a[name="delete-task"]', function () {
    Swal.fire({
      title: "Are you sure?",
      text: "You won't be able to revert this!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, delete it!",
    }).then((result) => {
      if (result.value) {
        Swal.fire("Deleted!", "Your task has been deleted.", "success");
        $(this).parent().parent().remove();
      }
    });
  });

  // Duplicate Task
  $("#task-body").on("click", 'a[name="duplicate-task"]', function () {
    Swal.fire({
      title: "Are you sure want to duplicate task?",
      text: "You won't be able to revert this!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, Duplicate it!",
    }).then((result) => {
      if (result.value) {
        Swal.fire("Duplicated!", "Your task has been duplicated.", "success");
        $("#task-body").append(
          `<tr> ${$(this).parent().parent().html()} </tr>`
        );
      }
    });
  });

  // Input Proxies Line Count

  $("#input-proxies").on("input", function () {
    line_count = $(this).val().split("\n").length;
    $("#total-proxies-loaded").text(`${line_count} Proxy`);
  });
});
