"""The following module is created for communication with the user, this is the UI module"""

from tkinter import *
from tkinter import messagebox

import dateutil

from model import Student, Tutor, OpenBid, CloseBid
from PIL import ImageTk, Image
import tkinter
from abc import ABC

import tkinter as tk
from datetime import datetime, timedelta
import dateutil.parser


class Page(ABC):
    def __init__(self, controller):
        self.root = Tk()

        self.controller = controller

        # Making the frame bigger
        w = 800
        h = 800
        x = 50
        y = 100
        # use width x height + x_offset + y_offset (no spaces!)
        self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))

        # Background colour
        self.root['background'] = '#dea5a4'


class Scroll(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#dea5a4")
        self.frame = tk.Frame(self.canvas, background="#dea5a4")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class ScrollablePage(ABC):
    def __init__(self, controller):
        self.root = Tk()
        self.controller = controller

        # Making the frame bigger
        w = 800
        h = 800
        x = 50
        y = 100
        # use width x height + x_offset + y_offset (no spaces!)
        self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))

        # Background colour
        self.root['background'] = '#dea5a4'

        self.scroll = Scroll(self.root)

        self.scroll.pack(side="top", fill="both", expand=True)


class LoginView(Page):
    def __init__(self, controller):
        super().__init__(controller)

        # Making LoginView title
        self.label = Label(self.root, text="Login", fg='#5c3f8f', font=("Arial", 25), justify=CENTER,
                           background="#dea5a4")
        self.label.place(x=360, y=165)

        # Making the username label
        self.username_label = Label(text="Username:", font=("Arial", 14), background="#dea5a4")
        self.username_label.place(x=240, y=250)

        # Making the username textbox
        self.username = Entry(font=("Arial", 14))
        self.username.place(x=360, y=250)

        # Making the password label
        self.password_label = Label(text="Password:", font=("Arial", 14), background="#dea5a4")
        self.password_label.place(x=240, y=345)

        # Making the password textbox
        self.password = Entry(show="*", font=("Arial", 14))
        self.password.place(x=360, y=345)

        # Making the button
        self.myButton = Button(text="Log in",
                               command=lambda: self.controller.login_btn(self.username.get(), self.password.get(),
                                                                         self), bg='#5c3f8f', font=("Arial", 14),
                               fg='white')
        self.myButton.place(x=370, y=435)

        self.root.mainloop()


class ProfileView(Page):
    def __init__(self, user, controller, initialisation):
        super().__init__(controller)

        # Create a profile pic image object of the image in the path
        profile_pic = Image.open("images/profile_pic.png")
        profile_pic = profile_pic.resize((130, 130), Image.ANTIALIAS)
        profile_pic = ImageTk.PhotoImage(profile_pic)

        profile_pic_label = tkinter.Label(image=profile_pic, bg='#dea5a4')
        profile_pic_label.image = profile_pic
        # Position image
        profile_pic_label.place(x=350, y=40)

        # Making the username label
        self.username_label = Label(text="Username:", font=("Arial", 14), background="#dea5a4")
        self.username_label.place(x=200, y=190)

        # Username:
        self.username = user.get_username()
        self.username_place = Text(height=1, width=len(self.username), font=("Arial", 12), background="white")
        self.username_place.insert(tkinter.END, self.username)
        self.username_place.config(state=DISABLED)
        self.username_place.place(x=300, y=195)

        # Making the Name label
        self.given_name_label = Label(text="Name:", font=("Arial", 14), background="#dea5a4")
        self.given_name_label.place(x=200, y=230)

        # Name:
        self.name_place = Text(height=1, width=len(user.get_full_name()), font=("Arial", 12), background="white")
        self.name_place.insert(tkinter.END, user.get_full_name())
        self.name_place.config(state=DISABLED)
        self.name_place.place(x=260, y=235)

        # Making the role label
        self.role_label = Label(text="Role(s):", font=("Arial", 14), background="#dea5a4")
        self.role_label.place(x=200, y=270)

        # Role:
        y = 310
        if isinstance(user, Student):
            self.role_place = Text(height=1, width=7, font=("Arial", 12), background="white")
            self.role_place.insert(tkinter.END, 'Student')
            self.role_place.config(state=DISABLED)
            self.role_place.place(x=230, y=y)
            y += 35

        if isinstance(user, Tutor):
            self.role_place_tutor = Text(height=1, width=5, font=("Arial", 12), background="white")
            self.role_place_tutor.insert(tkinter.END, 'Tutor')
            self.role_place_tutor.config(state=DISABLED)
            self.role_place_tutor.place(x=230, y=y)
            y += 35

        # Making the competencies label
        self.competencies_label = Label(text="Competencies:", font=("Arial", 14), background="#dea5a4")
        self.competencies_label.place(x=200, y=y)

        # Listing the competencies
        self.competencies = user.get_competencies()

        if len(self.competencies) == 0:
            y += 35
            self.competencies_place = Text(height=1, width=40, font=("Arial", 12),
                                           background="white")
            self.competencies_place.insert(tkinter.END, "None")
            self.competencies_place.config(state=DISABLED)
            self.competencies_place.place(x=230, y=y)

        else:
            for i in range(len(self.competencies)):
                y += 35
                self.competencies_place = Text(height=1, width=len(self.competencies[i]), font=("Arial", 12),
                                               background="white")
                self.competencies_place.insert(tkinter.END, self.competencies[i])
                self.competencies_place.config(state=DISABLED)
                self.competencies_place.place(x=230, y=y)

        y += 35
        # Making the Qualifications label
        self.qualifications_label = Label(text="Qualifications:", font=("Arial", 14), background="#dea5a4")
        self.qualifications_label.place(x=200, y=y)

        # Listing the Qualifications
        self.qualifications = user.get_qualifications()

        y += 35
        if len(self.qualifications) == 0:
            self.qualifications_place = Text(height=1, width=40, font=("Arial", 12), background="white")
            self.qualifications_place.insert(tkinter.END, "None")
            self.qualifications_place.config(state=DISABLED)
            self.qualifications_place.place(x=230, y=y)
            y += 35
        else:
            for i in range(len(self.qualifications)):
                if self.qualifications[i].get_verified():
                    self.qualifications_place = Text(height=1, width=len(self.qualifications[i]),
                                                     font=("Arial", 12),
                                                     background="white")
                    self.qualifications_place.insert(tkinter.END, self.qualifications[i])
                    self.qualifications_place.config(state=DISABLED)
                    self.qualifications_place.place(x=230, y=y)
                    y += 35

        # Making contract button
        self.contract_button = Button(text="Contracts", bg='#d152ff', font=("Arial", 14), fg='white', width="20",
                                      command=lambda: self.controller.contracts_btn(self))
        self.contract_button.place(x=320, y=y)

        # Making Bids/offer button
        if isinstance(user, Tutor):
            y += 50
            self.bid_button = Button(text="Pending Offers", bg='#f244aa', font=("Arial", 14), fg='white', width="20",
                                     command=lambda: self.controller.tutor_offers_btn(self))
            self.bid_button.place(x=320, y=y)

            y += 50
            self.student_bids_button = Button(text="Available student bids", bg='#7331F7', font=("Arial", 14),
                                              fg='white', width="20",
                                              command=lambda: self.controller.bids_list_btn(self))
            self.student_bids_button.place(x=320, y=y)

            y += 50
            self.student_bids_button = Button(text="Monitoring page", bg='#0FD1BE', font=("Arial", 14),
                                              fg='white', width="20",
                                              command=lambda: self.controller.monitor_page_btn(self))
            self.student_bids_button.place(x=320, y=y)

        if isinstance(user, Student):
            y += 50
            self.bid_button = Button(text="Pending Bids", bg='#f244aa', font=("Arial", 14), fg='white', width="20",
                                     command=lambda: self.controller.bids_list_btn(self))
            self.bid_button.place(x=320, y=y)

        # Make logout button
        y += 50
        self.bid_button = Button(text="Log out", bg='#aec6cf', font=("Arial", 14), fg='white', width="20",
                                 command=lambda: self.controller.log_out_btn(self))
        self.bid_button.place(x=320, y=y)

        # checks if its first login
        if initialisation == "Login":
            if not len(user.get_expiring_contracts()) == 0:
                message = "You have " + str(
                    len(user.get_expiring_contracts())) + " contract(s) that are about to expire. \nThese " \
                                                          "contract(s) are: \n"
                for c in user.get_expiring_contracts():
                    message += c.get_subject().get_name() + ", " + c.get_subject().get_description() + " with: "
                    if c.get_first_party().get_id() == user.get_id():
                        message += c.get_second_party().get_full_name() + "\n"
                    else:
                        message += c.get_first_party().get_full_name() + "\n"
                messagebox.showinfo("Expiring contracts", message=message)
        self.root.mainloop()


class BidsListView(ScrollablePage):
    def __init__(self, controller, bids, user):
        super().__init__(controller)
        if len(bids) == 0:
            column = 3
        else:
            column = 0
        if isinstance(user, Student):
            # Creating bid button
            self.bid_button = Button(self.scroll.frame, text="Create New bid", bg='#f244aa', font=("Arial", 14),
                                     fg='white', width="20",
                                     command=lambda: self.controller.create_bid_btn(self)).grid(row=0, column=column,
                                                                                                sticky="E", pady=10,
                                                                                                padx=10)
        else:
            # Label
            self.label = Label(self.scroll.frame, text="Available Bids", fg='#5c3f8f', bg='#f244aa', font=("Arial", 25),
                               justify=CENTER,
                               background="#dea5a4").grid(row=0, column=column, pady=10, padx=10)

        # Creating back button
        self.back_button = Button(self.scroll.frame, text="Back", bg='#aec6cf', font=("Arial", 14), fg='white',
                                  width="20",
                                  command=lambda: self.controller.back_btn(self)).grid(row=0, column=0, sticky="W",
                                                                                       pady=10, padx=10)

        # Bids list
        self.bids = bids

        # printing buttons for each bid on the screen
        row = 0
        for i in range(len(self.bids)):
            row = row + 10
            if isinstance(self.bids[i], OpenBid):
                closing_time = (dateutil.parser.parse(self.bids[i].get_date_created()[:-1]) + timedelta(
                    minutes=30)).isoformat()[:-3] + 'Z'
                closing_time = closing_time[:-14] + " " + closing_time[11:-8]
                background_color = "#BFA2F7"
                self.request_buttons = Button(self.scroll.frame,
                                              text=self.bids[i].get_subject().get_name() + ", " + self.bids[
                                                  i].get_subject().get_description() + "." + "\n Type: Open" + "\n Closing on: " + closing_time,
                                              bg=background_color, font=("Arial", 14), fg='black',
                                              width="66",
                                              height="4",
                                              command=lambda i=i: self.controller.show_bid_btn(self,
                                                                                               self.bids[i])).grid(
                    row=row, column=0, padx=20, pady=10)
            else:
                closing_time = (dateutil.parser.parse(self.bids[i].get_date_created()[:-1]) + timedelta(
                    days=7)).isoformat()[:-3] + 'Z'
                closing_time = closing_time[:-14] + " " + closing_time[11:-8]
                background_color = "#EF9DC9"
                self.request_buttons = Button(self.scroll.frame,
                                              text=self.bids[i].get_subject().get_name() + ", " + self.bids[
                                                  i].get_subject().get_description() + "." + "\n Type: Close" + "\n Closing on: " + closing_time,
                                              bg=background_color,
                                              font=("Arial", 14), fg='black',
                                              width="66",
                                              height="4",
                                              command=lambda i=i: self.controller.show_bid_btn(self,
                                                                                               self.bids[i])).grid(
                    row=row, column=0, padx=20, pady=10)

        self.root.mainloop()


class ChooseBidView(Page):
    # allows to choose which bid the user wants to create: open/close
    def __init__(self, controller):
        super().__init__(controller)

        # Making create bid title
        self.label = Label(self.root, text="Create a new bid", fg='#5c3f8f', font=("Arial", 25), justify=CENTER,
                           background="#dea5a4")
        self.label.place(x=270, y=165)

        # Creating open bid button
        self.open_bid_button = Button(text="Open Bid", bg="#BFA2F7", font=("Arial", 14), fg='black', width="20",
                                      command=lambda: self.controller.open_bid_btn(self))
        self.open_bid_button.place(x=140, y=300)

        # Creating close bid button
        self.close_bid_button = Button(text="Close Bid", bg="#EF9DC9", font=("Arial", 14), fg='black', width="20",
                                       command=lambda: self.controller.close_bid_btn(self))
        self.close_bid_button.place(x=430, y=300)

        # Creating close bid button
        self.cancel_bid_button = Button(text="Cancel", bg="#ff6961", font=("Arial", 14), fg='black', width="20",
                                        command=lambda: self.controller.cancel_bid_btn(self))
        self.cancel_bid_button.place(x=270, y=350)
        self.root.mainloop()


class CreateBidView(Page):
    def __init__(self, controller, type_bid):
        super().__init__(controller)
        # Subtitle
        # Making create bid title
        self.label = Label(self.root, text=type_bid + " Bid", fg='#5c3f8f', font=("Arial", 25), justify=CENTER,
                           background="#dea5a4")
        self.label.place(x=330, y=20)

        self.label = Label(self.root, text="Please fill in all the information below", fg='black', font=("Arial", 15),
                           justify=CENTER,
                           background="#dea5a4")
        self.label.place(x=240, y=90)

        # Subject name label
        self.subject_name_label = Label(text="Subject name: ", font=("Arial", 14), background="#dea5a4")
        self.subject_name_label.place(x=70, y=165)

        # Making the subject entry
        self.subject_name = Entry(font=("Arial", 12), width=55)
        self.subject_name.place(x=200, y=170)

        # Subject description label
        self.subject_description_label = Label(text="Subject description: ", font=("Arial", 14), background="#dea5a4")
        self.subject_description_label.place(x=70, y=205)

        # Making the subject description entry
        self.subject_description = Entry(font=("Arial", 12), width=50)
        self.subject_description.place(x=245, y=210)

        # Competency level
        self.subject_level_label = Label(text="Required \ncompetency level: ", font=("Arial", 14), background="#dea5a4",
                                         justify=LEFT)
        self.subject_level_label.place(x=70, y=245)
        self.subject_level = Entry(font=("Arial", 12), width=51)
        self.subject_level.place(x=235, y=270)

        # tutor qualification title
        self.qualification_title_label = Label(text="Required \nqualification title: ", font=("Arial", 14),
                                               background="#dea5a4",
                                               justify=LEFT)
        self.qualification_title_label.place(x=70, y=305)
        self.qualification_title = Entry(font=("Arial", 12), width=53)
        self.qualification_title.place(x=215, y=330)

        # Number of sessions per week
        self.ses_per_week_label = Label(text="Preferred \nno.session(s) per week: ", font=("Arial", 14),
                                        background="#dea5a4",
                                        justify=LEFT)
        self.ses_per_week_label.place(x=70, y=365)
        self.ses_per_week = Entry(font=("Arial", 12), width=46)
        self.ses_per_week.place(x=275, y=390)

        # Length of class
        self.hours_per_lesson = Label(text="Preferred length of\n lesson (in hours): ", font=("Arial", 14),
                                      background="#dea5a4",
                                      justify=LEFT)
        self.hours_per_lesson.place(x=70, y=425)
        self.hours_per_lesson = Entry(font=("Arial", 12), width=46)
        self.hours_per_lesson.place(x=275, y=450)

        # Creating next button
        self.next_button = Button(text="Next", bg="#BFA2F7", font=("Arial", 14), fg='black', width="20",
                                  command=lambda: self.next_click())
        self.next_button.place(x=400, y=480)

        # Creating close bid button
        self.cancel_bid_button = Button(text="Cancel", bg="#ff6961", font=("Arial", 14), fg='black', width="20",
                                        command=lambda: self.controller.cancel_btn(self))
        self.cancel_bid_button.place(x=100, y=480)

        self.root.mainloop()

    def next_click(self):
        # Picking time

        # preferred Day

        self.day = [None] * int(self.ses_per_week.get())
        self.day_label = [None] * int(self.ses_per_week.get())
        self.time_hour = [None] * int(self.ses_per_week.get())
        self.time_min = [None] * int(self.ses_per_week.get())
        self.time_label = [None] * int(self.ses_per_week.get())
        y = 575
        for i in range(int(self.ses_per_week.get())):
            # Day
            self.day_label[i] = Label(text="Preferred day " + str(i + 1) + ": ", font=("Arial", 14),
                                      background="#dea5a4",
                                      justify=LEFT)
            self.day_label[i].place(x=70, y=y)
            self.day[i] = Entry(font=("Arial", 12), width=30)
            self.day[i].place(x=220, y=y + 5)

            # Time
            self.time_label[i] = Label(text="Time: ", font=("Arial", 14),
                                       background="#dea5a4",
                                       justify=LEFT)
            self.time_label[i].place(x=500, y=y)

            self.time_label_extra = Label(text=":", font=("Arial", 14),
                                          background="#dea5a4",
                                          justify=LEFT)
            self.time_label_extra.place(x=595, y=y)
            hour_string = StringVar()
            min_string = StringVar()
            last_value_sec = ""
            last_value = ""

            self.time_min[i] = Spinbox(
                from_=0,
                to=59,
                wrap=True,
                textvariable=min_string,
                font=("Arial", 12),
                width=2,
                justify=CENTER
            )

            self.time_hour[i] = Spinbox(from_=0,
                                        to=23,
                                        wrap=True,
                                        textvariable=hour_string,
                                        width=2,
                                        state="readonly",
                                        font=("Arial", 12),
                                        justify=CENTER
                                        )

            # Time configuration
            if last_value == "59" and min_string.get() == "0":
                hour_string.set(int(hour_string.get()) + 1 if hour_string.get() != "23" else 0)
                last_value = min_string.get()

            if last_value_sec == "59" and self.time_min[i].get() == "0":
                min_string.set(int(min_string.get()) + 1 if min_string.get() != "59" else 0)
            if last_value == "59":
                hour_string.set(int(hour_string.get()) + 1 if hour_string.get() != "23" else 0)
            self.time_hour[i].place(x=560, y=y + 5)
            self.time_min[i].place(x=610, y=y + 5)
            y += 35

        # preferred rate
        self.rate_label = Label(text="Preferred rate: ", font=("Arial", 14),
                                background="#dea5a4",
                                justify=LEFT)
        self.rate_label.place(x=70, y=y)
        self.rate = Entry(font=("Arial", 12), width=40)
        self.rate.place(x=200, y=y + 5)

        # Drop down list
        self.rate_per = StringVar(self.root)
        self.rate_per.set("per session")  # default value

        w = OptionMenu(self.root, self.rate_per, "per hour", "per session")
        w.place(x=590, y=y)

        # Contract length
        y += 35
        self.customise_option_label = Label(text="Customise \nContract Length: ", font=("Arial", 14),
                                            background="#dea5a4",
                                            justify=LEFT)

        self.customise_option_label.place(x=70, y=y)

        self.customise_option = BooleanVar()
        self.customise_option_yes = Radiobutton(self.root, text='Yes', variable=self.customise_option, value=True)
        self.customise_option_yes.place(x=240, y=y + 25)
        self.customise_option_no = Radiobutton(self.root, text='No', variable=self.customise_option, value=False)
        self.customise_option_no.place(x=300, y=y + 25)

        self.contract_length_label = Label(text="Contract Length: ", font=("Arial", 14),
                                           background="#dea5a4",
                                           justify=LEFT)
        self.contract_length_label.place(x=360, y=y + 25)
        # Drop down list
        self.contract_length = StringVar(self.root)
        self.contract_length.set(6)  # default value

        contract_list = OptionMenu(self.root, self.contract_length, 3, 6, 12, 24, 36, 48)
        contract_list.place(x=530, y=y + 25)

        self.months_label = Label(text="Months", font=("Arial", 14),
                                  background="#dea5a4",
                                  justify=LEFT)
        self.months_label.place(x=590, y=y + 25)

        y += 60
        # Creating submit button

        bid_info = {
            "subjectName": self.subject_name.get(),
            "subjectDescription": self.subject_description.get(),
            "subjectLevel": self.subject_level.get(),
            "qualificationTitle": self.qualification_title.get()
        }

        lesson_info = {
            "sesPerWeek": self.ses_per_week.get(),
            "hoursPerLes": self.hours_per_lesson.get(),
            "day": self.day,
            "timeHour": self.time_hour,
            "timeMin": self.time_min,
            "rate": self.rate,
            "rateType": self.rate_per,
            "customContract": self.customise_option,
            "contractLen": self.contract_length
        }

        self.submit_button = Button(text="Submit", bg="#BFA2F7", font=("Arial", 14), fg='black', width="20",
                                    command=lambda: self.controller.submit_form(bid_info, lesson_info, self, ))
        self.submit_button.place(x=400, y=y)

        # Creating close bid button
        self.cancel_bid_button = Button(text="Cancel", bg="#ff6961", font=("Arial", 14), fg='black', width="20",
                                        command=lambda: self.controller.cancel_btn(self))
        self.cancel_bid_button.place(x=100, y=y)


class BidInfoView(Page):
    def __init__(self, controller, user, bid, initiators, is_monitor):
        super().__init__(controller)
        self.bid = bid
        self.user = user
        self.initiators = initiators

        found = False
        for i in self.initiators:
            if i.get_id() == self.user.get_id():
                found = True

        # Back button
        self.back_button = Button(text="Back", bg='#aec6cf', font=("Arial", 14), fg='white', width="20",
                                  command=lambda: self.controller.back_btn(self))
        self.back_button.place(x=40, y=40)

        if not found:
            if isinstance(self.user, Tutor):
                if isinstance(self.bid, OpenBid):
                    self.buy_out_button = Button(text="Buy out", bg='#d152ff', font=("Arial", 14), fg='white',
                                                 width="10",
                                                 command=lambda: self.controller.buy_out_btn(self))
                    self.buy_out_button.place(x=280, y=40)

                    # Add to favourites button
                    self.back_button = Button(text="Add to monitor", bg='#990099', font=("Arial", 14), fg='white',
                                              width="12",
                                              command=lambda: self.controller.monitor_btn())
                    self.back_button.place(x=580, y=40)

                self.contract_button = Button(text="Make an offer", bg='#5c3f8f', font=("Arial", 14), fg='white',
                                              width="12", command=lambda: self.controller.make_offer_btn(self))
                self.contract_button.place(x=420, y=40)

        # Type label
        y = 95
        self.type_label = Label(text="Type: ", font=("Arial", 14), background="#dea5a4")
        self.type_label.place(x=120, y=y)

        # Making the type display
        if isinstance(self.bid, OpenBid):
            self.type = Text(height=1, width=51, font=("Arial", 12), background="white")
            self.type.insert(tkinter.END, "Open")
            self.type.config(state=DISABLED)
            self.type.place(x=180, y=y + 5)
        else:
            self.type = Text(height=1, width=51, font=("Arial", 12), background="white")
            self.type.insert(tkinter.END, "Close")
            self.type.config(state=DISABLED)
            self.type.place(x=180, y=y + 5)

        # name label
        y += 35
        self.name_label = Label(text="Creator: ", font=("Arial", 14), background="#dea5a4")
        self.name_label.place(x=120, y=y)
        # Making the subject display
        self.name = Text(height=1, width=49, font=("Arial", 12), background="white")
        self.name.insert(tkinter.END, self.bid.get_initiator().get_full_name())
        self.name.config(state=DISABLED)
        self.name.place(x=200, y=y + 5)

        # Subject  label
        y += 35
        self.subject_label = Label(text="Subject: ", font=("Arial", 14), background="#dea5a4")
        self.subject_label.place(x=120, y=y)

        # Making the subject display
        self.subject = Text(height=1, width=49, font=("Arial", 12), background="white")
        self.subject.insert(tkinter.END, self.bid.get_subject())
        self.subject.config(state=DISABLED)
        self.subject.place(x=200, y=y + 5)

        # Competency level
        y += 35
        self.subject_level_label = Label(text="Required \ncompetency level: ", font=("Arial", 14), background="#dea5a4",
                                         justify=LEFT)
        self.subject_level_label.place(x=120, y=y)
        self.subject_level = Text(height=1, width=40, font=("Arial", 12), background="white")
        self.subject_level.insert(tkinter.END, str(self.bid.get_additional_info()['subjectLevel']))
        self.subject_level.config(state=DISABLED)
        self.subject_level.place(x=280, y=y + 25)

        # tutor qualification title
        y += 35 + 20
        self.qualification_title_label = Label(text="Required \nqualification title: ", font=("Arial", 14),
                                               background="#dea5a4",
                                               justify=LEFT)
        self.qualification_title_label.place(x=120, y=y)
        self.qualification_title = Text(height=1, width=42, font=("Arial", 12), background="white")
        self.qualification_title.insert(tkinter.END, self.bid.get_additional_info()['qualificationTitle'])
        self.qualification_title.config(state=DISABLED)
        self.qualification_title.place(x=260, y=y + 25)

        # Number of sessions per week
        y += 35 + 20
        self.ses_per_week_label = Label(text="Preferred \nno.session(s) per week: ", font=("Arial", 14),
                                        background="#dea5a4",
                                        justify=LEFT)
        self.ses_per_week_label.place(x=120, y=y)
        self.ses_per_week = Text(height=1, width=34, font=("Arial", 12), background="white")
        self.ses_per_week.insert(tkinter.END, self.bid.get_additional_info()['sesPerWeek'])
        self.ses_per_week.config(state=DISABLED)
        self.ses_per_week.place(x=330, y=y + 25)

        y += 35 + 20
        # Length of the session
        self.hours_per_lesson_label = Label(text="Preferred length \nof the session (in hours):", font=("Arial", 14),
                                            background="#dea5a4",
                                            justify=LEFT)
        self.hours_per_lesson_label.place(x=120, y=y)
        self.hours_per_lesson = Text(height=1, width=34, font=("Arial", 12), background="white")
        self.hours_per_lesson.insert(tkinter.END, self.bid.get_additional_info()['hoursPerLesson'])
        self.hours_per_lesson.config(state=DISABLED)
        self.hours_per_lesson.place(x=330, y=y + 25)

        y += 35 + 20
        # Rate
        self.rate_label = Label(text="Rate:", font=("Arial", 14),
                                background="#dea5a4",
                                justify=LEFT)
        self.rate_label.place(x=120, y=y)
        self.rate = Text(height=1, width=22, font=("Arial", 12), background="white")
        self.rate.insert(tkinter.END, self.bid.get_additional_info()['rate'])
        self.rate.config(state=DISABLED)
        self.rate.place(x=170, y=y + 5)

        # rate type:
        self.rate_type = Text(height=1, width=29, font=("Arial", 12), background="white")
        self.rate_type.insert(tkinter.END, self.bid.get_additional_info()['rateType'])
        self.rate_type.config(state=DISABLED)
        self.rate_type.place(x=375, y=y + 5)

        y += 35
        i = 0
        for t in self.bid.get_additional_info()['dayAndTime']:
            # Day
            i += 1
            self.day_label = Label(text="Preferred day " + str(i) + ": ", font=("Arial", 14),
                                   background="#dea5a4",
                                   justify=LEFT)
            self.day_label.place(x=120, y=y)
            self.day = Text(height=1, width=25, font=("Arial", 12), background="white")
            self.day.insert(tkinter.END, t['day'])
            self.day.config(state=DISABLED)
            self.day.place(x=263, y=y + 5)

            # Time
            self.time_label = Label(text="Time: ", font=("Arial", 14),
                                    background="#dea5a4",
                                    justify=LEFT)
            self.time_label.place(x=500, y=y)

            self.time_label_extra = Label(text=":", font=("Arial", 14),
                                          background="#dea5a4",
                                          justify=LEFT)
            self.time_label_extra.place(x=595, y=y)

            self.time_min = Text(height=1, width=3, font=("Arial", 12), background="white")
            self.time_min.insert(tkinter.END, t['timeMin'])

            self.time_hour = Text(height=1, width=3, font=("Arial", 12), background="white")
            self.time_hour.insert(tkinter.END, t['timeHour'])

            self.time_hour.config(state=DISABLED)
            self.time_min.config(state=DISABLED)
            self.time_hour.place(x=560, y=y + 5)
            self.time_min.place(x=610, y=y + 5)

            y += 35

        # Contract length
        self.contract_length_label = Label(text="Contract Length: ", font=("Arial", 14),
                                           background="#dea5a4",
                                           justify=LEFT)
        self.contract_length_label.place(x=120, y=y)
        self.contact_length = Text(height=1, width=20, font=("Arial", 12), background="white")
        self.contact_length.insert(tkinter.END, str(self.bid.get_additional_info()['contractLen']) + " months")
        self.contact_length.config(state=DISABLED)
        self.contact_length.place(x=263, y=y + 5)

        y += 35
        # Date label
        self.date_created_label = Label(text="Date created: ", font=("Arial", 14), background="#dea5a4")
        self.date_created_label.place(x=120, y=y)

        # Making the date display

        date_created = dateutil.parser.parse(self.bid.get_date_created()[:-1])
        self.date_created = Text(height=1, width=43, font=("Arial", 12), background="white")
        self.date_created.insert(tkinter.END, date_created.isoformat()[:-16] + " " + date_created.isoformat()[11:-10])
        self.date_created.config(state=DISABLED)
        self.date_created.place(x=250, y=y + 5)

        y += 35
        # Date label

        self.closing_date_label = Label(text="Closing date: ", font=("Arial", 14), background="#dea5a4")
        self.closing_date_label.place(x=120, y=y)

        # Making the close date

        if isinstance(self.bid, OpenBid):
            close_date = dateutil.parser.parse(self.bid.get_date_created()[:-1]) + timedelta(minutes=30)
        else:
            close_date = dateutil.parser.parse(self.bid.get_date_created()[:-1]) + timedelta(days=7)

        self.close_date = Text(height=1, width=43, font=("Arial", 12), background="white")
        self.close_date.insert(tkinter.END, close_date.isoformat()[:-16] + " " + close_date.isoformat()[11:-10])
        self.close_date.config(state=DISABLED)
        self.close_date.place(x=250, y=y + 5)

        # Offers
        y += 35
        self.offers_label = Label(text="Offers:", font=("Arial", 14),
                                  background="#dea5a4",
                                  justify=LEFT)
        self.offers_label.place(x=120, y=y)

        if (isinstance(self.user, Tutor) and isinstance(self.bid, OpenBid)) or isinstance(self.user, Student):

            if not ('offers' in self.bid.get_additional_info()) and len(self.bid.get_additional_info()['offers']) == 0:
                self.no_offers_label = Label(text="None", font=("Arial", 14),
                                             background="#dea5a4",
                                             justify=LEFT)
                self.no_offers_label.place(x=200, y=y)
            else:
                y += 40
                for o in range(len(self.bid.get_additional_info()['offers'])):
                    background_color = "#FFFFFF"
                    if self.user.get_id() == self.bid.get_additional_info()['offers'][o].get_initiator_id():
                        background_color = "#6AFFCE"
                    self.offer_buttons = Button(
                        text='@' + self.initiators[o].get_username() + ", " + self.initiators[o].get_full_name(),
                        bg=background_color, font=("Arial", 14), fg='black',
                        width="50",
                        height="2",
                        command=lambda o=o: self.controller.open_offer_btn(self,
                                                                           self.bid.get_additional_info()['offers'][o]))

                    self.offer_buttons.place(x=100, y=y)
                    y += 80

        counter = 0
        if isinstance(self.user, Tutor) and isinstance(self.bid, CloseBid):
            if not ('offers' in self.bid.get_additional_info()) or len(self.bid.get_additional_info()['offers']) == 0:
                self.no_offers_label = Label(text="None", font=("Arial", 14),
                                             background="#dea5a4",
                                             justify=LEFT)
                self.no_offers_label.place(x=200, y=y)
            else:
                y += 40
                for o in range(len(self.bid.get_additional_info()['offers'])):
                    if self.user.get_id() == self.bid.get_additional_info()['offers'][o].get_initiator_id():
                        background_color = "#6AFFCE"
                        self.offer_buttons = Button(
                            text='@' + self.initiators[o].get_username() + ", " + self.initiators[o].get_full_name(),
                            bg=background_color, font=("Arial", 14), fg='black',
                            width="50",
                            height="2",
                            command=lambda o=o: self.controller.open_offer_btn(self,
                                                                               self.bid.get_additional_info()['offers'][
                                                                                   o]))
                        self.offer_buttons.place(x=100, y=y)
                        counter = 1
                    y += 80
            if counter == 0:
                self.no_offers_label = Label(text="None", font=("Arial", 14),
                                             background="#dea5a4",
                                             justify=LEFT)
                self.no_offers_label.place(x=200, y=y)

        if isinstance(self.user, Tutor) and is_monitor:
            self.root.after(30000, lambda: self.controller.monitor_update(self))
        self.root.mainloop()


class CreateOfferView(Page):
    def __init__(self, controller, user, bid):
        super().__init__(controller)

        self.user = user
        self.bid = bid

        # Subtitle
        # Making create bid title and username of the creator
        if isinstance(bid, OpenBid):
            # Making create bid title
            self.label = Label(self.root, text="Open Bid", fg='#5c3f8f', font=("Arial", 25), justify=CENTER,
                               background="#dea5a4")
            self.label.place(x=330, y=20)
        else:
            self.label_bid = Label(self.root, text="Close Bid", fg='#5c3f8f', font=("Arial", 25), justify=CENTER,
                                   background="#dea5a4")
            self.label_bid.place(x=330, y=20)

        self.label = Label(self.root, text="Please fill in all the information below", fg='black',
                           font=("Arial", 15),
                           justify=CENTER,
                           background="#dea5a4")
        self.label.place(x=240, y=90)

        self.label_username = Label(self.root, text="@" + self.bid.get_initiator().get_username(), fg='black',
                                    font=("Arial", 15), justify=CENTER,
                                    background="#dea5a4")
        self.label_username.place(x=40, y=20)

        # Subject name label
        self.subject_name_label = Label(self.root, text="Subject name: ", font=("Arial", 14), background="#dea5a4")
        self.subject_name_label.place(x=70, y=165)

        self.subject = Text(height=1, width=len(
            bid.get_subject().get_name() + ": " + bid.get_subject().get_description()), font=("Arial", 12),
                            background="white")
        self.subject.insert(tkinter.END,
                            bid.get_subject().get_name() + ": " + bid.get_subject().get_description())
        self.subject.config(state=DISABLED)
        self.subject.place(x=275, y=175)

        # tutor qualification title
        self.qualification_title_label = Label(text="Your \nqualifications: ", font=("Arial", 14),
                                               background="#dea5a4",
                                               justify=LEFT)
        self.qualification_title_label.place(x=70, y=210)

        y = 245

        for qualification in self.user.get_qualifications():
            self.qualification_output = Text(height=1, width=len(
                qualification.get_title() + ": " + qualification.get_description()), font=("Arial", 12),
                                             background="white")
            self.qualification_output.insert(tkinter.END,
                                             qualification.get_title() + ": " + qualification.get_description())
            self.qualification_output.config(state=DISABLED)
            self.qualification_output.place(x=275, y=y)
            y = y + 35

        if len(self.user.get_qualifications()) == 0:
            self.qualification_output = Text(height=1, width=len("None") + 20, font=("Arial", 12),
                                             background="white")
            self.qualification_output.insert(tkinter.END, "None")
            self.qualification_output.config(state=DISABLED)
            self.qualification_output.place(x=275, y=y)
            y = y + 35

        # Number of sessions per week
        self.ses_per_week_label = Label(text="Preferred \nno.session(s) per week: ", font=("Arial", 14),
                                        background="#dea5a4",
                                        justify=LEFT)
        self.ses_per_week_label.place(x=70, y=y)
        y += 25
        self.ses_per_week = Entry(font=("Arial", 12), width=46)
        self.ses_per_week.place(x=275, y=y)

        # Length of class
        self.hours_per_lesson = Label(text="Preferred length of\n lesson (in hours): ", font=("Arial", 14),
                                      background="#dea5a4",
                                      justify=LEFT)
        y += 35
        self.hours_per_lesson.place(x=70, y=y)
        self.hours_per_lesson = Entry(font=("Arial", 12), width=46)
        y += 25
        self.hours_per_lesson.place(x=275, y=y)

        y += 40
        # Creating next button
        self.next_button = Button(text="Next", bg="#BFA2F7", font=("Arial", 14), fg='black', width="20",
                                  command=lambda: self.next_click(y))
        self.next_button.place(x=400, y=y)

        # Creating close bid button
        self.cancel_bid_button = Button(text="Cancel", bg="#ff6961", font=("Arial", 14), fg='black', width="20",
                                        command=lambda: self.controller.cancel_btn(self))
        self.cancel_bid_button.place(x=100, y=y)

        self.root.mainloop()

    def next_click(self, y):
        # Picking time

        # preferred Day

        self.day = [None] * int(self.ses_per_week.get())
        self.day_label = [None] * int(self.ses_per_week.get())
        self.time_hour = [None] * int(self.ses_per_week.get())
        self.time_min = [None] * int(self.ses_per_week.get())
        self.time_label = [None] * int(self.ses_per_week.get())
        y = y + 60
        for i in range(int(self.ses_per_week.get())):
            # Day
            self.day_label[i] = Label(text="Preferred day " + str(i + 1) + ": ", font=("Arial", 14),
                                      background="#dea5a4",
                                      justify=LEFT)
            self.day_label[i].place(x=70, y=y)
            self.day[i] = Entry(font=("Arial", 12), width=30)
            self.day[i].place(x=220, y=y + 5)

            # Time
            self.time_label[i] = Label(text="Time: ", font=("Arial", 14),
                                       background="#dea5a4",
                                       justify=LEFT)
            self.time_label[i].place(x=500, y=y)

            self.time_label_extra = Label(text=":", font=("Arial", 14),
                                          background="#dea5a4",
                                          justify=LEFT)
            self.time_label_extra.place(x=595, y=y)
            hour_string = StringVar()
            min_string = StringVar()
            last_value_sec = ""
            last_value = ""

            self.time_min[i] = Spinbox(
                from_=0,
                to=59,
                wrap=True,
                textvariable=min_string,
                font=("Arial", 12),
                width=2,
                justify=CENTER
            )

            self.time_hour[i] = Spinbox(from_=0,
                                        to=23,
                                        wrap=True,
                                        textvariable=hour_string,
                                        width=2,
                                        state="readonly",
                                        font=("Arial", 12),
                                        justify=CENTER
                                        )

            # Time configuration
            if last_value == "59" and min_string.get() == "0":
                hour_string.set(int(hour_string.get()) + 1 if hour_string.get() != "23" else 0)
                last_value = min_string.get()

            if last_value_sec == "59" and self.time_min[i].get() == "0":
                min_string.set(int(min_string.get()) + 1 if min_string.get() != "59" else 0)
            if last_value == "59":
                hour_string.set(int(hour_string.get()) + 1 if hour_string.get() != "23" else 0)
            self.time_hour[i].place(x=560, y=y + 5)
            self.time_min[i].place(x=610, y=y + 5)
            y += 35

        # preferred rate
        self.rate_label = Label(text="Preferred rate: ", font=("Arial", 14),
                                background="#dea5a4",
                                justify=LEFT)
        self.rate_label.place(x=70, y=y)

        self.rate = Entry(font=("Arial", 12), width=40)
        self.rate.place(x=200, y=y + 5)

        # Drop down list
        self.rate_per = StringVar(self.root)
        self.rate_per.set("per session")  # default value

        w = OptionMenu(self.root, self.rate_per, "per hour", "per session")
        w.place(x=590, y=y)

        y += 35
        # Custom contract
        self.customise_option_label = Label(text="Customise \nContract Length: ", font=("Arial", 14),
                                            background="#dea5a4",
                                            justify=LEFT)

        self.customise_option_label.place(x=70, y=y)

        self.customise_option = BooleanVar()
        self.customise_option_yes = Radiobutton(self.root, text='Yes', variable=self.customise_option, value=True)
        self.customise_option_yes.place(x=240, y=y + 25)
        self.customise_option_no = Radiobutton(self.root, text='No', variable=self.customise_option, value=False)
        self.customise_option_no.place(x=300, y=y + 25)

        self.contract_length_label = Label(text="Contract Length: ", font=("Arial", 14),
                                           background="#dea5a4",
                                           justify=LEFT)
        self.contract_length_label.place(x=360, y=y + 25)
        # Drop down list
        self.contract_length = StringVar(self.root)
        self.contract_length.set(6)  # default value

        contract_list = OptionMenu(self.root, self.contract_length, 3, 6, 12, 24, 36, 48)
        contract_list.place(x=530, y=y + 25)

        self.months_label = Label(text="Months", font=("Arial", 14),
                                  background="#dea5a4",
                                  justify=LEFT)
        self.months_label.place(x=590, y=y + 25)
        y += 55
        # Free class
        self.free_class_label = Label(text="Include free trial class:", font=("Arial", 14),
                                      background="#dea5a4",
                                      justify=LEFT)
        self.free_class_label.place(x=70, y=y)

        self.free_class = BooleanVar()
        self.free_class_yes = Radiobutton(self.root, text='Yes', variable=self.free_class, value=True)
        self.free_class_yes.place(x=280, y=y)
        self.free_class_no = Radiobutton(self.root, text='No', variable=self.free_class, value=False)
        self.free_class_no.place(x=340, y=y)

        y += 50

        # Creating next button
        offer_info = {
            "sesPerWeek": self.ses_per_week.get(),
            "hourPerLes": self.hours_per_lesson.get(),
            "day": self.day,
            "timeHour": self.time_hour,
            "timeMin": self.time_min,
            "rate": self.rate,
            "rateType": self.rate_per,
            "freeClass": self.free_class,
            "customContract": self.customise_option,
            "contractLen": self.contract_length
        }

        self.submit_button = Button(text="Submit offer", bg="#BFA2F7", font=("Arial", 14), fg='black', width="20",
                                    command=lambda: self.controller.submit_form(offer_info, self))

        self.submit_button.place(x=400, y=y)

        # Creating cancel button
        self.cancel_bid_button = Button(text="Cancel", bg="#ff6961", font=("Arial", 14), fg='black', width="20",
                                        command=lambda: self.controller.cancel_btn(self))
        self.cancel_bid_button.place(x=100, y=y)

        self.root.mainloop()


class OfferInfoView(Page):
    def __init__(self, controller, offer, initiator, user, bid):
        super().__init__(controller)
        self.bid = bid
        self.user = user
        self.initiator = initiator

        # Creating back button
        self.back_button = Button(text="Back", bg='#aec6cf', font=("Arial", 14), fg='white', width="20",
                                  command=lambda: self.controller.back_btn(self))
        self.back_button.place(x=15, y=40)

        # UserName label
        self.username_label = Label(text="Username: ", font=("Arial", 14), background="#dea5a4")
        self.username_label.place(x=120, y=80)

        # Making the username display

        self.username = Text(height=1, width=30, font=("Arial", 12), background="white")
        self.username.insert(tkinter.END, initiator.get_username())
        self.username.config(state=DISABLED)
        self.username.place(x=220, y=85)

        # Name label
        self.name_label = Label(text="Name: ", font=("Arial", 14), background="#dea5a4")
        self.name_label.place(x=120, y=120)

        # Making the name display

        self.name = Text(height=1, width=30, font=("Arial", 12), background="white")
        self.name.insert(tkinter.END, initiator.get_full_name())
        self.name.config(state=DISABLED)
        self.name.place(x=220, y=125)

        y = 155

        # Making the competencies label
        self.competencies_label = Label(text="Tutor's competency in this subject: ", font=("Arial", 14),
                                        background="#dea5a4")
        self.competencies_label.place(x=120, y=y)

        self.competencies_place = Text(height=1, width=10, font=("Arial", 12), background="white")
        self.competencies_place.insert(tkinter.END,
                                       initiator.get_competency(self.bid.get_subject().get_name()).get_level())
        self.competencies_place.config(state=DISABLED)
        self.competencies_place.place(x=430, y=y + 5)
        y += 35

        # Listing the qualifications
        # Making the qualifications label
        self.qualifications_label = Label(text="Qualifications: ", font=("Arial", 14), background="#dea5a4")
        self.qualifications_label.place(x=120, y=y)
        y += 35
        self.qualifications = initiator.get_qualifications()

        if not (len(self.qualifications) == 0):
            for i in self.qualifications:
                self.qualifications_place = Text(height=1, width=54, font=("Arial", 12),
                                                 background="white")
                self.qualifications_place.insert(tkinter.END, (i.get_title() + ": " +
                                                               i.get_description()))
                self.qualifications_place.config(state=DISABLED)
                self.qualifications_place.place(x=150, y=y)
                y += 35
        else:
            self.qualifications_place = Text(height=1, width=54, font=("Arial", 12),
                                             background="white")
            self.qualifications_place.insert(tkinter.END, "None")
            self.qualifications_place.config(state=DISABLED)
            self.qualifications_place.place(x=120, y=y + 5)
            y += 35

        # Rate
        self.rate_label = Label(text="Rate:", font=("Arial", 14),
                                background="#dea5a4",
                                justify=LEFT)
        self.rate_label.place(x=120, y=y)
        self.rate = Text(height=1, width=22, font=("Arial", 12), background="white")
        self.rate.insert(tkinter.END, offer.get_rate())
        self.rate.config(state=DISABLED)
        self.rate.place(x=170, y=y + 5)

        # rate type:
        self.rate_type = Text(height=1, width=29, font=("Arial", 12), background="white")
        self.rate_type.insert(tkinter.END, offer.get_rate_type())
        self.rate_type.config(state=DISABLED)
        self.rate_type.place(x=375, y=y + 5)

        y += 35
        # Number of sessions per week
        self.ses_per_week_label = Label(text="No.session(s) per week: ", font=("Arial", 14),
                                        background="#dea5a4",
                                        justify=LEFT)
        self.ses_per_week_label.place(x=120, y=y)
        self.ses_per_week = Text(height=1, width=34, font=("Arial", 12), background="white")
        self.ses_per_week.insert(tkinter.END, offer.get_ses_per_week())
        self.ses_per_week.config(state=DISABLED)
        self.ses_per_week.place(x=330, y=y + 5)

        y += 35
        # Duration of each session
        self.duration_label = Label(text="Duration of a session: ", font=("Arial", 14),
                                    background="#dea5a4",
                                    justify=LEFT)
        self.duration_label.place(x=120, y=y)
        self.duration = Text(height=1, width=36, font=("Arial", 12), background="white")
        self.duration.insert(tkinter.END, offer.get_duration())
        self.duration.config(state=DISABLED)
        self.duration.place(x=310, y=y + 5)

        # Lesson info
        y += 35
        self.lesson_info_label = Label(text="Lesson(s) Information: ", font=("Arial", 14), background="#dea5a4")
        self.lesson_info_label.place(x=120, y=y)
        for i in range(len(offer.get_day_and_time())):
            y += 35
            self.day_label = Label(text="Day: ", font=("Arial", 14), background="#dea5a4")
            self.day_label.place(x=170, y=y)
            self.day_info = Text(height=1, width=15, font=("Arial", 12), background="white")
            self.day_info.insert(tkinter.END, offer.get_day_and_time()[i]['day'])
            self.day_info.config(state=DISABLED)
            self.day_info.place(x=230, y=y + 5)

            self.time_label = Label(text="Time: ", font=("Arial", 14), background="#dea5a4")
            self.time_label.place(x=370, y=y)
            self.time_info = Text(height=1, width=15, font=("Arial", 12), background="white")
            self.time_info.insert(tkinter.END, offer.get_day_and_time()[i]['timeHour'] + ":" +
                                  offer.get_day_and_time()[i]['timeMin'])
            self.time_info.config(state=DISABLED)
            self.time_info.place(x=425, y=y + 5)

        y += 35

        # Contract length
        self.contract_length_label = Label(text="Contract Length: ", font=("Arial", 14),
                                           background="#dea5a4",
                                           justify=LEFT)
        self.contract_length_label.place(x=120, y=y)
        self.contact_length = Text(height=1, width=20, font=("Arial", 12), background="white")
        self.contact_length.insert(tkinter.END, str(offer.get_contract_len()) + " months")
        self.contact_length.config(state=DISABLED)
        self.contact_length.place(x=263, y=y + 5)

        y += 35
        # Free lesson
        self.free_lesson_label = Label(text="Free lesson: ", font=("Arial", 14),
                                       background="#dea5a4",
                                       justify=LEFT)
        self.free_lesson_label.place(x=120, y=y)
        self.free_lesson = Text(height=1, width=45, font=("Arial", 12), background="white")
        if offer.get_free_class():
            self.free_lesson.insert(tkinter.END, "Provided")
        else:
            self.free_lesson.insert(tkinter.END, "Not Provided")
        self.free_lesson.config(state=DISABLED)
        self.free_lesson.place(x=230, y=y + 5)

        y += 40
        if isinstance(self.user, Student):
            if isinstance(self.bid, OpenBid):
                self.accept_button = Button(text="Accept", bg='#77dd77', font=("Arial", 14), fg='white', width=20,
                                            command=lambda: self.controller.accept_btn(self))
                self.accept_button.place(x=130, y=y)
                self.decline_button = Button(text="Decline", bg='#ff6961', font=("Arial", 14), fg='white', width=20,
                                             command=lambda: self.controller.decline_btn(self))
                self.decline_button.place(x=400, y=y)
            else:
                self.accept_button = Button(text="Accept", bg='#77dd77', font=("Arial", 14), fg='white', width=13,
                                            command=lambda: self.controller.accept_btn(self))
                self.accept_button.place(x=130, y=y)
                self.decline_button = Button(text="Decline", bg='#ff6961', font=("Arial", 14), fg='white', width=13,
                                             command=lambda: self.controller.decline_btn(self))
                self.decline_button.place(x=300, y=y)
                self.chat_button = Button(text="Chat", bg="#BFA2F7", font=("Arial", 14), fg='white', width=13,
                                          command=lambda: self.controller.open_chat_btn(self))
                self.chat_button.place(x=470, y=y)
        else:
            if isinstance(self.bid, CloseBid):
                if offer.get_initiator_id() == self.user.get_id():
                    self.chat_button = Button(text="Chat", bg="#BFA2F7", font=("Arial", 14), fg='white', width=13,
                                              command=lambda: self.controller.open_chat_btn(self))
                    self.chat_button.place(x=300, y=y)

                    self.edit_button = Button(text="Edit", bg='#88EFEC', font=("Arial", 14), fg='black', width="20",
                                              command=lambda: self.controller.edit_btn(self))
                    self.edit_button.place(x=530, y=40)

        self.root.mainloop()


class ContractsListView(ScrollablePage):
    def __init__(self, controller, contracts):
        super().__init__(controller)
        self.contracts = contracts

        # labels
        self.label = Label(self.scroll.canvas, text="Contracts", fg='#5c3f8f', bg='#f244aa', width='12',
                           font=("Arial", 25),
                           justify=CENTER,
                           background="#dea5a4").grid(row=0, column=0, pady=10, padx=350, sticky="E")

        # Creating back button
        self.back_button = Button(self.scroll.frame, text="Back", bg='#aec6cf', font=("Arial", 14), fg='white',
                                  width="20", command=lambda: self.controller.back_btn(self)).grid(row=0, column=0,
                                                                                                   sticky="W", pady=10,
                                                                                                   padx=10)

        var = IntVar()
        Radiobutton(self.scroll.frame, text="Ongoing", variable=var, value=1,
                    command=lambda: self.controller.ongoing_btn(self)).grid(row=1, column=0, padx=300, sticky='W')

        Radiobutton(self.scroll.frame, text="Expired", variable=var, value=2,
                        command=lambda: self.controller.expired_btn(self)).grid(row=1, column=0, padx=400)

        Radiobutton(self.scroll.frame, text="Pending", variable=var, value=3,
                        command=lambda: self.controller.pending_btn(self)).grid(row=1, column=0, padx=300, sticky='E')
        # Bids list
        self.all_buttons = []
        self.show_contracts(self.contracts)

    def show_contracts(self, contracts):
        self.contracts = contracts

        # printing buttons for each bid on the screen
        row = 2
        for i in range(len(self.contracts)):
            row = row + 10

            btn = Button(self.scroll.frame,
                         text=self.contracts[i].get_summary(),
                         bg='#BFA2F7', font=("Arial", 14), fg='black',
                         width="64",
                         height="4",
                         command=lambda i=i: self.controller.show_contract_btn(self, self.contracts[i]))
            btn.grid(row=row, column=0, padx=20, pady=10)
            self.all_buttons.append(btn)

        self.root.mainloop()


class ContractInfoView(Page):
    def __init__(self, controller, contract, user):
        super().__init__(controller)
        self.contract = contract
        # Making Contracts title
        self.label = Label(self.root, text="Contract ", fg='#5c3f8f', font=("Arial", 25), justify=CENTER,
                           background="#dea5a4")
        self.label.place(x=320, y=60)

        # Student involved label
        self.student_label = Label(text="Student: ", font=("Arial", 14), background="#dea5a4")
        self.student_label.place(x=150, y=130)

        # Student involved
        self.student_place = Text(height=1, width=40, font=("Arial", 12),
                                  background="white")
        if isinstance(self.contract.get_first_party(), Student):
            self.student_place.insert(tkinter.END,
                                      self.contract.get_first_party().get_full_name() + ", " + self.contract.get_first_party().get_username())
            self.student = self.contract.get_first_party()
        else:
            self.student_place.insert(tkinter.END,
                                      self.contract.get_second_party().get_full_name() + ", " + self.contract.get_second_party().get_username())
            self.student = self.contract.get_second_party()

        self.student_place.config(state=DISABLED)
        self.student_place.place(x=225, y=135)

        # Tutor label
        self.tutor_label = Label(text="Tutor: ", font=("Arial", 14), background="#dea5a4")
        self.tutor_label.place(x=150, y=170)

        # Tutor involved
        self.tutor_place = Text(height=1, width=40, font=("Arial", 12),
                                background="white")
        if isinstance(self.contract.get_first_party(), Tutor):
            self.tutor_place.insert(tkinter.END,
                                    self.contract.get_first_party().get_full_name() + ", " + self.contract.get_first_party().get_username())
            self.tutor = self.contract.get_first_party()
        else:
            self.tutor_place.insert(tkinter.END,
                                    self.contract.get_second_party().get_full_name() + ", " + self.contract.get_second_party().get_username())
            self.tutor = self.contract.get_second_party()

        self.tutor_place.config(state=DISABLED)
        self.tutor_place.place(x=205, y=175)

        # Subject label
        self.subject_label = Label(text="Subject: ", font=("Arial", 14), background="#dea5a4")
        self.subject_label.place(x=150, y=210)

        # Subject
        self.subject = Text(height=1, width=45, font=("Arial", 12),
                            background="white")
        self.subject.insert(tkinter.END, self.contract.get_subject())
        self.subject.config(state=DISABLED)
        self.subject.place(x=225, y=215)

        # Competencies of tutor
        self.tutor_competency_label = Label(text="Tutor Competencies: ", font=("Arial", 14), background="#dea5a4")
        self.tutor_competency_label.place(x=150, y=245)
        # Listing competencies
        y = 245
        if len(self.tutor.get_competencies()) == 0:
            y += 35
            self.tutor_competency = Text(height=1, width=45, font=("Arial", 12), background="white")
            self.tutor_competency.insert(tkinter.END, "None")
            self.tutor_competency.config(state=DISABLED)
            self.tutor_competency.place(x=200, y=y)
        else:
            for i in self.tutor.get_competencies():
                y += 35
                self.tutor_competency = Text(height=1, width=45, font=("Arial", 12),
                                             background="white")
                self.tutor_competency.insert(tkinter.END, i)
                self.tutor_competency.config(state=DISABLED)
                self.tutor_competency.place(x=200, y=y)

        # Qualifications of tutor
        y += 35
        self.tutor_qualification_label = Label(text="Tutor Qualifications: ", font=("Arial", 14), background="#dea5a4")
        self.tutor_qualification_label.place(x=150, y=y)
        # Listing competencies

        if len(self.tutor.get_qualifications()) == 0:
            y += 35
            self.tutor_qualification = Text(height=1, width=45, font=("Arial", 12), background="white")
            self.tutor_qualification.insert(tkinter.END, "None")
            self.tutor_qualification.config(state=DISABLED)
            self.tutor_qualification.place(x=200, y=y)
        else:
            for i in self.tutor.get_qualifications():
                y += 35
                self.tutor_qualification = Text(height=1, width=45, font=("Arial", 12),
                                                background="white")
                self.tutor_qualification.insert(tkinter.END, i)
                self.tutor_qualification.config(state=DISABLED)
                self.tutor_qualification.place(x=200, y=y)

        # Number of lessons
        y += 35
        self.number_of_lessons_label = Label(text="No. of lessons: ", font=("Arial", 14), background="#dea5a4")
        self.number_of_lessons_label.place(x=150, y=y)
        self.number_of_lessons = Text(height=1, width=35, font=("Arial", 12), background="white")
        self.number_of_lessons.insert(tkinter.END, self.contract.get_additional_info()['sesPerWeek'])
        self.number_of_lessons.config(state=DISABLED)
        self.number_of_lessons.place(x=285, y=y + 5)

        # Duration
        y += 35
        self.duration_label = Label(text="Duration: ", font=("Arial", 14), background="#dea5a4")
        self.duration_label.place(x=150, y=y)
        self.duration = Text(height=1, width=40, font=("Arial", 12), background="white")
        self.duration.insert(tkinter.END, self.contract.get_additional_info()['hoursPerLesson'])
        self.duration.config(state=DISABLED)
        self.duration.place(x=230, y=y + 5)

        # Lesson info
        y += 35
        self.lesson_info_label = Label(text="Lesson(s) Information: ", font=("Arial", 14), background="#dea5a4")
        self.lesson_info_label.place(x=150, y=y)
        for i in range(len(self.contract.get_lesson_info()['day'])):
            y += 35
            self.day_label = Label(text="Day: ", font=("Arial", 14), background="#dea5a4")
            self.day_label.place(x=200, y=y)
            self.day_info = Text(height=1, width=15, font=("Arial", 12), background="white")
            self.day_info.insert(tkinter.END, self.contract.get_lesson_info()['day'][i])
            self.day_info.config(state=DISABLED)
            self.day_info.place(x=250, y=y + 5)

            self.time_label = Label(text="Time: ", font=("Arial", 14), background="#dea5a4")
            self.time_label.place(x=400, y=y)
            self.time_info = Text(height=1, width=15, font=("Arial", 12), background="white")
            self.time_info.insert(tkinter.END, self.contract.get_lesson_info()['timeHour'][i] + ":" +
                                  self.contract.get_lesson_info()['timeMin'][i])
            self.time_info.config(state=DISABLED)
            self.time_info.place(x=455, y=y + 5)

        # Rate
        y += 35
        self.rate_label = Label(text="Rate:", font=("Arial", 14),
                                background="#dea5a4",
                                justify=LEFT)
        self.rate_label.place(x=150, y=y)
        self.rate = Text(height=1, width=20, font=("Arial", 12), background="white")
        self.rate.insert(tkinter.END, self.contract.get_additional_info()['rate'])
        self.rate.config(state=DISABLED)
        self.rate.place(x=200, y=y + 5)

        # rate type:
        self.rate_type = Text(height=1, width=24, font=("Arial", 12), background="white")
        self.rate_type.insert(tkinter.END, self.contract.get_additional_info()['rateType'])
        self.rate_type.config(state=DISABLED)
        self.rate_type.place(x=410, y=y + 5)

        # Date created label
        y += 35
        self.date_created_label = Label(text="Date created: ", font=("Arial", 14), background="#dea5a4")
        self.date_created_label.place(x=150, y=y)

        # Date created
        self.date_created = Text(height=1, width=40, font=("Arial", 12),
                                 background="white")

        self.date_created.insert(tkinter.END,
                                 self.contract.get_date_created()[:-14] + " " + self.contract.get_date_created()[11:-8])
        self.date_created.config(state=DISABLED)
        self.date_created.place(x=270, y=y + 5)

        # Date expiry label

        if not (self.contract.get_expiry_date() is None):
            y += 35
            self.expiry_date_label = Label(text="Expiry date: ", font=("Arial", 14), background="#dea5a4")
            self.expiry_date_label.place(x=150, y=y)

            # Expiry date
            self.expiry_date = Text(height=1, width=40, font=("Arial", 12),
                                    background="white")
            self.expiry_date.insert(tkinter.END,
                                    self.contract.get_expiry_date()[:-14] + " " + self.contract.get_expiry_date()[
                                                                                  11:-8])
            self.expiry_date.config(state=DISABLED)
            self.expiry_date.place(x=255, y=y + 5)

            # Date signed label

            if not (self.contract.get_date_signed() is None):
                y += 35
                self.date_signed_label = Label(text="Date signed: ", font=("Arial", 14), background="#dea5a4")
                self.date_signed_label.place(x=150, y=y)

                # Date signed
                self.date_signed = Text(height=1, width=40, font=("Arial", 12),
                                        background="white")
                self.date_signed.insert(tkinter.END,
                                        self.contract.get_date_signed()[:-14] + " " + self.contract.get_date_signed()[
                                                                                      11:-8])
                self.date_signed.config(state=DISABLED)
                self.date_signed.place(x=260, y=y + 5)
            else:
                if isinstance(user, Student):
                    y += 35
                    self.date_signed_label = Label(text="Waiting for tutor confirmation! ", font=("Arial", 15),
                                                   background="#dea5a4")
                    self.date_signed_label.place(x=240, y=y)
                else:
                    y += 50
                    self.accept_button = Button(text="Accept", bg='#77dd77', font=("Arial", 14), fg='white', width=20,
                                                command=lambda: self.controller.accept_btn(self))
                    self.accept_button.place(x=130, y=y)
                    self.decline_button = Button(text="Decline", bg='#ff6961', font=("Arial", 14), fg='white', width=20,
                                                 command=lambda: self.controller.decline_btn(self))
                    self.decline_button.place(x=400, y=y)

        y += 50
        if isinstance(user, Student):
            if contract.get_expiry_date() <= datetime.now().isoformat()[:-3] + 'Z':
                # Creating reuse button
                self.reuse_button = Button(text="Reuse \nContract", bg='#f244aa', font=("Arial", 14), fg='white',
                                           width="20", command=lambda: self.controller.reuse_contract_btn(self))
                self.reuse_button.place(x=100, y=y)

                # Creating sign new contract
                self.sign_new_button = Button(text="Sign new contract\nwith this tutor", bg='#d152ff',
                                              font=("Arial", 14),
                                              fg='white', width="20",
                                              command=lambda: self.controller.sign_with_tutor_btn(self))
                self.sign_new_button.place(x=400, y=y)
                y += 100

        # Creating back button
        self.back_button = Button(text="Back", bg='#aec6cf', font=("Arial", 14), fg='white', width="20",
                                  command=lambda: self.controller.back_btn(self))
        self.back_button.place(x=270, y=y)


class ChooseNewContractView(Page):
    # allows to choose how to renew the contract
    def __init__(self, controller):
        super().__init__(controller)

        # Creating Reuse contract button
        self.reuse_contract_button = Button(text="Reuse contract", bg="#BFA2F7", font=("Arial", 14), fg='black',
                                            width="20", height="2", command=lambda: self.controller.reuse_terms_btn(self))
        self.reuse_contract_button.place(x=140, y=300)

        # Creating New terms of engagement button
        self.close_bid_button = Button(text="New terms\nof engagement", bg="#EF9DC9", font=("Arial", 14), fg='black',
                                       width="20", command=lambda: self.controller.new_terms_btn(self))
        self.close_bid_button.place(x=430, y=300)

        # Creating Cancel button
        self.cancel_bid_button = Button(text="Cancel", bg="#ff6961", font=("Arial", 14), fg='black', width="20",
                                        command=lambda: self.controller.cancel_btn(self))
        self.cancel_bid_button.place(x=270, y=400)
        self.root.mainloop()


class ReuseContractView(Page):
    def __init__(self, controller, contract, tutor):
        super().__init__(controller)
        # Renewing the contract with same terms
        self.contract = contract
        # Making Contracts title
        self.label = Label(self.root, text="Contract ", fg='#5c3f8f', font=("Arial", 25), justify=CENTER,
                           background="#dea5a4")
        self.label.place(x=320, y=60)

        # Student involved label
        self.student_label = Label(text="Student: ", font=("Arial", 14), background="#dea5a4")
        self.student_label.place(x=150, y=130)

        # Student involved
        self.student_place = Text(height=1, width=40, font=("Arial", 12),
                                  background="white")
        if isinstance(self.contract.get_first_party(), Student):
            self.student_place.insert(tkinter.END,
                                      self.contract.get_first_party().get_full_name() + ", " + self.contract.get_first_party().get_username())
            self.student = self.contract.get_first_party()
        else:
            self.student_place.insert(tkinter.END,
                                      self.contract.get_second_party().get_full_name() + ", " + self.contract.get_second_party().get_username())
            self.student = self.contract.get_second_party()

        self.student_place.config(state=DISABLED)
        self.student_place.place(x=225, y=135)

        # Tutor label
        self.tutor_label = Label(text="Tutor: ", font=("Arial", 14), background="#dea5a4")
        self.tutor_label.place(x=150, y=170)
        self.tutor = tutor
        # Tutor involved
        self.tutor_place = Text(height=1, width=40, font=("Arial", 12),
                                background="white")
        self.tutor_place.insert(tkinter.END,
                                self.tutor.get_full_name() + ", " + self.tutor.get_username())
        self.tutor_place.config(state=DISABLED)
        self.tutor_place.place(x=205, y=175)

        # Subject label
        self.subject_label = Label(text="Subject: ", font=("Arial", 14), background="#dea5a4")
        self.subject_label.place(x=150, y=210)

        # Subject
        self.subject = Text(height=1, width=45, font=("Arial", 12),
                            background="white")
        self.subject.insert(tkinter.END, self.contract.get_subject())
        self.subject.config(state=DISABLED)
        self.subject.place(x=225, y=215)

        # Competencies of tutor
        self.tutor_competency_label = Label(text="Tutor Competencies: ", font=("Arial", 14), background="#dea5a4")
        self.tutor_competency_label.place(x=150, y=245)
        # Listing competencies
        y = 245
        if len(self.tutor.get_competencies()) == 0:
            y += 35
            self.tutor_competency = Text(height=1, width=45, font=("Arial", 12), background="white")
            self.tutor_competency.insert(tkinter.END, "None")
            self.tutor_competency.config(state=DISABLED)
            self.tutor_competency.place(x=200, y=y)
        else:
            for i in self.tutor.get_competencies():
                y += 35
                self.tutor_competency = Text(height=1, width=45, font=("Arial", 12),
                                             background="white")
                self.tutor_competency.insert(tkinter.END, i)
                self.tutor_competency.config(state=DISABLED)
                self.tutor_competency.place(x=200, y=y)

        # Qualifications of tutor
        y += 35
        self.tutor_qualification_label = Label(text="Tutor Qualifications: ", font=("Arial", 14), background="#dea5a4")
        self.tutor_qualification_label.place(x=150, y=y)
        # Listing competencies

        if len(self.tutor.get_qualifications()) == 0:
            y += 35
            self.tutor_qualification = Text(height=1, width=45, font=("Arial", 12), background="white")
            self.tutor_qualification.insert(tkinter.END, "None")
            self.tutor_qualification.config(state=DISABLED)
            self.tutor_qualification.place(x=200, y=y)
        else:
            for i in self.tutor.get_qualifications():
                y += 35
                self.tutor_qualification = Text(height=1, width=45, font=("Arial", 12),
                                                background="white")
                self.tutor_qualification.insert(tkinter.END, i)
                self.tutor_qualification.config(state=DISABLED)
                self.tutor_qualification.place(x=200, y=y)

        # Number of lessons
        y += 35
        self.number_of_lessons_label = Label(text="No. of lessons: ", font=("Arial", 14), background="#dea5a4")
        self.number_of_lessons_label.place(x=150, y=y)
        self.number_of_lessons = Text(height=1, width=35, font=("Arial", 12), background="white")
        self.number_of_lessons.insert(tkinter.END, self.contract.get_additional_info()['sesPerWeek'])
        self.number_of_lessons.config(state=DISABLED)
        self.number_of_lessons.place(x=285, y=y + 5)

        # Duration
        y += 35
        self.duration_label = Label(text="Duration: ", font=("Arial", 14), background="#dea5a4")
        self.duration_label.place(x=150, y=y)
        self.duration = Text(height=1, width=40, font=("Arial", 12), background="white")
        self.duration.insert(tkinter.END, self.contract.get_additional_info()['hoursPerLesson'])
        self.duration.config(state=DISABLED)
        self.duration.place(x=230, y=y + 5)

        # Lesson info
        y += 35
        self.lesson_info_label = Label(text="Lesson(s) Information: ", font=("Arial", 14), background="#dea5a4")
        self.lesson_info_label.place(x=150, y=y)
        for i in range(len(self.contract.get_lesson_info()['day'])):
            y += 35
            self.day_label = Label(text="Day: ", font=("Arial", 14), background="#dea5a4")
            self.day_label.place(x=200, y=y)
            self.day_info = Text(height=1, width=15, font=("Arial", 12), background="white")
            self.day_info.insert(tkinter.END, self.contract.get_lesson_info()['day'][i])
            self.day_info.config(state=DISABLED)
            self.day_info.place(x=250, y=y + 5)

            self.time_label = Label(text="Time: ", font=("Arial", 14), background="#dea5a4")
            self.time_label.place(x=400, y=y)
            self.time_info = Text(height=1, width=15, font=("Arial", 12), background="white")
            self.time_info.insert(tkinter.END, self.contract.get_lesson_info()['timeHour'][i] + ":" +
                                  self.contract.get_lesson_info()['timeMin'][i])
            self.time_info.config(state=DISABLED)
            self.time_info.place(x=455, y=y + 5)

        # Rate
        y += 35
        self.rate_label = Label(text="Rate:", font=("Arial", 14),
                                background="#dea5a4",
                                justify=LEFT)
        self.rate_label.place(x=150, y=y)
        self.rate = Text(height=1, width=20, font=("Arial", 12), background="white")
        self.rate.insert(tkinter.END, self.contract.get_additional_info()['rate'])
        self.rate.config(state=DISABLED)
        self.rate.place(x=200, y=y + 5)

        # rate type:
        self.rate_type = Text(height=1, width=24, font=("Arial", 12), background="white")
        self.rate_type.insert(tkinter.END, self.contract.get_additional_info()['rateType'])
        self.rate_type.config(state=DISABLED)
        self.rate_type.place(x=410, y=y + 5)

        # Contract length
        y += 35
        self.customise_option_label = Label(text="Customise \nContract Length: ", font=("Arial", 14),
                                            background="#dea5a4",
                                            justify=LEFT)

        self.customise_option_label.place(x=70, y=y)

        self.customise_option = BooleanVar()
        self.customise_option_yes = Radiobutton(self.root, text='Yes', variable=self.customise_option, value=True)
        self.customise_option_yes.place(x=240, y=y + 25)
        self.customise_option_no = Radiobutton(self.root, text='No', variable=self.customise_option, value=False)
        self.customise_option_no.place(x=300, y=y + 25)

        self.contract_length_label = Label(text="Contract Length: ", font=("Arial", 14),
                                           background="#dea5a4",
                                           justify=LEFT)
        self.contract_length_label.place(x=360, y=y + 25)
        # Drop down list
        self.contract_length = StringVar(self.root)
        self.contract_length.set(6)  # default value

        contract_list = OptionMenu(self.root, self.contract_length, 3, 6, 12, 24, 36, 48)
        contract_list.place(x=530, y=y + 25)

        self.months_label = Label(text="Months", font=("Arial", 14),
                                  background="#dea5a4",
                                  justify=LEFT)
        self.months_label.place(x=590, y=y + 25)

        y += 70

        self.submit_button = Button(text="Submit offer", bg="#BFA2F7", font=("Arial", 14), fg='black', width="20",
                                    command=lambda: self.controller.submit_form(self.customise_option,
                                                                                self.contract_length, self, ))

        self.submit_button.place(x=400, y=y)

        # Creating cancel button
        self.cancel_bid_button = Button(text="Cancel", bg="#ff6961", font=("Arial", 14), fg='black', width="20",
                                        command=lambda: self.controller.cancel_btn(self))
        self.cancel_bid_button.place(x=100, y=y)


class NewTermsContractView(Page):
    def __init__(self, controller, user, tutor, subject, subject_level):
        super().__init__(controller)
        # Making Contracts title
        self.label = Label(self.root, text="Contract ", fg='#5c3f8f', font=("Arial", 25), justify=CENTER,
                           background="#dea5a4")
        self.label.place(x=320, y=60)

        # Student involved label
        self.student_label = Label(text="Student: ", font=("Arial", 14), background="#dea5a4")
        self.student_label.place(x=150, y=130)

        # Student involved
        self.student_place = Text(height=1, width=40, font=("Arial", 12),
                                  background="white")
        self.student_place.insert(tkinter.END,
                                  user.get_full_name() + ", " + user.get_username())
        self.student_place.config(state=DISABLED)
        self.student_place.place(x=225, y=135)

        # Tutor label
        self.tutor_label = Label(text="Tutor: ", font=("Arial", 14), background="#dea5a4")
        self.tutor_label.place(x=150, y=170)
        self.tutor = tutor
        # Tutor involved
        self.tutor_place = Text(height=1, width=40, font=("Arial", 12),
                                background="white")
        self.tutor_place.insert(tkinter.END,
                                self.tutor.get_full_name() + ", " + self.tutor.get_username())
        self.tutor_place.config(state=DISABLED)
        self.tutor_place.place(x=205, y=175)
        # Competencies of tutor
        self.tutor_competency_label = Label(text="Tutor Competencies: ", font=("Arial", 14), background="#dea5a4")
        self.tutor_competency_label.place(x=150, y=210)
        # Listing competencies
        y = 210
        if len(self.tutor.get_competencies()) == 0:
            y += 35
            self.tutor_competency = Text(height=1, width=45, font=("Arial", 12), background="white")
            self.tutor_competency.insert(tkinter.END, "None")
            self.tutor_competency.config(state=DISABLED)
            self.tutor_competency.place(x=200, y=y)
        else:
            for i in self.tutor.get_competencies():
                y += 35
                self.tutor_competency = Text(height=1, width=45, font=("Arial", 12),
                                             background="white")
                self.tutor_competency.insert(tkinter.END, i)
                self.tutor_competency.config(state=DISABLED)
                self.tutor_competency.place(x=200, y=y)

        # Qualifications of tutor
        y += 35
        self.tutor_qualification_label = Label(text="Tutor Qualifications: ", font=("Arial", 14), background="#dea5a4")
        self.tutor_qualification_label.place(x=150, y=y)
        # Listing competencies

        if len(self.tutor.get_qualifications()) == 0:
            y += 35
            self.tutor_qualification = Text(height=1, width=45, font=("Arial", 12), background="white")
            self.tutor_qualification.insert(tkinter.END, "None")
            self.tutor_qualification.config(state=DISABLED)
            self.tutor_qualification.place(x=200, y=y)
        else:
            for i in self.tutor.get_qualifications():
                y += 35
                self.tutor_qualification = Text(height=1, width=45, font=("Arial", 12),
                                                background="white")
                self.tutor_qualification.insert(tkinter.END, i)
                self.tutor_qualification.config(state=DISABLED)
                self.tutor_qualification.place(x=200, y=y)

        y += 35
        # Subject label
        self.subject_label = Label(text="Subject: ", font=("Arial", 14), background="#dea5a4")
        self.subject_label.place(x=150, y=y)

        # Subject
        self.subject = Text(height=1, width=45, font=("Arial", 12),
                            background="white")
        self.subject.insert(tkinter.END, subject)
        self.subject.config(state=DISABLED)
        self.subject.place(x=225, y=y + 5)
        # Competency level
        y += 35
        self.subject_level_label = Label(text="Required \ncompetency level: ", font=("Arial", 14), background="#dea5a4",
                                         justify=LEFT)
        self.subject_level_label.place(x=150, y=y)
        self.subject_level = Text(height=1, width=40, font=("Arial", 12), background="white")
        self.subject_level.insert(tkinter.END, str(subject_level))
        self.subject_level.config(state=DISABLED)
        self.subject_level.place(x=310, y=y + 25)
        y += 55
        # Number of sessions per week
        self.ses_per_week_label = Label(text="Preferred \nno.session(s) per week: ", font=("Arial", 14),
                                        background="#dea5a4",
                                        justify=LEFT)
        self.ses_per_week_label.place(x=150, y=y)
        self.ses_per_week = Entry(font=("Arial", 12), width=30)
        self.ses_per_week.place(x=355, y=y + 25)

        # Length of class
        y += 55
        self.hours_per_lesson = Label(text="Preferred length of\n lesson (in hours): ", font=("Arial", 14),
                                      background="#dea5a4",
                                      justify=LEFT)
        self.hours_per_lesson.place(x=150, y=y)
        self.hours_per_lesson = Entry(font=("Arial", 12), width=30)
        self.hours_per_lesson.place(x=355, y=y + 25)

        # Creating next button
        y += 50
        self.next_button = Button(text="Next", bg="#BFA2F7", font=("Arial", 14), fg='black', width="20",
                                  command=lambda: self.next_click(subject, subject_level, y))
        self.next_button.place(x=430, y=y)

        # Creating close bid button
        self.cancel_bid_button = Button(text="Cancel", bg="#ff6961", font=("Arial", 14), fg='black', width="20",
                                        command=lambda: self.controller.cancel_btn(self))
        self.cancel_bid_button.place(x=120, y=y)

    def next_click(self, subject, subject_level, y):

        self.day = [None] * int(self.ses_per_week.get())
        self.day_label = [None] * int(self.ses_per_week.get())
        self.time_hour = [None] * int(self.ses_per_week.get())
        self.time_min = [None] * int(self.ses_per_week.get())
        self.time_label = [None] * int(self.ses_per_week.get())
        y = y + 50
        for i in range(int(self.ses_per_week.get())):
            # Day
            self.day_label[i] = Label(text="Preferred day " + str(i + 1) + ": ", font=("Arial", 14),
                                      background="#dea5a4",
                                      justify=LEFT)
            self.day_label[i].place(x=150, y=y)
            self.day[i] = Entry(font=("Arial", 12), width=20)
            self.day[i].place(x=300, y=y + 5)

            # Time
            self.time_label[i] = Label(text="Time: ", font=("Arial", 14),
                                       background="#dea5a4",
                                       justify=LEFT)
            self.time_label[i].place(x=450, y=y)
            self.time_label_extra = Label(text=":", font=("Arial", 14),
                                          background="#dea5a4",
                                          justify=LEFT)
            self.time_label_extra.place(x=565, y=y)
            hour_string = StringVar()
            min_string = StringVar()
            last_value_sec = ""
            last_value = ""

            self.time_min[i] = Spinbox(
                from_=0,
                to=59,
                wrap=True,
                textvariable=min_string,
                font=("Arial", 12),
                width=2,
                justify=CENTER
            )

            self.time_hour[i] = Spinbox(from_=0,
                                        to=23,
                                        wrap=True,
                                        textvariable=hour_string,
                                        width=2,
                                        state="readonly",
                                        font=("Arial", 12),
                                        justify=CENTER
                                        )

            # Time configuration
            if last_value == "59" and min_string.get() == "0":
                hour_string.set(int(hour_string.get()) + 1 if hour_string.get() != "23" else 0)
                last_value = min_string.get()

            if last_value_sec == "59" and self.time_min[i].get() == "0":
                min_string.set(int(min_string.get()) + 1 if min_string.get() != "59" else 0)
            if last_value == "59":
                hour_string.set(int(hour_string.get()) + 1 if hour_string.get() != "23" else 0)
            self.time_hour[i].place(x=510, y=y + 5)
            self.time_min[i].place(x=560, y=y + 5)
            y += 35

        # preferred rate
        self.rate_label = Label(text="Preferred rate: ", font=("Arial", 14),
                                background="#dea5a4",
                                justify=LEFT)
        self.rate_label.place(x=150, y=y)
        self.rate = Entry(font=("Arial", 12), width=25)
        self.rate.place(x=280, y=y + 5)

        # Drop down list
        self.rate_per = StringVar(self.root)
        self.rate_per.set("per session")  # default value

        w = OptionMenu(self.root, self.rate_per, "per hour", "per session")
        w.place(x=520, y=y)

        # Contract length
        y += 35
        self.customise_option_label = Label(text="Customise \nContract Length: ", font=("Arial", 14),
                                            background="#dea5a4",
                                            justify=LEFT)

        self.customise_option_label.place(x=150, y=y)

        self.customise_option = BooleanVar()
        self.customise_option_yes = Radiobutton(self.root, text='Yes', variable=self.customise_option, value=True)
        self.customise_option_yes.place(x=300, y=y + 25)
        self.customise_option_no = Radiobutton(self.root, text='No', variable=self.customise_option, value=False)
        self.customise_option_no.place(x=360, y=y + 25)

        self.contract_length_label = Label(text="Contract Length: ", font=("Arial", 14),
                                           background="#dea5a4",
                                           justify=LEFT)
        self.contract_length_label.place(x=410, y=y + 25)
        # Drop down list
        self.contract_length = StringVar(self.root)
        self.contract_length.set(6)  # default value

        contract_list = OptionMenu(self.root, self.contract_length, 3, 6, 12, 24, 36, 48)
        contract_list.place(x=560, y=y + 25)

        self.months_label = Label(text="Months", font=("Arial", 14),
                                  background="#dea5a4",
                                  justify=LEFT)
        self.months_label.place(x=610, y=y + 25)

        y += 60
        # Creating submit button

        lesson_info = {
            "sesPerWeek": self.ses_per_week.get(),
            "hoursPerLes": self.hours_per_lesson.get(),
            "day": self.day,
            "timeHour": self.time_hour,
            "timeMin": self.time_min,
            "rate": self.rate,
            "rateType": self.rate_per,
            "customContract": self.customise_option,
            "contractLen": self.contract_length
        }

        self.submit_button = Button(text="Submit", bg="#BFA2F7", font=("Arial", 14), fg='black', width="20",
                                    command=lambda: self.controller.submit_form(lesson_info, subject, subject_level,
                                                                                self))
        self.submit_button.place(x=430, y=y)

        # Creating close bid button
        self.cancel_bid_button = Button(text="Cancel", bg="#ff6961", font=("Arial", 14), fg='black', width="20",
                                        command=lambda: self.controller.cancel_btn(self))
        self.cancel_bid_button.place(x=120, y=y)


class ChooseTutorForContractView(Page):
    # allows to choose how to renew the contract
    def __init__(self, controller):
        super().__init__(controller)

        # Creating Reuse contract button
        self.same_tutor_button = Button(text="Same Tutor", bg="#BFA2F7", font=("Arial", 14), fg='black',
                                            width="20", height="2", command=lambda: self.next_same_tutor())
        self.same_tutor_button.place(x=140, y=300)

        # Creating New terms of engagement button
        self.new_tutor_button = Button(text="New tutor", bg="#EF9DC9", font=("Arial", 14), fg='black',
                                       width="20", command=lambda: self.next_new_tutor())
        self.new_tutor_button.place(x=430, y=300)

        # Creating Cancel button
        self.cancel_button = Button(text="Cancel", bg="#ff6961", font=("Arial", 14), fg='black', width="20",
                                        command=lambda: self.controller.cancel_btn(self))
        self.cancel_button.place(x=270, y=400)
        self.root.mainloop()

    def next_same_tutor(self):
        self.next_button = Button(text="Next", bg="#A2B8F7", font=("Arial", 14), fg='black', width="20",
                                  command=lambda: self.controller.reuse_same_tutor_btn(self))
        self.next_button.place(x=270, y=450)

    def next_new_tutor(self):
        self.username= Label(text="Input tutor's \nusername: ", font=("Arial", 14),
                                               background="#dea5a4",
                                               justify=LEFT)
        self.username.place(x=140, y=445)
        self.username_input = Entry(font=("Arial", 12), width=53)
        self.username_input.place(x=245, y=455)

        self.next_button = Button(text="Next", bg="#A2B8F7", font=("Arial", 14), fg='black', width="20",
                                  command=lambda: self.controller.reuse_new_tutor_btn(self.username_input.get(), self))
        self.next_button.place(x=270, y=500)


class ChatView(Page):
    def __init__(self, controller, opponent_username):
        super().__init__(controller)

        # Back button
        # Creating back button
        self.back_button = Button(text="Back", bg='#aec6cf', font=("Arial", 14), fg='white',
                                  width="20",
                                  command=lambda: self.controller.back_btn(self)).place(x=15, y=20)
        # Create a Chat window
        self.chat_log = Text(self.root, bd=0, bg="white", height="8", width="50", font="Arial", )
        self.chat_log.insert(END, "Chat with @" + opponent_username + "..\n")
        self.chat_log.config(state=DISABLED)

        # Bind a scrollbar to the ChatView window
        self.scrollbar = Scrollbar(self.root, command=self.chat_log.yview, cursor="heart")
        self.chat_log['yscrollcommand'] = self.scrollbar.set
        self.scrollbar.config(command=self.chat_log.yview)

        # Create the Button to send message
        self.send_button = Button(self.root, width="12", text="Send", bg='#5c3f8f', fg='white', font=("Arial", 14),
                                  command=lambda: self.controller.send_btn(self))

        # Create the box to enter message
        self.entry_box = Text(self.root, bd=0, bg="white", width="29", height=2, font="Arial")
        self.entry_box.bind("<Return>", lambda event: self.controller.disable_entry(self))
        self.entry_box.bind("<KeyRelease-Return>", lambda event: self.controller.press_action(self))

        # Place all components on the screen
        self.scrollbar.place(x=656, y=100, height=386)
        self.chat_log.place(x=156, y=100, height=386, width=500)
        self.entry_box.place(x=280, y=495, height=50, width=395)
        self.send_button.place(x=156, y=495, height=50)

        controller.load_all_messages_screen(self)
        self.root.mainloop()
