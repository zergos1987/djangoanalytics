#from django.core.mail import send_mail
#send_mail('test test test', 'test message.', 'email', ['email'], fail_silently=False,)
# from exchangelib import DELEGATE, IMPERSONATION, Account, Credentials, EWSDateTime, EWSTimeZone, Configuration, NTLM, GSSAPI, CalendarItem, Message, Mailbox, Attendee, Q, ExtendedProperty, FileAttachment, ItemAttachment, HTMLBody, Build, Version, FolderCollection

# credentials = Credentials('domain\\username', 'passwrod')
# account = Account(
#     primary_smtp_address='email', 
#     credentials=credentials, 
#     autodiscover=True, 
#     #auth_type=NTLM, 
#     verify_ssl=False)

# for item in account.inbox.all().order_by('-datetime_received')[:100]:
#     print(item.subject, item.sender, item.datetime_received)




# from requests_kerberos import HTTPKerberosAuth
# from exchangelib import DELEGATE, Account, Credentials, Configuration
# import exchangelib.autodiscover

from requests_kerberos import HTTPKerberosAuth
from exchangelib import DELEGATE, Account, Credentials, Configuration
import exchangelib.autodiscover

from exchangelib import CalendarItem, Message, Mailbox, \
  FileAttachment, HTMLBody
from exchangelib.items import SEND_ONLY_TO_ALL, SEND_ONLY_TO_CHANGED
from exchangelib.properties import DistinguishedFolderId


def auth_model(**kwargs):
    #get kerberos ticket 
    return HTTPKerberosAuth()


def connect(server, email, username, password=1):
    from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
    # Care! Ignor Exchange self-signed SSL cert
    BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

    # fill Credential object with empty fields    
    creds = Credentials(
        username="",
        password=""
    )

    # add kerberos as GSSAPI auth_type
    exchangelib.transport.AUTH_TYPE_MAP["GSSAPI"] = auth_model

    # Create Config
    config = Configuration(server=server,credentials=creds, auth_type="GSSAPI")
    # return result
    return Account(primary_smtp_address=email, autodiscover=False, config=config, access_type=DELEGATE)

def main():
    # Connection details
    server = 'exchange_server' #server.dc.domain.ru
    email = 'email' #email@domain.ru
    username = 'domain\username' # domain\login
    account = connect(server, email, username)

    #print('ad_response ==========', my_account.ad_response)
    # for item in account.inbox.all().order_by('-datetime_received')[:2]:
    #     print(item.subject, item.sender, item.datetime_received)

    m = Message(
        account=account,
        subject='title test',
        body='body test',
        to_recipients=[
            Mailbox(email_address='email'),
            Mailbox(email_address='email'),
        ],
        # Simple strings work, tooa
        cc_recipients=['email', 'email'],
    )
    m.send()
    account.protocol.close()

print('111 ===============================================================================')
main()
print('222 ===============================================================================')
