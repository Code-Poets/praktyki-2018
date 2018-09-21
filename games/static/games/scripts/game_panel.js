/*
function myFunction(id) {
    var count = 0;
    {% for gamer in gamers.all %}
      {% if gamer.order is not null %}
      if ( {{ gamer.order }} == id){
        document.write('<table id="gamer" bgcolor="ffe5ba"><col width="25%"><col width="25%"><col width="25%"><col width="25%">');
        document.write('<tr align="center"><td style="border: 1px solid black;border-style: dotted;"><font color="DimGray" size="3">'+id+'</font></td>');
        document.write('<td colspan="2"><font size="5%">{{ gamer.nick }}</font></td>');
        document.write('<td align="left">');
        if ("{{ gamer.gender }}" == "Female"){
          document.write('<img src="{% static "games/images/female.png" %}" alt="Female" style="width:40%;">');
        }
        else if ("{{ gamer.gender }}" == "Male") {
          document.write('<img src="{% static "games/images/male.png" %}" alt="Male" style="width:40%;">');
        }
        else{
          document.write('<img src="{% static "games/images/none.png" %}" alt="None" style="width:40%;">');
        }
        document.write('</td></tr>');

        {% if gamer.status is not None and gamer.status != "" %}
            document.write('<tr><td align="center" colspan="4" style="word-wrap:break-word"><font color="#cc7e00" size="1%">"{{ gamer.status }}"</font></td></tr>');
        {% else %}
            document.write('<tr><td id="status" colspan="4" style="word-wrap:break-word"><font color="ffe5ba" size="1%">Status</font></td></tr>');
        {% endif %}

        document.write('<tr><td align="center" colspan="2"><font size="1%" color="DimGray">Lvl: <font size="6%" color="red">{{ gamer.level }}</font</td>');
        document.write('<td align="left" colspan="2"><font size="1%"color="DimGray">Bonus: <font size="6%" color="green">{{ gamer.bonus }}</font></td></tr>');

        document.write('<tr align="center"><td colspan="2"><font size="2%" color="DimGray">{% trans "Race" %}: </font></td>');
        document.write('<td colspan="2"><font size="2%" color="DimGray">{% trans "Class" %}: </font></td></tr>');

        document.write('<tr align="center"><td colspan="2">');
        {% if gamer.race_slot_1 != None %}
          document.write('{{ gamer.race_slot_1 }}');
        {% else %}
          document.write('<font color="ffe5ba">{% trans "Race" %}: </font>');
        {% endif %}
        document.write('</td><td colspan="2">');
        {% if gamer.class_slot_1 != None %}
          document.write('{{ gamer.class_slot_1 }}');
        {% else %}
          document.write('<font color="ffe5ba">{% trans "Class" %}: </font>');
        {% endif %}
        document.write('</td></tr>');

        document.write('<tr align="center"><td colspan="2">');
        {% if gamer.race_slot_2 != None %}
          document.write('{{ gamer.race_slot_2 }}');
        {% else %}
          document.write('<font color="ffe5ba">{% trans "Race" %}2: </font>');
        {% endif %}
        document.write('</td><td colspan="2">');
        {% if gamer.class_slot_2 != None %}
          document.write('{{ gamer.class_slot_2 }}');
        {% else %}
          document.write('<font color="ffe5ba">{% trans "Class" %}2: </font>');
        {% endif %}
        document.write('</td></tr>');

        document.write('</table>');

        count = count + 1;
      }
      {% endif %}
    {% endfor %}
    if (count == 0){
      document.write('<font color="DimGray">{% trans "Free place for gamer" %}');
      document.write('<font size="2"><br>{% trans "Chair number" %} '+id+'</font>');
    }
  }
*/

//sortowanie wektora graczy po parametrze order
//gamers.sort(function(a,b) {return (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0);} );

function sortFunction(a,b) {
  if (a.order > b.order){
    return 1;
  }
  else if (a.order < b.order){
    return -1;
  }
  else {

      if (a.id > b.id){
        return 1;
      }
      else if (a.id < b.id) {
        return -1;
      }
      else return 0;
  }
}
//sortowanie wektora graczy po parametrze order i id
gamers.sort(sortFunction);

  function GamerDisplay(x) {
    document.write('<table id="gamer" bgcolor="ffe5ba"><col width="25%"><col width="25%"><col width="25%"><col width="25%">');
    document.write('<tr align="center"><td style="border: 1px solid black;border-style: dotted;"><font color="DimGray" size="3">'+gamers[x].order+'</font></td>');
    document.write('<td colspan="2"><font size="5%">'+gamers[x].nick+'</font></td>');

    document.write('<td align="left">');
    if (gamers[x].gender == "Female"){
        document.write('<img src="/static/games/images/female.png" %}" alt="Female" style="width:40%;">');
    }
    else if (gamers[x].gender == "Male") {
        document.write('<img src="/static/games/images/male.png" %}" alt="Male" style="width:40%;">');
    }
    else{
        document.write('<img src="/static/games/images/none.png" %}" alt="None" style="width:40%;">');
    }
    document.write('</td></tr>');

    if (gamers[x].status != "None" && gamers[x].status != ""){
      document.write('<tr><td align="center" colspan="4" style="word-wrap:break-word"><font color="#cc7e00" size="1%">"'+gamers[x].status+'"</font></td></tr>');
    }
    else {
      document.write('<tr><td id="status" colspan="4" style="word-wrap:break-word"><font color="ffe5ba" size="1%">Status</font></td></tr>');
    }

    document.write('<tr><td align="center" colspan="2"><font size="1%" color="DimGray">Lvl: <font size="6%" color="red">'+gamers[x].level+'</font</td>');
    document.write('<td align="left" colspan="2"><font size="1%"color="DimGray">Bonus: <font size="6%" color="green">'+gamers[x].bonus+'</font></td></tr>');

    document.write('<tr align="center"><td colspan="2"><font size="2%" color="DimGray">'+trans_race+': </font></td>');
    document.write('<td colspan="2"><font size="2%" color="DimGray">'+trans_class+': </font></td></tr>');

    document.write('<tr align="center"><td colspan="2">');
    if (gamers[x].race_1 != "None"){
      document.write(gamers[x].race_1);
    }
    else{
      document.write('<font color="ffe5ba">_</font>');
    }
    document.write('</td><td colspan="2">');
    if (gamers[x].class_1 != "None"){
      document.write(gamers[x].class_1);
    }
    else {
      document.write('<font color="ffe5ba">_</font>');
    }
    document.write('</td></tr>');

    document.write('<tr align="center"><td colspan="2">');
    if (gamers[x].race_2 != "None"){
      document.write(gamers[x].race_2)
    }
    else {
      document.write('<font color="ffe5ba">_</font>');
    }
    document.write('</td><td colspan="2">');
    if (gamers[x].class_2 != "None"){
      document.write(gamers[x].class_2);
    }
    else{
      document.write('<font color="ffe5ba">_</font>');
    }
    document.write('</td></tr>');

    document.write('</table>');
  }

  function NoGamerDisplay() {
    document.write('<font color="DimGray">'+message_free);
    document.write('<font size="2"><br>'+message_order+' '+order+'</font></font>');
  }

//NoGamerDisplay();
//GamerDisplay();
/*
var text, len, i;

text = "<ul>";

len = gamers.length;
for (i = 0; i < len; i++) {
    text += "<li>" + gamers[i].nick + " id:" + gamers[i].id + " o:" + gamers[i].order +"</li>";
}
document.write(text);
*/

function Display() {
  var count = 0;
  var array_len = gamers.length;

  for (i = 0; i <array_len; i++){
    if (gamers[i].order == order){
      GamerDisplay(i);
      count += 1;
    }
  }
  if (count == 0) {
      NoGamerDisplay();
  }
}

Display();
