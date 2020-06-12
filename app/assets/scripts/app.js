$(document).ready(function () {
  $(window).load(function () {
    $(".overlay").fadeOut();
  });

  const Toast = Swal.mixin({
    toast: true,
    position: "bottom",
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
        let id = $(this).parent().parent().attr("data-id");
        $.ajax({
          type: "delete",
          url: "/task/delete",
          data: { id: id, csrf_token: $("#csrf_token").val() },
          success: function (res) {
            console.log(res);
          },
        });

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

  // Run Task
  $("#run-task").on("click", function () {
    Toast.fire({
      icon: "success",
      title: "Task started",
    });
    $(this).parent().parent().find(".status").text("Running");
    setTimeout(() => {
      $(this).parent().parent().find(".status").text("Submitting");
    }, 1000);

    setTimeout(() => {
      $(this).parent().parent().find(".status").text("Finished");
      Toast.fire({
        icon: "success",
        title: "Task finished",
      });
    }, 2000);
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
