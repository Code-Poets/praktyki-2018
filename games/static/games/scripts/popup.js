$( function() {
  $( "#dialog" ).dialog({
    modal: true,
    title: popup_message_title,
    buttons: [
      {
        text: popup_message_yes,
        click: function () {
          window.location.href = path_yes;
        }
      },
      {
        text: popup_message_no,
        click: function () {
          window.location.href = path_no;
        }
      }
    ]
  });
} );
