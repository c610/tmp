var ourTab = ['admin','administrator','robots.txt','somRandErr.file','joomla','wp-admin']
var req = new XMLHttpRequest();

for (var x = 0 ; x < ourTab.length ; x++){

        req.open('GET', ourTab[x], false);
        req.onreadystatechange = function() {
                if(req.readyState && req.status == 200) {
                        document.write("Check : " + ourTab[x] + " -> Status: " + req.status + "<br>");
                }
                if (req.readyState && req.status == 404){
                        document.write("Check : " + ourTab[x] + " -> Status: " + req.status + "<br>");
                }
                if (req.readyState && req.status == 403){
                        document.write("Check : " + ourTab[x] + " -> Status: " + req.status + "<br>");
                }
        }
        req.send();



}
