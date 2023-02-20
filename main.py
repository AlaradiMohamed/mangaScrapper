# %%
from whatsappScrapper import sendWhatsappMsg, getURLs
from animeScrapper import initiateScrapping
from emailScrapper import sendEmail

# %%
errors, success = [], []
whatsappMsg = ''
# emailList = 'MOHD19NASS_BSKQAF@kindle.com'
emailList = 'mohd19nass@gmail.com'

for aUrl in getURLs():
    try:
        pdfPath = initiateScrapping(aUrl)
        sendEmail(emailList, [pdfPath], messageBody = '')
        success.append(pdfPath.split('/')[-1]) 
    except:
        errors.append(aUrl)
    break
    
whatsappMsg = 'The following mangas have been sent successfully:\n' + '\n'.join(success)
if errors:
    whatsappMsg += '\n\nThe folowing URLs failed:\n' + '\n'.join(errors)

sendWhatsappMsg('+97333775430', whatsappMsg)



