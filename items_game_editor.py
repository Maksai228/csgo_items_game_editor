import os
import sys
import time
import re
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Colors
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class ItemsGameEditor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Valve Items Game Direct Injector Studio v3.0")
        self.geometry("1150x850")
        self.configure(fg_color="#F4F7F9") # color
        
        self.resizable(False, False) 

        self.file_path = None
        
        # rarites
        self.rarity_map = {
            "Covert (Red)": "legendary",
            "Classified (Pink)": "mythical",
            "Restricted (Purple)": "rare",
            "Mil-Spec (Blue)": "uncommon",
            "Industrial Grade (Light Blue)": "common",
            "Consumer Grade (Gray)": "default"
        }
        
        # idk what is this
        self.master_weapons = ["weapon_ak47", "weapon_awp", "weapon_deagle", "weapon_m4a1_silencer", "weapon_glock"]
        self.master_paints = ["aa_fade", "cu_ak47_asimov", "cu_awp_dragon_lore", "am_ruby", "an_sapphire"]
        self.master_collections = ["set_community_1", "set_bravo_i", "set_dust_2"]
        
        self.weapons = list(self.master_weapons)
        self.paint_kits = list(self.master_paints)
        self.collections = list(self.master_collections)
        
        self.next_free_id = 10001

        self.setup_ui()

    def setup_ui(self):
        self.tabview = ctk.CTkTabview(
            self, 
            width=1130, 
            height=810, 
            fg_color="#FFFFFF", 
            border_color="#002B5C", 
            border_width=1
        )
        self.tabview.pack(padx=10, pady=15, fill="both", expand=True)

        self.tabview._segmented_button.configure(
            selected_color="#002B5C", 
            selected_hover_color="#00418A",
            unselected_color="#1A1A1A",
            text_color="#FFFFFF"
        )

        self.tabview.add("Skin Editor")
        self.tabview.add("Collection Editor")

        self.setup_skin_tab()
        self.setup_collection_tab()

    def setup_skin_tab(self):
        tab = self.tabview.tab("Skin Editor")

        left_frame = ctk.CTkFrame(tab, width=530, fg_color="#FFFFFF")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.lbl_status = ctk.CTkLabel(left_frame, text="File Status: Waiting for items_game.txt...", text_color="#6C757D", font=("Arial", 13, "bold"))
        self.lbl_status.pack(pady=10)

        self.btn_load = ctk.CTkButton(left_frame, text="Load items_game.txt", fg_color="#002B5C", hover_color="#00418A", text_color="#FFFFFF", font=("Arial", 13, "bold"), command=self.load_file)
        self.btn_load.pack(padx=20, pady=5, fill="x")

        # --- Weapons ---
        ctk.CTkLabel(left_frame, text="1. Select Target Weapon:", text_color="#1A1A1A", font=("Arial", 12, "bold"), anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.search_weapon = ctk.CTkEntry(left_frame, placeholder_text="🔍 Type to search weapon...", fg_color="#F4F7F9", text_color="#1A1A1A", border_color="#E0E6ED")
        self.search_weapon.pack(padx=20, pady=2, fill="x")
        self.search_weapon.bind("<KeyRelease>", self.filter_weapons)
        
        self.combo_weapon = ctk.CTkComboBox(left_frame, values=self.weapons, fg_color="#FFFFFF", text_color="#1A1A1A", button_color="#002B5C")
        self.combo_weapon.pack(padx=20, pady=2, fill="x")

        # --- Textures ---
        ctk.CTkLabel(left_frame, text="2. Select Paint Kit (Visual Source):", text_color="#1A1A1A", font=("Arial", 12, "bold"), anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.search_paint = ctk.CTkEntry(left_frame, placeholder_text="🔍 Type to search paint kit...", fg_color="#F4F7F9", text_color="#1A1A1A", border_color="#E0E6ED")
        self.search_paint.pack(padx=20, pady=2, fill="x")
        self.search_paint.bind("<KeyRelease>", self.filter_paints)
        
        self.combo_paint = ctk.CTkComboBox(left_frame, values=self.paint_kits, fg_color="#FFFFFF", text_color="#1A1A1A", button_color="#002B5C")
        self.combo_paint.pack(padx=20, pady=2, fill="x")

        self.check_custom = ctk.CTkCheckBox(left_frame, text="Create Custom ID Node (Required for Emulator Inventory)", text_color="#1A1A1A", font=("Arial", 12), fg_color="#002B5C", command=self.toggle_custom_mode)
        self.check_custom.pack(padx=20, pady=15, anchor="w")

        self.custom_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        
        ctk.CTkLabel(self.custom_frame, text="Target Unique Skin ID (Auto-picked slot):", text_color="#1A1A1A", anchor="w").pack(fill="x")
        self.entry_id = ctk.CTkEntry(self.custom_frame, fg_color="#F4F7F9", text_color="#1A1A1A", border_color="#E0E6ED", placeholder_text="e.g. 10089")
        self.entry_id.pack(pady=(2, 8), fill="x")

        ctk.CTkLabel(self.custom_frame, text="New Unique Technical Paint Name:", text_color="#1A1A1A", anchor="w").pack(fill="x")
        self.entry_skin_name = ctk.CTkEntry(self.custom_frame, fg_color="#F4F7F9", text_color="#1A1A1A", border_color="#E0E6ED", placeholder_text="e.g. cz75_sapphire_custom")
        self.entry_skin_name.pack(pady=2, fill="x")

        # --- Rarity ---
        ctk.CTkLabel(left_frame, text="3. Select Rarity Tier (Item Color Frame):", text_color="#1A1A1A", font=("Arial", 12, "bold"), anchor="w").pack(padx=20, pady=(5, 0), fill="x")
        self.combo_rarity = ctk.CTkComboBox(left_frame, values=list(self.rarity_map.keys()), fg_color="#FFFFFF", text_color="#1A1A1A", button_color="#002B5C")
        self.combo_rarity.pack(padx=20, pady=5, fill="x")
        self.combo_rarity.set("Covert (Red)")

        # --- Collection ---
        ctk.CTkLabel(left_frame, text="4. Assign to Target Collection Set:", text_color="#1A1A1A", font=("Arial", 12, "bold"), anchor="w").pack(padx=20, pady=(5, 0), fill="x")
        self.search_coll = ctk.CTkEntry(left_frame, placeholder_text="🔍 Type to search collection...", fg_color="#F4F7F9", text_color="#1A1A1A", border_color="#E0E6ED")
        self.search_coll.pack(padx=20, pady=2, fill="x")
        self.search_coll.bind("<KeyRelease>", self.filter_collections)
        
        self.combo_coll = ctk.CTkComboBox(left_frame, values=self.collections, fg_color="#FFFFFF", text_color="#1A1A1A", button_color="#002B5C")
        self.combo_coll.pack(padx=20, pady=2, fill="x")

        self.btn_save = ctk.CTkButton(left_frame, text="Inject Config Blocks", fg_color="#002B5C", hover_color="#00418A", text_color="#FFFFFF", font=("Arial", 14, "bold"), height=40, command=self.inject_skin_to_file)
        self.btn_save.pack(padx=20, pady=25, fill="x")

        right_frame = ctk.CTkFrame(tab, width=490, fg_color="#1E293B")
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(right_frame, text="Live Operation Terminal Log:", text_color="#F8FAFC", font=("Arial", 12, "bold"), anchor="w").pack(padx=15, pady=5, fill="x")
        self.txt_log = ctk.CTkTextbox(right_frame, width=460, height=640, fg_color="#0F172A", text_color="#38BDF8", font=("Consolas", 12))
        self.txt_log.pack(padx=15, pady=5, fill="both", expand=True)
        
        self.log("System initialization complete. Awaiting items_game.txt alignment.")

    def setup_collection_tab(self):
        tab = self.tabview.tab("Collection Editor")
        
        center_frame = ctk.CTkFrame(tab, width=650, height=450, fg_color="#FFFFFF", border_color="#002B5C", border_width=1)
        center_frame.pack(expand=True, padx=50, pady=50)

        ctk.CTkLabel(center_frame, text="Create Custom Item Collection", text_color="#002B5C", font=("Arial", 22, "bold")).pack(pady=25)

        ctk.CTkLabel(center_frame, text="Technical Collection Key Name (Must start with 'set_'):\nWarning: Use lowercase and underscores only!", text_color="#1A1A1A", font=("Arial", 12, "bold"), justify="left", anchor="w").pack(padx=50, pady=(10, 0), fill="x")
        self.entry_coll_name = ctk.CTkEntry(center_frame, fg_color="#F4F7F9", text_color="#1A1A1A", border_color="#E0E6ED", placeholder_text="set_my_experimental_pack", width=450)
        self.entry_coll_name.pack(padx=50, pady=10)

        self.btn_create_coll = ctk.CTkButton(center_frame, text="Inject Collection Node into Config", fg_color="#002B5C", hover_color="#00418A", text_color="#FFFFFF", width=450, font=("Arial", 13, "bold"), height=35, command=self.create_collection)
        self.btn_create_coll.pack(padx=50, pady=35)
        
        ctk.CTkLabel(center_frame, text="Notice: Newly added nodes sync cross-tab instantly without a reload.", text_color="#6C757D", font=("Arial", 12, "italic")).pack(pady=(0, 20))


    def log(self, text):
        self.txt_log.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {text}\n")
        self.txt_log.see(tk.END)

    def filter_weapons(self, event=None):
        query = self.search_weapon.get().strip().lower()
        self.weapons = [w for w in self.master_weapons if query in w.lower()]
        self.combo_weapon.configure(values=self.weapons if self.weapons else ["No matches"])
        self.combo_weapon.set(self.weapons[0] if self.weapons else "No matches")

    def filter_paints(self, event=None):
        query = self.search_paint.get().strip().lower()
        self.paint_kits = [p for p in self.master_paints if query in p.lower()]
        self.combo_paint.configure(values=self.paint_kits if self.paint_kits else ["No matches"])
        self.combo_paint.set(self.paint_kits[0] if self.paint_kits else "No matches")

    def filter_collections(self, event=None):
        query = self.search_coll.get().strip().lower()
        self.collections = [c for c in self.master_collections if query in c.lower()]
        self.combo_coll.configure(values=self.collections if self.collections else ["No matches"])
        self.combo_coll.set(self.collections[0] if self.collections else "No matches")

    def toggle_custom_mode(self):
        if self.check_custom.get() == 1:
            self.custom_frame.pack(padx=20, pady=5, fill="x")
        else:
            self.custom_frame.pack_forget()

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Items Configuration Profile", "items_game.txt"), ("All Files", "*.*")])
        if path:
            self.file_path = path
            self.lbl_status.configure(text=f"Linked: {os.path.basename(path)}", text_color="#22C55E")
            self.log(f"[+] File linked successfully: {path}")
            
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                found_weapons = sorted(list(set([
                    w for w in re.findall(r'"(weapon_[a-zA-Z0-9_]+)"', content) 
                    if not w.endswith("_prefab")
                ])))
                
                found_colls = sorted(list(set(re.findall(r'"(set_[a-zA-Z0-9_]+)"', content))))
                
                found_paints = []
                existing_ids = []
                self.next_free_id = 10001
                
                pk_start = content.find('"paint_kits"')
                if pk_start != -1:
                    open_brace = content.find('{', pk_start)
                    if open_brace != -1:
                        brace_count = 1
                        current_idx = open_brace + 1
                        length = len(content)
                        while brace_count > 0 and current_idx < length:
                            if content[current_idx] == '{': brace_count += 1
                            elif content[current_idx] == '}': brace_count -= 1
                            current_idx += 1
                        
                        pk_block = content[open_brace:current_idx]
                        pk_entries = re.findall(r'"(\d+)"\s*\{([^}]+)\}', pk_block)
                        for pk_id, pk_body in pk_entries:
                            name_match = re.search(r'"name"\s+"([^"]+)"', pk_body)
                            if name_match:
                                pk_name = name_match.group(1)
                                if "prefab" not in pk_name.lower():
                                    found_paints.append(pk_name)
                                    existing_ids.append(int(pk_id))

                        if existing_ids:
                            self.next_free_id = max(existing_ids) + 1

                self.master_weapons = found_weapons
                self.master_paints = sorted(list(set(found_paints)))
                self.master_collections = found_colls

                self.search_weapon.delete(0, tk.END)
                self.search_paint.delete(0, tk.END)
                self.search_coll.delete(0, tk.END)
                
                self.filter_weapons()
                self.filter_paints()
                self.filter_collections()
               
                
                self.entry_id.delete(0, tk.END)
                self.entry_id.insert(0, str(self.next_free_id))
                    
                self.log(f"[Scan Master] File mapping successfully completed.")
                self.log(f"[Scan Master] Found {len(self.master_weapons)} clean weapons, {len(self.master_paints)} paint kits, and {len(self.master_collections)} collections.")
                self.log(f"[Auto-ID Engine] Safe unique paint kit slot index found: {self.next_free_id}")
                
            except Exception as e:
                self.log(f"[-] Structural parsing routine aborted: {e}")
                messagebox.showerror("Error", f"Failed to map file structure: {e}")

    def inject_block_before_end(self, content, section_name, block_text, start_pos=0):
        start_idx = content.find(f'"{section_name}"', start_pos)
        if start_idx == -1: return content
            
        open_brace = content.find('{', start_idx)
        brace_count = 1
        current_idx = open_brace + 1
        while brace_count > 0 and current_idx < len(content):
            if content[current_idx] == '{': brace_count += 1
            elif content[current_idx] == '}': 
                brace_count -= 1
                if brace_count == 0:
                    line_start = content.rfind('\n', 0, current_idx)
                    if line_start != -1:
                        brace_indent = content[line_start+1:current_idx]
                        formatted_block = ""
                        for line in block_text.split('\n'):
                            if not line.strip():
                                if line == block_text.split('\n')[-1]: continue
                                formatted_block += '\n'
                                continue
                            internal_tabs = len(line) - len(line.lstrip('\t'))
                            line_indent = brace_indent + '\t' + ('\t' * internal_tabs)
                            formatted_block += line_indent + line.lstrip('\t ') + '\n'
                        return content[:line_start+1] + formatted_block + content[line_start+1:]
                    else:
                        return content[:current_idx] + block_text + content[current_idx:]
            current_idx += 1
        return content

    def create_collection(self):
        if not self.file_path:
            messagebox.showerror("Error", "Load your items_game.txt profile on the first tab first!")
            return

        coll_name = self.entry_coll_name.get().strip()
        if not coll_name:
            messagebox.showwarning("Warning", "Collection text field can't be blank!")
            return
        if not coll_name.startswith("set_"):
            messagebox.showwarning("Style Guide Check", "Valve technical collection names MUST start with 'set_' prefix token!")
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if f'"{coll_name}"' in content:
                messagebox.showerror("Conflict", f"Node '{coll_name}' already exists in this schema configuration file!")
                return

            new_coll_node = (
                f'"{coll_name}"\n'
                f'{{\n'
                f'\t"name"\t\t"#CSGO_{coll_name}"\n'
                f'\t"set_description"\t\t"#CSGO_{coll_name}_desc"\n'
                f'\t"is_collection"\t\t"1"\n'
                f'\t"items"\n'
                f'\t{{\n'
                f'\t}}\n'
                f'}}'
            )

            with open(self.file_path + ".bak", "w", encoding="utf-8") as fb:
                fb.write(content)

            self.log(f"[*] Splicing new empty item_set tree for: {coll_name}")
            content = self.inject_block_before_end(content, "item_sets", new_coll_node)

            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(content)

            self.master_collections.append(coll_name)
            self.master_collections = sorted(list(set(self.master_collections)))
            
            self.search_coll.delete(0, tk.END)
            self.filter_collections()
            
            messagebox.showinfo("Success", f"Collection schema block for '{coll_name}' generated successfully!")
            self.entry_coll_name.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Write Failure", f"Collection compiler runtime failure: {e}")

    def inject_skin_to_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please link active configuration schema files first!")
            return

        weapon = self.combo_weapon.get()
        paint_texture = self.combo_paint.get()
        collection = self.combo_coll.get()
        is_custom_mode = self.check_custom.get() == 1
        
        chosen_rarity_display = self.combo_rarity.get()
        chosen_rarity_token = self.rarity_map.get(chosen_rarity_display, "legendary")

        if weapon == "No matches" or paint_texture == "No matches" or collection == "No matches":
            messagebox.showwarning("Warning", "Invalid selection! Filter terms returned no targets.")
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()

            with open(self.file_path + ".bak", "w", encoding="utf-8") as fb:
                fb.write(content)

            if is_custom_mode:
                skin_id = self.entry_id.get().strip()
                skin_name = self.entry_skin_name.get().strip()
                if not skin_id or not skin_name:
                    messagebox.showwarning("Warning", "Custom configuration modes dictate providing an active Unique Name and targeted Skin ID!")
                    return
                
                match = re.search(r'"name"\s+"' + re.escape(paint_texture) + r'"', content)
                if match:
                    pos = match.start()
                    open_brace_pos = content.rfind('{', 0, pos)
                    close_brace_pos = content.find('}', pos)
                    
                    if open_brace_pos != -1 and close_brace_pos != -1:
                        body = content[open_brace_pos+1:close_brace_pos]
                        body = re.sub(r'"name"\s+"[^"]+"', f'"name" "{skin_name}"', body)
                        body = re.sub(r'"description_string"\s+"[^"]+"', f'"description_string" "#PaintKit_{skin_name}"', body)
                        
                        paint_kit_block = f'"{skin_id}"\n{{\n{body.strip()}\n}}'
                        self.log(f"[*] Copying graphics parameters of skin node '{paint_texture}' directly into new ID: {skin_id} ('{skin_name}')")
                    else:
                        raise Exception("Failed to boundary-slice original visual property dictionaries.")
                else:
                    raise Exception(f"Visual asset core profile reference tracking targets failed locating: '{paint_texture}'")

                content = self.inject_block_before_end(content, "paint_kits", paint_kit_block)
                target_loot_name = skin_name
            else:
                self.log(f"[*] Default Mode active. Directly mapping native valve asset key index link: '{paint_texture}'")
                target_loot_name = paint_texture

            self.log(f"[*] Attaching color parameters tier index '{chosen_rarity_display}' -> target: '{target_loot_name}'")
            rarity_line = f'"{target_loot_name}"\t\t"{chosen_rarity_token}"'
            content = self.inject_block_before_end(content, "paint_kits_rarity", rarity_line)

            item_sets_pos = content.find('"item_sets"')
            if item_sets_pos != -1 and collection in content:
                coll_pos = content.find(f'"{collection}"', item_sets_pos)
                if coll_pos != -1:
                    item_line = f'"[{target_loot_name}]{weapon}"\t\t"1"'
                    content = self.inject_block_before_end(content, "items", item_line, start_pos=coll_pos)
                    self.log(f"[+] Hooked data tracking entry paths directly inside collection item data array: {collection}")
                else:
                    self.log(f"[-] Critical Error: Targeted collection set definition boundary map missing: '{collection}'")

            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(content)

            self.log("[Success] Config parameters successfully committed down on disk storage files!")
            messagebox.showinfo("Success", f"Operation successfully executed! Rarity color tier set to '{chosen_rarity_display}'.")

            if is_custom_mode:
                next_id = int(skin_id) + 1
                self.entry_id.delete(0, tk.END)
                self.entry_id.insert(0, str(next_id))

        except Exception as e:
            self.log(f"[-] Fatal Exception tracked during injection thread operations: {e}")
            messagebox.showerror("Execution Aborted", str(e))

if __name__ == "__main__":
    app = ItemsGameEditor()
    app.mainloop()