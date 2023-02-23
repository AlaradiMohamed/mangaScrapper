# %%
from whatsappScrapper import sendWhatsappMsg, getURLs
from animeScrapper import initiateScrapping
from emailScrapper import sendEmail

# %%
errors, success, pdfs = [], [], []
fileCount, batchsize = 0, 3
whatsappMsg = ''
emailList = 'MOHD19NASS_BSKQAF@kindle.com'

urls = set(getURLs())
files = len(urls)
if files < 5:
    batchsize = files

if urls:
    for aUrl in urls:
        try:
            fileCount += 1
            pdfPath = initiateScrapping(aUrl)
            pdfs.append(pdfPath)
            if fileCount == batchsize:
                print('email sent')
                sendEmail(emailList, pdfs, messageBody = '')
                pdfs = []
            success.append(pdfPath.split('/')[-1]) 
        except:
            errors.append(aUrl)

        if fileCount == batchsize:
            if  success:
                whatsappMsg = 'The following mangas have been sent successfully:\n' + '\n'.join(['- ' + item for item in success])
            if errors:
                whatsappMsg += '\n\nThe folowing URLs failed:\n' + '\n'.join(['- ' + item for item in errors])
            sendWhatsappMsg('+97333775430', whatsappMsg)

            fileCount = 0
            whatsappMsg = ''
            errors, success = [], []
            files -= batchsize
            if files < batchsize:
                batchsize = files



