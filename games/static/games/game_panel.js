function myFunction(id) {
    var count = 0;
    document.write("<p>Jestem</p>");
    document.write("<p>Gamer order="+id+"</p>");
    /*
    {% for gamer in gamers.all %}
      if ( {{ gamer.order }} == id){
        document.write('<table bgcolor="ffe5ba"><tr><td>{{ gamer.nick }}</td><td>{{ gamer.order }}</td></tr></table>');
        if ( {{ gamer.gender }} == "None"){
          document.write("None");
        }

        count = count + 1;
      }
    {% endfor %}
    if (count == 0){
      document.write("{% trans 'Free place for gamer' %}");
    }
    */
    document.write("<p>{{ gamers.0.nick }}</p>");
    if ( "{{ gamers.0.gender }}" == "Female"){
      document.write('<img src="{% static "games/images/female.png" %}" alt="Female" style="width:10%;">');
    }
  }
