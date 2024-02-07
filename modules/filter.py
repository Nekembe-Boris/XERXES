"""Module tasked with Filtering on the ADVANCED TAB"""
from tkinter import Label, StringVar, Frame
from tkinter import messagebox
import customtkinter
import pandas
from modules.functions import  list_box, bind_box, clear, style_bg, forget


FG = "white"
BACKGROUND_COLOR = "#212121"
FONT1 = ("Century Gothic", 10, "bold")
FONT3 = ("Century Gothic", 8, "bold")
records = ["Entries", "Exit", "General_ledger"]
ad_filter = ["Article", "ArticleID", "Date"]


class Filter():
    """
    Filters data and displays filtered data in listboxes
    """
    def __init__(self, frame:Frame, path):
        self.frame = frame
        self.file_path = path

        self.rec_var = StringVar()
        self.filter_var = StringVar()

        self.filter_label = Label(master=self.frame, text="FILTER RECORDS", font=FONT1, bg=BACKGROUND_COLOR, fg="red")
        self.filter_label.place(x=350, y=30)

        self.rec_typebox = customtkinter.CTkComboBox(master=self.frame, width=250, variable=self.rec_var, values=records, font=FONT3)
        self.rec_typebox.set("Select Record")
        self.rec_typebox.place(x=50, y=70)

        self.ad_typebox = customtkinter.CTkComboBox(master=self.frame, width=250, variable=self.filter_var, values=ad_filter, font=FONT3)
        self.ad_typebox.set("Filter By")
        self.ad_typebox.place(x=50, y=130)

        self.select_btn = customtkinter.CTkButton(master=self.frame, text="Apply", width=80, font=FONT3, command=self.get_info)
        self.select_btn.place(x=280, y=100)

        self.filter_btn = customtkinter.CTkButton(master=self.frame, text="Filter", width=80, font=FONT3, command=self.filter_data)

        self.cancel_filter_btn = customtkinter.CTkButton(master=self.frame, text="Cancel", width=80, font=FONT3, hover_color="red", command=self.reset_filter)

        self.fil_details_box = customtkinter.CTkComboBox(master=self.frame, width=250, font=FONT3)

        self.article_label= Label(master=self.frame, text="Article", font=FONT3, fg=FG, bg=BACKGROUND_COLOR)
        self.article_label.place(x=240, y=250)

        self.id_label= Label(master=self.frame, text="Article ID", font=FONT3, fg=FG, bg=BACKGROUND_COLOR)
        self.id_label.place(x=440, y=250)

        self.date_label= Label(master=self.frame, text="Date", font=FONT3, fg=FG, bg=BACKGROUND_COLOR)
        self.date_label.place(x=590, y=250)

        self.qty_label= Label(master=self.frame, text="QTY", font=FONT3, fg=FG, bg=BACKGROUND_COLOR)
        self.qty_label.place(x=700, y=250)

        self.fil_art_listbox = list_box(frame=self.frame, x_cor=140, y_cor=280, l_height=40, l_width=35)

        self.fil_id_listbox = list_box(frame=self.frame, x_cor=360, y_cor=280, l_height=40, l_width=30)

        self.fil_date_listbox = list_box(frame=self.frame, x_cor=550, y_cor=280, l_height=40, l_width=20)

        self.fil_quatity_listbox = list_box(frame=self.frame, x_cor=680, y_cor=280, l_height=40, l_width=10)

        bind_box(self.fil_art_listbox, self.fil_id_listbox, self.fil_date_listbox, self.fil_quatity_listbox, func=self.mousewheel)

    def mousewheel(self, event):
        """Responsible for binding all listboxes to mousewheel"""
        self.fil_art_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.fil_id_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.fil_date_listbox.yview_scroll(-2 * int(event.delta / 120), "units")
        self.fil_quatity_listbox.yview_scroll(-2 * int(event.delta / 120), "units")


    def get_info(self):
        """Function fills the Select combobox based on the Record and Filter param selected"""

        if (sheet := self.rec_typebox.get()) not in records or (filter_param := self.ad_typebox.get()) not in ad_filter:
            messagebox.showinfo(
                title="Error",
                message="No  Selected Record or Filter By"
            )
        else:

            self.fil_details_box.set(f"Select {filter_param}:")
            self.fil_details_box.place(x=400, y=70)
            self.filter_btn.place(x=565, y=100)
            self.cancel_filter_btn.place(x=565, y=130)

            try:
                data = pandas.read_csv(f"{self.file_path}/data/{sheet}.csv")
            except FileNotFoundError:
                messagebox.showinfo(
                title="Error",
                message=f"{sheet} data does not exist yet"
                )
            else:

                new_box_data = data.loc[:, f"{filter_param}"].to_list()
                fil_box_data = []
                for item in new_box_data:
                    if item not in fil_box_data:
                        fil_box_data.append(item)

                self.fil_details_box.configure(values=fil_box_data)


    def filter_data(self):
        """
        - Gets filtered data based on the inputs and displayes these data in the listboxes
        """
        clear(self.fil_art_listbox, self.fil_id_listbox, self.fil_date_listbox, self.fil_quatity_listbox)

        sheet = self.rec_typebox.get()
        filter_param = self.ad_typebox.get()
        filter_key = self.fil_details_box.get()

        if not sheet or not filter_param or not filter_key:
            messagebox.showinfo(
                title="Error",
                message="Check for empty Fields"
                )
        else:
            data = pandas.read_csv(f"{self.file_path}/data/{sheet}.csv")

            filtered_df = data.loc[data[f'{filter_param}'] == filter_key]

            if filtered_df.empty:
                messagebox.showinfo(
                    title="Error",
                    message="Data does not exist\nVerify filter parameters"
                    )
            else:
                filtered_df.to_csv(f"{self.file_path}/data/filtered.csv", index=False)

                filtered_data = pandas.read_csv(f"{self.file_path}/data/filtered.csv")
                entries_article_list = filtered_data.Article.to_list()
                entries_article_id_list = filtered_data.ArticleID.to_list()
                entries_date_list = filtered_data.Date.to_list()
                entries_qty_list = filtered_data.Quantity.to_list()

                rev_index = len(entries_date_list)

                for item in entries_article_list:
                    self.fil_art_listbox.insert(0, item)

                for item in entries_article_id_list:
                    self.fil_id_listbox.insert(0, item)

                for item in entries_date_list:
                    self.fil_date_listbox.insert(0, item)

                for item in entries_qty_list:
                    self.fil_quatity_listbox.insert(0, item)


                box_list = (self.fil_art_listbox, self.fil_id_listbox, self.fil_date_listbox, self.fil_quatity_listbox)

                style_bg(box=box_list, length=rev_index)

                forget(self.fil_details_box, self.filter_btn)
                self.rec_typebox.set("Select Record")
                self.ad_typebox.set("Filter By")

                
    def reset_filter(self):
        """
        Cancels the ongoing filter
        """
        forget(self.fil_details_box, self.filter_btn, self.cancel_filter_btn)