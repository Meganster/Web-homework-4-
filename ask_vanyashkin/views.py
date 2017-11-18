from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def getpost(request):
    getPar = "GET:<br>"
    for key in request.GET:
        getPar += str(key) + " = " + str(request.GET[key]) + "<br>"

    textVal = request.POST.get("textVal")

    htmlPart = ""
    htmlPart += """
    <html>
    <body>
       <form method="post" action="">
            <p>
               text: <input type="text" name="textVal" value="%(textVal)s">
            </p>
            <p>
                <input type="submit" value="Submit">
            </p>
        </form>
    </body>
    </html>""" % {
        'textVal': textVal or 'Empty'
    }

    postPar = "POST:<br>"
    for key in request.POST:
        postPar += str(key) + " = " + str(request.POST[key]) + "<br>"

    outPut = htmlPart + "<br>" + getPar + "<br>" + postPar
    return HttpResponse(outPut)


def helloworld(request):
    now = "Helloworld"
    html = "<html><body> %s </body></html>" %now
    return HttpResponse(html)


