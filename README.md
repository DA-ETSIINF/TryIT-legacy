Instructions  to set up a new edition:

1º Create new edition (django admin panel -> editions)
2º Go to  settings_global.py and change EDITION_YEAR, disable TICKETS_SALE, VOLUNTEERS, READY_FOR_NEW_ED
3º templates/congress.html Comment <li><a href="{% url 'congress:activities' %}">Programa</a></li>--> (computer line 77	 and computer line 65)
4º templates/congress/last_editions add last year edition to the list
