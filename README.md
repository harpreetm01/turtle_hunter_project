# 🐢 Turtle Hunter - ROS2 Project

This is a simple **ROS 2 project** where the main turtle (`turtle1`) hunts down other randomly spawned turtles inside the `turtlesim` simulation. By default, `turtle1` hunts the closest turtle first (`catch_closest_turtle_first = True`), but this behavior can be changed to make it catch turtles in the order they spawn. Once caught, the turtle disappears, and the process continues indefinitely.

## 🚀 Features

- **Random Turtle Spawning**: New turtles appear at random locations.
- **Automatic Hunting**: `turtle1` moves towards the nearest spawned turtle.
- **Catching Mechanism**: Once `turtle1` reaches a turtle, it gets removed.
- **Adjustable Parameters**: Modify spawn rate and hunting behavior.
- **Easy to Run**: Everything is launched using a single command.

## 🛠 How It Works

- `turtle_spawner` node generates new turtles at random positions.
- `turtle_controller` node makes `turtle1` move towards the closest turtle.
- When `turtle1` reaches a target, `turtle_controller` sends a request to `turtle_spawner`, which then calls the `/kill` service to remove the caught turtle.
- The process repeats, continuously spawning and catching turtles.

## 📌 ROS 2 Concepts Used

### **Nodes**

- `turtle_spawner`: Spawns turtles and kills them after receiving a request.
- `turtle_controller`: Moves `turtle1` to catch turtles and sends a request after reaching a target.

### **Topics**

- `/spawned_turtles`: Publishes the list of active turtles.
- `/turtle1/pose`: Monitors `turtle1`'s position.
- `/turtle1/cmd_vel`: Sends movement commands to `turtle1`.

### **Services**

- `/spawn`: Creates new turtles.
- `/kill`: Removes turtles when caught.
- `catch_turtle`: Custom service that gets called when `turtle1` reaches a target turtle, triggering its removal.

### **Parameters**

- `spawn_rate`: Controls how often turtles spawn.
- `turtle_name_prefix`: Sets the naming pattern for new turtles.
- `catch_closest_turtle_first`: Determines whether `turtle1` prioritizes the nearest turtle or catches them in order of spawning.

## 🔧 Installation & Setup

### **1. Clone the Repository**

```sh
git clone https://github.com/harpreetm01/turtle_hunter_project.git
```

### **2. Move the Project to Your ROS 2 Workspace**

```sh
mv turtle_hunter_project ~/ros2_ws/src/turtle_hunter
```

### **3. Build the Package**

```sh
cd ~/ros2_ws
colcon build --packages-select turtle_hunter
```

### **4. Source the Environment**

```sh
source install/setup.bash
```

## 🚀 Running the Project

To start the simulation, run:

```sh
ros2 launch turtle_hunter_bringup turtle_hunter.launch.py
```

## 📌 Future Improvements

- Improve movement to make it look smoother.
- Add different behaviors for spawned turtles.
- Experiment with smarter path planning.

🔧 **Feel free to explore the code and tweak the parameters to change how the turtle hunts!** 🏹🐢

