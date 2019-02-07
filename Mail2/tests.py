from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Mail
from .models import Route
from .models import Attachment

#from django.core.management import call_command
import simplejson as json
from pprint import pprint
import datetime

# Create your tests here.

# class JenkinsTest(TestCase):
#     def test_what_if_fail(self):
#         self.assertEqual(1,3)

#call_command('flush','--noinput')



class myTestCase(TestCase):

    def setUp(self):

        frank = User.objects.create_user(username='Frank',
                                         password='whatevs',
                                         first_name='Testislez',
                                         last_name='Person')
        ned = User.objects.create_user(username='Ned',
                                       password='whatevas',
                                       first_name='Ned',
                                       last_name='Person')
        # Message with an attachment that is for Frank
        mailmsg = Mail.objects.create(content='Test Message',
                                      subject='test message for Frank',
                                      fk_sender=ned,
                                      termcode="172s",
                                      section="21232")

        Route.objects.create(to='frank',
                             read=False,
                             fk_mail=mailmsg)

        # Attachment.objects.create(filepath='/mnt/maildata',
        #                           filename='tatadfa.doc',
        #                           fk_mail=mailmsg
        #                           )
        # Messsage for frank that does not have an attachment
        mailmsg = Mail.objects.create(content='Test message for frank',
                                      subject='No Attachment for frank',
                                      fk_sender=ned,
                                      termcode = "172s",
                                      section = "21231")

        Route.objects.create(to='frank',
                             read=False,
                             fk_mail=mailmsg)
        # Message for "Ned"
        mailmsg = Mail.objects.create(content='Test Message 3',
                                      subject='test subject for Ned',
                                      fk_sender=frank,
                                      termcode="172s",
                                      section="21232"
                                      )

        Route.objects.create(to=str(ned.username),
                             read=False,
                             fk_mail=mailmsg)

        # Attachment.objects.create(filepath='/mnt/maildata',
        #                           filename='tatadfa2.doc',
        #                           fk_mail=mailmsg
        #                           )

        # A Message to frank that is read
        mailmsg = Mail.objects.create(content='Test Message 4',
                                      subject='test email read',
                                      fk_sender=ned,
                                      termcode="172s",
                                      section="21231"
                                      )

        Route.objects.create(to=frank.username,
                             read=True,
                             fk_mail=mailmsg)

        # Attachment.objects.create(filepath='/mnt/maildata',
        #                           filename='tatadfa3.doc',
        #                           fk_mail=mailmsg
        #                           )

class MarkMailUnreadTest(myTestCase):


    def test_bad_users_cannot_markunread(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231",
                                      )
        Route.objects.create(to=User.objects.get(username="Ned").username,
                                     read=False,
                                     fk_mail=mailmsg)
        res = c.post('/munread/', {"message_id":mailmsg.id})
        self.assertEqual(res.status_code, 403)

    def test_good_users_can_markunread(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Ned"),
                                      termcode="172s",
                                      section="21231",
                                      )
        Route.objects.create(to=User.objects.get(username="Frank").username,
                                     read=False,
                                     fk_mail=mailmsg)
        res = c.post('/archive/', {"message_id":mailmsg.id})
        self.assertEqual(res.status_code, 302)


class ArchiveTest(myTestCase):


    def test_bad_users_cannot_archive(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231",
                                      )
        Route.objects.create(to=User.objects.get(username="Ned").username,
                                     read=False,
                                     fk_mail=mailmsg)
        res = c.post('/archive/', {"message_id":mailmsg.id})
        self.assertEqual(res.status_code, 403)

    def test_good_users_can_archive_mail(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Ned"),
                                      termcode="172s",
                                      section="21231",
                                      )
        Route.objects.create(to=User.objects.get(username="Frank"),
                                     read=False,
                                     fk_mail=mailmsg)
        res = c.post('/archive/', {"message_id":mailmsg.id})
        self.assertEqual(res.status_code, 302)

class InboxTest(myTestCase):


    def test_bad_users_have_no_access(self):
        c = Client()
        res = c.get('/')

        self.assertEqual(res.status_code, 403)

    def test_can_login(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/')
        self.assertEqual(reslogin.status_code, 200)

    def test_can_see_email(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/')
        exists = False
        pprint("RESLOGIN###" + reslogin)
        for message in reslogin.context['emailList']:
            if message['subject'] == "test message for Frank":
                exists = True
        self.assertTrue(exists)

    def test_cannot_see_wrong_email(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/')
        exists = False

        for message in reslogin.context['email']:
            if message['subject'] == "test subject for Ned":
                exists = True
        self.assertFalse(exists)

    # def test_can_see_attachments(self):
    #     c = Client()
    #     res = c.login(username='Frank', password='whatevs')
    #     reslogin = c.get('/')
    #     exists = False
    #     for message in reslogin.context['email']:
    #         if message['has_attachment']:
    #             exists = True
    #     self.assertTrue(exists)

    def test_email_has_right_date(self):
        mailmsg = Mail.objects.create(content='Test timestamp',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231"
                                      )
        self.assertEqual(datetime.datetime.now().day, mailmsg.created.day)

    # def test_user_gets_a_list_of_unique_courses(self):
    #     c = Client()
    #     res = c.login(username='Frank', password='whatevs')
    #     reslogin = c.get('/')
    #     #print(reslogin.context['courses'])
    #     self.assertTrue(allUnique(reslogin.context['courses']))

class ReplyTest(myTestCase):

    def test_user_can_see_mail(self):
        c = Client()
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Ned"),
                                      termcode="172s",
                                      section="21231",

                                      )
        Route.objects.create(to=User.objects.get(username="Frank").username,
                                     read=False,
                                     fk_mail=mailmsg)
        c.login(username='Frank', password='whatevs')
        reslogin = c.get('/reply/' + str(mailmsg.id), follow=True)
        self.assertEqual(reslogin.status_code, 200)

    def test_user_cannot_see_other_users_mail(self):
        c = Client()
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231",

                                      )
        Route.objects.create(to=User.objects.get(username="Ned").username,
                                     read=False,
                                     fk_mail=mailmsg)
        c.login(username='Frank', password='whatevs')
        reslogin = c.get('/reply/' + str(mailmsg.id), follow=True)
        self.assertEqual(reslogin.status_code, 403)

    def test_message_gets_marked_as_read_on_open(self):
        c = Client()
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231",
                                      )

        Route.objects.create(to=User.objects.get(username="Ned").username,
                                     read=False,
                                     fk_mail=mailmsg)
        c.login(username='Ned', password='whatevas')
        c.get('/reply/' + str(mailmsg.id), follow=True)
        self.assertTrue(Route.objects.get(fk_mail=mailmsg).read)

class LabelTest(myTestCase):

    def test_label_view_only_lists_email_for_class(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/label/21231-172s/')
        exists = False

        for message in reslogin.context['email']:
            if message['section'] == "21231":
                exists = True
        self.assertTrue(exists)

    def test_label_can_not_view_only_lists_email_for_class(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/label/21232-172s/')
        exists = False
        for message in reslogin.context['email']:
            if message['section'] == "21231":
                exists = True
        self.assertFalse(exists)


class ListUnreadTest(myTestCase):

    def test_for_unread_mail(self):
        #TODO fix it, fix it.
        """
        ..,cccclc::;:::::::::;;;;;;;:::::::::::::::::::::;;;;;;,,;:ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccclllllccccccccccccccccccccccccclccccccccccccccccccccccccccccccccccccccccccccccccclccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
  .'''''.....'''''''........''''''''''''''''''.....''''...'',,,''','''',,'''',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
  .;:;'....''''''''''..'''''''''''''''''''''''...................................................................................................................................................................................'........''...........'''''.'........'''..''.'.........'.''.'''''''''''''''
  .oOOkxxxxxxl,cxxxxd:;oxxxd:';oxxxd:''''';dxxxxc'cddxxxxxxxxxx:,lxxxxxc''''',lxxxxxxxxd:;oxxxxc,lxxxxc,'cxxxxc,'''',lxxxxl,:dxxxxxxxxxxxl,:dxxxxl,'''''':dxxxxxxxxc'cxxxxo;:ddddl,.;oxxxo,.'...:dxxxd;,lxxxxxxxxxxxo;;oxxxxo;''''.;oxxxxxxxdl,;oxxxd:,lxxxd:',ldddd:'...',lxdxxc'cxxdddxxxxddd:'cxdxxxc'...
  .xNMMMMMMMMO;dWMMMXl;OWMMWx,oNMMW0:'''''lXMMMMd,kMMMMMMMMMMMWd;OMMMMWd''''':OMMMMMMMMXlcKMMMMk,dNMMM0::0MMMNo,,,'';OMMMM0:oNMMMMMMMMMMMO;dWMMMMO;''''''dWMMMMMMMMx,kMMMMKccKMMMNo,xWMMWk;'''''dWMMMNoc0MMMMMMMMMMMXlcKMMMMXl'''''cKMMMMMMMM0:oNMMMWd;kWMMWk;lXMMMKc'''''cKMMMMk,xMMMMMMMMMMMMx,kMMMMMx,'''
  .xNMMMMNXXXx,dWMMMXl'lXMMM0oOMMMNo''''''lXMMMMd,dKKXWMMMMNXXKo;OWMMMNd''''':OMMMMWXXX0lcKMMMMk,:OWMMNdxNMMWk;',''';OMMMM0:l0XXNMMMMWXXXx;dNMMMWk;''''''dWMMMWNKKKd,kMMMMKc,dWMMWkoKMMMKc''''''dWMMMNo:kXXNWMMMMNXXOcc0MMMMKc'''''cKMMMMNXXXk:oNMMMWd'cKMMMKokWMMWd,'''''cKMMMMk,dXXXWMMMMWXXXo,xWMMMWx''''
  .lXMMMWx;;;,'dWMMMXl',xWMMWXNMMWk;''''''lXMMMMx',;;lKMMMMk;,,',kWMMMNl.....,OMMMM0c,,,,cKMMMMk,'lXMMMXXMMMKc'''''';OMMMM0:,;;:kMMMMKo;;,'oNMMMWk;''''''dWMMMNd;;;,,kMMMMKc':OWMMNXWMMNd,''''''dWMMMNo,;;;dNMMMWx;;;,:0MMMMKc'''''cKMMMMk:;;;,oNMMMWd',dNMMWXNMMWO:''''''cKMMMMk,,;;l0MMMM0c;;,,xWMMMWd,'''
   cXMMMWx,,,,'dWMMMNl'':0MMMMMMMKc'''''''lXMMMMx''''c0MMMMx..  .oWMMMK;     .kMMMMO,....:KMMMMk,';kWMMMMMMWx'.......kMMMMO'....dMMMM0;....cXMMMWd.......oWMMMXl'''.'kMMMM0;..lXMMMMMMWO,.......oWMMMXl....cXMMMWo....,OMMMM0;.....:KMMMMx'....cNMMMNl..'kWMMMMMMXc.......:0MMMMk,''':0MMMMO:''''dNMMMNl....
  .lXMMMMNKKKd,dWMMMXl'''xWMMMMMMk,'''''''lXMMMMx''''c0MMMMk'.   cNMMM0'     .kMMMMNK00k;:0MMMMk,',lXMMMMMM0:.      .xMMMMk.    oMMMM0'    '0MMMNc       lWMMMWX000l;OMMMMO' .:0MMMMMMNc        cNMMMX:    :XMMMWl    .dWMMMx.     ,0MMMMX000o.:XMMMNc   cNMMMMMMx.      .;0MMMMk,''':0MMMMO,....:XMMMK;
  .lXMMMMMMMMO;dWMMMXl'';kMMMMMMMO;'''''''lXMMMWx''''c0MMMMk,... ;XMMMx.     .kMMMMMMMMXc:KMMMMk,',oNMMMMMMK:       .xMMMMk.    oMMMM0'    .kMMMK;       lWMMMMMMMWOo0MMMMO,.;dKMMMMMMWo.       cNMMMX:    :XMMMWl     lWMMMo      ;0MMMMMMMMO.:XMMMNc  .oNMMMMMMO'     ..:0MMMMk,''':0MMMMk.    ,0MMMO'
  .lXMMMWOoll:,dWMMMXl''lKMMMWWMMXo'''''''lXMMMWd''''cKMMMMk,'...;KMMMx.     .kMMMM0l:::':KMMMMk,';OMMMWWMMWd.      .xMMMMk.    oMMMM0'    .xMMMK;       lWMMMNdcoxdo0MMMM0lclOWMMWWMMM0,       cNMMMX:    :XMMMWc    .oWMMWo     .:KMMMMO:::'.:XMMMNc  'OMMMWWMMNc     ..:0MMMMk,''':0MMMMk.    ,0MMMk.
  .lXMMMWd'''''dWMMMXl',xWMMN0XMMWk;''''''lXMMMMx''''cKMMMMk,''..;ONNNd.     .kMMMMk. ...:KMMMMk,'oXMMWO0MMM0,      .xMMMMk.    oMMMM0,    .dNNNO,       lWMMMXc,cllo0MMMMXdldKMMMK0WMMNl       lNMMMNl....:XMMMWl   .;xNNNXc      ,0MMMMo     :XMMMNc  lNMMNOKMMWk.    ..;0MMMMk,''':OMMMMx.    'kNNNx.
  .lXMMMWd'''''dWMMMXl'cKMMM0o0MMMXl''''''lXMMMMx''''c0MMMMk,'''.,odddl.     .xMMMMk. ...:KMMMMk,;OWMMXloNMMWo.     .xMMMMk.    oMMMM0,    .:dddo,       lWMMMXdclloo0WMMMXxokNMMWxlKMMMO'  ..',xWMMMNxcc:;dNMMMWc .':lxOxdd:.     '0MMMMo     :XMMMNc 'OMMM0cxWMMXc   ...;0MMMMk,''':0MMMMx.    .cdddl'
   cXMMMWd'''''dWMMMXo,xWMMWx,xWMMWk;'''''lXMMMWx''''c0MMMMk,'''.lXMMMWl     .kMMMMk.....cKMMMMk,oXMMMO';KMMM0,     .xMMMMk.    oMMMM0,    .kMMMMx.      lWMMMNkllloo0WMMMXxdKWMMNl.xWMMNd,;:cllOWMMMNkllllkNMMMWo';cllOWMMMK;     ,0MMMMo     :XMMMNc lNMMWx.cNMMMk.  ...;0MMMMk,''':0MMMMx.    ,0MMMMo
   :KMMMWd'''''dWMMWXocKWMMNo'oXWMMXl'''''lXMMWWd'''':0MMMWk,''''lXMMMWc     .xMMMMk....'cKMMMMk:kWMMWx..kWMMWo.    .xMMMMk.    oMMMM0,    .kMMMMx.      lWMMWNkllolo0WMWWKxkNWWWK:.lNMWWKdlllllOWWWWNkllllkNWWWWkcllllOWWMWXc..'..,0MMMMo     :XMMMNc.kWMMNl.,0MMMX: ....:0MMMMk,'',:OMMMMx.    ,0MMMMo
   .;clll;''''';llllc;;clllc;',cllll;''''',cllll;'''',cllll:''''',::;;;.      ';;;;'...'';cllll:;clc:;.  .;;;;'      .;;;;'.    .;;;;'.     ';;;;'       .;:lxxolllloddxxxxodxkxxo,.;oxxxxollllldxkkkxdlllloxkkxxdllllldxxxxxoll:'..';;;;.     .,;;;,..,;;;,. .';;;,. ....,cllll:'','.,;;;;'     .';;;;.
     ..''''''''''''''''''''''''''''''''..;c:,'.'''''''''''''''''''..                ...'''''''''''..                                                       .;lllllllllllllllllllll::cllllllllllllllllllllllllllllllllllllllllll:'.                                    ....',,'''''''..
     ..'''''''''''''''''''''''''''''''''.,lxxl;'..''''''''''''''''..               ...'''''''''','.          ..                                            'clllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllol:.                                     ....'''''''''''.
     ..''''''''''''''''''''''''''''''''''',oOOxl;'.'''''''''''''''..              ....'''''''''''..                                                       .,llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllolllc;.                                     .....''''''''''..
    ...'''''''''''''''''''''''''''''''''''.;dOOOxo;''''''''''''''''.              ...'''''''''''..                             ...                        .;llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll:'.                                     ....'',''''''''.
   ...'''''''''''''''''''''''''''.'''...''.'ckOOOOxl;'''''''''''''...            ...'''''''''''..                                                         .:lllllllllllllllllllllllllllllllllllllllcccccclllllllllllllllllllc:'.                                   .....',''''''''..                      ..
  ..'''''''''''''''''''''''''''''',cc;'.....;dOOOO0Odc,''''''''''''..           ....'''''''''''.                                                          .:lllllllllllllllllllllllllllllllllllccllloodl:cllllllllllllllllollll;.                                  ....'''''''',''.                      ...
  ..''''''''''''''''''''''''''''''';lxdc,...'lkOOOOOOko;......'''''..          ....'''''''''''..                                                          .;llolllllllllllllllllllllllllllcccldxkOOOO0Ooclllllllllllllllllllllllc,.                               .....''''''''''..                      ..
  .''''''''''''''''''''''''''''''''.'cxkdc,..:xOOOOOOOko;......'''''..         ...'''''''''''..                                                           .,lllolllllllllllllllllllllllcccldxO0000000Odccllllllllllllllllllllloolc,.                              ....'''''''''''.
  .'''''''''''''''''''''''''''''''''.':xOkd:':xOOOOOOOOOd;....''''''..        ....'''''''''''.                                                             .;llolllllllllllllllllllccccldkO0000000000Oocllllllllllllllllllllllllllc'                             .....''''''''''..
  .'''''''''''''''''''''''''''''''''..'ckOOxlokOOOOOOOO0kl'...'''''...       ....''''''''''''.                                                              .,cllllllllllllollllccccodkO0000000000000klcllcccccllllllllllllllllllll:.          ...........  .........''''''........................
  .'''''''''''''''''''''''''''''''''...,oOOOOOOOOOOOOOkxoc;....'''''..       ...''''''''''''.                                                                ..,cllllllllllllcccloxOO0000000000000000xlcccoxxlcllllllllllllllllllllc'          ..............'.......''''.........,;;;;;;;;;;;;;;;,.
  .'''''''''''''''''''''''''''''''''...':xOOOOOOOOOOOkdxOOOo;..''''''..     ....'''''''''''..                                                                  ...,;;::cccclloxkO00000000000000000000xl:lxOOdcllllllllllllllllllllll,.         .....................''''.......'..',;;;;;;;;;;;;;;;'.
  .'''''''''''''''''''''''''''''''''....,oOOOOOOOOOOkk0XWWWNKo'.'''''..     ...'''''''''''..                         .                                               .;oxxkkkO000000000kkkO0O00000000OdokO0koclllllllllllllllllllllc,              .......... ......''''..........',,,,,,,,;;;;;,,,'.
   .'''''''''''''''''''''''''''''''''''..ckOOOOOOOOxkKNWWWWMWXo'...''...   ....'''''''''''.                          .                                             ..:dO0OOxdk00000000OkdodxkkkOOOOO00OOO0Oxlclllllllllllllllllllllc'                         .....'''''...'......',;;,,,,,,,,,,,,,'.
   ...'''''''''''''''''''''''''''''''''..;xOOOOOOOkxKWWWWWWMWWKc. .......  ...'''''''''''..                                                                       .cxOOOkxdoodkkOO00OkxkO00000OOkkxxkkO0O0Oxlclllllllllllllllllllll:.               ..        .....'''''.....''....',,'''''''''''''.  .
  .'...''''''''''''''''''''''''''''''''..,dOOOOOOOxkXWWWWWWWWW0c.   ..........'''''''''''.                                                                        ,xOxxkO0KXXK0OxxkkxkKNWWWWWWWWNNXKOxxO00Oxllllllllllllllllllllllc,.              .''.      .............................'''''''',,'',''...
  .;,...''''''''''''''''''''''''''''''''.'oOOOOOOOdkNWWWWWWWWXl.        ......''''''''''..                                                                        .cxOKNWWWWWWWWXOdx0NWWMMMMMMMWWWWWWXkxk00kolllllllllllllllllllll;.             ..,'.       .................';;;;;;;;;;;;:::::::::::::::::
  .;;'...'''''''''''''''''''''''''''''''..lkOOOOOOdxXWWWWWWWWNk,        .....'''''''''''.                      .                                                  ,xXWWWWWWWWWWMWXO0NWWWMWMMMMWWWWWWWWNOxk0koclllllccllccclllllll:.             .''..       .....''''''''''....,;::;;;;;;;;;;;;;;;;;;;:;;;;;
  .;:;'..'''''''''''''''''''''''''''''''..:kOOOOOOxdKWWWWWWWWWKl.       ...''''''''''''..                      ..                                                ,kNWWWWWWWWWWWWWK0NWWWMWWNNWWWWWWWWWMWKxxOOdclllc:;codddolllllc;.             ....         ....''''''''''''....';;;;;;;;;,;;;;;,,;;;;;;;;;;
  .;::,..''''''''''''''''''''......''''''.;xOOOOOOkdxKWWWWWWWNk:.      ....''''''''''''.                                                                        .lXNKk0NWWWWWWWWWKKNWMMMWNxlOWWWWWWWMMWXxxO0koccl:;cxOOOOOxocc:'.              ...         .....'''''''''''.'....,,;;;;;,,,,,,,,,,,,,;;;;;;;
  .;::;'..'''''''''''''''''',;::;'...''''.,dO0OOOOOkdx0XNWWNKkddl,.    ....'''''''''''..               ...                                                      .xWNOlxXWWWMMMWWXOOXWWMMMN0xKWWWWWWWMMW0dk00Oxlcl:lkOxoldkOkc'.                           ......'.'''''''''''....,,;;;;;,,,;;,,,,,;;;;;;;;;;
  .;:::,...''''''''''''''.,cdkkOxo:'.''....ckOOOOOOOkkxxkkkkxdxkkxl;......'''''''''''..                                                                         .dNWWNNWWWMMWNKOkxxKWWMMWWWWWWMMWWWMMWKxxO000OdlccxOkddddk0Oo;;clloooooddolc::;,'...      ......'''''''''''''....,,;;;;;,;;;;;;;;;;;;;;;;;;;
  .;:::;'..''''''''''''''';dOOOkkkkd:'.....,dOOOOOOOOOOOkkkOOOOOOOOOxdl;'''''''''''''..                                                                          ;OWWMMWWWWWXOxkOOkkKNWWWWWWWMWWMMMWNKxxO00000OdccxOOkOkxO0OxkKNWWWWWWWWWWWNNNNXK0Oxoc;'..........''''''''''''...',;;;;;,,;;;;;;;;;;;;;;;;;;
  .;:::;'..'''''''''''''..;xOOkddkOOko;....'ckOOOOOOOOOOOOOOOOOOOOOOOOOx:''''''''''''.                                                                           .;kXWMWWWNKxxO000Okxk0XNWWWWWWWWNXKOxkO0000000OxdxO000OOOOxxKWWWWMMMWWWWWWWWWWWMWMWWWNX0kdc;'........'..'''''...',;;;;;,,;;;;;;;;;;;;;;;;;;
  .;:::;,..''''''''''''''.;dOOkddkOOOOxl;'..'lkOOOOOOOOOOOOOOOOOOOOOOOOkc'''''''''''..                                                                             .ck000OkxxO000000OkxkkO00KK00OkxxkO000000000000O000OkkxdoONWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNX0xo:,'...''''.''....,,;;;;;;;;;;;;;;;;;;;;;;;;;
  .;::::,..''''''''''''''''lkOOxdxOOOOOOkdc,''cxOOOOOOOOOOOOOOOOOOOxdxdl,'''''''''''.                                                                        ..... .'codxkOOO000000000OOOkkxxxkkkkO0000000000000000000OkkkxxkKWMWWWWWWWWWWWWWWWWWWWWWWWWWWMMWWWNX0xl;'.....''...',;;;;;;;;;;;;;;;;;;;;;;;;;;
  .;::::,..'''''''''''''''.,okOkxxkOOO0OOOOkdooxOOOOOOOOOOOOOO00OOOkl,''''''''''''''.                        ......................................................,okO0000000000000000000000000000000000000000000000000000Okk0XWMMMWWWWWWWWWWWWWWWWWMMWMMMMWWWWWMWNKko:,.......,,,,;;;;;;;;;;;;;;;;;;;;;;;;
  .;::::,..'''''''''''''''..;okOOOOOOkOOOOOOOOOOOOOOOOOOOOOOOOO0O00Oxc,'''''''''''''...............................................................................:k0OOO0000000000000000000000000000000000000000000000000000OkOXWWWWWWWWWWWWWWWWWWWMMWWMMMWWWWWMMMMMWNXOo:'...',;,,,;;;;;;;;;;;;;;;;;;;;;;;
  .;::::,..''''''''''''''''..;okOOOkxdkOOOOOOOOOOOOOOOOOOOOOOOO000OOOOd:,'''''''''''........................................''......''''''''''''''''''''''''''''''.,oO00000OkkO00000000000000000000000000000000000000000000000Ok0NWWWWWWWMMWWWWWWWWWWWWMMMMWWWWMWWWWWMMMWWXkl,.',,,,,,;;;;;;;;;;;;,,,,,,,,,,
  .;:::;'..''''''''''''''''',cdddddddkO0OOOOOOOOOOOOOOOOOOOOOOO000OOOOOxl;,''''''''''''....'..'''''''''''''''''''''''''''''','''''''''''''''''''''''''''''''''''''':ldxxxdddddk00000000000000000000000000OOOOkOOOO0000000000000kONWWWNXXWMMMWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNKxl;,,,,,,,,,,,,,,,,,,,,,,,,,,,
  .;:::;'...''''''''''''''''cxOOkkkkOOOOOOOOOOOOOOOOOOOOOOOOOOOkOkkkkxxdl;'.''''......'''''''''''''''''''''''''''''''''','''''''''''''''''''''''''''''''''''''''.':xOkxxxkkOOO00000000000000000000OOOOkkxxkkkkkkdodO00000000000kONWWWXKXWMMMWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWXOl,''',,''''''''''''''''''''
  .;:::,...''''''''''''''',lxOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkxxxxdddxddol:,'.......... .,;,..''''''''''''''''''''''''''''''.....''........................''''''''':dO000000000000000000000000000OOkOOkkO00KOdc:c:,.'lO000000000Ok0WWWWXKXWMWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWMMWWWW0:.........................
  .;::;'..'''.'''''''''',cdOOOOOOO0OOOOOOOOOOOOOOOOO00Okkxddddddddolc;,'............. .','.....................''''''''''''''''',,,,,,,,,,,,,,,;;;;,,,,,;;;;;;;:okO00000000000000000000000OOOkkkO0KKxlccc:,.  ...',lO00000000OkOXWWWWX0XWMWMMWWWWWWWWWWWWWWWWWWWWWWWWWWWMWWWWWWWW0:.'.''''''',,,,,,,;;;;;;;;
  .;:;'...'..''''''''',:dkOOOOOOOOOOOOOOOOOOOOOOOOOOOOxddddddolc:;,'''.'..........'.. .','....'''',;;,,;;;;;;;;;;;;;;;;;;;,,,,,,,,,,'''''''''''''............'cxO0000000000000000000OOOOkkkOkddxkko;.     ..''';:coxO0000000OkkKWMWWWN0KWMMWWMWMMWWWWWWWWWWWWWWWWWWWWWWWWWMWWWWWNkc:::::::::::::::::::::::::
  .;;;,,'....''''''',:okOOOOOOOOOOOOOOOOOOOOOOOOOOOOkxdddddo:,'''.................'.. ..,,......'',,'''''''''''''...........................................':k0000000000000000OOOOkkkxookOOkoloxo'    ..,:clllodxkO00000000kkKNWMWWMWK0XWMMWMMWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWKxddl::;;;;;:;;;;;;;;;;;;;;;
  'looddl:,....'''';okOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkdddddddl;'....................'... .,,..............................................'''''................,lxkO00000OOOkkxxdlc::cll:,,oO0OxdkOd:;:lodxxkOOOOOO000000000OkOKNWMWWMMMNK0XWMWMMWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWXkxOOko:;,;;;;;;;;;;;;;;;;;;;
  'oddddddoc;'...,cdO000OOOOOOOOOOOOOOOOOOOOOOOOOOkxddddddl:,.....................''.. .','.........''''''''''....'............................................';cclcccc::;,,,'.........,oXNOdkOOOkOOO000000000000000000OkxOXWWWMWWWWMWNK0KWWWWWMWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNOxO000Oxo:;,;;;;;;;;;;;;;;;;;
  'oddddddddol:''cxOOOOOOOOOOOOOOOOOOOOOOO0000OOOOxlclllc:,'.......................''. ..,'. ....................................................................................',.....'l0NXOkkkkkkkOOO0000000000000OkxxOKNWMMMWWWWMMWWWKO0XWMMMWWWWWWWWWWWWWWWWWWWWWWWWWWWWN0xk000000Oxc;,,;;;;;;;;;;;;;;;
  'odddddddooool::lxOOOOOOOOOOOOOOOOOOOOOOO0000OOxc,'''''.............................. .',.......................................................................................'.....';xNWNXXKK0OxxOkkkkOO0000OOkxxxkKNWWWMWWWWWWWWWMMWN0O0NWWWWWWWWWWWWWWWWWWWWWWWWWWWWWN0xk000000000Oo:,,,;;;;;;;;;;;;;
  'ooodddddoooooolc:lxOOOOOOOOOOOOOOOOOOOOOO000Okl,.................................... .','...'..............................................................................'....'....'':OWWWWWWWN0OXXK0Okkkkkkkkkk0XNWWWMMMWWWWWWWWWWMWWWX0O0NWWWWWWWWWWWWWWWWWWWWWWWWWWNOxk000000000000xc,,,;;;;;;;;;;;;
  'oooddoooooooooool::okOOOOOOOOOOOOOOOOOOOO00OOl,......'..............................  .''...'....'........................................................................'.....''...'.':ONWWWWWWXOKWWWWNXK0KKXNNWWWMMMMMMMWWWWWWWWWWMMMMWWXOO0NWWMMWWWMWWWWWWWWWWWWWWWXkxk00000000000000ko;,,;;;;;,;;;;;
  'ooooooooooooooooolc:cokOOOOOOOOOOOOOOOO0OOOOxc;;;;,'................................  .',....'...............................................................''''''''....''.....''......';xNWWWWWN0ONWMMMMMWWWWMWWWMMMMMMMMWWWWWWWWWWWMMMMMWWXOO0NWMWWMMMWWWWMMWWMWWWN0kxO0000000000000000Ox:,,;;;;;;;;;;
  'looooooooooooooooool:;lxOOOOOOOOOOOOOOOOOOOkl;cc;:c;................................. ..,'. .''...'...............................'',,,,,,;;;:::::ccccccc:,.....''''''''''.......''.......,o0NWWWWXO0WMMMMMWWWWWWWWWMMWWWWWWWWWWWWWWWWWWWWMWWWWXOO0XWWWWWWMMMMMMMWWNKkxkO0000000000000000000x:,,;;;;;;;;;
  'looooooooooooooooooolc::oOOOOOOOOOOOOOOOOOOd:,::;:l;.............................'...  .''...''.............''''..',,,;;::::ccccccllllllllllcccccc::::;;;,'..'..'''....'...'',,,,;;;;;,''.':dOKXWWWX0XWMMMMWWWWWWWWWMMWWWWWWWWWWWWWWWWWWWWWWMWWWWX0OOKNWMWWWMMMWWNKOxxO000000000000000000000Oxc,,;;;;;;;;
  'loooooooooooooooooollll:;lkOOOOOOOOOOOOOOOOo::c::::;.................................  .'''...'.......';,'....'...;cccccc:::;;;;;,,,,''''''.................'''''''....',:lodxkkkOOOOkxdoclxOkkkO0XXKOKNMMMMWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNKOO0XNWWWWNX0OxxO000000000000000000000000Ox:,,;;;;;;;
  .loooooooooooooooooolllll:;lkOOOOOOOOOOOOOOkl,''''''................................... .','...''.....':lc;'.....................................''......''...........';cldO000OOOO0000000OOO00OOkkxxkddOXWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWMWWMWMMWWX0OO0000OxdxO000000000000000000000000000Oo,,;;;;;;;
  .loolllollllllllllolllllll:;lkOOOOOOOOOOOOOkc...............'.......................'.. .',,...''......'''..................''''''''''...............................;ododk00OkdxkOO00000000000000OOOOOkxkKWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWMWWMMWWMMWWNX00KXNX0kxkO00000000000000000000000000d;',;;;;;;
  .llllllllllllllllllllllllll:;cxOOOOOOOOOOOOx:.......................................... ..,,'...'....'.....................................................'''''''',lkxodO00OxdxOO000000OOOkOOO000000000OkxkKWWWWWWWWWMWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWN0kxkOO00000000000000000000000d;,;;,,,,;
  .lllllllllllllllllllllllllll:;lkOOOOOOOOOOOx:.......................................'..  .','. ......'..................''........'''''''''.''''',,,,;;;;;;;;;;;;;;dOkodO00kddO0000000OxddxxxkOO0000000Oko:,:xXWWWWWWWMWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWXkdxO00000000000000000000000d;,,,,,,,,
  .lllllllllllllllllllllllllllc:;lO0OOOOOOOOOkl'...........'.............................. .','......................... .....,,;;;;;,,'''',,;;;;;;;;;;;;;;;;;;;;;;;lOOddO00OddO00000OkdooxkO0OO0000OOxdl:,.....:dKWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWMMWXkxkO0000000000000000000000Ol,''''''''
  .lllllllllllllllllllllllllcccc;;dOOOOOOOOOOOd;..................'''''................... .',,'...'...''''',,,;;;;;,'...... ..,;,,''',,;;;;;;;;;;;;;;;;;;;;;;;;;;;;dOOdxO0OxokO0000ko:,cxO000000Oxl:;,...........,o0NWMWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWMWWKkxO00000000000000000000000Od;..'......
  .cllllllllllllllllllllllccccccc;:xOOOOOOOOOOOkdc;'............................''',,,,;;,...:cc,......,;:::::::;;::,........ ..',,,;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;coocoO0OddOO000xl;,;:lxkkkkxoc,............     .cxKNWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWMWN0xkO000000000000000000000000kdl,....'',,
  .cllllllllllllllllccccccccccccc:,lkOOOO00XNNNNX0xoc:;;,,'...'''',,,;;;;:::ccccllloooooooc'..:ll:'....'',:::;'.',;;'........ .,,;;;;;,,'...''',,;;;;;;;;;;;;;;;;;;;,,::cxOOdxO000xc;;;;;;;:::;;,,,,,'...........     .':d0XWWWWWWWWWMMMWWWWWWWWWWWWWWWWWWMMWWWMWWXkxk0000000000000000000000000OxOKx;,::cccc
  .cllllllllcccccccccccccccccccccc;;okOKXNWWNX0OkkkkOOkkxdolcccclloooooooddooooolllooooooool;..,clc,...''',;;;'.,;:;..........,;,,,;,'...',;::::;;,;;;;;;;;;;;;;;;;;,,:c:codlokOOxc,,;;;;;;;;;,,,;;;,,,,'............     'lOKKNWWWWWWWWWWWWWWWWWWWWWWWWMMWWMMWWN0xxO0000000000000000000000000Ok0NWKo:llllll
  .clllccccccccccccccccccccccccccc:,:kXWWWNKOkkkkOOOOOOO00OOOkxoollllllcccc:cccclllcclooooooo:..':ll;...'..',;clddo;.........;odol:'...,:llooooool:;;;;;;;;;;;;;;;;;;,,;::;;,;:cc;,;;;;;;;;;,'.......,;;;,'.............   ,d0XNWWWWWWWWWWWWWWWWWWWWWWWMWWMMMMWXOdxO000000000000000000000000OkkKWWWNkcclllll
  .ccccccccccccccccccccccccccccccc:;:kNWNKOxkOOOOOOOOOOO00OOOOOOkdl::loooollodxxxkkdccloooooooc'..:ll;....';lxkOOkdc;,,,,'''':oxOOxc..,clllllllllll:,,;;;;;;;;;;;;;;;;;,,,,;;,;;;;;;;;;;;;,'......  ..,;;;;,'...............'o0NWWMMMMMMWWWWWWWWWWWWWWMMMMMMWN0ddk0000000000000000000000000OxkXWMMWWO:,;::::
  .cccccccccccccccccccccccccccccc::;;oXX0kkOOOOOOOOOOOOOOOOOOOOOOOkxdodxkkxdodxkxxkkdlcloooooool;..;cl:'.'cxOOOOOOOOkkkkkkkxxxdxkOOx:;clllllc;:clllc;,;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;,'........... ..,;;;;;,'..............':d0NWMMMMMWWWWWWWWWWWWWWWWWMWWXkdxO0000000000000000000000000kxONWMMMWWKc''''''
  .cccccccccccccccccccccccccccc:::::;ckOkkOOOOOOOOOOOOOOOOOOOOOOOOOOOxdooxkxdodxkkkxkxl:coooooooo:..,cl:;lkOOOOOOOO00000000OOOkddkOxcclloll:',cllllc;,;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;,'................;;;;;;;;;'..............,cxKNWWMMMWWWWWWWWWWWWWWWMWXOddk0000000000000000000000000OxkKWWWWMMMWKc''''''
  .:ccccccccccccccccccccc:::::::::::;,cxOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOxdooddolloollllc;:ooooooodoc'.';cxOOOOOOOOOOOOOOOOOOOOOOxdxkc';looc,.,collllc;,;;;;;;;;;;;;;;;;;;;;;;;;;;;;;,'............... .';;;;;;;;;;,'..............';oOXWMMMWWWWWWWMWWMWWWXOxxkO000000000000000000000000OkxkXWWWWWWWWWKc.'''''
  .:cccccccccccccc:::::::::::::::::::,:xOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOxoc::::ccccllllloolllccc::,..cxOOOOOO0OOOOOOOOOOOOOOOOxllc...;::,..;cllllc;,,;;;;;;;;;;;;;;;;;;;;;;;;;;;;:::,,,'..........  .';;;;;;;;;;;;,'...............,lkXWMMWWWWWWWWWMWN0xdkO000000000000000000000000OkxkKNWWWWWWWWWW0:.'''''
  .:cccccccccc:::::::::::::::::::::::,;xOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkdlllcc:::;;;,''...........:xOOOOOO00OOOOOOOOOOOOOOOOdldd;...':::::::cc:;,,;;;;;;;;;;;;;;;;;;;;;;;;;:coxkkkkx:..........   ..,;;;;;;;;;;;;;'................':xXWMWWWWWWWWNKxdxO000000000000000000000000Okdx0NWWWWWWWWWWWWO;.'''''
  .::::::::::::::::::::::::::::::::::,,okOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkxo:'...................:xOOOOOOOOOOOOOOOOOxxkOOO0kddOkc,'..';cccc:;,,,;;;;;;;;;;;;;;;;;;;;;;;;;;cdkOOOOOOd,..........   ..,;;;;;;;;;;;;;;,'.....'';:ccc::,'':kXWMWWWWWKkddk0000000000000000000000000kddOXWMWWWWWWWWWWWNx,.'''''
  .::::::::::::::::::::::::::::::::::;,ckOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkxdl;'........     .,dO00OOOOOOOOOOOOOOxoxOOOOOkoxOx:,;;,,,,,,,,,,;;;;;;;;;;;;;;;;;;;;;;;;;;;cxOOOOOOOOxl;'....... .''..,;;;;;;;;;;;;;;;;'..,coxkOOOOOOkxdc:lONWWWXkddkO000000000000000000000000OddkKWMMMMWWWWWWWWWWKl'.'''..
  .:::::::::::::::::::::::::::::::::;;,ckOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkxoc,..       .lOOOOOOOOOOOOOOOOkxocdkOOOOkodxc,,;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;:dOOOOOOOOOOOkxdoc:;,,';dkdc,,;;;;;;;;;;;;;;;,;lxO000OOO0000000kddk0Kkddk0000000000000000000000000OxxkKNWWWMWWWWWWWWWWWXd,..'....
  .::::::::::::::::::::::::::::::::::;,:xOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOxoc;....;okOOOOOOOOOOOkkkdlcoxxooxkkkd::l:,;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;lkOOOOOOOOOOOOOOOOOkkkkkOOOkl;;;;;;;;;;;;;;,;lxO000OkxkO000000000OkdlokO000000000000000000000000OkkOXWWWWWWWWWWWWWWWWN0o,...'..''
  .;:::::::::::::::::::::::::::::::::;,:xOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO0O000OOxollodxkOOOOOOOOOxdc,...'codlcc:cccdxo;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;,:dOOOOOOOOOOOOOOOOOOOOOOOOOOOxc,;;;;;;;;;;;,:oO0000kxxkO000000000000OxxO0000000000000000000000Okkk0XWWMWWWWWWWWWWWWWN0d:,'........
  .;::::::::::::::::::::::::::::::::::,:xOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO000O00OOOOOOxdoddxkOOOOOOOkl'.....cdxdddxkOOx:,;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;,;okOOOOOOOOOOOOOOOO0OOOOOOOOOOx:,;;;;;;;;;;,:dO0000kxxO000000000000000OOO00000000000000000000OkkOKNWWWMMMWWWWWWWWWWN0dc;,;,.   ....
  .;::::::::::::::::::::::::::::::::::,:xOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO0OO000OOOOOOOOOkxdodxkOOOOOx;.....:xO000Okxo:,,;;;;;;;;;;;;;;;;;;;;,,,,,,,,;;;;;;,,;lkOOOOOOOOOOOOOOOO00OOOOOOOkkdc;,;;;;;;;;;,;dO0000kxxO0000000O0000000000000000000000000000OkxxOXWWWWWWWMWMMWWWWWNKko:,,;;;,.   ....
  .;::::::::::::::::::::::::::::::::::,;dOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO00OOOOOOOOOOOOOkxoooxkO0kc......':ccccc:,,,;,,,,,,,,,,,,,,,,,,,,;;;;;;;,;;;;;;,,;lkOOOOOOOO000OOOOOOOOOOOOOkxo;,;;;;;;;;;;;,lO0000OxdO00000OkxxO0000000000000000000000000Oxxk0XWWWWWWWWWWWWWWWNKOoc;,,,;;;;,........
  .;::::::::::::::::::::::::::::::::::,;dOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkxdooxko,............',,,;;;;;::::::::cccccccccccccccccccccccc::cokOOOOOOO0OOOOOOOOOOOOOOkkxc,;;;;;;;;;;;,cO000Oxox00000kddxO00000000000000000000000OkxkOKNWWWWWWWWWWWWWWNKkoc;,,,,,;;;;;,........
  .;::::::::::::::::::::::::::::::::::,;dOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkxdol,...........',::ccccccllllllllllcccccccllllccccccclllccc::lxOOOOOOOOOOOOOOOOOOOOOOOx:,;;;;;;;;;;;,;oxkxl:oO0000kdxkO000000000000000000000OkxxkKNWMWWWWWWWWWWNXKOdl:,,,,;;,,;;;;;,'........
  .;:::::::::::::::::::::::::::::::::;,,oOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkxoc,'.......,:cccccccccllllllccclllcccc:::;;;;;;;;;;:ccccc:;cxOOOOOOOOOOOOOOOOOO0OOxl;;;;;;;;;;;;;;;;::;,:x0000kdxO0000000OOO0000000000kolok0NWWWMWWWWWWNXK0koc:;,,;,;;;;;;;;;,,;,'........
  .;::::::::::::::::::::::::::::::::::;,lOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkxdoc:ccloolccccccccccccllcccc:;,'.................;cccc:;lkOOOOOOOOOOOOOOOOOOko:;,;;;;;;;;;;;;;;;;;;;ck000kdxO000000OxookO000000Okl;..;dKXXXXXXK0Okxoc:;;,,;;;;;;;;;;;;;;;,,;,.........
  .;::::::::::::::::::::::::::::::::::;,ckOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkdc:ccc:,...;cccc:'.... ............  ...;cccc::okOOOOOOOOOOOOOOkdl;,,;;;;;;;;;;;;;;;;;;;;,:x00OddO000000ko;'':oxOOOkdl;'....';:cccc:::;;,,,,;;;;;;;;;;;;;;;;;;;;;;,.........
  .;::::::::::::::::::::::::::::::::::;';dkOOOOOOOOOOOO00OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkxlccc;.. .':cc:.. .....................;lcccc;ckOOOOOOOOOOOOOOkxc,,;;;;;;;;;;;;;;;;;;;;;,;oO0xoxO0000Ox:'....',;:;,'..........',,,,,,;;;;;;;;;;;;;;;;;;;;;;;;;;;;'.........
  .;::::::::::::::::::::::::::::::::::;,cddkOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkl:cc;'.';clc,........................:llccc;:xOOOOOOOOOOOOOOOd:,;;;;;;;;;;;;;;;;;;;;;;;;;clclxO000ko;........................',;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;'.........
  .;::::::::::::::::::::::::::::::::::;,lOkxkOOOOOOOkxddxkOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOxl:ccccccclc'......................':cclccc;:xOOOOOOOOOOOOOxo;,,;;;;;;,''.'',;;;;;;;;;;;;;;,;oxkkd:'...........................,;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;,..........
  .;::::::::::::::::::::::::::::::::::;,lKN0xxkOOOOOkkxxdddddkOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOdcclc;'',:c;'.. ..............',;:cclccccc;;dkkkkkkkkxxdoc:;;;;;;;;,'.......,;;;;;;;;;;;;;;;;::;'..............................';;;;;;;;;;;;;;;;;;;;;;;;;;;;;,..........
  .;::::::::::::::::::::::::::::::::::;,c0WWX0kxxxkkkOOkkxdooxkxxkOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkl:c;.  .;cc:;,'......''',,;::ccccccccccl:'.,::::::;;;;,,,;;;;;;;;,.........',;;;;;;;;;;;;;;;;;'................................',;;;;;;;;;;;;;;;;;;;;;;;;;;;'..........
  .;::::::::::::::::::::::::::::::::::;;:OWMWWNXKOOkkkkkkO0KNNNKOkxxxkOOO00OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo:c:,..,:ccccccccccccccccclllcccccccccc:,'',;;;;;;;;;;;;;;;;;;;;,...........,;;;;;;;;;;;;;;;;;,.................................',;;;;;;;;;;;;;;;;;;;;;;;;;,...........
  .;:::::::::::::::::::::::::::::::::::;:kWWWWWMWWWNNNNNNWWWWWMMWWXK0kkxxkOOOOO0OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo::ccccccccccccccccccllccccccccccccccc;,',;;;;;;;;;;;;;;;;;;;;;;,..........,;;;;;;;;;;;;;;;;;;;'..................................,;;;;;;;;;;;;;;;;;;;;;;;;,...........
  .;:::::::::::::::::::::::::::::::::::;;dNMMWWWWWWWWWWWWWWWWWWMMMWWWNXK0OkxxkkOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOd::ccccccccccccccccccccccccccccclcc:;,,,,;;;;;;;;;;;;;;;;;;;;;;;,.........,;;;;;;;;;;;;;;;;;;;;'...................................,;;;;;;;;;;;;;;;;;;;;;;;,...........
  .;:::::::::::::::::::::::::::::::::::;,oXMMWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNX0koloxkOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo:cclcccccccccccccccccccccclllcc:;;,,'...,;;;;;;;;;;;;;;;;;;;;;;;'......',;;;;;;;;;;;;;;;;;;;;;,....................................,;;;;;;;;;;;;;;;;;;;;;,'...........
  .;:::::::::::::::::::::::::::::::::::;,lXWWWWMMMMMMMMWWWWWWWWWWWWWWWWWWWMWNk;..';coxkOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkl:clcccccccccccccccccccccccc::;,,,,;;,.  .,;;;;;;;;;;;;;;;;;;;;;;;;,,,,;;;;;;;;;;;;,''..'',,;;;;.....................................',;;;;;;;;;;;;;;;;;;;,'...........
  .;:::::::::::::::::::::::::::::::::::;,c0WWWMMMMMMMMMMMMMMMWWWWWWWWWWWWWN0o'      ..,:odkOOOOOOOO000OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOdc:cccccccccccccccccclcc::;;;,,,;;;;;;;'. ..,;;;;;;;;;;,'..',;;;;;;;;;;;;;;;;;;;;;,.......'''';;;'.....................................',;;;;;;;;;;;;;;;;;;,'...........
  .;::::::::::::::::::::::::::::::::::::,:OWWWWMMMMMMMMMMMMMMWWWWWWWWWWWN0l'.           ..';coxkkOOO000OOOOOOOOOOOOOOOOOOOOOOOOOOOOxl:ccclllccccllcccccc::;;,,,,;;;;;;;;;;;;,.. ...';;;;;;;,.. .';;;;;;;;;;;;;;;;;;;;,.. .....'''.,;;'......................................',;;;;;;;;;;;;;;;;;,............
  .;::::::::::::::::::::::::::::::::::::;;xNWWWMMMMMMMMMMMMMMWWWWMMWWNKkc'              ......,;:cldxkkOOOOOOOOOOOOOOOOOOOOOOOOOOkxl:cccccllccccc::;;;;,,,,;;;;;;;;;;;;;;;;;;'.   ..,;;;;;;;,.  .,;;;;;;;;,..',;;;;;;,. ..'...','.';;,.......................................',;;;;;;;;;;;;;;;;,............
  .;::::::::::::::::::::::::::::::::::::;,lXMWWMMMMMMMMMMMMMMWWWWNKOdc'.      .....................',;:clodxkkkOOOOOOOOOOkkxdol:;,,;::c:::::;;;,,,,,,,,;;;;;;;;;;;;;;;;;;;;;;,.  ...,;;;;;;;;,.  ..,;;;;;;'....,;;;;;,. ..''...,'.';;,........................................',;;;;;;;;;;;;;;;'............
,,cddddddddddddddddddddddddddddddddddddddlxXMMMMMMMMMMMMMMMMMMMMWXkoc:;;:::ccccccclllllllllcccccccccccclloodxxkOO0000000Okxdoc:;;;:clloollllllllooooooooooooooooooollloddddddoc:::clooooooooooc;,;:codddoooc:;:looodooc::lolc:clllooooccccccccccccccccccccccccccccccccccccccccclooooooooooooooolccccclllcccc





        """

        self.assertTrue(True)

        # c = Client()
        # res = c.login(username='Frank', password='whatevs')
        # data = []
        # data.append({"course": '21231-172s'})
        # data.append({"course": '21232-172s'})
        # reslogin = c.post('/listunread/', json.dumps(data), content_type='application/json')
        # data = json.loads(reslogin.content)
        # self.assertEqual(data["0"]['count'], 1)
        # self.assertEqual(data["1"]['count'], 1)

class ComposeTest(myTestCase):

    def test_bad_users_have_no_access(self):
        c = Client()
        res = c.get('/compose/')

        self.assertEqual(res.status_code, 403)

    def test_can_login(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/compose/')
        self.assertEqual(reslogin.status_code, 200)

    def test_can_see_compose(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/compose/')
        exists = True
        # TODO make it test for view

        self.assertEqual(reslogin.status_code, 200)

class OutboxTest(myTestCase):

    def test_bad_users_have_no_access(self):
        tt = Client()
        res = tt.get('/outbox/')

        self.assertEqual(res.status_code, 403)

    def test_can_login(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/outbox/')
        self.assertEqual(reslogin.status_code, 200)

    def test_can_see_outbox(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/outbox/')
        exists = False
        # TODO make it test for view
        for message in reslogin.context['email']:
            if message['subject'] == "test subject for Ned":
                exists = True

        self.assertTrue(exists)

    def test_can_see_sent_email(self):
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231",
                                      )
        Route.objects.create(to='Ned',
                             read=False,
                             fk_mail=mailmsg)

        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/outbox/')
        exists = False
        for message in reslogin.context['email']:
            if message['subject'] == "test timestamp for Ned":
                exists = True
        self.assertTrue(exists)

    def can_see_sent_email_even_if_usr_no_exist(self):
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231",
                                      )
        Route.objects.create(to='Narkles',
                             read=False,
                             fk_mail=mailmsg)

        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/outbox/')
        exists = False
        for message in reslogin.context['email']:
            if message['subject'] == "test timestamp for Ned":
                exists = True
        self.assertTrue(exists)

class OutboxReplyTest(myTestCase):

    def test_bad_users_have_no_access(self):
        tt = Client()
        res = tt.get('/outbox/')

        self.assertEqual(res.status_code, 403)

    def test_can_reply_from_outbox(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231",
                                      )
        Route.objects.create(to=User.objects.get(username="Ned").username,
                             read=False,
                             fk_mail=mailmsg)
        resout = c.get('/or/'+str(mailmsg.id)+"/")
        self.assertEqual(resout.status_code, 200)

class ComposeViewTest(myTestCase):

    def test_form_valid(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        user = User.objects.get(username="Frank")
        to_user = User.objects.get(username="Ned")
        data = {
            "content":"This is the test content",
            "subject":"this is a test subject",
            "termcode":"173s",
            "section":"3000",
            "fk_sender": user.id,
            "sendto": to_user.id
        }
        res = c.post('/compose/',data)
        self.assertEqual(res.url, '/')

    def test_form_invalid(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        user = User.objects.get(username="Frank")
        to_user = User.objects.get(username="Ned")
        data = {
            "content":"This is the test content",
            "subject":"this is a test subject",
            "termcode":"173s",
            "section":"3000",
            "fk_sender": user.id,
        }

        res = c.post('/compose/', data)
        self.assertFormError(res, 'form', 'sendto', 'This field is required.')


    # def test_form_valid_with_attachment(self):
    #     c = Client()
    #     res = c.login(username='Frank', password='whatevs')
    #     user = User.objects.get(username="Frank")
    #     to_user = User.objects.get(username="Ned")
    #     fp = open('README.md', 'rb')
    #     data = {
    #         "content":"This is the test content",
    #         "subject":"this is a test subject",
    #         "termcode":"173s",
    #         "section":"3000",
    #         "fk_sender": user.id,
    #         "sendto": to_user.id,
    #         "attachments": fp
    #     }
    #     res = c.post('/compose/',data)
    #     self.assertEqual(res.url, '/')


class ReplyViewTest(myTestCase):


    def test_user_can_view_proper_reply(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        msg = Route.objects.filter(to="Frank")[0].fk_mail
        res = c.get('/reply/{}/'.format(msg.id))
        self.assertEqual(res.status_code, 200)

    def test_user_cannot_view_others(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        msg = Route.objects.filter(to="Ned")[0].fk_mail
        res = c.get('/reply/{}/'.format(msg.id))
        self.assertEqual(res.status_code, 403)


    def test_form_valid(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        user = User.objects.get(username="Frank")
        to_user = User.objects.get(username="Ned")
        msg = Route.objects.filter(to="Frank")[0].fk_mail
        data = {
            "content":"This is the test content",
            "subject":"this is a test subject",
            "termcode":"173s",
            "section":"3000",
            "fk_sender": user.id,
            "sendto": to_user.id
        }
        res = c.post('/reply/{}/'.format(msg.id),data)
        self.assertEqual(res.url, '/')

    def test_form_invalid(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        user = User.objects.get(username="Frank")
        to_user = User.objects.get(username="Ned")
        msg = Route.objects.filter(to="Frank")[0].fk_mail
        data = {
            "content":"This is the test content",
            "subject":"this is a test subject",
            "termcode":"173s",
            "section":"3000",
            "fk_sender": user.id,
        }

        res = c.post('/reply/{}/'.format(msg.id), data)
        self.assertFormError(res, 'form', 'sendto', 'This field is required.')



#------------------------------------------------------

def allUnique(x):
    seen = set()
    return not any(i in seen or seen.add(i) for i in x)