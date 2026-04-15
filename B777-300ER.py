import customtkinter as ctk
from tkinter import messagebox


V_SPEEDS_FLAPS_5 = {
    240000: {"v1": 139, "vr": 144, "v2": 152},
    260000: {"v1": 145, "vr": 150, "v2": 158},
    280000: {"v1": 151, "vr": 156, "v2": 164},
    300000: {"v1": 157, "vr": 162, "v2": 170},
    320000: {"v1": 163, "vr": 168, "v2": 176},
    340000: {"v1": 170, "vr": 176, "v2": 184},
    351000: {"v1": 173, "vr": 180, "v2": 188}
}

V_SPEEDS_FLAPS_15 = {
    240000: {"v1": 132, "vr": 138, "v2": 145},
    260000: {"v1": 138, "vr": 144, "v2": 151},
    280000: {"v1": 145, "vr": 150, "v2": 156},
    300000: {"v1": 150, "vr": 155, "v2": 162},
    320000: {"v1": 155, "vr": 160, "v2": 168},
    340000: {"v1": 162, "vr": 170, "v2": 176},
    351000: {"v1": 165, "vr": 173, "v2": 180} 
}


def interpolate_v_speeds(weight, data_dict):
    weights = sorted(data_dict.keys())
    
    if weight <= weights[0]: return data_dict[weights[0]]
    if weight >= weights[-1]: return data_dict[weights[-1]]
    
    for i in range(len(weights) - 1): 
        w1, w2 = weights[i], weights[i+1] 
        if w1 <= weight <= w2:
            v_speeds = {} 
            for speed_type in ["v1", "vr", "v2"]:
                
                low_speed = data_dict[w1][speed_type] 
                
               
                high_speed = data_dict[w2][speed_type] 
              
                interpolated_value = round(low_speed + (weight - w1) * (high_speed - low_speed) / (w2 - w1))
                
                v_speeds[speed_type] = interpolated_value
            return v_speeds


class EFBApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("B777-300ER EFB - Version 1.0")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark") 
        
        
        self.label_title = ctk.CTkLabel(self, text="Boeing 777-300ER EFB", font=("Arial", 28, "bold"))
        self.label_title.pack(pady=20)

        
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=10, padx=20, fill="both", expand=True)

       
        self.create_input("Distance (NM):", 0, 0)
        self.entry_dist = self.last_entry
        
        self.create_input("TOW (KG):", 1, 0)
        self.entry_tow = self.last_entry

        self.create_input("Fuel Flow (KG/H):", 2, 0)
        self.entry_ff = self.last_entry
        
        self.create_input("Wind Component (KTS):", 3, 0)
        self.entry_wind = self.last_entry
        
        self.create_input("Temperature (C):", 4, 0)
        self.entry_temp = self.last_entry
        
        self.create_input("Cruise Speed (KTS):", 5, 0)
        self.entry_cruise = self.last_entry

        self.create_input("Flaps Setting (5 or 15):", 6, 0)
        self.entry_flaps = self.last_entry

      
        self.result_box = ctk.CTkTextbox(self.main_frame, width=300, height=200)
        self.result_box.grid(row=0, column=2, rowspan=4, padx=20, pady=20)
        self.result_box.insert("0.0", "RESULTS WILL APPEAR HERE...") 

        
        self.btn_calc = ctk.CTkButton(self, text="CALCULATE PERFORMANCE", command=self.calculate)
        self.btn_calc.pack(pady=20)

    def create_input(self, text, row, col):
        lbl = ctk.CTkLabel(self.main_frame, text=text, font=("Arial", 14))
        lbl.grid(row=row, column=col, padx=20, pady=10, sticky="e")
        entry = ctk.CTkEntry(self.main_frame, width=150)
        entry.grid(row=row, column=col+1, padx=10, pady=10)
        self.last_entry = entry

    def calculate(self):
      
        try:
            weight = float(self.entry_tow.get())

            speeds5 = interpolate_v_speeds(weight, V_SPEEDS_FLAPS_5)
            speeds15 = interpolate_v_speeds(weight, V_SPEEDS_FLAPS_15)
            
           
            self.result_box.delete("0.0", "end")
            res = f"--- TAKEOFF DATA ---\n"
            if self.entry_flaps.get() == "5":
                res += f"Flaps 5: V1={speeds5['v1']} KTS, VR={speeds5['vr']} KTS, V2={speeds5['v2']} KTS\n"
            elif self.entry_flaps.get() == "15":
                res += f"Flaps 15: V1={speeds15['v1']} KTS, VR={speeds15['vr']} KTS, V2={speeds15['v2']} KTS\n"
            res += f"-------------------\n"
            res += f"ETA: {round(float(self.entry_dist.get()) / (float(self.entry_cruise.get()) + float(self.entry_wind.get())), 2)} Hours\n"
           
            ground_speed = float(self.entry_cruise.get()) + float(self.entry_wind.get())


            trip_fuel = float(self.entry_ff.get()) * (float(self.entry_dist.get()) / ground_speed)

            res += f"Trip Fuel: {round(trip_fuel, 1)} KG\n"
            
            if float(self.entry_temp.get()) > 15:
                res += f"Temp is above ISA, expect reduced performance.\n"
            elif float(self.entry_temp.get()) < 15:
                res += f"Temp is below ISA, expect improved performance.\n"
            
           
            thrust = "TO"
            if weight < 280000: thrust = "TO 2"
            elif weight < 320000: thrust = "TO 1"
            
            res += f"THRUST: {thrust}"
            self.result_box.insert("0.0", res)
            
        except Exception as e:
            messagebox.showerror("Error", "Please enter valid numbers!")

if __name__ == "__main__":
    app = EFBApp()
    app.mainloop()
    