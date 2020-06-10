$(document).ready(function () {
  const Toast = Swal.mixin({
    toast: true,
    position: "top",
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    onOpen: (toast) => {
      toast.addEventListener("mouseenter", Swal.stopTimer);
      toast.addEventListener("mouseleave", Swal.resumeTimer);
    },
  });

  // Input Proxies Line Count

  $("#input-proxies").on("input", function () {
    line_count = $(this).val().split("\n").length;
    $("#total-proxies-loaded").text(`${line_count} Proxy`);
  });

  // Entries max 10
  $("#entries").on("change", function () {
    if (parseInt($(this).val()) > 10) {
      $(this).val(10);
      Toast.fire({
        icon: "error",
        title: "Maximum 10 entries per task!",
      });
    }
  });

  // BUTTON SHOES
  $(".btn-shoes").on("click", function () {
    $(".shoes").each(function (index) {
      $(this).removeClass("selected");
    });
    $(this).parent().parent().toggleClass("selected");

    let id = $(this).parent().parent().attr("data-id");

    if ($("#raffle-id").val() != id) {
      $.ajax({
        type: "GET",
        url: "/raffles/products/" + id,
        dataType: "json",
        beforeSend: function () {
          $.LoadingOverlay("show", {
            background: "rgba(0, 0, 0, 0.5)",
            image: "",
            fontawesomeColor: "#FF60F4",
            fontawesome: "fa fa-cog fa-spin",
          });
        },
        success: function (response) {
          $.LoadingOverlay("hide");
          $("#raffle-id").val(response.id);
          $("#raffle-id").attr("value", response.id);
          console.log("change");
          $("#raffle-variant").val(response.name.split(" - ")[1]);
          $("#size").empty();
          $.each(JSON.parse(response.size), function (
            indexInArray,
            valueOfElement
          ) {
            $("#size").append(
              `<option value="${
                valueOfElement.split("US ")[1]
              }">${valueOfElement}</option>`
            );
          });
        },
      });
    }
  });

  // //Add task
  // $("#add-task").on("click", function () {
  //   // Close Modal
  //   $("#taskModal").modal("toggle");

  //   // Append Body
  //   let task_html = `<tr> <th scope="row" class="checkboxContainer"> <input type="checkbox"/> </th> <td>Bandana Box Logo Tee Black</td><td>Small</td><td>Profile 1</td><td>US Residental</td><td class="app-success-color">Successful Checkout</td><td> <a name="" id="" class="btn btn-sm btn-light mr-0 mt-2 mr-md-1 mt-lg-0" href="#" role="button" ><i class="fas fa-play fa-md btn-tasks-icon"></i ></a> <a name="" id="" class="btn btn-sm btn-light mr-0 mt-2 mr-md-1 mt-lg-0" href="#" role="button" ><i class="fas fa-edit fa-md btn-tasks-icon"></i ></a> <a name="duplicate-task" id="" class="btn btn-sm btn-light mr-0 mt-2 mr-md-1 mt-lg-0" href="#" role="button" ><i class="fas fa-copy fa-md btn-tasks-icon"></i ></a> <a name="delete-task" id="" class="btn btn-sm btn-light mr-0 mt-2 mr-md-1 mt-lg-0" href="#" role="button" ><i class="fas fa-trash fa-md btn-tasks-icon"></i ></a> </td></tr>`;
  //   $("#task-body").append(task_html);

  //   // send notif
  //   Swal.fire({
  //     position: "center",
  //     icon: "success",
  //     title: "Tasks Added",
  //     showConfirmButton: false,
  //     timer: 1500,
  //   });
  // });

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

  // Delete Proxies
  $("#proxies-body").on("click", 'a[name="delete-proxies"]', function () {
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
        let name = $(this).parent().parent().attr("data-name");
        $.ajax({
          type: "delete",
          url: "/proxies/delete",
          data: { name: name, csrf_token: $("#csrf_token").val() },
          success: function (res) {
            console.log(res);
          },
        });
        Swal.fire("Deleted!", "Your proxies has been deleted.", "success");
        $(this).parent().parent().remove();
      }
    });
  });

  // Delete Profile
  $("#profiles-body").on("click", 'a[name="delete-profile"]', function () {
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
        let id = $(this).parent().parent().attr("data-id");
        $.ajax({
          type: "delete",
          url: "/profiles/delete",
          data: { id: id, csrf_token: $("#csrf_token").val() },
          success: function (res) {
            console.log(res);
          },
        });
        Swal.fire("Deleted!", "Your profiles has been deleted.", "success");
        $(this).parent().parent().remove();
      }
    });
  });

  // Cleave JS
  new Cleave("#cc-number", {
    creditCard: true,
  });
  new Cleave("#cc-exp", {
    delimiters: ["/"],
    blocks: [2, 2],
  });
  new Cleave("#cc-cvv", {
    blocks: [4],
  });
});
