from mailersend import emails
import base64
import io
import urllib.request



def reset_password_email(token, name, email_address):
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNDY5MmE3ODBmOTZlOGQ0ZTVlNmQ0ZmZkMjM4ODliMmRkYTAxMDFhYWY2ZGI1YjZjZDUxYjI1ODIwNDYwZGI1YzFjYTJmZTQ3ZmZjOTFhNmYiLCJpYXQiOjE2NzAwMDk3OTQuNjc0NTgyLCJuYmYiOjE2NzAwMDk3OTQuNjc0NTg0LCJleHAiOjQ4MjU2ODMzOTQuNjcwNjAyLCJzdWIiOiIzMTgzMCIsInNjb3BlcyI6WyJlbWFpbF9mdWxsIiwiZG9tYWluc19mdWxsIiwiYWN0aXZpdHlfZnVsbCIsImFuYWx5dGljc19mdWxsIiwidG9rZW5zX2Z1bGwiLCJ3ZWJob29rc19mdWxsIiwidGVtcGxhdGVzX2Z1bGwiLCJzdXBwcmVzc2lvbnNfZnVsbCIsInNtc19mdWxsIiwiZW1haWxfdmVyaWZpY2F0aW9uX2Z1bGwiXX0.TfkGaBYmYL35MwhCqnXopTs06LtxeaX_WREqQPOub2AIbbD91Mz37BprpokFq1q3mbdyAEMDRMgG-8o6YDRAQdIyXV2O-PKB9ty8MKQvrJpNHrqyj22f45t4l-0ecuwku8uAEAyPD_4M3l4uSd2ykPYllWHaiVukyoOmguwZfv3ynt07XMOyuo5JjUNA2_0c-jE-aePCL56Rik37XJpwADyiYgfqLMKmNWd7QIci7qqHM19pIzU3RSfaP5HeilxMtPdzcAAjr9kqTRPyLPo4ym5E7ACL1jhRiLO60EPAco6efxsPdBlnxleLynvK76PlT-qaV3-MoNeL-nYzJUkhMMIMkPsCwmFDePfhZgvJar9s1JY5UR_F51XkP5DCQY7xvbVGJHpNn1Yo5Ih7m1DbQyYAj_a_VB0jZP709KfkPPRzIb9n5qmZclLjk5sOtsd88vDQZ-4xdExHbX6jX7bdlo8TzA600CPF2-ok-qcDLI9xZ7nBjv7YwobopXwYfnMM1ejFBaOg_7J6OzSlNLhpU-RQ-zhzeCqIOEwAUVGL7_IRiMVPe60gGI6UaXjVxtYqkz5HE5MVXIkG4THXI1JEBdpJ27TVYJJQ_sRZ9mOMqat8VxfmcVzX3rXXV7KyujSmwJzLq94wRbc6VFHgiZQo7xhnOlozZEIJcdeK3KnqSb8"
    mailer = emails.NewEmail(api_key)

    # define an empty dict to populate with mail values
    mail_body = {}

    mail_from = {
        "name": "HAYAK",
        "email": "info@hayaksa.com",
    }

    recipients = [
        {
            "name": "name",
            "email": email_address,
        }
    ]

    variables = [
        {
            "email": email_address,
            "substitutions": [
                {
                    "var": "name",
                    "value": name
                },
                {
                    "var": "token",
                    "value": token
                }
            ]
        }
    ]

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject("HAYAK | Reset Password", mail_body)
    mailer.set_template("zr6ke4n12eegon12", mail_body)
    mailer.set_simple_personalization(variables, mail_body)

    print(mailer.send(mail_body))




def invitation_email(name, email, event_name, event_date, event_location, qr_code, event_venue, event_city, event_logo, client_name, entries, invitation_type):
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNDY5MmE3ODBmOTZlOGQ0ZTVlNmQ0ZmZkMjM4ODliMmRkYTAxMDFhYWY2ZGI1YjZjZDUxYjI1ODIwNDYwZGI1YzFjYTJmZTQ3ZmZjOTFhNmYiLCJpYXQiOjE2NzAwMDk3OTQuNjc0NTgyLCJuYmYiOjE2NzAwMDk3OTQuNjc0NTg0LCJleHAiOjQ4MjU2ODMzOTQuNjcwNjAyLCJzdWIiOiIzMTgzMCIsInNjb3BlcyI6WyJlbWFpbF9mdWxsIiwiZG9tYWluc19mdWxsIiwiYWN0aXZpdHlfZnVsbCIsImFuYWx5dGljc19mdWxsIiwidG9rZW5zX2Z1bGwiLCJ3ZWJob29rc19mdWxsIiwidGVtcGxhdGVzX2Z1bGwiLCJzdXBwcmVzc2lvbnNfZnVsbCIsInNtc19mdWxsIiwiZW1haWxfdmVyaWZpY2F0aW9uX2Z1bGwiXX0.TfkGaBYmYL35MwhCqnXopTs06LtxeaX_WREqQPOub2AIbbD91Mz37BprpokFq1q3mbdyAEMDRMgG-8o6YDRAQdIyXV2O-PKB9ty8MKQvrJpNHrqyj22f45t4l-0ecuwku8uAEAyPD_4M3l4uSd2ykPYllWHaiVukyoOmguwZfv3ynt07XMOyuo5JjUNA2_0c-jE-aePCL56Rik37XJpwADyiYgfqLMKmNWd7QIci7qqHM19pIzU3RSfaP5HeilxMtPdzcAAjr9kqTRPyLPo4ym5E7ACL1jhRiLO60EPAco6efxsPdBlnxleLynvK76PlT-qaV3-MoNeL-nYzJUkhMMIMkPsCwmFDePfhZgvJar9s1JY5UR_F51XkP5DCQY7xvbVGJHpNn1Yo5Ih7m1DbQyYAj_a_VB0jZP709KfkPPRzIb9n5qmZclLjk5sOtsd88vDQZ-4xdExHbX6jX7bdlo8TzA600CPF2-ok-qcDLI9xZ7nBjv7YwobopXwYfnMM1ejFBaOg_7J6OzSlNLhpU-RQ-zhzeCqIOEwAUVGL7_IRiMVPe60gGI6UaXjVxtYqkz5HE5MVXIkG4THXI1JEBdpJ27TVYJJQ_sRZ9mOMqat8VxfmcVzX3rXXV7KyujSmwJzLq94wRbc6VFHgiZQo7xhnOlozZEIJcdeK3KnqSb8"
    mailer = emails.NewEmail(api_key)

    # define an empty dict to populate with mail values
    mail_body = {}

    mail_from = {
        "name": f"{client_name}",
        "email": "inf@hayaksa.com"
    }

    recipients = [
        {
            "name": "name",
            "email": email,
        }
    ]

    variables = [
        {
            "email": email,
            "substitutions": [
                {
                    "var": "name",
                    "value": name
                },
                {
                    "var": "event_name",
                    "value": event_name
                },
                {
                    "var": "event_date",
                    "value": event_date
                },
                {
                    "var": "event_location",
                    "value": event_location
                },
                {
                    "var": "qr_code",
                    "value": qr_code
                },
                {
                    "var": "event_venue",
                    "value": event_venue
                },
                {
                    "var": "event_city",
                    "value": event_city
                },
                {
                    "var": "event_logo",
                    "value": event_logo
                },
                {
                    "var": "entries",
                    "value": str(entries)
                },
                {
                    "var": "invitation_type",
                    "value": invitation_type
                }
            ]
        }
    ]


    attachment = urllib.request.urlopen(qr_code)
    att_read = attachment.read()
    att_base64 = base64.b64encode(bytes(att_read))

    attachments = [
        {
            "id": "profile-id",
            "filename": "qr-code.png",
            "content": f"{att_base64.decode('ascii')}"
        }
    ]

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(f"{client_name} | Ticket Information", mail_body)
    mailer.set_template("z3m5jgro55ogdpyo", mail_body)
    mailer.set_simple_personalization(variables, mail_body)
    mailer.set_attachments(attachments, mail_body)
    

    print(mailer.send(mail_body))