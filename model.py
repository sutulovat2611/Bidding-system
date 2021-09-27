from abc import ABC



class User(ABC):
    """
    The abstract class which holds all the data, which will be used by any kind of the user.
    """

    def __init__(self, id: str, username: str, given_name: str, family_name: str):
        self.id = id
        self.given_name = given_name
        self.family_name = family_name
        self.competencies = []
        self.qualifications = []
        self.username = username
        self.ongoing_contracts = []
        # attribute that represents contracts that are one month from expiry date
        self.expiring_contracts = []
        # attribute that represents contracts that are pending and not signed
        self.pending_contracts = []


    # getters
    def get_id(self):
        """
        :return: the user's id
        """
        return self.id

    def get_full_name(self):
        """

        :return: the user's full name
        """
        return self.given_name + " " + self.family_name

    def get_username(self):
        """

        :return: the user's username
        """
        return self.username

    def get_competencies(self):
        """

        :return: list of the user's competencies
        """
        return self.competencies

    def get_qualifications(self):
        """

        :return: list of the user's qualifications
        """
        return self.qualifications

    def get_ongoing_contracts(self):
        """
        :return: list of the ongoing contracts the user is involved in
        """
        return self.ongoing_contracts

    def get_expiring_contracts(self):
        """
        :return: list of the expiring contracts the user is involved in
        """
        return self.expiring_contracts

    def get_competency(self, subject_name):
        """
        Inputs:
            - subject_name: name of the subject to search the competency in
        Return:
            - the subject object with the subject_name, if the user has a competency in it, None otherwise
        Short description:
            searches through the subjects that the user has a competency level in, looking
            for the subject with the subject_name
        """
        for i in self.competencies:
            if i.get_subject().get_name() == subject_name:
                return i
        return None

    def add_qualification(self, qualification):
        """
        Inputs:
            - qualification: instance of the qualification class
        Return: None
        Short description:
            Adds the qualification to the list of qualifications
        """
        self.qualifications.append(qualification)

    def add_competency(self, competency):
        """
        Inputs:
            - competency: instance of the competency class
        Return: None
        Short description:
            Adds the competency to the list of competencies
        """
        self.competencies.append(competency)

    def add_ongoing_contract(self, contract):
        """
        Inputs:
            - contract instance of the contract class
        Return: None
        Short description:
            Adds the contract to the list of ongoing contracts
        """
        self.ongoing_contracts.append(contract)

    def add_pending_contract(self, contract):
        """
        Inputs:
            - contract instance of the contract class
        Return: None
        Short description:
            Adds the contract to the list of pending contracts
        """
        self.pending_contracts.append(contract)

    def set_competencies(self, competencies):
        """
        Inputs:
            - competencies: List of Competency classes
        Return: None
        Short description:
            sets the user competencies to the Competency list provided
        """
        self.competencies = competencies

    def set_qualifications(self, qualifications):
        """
        Inputs:
            - qualifications: List of Qualification classes
        Return: None
        Short description:
            sets the user qualifications to the Qualification list provided
        """
        self.qualifications = qualifications

    def set_ongoing_contracts(self, contracts):
        """
        Inputs:
            - contracts: List of Contract classes
        Return: None
        Short description:
            sets the user ongoing contracts to the Contract list provided
        """
        self.ongoing_contracts = contracts

    def set_expiring_contracts(self, contracts):
        """
        Inputs:
            - contracts: List of Contract classes that are one month from expiring date
        Return: None
        Short description:
            sets the user expiring contracts to the Contract list provided
        """
        self.expiring_contracts = contracts

    def remove_contract(self, contract_id):
        """
        Inputs:
            - contract_id: the contract to delete
        Return: None
        Short description:
            Removes the following contract from the user's contracts
        """
        # Update ongoing contract
        new_contracts = []
        for c in self.ongoing_contracts:
            if not c.get_id() == contract_id:
                new_contracts.append(c)
        self.ongoing_contracts = new_contracts

        # Update pending contract
        new_contracts = []
        for c in self.pending_contracts:
            if not c.get_id() == contract_id:
                new_contracts.append(c)
        self.pending_contracts = new_contracts

        # Update expiring contracts
        new_contracts = []
        for c in self.expiring_contracts:
            if not c.get_id() == contract_id:
                new_contracts.append(c)
        self.expiring_contracts = new_contracts


class Student(User):
    """
       The subclass of the User class , which has the array of bids_created
    """

    def __init__(self, id: str, username: str, given_name: str, family_name: str):
        super().__init__(id, username, given_name, family_name)
        self.bids_created = []

    # getters
    def get_bids(self):
        """

        :return: the bids created by the student
        """
        return self.bids_created

    def add_bids(self, bid):
        """
        Inputs:
            -bid : instance of the bid class
        Return: None
        Short description:
            Adds the bid to the bids_created array
        """
        self.bids_created.append(bid)

    def empty_bids(self):
        """
        Inputs: None
        Return: None
        Short description:
            Empties the array of bids_created
        """
        self.bids_created = []

    def set_bids(self, bids):
        """
        Inputs:
            - bids: list of bids
        Return: None
        Short description:
            Sets the students bids to the list that was passed as a parameter
        """
        self.bids_created = bids


class Tutor(User):
    """
        The subclass of the User class , which has the array of offers
    """

    def __init__(self, id: str, username: str, given_name: str, family_name: str):
        super().__init__(id, username, given_name, family_name)
        self.offers = []
        self.monitor_bids = []

    def add_offer(self, offer):
        """
        Inputs:
            - offer: instance of the offer class
        Return: None
        Short description:
            Adds the offer to the offers array
        """
        date_and_time = []
        for i in range(len(offer['dayAndTime'])):
            date_and_time.append(
                {'day': offer['dayAndTime'][i]['day'], 'timeHour': offer['dayAndTime'][i]['timeHour'],
                 'timeMin': offer['dayAndTime'][i]['timeMin']}
            )

        self.offers.append(
            Offer(offer['bidId'], offer['initiatorId'], offer['dateCreated'], date_and_time, offer['sesPerWeek'],
                  offer['rate'], offer['rateType'], offer['duration'], offer['freeClass'], offer['contractLen']))
        return self.offers

    def update_offer(self, bid_id):
        """
        Inputs:
            - bid_id : id of the bid to be updates
        Return: None
        Short description:
            Removes the offer that the tutor sent for the bid with the id=bid_id
        """
        updated_offers = []
        for i in range(len(self.offers)):
            if self.offers[i].get_bid_id() != bid_id:
                updated_offers.append(self.offers[i])

        self.offers = updated_offers

    def add_monitor_bids(self, bid):
        """
        Inputs:
            - bid: instance of the bid class to be added tutor's monitor list
        Return:
            - True, if the bid was successfully added
            - False, if the bid was found in the list
        Short description:
            Checks whether the bid was previously added to the monitor list, and if it was not adds it.
        """
        for i in self.monitor_bids:
            if i.get_id() == bid.get_id():
                return False
        self.monitor_bids.append(bid)
        return True

    def set_monitor_bids(self, monitor_bids):
        """
        Inputs:
            - monitor_bids: List of bids that the Tutor is monitoring
        Return: None
        Short description:
            sets the user monitor list to the bids list provided
        """
        self.monitor_bids = monitor_bids

    def get_monitor_bids(self):
        """

        :return: list of the bids that the Tutor is monitoring
        """
        return self.monitor_bids


class Subject:
    """
        The class, which represents the subject
    """

    def __init__(self, id: str, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description

    # getters
    def get_name(self):
        """

        :return: the subject name
        """
        return self.name

    def get_description(self):
        """

        :return: the subject description
        """
        return self.description

    def get_id(self):
        """

        :return: the subject ID
        """
        return self.id

    # setters
    def set_id(self, id):
        """
        Set the subject id to the parameter provided
        :param id: id we want the subject id to equate to
        """
        self.id = id

    def __str__(self):
        """
        :return: String representation of the subject
        """
        return self.get_name() + ": " + self.get_description()


class Contract:
    """The class, which represents the contract"""

    def __init__(self, id: str, first_party: User, second_party: User, subject: Subject, date_created: str,
                 date_signed: str, expiry_date: str):
        self.id = id
        self.first_party = first_party
        self.second_party = second_party
        self.subject = subject
        self.date_created = date_created
        self.date_sign = date_signed
        self.expiry_date = expiry_date
        self.lesson_info = {"day": [], "timeHour": [], "timeMin": []}
        self.additional_info = {}
        self.payment_info = []

    # getters
    def get_id(self):
        """

        :return: the contract id
        """
        return self.id

    def get_subject(self):
        """

        :return: The subject of the contract
        """
        subject = self.subject
        return subject

    def get_expiry_date(self):
        """

        :return: The expiry date of the contract
        """
        expiry_date = self.expiry_date
        return expiry_date

    def get_date_created(self):
        """

        :return: the date the contract was created
        """
        date = self.date_created
        return date

    def get_date_signed(self):
        """

        :return: the date the contract was signed
        """
        date = self.date_sign
        return date

    def get_first_party(self):
        """

        :return: first party user involved in the contract
        """
        return self.first_party

    def get_second_party(self):
        """

        :return: second party user involved in the contract
        """
        return self.second_party

    def get_lesson_info(self):
        """

        :return: the lesson(s) information agreed on in the contract
        """
        return self.lesson_info

    def get_additional_info(self):
        """

        :return: additional information regarding the contract agreement
        """
        return self.additional_info

    def get_competency(self):
        """

        :return: competency that is required in this contract
        """
        return self.additional_info['subjectLevel']

    # setters
    def set_additional_info(self, additional_info):
        """
        set the additional information of the contract
        :param additional_info: the additional information we want the contract additional information to equate to

        """
        self.additional_info = additional_info

    def set_lesson_info(self, lesson_info):
        """
        set the lesson information of the contract
        :param lesson_info: the lesson information we want the contract lesson information to equate to

        """
        self.lesson_info = lesson_info

    def add_lesson_info(self, day, time_hour, time_min):
        """
        Inputs:
            - day: string storing the weekday
            - timeHour: string storing the time in hour
            - timeMin: string storing the time in mins
        Return: None
        Short description:
            Adds the day, time_hour and time_min to the lesson info
        """
        self.lesson_info['day'].append(day)
        self.lesson_info['timeHour'].append(time_hour)
        self.lesson_info['timeMin'].append(time_min)

    # getters for the string representation
    def get_summary(self):
        """

        :return: Gets summary representation of the contract: The subject summary and the expiry date of the contract
        """
        return "Subject: " + self.get_subject().__str__() + ", Expiry date: " + self.get_expiry_date()[:-14] + " " + \
               self.get_expiry_date()[11:-8]

    def get_parties(self):
        """

        :return: The full name of both parties involved in the contract
        """
        return self.first_party.get_full_name() + " and " + self.second_party.get_full_name()

    def set_sign_date(self, date_signed):
        """

        :return: the date when the contract was signed
        """
        self.date_sign = date_signed

    def __eq__(self, other):
        """
        User to compare two instances of contract objects
        :return:
            - True if both contracts are the same
            - False if contracts are different
        """
        if not isinstance(other, Contract):
            # don't attempt to compare against unrelated types
            return NotImplemented
        if self.get_first_party().get_id() == other.get_first_party().get_id():
            if self.get_second_party().get_id() == other.get_second_party().get_id():
                if self.get_subject().get_id() == other.get_subject().get_id():
                    if self.get_date_created() == other.get_date_created():
                        if self.get_expiry_date() == other.get_expiry_date():
                            if self.get_lesson_info() == other.get_lesson_info():
                                if self.get_additional_info() == other.get_additional_info():
                                    return True
        return False


class Bid(ABC):
    """
    The abstract class which holds all the data, which is shared between both kinds of Bids
    """

    def __init__(self, id: str, initiator: User, day_created: str, day_closed: str, subject: Subject):
        self.id = id
        self.initiator = initiator
        self.date_created = day_created
        self.date_closed = day_closed
        self.subject = subject
        self.additional_info = {}

    # getters
    def get_id(self):
        """

        :return: the bid id
        """
        return self.id

    def get_initiator(self):
        """

        :return: the initiator of the bid
        """
        return self.initiator

    def get_date_created(self):
        """

        :return: the day the bid is created
        """
        return self.date_created

    def get_date_closed(self):
        """

        :return: the day the bid is closed
        """
        return self.date_closed

    def get_subject(self):
        """

        :return: the subject of the bid
        """
        return self.subject

    def get_additional_info(self):
        """

        :return: the additional information of the bid
        """
        return self.additional_info

    def get_offers(self):
        """

        :return: the offers made for this bid
        """
        return self.additional_info['offers']

    def set_additional_info(self, additional_info):
        """
        Inputs:
            - additional_info: dictionary that contains the additional info for this bid
        Return: None
        Short description:
            Loops through the offers in the additional_info dictionary and initialises each offer
            as the new object of the Offer class, adding each of it to the array of offers of this
            bid.
        """
        self.additional_info = additional_info
        offer_list = []

        if 'offers' in additional_info:

            for offer in additional_info['offers']:
                if 'contractLen' in offer:
                    contract_len = offer['contractLen']
                else:
                    contract_len = 0
                o = Offer(offer['bidId'], offer['initiatorId'], offer['dateCreated'], offer['dayAndTime'],
                          offer['sesPerWeek'], offer['rate'], offer['rateType'], offer['duration'],
                          offer['freeClass'], contract_len)

                offer_list.append(o)

            self.additional_info['offers'] = offer_list

    def add_offer(self, offer):
        """
        Inputs:
            - offer:  dictionary that contains the offer information
        Return: None
        Short description:
            Reformat the offer from dictionary to the new Offer class object and adds that object to the
            array of offers for this bid
        """
        o = Offer(offer['bidId'], offer['initiatorId'], offer['dateCreated'], offer['dayAndTime'],
                  offer['sesPerWeek'], offer['rate'], offer['rateType'], offer['duration'],
                  offer['freeClass'], offer['contractLen'])
        self.additional_info['offers'].append(o)

    def remove_offer(self, initiator_id):
        """
        Inputs:
            - initiator_id: if of the offer's initiator
        Return: None
        Short description:
            Removes the offer that was sent by the Tutor with the initiator_id from the list of offers
            of this bid
        """
        updated_offers = []
        offers = self.get_offers()
        for i in range(len(offers)):
            if offers[i].get_initiator_id() != initiator_id:
                updated_offers.append(offers[i])
        offers = updated_offers
        self.update_offers(offers)

    def update_offers(self, offers):
        """

        :return: updates the offers that belong to the bid
        """
        self.additional_info['offers'] = offers


class OpenBid(Bid):
    """
        The subclass of Bid class with the type='open'
    """

    def __init__(self, id: str, initiator: User, day_created: str, day_closed: str, subject: Subject):
        super().__init__(id, initiator, day_created, day_closed, subject)


class CloseBid(Bid):
    """
    The subclass of Bid class with the type='close'
    """

    def __init__(self, id: str, initiator: User, day_created: str, day_closed: str, subject: Subject):
        super().__init__(id, initiator, day_created, day_closed, subject)
        self.messages = []

    def get_messages(self):
        """

        :return: Messages exchanged between tutor and the student regarding the bid
        """
        return self.messages


class MessageClass:
    """
    The class, which represents the Message
    """

    def __init__(self, id: str, bid_id: str, poster_id: str, date_posted: str, content: str, additional_info):
        self.id = id
        self.bid_id = bid_id
        self.poster_id = poster_id
        self.date_posted = date_posted
        self.content = content
        self.additional_info = additional_info

    # getters
    def get_id(self):
        """

        :return: the message id
        """
        return self.id

    def get_bid_id(self):
        """

        :return: the bid id of which the message belongs to
        """
        return self.bid_id

    def get_poster_id(self):
        """

        :return: the id of the user that posted the message
        """
        return self.poster_id

    def get_date_posted(self):
        """

        :return: the date that the message is posted
        """
        return self.date_posted

    def get_content(self):
        """

        :return: the content of the message
        """
        return self.content

    def get_additional_info(self):
        """

        :return: additional information belonging to the message
        """
        return self.additional_info


class Qualification:
    """
    The class, which represents the Qualification
    """

    def __init__(self, id: str, title: str, description: str, verified: bool):
        self.id = id
        self.title = title
        self.description = description
        self.verified = verified

    # getters
    def get_title(self):
        """

        :return: title of the qualification
        """
        return self.title

    def get_description(self):
        """

        :return: the description of the qualification
        """
        return self.description

    def get_verified(self):
        """

        :return: True - if the qualification is verified and False - otherwise
        """
        return self.verified

    # methods that are required for string representation
    def __len__(self):
        """

        :return: length of the summary of the qualification
        """
        length = self.get_title() + ", " + self.get_description()
        return len(length)

    def __str__(self):
        """

        :return: string representation the qualification
        """
        if self.verified:
            return self.get_title() + ", " + self.get_description()
        else:
            return ""


class Competency:
    """
    The class, which represents the Competency
    """

    def __init__(self, id: str, subject: Subject, level: int):
        self.id = id
        self.subject = subject
        self.level = level

    # getters
    def get_subject(self):
        """

        :return: the competency subject
        """
        return self.subject

    def get_level(self):
        """

        :return: the level of the competency
        """
        return self.level

    # methods that are required for string representation
    def __len__(self):
        """

        :return: length of the string representation of the summary
        """
        length = self.get_subject().__str__() + ", level = " + str(self.get_level())
        return len(length)

    def __str__(self):
        """

        :return: the string representation of the summary
        """
        return self.get_subject().__str__() + ", level = " + str(self.get_level())


class UserCollection:
    """
        The class, which represents the collection of User objects
    """

    def __init__(self):
        self.index = -1
        self.users = []

    # setters
    def set_users(self, users):
        """

        :param users: the users we want out users attribute to equate to
        """
        self.users = users

    def add_user(self, user: User):
        """
        Inputs:
            - User: object of the User class
        Return: None
        Short description:
            Adds the user to the users array
        """

        self.users.append(user)

    # methods needed to iterate through the class
    def __iter__(self):
        """
        Allows the class to be iterable
        """
        return self

    def __next__(self):
        """
        Allows the class to be iterable
        """
        self.index += 1
        if self.index >= len(self.users):
            self.index = -1
            raise StopIteration()
        else:
            return self.users[self.index]


class Offer:
    """
    The class, which represents the Offer
    """

    def __init__(self, bid_id, initiator_id, date_created: str,
                 day_and_time: list, sessions: int, rate: int, rate_type: str, duration: int, free_class: bool, contract_len):
        self.bid_id = bid_id
        self.initiator_id = initiator_id
        self.day_and_time = day_and_time
        self.ses_per_week = sessions
        self.date_created = date_created
        self.rate = rate
        self.rate_type = rate_type  # per hour or per session
        self.duration = duration
        self.free_class = free_class
        self.contract_len = contract_len

    # getters
    def get_bid_id(self):
        """

        :return: the bid id of which the offer belongs to
        """
        return self.bid_id

    def get_initiator_id(self):
        """

        :return: the id of the initiator of the offer
        """
        return self.initiator_id

    def get_day_and_time(self):
        """

        :return: information regarding when and what time will the classes be held
        """
        return self.day_and_time

    def get_ses_per_week(self):
        """

        :return: number of sessions offered
        """
        return self.ses_per_week

    def get_date_created(self):
        """

        :return: date the offer was created
        """
        return self.date_created

    def get_rate(self):
        """

        :return: the rate of the offer initiator
        """
        return self.rate

    def get_rate_type(self):
        """

        :return: the type of rate (per session/ per hour)
        """
        return self.rate_type

    def get_duration(self):
        """

        :return: the duration of each session offered
        """
        return self.duration

    def get_free_class(self):
        """

        :return: True - If free class offered. False - otherwise
        """
        return self.free_class

    def get_contract_len(self):
        """
        :return: The length of contract that is offered by the tutor
        """
        return self.contract_len



