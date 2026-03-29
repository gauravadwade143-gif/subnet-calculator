from flask import Flask, render_template, request, jsonify
import ipaddress

app = Flask(__name__)

def get_ip_class(ip):
    first_octet = int(str(ip).split('.')[0])
    if 1 <= first_octet <= 126: return "A"
    elif 128 <= first_octet <= 191: return "B"
    elif 192 <= first_octet <= 223: return "C"
    return "Other/Special"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    ip_input = data.get("ip")
    try:
        net = ipaddress.IPv4Network(ip_input, strict=False)
        
        # Helper to get binary with dots every 8 bits
        def to_bin_dots(ip_int):
            b = f'{ip_int:032b}'
            return f"{b[0:8]}.{b[8:16]}.{b[16:24]}.{b[24:32]}"

        results = {
            "network": str(net.network_address),
            "broadcast": str(net.broadcast_address),
            "mask": str(net.netmask),
            "total_hosts": net.num_addresses,
            "cidr": net.prefixlen,
            "ip_class": get_ip_class(net.network_address),
            "bin_net": to_bin_dots(int(net.network_address)),
            "bin_mask": to_bin_dots(int(net.netmask))
        }
        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)