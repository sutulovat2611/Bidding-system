from logic import Student, UserAdapter, LoginMechanism, BidAdapter, BidCreator, ContractCreator, OfferAdapter, \
    Chat, MessagesAdapter, CloseDownBid, ContractAdapter, BidUpdater, ContractsSort
from view import LoginView, ProfileView, ChatView, BidsListView, ChooseBidView, CreateBidView, \
    BidInfoView, CreateOfferView, OfferInfoView, ContractInfoView, ContractsListView, END, NORMAL, DISABLED, \
    ChooseNewContractView, ReuseContractView, NewTermsContractView, ChooseTutorForContractView
from tkinter import messagebox
from datetime import datetime


class LoginController:
    """
        Attributes:
            None
        Short description:
            Initializes the LoginView page and controls it afterwards
    """

    def __init__(self):
        LoginView(self)

    def login_btn(self, username, password, login):
        """
        Inputs:
            -username: username which was input by the user
            -password: password that was input by the user
            -login: instance of the LoginView view page
        Return: None
        Short description:
             Calls the mechanism that verifies the credential.
             Allows to proceed to the profile page if the credentials are valid.
             Otherwise shows the proper message and allows to reenter credentials
        """
        l = LoginMechanism(username, password)
        verified_user = l.verify()
        if verified_user is not None:
            login.root.destroy()
            ProfileController(verified_user, "Login")
        else:
            messagebox.showerror("showerror", "This account does not exist. Try again")


class ProfileController:
    """
     Parameters:
         -user: user who is currently logged in to the system
         -initialisation: Indicates where the Profile controller is called from:
            -  "Login": If its called from login page
            - "Back": If its called from other pages

     Short description:
         Initializes the ProfileView page and controls it afterwards, allowing:
            1) Tutor and Student to:
                - log out of the app, redirecting them to LoginView
                - proceed to the ContractsListView to see their existing contracts
            2) Tutor:
                - proceed to the BidsListView page, which will represent all the available for them bids
                - proceed to the OffersBidsListView page, which will represent only the bids that he/she sent an
                offer to
            3) Student:
                - proceed to the BidsListView page, which will represent all their instantiated bids
     """

    def __init__(self, user, initialisation):
        self.user = user
        ProfileView(self.user, self, initialisation)

    def bids_list_btn(self, view):
        """
        Inputs:
            - view: instance of the ProfileView page
        Return: None
        Short description:
                Calls the  BidsListController which will redirect the user to the  BidsListView page
        """
        view.root.destroy()
        BidsListController(self.user)

    def log_out_btn(self, view):
        """
        Inputs:
            - view: instance of the ProfileView page
        Return: None
        Short description:
            Calls the LoginController() which will redirect the user to the LoginView page
        """
        view.root.destroy()
        LoginController()

    def tutor_offers_btn(self, view):
        """
        Inputs:
            - view: instance of the ProfileView page
        Return: None
        Short description:
            Calls the OffersBidsListController() which will redirect the user to the BidsListView page
        """
        view.root.destroy()
        OffersBidsListController(self.user)

    def contracts_btn(self, view):
        """
        Inputs:
            - view: instance of the ProfileView page
        Return: None
        Short description:
            Calls the ContractsListController() which will redirect the user to the ContractsListView page
        """
        view.root.destroy()
        ContractsListController(self.user)

    def monitor_page_btn(self, view):
        """
        Inputs:
            - view: instance of the ProfileView page
        Return: None
        Short description:
            Calls the MonitorPageController() which will redirect the user to the BidsListView page
        """

        view.root.destroy()
        MonitorPageController(self.user)


class BidsListController:
    """
    Attributes:
        -user: user who is currently logged in to the system
        -bids: up-to-date bids that - are initiated by the student if the user is the Student
                                    - are available for the tutor based on his competency if the user is Tutor

    Short description:
        Initializes the BidsList page calling the GetBids() class to sort out the bids to represents and Controls the page
        by responding to the user input (clicking buttons, etc)
    """

    def __init__(self, user):
        self.user = user
        if isinstance(self.user, Student):
            self.bids = BidAdapter().get_student_bids(self.user.get_id())
        else:
            self.bids = BidAdapter().get_tutor_bids(self.user.get_id())
        BidsListView(self, self.bids, self.user)

    def create_bid_btn(self, view):
        """
        Inputs:
            - view: instance of the BidsListView page
        Return: None
        Short description:
            Checks whether the student is not exceeding their limit on
            bids and contracts, restricting it to the maximum number of bids = 5 - number of existing
            contracts.
            If student is exceeding the limit an error message will appear else the student will be redirected to
            ChooseBidView.
        """

        if len(self.user.get_ongoing_contracts()) + len(self.bids) >= 5:
            messagebox.showerror("showerror", "The number of contracts and bids exceed the limit. "
                                 + str(len(self.user.get_ongoing_contracts())) + " contracts and " + str(len(self.bids))
                                 + " bids.")
        else:
            view.root.destroy()
            ChooseBidController(self.user)

    def show_bid_btn(self, view, bid):
        """
        Inputs:
            - view: instance of the BidsListView page
            - bid: instance of the bid to be viewed
        Return: None
        Short description:
            Calls the BidInfoController which will redirect the user to the BidInfoView page in order to
            represent more detailed information on the chosen bid
        """
        view.root.destroy()
        BidInfoController(self.user, bid, False)

    def back_btn(self, view):
        """
        Inputs:
            - view: instance of the BidsListView page
        Return: None
        Short description:
            Calls the ProfileController which will redirect the user to the ProfileView page
        """
        view.root.destroy()
        ProfileController(self.user, "Back")


class ChooseBidController:
    """
    Attributes:
        -user: user who is currently logged in to the system
    Short description:
        Controls the view that gives the user two options, whether to open an Open bid or Close bid
    """

    def __init__(self, user):
        self.user = user
        ChooseBidView(self)

    def open_bid_btn(self, view):
        """
        Inputs:
            - view: instance of the ChooseBidView page
        Return: None
        Short description:
            Redirects the user to the CreateBidView page, sending the 'open' type to it's controller
        """
        view.root.destroy()
        CreateBidController(self.user, 'open')

    def close_bid_btn(self, view):
        """
        Inputs:
            - view: instance of the ChooseBidView page
        Return: None
        Short description:
            Redirects the user to the CreateBidView page, sending the 'close' type to it's controller
        """
        view.root.destroy()
        CreateBidController(self.user, 'close')

    def cancel_bid_btn(self, view):
        """

        :param view: instance of the ChooseBidView page
        :return: None
        Short Description: redirects the user to BidsListsView page
        """
        view.root.destroy()
        BidsListController(self.user)


class CreateBidController:
    """
    Parameters:
        -user: user who is currently logged in to the system
        -type_bid: type of the bid to be created

    Attributes:
        -CreateBidView: page that is being created and controlled by this controller class

    Short description:
        Initializes the CreateBidView page based on the type of the bid that user has chosen and controls it afterwards.
        Creates new bid, based on all the information that the user input by calling the BidCreator class and
        passing the bid type there.
    """

    def __init__(self, user, type_bid):
        self.user = user
        self.type_bid = type_bid
        # checking what type the bid to be created is
        if self.type_bid == 'open':
            CreateBidView(self, 'Open')
        else:
            CreateBidView(self, 'Close')

    def submit_form(self, bid_info, lesson_info, view):
        """
        Inputs:
            - bid_info: Information regarding the bid created
            - lesson_info: Information regarding the lesson required by bid creator
            - view: instance of the CreateBidView page
        Return: None
        Short description:
            Gets all the data that was input by the student to create the bid and formats it properly.
            Calls the BidCreator passing the bid type and formatted data and redirects the user back to the
            BidListView page
        """
        # Configuring contract length
        if lesson_info["customContract"].get():
            contract_len = str(lesson_info["contractLen"].get())
        else:
            contract_len = 6

        additional_info = {'subjectLevel': bid_info["subjectLevel"], 'contractLen': contract_len,
                           'qualificationTitle': bid_info["qualificationTitle"],
                           'sesPerWeek': lesson_info["sesPerWeek"],
                           'hoursPerLesson': lesson_info["hoursPerLes"],
                           'dayAndTime': [], 'rate': lesson_info["rate"].get(),
                           'rateType': lesson_info["rateType"].get(),
                           'offers': []}

        for i in range(len(lesson_info["day"])):
            additional_info['dayAndTime'].append(
                {'day': lesson_info["day"][i].get(), 'timeHour': lesson_info["timeHour"][i].get(),
                 'timeMin': lesson_info["timeMin"][i].get()})

        # call to the mechanism that creates the bid
        BidCreator(self.user).create_bid(self.type_bid, bid_info["subjectName"], bid_info["subjectDescription"],
                                         additional_info)

        view.root.destroy()
        BidsListController(self.user)

    def cancel_btn(self, view):
        """
        Short description:
            1) destroys CreateBidView
            2) redirects the user to the BidslistView """
        view.root.destroy()
        BidsListController(self.user)


class BidInfoController:
    """

        Attributes:
            -user: user who is currently logged in to the system
            -bid: bid which is being viewed at the moment
            - initiators: tutors who sent offers for the following bid

        Short description:
            Uses UserAdapter() class to get the initiators of offers in the bid being viewed
            Initializes the BidInfoView page and controls it afterwards, allowing:
                1) The student to:
                    - see all the offers for the following bid
                2) The tutor to:
                    - make an offer
                    - buy out the bid if its an OpenBid
                    - see all the offers for the following bid if it's an open bid
                    - see only an offer that was sent by him/her if it's a close bid
                3) Both:
                    - go back to the ProfileView page
    """

    def __init__(self, user, bid, is_monitor):
        self.user = user
        self.bid = bid
        self.is_monitor=is_monitor
        self.initiators = UserAdapter().get_offer_initiators(bid)
        BidInfoView(self, self.user, self.bid, self.initiators, is_monitor)

    def make_offer_btn(self, view):
        """
        Inputs:
            - view: instance of the BidInfoView page
        Return: None
        Short description:
            Calls the CreateOfferController which will redirect the user to the ChooseBidView page in order to proceed
            to new offer creation
        """
        view.root.destroy()
        CreateOfferController(self.user, self.bid, self.is_monitor)

    def open_offer_btn(self, view, offer):
        """
        Inputs:
            - view: instance of the BidInfoView page
            - offer: instance of an offer to be viewed
        Return: None
        Short description:
            Calls the OfferInfoController which will redirect the user to the OfferInfoView page,
            representing the info about the chosen offer
        """
        view.root.destroy()
        OfferInfoController(self.user, offer, self.bid, self.is_monitor)

    def back_btn(self, view):
        """
        Inputs:
            - view: instance of the BidInfoView page
        Return: None
        Short description:
            Calls the ProfileController which will redirect the user to the ProfileView page
        """
        view.root.destroy()
        ProfileController(self.user, "Back")

    def buy_out_btn(self, view):
        """
        Inputs:
            - view: instance of the BidInfoView page
        Return: None
        Short description:
            Calls the ContractCreator class's method which creates a contract based on the information from the bid.
            Calls the CloseDownBid, which will close down the following bid
            Calls the ContractInfoController which will redirect the user to the ContractInfoView page,
            representing the info of the newly created contract
        """
        view.root.destroy()
        # create contract
        contract = ContractCreator(self.user).create_contract_buy_out(self.bid)
        # delete the bid from the API
        CloseDownBid(self.user, self.bid).close_down_accepted()
        # Go to contract view
        ContractInfoController(self.user, contract)

    def monitor_btn(self):
        """
        Inputs: None
        Return: None
        Short description: Adds the bid to the tutor's monitor list and notifies the user that the bid was successfully
        added. If the bis was in the tutor's monitor list, the system notifies the user about that
        """
        successful = UserAdapter().monitor_bid(self.user, self.bid)
        # if already added alert
        if not successful:
            messagebox.showerror("showerror", "The following bid is already in your monitor list")
        # if not then alert the bid was successfully added to the monitor list
        else:
            messagebox.showinfo("information", "Successfully added to monitoring list")

    def monitor_update(self, view):
        BidUpdater([self.bid])
        view.root.destroy()
        BidInfoController(self.user, self.bid, True)


class CreateOfferController:
    """
    Attributes:
        -user: user who is currently logged in to the system
        -bid: bid which is being viewed at the moment

    Short description:
        Initializes the CreateOfferView page and controls it afterwards, allowing
        the tutor to submit the offer with all the required info
    """

    def __init__(self, user, bid, is_monitor):
        self.user = user
        self.bid = bid
        self.is_monitor=is_monitor
        CreateOfferView(self, self.user, self.bid)

    def submit_form(self, offer_info, view):
        """
        Inputs:
            - offer_info: the information required to create the offer that is provided by the tutor
            - view: instance of the CreateOfferView page
        Return: None
        Short description:
            Gets all the data that was input by the student to create the offer.
            Creates an offer and adds it to the bid list of offers and user list of offers
            Calls the OfferAdapter that is responsible for Offer creation in the API
            After the offer is created, returns the user back to the BidInfoView page
        """

        # Creating date when the offer is created in isoformat
        date_created = datetime.now()
        date_created_isoformat = date_created.isoformat()[:-3] + 'Z'

        # Contract len
        if offer_info['customContract']:
            contract_len = offer_info['contractLen'].get()
        else:
            contract_len = 6

        # Creating offer dictionary to load to the API
        offer = {
            'bidId': self.bid.get_id(),
            'initiatorId': self.user.get_id(),
            'dateCreated': date_created_isoformat,
            'sesPerWeek': str(offer_info["sesPerWeek"]),
            'duration': str(offer_info["hourPerLes"]),
            'dayAndTime': [],
            'rate': str(offer_info["rate"].get()),
            'rateType': offer_info["rateType"].get(),
            'freeClass': offer_info["freeClass"].get(),
            'contractLen': contract_len
        }
        # adding the day and time in the proper format to the offer dictionary
        for i in range(len(offer_info["day"])):
            offer['dayAndTime'].append(
                {'day': offer_info["day"][i].get(), 'timeHour': offer_info["timeHour"][i].get(),
                 'timeMin': offer_info["timeMin"][i].get()})

        view.root.destroy()

        # calls the mechanism responsible for the offer creation

        mec = OfferAdapter(self.bid)

        # updates the user's offers removing the previous version of the offer
        self.user.update_offer(self.bid.get_id())
        # updates the bid's offers removing the previous version of the offer
        self.bid.remove_offer(self.user.get_id())

        # add the new offer to the user
        self.user.add_offer(offer)
        # add the new offer to the bid
        self.bid.add_offer(offer)
        # Creating new offer
        additional_info_updated = self.bid.get_additional_info()
        mec.update_offers_in_api(self.bid.get_id(), additional_info_updated)

        BidInfoController(self.user, self.bid, self.is_monitor)

    def cancel_btn(self, view):
        """
        Short description:
            1) destroys the creating bid window
            2) Directs the user to the BidInfoView by calling BidInfoController
            """
        view.root.destroy()
        BidInfoController(self.user, self.bid, self.is_monitor)


class MonitorPageController:
    """
        Parameters:
            -user: Tutor who is currently logged in to the system
        Attributes:
            -bids: the bids that the Tutor has added to their monitor bids list

        Short description:
            Initializes the BidsList getting all the bids from the tutor's monitor list
            1) show_bid_btn: represents more detailed information on the chosen bid
            2) back_btn: returns the user back to the ProfileView page
            3) Updates the bids information accordingly every 30 seconds
    """

    def __init__(self, user):
        self.user = user
        self.bids = self.user.get_monitor_bids()
        BidUpdater(self.bids)
        BidsListView(self, self.bids, self.user)

    def show_bid_btn(self, view, bid):
        """
        Inputs:
            - view: instance of the MonitorPageView page
            - bid: instance of the bid to be viewed
        Return: None
        Short description:
            Calls the BidInfoController which will redirect the user to the BidInfoView page in order to
            represent more detailed information on the chosen bid
        """
        view.root.destroy()
        BidInfoController(self.user, bid, True)

    def back_btn(self, view):
        """
        Inputs:
            - view: instance of the MonitorPageView page
        Return: None
        Short description:
            Calls the ProfileController which will redirect the user to the ProfileView page
        """
        view.root.destroy()
        ProfileController(self.user, "Back")


class ContractsListController:
    """
    Attributes:
        -user: user who is currently logged in to the system
    Short description:
        Responsible for Contract related operations :
        - allows the user to see the contracts sorted by:
            - ongoing (signed and not expired)
            - expired (signed but expired)
            - pending (the contract request sent ny the student to the tutor), which isnt signed by the tutor yet
        - back_btn: Sends the user back to their profile page
    """

    def __init__(self, user):
        self.user = user
        self.contracts =[]
        self.contracts= ContractsSort().sort_ongoing(self.user.get_id())
        ContractsListView(self, self.contracts)

    def show_contract_btn(self, view, contract):
        """
        Short Description:
            1) Destroys the view which the user is in
            2) Moves the user to contract info page
        :param view: The view which the user is in
        :param contract: The contract that the user want to view
        :return: None
        """
        view.root.destroy()
        ContractInfoController(self.user, contract)

    def back_btn(self, view):
        """
        Short Description:
            1) Closes the view which the user is in
            2) Redirects the user to the Profile page
        :param view: Instance of contractsListView
        :return: None
        """
        view.root.destroy()
        ProfileController(self.user, "Back")

    def ongoing_btn(self, view):
        """
        Short Description:
            1) Represents ongoing contracts on the page
        :param view: Instance of ContractsListView
        :return: None
        """
        # clear previously shown contracts
        for i in view.all_buttons:
            i.destroy()
        self.contracts= ContractsSort().sort_ongoing(self.user.get_id())
        view.show_contracts(self.contracts)

    def expired_btn(self, view):
        """
        Short Description:
            1) Represents expired contracts on the page
        :param view: Instance of ContractsListView
        :return: None
        """
        # in order to make sure that only 5 latest ones are represented for student
        is_student=isinstance(self.user, Student)
        # clears previously shown contracts
        for i in view.all_buttons:
            i.destroy()
        self.contracts= ContractsSort().sort_expired(self.user.get_id(), is_student)
        view.show_contracts(self.contracts)

    def pending_btn(self,view):
        """
        Short Description:
            1) Represents pending contracts (contract request which is nor signed by the tutor) on the page
        :param view: Instance of ContractsListView
        :return: None
        """
        # clears previously shown contracts
        for i in view.all_buttons:
            i.destroy()
        self.contracts= ContractsSort().sort_pending(self.user.get_id())
        view.show_contracts(self.contracts)


class ContractInfoController:
    """
        Attributes:
            -user: user who is currently logged in to the system
            -contract: The contract which the user wants to view
        Short description:
            - Controlling the page which shows the contract information
            - back_btn: Sends the user back to the page that shows the list of their contracts
            - sign_with_tutor_btn: shown for the Student only, allows to sign a contract with the same tutor: same terms
                                or new terms
            - reuse_contract_btn: shown for Student only, allows to renew the following contract with the same tutor
                                or with the new tutor
            - accept_btn: shown for Tutor only, when the contract is not signed by the tutor, allowing to sign
            - decline_btn: shown for TUtor only, when contract is nor signed by the tutor, allowing to decline
        """

    def __init__(self, user, contract):
        self.user = user
        self.contract = contract
        ContractInfoView(self, self.contract, self.user)

    def back_btn(self, view):
        """
        Short Description:
            1) Closes the view which the user is in
            2) Redirects the user to the ContractListView page
        :param view: Instance of ContractInfoView
        :return: None
        """
        view.root.destroy()
        ContractsListController(self.user)

    def sign_with_tutor_btn(self, view):
        """
        Inputs:
            - view: instance of the ContractInfoView page
        Return: None
        Short description:
            Checks whether the user is not exceeding the total number of 5 pending contracts + existing contracts + bids.
            If they are, shows the message accordingly, otherwise redirects the user to ChooseNewContractView, allowing
            to choose to renew the contract or to use new terms with the same tutor
        """
        if len(self.user.get_ongoing_contracts()) + len(self.user.get_bids()) >= 5:

            messagebox.showerror("showerror", "The number of contracts and bids exceed the limit. "
                                 + str(len(self.user.get_ongoing_contracts())) + " contracts and " + str(
                len(self.user.get_bids()))
                                 + " bids.")
        else:
            view.root.destroy()
            ChooseNewContractController(self.user, self.contract)

    def reuse_contract_btn(self, view):
        """
        Inputs:
            - view: instance of the ContractInfoView page
        Return: None
        Short description:
            Checks whether the user is not exceeding the total number of 5 pending contracts + existing contracts + bids.
            If they are, shows the message accordingly, otherwise redirects the user to ChooseTutorForContractView, allowing
            to choose the tutor to reuse that contract with
        """
        if len(self.user.get_ongoing_contracts()) + len(self.user.get_bids()) >= 5:
            messagebox.showerror("showerror", "The number of contracts and bids exceed the limit. "
                                 + str(len(self.user.get_ongoing_contracts())) + " contracts and " + str(
                len(self.user.get_bids()))
                                 + " bids.")
        else:
            view.root.destroy()
            ChooseTutorForContractController(self.user, self.contract)

    def accept_btn(self, view):
        """
        Inputs:
            - view: instance of the ContractInfoView page
        Return: None
        Short description:
            Allows the tutor to sign a contract
        """
        date_now = datetime.now()
        ContractAdapter().sign_contract(self.contract, self.contract.get_id(), date_now )
        view.root.destroy()
        ContractInfoView(self, self.contract, self.user)

    def decline_btn(self, view):
        """
        Inputs:
            - view: instance of the ContractInfoView page
        Return: None
        Short description:
            Allows the user to decline the offer, deleting the request
        """
        view.root.destroy()
        ContractAdapter().delete_contract(self.contract.get_id())
        ContractsListController(self.user)


class ChooseNewContractController:
    """
    Attributes:
        -user: user who is currently logged in to the system
        -contract: The contract being viewed
    Short description:
        - Allows to reuse the contract with the same terms (same tutor)
        - Allows to reuse the contract with the new terms (same tutor)
        - cancel_btn: Sends the user back to the page that shows the list of their contracts
    """
    def __init__(self, user, contract):
        self.user = user
        self.contract = contract
        ChooseNewContractView(self)

    def cancel_btn(self, view):
        """
        Inputs:
            - view: instance of the ChooseTutorForContractView page
        Return: None
        Short description:
            Redirects the user to the ContractInfoView page
        """
        view.root.destroy()
        ContractInfoController(self.user, self.contract)

    def reuse_terms_btn(self, view):
        """
        Inputs:
            - view: instance of the ChooseNewContractView page
        Return: None
        Short description:
            Redirects the user to the ReuseContractView, sending respective information about both parties and
            contract
        """
        view.root.destroy()
        if self.user.get_id() == self.contract.get_first_party().get_id():
            tutor = self.contract.get_second_party()
        else:
            tutor = self.contract.get_first_party()
        ReuseContractController(self.user, self.contract, tutor)

    def new_terms_btn(self, view):
        """
        Inputs:
            - view: instance of the ChooseNewContractView page
        Return: None
        Short description:
            Redirects the user to the NewTermsContractView, sending respective information about both parties,
            contract, subject stated in the contract and competency in this subject required in the contract
        """
        view.root.destroy()
        if self.user.get_id() == self.contract.get_first_party().get_id():
            tutor = self.contract.get_second_party()
        else:
            tutor = self.contract.get_first_party()
        NewTermsContractController(self.user, self.contract.get_subject(), tutor, self.contract.get_additional_info()['subjectLevel'])


class ReuseContractController:
    """
    Attributes:
        -user: user who is currently logged in to the system
        -tutor: tutor who the contract request will be sent to
        -contract: instance of the contract that is being renewed
    Short description:
        - Creates new contract request with the same terms as the contract
    """
    def __init__(self, user, contract, tutor):
        self.user = user
        self.contract = contract
        self.tutor = tutor
        ReuseContractView(self, contract, tutor)

    def submit_form(self, customise_contract, contract_len, view):
        """
        Inputs:
            - information_collected: information related to  the contract
            - subject: subject related to the contract
            - subject_level: competency of the tutor in the subject required in the following contract
            - view: instance of the NewTermsContractView page
        Return: None
        Short description:
            Creates the new contract request with the same terms, requesting the tutor to sign/decline.
        """
        view.root.destroy()
        if customise_contract.get():
            contract_len = contract_len.get()
        else:
            contract_len = 6

        # create contract
        contract = ContractCreator(self.user).reuse_contract_unsigned(self.contract, self.tutor, contract_len)
        # Go to contract view
        ContractInfoController(self.user, contract)


class NewTermsContractController:
    """
    Attributes:
        -user: user who is currently logged in to the system
        -tutor: tutor who the contract request will be sent to
        -subject: subject associated with the contract
        -subject_level: competency in the subject associated with the contract
    Short description:
        - Creates new contract with the user input of the new terms
    """
    def __init__(self, user, subject, tutor, subject_level):
        self.user = user
        self.tutor = tutor
        NewTermsContractView(self, user, tutor, subject, subject_level)

    def submit_form(self, information_collected, subject, subject_level, view):
        """
        Inputs:
            - information_collected: information related to  the contract
            - subject: subject related to the contract
            - subject_level: competency of the tutor in the subject required in the following contract
            - view: instance of the NewTermsContractView page
        Return: None
        Short description:
            Creates the new contract request with the new terms, requesting the tutor to sign/decline.
        """

        # getting contract length
        if information_collected['customContract'].get():
            contract_len = information_collected['contractLen'].get()
        else:
            contract_len = 6
        contract_info = {
            "subject": subject,
            "subjectLevel": subject_level,
            "sesPerWeek": information_collected["sesPerWeek"],
            "hoursPerLes": information_collected["hoursPerLes"],
            "rate": information_collected["rate"].get(),
            "rateType": information_collected["rateType"].get(),
            "contractLen": contract_len
        }

        lesson_info = []
        for i in range(len(information_collected["day"])):
            lesson_info.append(
                {'day': information_collected["day"][i].get(), 'timeHour': information_collected["timeHour"][i].get(),
                 'timeMin': information_collected["timeMin"][i].get()})
        # create contract
        contract = ContractCreator(self.user).new_terms_contract_unsigned(self.tutor, contract_info,
                                                                          lesson_info)
        view.root.destroy()
        # Go to contract view
        ContractInfoController(self.user, contract)


class ChooseTutorForContractController:
    """
    Attributes:
        -user: user who is currently logged in to the system
        -contract: The contract being viewed
    Short description:
        - Allows to reuse the contract with the same tutor
        - Allows to reuse the contract with the new tutor, which is being searched by the username
        - back_btn: Sends the user back to the page that shows the list of their contracts
    """

    def __init__(self, user, contract):
        self.user = user
        self.contract = contract
        ChooseTutorForContractView(self)

    def reuse_same_tutor_btn(self, view):
        """
        Inputs:
            - view: instance of the ChooseTutorForContractView page
        Return: None
        Short description:
            Chooses the tutor from the contract and redirects the user to the ReuseContractView page,
            with all the information related to the contract, including the information on the tutor
        """
        view.root.destroy()
        if self.user.get_id() == self.contract.get_first_party().get_id():
            tutor = self.contract.get_second_party()
        else:
            tutor = self.contract.get_first_party()
        ReuseContractController(self.user, self.contract, tutor)

    def reuse_new_tutor_btn(self, username, view):
        """
        Inputs:
            - view: instance of the ChooseTutorForContractView page
            - username: username in the string form
        Return: None
        Short description:
            Checks if the tutor with the following username exists. Gets the tutor by the id calling the
            UserAdapter and checks whether the competency matches the required ( by 2 greater than the stated one).
            If tutor exists and competency matches, redirects the user to ReuseContractView page.
        """
        tutor=UserAdapter().get_user_by_username(username)
        if tutor is None or isinstance(tutor, Student):
            messagebox.showerror("showerror", " The tutor with the following username does not exist, try again ")
        else:
            tutor_comp=tutor.get_competency(self.contract.get_subject().get_name())
            if tutor_comp is None or tutor_comp.get_level()-2 < int(self.contract.get_competency()):
                messagebox.showerror("showerror", " The following tutor does not match the required competency, try another one ")
            else:
                view.root.destroy()
                ReuseContractController(self.user, self.contract, tutor)

    def cancel_btn(self, view):
        """
        Inputs:
            - view: instance of the ChooseTutorForContractView page
        Return: None
        Short description:
            Redirects the user to the ContractInfoView page
        """
        view.root.destroy()
        ContractInfoController(self.user, self.contract)


class OffersBidsListController:
    """
        Parameters:
            -user: user who is currently logged in to the system
        Attributes:
            -bids: up-to-date bids that - are initiated by the student if the user is the Student
                                        - have offers initiated by the user if the user is Tutor

        Short description:
            Initializes the BidsList page calling the BidAdapter class to sort out the bids to represent
            1) show_bid_btn: represents more detailed information on the chosen bid
            2) back_btn: returns the user back to the ProfileView page
    """

    def __init__(self, user):
        self.user = user
        self.bids = BidAdapter().get_tutor_offer_bids(self.user.get_id())
        BidsListView(self, self.bids, self.user)

    def show_bid_btn(self, view, bid):
        """
        Inputs:
            - view: instance of the BidsListView page
            - bid: instance of the bid to be viewed
        Return: None
        Short description:
            Calls the BidInfoController which will redirect the user to the BidInfoView page in order to
            represent more detailed information on the chosen bid
        """
        view.root.destroy()
        BidInfoController(self.user, bid, False)

    def back_btn(self, view):
        """
        Inputs:
            - view: instance of the BidsListView page
        Return: None
        Short description:
            Calls the ProfileController which will redirect the user to the ProfileView page
        """
        view.root.destroy()
        ProfileController(self.user, "Back")


class OfferInfoController:
    """
    Attributes:
        -user: user who is currently logged in to the system
        -offer: offer which is being viewed
        -bid: bid which is being viewed
        -offer_initiator: the creator of the offer being viewed

    Short description:
        Initializes the OfferInfoView page and controls it afterwards, allowing:
            1) The student to:
                - see all the necessary info to evaluate the offer and make their decision
                - decline or accept the offer
                - chat the tutor if it is the close bid
                - return back to BidInfoView()
            2) The tutor to:
                - check information they provided in their offer
                - chat the student if it is the close bid
                - return back to BidInfoView()
    """

    def __init__(self, user, offer, bid, is_monitor):
        self.user = user
        self.offer = offer
        self.bid = bid
        self.is_monitor=is_monitor
        self.offer_initiator = UserAdapter().get_user_id(offer.get_initiator_id())
        OfferInfoView(self, offer, self.offer_initiator, user, bid)

    def back_btn(self, view):
        """
        Inputs:
            - view: instance of the OfferInfoView page
        Return: None
        Short description:
            Calls the BidInfoController which will redirect the user to the BidInfoView page
        """
        view.root.destroy()
        BidInfoController(self.user, self.bid, self.is_monitor)

    def edit_btn(self, view):
        """
        Inputs:
            - view: instance of the OfferInfoView page
        Return: None
        Short description:
            Calls the CreateOfferController which will redirect the user to the CreateOfferView page,
            allowing to edit the offer"""
        view.root.destroy()
        CreateOfferController(self.user, self.bid)

    def open_chat_btn(self, view):
        """
        Inputs:
            - view: instance of the OfferInfoView page
        Return: None
        Short description:
            Calls the ChatController which will redirect the user to the ChatView page
        """
        view.root.destroy()
        ChatController(self.user, self.bid, self.offer)

    def decline_btn(self, view):
        """
        Inputs:
            - view: instance of the OfferInfoView page
        Return: None
        Short description:
            Calls the OfferAdapter to remove the offer being viewed from the bid and redirects the user back to the
            BidInfoView page
        """
        view.root.destroy()
        OfferAdapter(self.bid).remove_offer(self.offer.get_initiator_id())

        # Return to bid
        BidInfoController(self.user, self.bid, self.is_monitor)

    def accept_btn(self, view):
        """
        Inputs:
            - view: instance of the OfferInfoView page
        Return: None
        Short description:
            Calls the ContractCreator to create the contract by taking the info from the offer being viewed.
            Calls the CloseDownBid to close the bid, since the contract was created
            Redirects the user to the ContractInfoView, representing all the info of the newly
            created Contract
        """
        view.root.destroy()
        contract = ContractCreator(self.user).create_contract_by_offer(self.bid, self.offer, self.offer_initiator)
        CloseDownBid(self.user, self.bid).close_down_accepted()
        ContractInfoController(self.user, contract)


class ChatController:
    """
    Parameters:
        -user: user who is currently logged in to the system
        -offer: offer which is being viewed at the moment
        -bid: bid which is being viewed at the moment

    Attributes:
        -messages: the messages that belong to this offer only (between the bid creator and the offer creator)
        -opponent_username: the username of the other user the currently logged in user is chatting with
    Short description:
        1) Calls the MessageAdapter to get the messages that belong to this offer only
        (between the bid creator and the offer creator)
        2) Calls UserAdapter to get the username of the other user the currently logged in user is chatting with
        3) Redirects the user to the ChatView page
        4) Loads all the messages related to this offer to the screen filtering messages that were sent TO the user
        and which were sent BY (from the API to the screen)
        5) Allows the use to send the message of the button is clicked, calling Chat class to add it to the api
        and updating the screen
        6) Redirects the user to the OfferInfoView page if the back button is clicked
    """

    def __init__(self, user, bid, offer):
        self.user = user
        self.bid = bid
        self.offer = offer
        self.messages = MessagesAdapter().get_messages(self.bid, self.offer)
        self.opponent_username = UserAdapter().get_user_username(user, bid.get_initiator(), offer.get_initiator_id())
        ChatView(self, self.opponent_username)

    def send_btn(self, chat):
        """
        Inputs:
            -chat: instance of the ChatView page
        Return: None
        Short description:
            Updates the screen when the message is sent and calls the send_message(..) method of the Chat class
        """
        # Write message to chat window
        chat.entry_text = self.filter_message(chat.entry_box.get("0.0", END))

        Chat(self.user, self.bid, self.offer).send_message(chat.entry_text)
        self.load_entry_you(chat.chat_log, chat.entry_text)

        # Scroll to the bottom of chat windows
        chat.chat_log.yview(END)

        # Erase previous message in Entry Box
        chat.entry_box.delete("0.0", END)

    def filter_message(self, entry_text):
        """
        Inputs:
            - entry_text: not filtered content of the message to be sent
        Return:
            - filtered content of the message to be sent
        Short description:
            Filter out all useless white lines at the end of a string,
            returns a new, beautifully filtered string.
        """
        end_filtered = ''
        for i in range(len(entry_text) - 1, -1, -1):
            if entry_text[i] != '\n':
                end_filtered = entry_text[0:i + 1]
                break
        for i in range(0, len(end_filtered), 1):
            if end_filtered[i] != "\n":
                return end_filtered[i:] + '\n'
        return ''

    def load_entry_you(self, chat_log, entry_text):
        """
        Inputs:
            - chat_log: field on the screen to add messages to
            - entry_text: content of the message to be sent
        Return: None
        Short description:
            Responsible for representing the messages sent BY the user who is logged in
        """
        if entry_text != '':
            chat_log.config(state=NORMAL)
            if chat_log.index('end') != None:
                line_number = float(chat_log.index('end')) - 1.0
                chat_log.insert(END, "You: " + entry_text)
                chat_log.tag_add("You", line_number, line_number + 0.4)
                chat_log.tag_config("You", foreground="#ff006a", font=("Arial", 12, "bold"))
                chat_log.config(state=DISABLED)
                chat_log.yview(END)

    def load_entry_other(self, chat_log, entry_text):
        """
        Inputs:
            - chat_log: field on the screen to add messages to
            - entry_text: content of the message to be sent
        Return: None
        Short description:
            Responsible for representing the messages sent TO the user who is logged in
        """
        if entry_text != '':
            chat_log.config(state=NORMAL)
            if chat_log.index('end') != None:
                line_number = float(chat_log.index('end')) - 1.0
                chat_log.insert(END, "Other: " + entry_text)
                chat_log.tag_add("Other", line_number, line_number + 0.6)
                chat_log.tag_config("Other", foreground="#1AA416", font=("Arial", 12, "bold"))
                chat_log.config(state=DISABLED)
                chat_log.yview(END)

    def press_action(self, chat):
        """"Keyboard event"""
        chat.entry_box.config(state=NORMAL)
        self.send_btn(chat)

    def disable_entry(self, chat):
        """"Keyboard event"""
        chat.entry_box.config(state=DISABLED)

    def back_btn(self, view):
        """
        Inputs:
            - view: instance of the Chat page
        Return: None
        Short description:
            Calls the OfferInfoController which will redirect the user to the OfferInfoView page
        """
        view.root.destroy()
        OfferInfoController(self.user, self.offer, self.bid)

    def load_all_messages_screen(self, chat):
        """
        Inputs:
            -chat: instance of the ChatView page
        Return: None
        Short description:
            Loads all the messages related to this offer to the screen filtering,
            which messages were sent TO the user and which were sent BY
        """
        for i in self.messages:
            if i.get_poster_id() == self.user.get_id():
                message_to_print = i.get_content()
                self.load_entry_you(chat.chat_log, message_to_print)
            else:
                message_to_print = i.get_content()
                self.load_entry_other(chat.chat_log, message_to_print)


# start of the app
if __name__ == "__main__":
    LoginController()
