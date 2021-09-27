from datetime import timedelta, datetime
import dateutil
from dateutil.relativedelta import relativedelta
import threading

from api_access import User_API_access, Bid_API_access, Subject_API_access, Message_API_access, Contract_API_access, \
    ReformatForAPI

from abc import  abstractmethod

from model import UserCollection, Student, Tutor, Competency, Qualification, Contract, Subject, OpenBid, CloseBid, \
    MessageClass


class UserAdapter:
    """"Works with the User, creating it's objects and getting all the info related to it from the API/ adding to the
    API """

    def get_all_users(self):
        """
        Short description:
            gets all the users from the API and makes them into user class instances
        :return: users: all the users in the system
        """
        all_users_dict = User_API_access().get_all_users()
        users = UserCollection()
        for u in all_users_dict:
            if u["isStudent"]:
                user = Student(u["id"], u["userName"], u["givenName"], u["familyName"])
            else:
                user = Tutor(u["id"], u["userName"], u["givenName"], u["familyName"])

            # Adding the competencies
            competencies = CompetencyAdapter().create_competencies_user(u)
            user.set_competencies(competencies)

            # Adding the qualifications
            qualifications = QualificationAdapter().create_qualifications_user(u)
            user.set_qualifications(qualifications)

            # adding contracts
            contracts = ContractAdapter().get_contracts_user(user.get_id())


            # Looping through contracts to find the one that are one month from expiry date
            expiring_contracts = []
            ongoing_contracts = []
            for c in contracts:
                date_now = datetime.now()
                contract_expiry_date = dateutil.parser.parse(c.get_expiry_date()[:-1])
                num_months = (contract_expiry_date.year - date_now.year) * 12 + (contract_expiry_date.month - date_now.month)
                if num_months <= 1 and contract_expiry_date > date_now:
                    expiring_contracts.append(c)
                if not(contract_expiry_date <= date_now):
                    ongoing_contracts.append(c)

            # Setting the expiring contracts for the user
            user.set_expiring_contracts(expiring_contracts)
            # Setting ongoing contracts
            user.set_ongoing_contracts(ongoing_contracts)

            # Adding the initiated bids for the user
            if isinstance(user,Student):
                user.set_bids(BidAdapter().get_student_bids(user.get_id()))

            if isinstance(user, Tutor):
                # adding the monitor bids for Tutor
                if 'monitoredBids' in u['additionalInfo']:
                    monitor_bids_ids = u['additionalInfo']['monitoredBids']
                    monitor_bids = BidAdapter().get_monitor_bids(monitor_bids_ids)
                    user.set_monitor_bids(monitor_bids)
            users.add_user(user)
        return users

    def create_contract_tutor(self, tutor_dict):
        """
        Short description:
            translates the tutor dictionary to the tutor class instance
        Input:
            tutor_dict: information about the tutor in the dictionary form
        return:
            tutor object
        """
        tutor = Tutor(tutor_dict["id"], tutor_dict["userName"], tutor_dict["givenName"], tutor_dict["familyName"])
        return tutor

    def create_contract_student(self, student_dict):
        """
        Short description:
            translates the Student dictionary to the Student class instance
        Input:
            student_dict: information about the student in the dictionary form
        return:
            student object
        """
        student = Student(student_dict["id"], student_dict["userName"], student_dict["givenName"],
                          student_dict["familyName"])
        return student

    def get_user_id(self, user_id):
        """
        Short description: gets the user by the user id
        Input: user_id, an id of the user
        Return: instance of the user subclass
        """

        user_dict = User_API_access().get_user_by_id(user_id)
        if user_dict['isStudent']:
            user = self.create_contract_student(user_dict)
        else:
            user = self.create_contract_tutor(user_dict)

        # Adding the competencies
        competencies = CompetencyAdapter().create_competencies_user(user_dict)
        user.set_competencies(competencies)

        # Adding the qualifications
        qualifications = QualificationAdapter().create_qualifications_user(user_dict)
        user.set_qualifications(qualifications)

        # adding contracts
        contracts = ContractAdapter().get_contracts_user(user.get_id())

        # Looping through contracts to find the one that are one month from expiry date
        expiring_contracts = []
        ongoing_contracts = []
        for c in contracts:
            date_now = datetime.now()
            contract_expiry_date = dateutil.parser.parse(c.get_expiry_date()[:-1])
            num_months = (contract_expiry_date.year - date_now.year) * 12 + (
                        contract_expiry_date.month - date_now.month)
            if num_months <= 1 and contract_expiry_date > date_now:
                expiring_contracts.append(c)
            if not (contract_expiry_date <= date_now):
                ongoing_contracts.append(c)

        # Setting the expiring contracts for the user
        user.set_expiring_contracts(expiring_contracts)
        # Setting ongoing contracts
        user.set_ongoing_contracts(ongoing_contracts)

        # Adding the initiated bids for the user
        if isinstance(user, Student):
            user.set_bids(BidAdapter().get_student_bids(user.get_id()))

        return user

    def get_offer_initiators(self, bid):

        """
        Inputs: bid: the object of the Bid subclass that we want to get the offer initiator for
        Return:
            - list of all the initiators of the offers for the following bid
        Short description:
            Gets the list of all offer initiators that belong to the bid
        """
        initiators = []
        for o in bid.get_offers():
            initiator_id = o.get_initiator_id()
            u = self.get_user_id(initiator_id)
            initiators.append(u)
        return initiators

    def get_user_username(self, user, bid_initiator, offer_initiator_id):
        """
        Inputs:
            user: user that is logged in
            bid_initiator: the bid initiator
            offer_initiator_id: id of the offer initiator
        Return:
            - the username of the user
        Short description:
            Being called in the chat to find the username of the user that the currently logged in.
            If the user who is currently logged in is:
             - Tutor: takes the username of the bid creator
             - Student: takes the id of the offer creator and accesses the API to get her/his username
        """
        if isinstance(user, Student):
            return self.get_user_id(offer_initiator_id).get_username()
        else:
            return bid_initiator.get_username()

    def monitor_bid(self, tutor, bid):
        """
        Inputs:
            user: instance of the Tutor class, for the tutor who is logged in
            bid: instance of the Bid that the Tutor is willing to add
        Return:
            - True, if the bid is successfully added
            - False, if the bid was in the tutor's monitor list before
        Short description:
            Adds the new bid to the tutor's monitor bid list, if the bid was not there before and updates the
            API accordingly
        """
        successful = tutor.add_monitor_bids(bid)
        if successful:
            # updating the monitor list in the API
            updated_monitor_bids = tutor.get_monitor_bids()
            bids_id = []
            for i in updated_monitor_bids:
                bids_id.append(i.get_id())
            update_api_body = {"additionalInfo":
                {
                    "monitoredBids": bids_id
                }
            }
            User_API_access().patch_user(tutor.get_id(), update_api_body)
            return True
        return False

    def get_user_by_username(self, username):
        """
        Inputs:
            username: username in string
        Return:
            - u: instance of the user with the username
            - None: if the user does not exist in the system
        Short description:
            Gets all the users and finds the one with the username, that was passed as a parameter.
            If the user is not found, returns None:
        Pre-condition:
            all the users in the system have unique usernames
        """
        all_users=self.get_all_users()
        for u in all_users:
            if u.get_username() == username:
                return u
        return None


class CompetencyAdapter:
    """Works with the Competency, creating it's objects, getting all the info from the dictionary which is passed"""

    def create_competencies_user(self, user_dict):
        """
        Input:
            -user_dict: information about the user in the dictionary form
        Return:
            - competencies: list of instances of competency class
        Short description:
            translates from dictionary into Competency class instance
        """

        competencies = []
        for comp in user_dict["competencies"]:
            subject = SubjectAdapter().create_subject(comp['subject'])
            competencies.append(Competency(comp["id"], subject, comp["level"]))
        return competencies


class QualificationAdapter:
    """Works with the Qualification, creating it's objects, getting all the info from the dictionary which is passed"""

    def create_qualifications_user(self, user_dict):
        """
        Input:
            -user_dict: information about the user in the dictionary form
        Return:
            - qualifications: list of instances of the Qualification class
        Short description:
            translates subject from dictionary into Qualification class instance
        """
        qualifications = []
        for qual in user_dict["qualifications"]:
            qualifications.append(
                Qualification(qual["id"], qual["title"], qual["description"], qual["verified"]))
        return qualifications


class ContractAdapter:
    """Works with the Contract, creating it's objects and getting all the info related to it from the API/adding to
    the API """

    def get_contracts_user(self, user_id):
        """
        Short Description:
            1) Gets all the contracts for the user
        :param user_id: instance of the user class, the user whose contracts we are searching for
        :return contracts: list of contracts the user is involved in
        """
        all_contracts = self.get_all_contracts()
        user_contracts = []
        for con in all_contracts:
            if con.get_first_party().get_id() == user_id:
                user_contracts.append(con)
            elif con.get_second_party().get_id() == user_id:
                user_contracts.append(con)
        return user_contracts

    def get_all_contracts(self):
        """
        Short Description:
            1) Gets all the contracts
        :return contracts: list of all the contracts in the system
        """
        all_contracts_dict = Contract_API_access().get_all_contracts()
        contracts = []
        for con in all_contracts_dict:
            # Creating first party users
            if con['firstParty']['isStudent']:
                first_party = UserAdapter().create_contract_student(con['firstParty'])
            elif con['firstParty']["isTutor"]:
                first_party = UserAdapter().create_contract_tutor(con['firstParty'])

            # Creating second party users
            if con['secondParty']['isStudent']:
                second_party = UserAdapter().create_contract_student(con['secondParty'])
            elif con['secondParty']["isTutor"]:
                second_party = UserAdapter().create_contract_tutor(con['secondParty'])

            # Creating the subject
            subject = SubjectAdapter().create_subject(con['subject'])

            # Creating contract
            contract = Contract(con['id'], first_party, second_party, subject, con['dateCreated'], con['dateSigned'],
                                con['expiryDate'])
            contract.set_additional_info(con['additionalInfo'])
            contract.set_lesson_info(con['lessonInfo'])

            # adding the contract to contract list
            contracts.append(contract)
        return contracts

    def add_contract_api(self, contract, sign):
        """
        Short Description:
            1) Reformat the class object to the dictionary and adds it to the API
        :param contract: Instance of the contract class
        :param sign: boolean that is true if the contract is not signed yet
        """
        add_contract = {
            "firstPartyId": contract.get_first_party().get_id(),
            "secondPartyId": contract.get_second_party().get_id(),
            "subjectId": contract.get_subject().get_id(),
            "dateCreated": contract.get_date_created(),
            "expiryDate": contract.get_expiry_date(),
            "paymentInfo": {},
            "lessonInfo": contract.get_lesson_info(),
            "additionalInfo": contract.get_additional_info()
        }

        Contract_API_access().add_new_contract(add_contract)
        if sign:
            id = self.get_contract_id(contract)
            date_signed_calculate = dateutil.parser.parse(add_contract["dateCreated"][:-1])  + timedelta(
                minutes=1)
            self.sign_contract(contract,id, date_signed_calculate)

    def get_contract_id(self, contract):
        """
        Short Description:
            1) Gets all the contracts from the api
            2) loops through contracts until the contract is found based on comparison of the properties
        :param contract: The contract we want to find
        :return: the contract id if found. None otherwise
        """
        all_contracts = self.get_all_contracts()
        for i in all_contracts:
            if i == contract:
                return i.get_id()
        return None

    def sign_contract(self, contract, id, date_signed):
        """
        Short Description:
            Allows to sign a contract of id on the certain date
        :param contract: Instance of the contract class
        :param id: id of the contract that is to be signed
        :param date_signed: date when the contract should be signed
        """
        date_signed_isoformat = date_signed.isoformat()[:-3] + 'Z'
        date_signed = {
            "dateSigned": date_signed_isoformat
        }
        Contract_API_access().sign_contract(id, date_signed)
        contract.set_sign_date(date_signed_isoformat)

    def delete_contract(self, id):
        """
        Short Description:
            Deletes the contract from the API
        :param id: id of the contract that is to be deleted
        """
        Contract_API_access().delete_contract(id)


class ContractsSort:
    """Sorts the contracts based on ongoing, expired and pending"""

    def sort_ongoing(self, user_id ):
        """
        Short Description:
            Sorts out the ongoing contracts: signed and not expired
        :param user_id: id of the user, whose contracts are being sorted
        """
        contracts=ContractAdapter().get_contracts_user(user_id)
        ongoing_contracts=[]
        for c in contracts:
            expiry_date=dateutil.parser.parse(c.get_expiry_date()[:-1])
            if expiry_date > datetime.now() and c.get_date_signed()!=None:
                ongoing_contracts.append(c)
        return ongoing_contracts

    def sort_expired(self,  user_id, is_student):
        """
        Short Description:
            Sorts out the expired contracts, representing all the expired contracts if the user who is logged in is a tutor
            and only the five latest expired contracts if the user is a student
        :param user_id: id of the user, whose contracts are being sorted
        :param is_student: boolean which is true if the user who is logged in is a student, false otherwise
        """
        contracts = ContractAdapter().get_contracts_user(user_id)
        expired_contracts = []
        for c in contracts:
            expiry_date = dateutil.parser.parse(c.get_expiry_date()[:-1])
            if expiry_date <= datetime.now():
                expired_contracts.append(c)
        if is_student and len(expired_contracts)>5:
            sort_out_five=[]
            for c in range(len(expired_contracts)):
                if c>=len(expired_contracts)-5:
                    sort_out_five.append(expired_contracts[c])
            return sort_out_five
        return expired_contracts

    def sort_pending(self,  user_id):
        """
        Short Description:
            Sorts out the pending contracts: NOT signed and not expired
        :param user_id: id of the user, whose contracts are being sorted
        """
        contracts = ContractAdapter().get_contracts_user( user_id)
        pending_contracts = []
        for c in contracts:
            expiry_date = dateutil.parser.parse(c.get_expiry_date()[:-1])
            if expiry_date > datetime.now() and c.get_date_signed() == None:
                pending_contracts.append(c)
        return pending_contracts


class SubjectAdapter:
    """Works with the Subject, creating it's objects and getting all the info related to it from the API/adding to
    the API """

    def create_subject(self, subject_dict):
        """
        Input:
            -subject_dict: information about the subject in the dictionary form
        Return:
            - subject: instance of the subject class
        Short description:
            translates subject from dictionary into Subject class instance
        """
        subject = Subject(subject_dict["id"], subject_dict["name"],
                          subject_dict["description"])
        return subject

    def verify_subject(self, subject):
        """Checks whether the subject exists"""
        all_subjects = Subject_API_access().get_all_subjects()
        count = False
        # check if the subject exists
        for subj in all_subjects:
            if subj["name"] == subject.get_name() and subj["description"] == subject.get_description():
                subject.set_id(subj["id"])
                count = True
                break
        return count

    def add_subject_api(self, subject):
        """Adds the new subject to the api"""
        subject_dictionary = {
            "name": subject.get_name(),
            "description": subject.get_description()
        }
        id_new_subject = Subject_API_access().add_new_subject(subject_dictionary)["id"]
        subject.set_id(id_new_subject)


class LoginMechanism:
    """
    Attributes:
        -username: username which was input by the user
        -password: password that was input by the user
    Short description:
        Responsible for verifying the user credentials
        Calls UserAdapter() to return the User class that logged in
    """

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def verify(self):
        """
        Inputs: none
        Return:
            -user: object of the user who logged into the system
        Short description:
            Verifies the user credentials
        """
        user_api = User_API_access()
        user = None
        if user_api.verify_login(self.username, self.password):
            user = self.create_user()
        return user

    def create_user(self):
        """
        Inputs:
            None
        Return:
            -user: object of the user who logged into the system
        Short description:
            Returns the user that matches the username inputted
        """
        users = UserAdapter().get_all_users()
        # looping through all the users finding the one with the proper credentials
        for u in users:
            if u.get_username() == self.username:
                user = u
        return user


class BidAdapter:
    """"Works with the Bid, creating it's objects and getting all the info related to it from the API/adding to the API"""

    def get_all_bids(self):
        """
        Inputs: None
        Return: all_bids, list of bids which are not closed
        Short description:
            Gets all the non-closed down bids
        """

        all_bids = []
        bids_API = Bid_API_access().get_all_bids()
        for b in bids_API:

            if b['dateClosedDown'] is None:
                subject = SubjectAdapter().create_subject(b["subject"])
                u = UserAdapter().create_contract_student(b['initiator'])
                if b['type'] == 'open':
                    bid = OpenBid(b['id'], u, b['dateCreated'], b['dateClosedDown'], subject)
                    bid.set_additional_info(b['additionalInfo'])

                    if dateutil.parser.parse(b['dateCreated'][:-1]) + timedelta(
                            minutes=30) <= datetime.now():
                        CloseDownBid(u, bid).close_down_by_time()
                    else:
                        all_bids.append(bid)
                else:
                    bid = CloseBid(b['id'], u, b['dateCreated'], b['dateClosedDown'], subject)
                    bid.set_additional_info(b['additionalInfo'])

                    if dateutil.parser.parse(b['dateCreated'][:-1]) + timedelta(
                            days=7) <= datetime.now():
                        CloseDownBid(u, bid).close_down_by_time()
                    else:
                        all_bids.append(bid)

        return all_bids

    def get_student_bids(self, initiator_id):
        """
        Inputs:
            - initiator_id, id of the student for whom we are getting the initiated bids
        Return: student_bids, list of bids initiated by the student
        Short description:
            Gets all the non-closed down bids that are initiated by the student
        """
        all_bids = self.get_all_bids()
        student_bids = []
        for b in all_bids:
            if b.get_initiator().get_id() == initiator_id:
                student_bids.append(b)
        return student_bids

    def get_tutor_bids(self, tutor_id):
        """
        Inputs:
            - tutor_id, id of the tutor for whom we are getting the available bids
        Return: tutor_bids, list of bids of the tutor
        Short description:
            Gets the available bids for the tutor according to their competency level
        """
        all_bids = self.get_all_bids()
        tutor = UserAdapter().get_user_id(tutor_id)
        tutor_bids = []
        for b in all_bids:
            for comp in tutor.get_competencies():
                if comp.get_subject().get_name() == b.get_subject().get_name():
                    if comp.get_level() >= int(b.get_additional_info()['subjectLevel']) + 2:
                        tutor_bids.append(b)
        return tutor_bids

    def add_bid_api(self, initiator_id, subject_id, bid):
        """
        Inputs:
            - initiator_id, id of the student who initiated the bid
            - subject_id, id of the subject that the bid is related to
            - bid, instance of the Bid subclass
        Return: None
        Short description:
            Formats and adds the new bid to the API
        """
        if isinstance(bid, OpenBid):
            type = 'open'

        else:
            type = 'close'
        bid_dictionary = {
            "type": type,
            "initiatorId": initiator_id,
            "dateCreated": bid.get_date_created(),
            "subjectId": subject_id,
            "additionalInfo": bid.get_additional_info()
        }
        # add new bid to API
        Bid_API_access().add_new_bid(bid_dictionary)

    def get_tutor_offer_bids(self, tutor_id):
        """
        Inputs:
            - tutor_id, id of the tutor whose offers are to be found
        Return: updated list of bids
        Short description:
            Gets the data about all the bids that are not closed down from the API.
            Checks if the tutor made an offer in that bid
            Returns list of bids that tutor made offer to
        """

        # uploads only the ones which are up-to-date
        all_bids = self.get_all_bids()
        bids_offers = []
        for i in all_bids:
            initiators = UserAdapter().get_offer_initiators(i)
            for init in initiators:
                if tutor_id == init.get_id():
                    bids_offers.append(i)
        return bids_offers

    def bid_close_down(self, bid_id, date_closed):
        """
        Inputs:
            - bid_id: id of the bid which will be closed
            - date_closed: date when the bid is closed
        Return: None
        Short description: closes the bid in the API
        """
        Bid_API_access().close_down_bid(bid_id, date_closed)

    def get_monitor_bids(self, monitor_bids_ids):
        """
        Inputs:
            - monitor_bids_ids: list of (strings) bid ids to be extracted
        Return:
            - list of the bids, which correspond to ids that were sent as a parameter
        Short description: from all the available bids, finds the ones with the ids that were sent as a parameter
        """
        all_bids = self.get_all_bids()
        monitor_bids = []
        for bid in all_bids:
            for bid_id in monitor_bids_ids:
                if bid.get_id() == bid_id:
                    monitor_bids.append(bid)
        return monitor_bids


class BidCreator:
    """
    Attributes:
        - user: user who is currently logged in to the system
    Short description:
        1) Declares a create_bid method which calls the proper subclass: OpenBidCreator/ClosedBidCreator based on the
        type that was passed in from the student input
        2) Declares the abstract factory method that the subeclasses will be overriding
    """

    def __init__(self, user):
        self.user = user

    @abstractmethod
    def factory_method(self, subject_name, description, additional_info):
        """
        Inputs:
            - subject_name: the name of the subject involved in the bid
            - description: the description of the subject involved in the bid
            - additional_info: all the information that was input by the creator of the bid

        Short description:
            Initialises the method to be overridden by the subclasses
        """
        pass

    def create_bid(self, type_bid, subject_name, description, additional_info):
        """
        Inputs:
            - type_bid: the string that holds the type of the bid that was chosen by the user
            - subject_name:the name of the subject involved in the bid
            - description: the description of the subject involved in the bid
            - additional_info: all the information that was input by the creator of the bid
        Return: None
        Short description:
           Calls the factory method of the concrete creator subclass based on the type of bid to be created:
           OpenBidCreator/ CloseBidCreator, which will be responsible for creation of the bid
           of the chosen type
        """
        if type_bid == 'open':
            OpenBidCreator(self.user).factory_method(subject_name, description, additional_info)
        else:
            CloseBidCreator(self.user).factory_method(subject_name, description, additional_info)


class OpenBidCreator(BidCreator):
    """
    Short description:
        Overrides the base factory method so it returns the Bid of Type OpenBid
    """

    def factory_method(self, subject_name, description, additional_info):
        """
        Inputs:
            - subject_name: The name of the subject involved in the subject
            - description: The description of subject involved in the subject
            - additional_info: all the information that was input by the creator of the bid
        Return:
            - bid: instance of the newly created OpenBid
        Short description:
            1) Creates the OpenBid with all the information input by the user and date created.
            2) Checks whether the subject that the user required exists, if not create a new subject and add to API.
            3) Loads the newly created bid to the API
        """

        # Creating date
        date_created = datetime.now()
        date_created_isoformat = date_created.isoformat()[:-3] + 'Z'
        subject = {
            "id": '',
            "name": subject_name,
            "description": description
        }
        subject = SubjectAdapter().create_subject(subject)
        bid = OpenBid('', self.user, date_created_isoformat, "", subject)
        bid.set_additional_info(additional_info)

        # add new bid to user
        self.user.add_bids(bid)

        if not SubjectAdapter().verify_subject(subject):
            SubjectAdapter().add_subject_api(subject)

        subject_id = subject.get_id()

        BidAdapter().add_bid_api(self.user.get_id(), subject_id, bid)

        return bid


class CloseBidCreator(BidCreator):
    """
    Short description:
        Overrides the base factory method so it returns the Bid of type CloseBid
    """

    def factory_method(self, subject_name, description, additional_info):
        """
        Inputs:
            - subject_name: The name of the subject in the bid
            - description: the description of the subject in the bid
            - additional_info: all the information that was input by the creator of the bid
        Return:
            - bid: instance of the newly created CloseBid

        Short description:
            1) Creates the CloseBid with all the information input by the user and date created.
            2) Checks whether the subject that the user required exists, if not calls create a new subject and add to API.
            3) Loads the newly created bid to the API using BidAdapter
        """
        # Creating date
        date_created = datetime.now()
        subject = {
            "id": '',
            "name": subject_name,
            "description": description
        }
        subject = SubjectAdapter().create_subject(subject)
        bid = CloseBid('', self.user, date_created.isoformat()[:-3] + 'Z', "", subject)
        bid.set_additional_info(additional_info)

        # add new bid to user
        self.user.add_bids(bid)

        if not SubjectAdapter().verify_subject(subject):
            SubjectAdapter().add_subject_api(subject)

        subject_id = subject.get_id()

        BidAdapter().add_bid_api(self.user.get_id(), subject_id, bid)

        return bid


class OfferAdapter:
    """
    Attributes:
        -bid: bid which is being viewed at the moment
    Parameters: None
    Short description:
        Responsible for offer related operations :
        - update offers in the API
        - remove offer: deletes the offer from the bid and from the bid API
     """

    def __init__(self, bid):
        self.bid = bid

    def update_offers_in_api(self, bid_id, additional_info_updated):
        """
            :param additional_info_updated: the updated version of the additional info that should go to API
            :param bid_id: the id of the bid
            Return: None
            Short description:
                1) calls the ReformatForAPI() class to reformat the given info into a proper format for api
                2) updates the additional info for this bid in the API
        """
        # access the API for bids
        bid_api = Bid_API_access()
        # reformat the updated additional info to the proper format for the API
        additional_info_format = ReformatForAPI().reformat_additional_info(additional_info_updated)
        # add the new offer to the API
        bid_api.patch_bid(bid_id, additional_info_format)

    def remove_offer(self, offer_initiator_id):
        """
            :param offer_initiator_id: the id of the tutor that initiated the offer
            Return: None
            Short description:
                        1) removes the offer from the bid class
                        2) calls the ReformatForApi() class to reformat the given info into a proper format for api
                        2) updates the additional info for this bid in the API
        """
        bid_api = Bid_API_access()

        # Removing offer from bid class
        self.bid.remove_offer(offer_initiator_id)

        # removing offer from API
        additional_info_format = ReformatForAPI().reformat_additional_info(self.bid.get_additional_info())

        bid_api.patch_bid(self.bid.get_id(), additional_info_format)


class BidUpdater:
    """
        Parameters:
            -subscribers: list of open bids that were added to Monitor page
        Short description:
            Updates the list of subscribers if the new bids were added
            Updates all the bids every 30 seconds, checking whether there were any new offers added to them
    """
    def __init__(self, bids):
        self.subscribers=[]
        self.subscribe(bids)
        self.notify_subscribers()

    def subscribe(self, bids):
        """
        Inputs:
            - bids: list of bids from the monitoring page
        Return: None
        Short description:
            Updates the subscribers if there were any new bids added to the monitoring page
        """
        for b in bids:
            self.subscribers.append(b)

    def notify_subscribers(self):
        """
        Inputs: None
        Return: None
        Short description:
            Every 30 seconds updates every open bid, that the tutor added to monitor, representing new offers that were
            added by other tutors.
        """
        for s in self.subscribers:
            bid_id = s.get_id()
            bid_from_api = Bid_API_access().get_bid_by_id(bid_id)
            s.set_additional_info(bid_from_api['additionalInfo'])
        threading.Timer(30.0, self.notify_subscribers).start()


class ContractCreator:
    """
    Attributes:
        -user: user who is currently logged in to the system
    Short description:
        Responsible for offer related operations :
        - Create_contract_by_offer: Creates a contract when the contract is formed due to acceptance by student of a Tutor's offer
        - Create_contract_buy_out: creates a contract when the Tutor agrees to all the requirements stated in an open bid by buying the
        offer out
     """

    def __init__(self, user):
        self.user = user


    def create_contract_by_offer(self, bid, offer, offer_initiator):
        """
        Parameters:
            -bid: bid of which the contract will be created from
            -offer: the offer that is offered by the tutor based on the bid
            -offer_initiator: the tutor who initiated the offer
        Short description:
            method used when an offer is made buy a tutor and later on accepted by the student
            1) Creates the contract based on the offer provided by the offer initiator
            2) Adds the contract to the user (student) contracts list
            3) Adds the newly created contract to the API
        :return: newly created contract
        """
        # Creating date
        date_created = datetime.now()
        date_created_isoformat = date_created.isoformat()[:-3] + 'Z'
        # Expiry_date
        expiry_date_calc = date_created + relativedelta(months=+int(offer.get_contract_len()))
        expiry_date = expiry_date_calc.isoformat()[:-3] + 'Z'
        new_contract = Contract('', bid.get_initiator(), offer_initiator, bid.get_subject(),
                                date_created_isoformat, date_created_isoformat, expiry_date)

        for i in range(int(bid.get_additional_info()['sesPerWeek'])):
            # Additional Information - Lesson Info
            new_contract.add_lesson_info(offer.get_day_and_time()[i]['day'],
                                         offer.get_day_and_time()[i]['timeHour'],
                                         offer.get_day_and_time()[i]['timeMin'])

        free_class = "Not provided"
        if offer.get_free_class():
            free_class = "Provided"

        # Additional Information
        additional_info = {
            'subjectLevel':bid.get_additional_info()['subjectLevel'],
            'sesPerWeek': offer.get_ses_per_week(),
            "hoursPerLesson": offer.get_duration(),
            "rate": offer.get_rate(),
            "rateType": offer.get_rate_type(),
            "freeClass": free_class,
        }

        new_contract.set_additional_info(additional_info)
        # add contract to user
        self.user.add_ongoing_contract(new_contract)

        # contract in API
        ContractAdapter().add_contract_api(new_contract, True)
        return new_contract

    def create_contract_buy_out(self, bid):
        """
        Parameters:
            -bid: bid of which the contract will be created from
        Short description:
            Function used when the tutor buys out the bid in an open bid
            1) creates a new contract based on the Bid requirements
            2) Adds new contract to the user (Tutor) contracts list
            3) Adds newly created contract to the API
        :return: newly created contract
        """
        # Creating date
        date_created = datetime.now()
        date_created_isoformat = date_created.isoformat()[:-3] + 'Z'
        # Expiry_date
        expiry_date_calc = date_created + relativedelta(months=+int(bid.get_additional_info()['contractLen']))
        # expiry_date_calc = date_created + timedelta(minutes=2)

        expiry_date = expiry_date_calc.isoformat()[:-3] + 'Z'
        new_contract = Contract('', bid.get_initiator(), self.user, bid.get_subject(),
                                date_created_isoformat, date_created_isoformat, expiry_date)

        for i in range(int(bid.get_additional_info()['sesPerWeek'])):
            # Additional Information - Lesson Info
            new_contract.add_lesson_info(bid.get_additional_info()['dayAndTime'][i]['day'],
                                         bid.get_additional_info()['dayAndTime'][i]['timeHour'],
                                         bid.get_additional_info()['dayAndTime'][i]['timeMin'])

        # Additional Information
        additional_info = {
            'subjectLevel': bid.get_additional_info()['subjectLevel'],
            'sesPerWeek': bid.get_additional_info()['sesPerWeek'],
            "hoursPerLesson": bid.get_additional_info()['hoursPerLesson'],
            "rate": bid.get_additional_info()['rate'],
            "rateType": bid.get_additional_info()['rateType'],
            "freeClass": "Not provided",
        }

        new_contract.set_additional_info(additional_info)
        self.user.add_ongoing_contract(new_contract)

        # contract in API
        ContractAdapter().add_contract_api(new_contract, True)
        return new_contract

    def reuse_contract_unsigned(self, contract, tutor, contract_len):
        """
        Parameters:
            - contract: instance of the contract that will be renewed
            - tutor : tutor to renew the contract with
            - contract_len : newly set contract duration
        Short description:
            Creates a contract request with the terms of the contract, which was sent to the method, setting the tutor
            and the contract duration
        :return: newly created contract request
        """
        # Creating date
        date_created = datetime.now()
        date_created_isoformat = date_created.isoformat()[:-3] + 'Z'
        # Expiry_date
        expiry_date_calc = date_created + relativedelta(months=+int(contract_len))
        expiry_date = expiry_date_calc.isoformat()[:-3] + 'Z'
        new_contract = Contract('', self.user, tutor, contract.get_subject(),
                                date_created_isoformat, None, expiry_date)

        for i in range(int(contract.get_additional_info()['sesPerWeek'])):
            # Additional Information - Lesson Info
            new_contract.add_lesson_info(contract.get_lesson_info()['day'][i],
                                         contract.get_lesson_info()['timeHour'][i],
                                         contract.get_lesson_info()['timeMin'][i])

        # Additional Information
        additional_info = {
            'subjectLevel': contract.get_additional_info()['subjectLevel'],
            'sesPerWeek': contract.get_additional_info()['sesPerWeek'],
            "hoursPerLesson": contract.get_additional_info()['hoursPerLesson'],
            "rate": contract.get_additional_info()['rate'],
            "rateType": contract.get_additional_info()['rateType'],
            "freeClass": "Not provided",
        }

        new_contract.set_additional_info(additional_info)
        self.user.add_pending_contract(new_contract)
        # contract in API
        ContractAdapter().add_contract_api(new_contract, False)
        return new_contract

    def  new_terms_contract_unsigned(self, tutor, contract_info, lesson_info):
        """
        Parameters:
            - tutor : tutor to renew the contract with
            - contract_info: the terms of the contract that will not be renewed (competency, subject, etc)
            - lesson_info: info on the lesson, that was renewed
        Short description:
            Creates a contract request with the new terms, setting the tutor
        :return: newly created contract request
        """
        # Creating date
        date_created = datetime.now()
        date_created_isoformat = date_created.isoformat()[:-3] + 'Z'
        # Expiry_date
        expiry_date_calc = date_created + relativedelta(months=+int(contract_info["contractLen"]))
        expiry_date = expiry_date_calc.isoformat()[:-3] + 'Z'
        new_contract = Contract('', self.user, tutor, contract_info["subject"],
                                date_created_isoformat, None, expiry_date)

        for i in range(int(contract_info['sesPerWeek'])):
            # Additional Information - Lesson Info
            new_contract.add_lesson_info(lesson_info[i]['day'],
                                         lesson_info[i]['timeHour'],
                                         lesson_info[i]['timeMin'])

        # Additional Information
        additional_info = {
            'subjectLevel': contract_info["subjectLevel"],
            'sesPerWeek': contract_info['sesPerWeek'],
            "hoursPerLesson": contract_info['hoursPerLes'],
            "rate": contract_info['rate'],
            "rateType": contract_info['rateType'],
            "freeClass": "Not provided",
        }

        new_contract.set_additional_info(additional_info)
        self.user.add_pending_contract(new_contract)
        # contract in API
        ContractAdapter().add_contract_api(new_contract, False)
        return new_contract


class MessagesAdapter:
    """
    Parameters:
        -user: user who is currently logged in to the system

    Short description:
            1) Gets all the messages in the API
            2) Filters out messages for the chosen bid only
            3) Filters out messages for this offer only
        """

    def get_messages(self, bid, offer):
        """
        Inputs:
            - bid: instance of the bid being viewed
            - offer: instance of the offer being viewed
        Return:
            - messages: the messages that belong to this offer only (between the bid creator and the offer creator)
        Short description:
            1) Gets all the messages in the API
            2) Filters out messages for the chosen bid only
            3) Filters out messages for this offer only

        """
        # accessing the API for messages
        api_access = Message_API_access()
        # exporting all the messages from the API
        all_messages = []
        all_messages_json = api_access.get_all_messages()
        # creating an object of all the messages
        for i in range(len(all_messages_json)):
            all_messages.append(MessageClass(all_messages_json[i]['id'], all_messages_json[i]['bidId'],
                                             all_messages_json[i]['poster']['id'], all_messages_json[i]['datePosted'],
                                             all_messages_json[i]['content'], all_messages_json[i]['additionalInfo']))
        # get messages for this bid only
        messages_this_bid = []
        for i in range(len(all_messages)):
            if bid.get_id() == all_messages[i].get_bid_id():
                messages_this_bid.append(all_messages[i])

        # get messages between the current user and the creator of the offer
        messages_this_offer = []
        for i in range(len(messages_this_bid)):
            if messages_this_bid[i].get_additional_info()['receiver_id'] == offer.get_initiator_id() or \
                    messages_this_bid[i].get_poster_id() == offer.get_initiator_id():
                messages_this_offer.append(messages_this_bid[i])

        return messages_this_offer


class CloseDownBid:
    """
    Attributes:
        -user: user who is currently logged in to the system
        -bid: The bid to be removed/close down
    Short description:
        Responsible for offer related operations :
        - closed_done_by_time: Responsible for closing down the bid when the time has run out:
            - open bid: 30 mins
            - Close bid: 7 Days
        - close_down_accepted: Responsible for closing down the bid when the user has accepted an offer
    """

    def __init__(self, user, bid):
        self.user = user
        self.bid = bid

    def close_down_by_time(self):
        """
        Short description:
            - when the bid is an open bid:
                1) checks if there are offers made by tutors to the student for the particular bid
                2) if offers exist, choose the latest offer made
                3) Call contractCreator to create the bid based on that offer
                4) Close down the bid in the API
            - when the bid is a closed bid:
                1) Close down the bid in the API

        :return: None
        """
        # the case when the open bid is closed with no offers
        if 'offers' in self.bid.get_additional_info() and not len(self.bid.get_offers()) == 0:
            if isinstance(self.bid, OpenBid):
                offers = self.bid.get_offers()

                final_offer = offers[0]
                for i in range(1, len(offers)):
                    if final_offer.get_date_created() <= offers[i].get_date_created():
                        final_offer = offers[i]
                offer_initiator = UserAdapter().get_user_id(final_offer.get_initiator_id())
                ContractCreator(self.user).create_contract_by_offer(self.bid, final_offer, offer_initiator)

        # Date closed down
        self.close_down_accepted()

    def close_down_accepted(self):
        """
        Short description:
            - Closes down a bid when an offer made by the tutor has been accepted by the student
        :return: None
        """
        # closes down the bid when it is accepted
        # Date closed down
        date_closed = datetime.now()
        date_closed = date_closed.isoformat()[:-3] + 'Z'

        date_closed = {
            "dateClosedDown": date_closed
        }
        Bid_API_access().close_down_bid(self.bid.get_id(), date_closed)


class Chat:
    """
    Parameters:
        -user: user who is currently logged in to the system
        -offer: offer which is being viewed at the moment
        -bid: bid which is being viewed at the moment


    Short description:
        Called when a new message is to be sent: reformat the message and adds it to the api
    """
    def __init__(self, user, bid, offer):
        self.user = user
        self.bid = bid
        self.offer = offer

    def send_message(self, content):
        """
        Inputs:
            - content: content of the message to be sent
        Return: None
        Short description:
            1) Reformat the message to the proper API format
            2) Uploads the new message to the API
        """
        # acesses the API for messages
        api_access = Message_API_access()

        # gets the date and time when the message is sent in isoformat
        date_created = datetime.now()
        date_created_isoformat = date_created.isoformat()[:-3] + 'Z'

        # setting up the receiver id
        if isinstance(self.user, Student):
            additional_info = {
                "receiver_id": self.offer.get_initiator_id()
            }
        else:
            additional_info = {
                "receiver_id": self.bid.get_initiator().get_id()
            }

        # creating the message in the format required to upload it to the API
        new_message = \
            {
                "bidId": self.bid.get_id(),
                "posterId": self.user.get_id(),
                "datePosted": date_created_isoformat,
                "content": content,
                "additionalInfo": additional_info
            }

        # load a new message to the api
        api_access.add_new_message(new_message)


