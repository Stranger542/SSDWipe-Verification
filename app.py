import os
from flask import Flask, jsonify
from flask_cors import CORS
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
PORT = os.getenv("PORT", 5001)
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
# This is the full, up-to-date ABI for your smart contract
CONTRACT_ABI = [
  {
    "inputs": [ { "internalType": "address", "name": "initialOwner", "type": "address" } ],
    "stateMutability": "nonpayable", "type": "constructor"
  },
  {
    "anonymous": False,
    "inputs": [
      { "indexed": True, "internalType": "string", "name": "serialNumber", "type": "string" },
      { "indexed": False, "internalType": "string", "name": "certificateId", "type": "string" },
      { "indexed": True, "internalType": "address", "name": "minter", "type": "address" }
    ],
    "name": "CertificateStored", "type": "event"
  },
  {
    "inputs": [ { "internalType": "string", "name": "_serialNumber", "type": "string" } ],
    "name": "getCertificateData",
    "outputs": [
      {
        "components": [
          { "internalType": "string", "name": "deviceType", "type": "string" },
          { "internalType": "string", "name": "model", "type": "string" },
          { "internalType": "string", "name": "serialNumber", "type": "string" },
          { "internalType": "uint64", "name": "capacityBytes", "type": "uint64" },
          { "internalType": "string", "name": "wipeMethod", "type": "string" },
          { "internalType": "string", "name": "startTime", "type": "string" },
          { "internalType": "string", "name": "endTime", "type": "string" },
          { "internalType": "uint32", "name": "durationSeconds", "type": "uint32" },
          { "internalType": "string", "name": "verificationStatus", "type": "string" },
          { "internalType": "string", "name": "operator", "type": "string" },
          { "internalType": "string", "name": "host", "type": "string" },
          { "internalType": "string", "name": "certificateId", "type": "string" },
          { "internalType": "string", "name": "digitalSignature", "type": "string" },
          { "internalType": "uint256", "name": "blockTimestamp", "type": "uint256" },
          { "internalType": "address", "name": "minter", "type": "address" }
        ],
        "internalType": "struct SSDWipeStorage.WipeCertificateData", "name": "", "type": "tuple"
      }
    ],
    "stateMutability": "view", "type": "function"
  }
]


# --- INITIALIZATION ---
app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing
w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

print("✅ Python verifier backend configured.")
print(f"Connection to blockchain node successful: {w3.is_connected()}")


# --- API ENDPOINT ---
@app.route('/verify/<serial_number>', methods=['GET'])
def verify_certificate(serial_number):
    print(f"Received verification request for S/N: {serial_number}")
    try:
        data = contract.functions.getCertificateData(serial_number).call()

        # The serial number is at index 2 in the returned tuple
        if not data or data[2] == "":
            return jsonify({"success": False, "message": "Certificate not found."}), 404

        # Format the data into a clean dictionary
        result = {
            "serialNumber": data[2],
            "model": data[1],
            "wipeMethod": data[4],
            "timestamp": data[13] # blockTimestamp is at index 13
        }
        return jsonify({"success": True, "data": result}), 200

    except Exception as e:
        print(f"Error querying the blockchain: {e}")
        return jsonify({"success": False, "message": "An internal server error occurred."}), 500


if __name__ == '__main__':
    app.run(port=PORT, debug=True)