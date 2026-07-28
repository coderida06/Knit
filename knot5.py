import customtkinter as ctk
import random
import json
import math

def show_knot5(app, show_menu):
    # Clear previous page widgets
    for widget in app.winfo_children():
        widget.destroy()

    # Configure root app background
    app.configure(fg_color="#efcfe3")

    # --------------------------------------------------
    # GLOBAL STATE & DATA
    # --------------------------------------------------
    selected_tiles = []
    solved_groups = []
    lives = 5
    max_lives = 5
    tiles = []
    
    PUZZLE = []
    COLOR_LOOKUP = {}
    words_data = []

    # --------------------------------------------------
    # WIDGET & LAYOUT SETUP
    # --------------------------------------------------
    yarn_canvas = ctk.CTkCanvas(app, bg="#efcfe3", highlightthickness=0)
    yarn_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Top Frame Header
    top_frame = ctk.CTkFrame(app, fg_color="transparent", height=80)
    top_frame.pack(side="top", fill="x", pady=(15, 0))

    back_button = ctk.CTkButton(
        top_frame,
        text="← Back",
        font=("Segoe UI Semibold", 15),
        width=80,
        height=36,
        corner_radius=14,
        fg_color="#FFF8FB",
        hover_color="#F7DDE8",
        text_color="#444444",
        border_width=2,
        border_color="#E7B5C8",
        command=show_menu
    )
    back_button.pack(side="left", padx=20)

    header_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
    header_frame.pack(expand=True)

    hint_button = ctk.CTkButton(
        header_frame,
        text="💡 Hint",
        font=("Segoe UI Semibold", 15),
        width=90,
        height=36,
        corner_radius=14,
        fg_color="#FFF8FB",
        hover_color="#F7DDE8",
        text_color="#444444",
        border_width=2,
        border_color="#E7B5C8",
        command=lambda: give_hint()
    )
    hint_button.pack(side="left", padx=20)

    lives_container = ctk.CTkFrame(header_frame, fg_color="transparent")
    lives_container.pack(side="left", padx=20)

    # Main Game Area
    game_frame = ctk.CTkFrame(app, fg_color="transparent")
    game_frame.pack(side="top", fill="both", expand=True)

    game_content = ctk.CTkFrame(game_frame, fg_color="transparent")
    game_content.pack(expand=True)

    cards_container = ctk.CTkFrame(game_content, fg_color="transparent")
    cards_container.pack(side="top", pady=(0, 4))

    grid_container = ctk.CTkFrame(game_content, fg_color="transparent")
    grid_container.pack(side="top")

    # --------------------------------------------------
    # YARN DRAWING ENGINE
    # --------------------------------------------------
    def redraw_yarn_threads(snap_effect=False):
        yarn_canvas.delete("yarn")
        
        if len(selected_tiles) < 2 or snap_effect:
            return

        coords = []
        for tile in selected_tiles:
            x = tile.winfo_rootx() - app.winfo_rootx() + (tile.winfo_width() / 2)
            y = tile.winfo_rooty() - app.winfo_rooty() + (tile.winfo_height() / 2)
            coords.append((x, y))

        for i in range(len(coords) - 1):
            x1, y1 = coords[i]
            x2, y2 = coords[i + 1]

            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = x2 - x1, y2 - y1
            dist = math.hypot(dx, dy)
            if dist == 0:
                continue

            ctrl_x = mid_x - (dy / dist) * 18
            ctrl_y = mid_y + (dx / dist) * 18

            points = []
            steps = 16
            for t in range(steps + 1):
                t_val = t / steps
                px = (1 - t_val)**2 * x1 + 2 * (1 - t_val) * t_val * ctrl_x + t_val**2 * x2
                py = (1 - t_val)**2 * y1 + 2 * (1 - t_val) * t_val * ctrl_y + t_val**2 * x2
                py += math.sin(t_val * math.pi * 2) * 2
                points.extend([px, py])

            yarn_canvas.create_line(points, fill="#e27396", width=5, smooth=True, capstyle="round", tags="yarn")
            yarn_canvas.create_line(points, fill="#f7b2bd", width=2, smooth=True, capstyle="round", tags="yarn")

    # --------------------------------------------------
    # BOARD LAYOUT MANAGEMENT
    # --------------------------------------------------
    def create_solved_card(group_id):
        info = COLOR_LOOKUP[group_id]
        words_str = " • ".join(info["words"])
        
        card = ctk.CTkFrame(
            cards_container,
            width=580,
            height=46,
            corner_radius=12,
            fg_color=info["color"],
            border_width=2,
            border_color=info["border"]
        )
        card.pack_propagate(False)
        card.pack(side="top", pady=2)
        
        cat_lbl = ctk.CTkLabel(
            card,
            text=info["connection"].upper(),
            font=("Segoe UI Bold", 11),
            text_color=info["text_color"]
        )
        cat_lbl.pack(side="top", pady=(3, 0))
        
        words_lbl = ctk.CTkLabel(
            card,
            text=words_str,
            font=("Segoe UI Semibold", 10),
            text_color=info["text_color"]
        )
        words_lbl.pack(side="top")

    def update_grid_positions():
        """Renders active unsolved tiles in a dynamic 5x5 grid."""
        unsolved = [t for t in tiles if not t.is_solved]
        
        for tile in tiles:
            tile.grid_forget()
            
        for index, tile in enumerate(unsolved):
            row = index // 5
            col = index % 5
            tile.grid(row=row, column=col, padx=3, pady=3)
            
        app.after(60, redraw_yarn_threads)

    # --------------------------------------------------
    # GAME LOGIC
    # --------------------------------------------------
    def check_group():
        nonlocal lives
        group_ids = {tile.group_id for tile in selected_tiles}

        if len(group_ids) == 1:
            group_id = list(group_ids)[0]
            solved_groups.append(group_id)
            
            for tile in selected_tiles:
                tile.is_solved = True
                tile.grid_forget()
                
            selected_tiles.clear()
            yarn_canvas.delete("yarn")
            
            create_solved_card(group_id)
            update_grid_positions()
            
            if len(solved_groups) == len(PUZZLE):
                app.after(400, trigger_win_animation)
                
        else:
            current_selection = list(selected_tiles)
            selected_tiles.clear()
            
            redraw_yarn_threads(snap_effect=True)
            
            for tile in current_selection:
                tile.configure(fg_color="#E57373", text_color="white", border_color="#D32F2F")
                
            def reset_tiles():
                for tile in current_selection:
                    tile.selected = False
                    tile.configure(fg_color="#FFF8FB", text_color="#444444", border_color="#E7B5C8")
                yarn_canvas.delete("yarn")
                    
            app.after(300, reset_tiles)
            
            lives -= 1
            update_lives_display()
            
            if lives <= 0:
                app.after(350, reveal_answers_and_show_game_over)

    def reveal_answers_and_show_game_over():
        """Reveals all remaining unsolved categories on the board and shows the game over overlay."""
        # Reveal all remaining groups
        for group in PUZZLE:
            if group["id"] not in solved_groups:
                solved_groups.append(group["id"])
                create_solved_card(group["id"])

        # Mark all tiles as solved and hide them
        for tile in tiles:
            tile.is_solved = True
            tile.grid_forget()

        yarn_canvas.delete("yarn")
        update_grid_positions()
        show_game_over()

    def update_lives_display():
        for child in lives_container.winfo_children():
            child.destroy()
        
        for i in range(max_lives):
            color = "#e27396" if i < lives else "#d4b2c7"
            lbl = ctk.CTkLabel(
                lives_container, 
                text="♥", 
                font=("Arial Rounded MT Bold", 26), 
                text_color=color
            )
            lbl.pack(side="left", padx=2)

    # --------------------------------------------------
    # SMART HINT SYSTEM
    # --------------------------------------------------
    def give_hint():
        unsolved = [t for t in tiles if not t.is_solved]
        if not unsolved:
            return

        target_tiles = []

        if 1 <= len(selected_tiles) <= 4:
            selected_group = selected_tiles[0].group_id
            if all(t.group_id == selected_group for t in selected_tiles):
                unselected_partners = [t for t in unsolved if t.group_id == selected_group and t not in selected_tiles]
                if unselected_partners:
                    target_tiles.append(random.choice(unselected_partners))

        if not target_tiles:
            remaining_groups = list({t.group_id for t in unsolved})
            chosen_group = random.choice(remaining_groups)
            group_members = [t for t in unsolved if t.group_id == chosen_group]
            target_tiles = random.sample(group_members, min(2, len(group_members)))

        for tile in target_tiles:
            tile.configure(fg_color="#FFF59D", border_color="#FBC02D")

        def restore_hint():
            for tile in target_tiles:
                if not tile.is_solved and not tile.selected:
                    tile.configure(fg_color="#FFF8FB", border_color="#E7B5C8")

        app.after(1800, restore_hint)

    # --------------------------------------------------
    # WIN ANIMATION & OVERLAYS
    # --------------------------------------------------
    def trigger_win_animation():
        w = app.winfo_width()
        h = app.winfo_height()
        steps = 25

        def animate_stitch(step=0):
            if step <= steps:
                x_end = (w / steps) * step
                yarn_canvas.delete("win_stitch")
                yarn_canvas.create_line(0, h/2, x_end, h/2, fill="#e27396", width=8, smooth=True, tags="win_stitch")
                yarn_canvas.create_line(0, h/2, x_end, h/2, fill="#f7b2bd", width=3, smooth=True, tags="win_stitch")
                app.after(15, lambda: animate_stitch(step + 1))
            else:
                app.after(300, show_win_overlay)

        animate_stitch()

    def show_win_overlay():
        overlay = ctk.CTkFrame(app, fg_color="#efcfe3", corner_radius=0)
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        content = ctk.CTkFrame(overlay, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        cat_lbl = ctk.CTkLabel(content, text="🧶\n✨ Puzzle Complete! ✨", font=("Segoe UI Bold", 36), text_color="#523a73")
        cat_lbl.pack(pady=20)
        
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=10)

        next_puzzle_btn = ctk.CTkButton(
            btn_frame,
            text="Next Puzzle →",
            font=("Segoe UI Semibold", 18),
            width=180,
            height=48,
            corner_radius=16,
            fg_color="#e27396",
            hover_color="#d96a92",
            text_color="white",
            command=load_new_puzzle
        )
        next_puzzle_btn.pack(side="left", padx=10)

        menu_btn = ctk.CTkButton(
            btn_frame,
            text="Menu",
            font=("Segoe UI Semibold", 18),
            width=120,
            height=48,
            corner_radius=16,
            fg_color="#FFF8FB",
            hover_color="#F7DDE8",
            text_color="#444444",
            border_width=2,
            border_color="#E7B5C8",
            command=show_menu
        )
        menu_btn.pack(side="left", padx=10)

    def show_game_over():
        overlay = ctk.CTkFrame(app, fg_color="#efcfe3", corner_radius=0)
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        content = ctk.CTkFrame(overlay, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        lbl = ctk.CTkLabel(content, text="GAME OVER", font=("Segoe UI Bold", 42), text_color="#D32F2F")
        lbl.pack(pady=10)

        sub_lbl = ctk.CTkLabel(content, text="All correct categories have been revealed above!", font=("Segoe UI Semibold", 14), text_color="#523a73")
        sub_lbl.pack(pady=(0, 20))
        
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=10)

        restart_btn = ctk.CTkButton(
            btn_frame,
            text="Try Again",
            font=("Segoe UI Semibold", 18),
            width=140,
            height=48,
            corner_radius=16,
            fg_color="#e27396",
            hover_color="#d96a92",
            text_color="white",
            command=reset_game
        )
        restart_btn.pack(side="left", padx=8)

        show_answers_btn = ctk.CTkButton(
            btn_frame,
            text="View Answers",
            font=("Segoe UI Semibold", 18),
            width=140,
            height=48,
            corner_radius=16,
            fg_color="#FFF8FB",
            hover_color="#F7DDE8",
            text_color="#444444",
            border_width=2,
            border_color="#E7B5C8",
            command=lambda: overlay.destroy()  # Dismisses overlay so player can inspect the revealed cards
        )
        show_answers_btn.pack(side="left", padx=8)

        menu_btn = ctk.CTkButton(
            btn_frame,
            text="Menu",
            font=("Segoe UI Semibold", 18),
            width=120,
            height=48,
            corner_radius=16,
            fg_color="#FFF8FB",
            hover_color="#F7DDE8",
            text_color="#444444",
            border_width=2,
            border_color="#E7B5C8",
            command=show_menu
        )
        menu_btn.pack(side="left", padx=8)

    def reset_game():
        nonlocal lives, tiles, words_data
        
        lives = max_lives
        selected_tiles.clear()
        solved_groups.clear()
        
        for child in app.winfo_children():
            if isinstance(child, ctk.CTkFrame) and child not in (top_frame, game_frame, yarn_canvas):
                child.destroy()
        
        for child in cards_container.winfo_children():
            child.destroy()
        for child in grid_container.winfo_children():
            child.destroy()

        yarn_canvas.delete("all")
        
        random.shuffle(words_data)
        tiles = [WordTile(grid_container, item["word"], item["group_id"]) for item in words_data]
        
        update_lives_display()
        update_grid_positions()

    # --------------------------------------------------
    # WORD TILE COMPONENT
    # --------------------------------------------------
    class WordTile(ctk.CTkButton):
        def __init__(self, master, word, group_id):
            super().__init__(
                master,
                text=word,
                width=110,
                height=68,
                corner_radius=14,
                fg_color="#FFF8FB",
                hover_color="#F7DDE8",
                text_color="#444444",
                border_width=2,
                border_color="#E7B5C8",
                font=("Segoe UI Semibold", 13),
                command=self.clicked
            )
            self.selected = False
            self.is_solved = False
            self.group_id = group_id

        def clicked(self):
            if self.is_solved:
                return

            if self.selected:
                self.selected = False
                selected_tiles.remove(self)
                self.configure(fg_color="#FFF8FB", text_color="#444444", border_color="#E7B5C8")
            else:
                if len(selected_tiles) == 5:
                    return
                self.selected = True
                selected_tiles.append(self)
                self.configure(fg_color="#E684A5", text_color="white", border_color="#D96A92")

            redraw_yarn_threads()

            if len(selected_tiles) == 5:
                check_group()

    # --------------------------------------------------
    # NEXT PUZZLE LOGIC (In-Memory Reset)
    # --------------------------------------------------
    def load_new_puzzle():
        """Generates a clean 5-category x 5-word puzzle."""
        nonlocal lives, tiles, words_data, PUZZLE, COLOR_LOOKUP, selected_tiles, solved_groups

        lives = max_lives
        selected_tiles.clear()
        solved_groups.clear()

        for child in app.winfo_children():
            if isinstance(child, ctk.CTkFrame) and child not in (top_frame, game_frame, yarn_canvas):
                child.destroy()
        
        for child in cards_container.winfo_children():
            child.destroy()
        for child in grid_container.winfo_children():
            child.destroy()
        
        yarn_canvas.delete("all")

        with open("categories.json", "r", encoding="utf-8") as f:
            all_categories = json.load(f)

        valid_categories = [cat for cat in all_categories if len(cat.get("words", [])) >= 5]
        
        if len(valid_categories) < 5:
            raise ValueError("categories.json must contain at least 5 categories with 5 or more words each.")

        selected_cats = random.sample(valid_categories, 5)

        PALETTE = [
            {"color": "#FFE3B3", "border": "#F4C97A", "text_color": "#6A4D13"},
            {"color": "#d8f1c6", "border": "#b8dba2", "text_color": "#334f24"},
            {"color": "#d9c5f5", "border": "#b9a2dc", "text_color": "#3c2957"},
            {"color": "#ccecf2", "border": "#a8d6de", "text_color": "#20464d"},
            {"color": "#ffd6cc", "border": "#fca895", "text_color": "#5e2318"}
        ]

        PUZZLE = []
        for i, category in enumerate(selected_cats):
            chosen_words = random.sample(category["words"], 5)
                
            PUZZLE.append({
                "id": i + 1,
                "connection": category["connection"],
                "words": chosen_words,
                **PALETTE[i]
            })

        COLOR_LOOKUP = {group["id"]: group for group in PUZZLE}

        words_data = []
        for group in PUZZLE:
            for word in group["words"]:
                words_data.append({
                    "word": word,
                    "group_id": group["id"],
                    "connection": group["connection"]
                })

        random.shuffle(words_data)

        tiles = [WordTile(grid_container, item["word"], item["group_id"]) for item in words_data]

        update_lives_display()
        update_grid_positions()

    # Initialize game
    load_new_puzzle()

    def finish_startup():
        app.update_idletasks()
        update_grid_positions()
        update_lives_display()

    app.after(250, finish_startup)
