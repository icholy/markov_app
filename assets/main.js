
var users = [
    "Brandon Rosier",
    "Caroline Kupka",
    "Christopher Daniel",
    "Claire",
    "Deven Gelinas",
    "Dylan St Onge",
    "Ilia Choly",
    "John Clare",
    "Kaitlin Labatte",
    "Kate DeGasperis",
    "Kelsey Kaupp",
    "Lindsey Brown",
    "Mark Meleka",
    "Mike Edward",
    "Mike Oligradskyy",
    "Nate Fawcett",
    "Nick Felice",
    "Olivia Bullock",
    "Pola Kurzydlo",
    "Sarah Ollikainen",
    "Sarah Ross",
    "Sean Haine",
    "Steven Murphy",
    "Thomas Gabriele",
    "Tom Bonomi"
];

$(document).ready(function () {

  var $sentence = $("#sentence");

  function getSelectedUsers() {
    var users = [];
    $(".user-checkbox").each(function (index, el) {
      var $checkbox = $(el);
      if ($checkbox.is(":checked")) {
        users.push($checkbox.val());
      }
    });
    return users;
  }

  function refresh() {
    var users = getSelectedUsers();
    $.ajax({
      dataType: "text",
      url: "/generate_sentence",
      data: { u: users },
      success: function (response) {
        $sentence.html(response);
      },
      error: function () {
        $sentence.html("Error: try again :(");
      }
    });
  }

  $("#generate_btn").click(function () {
    refresh();
    return false;
  });

  refresh();
});
