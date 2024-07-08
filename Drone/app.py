from flask import Flask, render_template, request, redirect, url_for
import time

app = Flask(__name__)

class AgriculturalDrone:
    def __init__(self):
        self.battery_level = 100
        self.position = (0, 0)
        self.task = None
        self.module = None

    def navigate_to(self, x, y):
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

drone = AgriculturalDrone()

@app.route('/')
def index():
    return render_template('index.html', battery_level=drone.battery_level, position=drone.position)

@app.route('/navigate', methods=['POST'])
def navigate():
    x = int(request.form['x'])
    y = int(request.form['y'])
    drone.navigate_to(x, y)
    return redirect(url_for('index'))

@app.route('/task', methods=['POST'])
def task():
    task = request.form['task']
    drone.task = task
    drone.check_battery()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
