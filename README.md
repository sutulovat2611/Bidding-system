# Description 
The application is an online matching system to put prospective students in touch with private tutors. 
Users whose accounts exist in the API are allowed to login into the application using their username and 
the respective password. The account is initially assigned a role, so that the user will be immediately logged in 
with their respective role: __tutor__ or __student__. 
### Student
The student can create two types of bids: closed and open bid, where all the required information about the subject
and the tutor is filled up. Bids created by the student will be shown to all the tutors that have the sufficient
competency ( higher than the one required in the bid by 2). 

### Tutor
The tutor can see bids and make offers for them, where an offer is the way of negotiation between the student and the tutor.
The tutor may request different charge, weekday, time, etc and the student will be able to see the offer and accept or decline it.
If the tutor has nothing to negotiate and they want to proceed, they may buy out an open bid, which will immediately create a contract.
If a bid is close, the tutor may create an offer and negotiate with the student in the chat.

### Open bid
- may be seen by any tutor with the sufficient competency 
- all the offers related to this bid may be seen by other tutors
- may be bought out by the tutor, immediately creating the contract
- expires after 30 minutes from it's creation and disappears from the system 

### Close bid
- may be seen by any tutor with the sufficient competency
- any offer may be seen only by it's creator and the creator of the bid
- cannot be bought out by the tutor
- tutor may send an offer and negotiation is done in the chat. 
- the offer may be edited after the negotiation
- expires after 7 days from it's creation and disappears from the system 

### Contract
- both students and tutors have a list of contracts
- if the contract is about to expire the user will get a notification about it once logged in
- contracts are sorted by:
  - ongoing: current contracts
  - expired: five (latest) or less contracts that expired
  - pending: contract requests
- contract length is specified in an offer or a bid
- contract may be renewed:
   - with the same terms, same tutor
   - with the same terms, new tutor, which is to be searched by the username
   - with the new terms, same tutor

### Monitoring page
The tutor may add any open bid to the monitoring page and all the offers for all the bids on that page will be updated every 30 seconds.

# Development
The application was developed in Python with Tkinter GUI toolkit. The main goal of this project was to not just create a working system,
but to ensure that the application is developed in an object oriented programming model utilizing various object oriented principles, such
as SOLID principles and different design patterns, such as factory method, adapter pattern, etc. That ensured the application's extensibility 
and maintainabilty.

### Running the application
      The code is to be run with the controller.py package. 

## Additinal documents
The rationale and class diagram may be found in the __Documents__ folder

## External libraries used in the application:
1. _ABC_: This module provides the infrastructure for defining abstract base classes (ABCs) in Python
2. _requests_: The requests module allows you to send HTTP requests using Python.The HTTP request returns a 
Response Object with all the response data (content, encoding, status, etc).
3. _json_: a built-in package, which can be used to work with JSON data.
4. _tkinter_: the standard Python interface to the Tk GUI toolkit.
5. _datetime_: a date in Python is not a data type of its own, but we can import a module named datetime to work 
with dates as date objects.
6. _dateutil_: provides powerful extensions to the standard datetime module, available in Python.
7. _PIL_: The Python Imaging Library adds image processing capabilities to your Python interpreter.This library provides 
extensive file format support, an efficient internal representation, and fairly powerful image processing capabilities.
8. _threading_: Using threads allows a program to run multiple operations concurrently in the same process space.
