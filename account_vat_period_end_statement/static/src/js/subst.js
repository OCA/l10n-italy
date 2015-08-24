function subst() {
    var vars = {};
    var x = document.location.search.substring(1).split('&');
    for (var i in x) {
        var z = x[i].split('=', 2);
        vars[z[0]] = unescape(z[1]);
    }
    var x=['frompage', 'topage', 'page', 'webpage', 'section', 'subsection', 'subsubsection'];
    for (var i in x) {
        var y = document.getElementsByClassName(x[i]);
        
        fiscal_page_base = 0
        if (document.getElementById('count_fiscal_page_base').innerHTML){
            fiscal_page_base = parseInt(document.getElementById('count_fiscal_page_base').innerHTML);    
        }    
        
        for (var j=0; j<y.length; ++j)
             if (x[i] == 'page') { y[j].textContent = eval(vars[x[i]])+ fiscal_page_base; }
           else { y[j].textContent = vars[x[i]]; }

    }
   
  
}


