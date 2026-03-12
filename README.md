# Magic: The Gathering Card Viewer

A simple web application built with **FastHTML** designed for learning FastHTML, focusing on form handling, data
fetching, API integration, and responsive UI design.

## Project Overview

This project works around the use of the **FastHTML** framework to build a fully functional card viewer for Magic:
The Gathering. It connects to the official Scryfall API to fetch card data and provides a clean, responsive user
interface.

## Installation

### Prerequisites

Ensure you have a working virtual environment set up. You can use either `pip` or `uv` (recommended for modern
projects).

### Using `uv` (Recommended)

```bash
# Install the application and dependencies (if not already installed)
uv venv

# Source binaries
uv sync

uv run main.py
```

### Using `pip`

```bash
python3 -m venv .venv

# Source binaries
source .venv/bin/activate

# Install the application and dependencies
pip install -r requirements.txt

# Run the development server
python3 main.py
```

> **Note**: If you installed the dependencies manually using `pip` and the project files were cloned, you can simply run `python3 main.py` without a virtual environment.

## Project Structure

The codebase is structured to demonstrate key web development concepts:

- **Backend Framework**: FastHTML
- **Data Fetching**: Scryfall API via `requests`
- **Data Validation**: Pydantic models (`BaseModel`)
- **Routing**: FastHTML Router (`@rt`)
- **UI Components**: Monster UI Tailwind Library.

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Lilithbtw/MTG_Wrapper.git
   cd MTG_Wrapper
   ```

2. Start the application:
   ```bash
    uv venv

    source .venv/bin/activate

    uv pip install -r requirements.txt
    uv run main.py
   ```

3. Open your browser and navigate to `http://localhost:5555` to see the application.

## Features

- **Search Functionality**: Enter a card name to search the Scryfall database.
- **Real-time Data**: Fetches card information including name, image, mana cost, type, and rarity.
- **Responsive Design**: Adapts to different screen sizes using Flexbox and Grid.
- **User Feedback**: Handles errors gracefully and provides user-friendly messages.

## Technology Stack

- **Backend**: FastHTML (Python framework)
- **API**: Scryfall API (https://api.scryfall.com/cards)
- **UI Components**: FastHTML Components, Pydantic Models
- **Routing**: FastHTML Router
- **Dependencies**: FastHTML, Pydantic, MonsterUI, Requests
