from flask import Flask, request, jsonify
import os
import threading

# Clear the terminal screen automatically
os.system('cls')  # Use 'clear' instead if on Linux/Mac

app = Flask(__name__)

# In-memory storage for testing purpose
sensor_data = []
data =[]

def clear_screen():
    while True:
        cmd = input()
        if cmd.strip().lower() == 'c':
            os.system('cls' if os.name == 'nt' else 'clear')

# Start a background thread to listen for "c"
threading.Thread(target=clear_screen, daemon=True).start()

# ---------------- HTTP root ----------------
@app.route('/')
def home():
    return "Hello! Flask Server is Running 🚀"

# ---------------- HTTP GET ----------------
@app.route('/update', methods=['GET'])
def update_get():
    temp = request.args.get('temp')
    hum = request.args.get('hum')

    if temp is None or hum is None:
        return jsonify({"status": "error", "message": "Missing temp or hum"}), 400

    # Save data to memory
    data = {"temp": temp, "hum": hum}
    sensor_data.append(data)

    print(f"Received via GET: {data}")
    
    return jsonify({"status": "ok", "message": "Data stored", "data": data})

# ---------------- HTTP POST ----------------
@app.route('/update', methods=['POST'])
def update_post():
    content = request.json

    if not content or 'temp' not in content or 'hum' not in content:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    # Save data to memory
    sensor_data.append(content)

    print(f"Received via POST: {content}")
    return jsonify({"status": "ok", "message": "Data stored", "data": content})

# ---------------- Display Stored Data ----------------
@app.route('/data', methods=['GET'])
def get_all_data():
    return jsonify(sensor_data,data)


@app.route('/saiadmin/saivdata/', methods=['POST'])
def saiadmin_saivdata():
    data = request.get_json(force=True)
    sensor_data.clear()
    sensor_data.append(data)

    print(f"Received at /saiadmin/saivdata/: {data}")
    return jsonify({"status": "ok", "path": "/saiadmin/saivdata/"}), 200


@app.route('/api/sensor-data', methods=['POST'])
def api_sensor_data():
    data = request.get_json(force=True)
    sensor_data.append(data)

    print(f"Received at /api/sensor-data: {data}")
    return jsonify({"status": "ok", "path": "/api/sensor-data"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
