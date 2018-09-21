$(function () {
    $("#dialog").dialog ({
        modal: true,
        autoOpen: false,
        buttons : [
          {
            text: trans_yes,
            click: function () {
              window.location.href = end_game_path;
            }
          },
          {
            text: trans_no,
            click: function () {
              $(this).dialog('close');
            }
          }
        ]
    }).prev().find(".ui-dialog-titlebar-close").hide ();

    $("#DialogShow").click(function () {
        $('#dialog').dialog('open');
    });

    $("#alert").dialog ({
        modal: true,
        autoOpen: false,
        buttons : [
          {
            text: message_yes,
            click: function () {
              window.location.href = game_panel_path;
            }
          },
          {
            text: message_no,
            click: function () {
              $(this).dialog('close');
            }
          }
        ]
    }).prev().find(".ui-dialog-titlebar-close").hide ();

    $("#AlertShow").click(function () {
      var check = false;
      for (x in gamers) {
        if (gamers[x].order == "None") {
          check = true;
        }
      }
      if ( check == true ){
        $('#alert').dialog('open');
      }
      else {
        window.location.href = game_panel_path;
      }
    });
});
