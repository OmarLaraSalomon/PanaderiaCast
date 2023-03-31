#variable global para manejar la vlase de carrito 

def importe_total_carro(request):
    total = 0

    if request.user.is_authenticated:
     #   if request.user.is_superuser == True:
       if "carro" in request.session.keys():
        for key, value in request.session["carro"].items():
                total=total+ float(value["precio"])
    return {"importe_total_carro": total} 



#def importe_total_carro(request):
 #   total=0
  #  if request.user.is_authenticated:
   #     for key, value in request.session["carro"].items():
    #        total=total+float(value["precio"])

    #else:
     #   total="Debes hacer login"
   
        
    #return {"importe_total_carro":total}
    