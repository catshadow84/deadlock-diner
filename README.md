🍽️ Deadlock Diner — Banker's Algorithm Visualizer
A full-stack web application that visualizes the Banker's Algorithm for deadlock detection and avoidance in operating systems. Built with Python (Flask) and vanilla HTML/CSS/JavaScript.
📋 Project Description
Deadlock Diner is an interactive teaching tool that demonstrates how modern operating systems prevent deadlocks using the Banker's Algorithm (Dijkstra, 1965). Users input system state matrices (Available resources, Maximum Demand, Current Allocation), and the application:
Calculates the Need Matrix (Need = Max - Allocation)
Simulates the Safety Algorithm step-by-step
Determines whether the system is in a Safe State or Deadlock
If safe, displays the Safe Sequence of process execution
Animates each decision with real-time visual feedback
The project includes three pre-loaded textbook examples (Safe, Unsafe, Deadlock) for instant demonstration.
Key Features
✅ Full implementation of Banker's Algorithm with step-by-step logging
✅ Dynamic matrix input with preservation of existing values
✅ Animated execution visualization (PASS / WAIT / DEADLOCK states)
✅ Safe Sequence display with arrow-chain visualization
✅ Resource Allocation Graph API endpoint (ready for SVG extension)
✅ Dark-mode diner aesthetic with responsive design
✅ Client-side validation (Allocation ≤ Max)
🛠️ Requirements
Dependencies
Table
Tool	Version	Purpose
Python	3.8+	Backend server & algorithm engine
Flask	2.0+	Web framework (micro)
Installation
bash
Copy
pip install flask
No database, no external APIs, no build tools required.
🚀 Step-by-Step Instructions
1. Clone the Repository
bash
Copy
git clone <repository-url>
cd deadlock-diner
2. Install Dependencies
bash
Copy
pip install flask
3. Project Structure
Ensure your folder looks like this:
plain
Copy
deadlock-diner/
├── app.py
├── README.md
└── templates/
    └── index.html
4. Run the Application
bash
Copy
python app.py
You should see:
plain
Copy
 * Running on http://127.0.0.1:5000
5. Open in Browser
Navigate to:
plain
Copy
http://127.0.0.1:5000
6. Using the Application
Load an Example: Select "Safe State Example" from the dropdown (auto-fills matrices)
Or Input Custom Data:
Set Number of Processes and Resource Types
Click Generate Matrices
Fill in Maximum Demand, Allocation, and Available vectors
Click Run Analysis
Watch the animated step-by-step execution
Observe the result: Safe Sequence (green) or Deadlock Alert (red)
📁 API Endpoints
Table
Endpoint	Method	Description
/	GET	Serves the main application page
/api/examples	GET	Returns list of pre-loaded examples
/api/example/<id>	GET	Returns specific example data
/api/analyze	POST	Runs Banker's Algorithm, returns steps & result
/api/resource-graph	POST	Returns Resource Allocation Graph nodes/edges
Sample API Request
bash
Copy
curl -X POST http://127.0.0.1:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "available": [3, 3, 2],
    "max_demand": [[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]],
    "allocation": [[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]
  }'
🎓 Algorithm Reference
Banker's Algorithm (Safety Check):
Let Work = Available, Finish = [false, ..., false]
Find a process Pi such that Finish[i] == false and Need[i] <= Work
If found: Work = Work + Allocation[i], Finish[i] = true, goto step 2
If no such process exists and Finish contains false → Deadlock
If all Finish == true → Safe State, execution order is the Safe Sequence
Time Complexity: O(m × n²) where m = resource types, n = processes
👤 Author: Mohammad Amin Al-Hajj
Course: Data Structures and Algorithms Lab
Instructor: Prof. Hassan Tfaily
Tech Stack: Python (Flask), HTML5, CSS3, JavaScript (ES6+)
📝 Notes
The application runs entirely offline after pip install flask
No database or external services required
Responsive design works on desktop and mobile browsers
All animations are CSS-based for smooth performance
This README was written using generative AI, with content prompted by programmer. Moreover, example matrices of different states and debugging were also provided by generative AI.
