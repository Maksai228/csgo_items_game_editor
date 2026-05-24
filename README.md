# csgo_items_game_editor
PY program, can create collections and new skins. Only for CS:GO from 2023

# SOURCE-NET Config Injector

An automation utility designed for safely editing and injecting structured blocks into nested configuration files (`items_game.txt`). This tool streamlines array management, hierarchy validation, and structural injection for developers working with custom data environments.

The utility establishes a direct relationship between asset collections and parent deployment bundles. By mapping the items directly to the targeted set, it bypasses redundant structural layers, ensuring optimal layout rendering within the UI rendering engine and preventing indexing or fallback display bugs.

---

## Requirements

* Python 3.x
* No external dependencies required (built entirely using the standard Tkinter graphical library).

---

## Usage Guide

### Step 1: File Selection
1. Launch the application from your terminal: `python main.py`
2. Navigate to the first tab labeled **1. File**.
3. Click **Select File** and target your configuration file. The application will validate the file structure and maintain the path lock for subsequent operations.

### Step 2: Asset Definition Injection
1. Navigate to the second tab labeled **2. Inject Skins**.
2. Input the technical identifier of the custom modification in the **Target Loot Name** field.
3. Specify the base weapon class system in the **Weapon** field.
4. Input the destination group identifier in the **Collection Name** field.
5. Click **Inject Skin** to append the entry directly into the specified data block.

---
