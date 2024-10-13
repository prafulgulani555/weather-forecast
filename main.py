import subprocess
import sys
import os
import streamlit as st
import plotly.express as px
from backend import get_data


def create_virtualenv():
    # Check if virtualenv is already installed, otherwise install it
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "virtualenv"])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install virtualenv: {e}")
        sys.exit(1)

    # Create the virtual environment
    venv_dir = None
    if os.path.exists(".venv"):
        venv_dir = ".venv"
        print("Found .venv folder.")
    elif os.path.exists("venv"):
        venv_dir = "venv"
        print("Found venv folder.")
    else:
        # Create the virtual environment if none exists
        venv_dir = ".venv"  # Default to .venv for new environments
        print(f"Creating virtual environment in {venv_dir}...")
        subprocess.check_call([sys.executable, "-m", "virtualenv", venv_dir])

    return venv_dir


def install_requirements(venv_dir):
    # Activate virtual environment and install dependencies inside it
    if os.name == "nt":  # Windows
        activate_script = os.path.join(venv_dir, "Scripts", "activate")
    else:  # macOS/Linux
        activate_script = os.path.join(venv_dir, "bin", "activate")

    # Install packages in the virtual environment
    print(f"Installing dependencies in the {venv_dir} virtual environment...")
    try:
        subprocess.check_call(f"{activate_script} && pip install -r requirements.txt", shell=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while trying to install dependencies: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Create a virtual environment
    venv = create_virtualenv()

    # Install dependencies
    install_requirements(venv)

    # Step 3: Proceed with your program logic
    print("All dependencies installed in virtual environment. Running the main program...")

    # frontend of webpage
    st.title("Weather Forecast for the Next Days")
    place = st.text_input("Place: ")
    days = st.slider("Forecast Days", min_value=1, max_value=5,
                     help="Select the number of forecast days")
    option = st.selectbox("Select data to view",
                          ("Temperature", "Sky"))
    st.subheader(f"{option} for the next {days} days in {place}")

    if place:
        try:
            filtered_data = get_data(place, days)

            if option == "Temperature":
                temperatures = [dict["main"]["temp"] / 10 for dict in filtered_data]
                dates = [dict["dt_txt"] for dict in filtered_data]
                figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (C"})
                st.plotly_chart(figure)

            if option == "Sky":
                images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                          "Rain": "images/rain.png", "Snow": "images/snow.png"}
                sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
                image_paths = [images[condition] for condition in sky_conditions]
                st.image(image_paths, width=115)
        except:
            st.error("Place doesn't exist.")
