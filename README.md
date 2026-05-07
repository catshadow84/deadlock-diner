# 🍽️ Deadlock Diner — Banker's Algorithm Visualizer

A full-stack web application that visualizes the **Banker's Algorithm** for deadlock detection and avoidance. Built with Python (Flask) and vanilla HTML/CSS/JavaScript for the **Data Structures and Algorithms Lab** course.

---

## 📋 Project Description

Deadlock Diner is an interactive teaching tool that demonstrates how the **Banker's Algorithm** (Dijkstra, 1965) detects and prevents deadlocks in operating systems. Users input system state matrices (Available resources, Maximum Demand, Current Allocation), and the application:

1. Calculates the **Need Matrix** (`Need = Max - Allocation`)
2. Simulates the **Safety Algorithm** step-by-step
3. Determines whether the system is in a **Safe State** or **Deadlock**
4. If safe, displays the **Safe Sequence** of process execution
5. Animates each decision with real-time visual feedback

The project includes three pre-loaded textbook examples (Safe, Unsafe, Deadlock) for instant demonstration.

### Key Features
- ✅ Full implementation of Banker's Algorithm with step-by-step logging
- ✅ Dynamic matrix input with preservation of existing values
- ✅ Animated execution visualization (PASS / WAIT / DEADLOCK states)
- ✅ Safe Sequence display with arrow-chain visualization
- ✅ Resource Allocation Graph API endpoint (ready for SVG extension)
- ✅ Dark-mode diner aesthetic with responsive design
- ✅ Client-side validation (Allocation ≤ Max)

---

## 🛠️ Requirements

### Dependencies
| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.8+ | Backend server & algorithm engine |
| Flask | 2.0+ | Web framework (micro) |

### Installation
```bash
pip install flask
```

No database, no external APIs, no build tools required.

---

## 🚀 Step-by-Step Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd deadlock-diner
```

### 2. Install Dependencies
```bash
pip install flask
```

### 3. Project Structure
Ensure your folder looks like this:
```
deadlock-diner/
├── app.py
├── README.md
└── templates/
    └── index.html
```

### 4. Run the Application
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### 5. Open in Browser
Navigate to:
```
http://127.0.0.1:5000
```

### 6. Using the Application
1. **Load an Example**: Select "Safe State Example" from the dropdown (auto-fills matrices)
2. **Or Input Custom Data**:
   - Set Number of Processes and Resource Types
   - Click **Generate Matrices**
   - Fill in Maximum Demand, Allocation, and Available vectors
3. **Click Run Analysis**
4. **Watch** the animated step-by-step execution
5. **Observe** the result: Safe Sequence (green) or Deadlock Alert (red)

---

## 📁 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves the main application page |
| `/api/examples` | GET | Returns list of pre-loaded examples |
| `/api/example/<id>` | GET | Returns specific example data |
| `/api/analyze` | POST | Runs Banker's Algorithm, returns steps & result |
| `/api/resource-graph` | POST | Returns Resource Allocation Graph nodes/edges |

### Sample API Request
```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "available": [3, 3, 2],
    "max_demand": [[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]],
    "allocation": [[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]
  }'
```

---

## 🎓 Algorithm Reference

**Banker's Algorithm** (Safety Check):
1. Let `Work` = `Available`, `Finish` = [false, ..., false]
2. Find a process `Pi` such that `Finish[i] == false` and `Need[i] <= Work`
3. If found: `Work = Work + Allocation[i]`, `Finish[i] = true`, goto step 2
4. If no such process exists and `Finish` contains false → **Deadlock**
5. If all `Finish == true` → **Safe State**, execution order is the **Safe Sequence**

**Time Complexity**: O(m × n²) where m = resource types, n = processes

---

## 👤 Author

- **Name**: Mohammad Amin Al-Hajj
- **Course**: Data Structures and Algorithms Lab
- **Instructor**: Prof. Hassan Tfaily
- **Tech Stack**: Python (Flask), HTML5, CSS3, JavaScript (ES6+)

---

## 🙏 Acknowledgments

- **Generative AI**: Portions of this project, including code structure, documentation, and debugging assistance, were developed with the help of generative AI tools.
- **Example State Matrices**: The pre-loaded example matrices (Safe State, Unsafe State, and Deadlock scenarios) were provided as reference implementations for testing and demonstration purposes.
- **Debugging Support**: Debugging assistance was received during the development process to resolve syntax errors, logic issues, and algorithm correctness.

---

## 📝 Notes

- The application runs entirely offline after `pip install flask`
- No database or external services required
- Responsive design works on desktop and mobile browsers
- All animations are CSS-based for smooth performance
