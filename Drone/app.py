from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import time
from typing import Optional, Tuple

app = Flask(__name__)

class AgriculturalDrone:
    def __init__(self):
        self.battery_level: int = 100
        self.position: Tuple[int, int] = (0, 0)
        self.task: Optional[str] = None
        self.module: Optional[str] = None

    def navigate_to(self, x: int, y: int):
        print(f"Navigating to position ({x}, {y})...")
        self.position = (x, y)
        time.sleep(2)
        print("Arrived at position.")

    def perform_task(self):
        if self.task == 'plowing':
            self.plow()
        elif self.task == 'seeding':
            self.seed()
        elif self.task == 'harvesting':
            self.harvest()

    def plow(self):
        print("Plowing the field...")
        time.sleep(5)
        print("Plowing completed.")
        self.battery_level -= 20

    def seed(self):
        print("Seeding the field...")
        time.sleep(5)
        print("Seeding completed.")
        self.battery_level -= 20

    def harvest(self):
        print("Harvesting the crops...")
        time.sleep(5)
        print("Harvesting completed.")
        self.battery_level -= 20

    def return_to_base(self):
        print("Returning to base for charging...")
        self.navigate_to(0, 0)
        self.charge_battery()

    def charge_battery(self):
        print("Charging battery...")
        while self.battery_level < 100:
            self.battery_level += 10
            time.sleep(1)
            print(f"Battery level: {self.battery_level}%")
        print("Battery fully charged.")

    def check_battery(self):
        if self.battery_level < 30:
            self.return_to_base()
        else:
            self.perform_task()

    def decide_task_based_on_coordinates(self, x: int, y: int):
        if 0 <= x < 50 and 0 <= y < 50:
            self.task = 'plowing'
        elif 50 <= x < 100 and 0 <= y < 50:
            self.task = 'seeding'
        elif 0 <= x < 50 and 50 <= y < 100:
            self.task = 'harvesting'
        else:
            self.task = 'plowing'  # Default task if coordinates don't match specific areas
        print(f"Decided task {self.task} based on coordinates ({x}, {y})")
        self.check_battery()

    def move_manual(self, direction: str):
        x, y = self.position
        if direction == 'up':
            y -= 1
        elif direction == 'down':
            y += 1
        elif direction == 'left':
            x -= 1
        elif direction == 'right':
            x += 1
        self.position = (x, y)
        print(f"Moved {direction}. New position: {self.position}")

drone = AgriculturalDrone()

@app.route('/')
def index():
    return render_template('index.html', battery_level=drone.battery_level, position=drone.position)

@app.route('/navigate', methods=['POST'])
def navigate():
    x = int(request.form['x'])
    y = int(request.form['y'])
    drone.navigate_to(x, y)
    drone.decide_task_based_on_coordinates(x, y)
    return redirect(url_for('index'))

@app.route('/task', methods=['POST'])
def task():
    task = request.form['task']
    drone.task = task
    drone.check_battery()
    return redirect(url_for('index'))

@app.route('/position', methods=['GET'])
def position():
    return jsonify(x=drone.position[0], y=drone.position[1])

@app.route('/move_manual', methods=['POST'])
def move_manual():
    direction = request.form['direction']
    drone.move_manual(direction)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
