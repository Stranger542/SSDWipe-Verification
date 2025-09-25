# SSD Wipe Certificate Verifier

This project provides a web-based interface and backend API to verify SSD data wipe certificates stored on the blockchain.

## Features

- **Frontend:** Simple UI to enter a device serial number and view certificate details.
- **Backend:** Python Flask API connects to an Ethereum smart contract to fetch certificate data.
- **Blockchain Integration:** Uses Web3 to query certificate data from a deployed smart contract.

## Project Structure

- [`index.html`](index.html): Main web page UI.
- [`script.js`](script.js): Frontend logic for verification and UI state management.
- [`app.py`](app.py): Flask backend server and blockchain query logic.
- [`requirements.txt`](requirements.txt): Python dependencies.
- [`.env`](.env): Environment variables (RPC URL, contract address, etc.).
- [`.gitignore`](.gitignore): Files and folders to ignore in git.

## Setup

### Prerequisites

- Python 3.8+
- Node.js (optional, for frontend development)
- An Ethereum node endpoint (e.g., Infura)

### Installation

1. **Clone the repository**  
   ```sh
   git clone <your-repo-url>
   cd SDataWipe Verify
   ```

2. **Install Python dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure environment variables**  
   Edit the [`.env`](.env) file with your RPC URL and contract address.

4. **Run the backend server**  
   ```sh
   python app.py
   ```
   The server will start on port `5001` by default.

5. **Open the frontend**  
   Open [`index.html`](index.html) in your browser.

## Usage

1. Enter the device serial number in the input field.
2. Click **Verify**.
3. The app will display certificate details if found, or an error if not.

## Notes

- The backend queries an Ethereum smart contract using the ABI defined in [`app.py`](app.py).
- Make sure your RPC URL and contract address are correct in [`.env`](.env).
- Cross-Origin Resource Sharing (CORS) is enabled for local development.

## License

MIT License
