import pandas as pd
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from string import Template
from django.conf import settings

# Starting mailchimp camaign creation and sending process
def StartMailChimpCampaignProcess(audience_id,
            company_id,
            subscription_id,
            mc_api_key,
            mc_server,
            subject_line,
            df,
            email_template):

    min_class = 4
    # Authentication users mailchimp account
    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": settings.MAILCHIMP_API_KEY,
            "server": settings.MAILCHIMP_DATA_CENTER
        })
        response = client.ping.get()
        print(response)

    except ApiClientError as error:
        # Authentication failed
        print("An exception occurred in StartMailChimpCampaignProcess: {}".format(error.text))
        return False

    success = SendCampaignMails(client,
        audience_id,
        min_class,
        company_id,
        subscription_id,
        df,
        subject_line=subject_line, 
        from_name="Lambda Crunch Marketing",
        from_email="saeedusama181@gmail.com",
        language="en",
        email_template = email_template
    )

    if success:
        return True

    else:
        return False

def SendCampaignMails(client,
    audience_id,
    min_class,
    company_id,
    subscription_id,
    df,
    subject_line,
    from_name,
    from_email,
    language,
    email_template):
    
    AddMembersInAudienceList(audience_id=audience_id,
        min_class=min_class,
        company_id=company_id,
        subscription_id=subscription_id,
        client=client,
        df=df,
    )
    # =============================================================================
    # campaign creation
    # =============================================================================
    from_name = from_name
    reply_to = from_email
    campaign = CreateMailChimpCampaign(
        subject_line, 
        audience_id=audience_id,
        from_name=from_name,
        reply_to=reply_to,
        client=client
    )

    # =============================================================================
    #  templates creation
    # =============================================================================
        
    CreateEmailTemplate(html_code=email_template,
                        campaign_id=campaign['id'],
                        client=client
    )
    # =============================================================================
    # send the mail campaign
    # =============================================================================

    SendEmail(campaign_id=campaign['id'], client=client)

# =============================================================================
# add members to the existing audience function from a csv file
# =============================================================================
def AddMembersInAudienceList(audience_id,
    min_class, 
    company_id,
    subscription_id,
    client,
    df):
    
    print('Inside AddMembersInAudienceList')
     
    if len(df) != 0:
        print('Inside if')
        row_iter = df.iterrows()
        for index, row in row_iter:
            try:
                print('In Try')
                data = {
                    "status": "subscribed",
                    "email_address": row['email'],
                }
                client.lists.add_list_member(audience_id, data)
                print("response: {}".format(response))

            except ApiClientError as error:
                print("An exception occurred in AddMembersInAudienceList: {}".format(error.text))

    else:
        print('Email list is empty')


def CreateMailChimpCampaign(subject_line,audience_id, from_name, reply_to, client):

    data = {
        "recipients":
            {
                "list_id": audience_id
            },
        "settings":
            {
                "subject_line": subject_line,
                "from_name": from_name,
                "reply_to": reply_to
            },
        "type": "regular"
    }

    try:
        new_campaign = client.campaigns.create(data)

    except ApiClientError as error:
        print("An exception occurred in CreateMailChimpCampaign: {}".format(error.text))

    return new_campaign


def CreateEmailTemplate(html_code, campaign_id, client):
     
     
    string_template = Template(html_code).safe_substitute()

    try:
        client.campaigns.set_content(
            campaign_id,
            {'html': string_template}
        )

    except ApiClientError as error:
        print("An exception occurred in CreateEmailTemplate: {}".format(error.text))


# =============================================================================
# Sending cmapign as email
# =============================================================================

def SendEmail(campaign_id, client ):
    try:
        client.campaigns.send(
            campaign_id,
        )
    except ApiClientError as error:
        print("An exception occurred in SendEmail: {}".format(error.text))