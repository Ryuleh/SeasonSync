$(document).ready(function () {
  $("#cityInput").on("input", function () {
    var query = $(this).val();
    $.ajax({
      url: "/autocomplete?query=" + query,
      type: "GET",
      success: function (response) {
        var suggestions = response.suggestions;
        var datalist = $("#suggestions");
        datalist.empty();
        suggestions.forEach(function (item) {
          datalist.append('<option value="' + item + '">');
        });
      },
    });
  });
});
