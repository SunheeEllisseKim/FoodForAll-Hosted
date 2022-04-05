from django.shortcuts import render
from django.http import HttpResponse
import datetime
print("VIEWS>.py")
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates)'
)
from foodbank import foodBankAndCovid 


# Create your views here.
def index(request):
    print("at INDEX", request)
    today = datetime.datetime.now().date()
    print("***")
    #foodBankAndCovidData = foodBankAndCovid()
    foodBankAndCovidData = foodBankAndCovid.returnDataForRecipient('115 New Cavendish Street')
    #print("here getFoodBankAndCovidData",foodBankAndCovidData)

    #response = HttpResponse('index.html')
    # print('response', response)
    #response.write("<p>Here's the text of the web page.</p>")
    #response.write("<p>Here's another paragraph.</p>")

    #foodBankAndCovidData = "\n\n <span style="white-space: pre-line"> <br> <<br/>> <p>This is Line1 </span></p> <p>This is Line2</p>here we go"
    #v = render(request, "index.html", {"today": today})
    if request.method == 'POST':
            print("POST METHOD")
            content = request.POST.get('content', '')
            print("inputAddress")
            if content:
                print('Content', content)
                foodBankAndCovidData = foodBankAndCovid.returnDataForRecipient(str(content))
    #inputAddress = request.POST.get('inputAddress', '')

    return render(request, "index1.html", {"FoodBankData": foodBankAndCovidData})
