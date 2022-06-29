from tkinter import *
import tkinter as tk
import customtkinter
import sys
import os
import threading
from callSQL import sqlConnect
from chat import teamsChat


class vtKinterClass(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chat Selection")
        # Main Window
        self.geometry(f"{500}x{400}")

        # Main Frame
        self.MainFrame = customtkinter.CTkFrame(self, corner_radius=10, width=1000, height=500)
        self.MainFrame.pack(pady=20, expand=True)

        # Ticket Entry Section
        self.identifierFrame = customtkinter.CTkFrame(self.MainFrame, corner_radius=10)
        self.identifier = customtkinter.CTkEntry(
            self.identifierFrame,
            width=400,
            height=40,
            border_width=1,
            placeholder_text="Enter Identification Number",
            text_color="silver",
        )
        self.identifier.grid(row=0, column=0, padx=10, pady=10)

        # Button String Setup
        self.btn1 = tk.StringVar()
        self.btn2 = tk.StringVar()

        # Radio Button Setup
        self.buttomFrame = customtkinter.CTkFrame(self.MainFrame, corner_radius=10)
        self.buttomFrame.grid(row=0, column=0, padx=10, pady=10)

        # Radio Frames
        self.radioFrameLeft = customtkinter.CTkFrame(self.buttomFrame, corner_radius=10)
        self.radioFrameLeft.grid(row=0, column=0, padx=10, pady=10)

        # Right and CCM are shown/hidden using Functions at the bottom
        self.radioFrameRight = customtkinter.CTkFrame(self.buttomFrame, corner_radius=10)
        self.radioFrameCCM = customtkinter.CTkFrame(self.buttomFrame, corner_radius=10)

        # Team Radio Buttons
        self.radio_button = customtkinter.CTkRadioButton(
            self.radioFrameLeft,
            text="Portal Posse",
            variable=self.btn1,
            value="portal_posse",
            command=self.showRightRadioFrame,
        )
        self.radio_button2 = customtkinter.CTkRadioButton(
            self.radioFrameLeft,
            text="Data Chat",
            variable=self.btn1,
            value="mainDataChat",
            command=self.showRightRadioFrame,
        )
        self.radio_button3 = customtkinter.CTkRadioButton(
            self.radioFrameLeft,
            text="GCA Education Team",
            variable=self.btn1,
            value="gcaEduTeam",

            command=self.showRightRadioFrame,
        )
        self.radio_button4 = customtkinter.CTkRadioButton(
            self.radioFrameLeft,
            text="CCM Logistics",
            variable=self.btn1,
            value="ccmChat",
            command=self.showCCM,
        )
        self.radio_button5 = customtkinter.CTkRadioButton(
            self.radioFrameLeft,
            text="Code Collab",
            variable=self.btn1,
            value="code_collab",
            command=self.showRightRadioFrame,
        )

        # Query Radio Buttons
        self.radio_button6 = customtkinter.CTkRadioButton(
            self.radioFrameRight,
            text="Family Lookup",
            variable=self.btn2,
            value="Fam_Lookup",
        )
        self.radio_button7 = customtkinter.CTkRadioButton(
            self.radioFrameRight,
            text="Shipping Clearance",
            variable=self.btn2,
            value="shipClearance",
        )
        self.radio_button8 = customtkinter.CTkRadioButton(
            self.radioFrameRight,
            text="Current Equipment",
            variable=self.btn2,
            value="currentAssignments",
        )
        self.radio_button9 = customtkinter.CTkRadioButton(
            self.radioFrameRight,
            text="Unreturned Equipment",
            variable=self.btn2,
            value="unreturned",
        )
        self.radio_button10 = customtkinter.CTkRadioButton(
            self.radioFrameRight,
            text="Returned Equipment",
            variable=self.btn2,
            value="returns",
        )
        self.radio_button11 = customtkinter.CTkRadioButton(
            self.radioFrameCCM,
            text="CCM Stock",
            variable=self.btn2,
            value="ccmStock",
        )

        self.my_button = customtkinter.CTkButton(self.buttomFrame, text="Submit", command=lambda: threading.Thread(target=self.runIt).start())

        # Placement of the radio buttons
        self.radio_button.grid(row=1, column=0, sticky="nw")
        self.radio_button2.grid(row=2, column=0, sticky="nw")
        self.radio_button3.grid(row=3, column=0, sticky="nw")
        self.radio_button4.grid(row=4, column=0, sticky="nw")
        # self.radio_button5.grid(row=5, column=0, sticky="nw")
        self.radio_button6.grid(row=1, column=1, sticky="nw")
        self.radio_button7.grid(row=2, column=1, sticky="nw")
        self.radio_button8.grid(row=3, column=1, sticky="nw")
        self.radio_button9.grid(row=4, column=1, sticky="nw")
        self.radio_button10.grid(row=5, column=1, sticky="nw")
        self.radio_button11.grid(row=1, column=1, sticky="nw")

    def showRightRadioFrame(self):
        self.radioFrameCCM.grid_remove()
        self.radioFrameRight.grid(row=0, column=2, padx=10, pady=10)
        self.identifierFrame.grid(row=1, column=0, padx=10, pady=10)
        self.my_button.grid(row=2, column=1, sticky="nw")

    def showCCM(self):
        self.radioFrameRight.grid_remove()
        self.identifierFrame.grid_remove()
        self.radioFrameCCM.grid(row=0, column=2, padx=10, pady=10)
        self.my_button.grid(row=6, column=1, sticky="nw")

    def submitButton(self):
        print(self.btn1.get())
        print(self.btn2.get())
        print(self.identifier.get().strip())

    def destroyButton(self):
        self.submitButton()
        self.destroy()

    def runIt(self):
        print(self.btn1.get())
        print(self.btn2.get())
        print(self.identifier.get().strip())
        identifier = str(self.identifier.get().strip())
        sqlQuery = self.btn2.get()
        msTeam = self.btn1.get()

        sqlProc = sqlConnect(identifier).callThatSQL(sqlQuery)
        print(sqlProc)
        teamsChat(msTeam).sendTable(sqlProc)


if __name__ == '__main__':
    app = vtKinterClass()
    app.mainloop()
