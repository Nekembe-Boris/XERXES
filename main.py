"""This module generates the GUI Interface of this software"""
from tkinter import ttk
import customtkinter
from entry import Input, RecentEntries
from exit import Exit, RecentExits
from stk_check import StockLook
from filter import Filter


BACKGROUND_COLOR = "#DDD0C8"
FG_COLOR = "#212121"
customtkinter.set_default_color_theme("dark-blue")

class InvManager():

    def __init__(self) :
        self.root = customtkinter.CTk()
        self.root.title("Inventory Manager 2.0")
        self.root.state("zoomed")
        # self.root.config(bg=BACKGROUND_COLOR)

        self.screen_height = self.root.winfo_screenheight()
        self.screen_width = self.root.winfo_screenwidth()

        self.main_tab = ttk.Notebook(self.root)
        self.main_tab.pack(fill="both")

        ##########-----EXIT TAB-----###############
        #main frame for the EXIT Tab
        self.exit_frame = customtkinter.CTkFrame(master=self.main_tab, height=self.screen_height, width=self.screen_width, fg_color=FG_COLOR)
        self.exit_frame.pack(fill="both", expand=1)

        #frame for the recent exit section of the tab.
        self.exit_info_frame = customtkinter.CTkFrame(master=self.exit_frame, height=820, width=720)
        self.exit_info_frame.grid(column=1, row=0)
        self.exit_info_sec = RecentExits(frame=self.exit_info_frame)

        #frame for the withdraw section of the Tab
        self.output_frame = customtkinter.CTkFrame(master=self.exit_frame, height=820, width=550)
        self.output_frame.grid(column=0, row=0)
        self.exit_sec = Exit(frame=self.output_frame, updates=self.exit_info_sec)

        ###########-------ENTRY TAB-----################
        #main frame for the ENTRY Tab
        self.entry_frame = customtkinter.CTkFrame(master=self.main_tab, height=self.screen_height, width=self.screen_width, fg_color=FG_COLOR)
        self.entry_frame.pack(fill="both", expand=1)

        #frame for the recent entries section of the tab.
        self.info_frame = customtkinter.CTkFrame(master=self.entry_frame, height=820, width=720)
        self.info_frame.grid(column=1, row=0)
        self.info_sec = RecentEntries(frame=self.info_frame)

        #frame for the input section of the Entry Tab
        self.input_frame = customtkinter.CTkFrame(master=self.entry_frame, height=820, width=550)
        self.input_frame.grid(column=0, row=0)
        self.entry_sec = Input(frame=self.input_frame, updates=self.info_sec, exit_up=self.exit_sec)

        ##########-------ADVANCED TAB-------##############
        #main frame for the ADVANCED Tab
        self.advanced_frame = customtkinter.CTkFrame(master=self.main_tab, height=self.screen_height, width=self.screen_width, fg_color=FG_COLOR)
        self.advanced_frame.pack(fill="both", expand=1)

        #frame for the verify and reports section of the tab.
        self.check_report_frame = customtkinter.CTkFrame(master=self.advanced_frame, height=820, width=500)
        self.check_report_frame.grid(column=0, row=0)
        self.stock_check = StockLook(frame=self.check_report_frame, entry_update=self.entry_sec, exit_update=self.exit_sec)

        #frame for the filter section of the tab.
        self.filter_frame = customtkinter.CTkFrame(master=self.advanced_frame, height=820, width=780)
        self.filter_frame.grid(column=1, row=0)
        self.filter_sec = Filter(frame=self.filter_frame)

        
        ##########-------HOME TAB-------##############
        #main frame for the ADVANCED Tab
        self.home_frame = customtkinter.CTkFrame(master=self.main_tab, height=self.screen_height, width=self.screen_width, fg_color=FG_COLOR)
        self.home_frame.pack(fill="both", expand=1)

        #frame for the Create project section of the tab.
        self.create_project_frame = customtkinter.CTkFrame(master=self.home_frame, height=820, width=500)
        self.create_project_frame.grid(column=0, row=0)
        # self.stock_check = StockLook(frame=self.check_report_frame, entry_update=self.entry_sec, exit_update=self.exit_sec)

        #making frame screen responsive
        IN_COLUMNS = 2
        for i in range(IN_COLUMNS):
            self.advanced_frame.grid_columnconfigure(i,  weight = 1)
            self.entry_frame.grid_columnconfigure(i,  weight = 1)
            self.exit_frame.grid_columnconfigure(i,  weight = 1)

        ################################################
        self.main_tab.add(self.home_frame, text="     HOME     ")
        self.main_tab.add(self.entry_frame, text="     ENTRY     ")
        self.main_tab.add(self.exit_frame, text="     EXIT     ")
        self.main_tab.add(self.advanced_frame, text="     ADVANCED     ")

        self.root.mainloop()


InvManager()
