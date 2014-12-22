import control
import signal
import sys
from flask import Flask
from flask import jsonify
app = Flask(__name__)

@app.route("/pin/<int:logicalPin>", methods=["GET"])
def activate_pin(logicalPin):
    control.activate(logicalPin)
    return jsonify(pin = logicalPin, state = 1)

def signal_handler(signal, frame):
    print "Cleaning up."
    control.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    control.init_pins()
    signal.signal(signal.SIGINT, signal_handler)
    app.run(debug=True,host="0.0.0.0",port=80)
