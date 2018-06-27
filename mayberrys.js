window.onload = function(){//window.addEventListener('load',function(){...}); (for Netscape) and window.attachEvent('onload',function(){...}); (for IE and Opera) also work
    alert('<%: TempData["Resultat"]%>');
}
<!-- Some custom code to redirect customers that don't have the right tags-->
    {% if template.name == 'list-collections' or collection %}
  		{% unless customer.tags contains 'stylist' and customer.tags contains 'registered' %}
  
          <script>
            //alert('{{ customer.tags }}');
            {% if customer.tags contains 'stylist' %}
            	if (confirm("Press 'OK' if this is your first time shopping wholesale with Mayberrys Fashion.")) {
    				alert("Awesome!!! Purchase a stylist package to complete your stylist registration and get access great fashion at wholesale prices!");
            		window.location.top.href='/pages/become-a-stylist';
				} else {
    				alert("You've logged into an account that hasn't completed stylist registration.  Please check that you've logged into the correct stylist dashboard account and click 'Shop Wholesale' again.  If you continue to have problems, please email stylistsupport@mayberrysfashion.com.");
                  	window.location.top.href='https://stylists.mayberrysfashion.com';
				}
            	
            {% else %}
            	alert("Welcome to Mayberrys Fashion's wholesale site! Signup to become a stylist to get access to our amazing fashion at wholesale prices!");
            	window.location.top.href='https://mayberrysfashion.com/pages/become-a-stylist';
            {% endif %}
            
          </script>
  		
  
  		{% endunless %}
  	{% endif %}
    
   <!--End comment -->

<!-- Some custom code to redirect customers that don't have the right shopify tags-->
    {% if template.name == 'list-collections' or collection %}
  		{% unless customer.tags contains 'stylist' and customer.tags contains 'registered' %}
  
          <script>
            //alert('{{ customer.tags }}');
            {% if customer.tags contains 'stylist' %}
            	window.onload = function(){
                    if (confirm("You made it to Mayberrys Fashion wholesale catalog!!!  Press 'OK' if this is your first time shopping wholesale with Mayberrys Fashion.")) {
    				    alert("Awesome!!! Purchase a stylist package to complete your stylist registration and get access to great fashion at wholesale prices!" +"\r\n" +"\r\n" +"If you've already purchased a stylist package, then you've logged into an account that hasn't completed stylist registration.  Please check that you've logged into the correct stylist dashboard account and click 'Shop Wholesale' again.  If you continue to have problems, please email stylistsupport@mayberrysfashion.com.");
            		    window.location.href='/pages/become-a-stylist';
                    } else {
                        alert("It doesn't look like you've purchased a Stylist package yet!  Purchase a stylist package to get access to great fashion at wholesale prices!" +"\r\n" +"\r\n" +"If you've already purchased a stylist package, double check that you've logged into the correct stylist dashboard account  at stylists.mayberrysfashion.com and click 'Shop Wholesale' again.  If you continue to have problems, email stylistsupport@mayberrysfashion.com, and we'll get you squared away.");
                        window.location.href='https://stylists.mayberrysfashion.com';
                    }
                }
            	
            {% else %}
            	window.onload = function(){
                    alert("Welcome to Mayberrys Fashion's wholesale site! Signup to become a stylist and get access to our amazing fashion at wholesale prices!");
            	    window.location.href='https://mayberrysfashion.com/pages/become-a-stylist';
                }
            {% endif %}
            
          </script>
  		
  
  		{% endunless %}
  	{% endif %}
    
   <!--End custom code to redict customers that don't have the right shopify tags -->
     
     