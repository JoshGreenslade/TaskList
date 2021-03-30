$(function () {

  /* Functions */

  var rerender_projects = function(data) {
    let pre_cards = $('.collapsable');
    $("#project-accordian").html(data.html_project_list);
    let post_cards = $('.collapsable');
    pre_cards.each((idx, value) => {
      if (value.classList.contains("show")) {
        if (post_cards[idx]) {
          $('#'+post_cards[idx].id).addClass('no-transition').collapse('show').removeClass('no-transition');
        }
      }
    })
  }

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-project").modal("show");
      },
      success: function (data) {
        $("#modal-project .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function (e) {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        console.log('hello');
        if (data.form_is_valid) {
        //  Rerender the form, but render the collapsed elements correctly.
          rerender_projects(data)
          $("#modal-project").modal("hide");
        }
        else {
          $("#modal-project .modal-content").html(data.html_form);
        }
      },
      fail: function (e) {
        console.log(e);
      }
    });
    return false;
  };

  var _runViewAndCloseModal = function(btn) {
    $.ajax({
      url: btn.attr("data-url"),
      dataType: 'json',
      success: function (data) {
        rerender_projects(data)
        $("#modal-project").modal("hide");
      }
    });
  }

  var toggleDone = function (e) {
    var btn = $(this);
    console.log('Button Pushed ' + btn.attr("data-url"))
    _runViewAndCloseModal(btn);
  }

  var delete_item = function (e) {
    var btn = $(this);
    var confirmed = confirm("Are you sure?");
    if (confirmed) {
      console.log('Time to delete: ' + btn.attr("data-url"));
      _runViewAndCloseModal(btn);
    }
  }


  


  /* Binding */

  // Create project
  $(".js-create-project").click(loadForm);
  $("#modal-project").on("submit", ".js-project-create-form", saveForm);

  // Update project
  $("#project-accordian").on("click", ".js-update-project", loadForm);
  $("#modal-project").on("submit",".js-project-update-form", saveForm);

  // Update task
  $("#project-accordian").on("click", ".js-update-task", loadForm);
  $("#modal-project").on("submit",".js-task-update-form", saveForm);

  // Delete task
  $("#modal-project").on("click",".js-delete-task", delete_item);

  // Delete project
  $("#modal-project").on("click",".js-delete-project", delete_item);

  // Create task
  $("#project-accordian").on("click", ".js-create-task", loadForm);
  $("#modal-project").on("submit", ".js-task-create-form", saveForm);

  // Toggle done button
  $("#project-accordian").on("click", ".js-completed-toggle", toggleDone);
  
});