# Dynamic Flood Fill Pathfinding Bot

This project was inspired by a video from the YouTube channel **Veritasium**:  
👉 https://youtu.be/ZMQbHMgK2rw

The goal of this project is to design a **pathfinding algorithm that starts with an empty map**, explores its environment, and progressively builds its own knowledge of the world while navigating.

The pathfinder:
- Only detects walls within a **one-block distance**
- Updates its internal map while moving
- Recalculates the shortest path dynamically
- Uses a **Flood Fill–based algorithm**

During the exploration process, **wall cells have a value of `-1`**.

---

## 🧠 Core Concept

Unlike traditional pathfinding algorithms that rely on a fully known map, this project simulates a more realistic scenario where:
- The environment is initially unknown
- The agent discovers obstacles as it moves
- The shortest path is constantly recomputed based on new information

---

## 🛠️ Technologies Used

- **Python**
- **Pygame** (for visualization)
- Flood Fill algorithm
- DFS (for maze generation)
- Experimental multiprocessing (not functional yet)

---

## 🎮 Controls (Pygame versions)

- **Left Click**
  - First click: Start node (🟧 orange)
  - Second click: End node (🟦 cyan)
  - Next clicks: Walls (⬛ black)
- **Right Click**: Remove a node
- **SPACE**: Launch the pathfinder
- **C**: Clear the map
- **N**: Generate a new map
- **G**: Generate a maze (DFS) (from level code 7)
- **S**: Skip maze generation and exploration (from level code 11)
- **ESC**: Quit the program

---

## 📂 Project Files Overview

### Early Algorithm & Console Versions

- **`flood_fill_01.py`**  
  Base implementation of the **Flood Fill algorithm**.  
  Displays a map showing distances from the destination.

- **`flood_fill_02.py`**  
  Displays the updated map and the path update process.

- **`flood_fill_03.py`**  
  Similar to version 02, but only displays the map and the pathfinder position.

- **`flood_fill_04.py`**  
  Code refactoring with improved structure and comments.

---

### 🖥️ Pygame Visualization Versions

- **`flood_fill_05_(bot).py`**  
  First graphical version using Pygame.

- **`flood_fill_06_(bot).py`**  
  Adds round trips. If no map update occurs, the shortest path is confirmed.

- **`flood_fill_07_(bot_+_maze).py`**  
  Adds maze generation using a DFS algorithm with multiple openings.

- **`flood_fill_08_(bot_+_maze).py`**  
  The bot leaves a green trail behind while moving.

---

### 🪟 Dual-Screen & Debug Versions

- **`flood_fill_09_(maze_+_db_screen).py`**  
  Window split into two:
  - Left: Real map
  - Right: Bot’s internal map and predicted path

- **`flood_fill_10_(maze_+_db_screen).py`**  
  Discovered walls are displayed on the right screen.

- **`flood_fill_11_(maze_+_db_screen).py`**  
  Press **S** to skip maze generation and exploration.

- **`flood_fill_12_(maze_+_db_screen).py`**  
  The bot recalculates and displays the shortest path **at every move**.

- **`flood_fill_13_(db_screen_+_graphic).py`**  
  Displays a comparison between:
  - Initial map (no wall discovery)
  - Final updated map

---

### 🤖 Multi-Bot Experiments

- **`flood_fill_14_(maze_+_pair_bot).py`**  
  Two bots cooperate to find the path.

- **`flood_fill_14_(maze_+_pair_bot)+.py`**  
  Attempt to use multiprocessing (❌ not working).

- **`flood_fill_15_(maze_+_pair_bot).py`**  
  Displays the current shortest path with a pink line.

- **`flood_fill_16_(maze_+_multi_pair_bot).py`**  
  Multiple bot pairs launched with a delay.

---

### ⚡ Performance & Speed Testing

- **`flood_fill_17_(multi_pair_bot_+_speed).py`**  
  Bots are not rendered to improve performance.  
  Displays total computation time.

- **`flood_fill_17_(multi_pair_bot_+_speed)+.py`**  
  Multiprocessing attempt (❌ not working).

- **`flood_fill_18_(multi_pair_bot_+_speed).py`**  
  User chooses how many bots are used.

- **`flood_fill_19_(bot_+_speed).py`**  
  Single bot version for performance comparison.

- **`flood_fill_20_(bot_+_speed).py`**  
  Loop optimization.

- **`flood_fill_21_(bot_+_speed).py`**  
  Bot has full knowledge of walls (no exploration, algorithm only).

---

## 🚀 Future Improvements

- Fix multiprocessing implementation
- Optimize performance for large maps
- Add agent communication strategies
- Export metrics and statistics
- Improve code modularity

---

## 📜 License

This project is for **educational and experimental purposes**.

