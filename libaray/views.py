from datetime import date

from libaray.utils import promo
from .models import Book
from .serializers import BookSerializer
import json 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Sum
from datetime import datetime
@csrf_exempt
@require_http_methods(['GET'])
def get_all_books(request):
    """GET: get all books """
    books = Book.objects.all()
    serializer_for_book = BookSerializer(books, many=True)
    # first format of totale price 
    # total_price = 0
    # for book in books:
    #     total_price+= book.price
    
    # second format of totale price
    total_price = books.aggregate(total=Sum('price'))['total'] or 0 
    # total_price = books.aggregate(total=Sum('price'))
    # print({"total_price": total_price})
    return JsonResponse({
        "books": serializer_for_book.data,
        "count": len(serializer_for_book.data),
        "total_price": total_price
    })


@csrf_exempt
@require_http_methods(['GET'])
def get_book(request, book_id):
    """GET: get a single book"""
    # the get book is obligation try/except
    try:
        book = Book.objects.get(id=book_id)
        # en ajoute un condition  
        limite_date = date(2019,12,31)
        if book.published_data > limite_date:
            serializer = BookSerializer(book)
            return JsonResponse({
                "book" :serializer.data,
                "success": True
            })
        else:
            return JsonResponse({
                "error" :"book published before 2019/12/31",
                "success": False
            })
    # on exist un mesage d'error par default        
    except Book.DoesNotExist:
        return JsonResponse({
           "error" : "book not found",
           "success" : False
        })


@csrf_exempt
@require_http_methods(['POST'])
def create_book(request):
    """POST : create a book"""
    # input at a users
    json_data = json.loads(request.body)
    
    """part in the date """
    # traitement : exp: promo date  i want to 2019/12/31 : on aplique a promo
    promo_date = date(2019,12,31) # fixé la date 
    print({"type_promo_date": type(promo_date)}) # type date
    print({"type_published_data": type(json_data['published_data'])})# published_data: type str
    
    # acceder published_date (date+str) en transfert type date 
    date_book =datetime.strptime(json_data['published_data'], "%Y-%m-%d").date()
    print({"date_book": date_book}) 
    print({"type_date_book":type(date_book)})
    
    """part for in a price """
    # la promo price in the book -25% for a date at time long 
    price_book = json_data['price'] # json_data : key or value the price 
    if date_book < promo_date:
        promo_price = round(price_book -((price_book/100)*25),2) # v1 
        promo_price=promo(promo_price) # v2
        print({"promo_price": promo_price}) # it's not execute of the response the promo_price 
        json_data['price'] = promo_price  # en verifiver dans l'execution de requet est existe sous format json    
    
    #return JsonResponse({ "message": "test trait"})
    
    serializer_book = BookSerializer(data=json_data) #  serializer : is validate the  json_data in body on execution it's all  True  
    if serializer_book.is_valid():
        book = serializer_book.save()
        book_data = BookSerializer(book).data
        return JsonResponse({
            "message": "book created successfully",
            "book": book_data,
            "success": True
        })
    return JsonResponse({
        "error": serializer_book.errors,
        "success": False
    })
 

@csrf_exempt
@require_http_methods(['PUT'])
def update_book(request):
    """PUT: update a book """
    json_data = json.loads(request.body)
    
    try:
        book = Book.objects.get(id=json_data['id'])
    except Book.DoesNotExist:
        return JsonResponse({
            "error": "book not found", 
            "success": False
        })
    serializer_book_update = BookSerializer(book, data=json_data)
    if serializer_book_update.is_valid():
        book = serializer_book_update.save()
        book_data= BookSerializer(book).data
        return JsonResponse({
            "messaage": "book updated sucessfully",
            "book": book_data,
            "success": True
        })
    return JsonResponse({
        "error" : serializer_book_update.errors,
        "success" : False
    })

@csrf_exempt
@require_http_methods(['DELETE'])
def delete_book(request, book_id):
    """delete a books"""
    try:
        book =Book.objects.get(id=book_id)
        book.delete()
        return JsonResponse({
            "message": "book deleted successfully",
            "success": True
        })
        
    except Book.DoesNotExist:
        return JsonResponse({
            "error": "book not found",
            "success": False
        })