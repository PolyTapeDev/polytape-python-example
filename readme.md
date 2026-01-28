# 📊 PolyTape Python Example

A high-fidelity Python client and example suite for the **PolyTape Prediction Market Data API**. This repository demonstrates how to bridge the gap between Polymarket's web interface and professional-grade quant data by resolving parent events into specific tradable asset ID.

---

## 🌟 Highlights

* **Slug-to-Asset Resolution**: Automatically convert Polymarket URLs into machine-readable CLOB Token IDs for individual outcomes.
* **High-Fidelity Orderbooks**: Fetch Central Limit Order Book (CLOB) snapshots with millisecond precision.
* **Trade Simulation**: Calculate the exact price impact and liquidity for market buy ($USD) and sell (Shares) orders.
* **Local Data Persistence**: Saves raw and processed API responses to `.json` files for backtesting and historical analysis.

---

## 🔍 Walkthrough: Finding Asset IDs

Polymarket uses a hierarchical structure where one **Event** (the overall question) can contain many **Markets** (the specific outcomes). To use the PolyTape API, you need the unique `asset_id` for the specific outcome you want to track.

### 1. Identify the Event Slug

Navigate to an event on the Polymarket website. For example:
`https://polymarket.com/event/democratic-presidential-nominee-2028`

The **Event Slug** is the unique identifier at the end of the URL: `democratic-presidential-nominee-2028`.

### 2. Resolve the Slug with the Fetch Script

Your script `Fetch_assetId_from_event_slug.py` acts as a bridge. It queries the Polymarket Gamma API for that slug and displays every tradeable market within that event.

```bash
# Run the resolver script to see all markets for this event
python Fetch_assetId_from_event_slug.py

```

### 3. Extract the Asset ID (CLOB Token ID)

In the generated JSON output or terminal logs, locate your target. Each market has a `clobTokenIds` field, which is an array of IDs corresponding to the available outcomes.

* **Binary Markets (YES/NO)**:
* **Index 0**: The **"Yes"** Token ID.
* **Index 1**: The **"No"** Token ID.


* **Sports & Multi-Outcome Markets**: Outcomes are mapped 1:1 with the `outcomes` array (e.g., `["Team A", "Team B"]` or `["Candidate X", "Candidate Y", "Candidate Z"]`).

**Example Configuration:**
Once you have the correct ID, paste it into the `TARGET_ASSET` object in `Polytape_api_example.py`:

```python
{
    "question": "Will another person win the 2028 Democratic presidential nomination?",
    "outcome_type": "Yes",
    "asset_id": "56276407178137464106155902677779647430650342076032000643690644026940603132442",
    "condition_id": "0x20280a56684e9e9b18dd81e1dc2c10433b7b08913ba03aa5bbd481f6e4f2f754"
  },

```

---

## 📁 Repository Structure

* `Polytape_api_example.py`: Main client for fetching L2 orderbooks and running trade simulations.
* `Fetch_assetId_from_event_slug.py`: Automated utility to resolve event slugs and map outcomes.
* `data_samples/`: Directory where API responses (Orderbooks/Simulations) are stored as JSON.
* `sample_event_slug_to_asset_id_data.json`: Static sample showing the resolved structure of a Polymarket event.

---

## 🚀 Getting Started

### 1. Installation

```bash
git clone https://github.com/PolyTapeDev/polytape-python-example.git
cd polytape-python-example
pip install requests

```

### 2. Configuration

Open `Polytape_api_example.py` and update the `API_URL` to your live endpoint:

```python
API_URL = "https://api.polytape.xyz" 
API_KEY = "your_api_key_here"

```

### 3. Execution

Run the example to fetch a live orderbook and perform trade simulations:

```bash
python Polytape_api_example.py

```

---

## 🤝 Contributing

Feel free to fork this repository or open an issue for new simulation logic (e.g., slippage analysis or VWAP calculations).

## 📄 License

MIT License