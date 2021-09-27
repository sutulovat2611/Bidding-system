"""The following module is created for communication with the API"""

from abc import ABC
import requests
import json

class API_access(ABC):
    """
    The abstract class which holds the API key and the root url which will be used by all the subclasses in order
    to get data from the API.
    It includes the "get_all" method that is inherited by all the API_access classes.
    """
    def __init__(self):
        self.my_api_key = 'JcqJqRRn6RbPNNJFmfGKDz6Tbp9jWR'
        self.root_url = 'https://fit3077.com/api/v2'

    def get_all(self, url):
        """
        Inputs:
            - url, which includes what has to be gotten from the API
        Return:
            - dictionary including the objects from the api, according to the url request
        Short description:
            Gets all the objects (based ono the url passed) from the api with all the data related to it
        """
        self.response = requests.get(url=url, headers={'Authorization': self.my_api_key})
        self.json_data = self.response.json()
        return self.json_data


class API_access_add_new(API_access):
    """
    Responsible for adding a new object to the API
    """
    def __init__(self):
        super().__init__()

    def add_new(self, url, object_to_add):
        """
        Inputs:
            - url, which includes what has to be added to the API
            - object_to_add, object to add to the API
        Return:
            - dictionary of the object that was just added to the API
        Short description:
           Adds the new object to the API, based on the url that was passed as a parameter
        """
        self.response = requests.post(
            url=url,
            data=json.dumps(object_to_add),
            headers={'Content-type': 'application/json', 'Accept': 'application/json',
                     'Authorization': self.my_api_key},
        )
        return self.response.json()


class API_access_patch_get_by_id(API_access):
    """
    Responsible for patching and oject and getting the object from the API by id
    """

    def __init__(self):
        super().__init__()

    def get_by_id(self, url):
        """
        Inputs:
            - url, which includes what has to be gotten from the API
        Return:
            - dictionary of the object that is gotten from the API
        Short description:
           Gets the object from the API, according to it's id, that was passed as a parameter in the url
        """
        self.response = requests.get(url=url, headers={'Authorization': self.my_api_key})
        self.json_data = self.response.json()
        return self.json_data

    def patch(self, url, request_body):
        """
        Inputs:
            - url, which includes what has to be patched in the API
            - request_body: updated body of the object that is to be patched
        Return:
            - boolean: True if the object was successfully patche, false otherwise
        Short description:
           Replaces the body of the object in the API with the request_body
        """
        self.response = requests.patch(
            url=url,
            data=json.dumps(request_body),
            headers={'Content-type': 'application/json', 'Authorization': self.my_api_key},
        )
        return format(self.response.reason) == 'OK'


class User_API_access(API_access_patch_get_by_id):
    """
    The subclass of the API_access which is responsible for user related actions with the API
    """

    def __init__(self):
        super().__init__()
        self.users_url = self.root_url + "/user"

    def get_all_users(self):
        """
        Inputs: None
        Return:
            all the users in the json format
        Short description:
            Calls the parent's get_all method, that is passing the url with all the required data, including competencies,
            competencies.subject, qualifications and initiated bids to get all the users from the API
        """
        url = self.users_url + "?fields=competencies&fields=competencies.subject&fields=qualifications&fields=initiatedBids"
        return super().get_all(url)

    def get_user_by_id(self, id):
        """
            Inputs:
                - id: user id in string format
            Return:
                the user in the json format
            Short description:
                Calls the parent get_by_id() method, passing the url that includes all the required data including
                competencies, competencies.subject, qualifications, initiated bids and including the user id to get that
                user from the API
        """
        url = self.users_url + "/{}".format(
            id) + "?fields=competencies&fields=competencies.subject&fields=qualifications&fields=initiatedBids"
        return super().get_by_id(url)

    def verify_login(self, username, password):
        """
            Inputs:
                - password: string format
                - username: string format
            Return: True if the credentials provided are valid, False otherwise
            Short description:
                Verifies the user credentials
        """
        users_login_url = self.users_url + "/login"
        self.response = requests.post(
            url=users_login_url,
            headers={'Authorization': self.my_api_key},
            data={
                'userName': username,
                'password': password
            }
        )
        return format(self.response.reason) == 'OK'

    def patch_user(self, id: 'str', new_request_body: dict):
        """
            Inputs:
                - new_request_body: dictionary format of parts to be updated
            Return: True if the update was successful, False otherwise
            Short description:
                Calls the parent's patch() method to partially update the user in the API according to the new_request_body
        """
        url = self.users_url + "/{}".format(id)
        return super().patch(url, new_request_body)


class Bid_API_access(API_access_add_new, API_access_patch_get_by_id):
    """
    The subclass of the API_access which is responsible for Bid related actions with the API
    """

    def __init__(self):
        super().__init__()
        self.bids_url = self.root_url + "/bid"

    def get_all_bids(self):
        """
        Inputs: None
        Return:
            all the bids in the json format
        Short description:
            Calls the parent's get_all method, that is passing the url with all the required data, including messages,
            to get all the bids from the API
        """
        url=self.bids_url + "?fields=messages"
        return super().get_all(url)

    def add_new_bid(self, bid_to_add: dict):
        """
        Inputs:
            - bid_to_add: dictionary format
        Return:
            - newly added bid in json format
        Short description:
            Calls the parent's add_new() method, passing the url and the new bid dictionary to add the new bid to the API
        """
        return super().add_new(self.bids_url, bid_to_add)

    def get_bid_by_id(self, id: str):
        """
        Inputs:
            - id: string format
        Return:
            - the bid that was found (in json format)
        Short description:
           Calls the parent get_by_id() method, passing the url that includes the bid id to get that bid from the API
        """
        url = self.bids_url + "/{}".format(id)
        return super().get_by_id(url)

    def patch_bid(self, id: 'str', new_request_body: dict):
        """
        Inputs:
            - id: string format
            - new_request_body: dictionary format, the updated body of the bid
        Return:
            - true, if the data in the bid is updated successfully, otherwise false
        Short description:
            Calls the parent's patch() method to partially update the bid in the API according to the new_request_body
        """
        url = self.bids_url + "/{}".format(id)
        return super().patch(url, new_request_body)

    def close_down_bid(self, id: 'str', date_close_down: dict):
        """
        Inputs:
            - id: string format
            - date_closed_down: dictionary format, date when the bid should close_down
        Return:
            - true, if the bid was closed down successfully, otherwise false
        Short description:
            Closes down the bid of id when the date reaches the date_close_down
        """
        bids_id_url = self.bids_url + "/{}".format(id) + "/close-down"
        self.response = requests.post(
            url=bids_id_url,
            data=json.dumps(date_close_down),
            headers={'Content-type': 'application/json', 'Authorization': self.my_api_key}
        )
        return format(self.response.reason) == 'OK'


class Subject_API_access(API_access_add_new):
    """
    The subclass of the API_access which is responsible for Subject related actions with the API
    """

    def __init__(self):
        super().__init__()
        self.subjects_url = self.root_url + "/subject"

    def get_all_subjects(self):
        """
        Inputs: None
        Return:
            all the subjects in the json format
        Short description:
            Calls the parent's get_all method to get all the subjects from the API
        """
        return super().get_all(self.subjects_url)

    def add_new_subject(self, subject_to_add: dict):
        """
        Inputs:
            - subject_to_add: dictionary format
        Return:
            - newly added subject in json format
        Short description:
            Calls the parent's add_new() method, passing the url and the new subject dictionary to add the new
            subject to the API
        """
        return super().add_new(self.subjects_url, subject_to_add)


class Message_API_access(API_access_add_new):
    """
    The subclass of the API_access which is responsible for Message related actions with the API
    """

    def __init__(self):
        super().__init__()
        self.messages_url = self.root_url + "/message"

    def get_all_messages(self):
        """
        Inputs: None
        Return:
            all the messages in the json format
        Short description:
           Calls the parent's get_all method to get all the messages from the API
        """
        return super().get_all(self.messages_url)

    def add_new_message(self, message_to_add: dict):
        """
        Inputs:
            - message_to_add: dictionary format
        Return:
            - newly added message in json format
        Short description:
            Calls the parent's add_new() method, passing the url and the new message dictionary to add the new message
            to the API
        """
        return super().add_new(self.messages_url, message_to_add)


class Contract_API_access(API_access_add_new):
    """
    The subclass of the API_access which is responsible for Contract related actions with the API
    """

    def __init__(self):
        super().__init__()
        self.contracts_url = self.root_url + "/contract"

    def get_all_contracts(self):
        """
        Inputs: None
        Return:
            all the contracts in the json format
        Short description:
            Calls the parent's get_all method to get all the contracts from the API
        """
        return super().get_all(self.contracts_url)

    def add_new_contract(self, contract_to_add: dict):
        """
        Inputs:
            - contract_to_add: dictionary format
        Return:
            - newly added contract in json format
        Short description:
            Calls the parent's add_new() method, passing the url and the new contract dictionary to add the new contract
            to the API
        """
        return super().add_new(self.contracts_url, contract_to_add)

    def sign_contract(self, id: 'str', date_signed: dict):
        """
        Inputs:
            - id: string format id of the contract to be signed
            - date signed: dictionary format date signed
        Return:
            - True, if the contract was successfully signed, otherwise False
        Short description:
            Signs the contract (setting the sign_date)
        """
        contracts_id_url = self.contracts_url + "/{}".format(id) + "/sign"
        self.response = requests.post(
            url=contracts_id_url,
            data=json.dumps(date_signed),
            headers={'Content-type': 'application/json',
                     'accept': '*/*',
                     'Authorization': self.my_api_key}
        )

        return format(self.response.reason) == 'OK'

    def delete_contract(self, id):
        """
        Inputs:
            - id: string format id of the contract to be deleted
        Return:
            - True, if the contract was successfully deleted, otherwise False
        Short description:
            Deletes the contract of the id from the API
        """
        contract_id_url = self.contracts_url + "/{}".format(id)
        self.response = requests.delete(url=contract_id_url, headers={'Authorization': self.my_api_key})
        print(self.response.status_code)
        return self.response.status_code == 204


class ReformatForAPI:
    """Responsible for reformatting the info into the API valid format"""

    def reformat_additional_info(self, info_to_reformat):
        """Makes the proper format of the additional info to update it in the API"""

        additional_info_format = {
            'subjectLevel': info_to_reformat['subjectLevel'],
            'contractLen': info_to_reformat['contractLen'],
            'qualificationTitle': info_to_reformat['qualificationTitle'],
            'sesPerWeek': info_to_reformat['sesPerWeek'],
            'hoursPerLesson': info_to_reformat['hoursPerLesson'],
            'dayAndTime': [],
            'rate': info_to_reformat['rate'],
            'rateType': info_to_reformat['rateType'],
            'offers': []
        }

        # add date and time for the bid
        for i in range(len(info_to_reformat['dayAndTime'])):
            additional_info_format['dayAndTime'].append(
                {'day': info_to_reformat['dayAndTime'][i]['day'],
                 'timeHour': info_to_reformat['dayAndTime'][i]['timeHour'],
                 'timeMin': info_to_reformat['dayAndTime'][i]['timeMin']})

        # add every offer including the new one
        for i in range(len(info_to_reformat['offers'])):
            offer_format = {
                'bidId': info_to_reformat['offers'][i].get_bid_id(),
                'initiatorId': info_to_reformat['offers'][i].get_initiator_id(),
                'dateCreated': info_to_reformat['offers'][i].get_date_created(),
                'sesPerWeek': info_to_reformat['offers'][i].get_ses_per_week(),
                'duration': info_to_reformat['offers'][i].get_duration(),
                'dayAndTime': [],
                'rate': info_to_reformat['offers'][i].get_rate(),
                'rateType': info_to_reformat['offers'][i].get_rate_type(),
                'freeClass': info_to_reformat['offers'][i].get_free_class(),
                'contractLen': info_to_reformat['offers'][i].get_contract_len()
            }

            # add date and time for the offer
            for b in range(len(info_to_reformat['offers'][i].get_day_and_time())):
                offer_format['dayAndTime'].append(
                    {
                        'day': info_to_reformat['offers'][i].get_day_and_time()[b]['day'],
                        'timeHour': info_to_reformat['offers'][i].get_day_and_time()[b]['timeHour'],
                        'timeMin': info_to_reformat['offers'][i].get_day_and_time()[b]['timeMin']
                    }
                )
            additional_info_format['offers'].append(offer_format)

        updated_info = {
            'additionalInfo': additional_info_format
        }
        return updated_info
